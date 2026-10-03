"""CDL の字句解析器（bnf.y.rb の `Generator#parse` のうち、トークン列 `@q` を作る走査ループ）。

Ruby 版は1行ずつ正規表現を順に当て、先頭から切り出したトークンを `@q` に積む。
行をまたぐのはコメント（`/* */` と `+---` 〜 `---+`）と、行末に `\\` のある文字列だけ。

文字コード（内部仕様5章）:

- Ruby 版は Shift_JIS 以外のファイルを ASCII-8BIT で読むので、1バイトを1文字として走査し、
  桁もバイト単位で数える。Python 版は latin-1 で復号して同じ走査をする。
  非 ASCII の文字の先頭バイトだけが未知の記号として切り出される（`near '\\xe3'`）のも同じになる
- 切り出したトークンの値は、latin-1 のバイト列に戻してから `TecsgenContext.file_codec` と
  `surrogateescape` で復号し直す。P1 の `TECSIO` と同じ文字列表現にそろえるためで、
  出力時に同じコーデックで符号化すれば元のバイト列に戻る
- Shift_JIS は Ruby 版と同じく Windows-31J（cp932）として読み、文字単位で走査する
- 正規表現は `re.ASCII` で使う。Ruby の `\\s`・`\\w` は ASCII-8BIT の文字列では ASCII にしか
  当たらないため（Windows-31J で `\\w` が全角文字に当たるかは未確認 — TBC）
"""

from __future__ import annotations

import re
from collections.abc import Callable, Iterator
from pathlib import Path
from typing import Any

from tecsgen.context import get_context
from tecsgen.core.generator import Generator, Token
from tecsgen.ruby_compat import Symbol, rb_puts

# 予約語（bnf.y.rb の RESERVED）。値はトークン種別
RESERVED: dict[str, str] = {
    # keyword
    "namespace": "NAMESPACE",
    "signature": "SIGNATURE",
    "celltype": "CELLTYPE",
    "cell": "CELL",
    "attr": "ATTRIBUTE",
    "var": "VAR",
    "call": "CALL",
    "entry": "ENTRY",
    "composite": "COMPOSITE",
    "require": "REQUIRE",
    "factory": "FACTORY",
    "FACTORY": "CTFACTORY",
    "typedef": "TYPEDEF",
    "struct": "STRUCT",
    "region": "REGION",
    "import": "IMPORT",
    "import_C": "IMPORT_C",
    "generate": "GENERATE",
    "__tool_info__": "TOOL_INFO",
    # types
    "void": "VOID",
    "volatile": "VOLATILE",
    "const": "CONST",
    "signed": "SIGNED",
    "unsigned": "UNSIGNED",
    "int8_t": "INT8_T",
    "int16_t": "INT16_T",
    "int32_t": "INT32_T",
    "int64_t": "INT64_T",
    "int128_t": "INT128_T",
    "uint8_t": "UINT8_T",
    "uint16_t": "UINT16_T",
    "uint32_t": "UINT32_T",
    "uint64_t": "UINT64_T",
    "uint128_t": "UINT128_T",
    "float32_t": "FLOAT32_T",
    "double64_t": "DOUBLE64_T",
    "bool_t": "BOOL_T",
    "char_t": "CHAR_T",
    "schar_t": "SCHAR_T",
    "uchar_t": "UCHAR_T",
    # unrecommened types
    "int": "INT",
    "short": "SHORT",
    "long": "LONG",
    # obsolete types
    "char": "CHAR",
    "enum": "ENUM",
    "enum8": "ENUM8",
    "enum16": "ENUM16",
    "enum32": "ENUM32",
    "enum64": "ENUM64",
    "true": "TRUE",
    "false": "FALSE",
    "C_EXP": "C_EXP",
    "Descriptor": "DESCRIPTOR",
}

_A = re.ASCII

# コメント中
_COMMENT_END = re.compile(r"\A\*/", _A)
_COMMENT2_END = re.compile(r"\A\-\-\-\+", _A)
_ANY_CHAR = re.compile(r"\A.", _A)
_SPACES = re.compile(r"\s+", _A)  # Ruby 版もここだけ \A が無い

