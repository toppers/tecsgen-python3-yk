"""P2 の差分テストが使う、Ruby 版オラクルの記録（tests/golden/p2/）の読み込み。

記録は tools/port/run_p2_oracle.sh が tests/ruby/p2_oracle.rb を使って採る。1ケースにつき
1ファイルで、parse の呼び出しごとに、読んだファイルの中身・字句解析直後のトークン列・
next_token が返したトークン列・アクションの呼び出し順・on_error の呼び出しが入っている。
"""

from __future__ import annotations

import gzip
import json
from collections.abc import Iterator
from dataclasses import dataclass, field
from typing import Any

from conftest import GOLDEN

P2_GOLDEN = GOLDEN.parent / "p2"

# Ruby の値の表現 [クラス名, 文字列]。文字列はバイト列を latin-1 として JSON にしたもの
RubyValue = list[str]
# [種別, 値, [ファイル, 行, 桁]]。値と位置は Token でないとき null
RubyToken = list[Any] | None


@dataclass
class ParseRecord:
    """Generator#parse（または C_parser#parse）の1回の呼び出し。"""

    case_id: str
    parser: str  # "cdl" | "c"
    id: int
    files: list[str]
    sources: dict[str, bytes | None] = field(default_factory=dict)
    q: list[RubyToken] | None = None
    tokens: list[RubyToken] = field(default_factory=list)
    # ("tok",)・("red", メソッド名)・("err", 記号番号, 値)。呼ばれた順
    events: list[tuple[Any, ...]] = field(default_factory=list)
    # 例外で parse が中断したときの例外クラス名
    aborted: str | None = None


def raw(s: str) -> bytes:
    """オラクルが latin-1 で JSON にした文字列を、元のバイト列に戻す。"""
    return s.encode("latin-1")


def case_ids() -> list[str]:
    return sorted(
        p.relative_to(P2_GOLDEN).as_posix().removesuffix(".jsonl.gz")
        for p in P2_GOLDEN.rglob("*.jsonl.gz")
    )


def case_env(case_id: str) -> dict[str, str]:
    meta = json.loads((GOLDEN / case_id / "meta.json").read_text(encoding="utf-8"))
    return dict(meta["env"])


def load_case(case_id: str) -> list[ParseRecord]:
    records: dict[int, ParseRecord] = {}
    path = P2_GOLDEN / f"{case_id}.jsonl.gz"
    with gzip.open(path, "rt", encoding="utf-8") as f:
        for line in f:
            if not line.strip():
                continue
            ev = json.loads(line)
            kind = ev["ev"]
            if kind == "parse":
                records[ev["id"]] = ParseRecord(case_id, ev["p"], ev["id"], ev["files"])
                continue
            rec = records[ev["id"]]
            if kind == "src":
                rec.sources[ev["file"]] = (
                    None if ev["data"] is None else raw(ev["data"])
                )
            elif kind == "q":
                rec.q = ev["q"]
            elif kind == "tok":
                rec.tokens.append(ev["t"])
                rec.events.append(("tok",))
            elif kind == "red":
                rec.events.append(("red", ev["m"]))
            elif kind == "err":
                rec.events.append(("err", ev["t"], ev["v"]))
            elif kind == "abort":
                rec.aborted = ev["error"]
    return list(records.values())


def all_records(parser: str) -> Iterator[ParseRecord]:
    for case_id in case_ids():
        for rec in load_case(case_id):
            if rec.parser == parser:
                yield rec
