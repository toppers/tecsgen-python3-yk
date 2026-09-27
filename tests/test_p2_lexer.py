"""CDL の字句解析器の差分テスト。Ruby 版が字句解析した直後のトークン列 `@q` と比べる。

正解は tests/golden/p2/（tests/ruby/p2_oracle.rb の記録）。全155ケースで Ruby 版が
Generator#parse に渡したすべてのファイルについて、種別・値・位置が一致することを確かめる。
"""

from __future__ import annotations

import re
from typing import Any

import pytest
from conftest import GOLDEN  # noqa: F401  （p2_oracle_data が使う）
from p2_oracle_data import ParseRecord, case_env, case_ids, load_case, raw

from tecsgen.context import TecsgenContext, get_context
from tecsgen.core.generator import Token
from tecsgen.core.tecs_lang import TECS_LANG
from tecsgen.syntax.cdl_lexer import lex_files

# リテラルの種別。これ以外の名前の種別（予約語・IDENTIFIER・TYPE_NAME など）は、
# Ruby 版では値も Symbol（word.intern）になる
LITERAL_KINDS = {
    "HEX_CONSTANT",
    "OCTAL_CONSTANT",
    "FLOATING_CONSTANT",
    "INTEGER_CONSTANT",
    "CHARACTER_LITERAL",
    "STRING_LITERAL",
    "AB_STRING_LITERAL",
}
# 名前の種別（Ruby の Symbol）。記号の種別（Ruby の String）は、この形にならない
NAMED_KIND = re.compile(r"[A-Z_][A-Z0-9_]*")


def value_codec() -> str:
    ctx = get_context()
    return "cp932" if ctx.ruby19_file_encode == "Shift_JIS" else ctx.file_codec


def as_ruby(kind: str, tok: Token) -> list[Any]:
    """Python のトークンを、オラクルの記録と同じ形に直す。"""
    codec = value_codec()

    def s(x: str) -> str:
        return x.encode(codec, errors="surrogateescape").decode("latin-1")

    named = NAMED_KIND.fullmatch(kind) is not None
    kind_v = ["Symbol", kind] if named else ["String", s(kind)]
    if isinstance(tok.val, int):
        val = ["Integer", str(tok.val)]
    else:
        cls = "Symbol" if named and kind not in LITERAL_KINDS else "String"
        val = [cls, s(tok.val)]
    return [kind_v, val, [s(tok.file), tok.lineno, tok.col]]


def lex_record(rec: ParseRecord) -> list[Any]:
    def reader(file: str) -> bytes:
        data = rec.sources.get(
            file.encode(value_codec(), "surrogateescape").decode("latin-1")
        )
        if data is None:
            raise OSError(f"no such file: {file}")
        return data

    q: list[Any] = []
    files = [raw(f).decode(value_codec(), "surrogateescape") for f in rec.files]
    lex_files(files, q, reader)
    return [as_ruby(kind, tok) for kind, tok in q]


@pytest.mark.parametrize("case_id", case_ids())
def test_lexer_matches_ruby(case_id: str, fresh_state: TecsgenContext) -> None:
    TECS_LANG.setup(fresh_state, case_env(case_id))
    records = [r for r in load_case(case_id) if r.parser == "cdl"]
    assert records, "parse の記録が無い"
    for rec in records:
        assert rec.q is not None, f"{rec.files}: @q の記録が無い（parse 前に止まった）"
        assert rec.q[-1] is None, "@q の末尾は終了の印 nil"
        expected = rec.q[:-1]
        actual = lex_record(rec)
        for i, (a, e) in enumerate(zip(actual, expected, strict=False)):
            assert a == e, f"{rec.files} token #{i}"
        assert len(actual) == len(expected), rec.files