# 行をまたぐ文字列の途中
_STR_CLOSE = re.compile(r'\A(?:[^"\\]|\\.)*"', _A)
_STR_CONT = re.compile(r"\A.*\\\n", _A)
_STR_NL = re.compile(r"\A.*\n", _A)

# 通常。Ruby 版の case 文の when の順に並べる
_MAIN: list[tuple[str, re.Pattern[str]]] = [
    ("space", re.compile(r"\A\s+", _A)),
    ("ident", re.compile(r"\A[a-zA-Z_]\w*", _A)),
    ("HEX_CONSTANT", re.compile(r"\A0x[0-9A-Fa-f]+", _A)),
    ("OCTAL_CONSTANT", re.compile(r"\A0[0-7]+", _A)),
    ("FLOATING_CONSTANT", re.compile(r"\A[0-9]+\.([0-9]*)?([Ee][+-]?[0-9]+)?", _A)),
    ("INTEGER_CONSTANT", re.compile(r"\A\d+", _A)),
    ("CHARACTER_LITERAL", re.compile(r"\A'(?:[^'\\]|\\.)'", _A)),
    ("STRING_LITERAL", re.compile(r'\A"(?:[^"\\]|\\.)*"', _A)),
    ("str_cont", re.compile(r'\A"(?:[^"\\]|\\.)*\\\n$', _A)),
    # Ruby 版の \e（ESC、0x1b）は \\. の誤記と思われるが、そのまま写す
    ("str_nl", re.compile(r'\A("(?:[^"\\]|\x1b\.)*)\n$', _A)),
    ("AB_STRING_LITERAL", re.compile(r"\A<(?:[^>\\]|\\.)*>", _A)),
    ("line_comment", re.compile(r"\A//.*$", _A)),
    ("comment", re.compile(r"\A/\*", _A)),
    ("comment2", re.compile(r"^\+\-\-\-", _A)),
    ("op2", re.compile(r"\A(?:>>|<<|==|!=|&&|\|\|)", _A)),
    ("op2", re.compile(r"\A(?:::|=>|<=|>=)", _A)),
    ("op1", re.compile(r"\A.", _A)),
]

_STRING_NEWLINE_ERROR = "string literal has newline without escape"


class LexError(Exception):
    """Ruby 版で走査ループが例外になる箇所（どの正規表現にも当たらない、など）。"""


class InvalidByteSequence(LexError):
    """Windows-31J として不正なバイト列の行（Ruby 版の ArgumentError `invalid byte sequence`）。"""


Reader = Callable[[str], bytes]

# Windows-31J として正しい並び（Ruby の `valid_encoding?` は文字の構造だけで判定し、
# 対応する Unicode が無い符号（81AD など）も正しいとする。Ruby 3.2.3 で全 1・2 バイトを調べて確かめた）
_WINDOWS_31J_VALID = re.compile(
    rb"(?:[\x00-\x7f\xa1-\xdf]|[\x81-\x9f\xe0-\xfc][\x40-\x7e\x80-\xfc])*"
)


def _read_file(file: str) -> bytes:
    return Path(file).read_bytes()


def _lines(file: str, reader: Reader) -> Iterator[str]:
    """ファイルを LF で行に分け、走査用に復号して返す（改行文字を含む）。

    Shift_JIS のとき、Windows-31J として不正なバイト列の行に来ると例外にする。Ruby 版は不正な文字列へ
    正規表現を当てて ArgumentError になり、CDL は G1014、C ヘッダは B1002 になる。
    """
    sjis = get_context().ruby19_file_encode == "Shift_JIS"
    codec = "cp932" if sjis else "latin-1"
    data = reader(file)
    start = 0
    while start < len(data):
        end = data.find(b"\n", start)
        end = len(data) if end < 0 else end + 1
        chunk = data[start:end]
        if sjis and not _WINDOWS_31J_VALID.fullmatch(chunk):
            raise InvalidByteSequence("invalid byte sequence in Windows-31J")
        yield chunk.decode(codec, errors="surrogateescape")
        start = end


def _value_converter() -> Any:
    """走査用の文字列を、P1 の TECSIO と同じ文字列表現へ変換する関数を返す。"""
    ctx = get_context()
    if ctx.ruby19_file_encode == "Shift_JIS":
        return lambda s: s
    codec = ctx.file_codec
    if codec == "latin-1":
        return lambda s: s
    return lambda s: s.encode("latin-1").decode(codec, errors="surrogateescape")


