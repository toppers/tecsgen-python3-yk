"""Ruby 版 tecsflow を実行して、差分テストの正解データ（tests/golden/tecsflow/）を採る。

WSL（Linux）で実行する。移植元の tecsgen ディレクトリ（tecsflow.rb がある所）と、
TOPPERS TECS の test/ 一式（SVN trunk の test/）を渡す。

    python3 tools/port/collect_tecsflow_oracle.py <移植元 tecsgen ディレクトリ> <test/ ディレクトリ> [出力先] [--case ID ...]

ケースの定義は tests/golden/tecsflow/cases.toml。ケースごとに、test/ をコピーして
`make tecsflow`（tecsgen → tcflow → tecsflow）を Ruby 版で実行し、`<id>.json.gz` を作る。
入力（tests/golden/tecsflow/inputs/）は `--copy-inputs` で test/ から写し直せる。

記録するもの:
- tecsflow : tecsflow の引数・終了コード・標準出力・標準エラー出力
- funclist : tcflow が書いた tcflow.rbdmp を tests/ruby/tcflow_dump_json.rb で JSON にしたもの

バイト列は latin-1 で復号した文字列にして持つ（Python 版の内部表現と同じ）。
"""

from __future__ import annotations

import argparse
import gzip
import json
import os
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "tests" / "golden" / "tecsflow"
DUMP_JSON = ROOT / "tests" / "ruby" / "tcflow_dump_json.rb"
TIMEOUT = 600
# 入力に写さない（make が作る）ファイル
SKIP_SUFFIXES = (".o", ".exe", ".cde", ".rbdmp")
SKIP_DIRS_PREFIX = ("gen",)

WRAPPER = """#!/bin/sh
exec ruby {src}/{name}.rb "$@"
"""

FLOW_WRAPPER = """#!/bin/sh
echo "$@" > "$OUTDIR/flow.args"
ruby {src}/tecsflow.rb "$@" > "$OUTDIR/flow.out" 2> "$OUTDIR/flow.err"
rc=$?
echo $rc > "$OUTDIR/flow.rc"
cat "$OUTDIR/flow.out"
cat "$OUTDIR/flow.err" >&2
exit $rc
"""


def latin1(b: bytes) -> str:
    return b.decode("latin-1")


def copy_inputs(test_dir: Path, cases: list[dict], out: Path) -> None:
    """test/ から、ケースの実行に要るものだけを inputs/ に写す。"""
    dirs = {"cygwin", "cygwin3", "RUNTIME"}
    for case in cases:
        dirs.add(case["cwd"])
    if out.exists():
        shutil.rmtree(out)
    for name in sorted(dirs):
        src = test_dir / name
        for path in src.rglob("*"):
            rel = path.relative_to(test_dir)
            if path.is_dir():
                continue
            if path.suffix in SKIP_SUFFIXES or rel.parts[1].startswith(
                SKIP_DIRS_PREFIX
            ):
                continue
            dest = out / rel
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy(path, dest)


def run_case(src: Path, inputs: Path, case: dict, work: Path) -> dict:
    shutil.copytree(inputs, work / "test")
    bindir = work / "bin"
    bindir.mkdir()
    for name in ("tecsgen", "tcflow"):
        (bindir / name).write_text(WRAPPER.format(src=src, name=name))
    (bindir / "tecsflow").write_text(FLOW_WRAPPER.format(src=src))
    for p in bindir.iterdir():
        p.chmod(0o755)
    outdir = work / "out"
    outdir.mkdir()
    cwd = work / "test" / case["cwd"]
    env = dict(
        os.environ,
        PATH=f"{bindir}:{os.environ['PATH']}",
        OUTDIR=str(outdir),
        TECSPATH=str(src / "tecs"),
        LANG="C",
    )
    make = subprocess.run(
        ["make", "tecsflow"],
        cwd=cwd,
        env=env,
        capture_output=True,
        timeout=TIMEOUT,
        check=False,
    )
    if not (outdir / "flow.out").exists():
        sys.exit(f"{case['id']}: tecsflow が実行されなかった\n{latin1(make.stdout)}")
    dumps = sorted(cwd.rglob("tcflow.rbdmp"))
    if len(dumps) != 1:
        sys.exit(f"{case['id']}: tcflow.rbdmp が {len(dumps)} 個")
    funclist = json.loads(
        subprocess.run(
            ["ruby", str(DUMP_JSON), str(src), str(dumps[0])],
            capture_output=True,
            timeout=TIMEOUT,
            check=True,
        ).stdout.decode("utf-8")
    )
    return {
        "id": case["id"],
        "gen_dir": dumps[0].parent.relative_to(cwd).as_posix(),
        "tecsflow": {
            "args": (outdir / "flow.args").read_text().split(),
            "returncode": int((outdir / "flow.rc").read_text()),
            "stdout": latin1((outdir / "flow.out").read_bytes()),
            "stderr": latin1((outdir / "flow.err").read_bytes()),
        },
        "funclist": funclist,
    }


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="移植元 tecsgen ディレクトリ")
    ap.add_argument("test_dir", type=Path, help="TECS の test/ ディレクトリ")
    ap.add_argument("out", type=Path, nargs="?", default=GOLDEN)
    ap.add_argument("--case", action="append", default=[], help="採るケースの id")
    ap.add_argument(
        "--copy-inputs", action="store_true", help="inputs/ を test/ から写し直す"
    )
    opts = ap.parse_args()

    cases = tomllib.loads((GOLDEN / "cases.toml").read_text(encoding="utf-8"))["case"]
    unknown = sorted(set(opts.case) - {c["id"] for c in cases})
    if unknown:
        sys.exit(f"unknown case: {unknown}")
    inputs = GOLDEN / "inputs"
    if opts.copy_inputs:
        copy_inputs(opts.test_dir, cases, inputs)
    ruby_version = subprocess.run(
        ["ruby", "-v"], capture_output=True, text=True, check=True
    ).stdout.strip()

    opts.out.mkdir(parents=True, exist_ok=True)
    for case in cases:
        if opts.case and case["id"] not in opts.case:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            record = run_case(opts.source, inputs, case, Path(tmp))
        record["ruby"] = ruby_version
        text = json.dumps(record, ensure_ascii=True, indent=1)
        with gzip.GzipFile(opts.out / f"{case['id']}.json.gz", "wb", mtime=0) as f:
            f.write(text.encode("ascii"))
        print(f"{case['id']}: {len(record['tecsflow']['stdout'].splitlines())} lines")


if __name__ == "__main__":
    main()
