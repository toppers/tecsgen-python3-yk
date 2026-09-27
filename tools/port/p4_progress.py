"""P4 の差分テストの進み具合を一覧する（Ruby は不要。記録を再生する）。

    uv run python tools/port/p4_progress.py [ケースID の前方一致...] [-v]

プラグインを使わないケースを通しで実行し、ケースごとに終了コード・標準出力・生成物の一致を表示する。
-v で、一致しなかった生成物の名前も表示する。
"""

from __future__ import annotations

import sys
import traceback
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
sys.path[:0] = [str(ROOT / "tests"), str(ROOT / "src")]

from p3_oracle_data import case_ids, load_case  # ty: ignore[unresolved-import]
from p4_gen_check import run_case_captured  # ty: ignore[unresolved-import]


def main(argv: list[str]) -> int:
    verbose = "-v" in argv
    prefixes = [a for a in argv if not a.startswith("-")]
    n_ok = 0
    n_total = 0
    kinds: Counter[str] = Counter()
    for cid in case_ids():
        if prefixes and not any(cid.startswith(p) for p in prefixes):
            continue
        rec = load_case(cid)
        if rec.uses_plugin or rec.exit_error == "SystemStackError":
            continue
        n_total += 1
        try:
            r = run_case_captured(cid)
        except Exception:  # noqa: BLE001
            print(f"EXC  {cid}")
            if verbose:
                traceback.print_exc()
            continue
        if r.ok:
            n_ok += 1
        mark = "OK  " if r.ok else "NG  "
        st = (
            ""
            if r.status == r.golden_status
            else f" status={r.status}/{r.golden_status}"
        )
        so = "" if r.stdout == r.golden_stdout else " stdout!"
        files = f"{len(r.same)}/{len(r.golden)}"
        print(f"{mark}{cid}: files {files}{st}{so}")
        for name in r.missing + r.differ + r.extra:
            kinds[
                Path(name).name.split("_")[-1]
                if "_" in Path(name).name
                else Path(name).name
            ] += 1
        if verbose and not r.ok:
            for label, names in (
                ("missing", r.missing),
                ("differ", r.differ),
                ("extra", r.extra),
            ):
                for n in names:
                    print(f"      {label}: {n}")
            if r.stdout != r.golden_stdout:
                print("      --- stdout (python)")
                print(
                    "      "
                    + r.stdout.decode("utf-8", "replace").replace("\n", "\n      ")
                )
                print("      --- stdout (ruby)")
                print(
                    "      "
                    + r.golden_stdout.decode("utf-8", "replace").replace(
                        "\n", "\n      "
                    )
                )
            if r.stderr:
                print("      --- stderr (python)")
                print(
                    "      "
                    + r.stderr.decode("utf-8", "replace").replace("\n", "\n      ")
                )
    print(f"\n{n_ok}/{n_total} cases match")
    if kinds:
        print("mismatched file kinds:", dict(kinds.most_common()))
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
