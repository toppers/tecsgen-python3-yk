"""カーネル依存プラグイン（HRP・FMP など）の正解データを採取する。

WSL（Linux）上で実行することを前提とする。標準ライブラリだけで動く。

    python3 tools/golden/collect_kernel.py \\
        --repos-root ~/repo/svn-toppers-TECS-2/svn/toppers \\
        --tecsgen-wc /mnt/e/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033 \\
        --out tests/golden/kernel

`generate_golden.py` は tecsgen の `test/` を対象にするが、こちらは TOPPERS カーネル
（hrp3+tecs・fmp3+tecs など）のアプリケーション CDL を対象にする。ケースごとに、

1. カーネルのリポジトリを `svn export -r BASE --native-eol LF` で書き出す
2. 同梱の tecsgen を、移植元（`--tecsgen-wc`）の tecsgen に差し替える
   （同梱の r3306 は Ruby 3.x で `Proc.new` のエラーになり、移植元と版も揃わない）
3. `obj-golden/` で `configure.rb` を実行して Makefile を作る（`configure` を持つケース）。
   `workdir` を持つケース（ev3rt+tecs）は、リポジトリ内のそのディレクトリをそのまま使う
4. `make -n tecs` で tecsgen の呼び出し行を記録し、`make tecs` を実行する

の順に行い、作業ディレクトリの中に作られたファイルと標準出力・終了コードを保存する。

tecsgen が C プリプロセッサとして呼ぶ `$(CC)` は、ターゲット本来の交差コンパイラ
（`arm-none-eabi-gcc`）をそのまま使う。WSL に `gcc-arm-none-eabi` パッケージが必要。
バージョンは environment.json の `target_gcc` に記録する。
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import os
import shlex
import shutil
import subprocess
import sys
import tomllib
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from generate_golden import (
    EXCLUDED_PATTERNS,
    Normalizer,
    command_version,
    is_excluded,
    parse_counts,
    sha256,
    snapshot,
)

HERE = Path(__file__).resolve().parent
DEFAULT_MANIFEST = HERE / "cases_kernel.toml"
DEFAULT_WORK = Path.home() / "p5kernel"
# make に渡す上書き。無し（ターゲットの Makefile.target が決める CC をそのまま使う）
MAKE_OVERRIDES: list[str] = []
# ケースの target が使う交差コンパイラ。environment.json に版を記録する
TARGET_GCC = "arm-none-eabi-gcc"


def run(cmd: list[str], *, cwd: Path, env: dict[str, str], timeout: int):
    try:
        proc = subprocess.run(
            cmd, cwd=cwd, env=env, capture_output=True, timeout=timeout, check=False
        )
        return proc.returncode, proc.stdout, proc.stderr, False
    except subprocess.TimeoutExpired as exc:
        return None, exc.stdout or b"", exc.stderr or b"", True


def svn_export(src: Path, dest: Path) -> str:
    """作業コピーの BASE を LF で書き出し、そのリビジョン番号を返す。"""
    if dest.exists():
        shutil.rmtree(dest)
    dest.parent.mkdir(parents=True, exist_ok=True)
    subprocess.run(
        [
            "svn",
            "export",
            "-q",
            "-r",
            "BASE",
            "--native-eol",
            "LF",
            str(src),
            str(dest),
        ],
        check=True,
    )
    info = subprocess.run(
        ["svn", "info", "--show-item", "revision", str(src)],
        capture_output=True,
        text=True,
        check=True,
    )
    return info.stdout.strip()


def find_tecsgen_command(make_n_stdout: bytes) -> list[str] | None:
    """`make -n tecs` の出力から、tecsgen の呼び出し行を引数のリストにして返す。

    行末のバックスラッシュで続く行は1行につなぐ。`printf` などの表示用の行は除く。
    """
    text = make_n_stdout.decode(errors="replace").replace("\\\n", " ")
    for raw in text.splitlines():
        if "tecsgen.rb" in raw and not raw.lstrip().startswith("printf"):
            return shlex.split(raw)
    return None


def run_case(
    case: dict,
    *,
    pristine: Path,
    run_root: Path,
    out_dir: Path,
    normalize: Normalizer,
    revisions: dict[str, str],
    timeout: int,
) -> dict:
    if run_root.exists():
        shutil.rmtree(run_root)
    shutil.copytree(pristine / case["repo"], run_root, symlinks=True)
    # workdir を指定したケースは、リポジトリ内に既にあるそのディレクトリで実行する。
    # 指定しないケースは、別名のディレクトリを作って configure.rb を実行する
    # （fmp3+tecs は obj/ を持っているので、obj-golden という別名にする）
    if "workdir" in case:
        obj = run_root / case["workdir"]
        if not obj.is_dir():
            raise RuntimeError(f"{case['id']}: workdir not found: {case['workdir']}")
    else:
        obj = run_root / "obj-golden"
        obj.mkdir()

    env = dict(os.environ)
    env["LANG"] = "C"
    env.update(case.get("env", {}))

    if "configure" in case:
        conf_code, conf_out, conf_err, _ = run(
            ["ruby", "../configure.rb", *case["configure"]],
            cwd=obj,
            env=env,
            timeout=timeout,
        )
        if conf_code != 0:
            raise RuntimeError(
                f"{case['id']}: configure.rb failed ({conf_code})\n"
                f"{conf_out.decode(errors='replace')}\n{conf_err.decode(errors='replace')}"
            )

    if "tecsgen_args" in case:
        # Makefile が無い構成（atk1+tecs）: tecsgen の引数を一覧に直接書き、make を使わない。
        # リポジトリにコミットされている古い生成物が混ざらないよう、clean のディレクトリを消す
        tecsgen_rb = run_root / case.get("tecsgen_dest", "tecsgen") / "tecsgen.rb"
        tecsgen_args = ["ruby", os.path.relpath(tecsgen_rb, obj), *case["tecsgen_args"]]
        for name in case.get("clean", []):
            shutil.rmtree(obj / name, ignore_errors=True)
        before = snapshot(obj)
        exit_code, stdout, stderr, timed_out = run(
            tecsgen_args, cwd=obj, env=env, timeout=timeout
        )
        make_overrides: list[str] = []
    else:
        _, dry_out, _, _ = run(
            ["make", "-n", "tecs", *MAKE_OVERRIDES], cwd=obj, env=env, timeout=timeout
        )
        tecsgen_args = find_tecsgen_command(dry_out)
        before = snapshot(obj)
        exit_code, stdout, stderr, timed_out = run(
            ["make", "tecs", *MAKE_OVERRIDES], cwd=obj, env=env, timeout=timeout
        )
        make_overrides = MAKE_OVERRIDES
    after = snapshot(obj)
    created = sorted(p for p in after if p not in before)
    modified = sorted(p for p in after if p in before and after[p] != before[p])
    deleted = sorted(p for p in before if p not in after)

    case_dir = out_dir / "cases" / case["id"]
    if case_dir.exists():
        shutil.rmtree(case_dir)
    files_dir = case_dir / "files"
    files_dir.mkdir(parents=True)

    excluded: dict[str, dict] = {}
    for rel in created + modified:
        data = (obj / rel).read_bytes()
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
    meta = {
        "id": case["id"],
        "repo": case["repo"],
        "repo_revision": revisions[case["repo"]],
        "target": case["target"],
        "workdir": case.get("workdir"),
        "configure": case.get("configure"),
        "make_overrides": make_overrides,
        "tecsgen_args": tecsgen_args,
        "exit_code": exit_code,
        "timed_out": timed_out,
        "errors": counts[0] if counts else 0,
        "warnings": counts[1] if counts else 0,
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
        "--repos-root",
        type=Path,
        required=True,
        help="<repo>/trunk を持つ SVN 作業コピー群のディレクトリ",
    )
    parser.add_argument(
        "--tecsgen-wc",
        type=Path,
        required=True,
        help="移植元 tecsgen のブランチ（tecsgen/ を含む作業コピー）",
    )
    parser.add_argument("--out", type=Path, required=True)
    parser.add_argument("--manifest", type=Path, default=DEFAULT_MANIFEST)
    parser.add_argument(
        "--work",
        type=Path,
        default=DEFAULT_WORK,
        help="作業ディレクトリ（毎回作り直す。/tmp は WSL 再起動で消える）",
    )
    parser.add_argument("--timeout", type=int, default=600)
    parser.add_argument(
        "--case",
        action="append",
        default=[],
        help="対象ケースの id（glob 可、複数指定可）",
    )
    opts = parser.parse_args(argv)

    manifest = tomllib.loads(opts.manifest.read_text(encoding="utf-8"))
    cases = manifest["case"]
    ids = [c["id"] for c in cases]
    dup = sorted({i for i in ids if ids.count(i) > 1})
    if dup:
        print(f"duplicate case id: {dup}", file=sys.stderr)
        return 2
    out_dir = opts.out.resolve()
    if opts.case:
        cases = [
            c for c in cases if any(fnmatch.fnmatch(c["id"], p) for p in opts.case)
        ]
    elif (out_dir / "cases").exists():
        shutil.rmtree(out_dir / "cases")

    work = opts.work.resolve()
    tecsgen_src = work / "tecsgen-src"
    tecsgen_rev = svn_export(opts.tecsgen_wc / "tecsgen", tecsgen_src)

    pristine = work / "pristine"
    revisions: dict[str, str] = {}
    for repo in sorted({c["repo"] for c in cases}):
        dest = pristine / repo
        revisions[repo] = svn_export(opts.repos_root / repo / "trunk", dest)
        # 同梱の tecsgen（あれば）を移植元のものに差し替える。置き場所はリポジトリごとに違う
        # （既定は tecsgen/。ev3rt+tecs は hr-tecs/tecsgen/tecsgen/）
        rel = next(c.get("tecsgen_dest", "tecsgen") for c in cases if c["repo"] == repo)
        if (dest / rel).exists():
            shutil.rmtree(dest / rel)
        (dest / rel).parent.mkdir(parents=True, exist_ok=True)
        shutil.copytree(tecsgen_src, dest / rel, symlinks=True)

    run_root = work / "run"
    normalize = Normalizer(run_root, tecsgen_src)
    results = []
    for case in cases:
        meta = run_case(
            case,
            pristine=pristine,
            run_root=run_root,
            out_dir=out_dir,
            normalize=normalize,
            revisions=revisions,
            timeout=opts.timeout,
        )
        results.append(meta)
        print(
            f"{'TIMEOUT' if meta['timed_out'] else 'exit=' + str(meta['exit_code']):8} "
            f"{case['id']:40} err={meta['errors']:<3} warn={meta['warnings']:<3} "
            f"files={len(meta['created']) + len(meta['modified'])}"
        )

    env_path = out_dir / "environment.json"
    previous = {}
    if env_path.exists():
        previous = json.loads(env_path.read_text(encoding="utf-8"))
    environment = {
        "ruby": command_version(["ruby", "--version"]),
        "gcc": command_version(["gcc", "--version"]),
        "tecsgen": command_version(
            ["ruby", str(tecsgen_src / "tecsgen.rb"), "--version"]
        ),
        "tecsgen_revision": tecsgen_rev,
        "platform": command_version(["uname", "-srm"]),
        "target_gcc": command_version([TARGET_GCC, "--version"]),
        "repo_revisions": {**previous.get("repo_revisions", {}), **revisions},
        "manifest_sha256": sha256(opts.manifest.read_bytes()),
        "excluded_patterns": EXCLUDED_PATTERNS,
        "cases": len(list((out_dir / "cases").rglob("meta.json"))),
    }
    out_dir.mkdir(parents=True, exist_ok=True)
    env_path.write_text(
        json.dumps(environment, ensure_ascii=False, indent=2) + "\n", encoding="utf-8"
    )
    failed = [m["id"] for m in results if m["exit_code"] != 0]
    print(f"\n{len(results)} cases, non-zero exit: {failed or 'none'}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
