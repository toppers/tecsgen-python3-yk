"""P2 のオラクルの記録を、正解データとして tests/golden/p2/ に保存する。

tests/ruby/ruby-p2-oracle を --ruby に渡して generate_golden.py で採取した出力から、
各ケースの stderr.txt の "@@P2 " 行を取り出し、tests/golden/p2/<ケース>.jsonl.gz に書く。
同時に、stdout.txt が tests/golden/cases の正解データと一致すること（フックが出力を
変えていないこと）を確かめる。

    python3 tools/port/collect_p2_oracle.py <採取した出力ディレクトリ>
"""

from __future__ import annotations

import gzip
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
GOLDEN = ROOT / "tests" / "golden" / "cases"
OUT = ROOT / "tests" / "golden" / "p2"
PREFIX = b"@@P2 "


def main() -> int:
    trace_cases = Path(sys.argv[1]) / "cases"
    mismatched = []
    total = 0
    for meta in sorted(trace_cases.rglob("meta.json")):
        case_dir = meta.parent
        case_id = case_dir.relative_to(trace_cases).as_posix()
        stdout = (case_dir / "stdout.txt").read_bytes()
        if stdout != (GOLDEN / case_id / "stdout.txt").read_bytes():
            mismatched.append(case_id)
        lines = [
            line[len(PREFIX) :]
            for line in (case_dir / "stderr.txt").read_bytes().splitlines()
            if line.startswith(PREFIX)
        ]
        out = OUT / f"{case_id}.jsonl.gz"
        out.parent.mkdir(parents=True, exist_ok=True)
        # mtime=0 で、同じ内容なら同じバイト列になるようにする
        with (
            out.open("wb") as raw,
            gzip.GzipFile(fileobj=raw, mode="wb", mtime=0) as gz,
        ):
            gz.write(b"\n".join(lines) + b"\n")
        total += 1
    print(f"{total} cases written to {OUT}")
    if mismatched:
        print(f"stdout differs from golden: {mismatched}")
        return 1
    return 0


if __name__ == "__main__":
    sys.exit(main())
