"""Ruby 版 tecsgen を実行し、Python 版との比較に使う正解データを採取する。

WSL（Linux）上で実行することを前提とする。標準ライブラリだけで動く。

    python3 tools/golden/generate_golden.py --source <tecsgen のブランチ> --out tests/golden

各ケースについて、テストツリーの作業コピーを毎回作り直してから Ruby 版を実行し、
次のものを <out>/cases/<id>/ に保存する。

- stdout.txt / stderr.txt : 標準出力・標準エラー出力
- files/                  : 実行によって作られた、または変更されたファイル（test/ からの相対パス）
- meta.json               : 引数・終了コード・エラー/警告件数・保存しなかったファイルのハッシュなど

作業ディレクトリとソースの絶対パスは、出力の中で @WORK@・@SOURCE@ に置き換える。
"""

from __future__ import annotations

import argparse
import fnmatch
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cases.toml"
DEFAULT_WORK = Path("/tmp/tecsgen-golden-work")
# mruby のヘッダ。collect_kernel.py のカーネルのリポジトリと同じ作業コピー群にある
DEFAULT_MRUBY_INCLUDE = (
    Path.home() / "repo/svn-toppers-TECS-2/svn/toppers/mruby/mruby-master/include"
)

# 保存しないファイル（ハッシュとサイズだけを meta.json に記録する）
#   *.rbdmp  : Ruby の Marshal 形式の内部モデルダンプ。Python 版では再現しない
#   tmp_*.h  : import_C で C プリプロセッサが出力したヘッダ。サイズが大きく、中身は cpp に依存する
EXCLUDED_PATTERNS = ["*.rbdmp", "tmp_*.h"]

SUMMARY_RE = re.compile(
    rb"^(?:(?P<err>\d+) errors?)?\s*(?:(?P<warn>\d+) warnings?)?\s*$", re.MULTILINE
)


def sha256(data: bytes) -> str:
    return hashlib.sha256(data).hexdigest()


def snapshot(root: Path) -> dict[str, str]:
    """root 以下の全ファイルについて、相対パス → sha256 の対応を返す。"""
    result: dict[str, str] = {}
    for path in root.rglob("*"):
        if path.is_file():
            result[path.relative_to(root).as_posix()] = sha256(path.read_bytes())
    return result


def is_excluded(rel_path: str) -> bool:
    name = rel_path.rsplit("/", 1)[-1]
    return any(fnmatch.fnmatch(name, pattern) for pattern in EXCLUDED_PATTERNS)


def parse_counts(output: bytes) -> tuple[int, int] | None:
    """tecsgen が最後に出す "N errors  M warnings" の行から件数を取り出す。"""
    counts = None
    for match in SUMMARY_RE.finditer(output):
        if match.group("err") or match.group("warn"):
            counts = (int(match.group("err") or 0), int(match.group("warn") or 0))
    return counts


def command_version(cmd: list[str]) -> str:
    try:
        proc = subprocess.run(cmd, capture_output=True, check=False)
    except FileNotFoundError:
        return "(not found)"
    # tecsgen --version は標準エラー出力に書く
    out = proc.stdout or proc.stderr
    return out.decode(errors="replace").splitlines()[0].strip() if out else ""


def prepare_pristine(
    source: Path, pristine: Path, mruby_include: Path | None = None
) -> None:
    """テストツリーと tecsgen/tecs を、移植元と同じ相対配置で作業ディレクトリへ写す。

    mruby_include があれば、mruby のヘッダを ext/mruby/include へ写す（ケースの引数の
    {MRUBY_INCLUDE}）。移植元の test/mruby は MRUBYPATH の mruby 本体を前提にしているが、
    tecsgen の実行に要るのはヘッダだけ。
    """
    if pristine.exists():
        shutil.rmtree(pristine)
    shutil.copytree(source / "test", pristine / "test", symlinks=True)
    shutil.copytree(
        source / "tecsgen" / "tecs", pristine / "tecsgen" / "tecs", symlinks=True
    )
    if mruby_include is not None:
        shutil.copytree(
            mruby_include, pristine / "ext" / "mruby" / "include", symlinks=True
        )


