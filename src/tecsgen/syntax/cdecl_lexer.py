"""import_C 用の C ヘッダの字句解析器（C_parser.y.rb の `C_parser#parse` の走査ループ）。

入力は C プリプロセッサの出力（`tmp_*.h`）。CDL の字句解析器（`cdl_lexer`）と同じく、
Shift_JIS 以外は1バイトを1文字として走査する。違いは次のとおり。

- 行末の空白を先に取り除く（Ruby の `String#rstrip!`。NUL も取り除く）ので、行をまたぐ
  文字列は無い。コメントは `/* */` だけ
- 整数リテラルに接尾辞（`U`・`L`・`LL` など）が付く
- 読み込みに失敗したときは B1002 を出し、Ruby の例外メッセージも出力する（print_exception）
"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import print_exception
from tecsgen.core.generator import Generator, Token
from tecsgen.syntax.cdl_lexer import (
    LexError,
    Reader,
    _lines,
    _read_file,
    _value_converter,
)

# 予約語（C_parser.y.rb の RESERVED）。値はトークン種別
RESERVED: dict[str, str] = {
    # keyword
    "typedef": "TYPEDEF",
    "struct": "STRUCT",
    "union": "UNION",
    "sizeof": "SIZEOF",
    "__typeof__": "TYPEOF",
    "typeof": "TYPEOF",
    "throw": "THROW",
    # specifier
    # types
    "void": "VOID",
    "char": "CHAR",
    "short": "SHORT",
    "volatile": "VOLATILE",
    "const": "CONST",
    "extern": "EXTERN",
    "long": "LONG",
    "float": "FLOAT",
    "double": "DOUBLE",
    "signed": "SIGNED",
    "unsigned": "UNSIGNED",
    "int": "INT",
    "enum": "ENUM",
    "if": "IF",
    "else": "ELSE",
    "while": "WHILE",
    "do": "DO",
    "for": "FOR",
    "case": "CASE",
    "default": "DEFAULT",
    "goto": "GOTO",
    "continue": "CONTINUE",
    "break": "BREAK",
    "return": "RETURN",
    "__inline__": "__INLINE__",
    "inline": "INLINE",
    "__inline": "__INLINE",
    "Inline": "CINLINE",  # inline starting with Capital letter
    "static": "STATIC",
    "register": "REGISTER",
    "auto": "AUTO",
    "__extension__": "EXTENSION",
    "__asm__": "_ASM",
    "__int64": "INT64",  # MS extension. unsigned __int64_t も使用できる
    "_Bool": "BOOL",  # MS extension
}

_A = re.ASCII

# 800U, 0xffLL など（整数リテラルに共通の修飾子）
_IQ = "([Uu][Ll][Ll]|[Uu][Ll]|[Uu]|[Ll][Ll]|[Ll])?"

_COMMENT_END = re.compile(r"\A\*/", _A)
_ANY_CHAR = re.compile(r"\A.", _A)

# Ruby 版の case 文の when の順に並べる
_MAIN: list[tuple[str, re.Pattern[str]]] = [
    ("space", re.compile(r"\A\s+", _A)),
    ("ident", re.compile(r"\A[a-zA-Z_]\w*", _A)),
    ("HEX_CONSTANT", re.compile(r"\A0x[0-9A-Fa-f]+" + _IQ, _A)),
    ("OCTAL_CONSTANT", re.compile(r"\A0[0-7]+" + _IQ, _A)),
    ("FLOATING_CONSTANT", re.compile(r"\A[0-9]+\.([0-9]*)?([Ee][+-]?[0-9]+)?", _A)),
    ("INTEGER_CONSTANT", re.compile(r"\A\d+" + _IQ, _A)),
    ("CHARACTER_LITERAL", re.compile(r"\A'(?:[^'\\]|\\.)'", _A)),
    ("STRING_LITERAL", re.compile(r'\A"(?:[^"\\]|\\.)*"', _A)),
    ("line_comment", re.compile(r"\A//.*$", _A)),
    ("comment", re.compile(r"\A/\*", _A)),
    ("op", re.compile(r"\A(?:>>=|<<=|>>|<<)", _A)),
    ("op", re.compile(r"\A(?:\+=|\-=|\*=|/=|%=|&=|\|=|\^=)", _A)),
    ("op", re.compile(r"\A(?:::|==|!=|>=|<=|\->|\+\+|\-\-)", _A)),
    ("op", re.compile(r"\A(?:\|\||&&)", _A)),
    ("op", re.compile(r"\A.", _A)),
]

# Ruby の String#rstrip が取り除く文字
_RSTRIP_CHARS = " \t\n\v\f\r\0"

_LEADING_DIGITS = re.compile(r"\A\d+", _A)


def _ruby_to_i(text: str) -> int:
    """Ruby の String#to_i（先頭の数字だけを10進で読む。"800U" は 800）。"""
    m = _LEADING_DIGITS.match(text)
    return int(m.group()) if m else 0


def lex_files(files: list[str], q: list[Any], reader: Reader = _read_file) -> None:
    """files を順に走査し、(トークン種別, Token) を q に積む。

    コメント中という状態は、ファイルをまたいで引き継ぐ（Ruby 版と同じ）。
    """
    conv = _value_converter()
    state = {"comment": False}
    for file in files:
        lineno = 1
        try:
            for line in _lines(file, reader):
                _lex_line(line.rstrip(_RSTRIP_CHARS), file, lineno, q, state, conv)
                lineno += 1
        except (OSError, LexError) as evar:
            Generator.error("B1002 while open or reading '$1'", file)
            print_exception(evar)


def _lex_line(
    line: str, file: str, lineno: int, q: list[Any], state: dict[str, Any], conv: Any
) -> None:
    col = 1
    while line:
        if state["comment"]:
            m = _COMMENT_END.match(line)
            if m:
                state["comment"] = False
            else:
                m = _ANY_CHAR.match(line)
        else:
            m = _lex_main(line, file, lineno, col, q, state, conv)
        if m is None:
            # Ruby 版では $' が nil になり、NoMethodError が B1002 として報告される
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
        m = pattern.match(line)
        if m is None:
            continue
        text = m.group()
        if kind == "space" or kind == "line_comment":
            pass
        elif kind == "ident":
            q.append((RESERVED.get(text, "IDENTIFIER"), Token(text, file, lineno, col)))
        elif kind == "INTEGER_CONSTANT":
            q.append((kind, Token(_ruby_to_i(text), file, lineno, col)))
        elif kind == "comment":
            state["comment"] = True
        elif kind == "op":
            value = conv(text)
            q.append((value, Token(value, file, lineno, col)))
        else:
            q.append((kind, Token(conv(text), file, lineno, col)))
        return m
    return None
