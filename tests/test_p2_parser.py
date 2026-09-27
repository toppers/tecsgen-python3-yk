"""CDL・import_C のパーサを通しで動かす差分テスト。

ファイルの中身から字句解析・next_token（TYPE_NAME と指定子キーワードへの置換、import_C の
typedef・struct 以外の読み飛ばし）・racc の駆動・on_error までを Python 版で動かし、
Ruby 版と比べる。

- next_token が返したトークン列（置換後）が、parse の呼び出しごとに Ruby 版と一致する
- 構文エラー（G1015・G1016・B1003・B1004）と字句解析のエラーの出力が、正解データの
  stdout にある同じ種類の行と一致する（行の集合として比べる。import による入れ子で
  出力の順序が前後するため）

TYPE_NAME の判定はシンボル表（Namespace）が要るので、Ruby 版の記録から
「その位置のトークンが TYPE_NAME になったか」を返す仮の関数を使う。
文法アクションは、字句解析の状態を変えるもの（指定子の中か、TYPE_NAME に置き換えるか、
typeof・__asm__ の読み飛ばし）だけを動かし、他は値を素通しする（モデルは P3 の
test_p3_model で比べる）。そのため import による入れ子のパースは起きない。
入れ子のパースは、Ruby 版の記録の parse ごとに独立に動かして確かめる。
"""

from __future__ import annotations

import re
from collections.abc import Iterator
from typing import Any

import pytest
from conftest import GOLDEN
from p2_oracle_data import ParseRecord, case_env, case_ids, load_case, raw
from test_p2_lexer import as_ruby, value_codec

from tecsgen.context import TecsgenContext
from tecsgen.core.generator import Generator
from tecsgen.core.tecs_lang import TECS_LANG
from tecsgen.syntax import cdecl_actions, cdl_actions
from tecsgen.syntax.cdecl_parser import CdeclParser
from tecsgen.syntax.cdl_parser import CdlParser

# 字句解析の状態を変えるアクション（それ以外は素通しにする）
CDL_LEXER_RULES = {419, 420}
CDECL_LEXER_RULES = {
    *range(102, 119),
    120,
    122,
    123,
    124,
    127,
    139,
    140,
    141,
    142,
    212,
    261,
}


def _passthrough(self: Any, val: list[Any], _values: list[Any], result: Any) -> Any:
    return result


def _lexer_only_c_action(rule: int) -> Any:
    """C_parser の、状態だけを変えるアクション（モデルは作らない）。"""
    orig = getattr(cdecl_actions.CdeclActions, f"_reduce_{rule}")
    if rule in (117, 261):
        return orig  # トークンの読み飛ばし（モデルは CVoidType を作るだけ）

    def f(self: Any, val: list[Any], _values: list[Any], result: Any) -> Any:
        self.set_no_type_name(rule != 212)
        return result

    return f


# 構文解析で出るメッセージ（stdout の行）
# （print_exception の "*** Begin Ruby exception message ***" は、他のフェーズでも出るので含めない）
SYNTAX_MESSAGE = re.compile(
    rb": error: (?:G101[456]|B100[234]) |string literal has newline without escape"
)


def typename_positions(rec: ParseRecord) -> set[tuple[str, int, int]]:
    """Ruby 版で TYPE_NAME に置き換わったトークンの位置。"""
    return {
        (t[2][0], t[2][1], t[2][2])
        for t in rec.tokens
        if t is not None and t[2] is not None and t[0] == ["Symbol", "TYPE_NAME"]
    }


def make_parser(rec: ParseRecord) -> Any:
    positions = typename_positions(rec)
    codec = value_codec()

    def reader(file: str) -> bytes:
        data = rec.sources.get(file.encode(codec, "surrogateescape").decode("latin-1"))
        if data is None:
            raise FileNotFoundError(2, "No such file or directory", file)
        return data

    def locale_key(locale: Any) -> tuple[str, int, int]:
        file, line, col = locale
        return (file.encode(codec, "surrogateescape").decode("latin-1"), line, col)

    base: Any = CdlParser if rec.parser == "cdl" else CdeclParser

    class RecordingParser(base):
        returned: list[Any]

        @staticmethod
        def typename_resolver(name: Any) -> bool:
            locale = (
                Generator.current_locale()
                if rec.parser == "cdl"
                else CdeclParser.current_locale()
            )
            return locale_key(locale) in positions

        def next_token(self) -> Any:
            token = super().next_token()
            if token is None:
                self.returned.append(None)
            elif token[0] is False:
                self.returned.append([["FalseClass", ""], None, None])
            else:
                self.returned.append(as_ruby(token[0], token[1]))
            return token

    if rec.parser == "cdl":
        for r in cdl_actions.ACTION_RULES - CDL_LEXER_RULES:
            setattr(RecordingParser, f"_reduce_{r}", _passthrough)
    else:
        for r in cdecl_actions.ACTION_RULES:
            f = _lexer_only_c_action(r) if r in CDECL_LEXER_RULES else _passthrough
            setattr(RecordingParser, f"_reduce_{r}", f)
    RecordingParser._push_model_stacks = lambda self: None  # type: ignore[method-assign]
    RecordingParser._pop_model_stacks = lambda self: None  # type: ignore[method-assign]

    parser = RecordingParser(reader)
    parser.returned = []
    return parser


def run_record(rec: ParseRecord) -> list[Any]:
    parser = make_parser(rec)
    files = [raw(f).decode(value_codec(), "surrogateescape") for f in rec.files]
    parser.parse(files)
    return parser.returned


def syntax_lines(data: bytes) -> Iterator[bytes]:
    for line in data.splitlines():
        if SYNTAX_MESSAGE.search(line):
            yield line


@pytest.mark.parametrize("case_id", case_ids())
def test_parser_matches_ruby(
    case_id: str,
    fresh_state: TecsgenContext,
    capsysbinary: pytest.CaptureFixture[bytes],
) -> None:
    TECS_LANG.setup(fresh_state, case_env(case_id))
    records = load_case(case_id)
    aborted = any(r.aborted for r in records)
    for rec in records:
        returned = run_record(rec)
        expected = rec.tokens
        if rec.aborted:
            returned = returned[: len(expected)]
        for i, (a, e) in enumerate(zip(returned, expected, strict=False)):
            assert a == e, f"{rec.parser} {rec.files} token #{i}"
        assert len(returned) == len(expected), f"{rec.parser} {rec.files}"

    if aborted:
        return  # Ruby 版は途中で止まったので、出力は比べない
    out = capsysbinary.readouterr().out
    golden = (GOLDEN / case_id / "stdout.txt").read_bytes()
    assert sorted(syntax_lines(out)) == sorted(syntax_lines(golden))