def place_inputs(cases: list[dict], pristine: Path) -> None:
    """ケースの inputs（tools/golden/inputs/<名前>/ の *.cdl・*.rb）を、cwd へ写す。

    実プロジェクトのテストに無い経路を動かす合成入力。実行前から在るファイルとして扱う
    （pristine に置くので、生成物には数えない）。*.rb は `-L .` で読ませる利用者プラグイン。
    cwd が test/ に無ければ作る。base があれば、先に test/<base> を cwd へ丸ごと写してから重ねる
    （既存ケースのプラグインを差し替えた変種。pristine は全ケースで共有するので、test/<base>
    そのものを上書きすると元のケースが変わってしまう）。
    """
    for case in cases:
        if "inputs" not in case:
            continue
        dest = pristine / "test" / case["cwd"]
        if "base" in case:
            shutil.copytree(pristine / "test" / case["base"], dest, symlinks=True)
        dest.mkdir(parents=True, exist_ok=True)
        src_dir = HERE / "inputs" / case["inputs"]
        for src in sorted([*src_dir.glob("*.cdl"), *src_dir.glob("*.rb")]):
            shutil.copyfile(src, dest / src.name)


class Normalizer:
    def __init__(self, work: Path, source: Path) -> None:
        # 長いパスから先に置き換える
        pairs = [(str(work), b"@WORK@"), (str(source), b"@SOURCE@")]
        self._pairs = sorted(
            ((p.encode(), r) for p, r in pairs), key=lambda x: -len(x[0])
        )

    def __call__(self, data: bytes) -> bytes:
        for path, replacement in self._pairs:
            data = data.replace(path, replacement)
        return data


