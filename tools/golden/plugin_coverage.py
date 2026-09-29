"""plugin_trace.rb のログから、正解データがどのプラグインを実行したかを集計する。

標準ライブラリだけで動く。

    python3 tools/golden/plugin_coverage.py --plugin-dir <tecsgen>/tecslib/plugin \\
        --trace main=trace_main.log --trace kernel=trace_kernel.log

ログの各行は `load<TAB>ファイル名`（Kernel#load / require）か `new<TAB>クラス名`
（Plugin の子クラスのインスタンス生成）。プラグインごとに、ケース群（--trace の名前）別の
ロード回数と生成回数を数え、次の3つに分ける。

- 一度もロードされなかった: 正解データが無いプラグイン
- ロードされたが生成されなかった: 基底クラス・振り分け用・管理用（抜けとは限らない）
- 生成された: 採取済み（生成回数が少ないものは「薄い」として別に並べる）

判定はロードと生成の有無だけで、プラグイン内の全メソッド・全分岐を実行したかは見ない。
"""

from __future__ import annotations

import argparse
import collections
import sys
from pathlib import Path

THIN_LIMIT = 3  # この回数以下の生成は「薄い」とみなす


def read_trace(path: Path) -> tuple[collections.Counter, collections.Counter]:
    loads: collections.Counter = collections.Counter()
    news: collections.Counter = collections.Counter()
    for line in path.read_text(encoding="utf-8", errors="replace").splitlines():
        kind, _, name = line.partition("\t")
        if kind == "load":
            loads[name] += 1
        elif kind == "new":
            news[name] += 1
    return loads, news


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--plugin-dir", type=Path, required=True,
                        help="移植元の tecslib/plugin（lib/ を含む）")
    parser.add_argument("--trace", action="append", default=[], metavar="名前=ログ",
                        help="ケース群の名前とログのパス（複数指定可）")
    opts = parser.parse_args(argv)
    if not opts.trace:
        parser.error("--trace を1つ以上指定してください")

    traces: dict[str, tuple[collections.Counter, collections.Counter]] = {}
    for spec in opts.trace:
        name, sep, path = spec.partition("=")
        if not sep:
            parser.error(f"--trace は 名前=ログ の形で指定します: {spec}")
        traces[name] = read_trace(Path(path))

    plugins = sorted(p.stem for p in opts.plugin_dir.glob("*.rb"))
    libs = sorted(p.stem for p in (opts.plugin_dir / "lib").glob("*.rb"))

    def loaded(n: str) -> int:
        return sum(t[0][n + ".rb"] for t in traces.values())

    def created(n: str) -> int:
        return sum(t[1][n] for t in traces.values())

    def per(n: str, which: int) -> str:
        return " ".join(f"{k}={t[which][n + '.rb' if which == 0 else n]}" for k, t in traces.items())

    never = [n for n in plugins + libs if loaded(n) == 0]
    load_only = [n for n in plugins if loaded(n) > 0 and created(n) == 0]
    made = [n for n in plugins if created(n) > 0]
    thin = [n for n in made if created(n) <= THIN_LIMIT]

    print(f"plugins {len(plugins)}, libs {len(libs)}; traces: {', '.join(traces)}")
    print(f"created at least once: {len(made)}")
    print(f"loaded but never created: {len(load_only)}")
    print(f"never loaded: {len(never)} (incl. libs)")
    print("\n== NEVER LOADED (no golden data)")
    for n in never:
        print(f"  {n}{'  [lib]' if n in libs else ''}")
    print("\n== LOADED BUT NEVER CREATED (abstract / dispatch / manager: not necessarily a gap)")
    for n in load_only:
        print(f"  {n:32} load: {per(n, 0)}")
    print(f"\n== THIN (created <= {THIN_LIMIT} times in total)")
    for n in thin:
        print(f"  {n:32} new: {per(n, 1)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
