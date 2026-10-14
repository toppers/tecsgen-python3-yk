"""tcflow の C パーサ（flowlib/C_parser.y.rb の `TCFLOW_Cparser`）。

C のソースを読み、関数定義ごとの呼び出し関数・参照グローバル変数を `Function` に記録する。
文法は racc が生成した LALR 表（c_parser_tables.py）で動かし、字句解析は手書きの1行ごとの
正規表現マッチで行う（Ruby 版と同じ）。

ソースは ASCII-8BIT（バイト列）として読むので、Python 版は **latin-1 で復号した文字列**を
バイト列の代わりに使う（1文字が1バイト。桁の数え方と正規表現の挙動が Ruby と一致する）。
ファイル名も同じ表現（`to_bstr`）で持ち、出力するときに latin-1 で符号化する。

cpp を使うとき（`-c`）は、`<gen_dir>/tmp_<ファイル名>` に GCC 拡張を無効にする前置きを付けた
コピーを書いて cpp に通し、出力を `<gen_dir>/tmp_<ファイル名>_2.c` にも残す。
"""

from __future__ import annotations

import re
import sys
from collections import deque
from typing import Any, ClassVar

from tecsgen.flowlib import c_parser_tables
from tecsgen.flowlib.c_parser_actions import TcflowActions
from tecsgen.flowlib.classes import Function
from tecsgen.flowlib.ruby_errors import open_error
from tecsgen.host import get_host
from tecsgen.ruby_compat import Symbol, puts_str, sym, to_s, write_stdout
from tecsgen.syntax.racc_runtime import RaccParser

LATIN1 = "latin-1"

RESERVED = {
    "typedef": "TYPEDEF",
    "struct": "STRUCT",
    "union": "UNION",
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
    "__int8": "__INT8",
    "__int16": "__INT16",
    "__int32": "__INT32",
    "__int64": "__INT64",
    "__bool": "__BOOL",
    "return": "RETURN",
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
    "static": "STATIC",
    "register": "REGISTER",
    "auto": "AUTO",
    "switch": "SWITCH",
    "sizeof": "SIZEOF",
    "__inline__": "__INLINE__",
    "__forceinline": "__FORCEINLINE",
    "inline": "INLINE",
    "__inline": "INLINE",
    "__declspec": "__DECLSPEC",
    "__cdecl": "__CDECL",
    "__stdcall": "__STDCALL",
    "__fastcall": "__FASTCALL",
    "__extension__": "EXTENSION",
    "__asm__": "_ASM",
}

# cpp に通すソースの前置き（GCC 拡張の無効化）。@@header_lines
HEADER_LINES = """#ifndef TECS_NO_GCC_EXTENSION_SUPPORT

/*
 * these extension can be eliminated also by spefcifying option
 * --no-gcc-extension-support for tecsgen.
 */
#ifdef __GNUC__

#ifndef __attribute__
#define __attribute__(x)
#endif

#ifndef __extension__
#define __extension__
#endif

#ifndef __builtin_va_list
typedef char  *__builtin_va_list;
// #define __builtin_va_list va_list
#endif

#ifndef restrict
#define restrict
#define __restrict
#endif

#define __asm__(x)

#define __builtin_offsetof( x, y )  (1)

#endif /* ifdef __GNUC__ */
#endif /* TECS_NO_GCC_EXTENSION_SUPPORT */
"""

_INTEGER_QUALIFIER = r"([Uu](LL|ll|L|l)|(LL|ll|L|l)[Uu]?|[Uu])?"
_A = re.ASCII  # Ruby の \w・\d・\s は ASCII-8BIT では ASCII だけ

_DIRECTIVE_LINE = re.compile(r'#\s+(\d+)\s+"(.*)".*$', _A)  # cpp の行番号情報
_DIRECTIVE = re.compile(r"#.*$", _A)
_SPACE = re.compile(r"\s+", _A)
_IDENTIFIER = re.compile(r"[a-zA-Z_]\w*", _A)
# 浮動小数点定数（3種）、16 進・8 進・10 進の整数定数、文字、文字列。Ruby 版と同じ順に試す
_NUMBERS = (
    (
        "FLOATING_CONSTANT",
        re.compile(r"[0-9]+\.([0-9]*)?([Ee][+-]?[0-9]+)?([Ff]|[Ll])?", _A),
    ),
    ("FLOATING_CONSTANT", re.compile(r"\.[0-9]+([Ee][+-]?[0-9]+)?([Ff]|[Ll])?", _A)),
    ("FLOATING_CONSTANT", re.compile(r"[0-9]+[Ee][+-]?[0-9]+([Ff]|[Ll])?", _A)),
    ("HEX_CONSTANT", re.compile(r"0x[0-9A-Fa-f]+" + _INTEGER_QUALIFIER, _A)),
    ("OCTAL_CONSTANT", re.compile(r"0[0-7]+" + _INTEGER_QUALIFIER, _A)),
    ("INTEGER_CONSTANT", re.compile(r"\d+" + _INTEGER_QUALIFIER, _A)),
    ("CHARACTER_LITERAL", re.compile(r"'(?:[^'\\]|\\.){1,4}'", _A)),
    ("STRING_LITERAL", re.compile(r'"(?:[^"\\]|\\.)*"', _A)),
)
_LINE_COMMENT = re.compile(r"//.*$", _A)
# 2文字以上の演算子。Ruby 版の when の並びのまま（先に書いたものが優先）
_OPERATORS = (
    ">>=", "<<=", ">>", "<<", "||", "&&", "->", "++", "--",
    "+=", "-=", "*=", "/=", "%=", "&=", "|=", "^=", "...",
    "::", "==", "!=", ">=", "<=",
)  # fmt: skip

