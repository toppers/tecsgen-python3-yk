"""P4/P5 の差分テストの進み具合を一覧する（Ruby は不要。記録を再生する）。

    uv run python tools/port/p4_progress.py [ケースID の前方一致...] [-v]

プラグインを使う・使わないケースの両方を通しで実行し、ケースごとに終了コード・標準出力・
生成物の一致を表示する。プラグインを使うケースは末尾に " [plugin]" を付け、集計もプラグイン
の有無で分けて出す（[[tecsgen-python3移植計画]] P5「最初に」の一致一覧・1ケース差分表示）。
-v で、一致しなかった生成物の名前・標準出力の差分も表示する（1ケースの差分表示は
`uv run python tools/port/p4_progress.py <ケースID> -v` で見る）。
-d で、中身が違う生成物の unified diff（正解 → Python）も表示する。
"""

from __future__ import annotations

import difflib
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
    show_diff = "-d" in argv
    prefixes = [a for a in argv if not a.startswith("-")]
    n_ok = 0
    n_total = 0
    n_ok_plugin = 0
    n_total_plugin = 0
    kinds: Counter[str] = Counter()
    for cid in case_ids(include_kernel=True):
        if prefixes and not any(cid.startswith(p) for p in prefixes):
            continue
        rec = load_case(cid)
        if rec.exit_error == "SystemStackError":
            continue
        if rec.uses_plugin:
            n_total_plugin += 1
        else:
            n_total += 1
        try:
            r = run_case_captured(cid)
        except Exception as exc:  # noqa: BLE001
            print(f"EXC  {cid}: {exc}")
            if verbose:
                traceback.print_exc()
            continue
        if r.ok:
            if rec.uses_plugin:
                n_ok_plugin += 1
            else:
                n_ok += 1
        mark = "OK  " if r.ok else "NG  "
        tag = " [plugin]" if rec.uses_plugin else ""
        st = (
            ""
            if r.status == r.golden_status
            else f" status={r.status}/{r.golden_status}"
        )
        so = "" if r.stdout == r.golden_stdout else " stdout!"
        files = f"{len(r.same)}/{len(r.golden)}"
        print(f"{mark}{cid}{tag}: files {files}{st}{so}")
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
            if show_diff:
                for n in r.differ:
                    _print_file_diff(n, r.golden[n], r.written[n])
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
    print(f"\n{n_ok}/{n_total} cases match (no plugin)")
    print(f"{n_ok_plugin}/{n_total_plugin} cases match (plugin)")
    if kinds:
        print("mismatched file kinds:", dict(kinds.most_common()))
    return 0


def _print_file_diff(name: str, golden: bytes, written: bytes) -> None:
    """生成物1件の unified diff（正解 → Python）を表示する。"""
    a = golden.decode("utf-8", "replace").splitlines(keepends=True)
    b = written.decode("utf-8", "replace").splitlines(keepends=True)
    for line in difflib.unified_diff(a, b, f"ruby/{name}", f"python/{name}"):
        print("      " + line, end="" if line.endswith("\n") else "\n")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
