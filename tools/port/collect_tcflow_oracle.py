"""Ruby 版 tcflow を実行して、差分テストの正解データ（tests/golden/tcflow/）を採る。

WSL（Linux）で実行する。移植元の tecsgen ディレクトリ（tcflow.rb と flowlib/ がある所）と、
出力先を渡す。

    python3 tools/port/collect_tcflow_oracle.py <移植元 tecsgen ディレクトリ> [出力先] [--case ID ...]

出力先の既定は tests/golden/tcflow/。ケースの定義は tests/golden/tcflow/cases.toml、
入力の C ファイルは tests/golden/tcflow/inputs/。ケースごとに `<id>.json.gz` を作る。

記録するもの:
- steps : 実行ごとの引数・終了コード・標準出力・標準エラー出力
- files : 実行後の `gen/`・`out/` のファイル（tcflow.rbdmp を除く）。cpp の一時ファイルなど
- funclist : 最後の tcflow.rbdmp を tests/ruby/tcflow_dump_json.rb で JSON にしたもの（無ければ null）

バイト列は latin-1 で復号した文字列にして持つ（Python 版の内部表現と同じ）。
"""

from __future__ import annotations

import argparse
import gzip
import json
import shutil
import subprocess
import sys
import tempfile
import tomllib
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "tests" / "golden" / "tcflow"
DUMP_JSON = ROOT / "tests" / "ruby" / "tcflow_dump_json.rb"
DUMP_NAME = "tcflow.rbdmp"
TIMEOUT = 120


def latin1(b: bytes) -> str:
    return b.decode("latin-1")


def run_case(src: Path, case: dict, work: Path) -> dict:
    for name in case.get("dirs", ["gen"]):
        (work / name).mkdir()
    for name in case["inputs"]:
        shutil.copy(GOLDEN / "inputs" / name, work / name)

    steps = []
    for args in case["steps"]:
        proc = subprocess.run(
            ["ruby", str(src / "tcflow.rb"), *args],
            cwd=work,
            capture_output=True,
            timeout=TIMEOUT,
            check=False,
        )
        steps.append(
            {
                "args": args,
                "returncode": proc.returncode,
                "stdout": latin1(proc.stdout),
                "stderr": latin1(proc.stderr),
            }
        )

    files = {}
    for path in sorted(work.rglob("*")):
        rel = path.relative_to(work).as_posix()
        if (
            path.is_file()
            and rel.split("/")[0] in ("gen", "out")
            and path.name != DUMP_NAME
        ):
            files[rel] = latin1(path.read_bytes())

    funclist = None
    dumps = sorted(work.rglob(DUMP_NAME))
    if dumps:
        # NOSONAR: 開発用ツール。リスト形式（シェルを通さない）で、引数は作業者が渡す移植元のパスと採取した一時ファイル
        out = subprocess.run(  # NOSONAR
            ["ruby", str(DUMP_JSON), str(src), str(dumps[0])],
            capture_output=True,
            timeout=TIMEOUT,
            check=True,
        ).stdout
        funclist = json.loads(out.decode("utf-8"))
    return {"id": case["id"], "steps": steps, "files": files, "funclist": funclist}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("source", type=Path, help="移植元 tecsgen ディレクトリ")
    ap.add_argument("out", type=Path, nargs="?", default=GOLDEN)
    ap.add_argument("--case", action="append", default=[], help="採るケースの id")
    opts = ap.parse_args()

    cases = tomllib.loads((GOLDEN / "cases.toml").read_text(encoding="utf-8"))["case"]
    ids = [c["id"] for c in cases]
    unknown = sorted(set(opts.case) - set(ids))
    if unknown:
        sys.exit(f"unknown case: {unknown}")
    ruby_version = subprocess.run(
        ["ruby", "-v"], capture_output=True, text=True, check=True
    ).stdout.strip()

    opts.out.mkdir(parents=True, exist_ok=True)
    for case in cases:
        if opts.case and case["id"] not in opts.case:
            continue
        with tempfile.TemporaryDirectory() as tmp:
            record = run_case(opts.source, case, Path(tmp))
        record["ruby"] = ruby_version
        data = json.dumps(record, ensure_ascii=True, indent=1, sort_keys=False)
        with gzip.GzipFile(opts.out / f"{case['id']}.json.gz", "wb", mtime=0) as f:
            f.write(data.encode("ascii"))
        print(f"{case['id']}: {[s['returncode'] for s in record['steps']]}")


if __name__ == "__main__":
    main()