_RSTRIP_CHARS = " \t\n\v\f\r\0"  # Ruby の String#rstrip

_RESET_NO_TYPE_NAME = frozenset({";", ":", ",", "(", ")", "{", "}"})
_SET_NO_TYPE_NAME = frozenset({".", "->"})

_EOF = object()  # ファイルの終わり（Ruby 版の :EOF）


def to_bstr(s: str) -> str:
    """ファイル名などを、バイト列を latin-1 で復号した表現にする。"""
    return s.encode("utf-8", errors="surrogateescape").decode(LATIN1)


def from_bstr(s: str) -> str:
    """`to_bstr` の逆。"""
    return s.encode(LATIN1).decode("utf-8", errors="surrogateescape")


def out(text: str) -> None:
    """バイト列表現の文字列を標準出力へ書く。"""
    write_stdout(text, LATIN1)


def err(text: str) -> None:
    """バイト列表現の文字列を標準エラー出力へ書く。"""
    sys.stderr.flush()
    buffer = getattr(sys.stderr, "buffer", None)
    if buffer is None:
        sys.stderr.write(text)
        return
    buffer.write(text.encode(LATIN1, errors="replace"))
    buffer.flush()


class Token:
    """字句。val は識別子なら Symbol、ほかは文字列。"""

    __slots__ = ("col", "file", "lineno", "val")

    def __init__(self, val: Any, file: str | None, lineno: int, col: int) -> None:
        self.val = val
        self.file = file
        self.lineno = lineno
        self.col = col

    def to_s(self) -> str:
        return to_s(self.val)

    def to_sym(self) -> Symbol:
        return sym(self.val)

    def locale(self) -> list[Any]:
        return [self.file, self.lineno, self.col]

    # Ruby 版の Token#eql?・== （Symbol・Token・String 以外との比較は ArgumentError）
    def __eq__(self, other: object) -> bool:
        if isinstance(other, Symbol):
            return self.val == other
        if isinstance(other, Token):
            return self.val == other.val
        if isinstance(other, str):
            return to_s(self.val) == other
        raise ValueError("ArgumentError")

    __hash__ = object.__hash__