def run_case(
    case: dict,
    *,
    defaults: dict,
    source: Path,
    pristine: Path,
    pristine_hashes: dict[str, str],
    run_root: Path,
    out_dir: Path,
    ruby: str,
    timeout: int,
    normalize: Normalizer,
) -> dict:
    if run_root.exists():
        shutil.rmtree(run_root)
    shutil.copytree(pristine, run_root, symlinks=True)

    tecspath = run_root / "tecsgen" / "tecs"
    mruby_include = run_root / "ext" / "mruby" / "include"
    args = [
        a.replace("{TECSPATH}", str(tecspath)).replace(
            "{MRUBY_INCLUDE}", str(mruby_include)
        )
        for a in case["args"]
    ]
    env = dict(os.environ)
    env.update(defaults.get("env", {}))
    env.update(case.get("env", {}))
    env["TECSPATH"] = str(tecspath)
    cwd = run_root / "test" / case["cwd"]
    cmd = [ruby, str(source / "tecsgen" / "tecsgen.rb"), *args]

    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout, check=False
        )
        exit_code: int | None = proc.returncode
        stdout, stderr = proc.stdout, proc.stderr
        timed_out = False
    except subprocess.TimeoutExpired as exc:
        exit_code, timed_out = None, True
        stdout, stderr = exc.stdout or b"", exc.stderr or b""

    after = snapshot(run_root / "test")
    created = sorted(p for p in after if p not in pristine_hashes)
    modified = sorted(
        p for p in after if p in pristine_hashes and after[p] != pristine_hashes[p]
    )
    deleted = sorted(p for p in pristine_hashes if p not in after)

    case_dir = out_dir / "cases" / case["id"]
    if case_dir.exists():
        shutil.rmtree(case_dir)
    files_dir = case_dir / "files"
    files_dir.mkdir(parents=True)

    excluded: dict[str, dict] = {}
    for rel in created + modified:
        data = (run_root / "test" / rel).read_bytes()
        if is_excluded(rel):
            excluded[rel] = {"sha256": sha256(data), "size": len(data)}
            continue
        dest = files_dir / rel
        dest.parent.mkdir(parents=True, exist_ok=True)
        dest.write_bytes(normalize(data))

    stdout, stderr = normalize(stdout), normalize(stderr)
    (case_dir / "stdout.txt").write_bytes(stdout)
    (case_dir / "stderr.txt").write_bytes(stderr)

    counts = parse_counts(stdout + b"\n" + stderr)
    expect = case.get("expect")
    meta = {
        "id": case["id"],
        "source": case.get("source", ""),
        "cwd": case["cwd"],
        "args": case["args"],
        "env": {**defaults.get("env", {}), **case.get("env", {})},
        "exit_code": exit_code,
        "timed_out": timed_out,
        "errors": counts[0] if counts else 0,
        "warnings": counts[1] if counts else 0,
        "expect": expect,
        "expect_matched": None
        if expect is None
        else (counts or (0, 0)) == tuple(expect),
        "created": created,
        "modified": modified,
        "deleted": deleted,
        "excluded": excluded,
    }
    (case_dir / "meta.json").write_text(
        json.dumps(meta, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    return meta


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument(
        "--source",
        type=Path,
        required=True,
        help="tecsgen のブランチ（test/ と tecsgen/ を含む）",
    )
    parser.add_argument("--out", type=Path, required=True, help="正解データの出力先")
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--work",
        type=Path,
        default=DEFAULT_WORK,
        help="作業ディレクトリ（毎回作り直す）",
    )
    parser.add_argument(
        "--source-label",
        default="",
        help="ソースの出所（SVN リビジョンなど）。environment.json に記録する",
    )
    parser.add_argument(
        "--mruby-include",
        type=Path,
        default=DEFAULT_MRUBY_INCLUDE,
        help="mruby のヘッダのディレクトリ（ケースの引数の {MRUBY_INCLUDE}）。"
        "既に在れば作業ディレクトリへ写す",
    )
    parser.add_argument("--ruby", default="ruby")
    parser.add_argument(
        "--timeout", type=int, default=300, help="1ケースあたりの制限時間（秒）"
    )
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="対象ケースの id（glob 可、複数指定可）",
    )
    parser.add_argument(
        "--exclude",
        action="append",
        default=[],
        help="採取しないケースの id（glob 可、複数指定可）。出力先にある既存の正解データは消さずに残す"
        "（移植元に無いプラグインを使うため再採取できないケース用）",
    )
    opts = parser.parse_args(argv)

    source = opts.source.resolve()
    work = opts.work.resolve()
    out_dir = opts.out.resolve()
    manifest = tomllib.loads(opts.manifest.read_text(encoding="utf-8"))
    defaults = manifest.get("defaults", {})
    cases = manifest["case"]

    ids = [c["id"] for c in cases]
    duplicates = sorted({i for i in ids if ids.count(i) > 1})
    if duplicates:
        print(f"duplicate case id: {duplicates}", file=sys.stderr)
        return 2

    if opts.case:
        cases = [
            c for c in cases if any(fnmatch.fnmatch(c["id"], p) for p in opts.case)
        ]
    if opts.exclude:
        cases = [
            c
            for c in cases
            if not any(fnmatch.fnmatch(c["id"], p) for p in opts.exclude)
        ]
    if not opts.case and (out_dir / "cases").exists():
        if opts.exclude:
            # 除外したケースの既存の正解データを残すため、採取するケースだけを消す
            for c in cases:
                shutil.rmtree(out_dir / "cases" / c["id"], ignore_errors=True)
        else:
            shutil.rmtree(out_dir / "cases")

    pristine = work / "pristine"
    needs_mruby = any("{MRUBY_INCLUDE}" in a for c in cases for a in c["args"])
    if needs_mruby and not opts.mruby_include.is_dir():
        print(f"mruby include not found: {opts.mruby_include}", file=sys.stderr)
        return 2
    prepare_pristine(
        source, pristine, opts.mruby_include if opts.mruby_include.is_dir() else None
    )
    place_inputs(cases, pristine)
    pristine_hashes = snapshot(pristine / "test")
    normalize = Normalizer(work / "run", source)

    results = []
    for case in cases:
        if case.get("skip"):
            print(f"SKIP  {case['id']}: {case['skip']}")
            continue
        meta = run_case(
            case,
            defaults=defaults,
            source=source,
            pristine=pristine,
            pristine_hashes=pristine_hashes,
            run_root=work / "run",
            out_dir=out_dir,
            ruby=opts.ruby,
            timeout=opts.timeout,
            normalize=normalize,
        )
        results.append(meta)
        mark = {None: "", True: "  expect=OK", False: "  expect=MISMATCH"}[
            meta["expect_matched"]
        ]
        print(
            f"{'TIMEOUT' if meta['timed_out'] else 'exit=' + str(meta['exit_code']):8} "
            f"{case['id']:45} err={meta['errors']:<3} warn={meta['warnings']:<3} "
            f"files={len(meta['created']) + len(meta['modified'])}{mark}"
        )

    # 一部のケースだけ採り直した場合も、マニフェストのハッシュとケース数を最新にする
    environment = {
        "ruby": command_version([opts.ruby, "--version"]),
        "gcc": command_version(["gcc", "--version"]),
        "tecsgen": command_version(
            [opts.ruby, str(source / "tecsgen" / "tecsgen.rb"), "--version"]
        ),
        "platform": command_version(["uname", "-srm"]),
        "source": opts.source_label,
        "manifest_sha256": sha256(opts.manifest.read_bytes()),
        "excluded_patterns": EXCLUDED_PATTERNS,
        "cases": len(list((out_dir / "cases").rglob("meta.json"))),
    }
    (out_dir / "environment.json").write_text(
        json.dumps(environment, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    mismatched = [m["id"] for m in results if m["expect_matched"] is False]
    timed_out = [m["id"] for m in results if m["timed_out"]]
    print(
        f"\n{len(results)} cases, expect mismatched: {mismatched or 'none'}, timed out: {timed_out or 'none'}"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