def lex_files(files: list[str], q: list[Any], reader: Reader = _read_file) -> None:
    """files を順に走査し、(トークン種別, Token) を q に積む。

    Ruby 版と同じく、ファイルを開けないときや走査が例外になったときは G1014 を出し、
    そのファイルのそれまでのトークンは残したまま次のファイルへ進む。
    reader はファイルの中身を返す関数（差分テストで、記録した中身を渡すために使う）。
    コメント中・文字列中という状態は、ファイルをまたいで引き継ぐ（Ruby 版と同じ）。
    """
    conv = _value_converter()
    state = {"comment": False, "comment2": False, "string": False, "buf": ""}
    for file in files:
        lineno = 1
        state["buf"] = (
            ""  # Ruby 版の string はファイルごとに初期化される（b_in_string は引き継ぐ）
        )
        try:
            for line in _lines(file, reader):
                _lex_line(line, file, lineno, q, state, conv)
                lineno += 1
        except (OSError, LexError):
            Generator.error("G1014 while open or reading '$1'", file)


def _lex_line(
    line: str, file: str, lineno: int, q: list[Any], state: dict[str, Any], conv: Any
) -> None:
    col = 1
    while line:
        if state["comment"] or state["comment2"]:
            m = _COMMENT_END.match(line)
            if m:
                state["comment"] = False
            else:
                m = _COMMENT2_END.match(line)
                if m:
                    state["comment2"] = False
                else:
                    m = _ANY_CHAR.match(line) or _SPACES.search(line)
        elif state["string"]:
            m = _STR_CLOSE.match(line)
            if m:
                string = state["buf"] + m.group()
                q.append(("STRING_LITERAL", Token(conv(string), file, lineno, col)))
                state["string"] = False
            else:
                m = _STR_CONT.match(line)
                if m:
                    state["buf"] += m.group()
                else:
                    m = _STR_NL.match(line)
                    if m:
                        state["buf"] += line
                        # この位置では error メソッドは使えない（トークン読出し前）
                        rb_puts(
                            f"{file}:{lineno}:{col}: error: {_STRING_NEWLINE_ERROR}"
                        )
                        Generator._n_error += 1
        else:
            m = _lex_main(line, file, lineno, col, q, state, conv)
        if m is None:
            # Ruby 版では $' が nil になり、NoMethodError が G1014 として報告される
            raise LexError(f"{file}:{lineno}:{col}")
        line = line[m.end() :]
        col += m.end() - m.start()


def _lex_main(
    line: str,
    file: str,
    lineno: int,
    col: int,
    q: list[Any],
    state: dict[str, Any],
    conv: Any,
) -> re.Match[str] | None:
    for kind, pattern in _MAIN:
        m = pattern.match(line) if kind != "comment2" else pattern.search(line)
        if m is None:
            continue
        text = m.group()
        if kind == "space" or kind == "line_comment":
            pass
        elif kind == "ident":
            # Ruby 版は word.intern（Symbol）
            q.append(
                (
                    RESERVED.get(text, "IDENTIFIER"),
                    Token(Symbol(text), file, lineno, col),
                )
            )
        elif kind == "INTEGER_CONSTANT":
            q.append((kind, Token(int(text), file, lineno, col)))
        elif kind in (
            "HEX_CONSTANT",
            "OCTAL_CONSTANT",
            "FLOATING_CONSTANT",
            "CHARACTER_LITERAL",
            "STRING_LITERAL",
            "AB_STRING_LITERAL",
        ):
            q.append((kind, Token(conv(text), file, lineno, col)))
        elif kind == "str_cont":
            state["buf"] = text
            state["string"] = True
        elif kind == "str_nl":
            state["buf"] = m.group(1) + "\\\n"
            state["string"] = True
            # この位置では error メソッドは使えない（トークン読出し前）
            rb_puts(f"{file}:{lineno}:{col}: error: {_STRING_NEWLINE_ERROR}")
            Generator._n_error += 1
        elif kind == "comment":
            state["comment"] = True
        elif kind == "comment2":
            state["comment2"] = True
        else:  # op2, op1: 記号そのものがトークン種別
            value = conv(text)
            q.append((value, Token(value, file, lineno, col)))
        return m
    return None
