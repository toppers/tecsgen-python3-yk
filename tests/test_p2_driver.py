"""racc 駆動部（tecsgen.syntax.racc_runtime）の差分テスト。

Ruby 版の next_token が返したトークン列（TYPE_NAME への置換後）を、そのまま Python の
駆動部に入れる。アクションは呼ばれた順を記録するだけの仮のものにする。next_token・
アクション・on_error の呼び出し列が、parse の呼び出しごとに Ruby 版と一致することを確かめる。
構文エラーからの回復（error トークン、error_status）の挙動もここで確かめる。

アクションの値は shift・reduce・エラー回復の判断に使われないので、仮のアクションで十分。
Ruby 版が使う racc の C 実装は `_reduce_none` を呼ばないので、記録にも現れない。
（文法アクションの yyerror・yyaccept・yyerrok は、文法から使われていない）
"""

from __future__ import annotations

from typing import Any

import pytest
from conftest import GOLDEN  # noqa: F401  （p2_oracle_data が使う）
from p2_oracle_data import ParseRecord, case_ids, load_case

from tecsgen.syntax import cdecl_tables, cdl_tables
from tecsgen.syntax.racc_runtime import RaccParser


def ruby_kind(v: list[str]) -> Any:
    cls, s = v
    if cls == "FalseClass":
        return False
    if cls == "NilClass":
        return None
    return s


class TokensExhausted(Exception):
    """記録したトークンを使い切った（Ruby 版が例外で中断したケース）。"""


class ReplayParser(RaccParser):
    """記録したトークン列を返し、呼び出しを記録するパーサ。"""

    def __init__(self, tokens: list[Any]) -> None:
        self._tokens = list(tokens)
        self.events: list[tuple[Any, ...]] = []
        super().__init__()

    def next_token(self) -> tuple[Any, Any] | None:
        if not self._tokens:
            raise TokensExhausted
        self.events.append(("tok",))
        tok = self._tokens.pop(0)
        if tok is None:  # C_parser は EOF で nil を返す
            return None
        kind, _val, loc = tok
        if loc is None:  # Generator は EOF で [false, false] を返す
            return ruby_kind(kind), ruby_kind(kind)
        return ruby_kind(kind), tok

    def on_error(self, t: int, val: Any, vstack: list[Any]) -> None:
        if isinstance(val, list):
            v: Any = [["NilClass", ""], val[1], val[2]]
        elif val is False:
            v = ["FalseClass", ""]
        elif isinstance(val, str):  # C_parser の EOF（C 実装が値を "$" にする）
            v = ["String", val]
        else:
            v = ["NilClass", ""]
        self.events.append(("err", t, v))

    def __getattr__(self, name: str) -> Any:
        if not name.startswith("_reduce_"):
            raise AttributeError(name)

        def action(val: list[Any], vstack: list[Any], result: Any = None) -> Any:
            self.events.append(("red", name))
            return result

        return action


class CdlReplay(ReplayParser):
    TABLES = cdl_tables


class CdeclReplay(ReplayParser):
    TABLES = cdecl_tables


REPLAYS: dict[str, type[ReplayParser]] = {"cdl": CdlReplay, "c": CdeclReplay}


def check(rec: ParseRecord) -> None:
    if rec.q is None:
        return  # parse の前に止まった（読み込みエラーなど）
    parser = REPLAYS[rec.parser](rec.tokens)
    if rec.aborted:
        # Ruby 版はアクションの中の例外で中断した。中断までの呼び出し列が一致すればよい
        with pytest.raises(TokensExhausted):
            parser.do_parse()
        actual = parser.events[: len(rec.events)]
    else:
        parser.do_parse()
        actual = parser.events
    for i, (a, e) in enumerate(zip(actual, rec.events, strict=False)):
        assert a == e, f"{rec.case_id} {rec.files} event #{i}"
    assert len(actual) == len(rec.events), f"{rec.case_id} {rec.files}"


@pytest.mark.parametrize("case_id", case_ids())
def test_driver_matches_ruby(case_id: str) -> None:
    for rec in load_case(case_id):
        check(rec)