class TcflowCparser(TcflowActions, RaccParser):
    TABLES = c_parser_tables

    # Ruby 版のクラス変数 @@current_locale・@@n_error・@@n_warning
    current_locale: ClassVar[list[Any]] = []
    n_error: ClassVar[int] = 0
    n_warning: ClassVar[int] = 0

    def __init__(self, gen_dir: str = "gen", print_all_token: bool = False) -> None:
        super().__init__()
        self._gen_dir = gen_dir
        self._print_all_token = print_all_token
        self._current_function: Function | None = None
        self._type_name_list: dict[Any, Any] = {}
        self._b_no_type_name = False
        self._q: deque[Any] = deque()
        self._processing_file: str | None = None
        self._comment = False

    @classmethod
    def reset(cls) -> None:
        """クラス変数を初期状態に戻す（Ruby 版には無い。1プロセスで複数回実行するテスト用）。"""
        cls.current_locale = []
        cls.n_error = 0
        cls.n_warning = 0

    def finalize(self) -> None:
        pass

    def _current_locale_ref(self) -> list[Any]:
        return type(self).current_locale

    # --- 構文解析 -------------------------------------------------------------

    def parse(self, files: list[str], cpp_cmd: str | None) -> None:
        """`files` を読んで構文解析する。cpp_cmd があれば cpp に通す。"""
        self._current_function = None
        self._type_name_list = {}
        self._b_no_type_name = False
        self._q = deque([_EOF])
        self._processing_file = None
        self._comment = False

        host = get_host()
        for file in files:
            file2_name = ""
            if cpp_cmd:
                file2_name = f"{self._gen_dir}/tmp_{file[file.rfind('/') + 1 :]}"
                try:
                    f = host.open_write(file2_name)
                except OSError as e:
                    raise open_error(e, file2_name) from e
                with f:
                    try:
                        src = host.read_bytes(file)
                    except OSError as e:
                        raise open_error(e, file) from e
                    f.write(HEADER_LINES.encode("ascii"))
                    f.write(_puts_lines(src))
            bfile = to_bstr(file)
            self._processing_file = bfile
            err(f"reading {bfile}\n")
            try:
                if cpp_cmd:
                    data = host.popen_read(f"{cpp_cmd} {file2_name}")
                    file3 = host.open_write(f"{file2_name}_2.c")
                else:
                    file3 = None
                    try:
                        data = host.read_bytes(file)
                    except OSError as e:
                        raise open_error(e, file) from e
                try:
                    self._scan(data, bfile, file3)
                finally:
                    if file3 is not None:
                        file3.close()
                self._q.append(_EOF)
            except Exception as e:  # noqa: BLE001  Ruby の rescue => evar
                self.error(to_bstr(str(e)))

        self._q.append(None)  # 終了の印
        self.do_parse()

    # --- 字句解析 -------------------------------------------------------------

    def _scan(self, data: bytes, file: str, file3: Any) -> None:
        """1つのソース（バイト列）を行ごとに字句に分け、キューに積む。"""
        lineno = 0
        text = data.decode(LATIN1)
        lines = text.split("\n")
        if lines[-1] == "":
            lines.pop()  # 末尾の改行の後ろは行ではない
        for raw in lines:
            lineno += 1
            if file3 is not None:
                file3.write((raw + "\n").encode(LATIN1))  # file3.puts line
            col = 1
            line = raw.rstrip(_RSTRIP_CHARS)
            while line:
                if self._comment:
                    matched = "*/" if line.startswith("*/") else line[0]
                    if matched == "*/":
                        self._comment = False
                else:
                    matched, file, lineno = self._scan_token(line, file, lineno, col)
                line = line[len(matched) :]
                col += len(matched)

    def _scan_token(
        self, line: str, file: str, lineno: int, col: int
    ) -> tuple[str, str, int]:
        """行の先頭の字句を1つ切り出し、(読み取った文字列, file, lineno) を返す。"""
        m = _DIRECTIVE_LINE.match(line)
        if m:
            return m.group(0), m.group(2), int(m.group(1)) - 1
        m = _DIRECTIVE.match(line) or _SPACE.match(line)
        if m:
            return m.group(0), file, lineno
        m = _IDENTIFIER.match(line)
        if m:
            word = m.group(0)
            self._push(RESERVED.get(word, "IDENTIFIER"), sym(word), file, lineno, col)
            return word, file, lineno
        for kind, pattern in _NUMBERS:
            m = pattern.match(line)
            if m:
                self._push(kind, m.group(0), file, lineno, col)
                return m.group(0), file, lineno
        m = _LINE_COMMENT.match(line)
        if m:
            return m.group(0), file, lineno
        if line.startswith("/*"):
            self._comment = True
            return "/*", file, lineno
        for op in _OPERATORS:
            if line.startswith(op):
                self._push(op, op, file, lineno, col)
                return op, file, lineno
        ch = line[0]
        self._push(ch, ch, file, lineno, col)
        return ch, file, lineno

    def _push(self, kind: str, val: Any, file: str, lineno: int, col: int) -> None:
        self._q.append([kind, Token(val, file, lineno, col)])

    # --- racc から呼ばれる ------------------------------------------------------

    def next_token(self) -> Any:
        if not self._q:
            return None
        token = self._q.popleft()
        while token is _EOF:  # ファイルが空のとき _EOF が連続する
            self._type_name_list = {}
            if not self._q:
                return None
            token = self._q.popleft()

        if token is not None:
            type(self).current_locale = token[1].locale()
            val = token[1].val
            if val in _RESET_NO_TYPE_NAME:
                self.set_no_type_name(False)
            elif val in _SET_NO_TYPE_NAME:
                self.set_no_type_name(True)

            # 型名の識別子は TYPE_NAME に置き換える
            if not self._b_no_type_name and token[0] == "IDENTIFIER":
                if self._current_function is not None and (
                    self._current_function.is_local_var(val)
                ):
                    pass  # ローカル変数または引数
                elif self._type_name_list.get(val) is not None:
                    token[0] = "TYPE_NAME"

            if self._print_all_token:
                locale = type(self).current_locale
                out(
                    f"{to_s(locale[0])}: line {to_s(locale[1])} : {token[0]} : "
                    f"'{to_s(token[1].val)}'\n"
                )
        return token

    def set_no_type_name(self, b_no_type_name: bool) -> None:
        self._b_no_type_name = b_no_type_name

    def on_error(self, t: int, val: Any, vstack: list[Any]) -> None:
        if val == "$":
            self.error("Unexpected EOF")
        else:
            self.error(f"syntax error near '{to_s(val.val)}'")

    def error(self, msg: Any) -> None:
        cls = type(self)
        cls.n_error += 1
        locale = cls.current_locale
        file = locale[0] if len(locale) > 0 else None
        lineno = locale[1] if len(locale) > 1 else None
        out(puts_str(f"error: {to_s(file)}: line {to_s(lineno)} {to_s(msg)}"))
        if file is not None and file != self._processing_file:
            out(f"  {to_s(file)} is included from {to_s(self._processing_file)}\n")

    @classmethod
    def get_n_error(cls) -> int:
        return cls.n_error

    @classmethod
    def get_n_warning(cls) -> int:
        return cls.n_warning


def _puts_lines(src: bytes) -> bytes:
    """Ruby の `f.puts lines`（行ごとに、末尾が改行でなければ改行を足す）。"""
    if not src:
        return b"\n"
    return src if src.endswith(b"\n") else src + b"\n"
