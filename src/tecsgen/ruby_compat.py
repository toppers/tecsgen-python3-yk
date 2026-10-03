"""Ruby の組み込み機能のうち、出力をバイト単位で一致させるのに必要な部分の再現。

- `to_s`: Ruby の `Object#to_s`（nil → ""、true → "true" など）
- `sub_first`: Ruby の `String#sub` （置換文字列中の `\\1`・`\\&`・`\\\\` などを Ruby の規則で解釈する）
- `truthy`: Ruby の真偽判定（nil と false だけが偽）
- `rb_print`・`rb_puts`: Ruby の `print`・`puts`（改行コードを変換せず、標準出力へバイト列で書く）
- `Symbol`: Ruby の Symbol（同じ綴りの String とは等しくない。Hash のキーとしても別物）
- `rb_integer`・`str_to_i`・`str_oct` など: Ruby の数値変換

標準出力の改行コードは常に LF にする（正解データは Linux 上の Ruby で採取している）。
"""

from __future__ import annotations

import math
import re
import sys
from collections.abc import Callable
from decimal import Decimal
from typing import Any, Self

# --- 真偽 -------------------------------------------------------------------


def truthy(x: Any) -> bool:
    """Ruby の真偽判定。偽は nil と false だけで、0・空文字列・空配列は真。"""
    return x is not None and x is not False


def rb_or(a: Any, b: Any) -> Any:
    """Ruby の `a || b`（値を返す。b は評価済みの値を渡す）。"""
    return a if truthy(a) else b


def rb_and(a: Any, b: Any) -> Any:
    """Ruby の `a && b`（値を返す。b は評価済みの値を渡す）。"""
    return b if truthy(a) else a


def utf8_literal(s: str) -> str:
    """UTF-8 の Ruby ソース内の文字列リテラルを、ファイルへ書いたときのバイト列のまま残す。

    Ruby 版は `-k euc` などのときも、生成ファイルを ASCII-8BIT で開いて書く。CDL から読んだ文字列は
    元のバイト列（EUC など）のまま、プラグインの UTF-8 のソースに書かれた日本語のリテラルは UTF-8
    のバイト列のままファイルに出る。`RubyIO` は surrogateescape で符号化するので、UTF-8 のバイトを
    surrogateescape の文字に直しておけば、どのコーデックでも同じバイト列で書かれる。

    例外は `-k sjis`。Ruby 版は生成ファイルを Shift_JIS 指定で開くので、UTF-8 のリテラルは書き込み時に
    Shift_JIS へ変換される。このときは変換を `RubyIO` に任せるので、文字列をそのまま返す。
    """
    from tecsgen.context import get_context

    if get_context().ruby19_file_encode == "Shift_JIS":
        return s
    return s.encode("utf-8").decode("ascii", errors="surrogateescape")


# --- to_s / inspect ---------------------------------------------------------


def to_s(obj: Any) -> str:
    """Ruby の `obj.to_s` に相当する文字列を返す。

    Python 版のモデルクラスは Ruby と同じ名前の `to_s` メソッドを持てる。
    持っていればそれを呼ぶ。
    """
    if obj is None:
        return ""
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, str):
        return str(obj)  # Symbol も String になる
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return _float_to_s(obj)
    if isinstance(obj, (list, tuple, dict)):
        return inspect(obj)
    if isinstance(obj, type):
        return class_name(obj)
    method = getattr(obj, "to_s", None)
    if callable(method):
        return method()
    return str(obj)


def inspect(obj: Any) -> str:
    """Ruby の `obj.inspect` に相当する文字列を返す。

    Ruby の Symbol は Python 版では str で表すため、`:name` ではなく `"name"` になる
    （Ruby 版との差異。内部仕様12章）。
    """
    if obj is None:
        return "nil"
    if obj is True:
        return "true"
    if obj is False:
        return "false"
    if isinstance(obj, Symbol):
        return _symbol_inspect(obj)
    if isinstance(obj, str):
        return _str_inspect(obj)
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return _float_to_s(obj)
    if isinstance(obj, type):
        return class_name(obj)
    if isinstance(obj, (list, tuple)):
        return "[" + ", ".join(inspect(o) for o in obj) + "]"
    if isinstance(obj, dict):
        if not obj:
            return "{}"
        # 正解データを採取した Ruby 3.2 の書式（3.4 以降は {"k" => v} と空白が入る）
        return (
            "{" + ", ".join(f"{inspect(k)}=>{inspect(v)}" for k, v in obj.items()) + "}"
        )
    method = getattr(obj, "inspect", None)
    if callable(method):
        return method()
    return repr(obj)


def _float_to_s(f: float) -> str:
    """Ruby の Float#to_s。

    最短で元の値に戻る桁列（Python の repr と同じ）を使い、次の規則で書式を選ぶ
    （Ruby 版の出力から導いた規則。tests/test_p1_ruby_oracle.py で Ruby と突き合わせている）:
    小数点の位置 decpt が 0 < decpt かつ（decpt < 桁数 または decpt <= 15）なら固定小数点、
    -4 < decpt <= 0 なら "0.000ddd"、それ以外は "d.ddde+XX"（指数は2桁以上）。
    """
    if math.isnan(f):
        return "NaN"
    if math.isinf(f):
        return "Infinity" if f > 0 else "-Infinity"
    if f == 0.0:
        return "-0.0" if math.copysign(1.0, f) < 0 else "0.0"
    sign = "-" if f < 0 else ""
    t = Decimal(repr(abs(f))).normalize().as_tuple()
    digits = "".join(str(d) for d in t.digits)
    exponent = t.exponent
    assert isinstance(exponent, int)
    decpt = len(digits) + exponent
    if 0 < decpt and (decpt < len(digits) or decpt <= _DBL_DIG):
        if decpt >= len(digits):
            return f"{sign}{digits}{'0' * (decpt - len(digits))}.0"
        return f"{sign}{digits[:decpt]}.{digits[decpt:]}"
    if -4 < decpt <= 0:
        return f"{sign}0.{'0' * -decpt}{digits}"
    e = decpt - 1
    frac = digits[1:] or "0"
    return f"{sign}{digits[0]}.{frac}e{'+' if e >= 0 else '-'}{abs(e):02d}"


_DBL_DIG = 15

_STR_ESCAPES = {
    '"': '\\"',
    "\\": "\\\\",
    "\n": "\\n",
    "\t": "\\t",
    "\r": "\\r",
    "\f": "\\f",
    "\v": "\\v",
    "\a": "\\a",
    "\b": "\\b",
    "\x1b": "\\e",
}


def _str_inspect(s: str) -> str:
    out = ['"']
    for i, ch in enumerate(s):
        if ch == "#" and i + 1 < len(s) and s[i + 1] in "{$@":
            out.append("\\#")
        elif ch in _STR_ESCAPES:
            out.append(_STR_ESCAPES[ch])
        elif ord(ch) < 0x20 or ord(ch) == 0x7F:
            out.append(f"\\x{ord(ch):02X}")
        else:
            out.append(ch)
    out.append('"')
    return "".join(out)


# --- String#sub -------------------------------------------------------------

_REPL_ESCAPE = re.compile(r"\\(k<(\w+)>|.)", re.DOTALL)


def _expand_replacement(repl: str, m: re.Match[str]) -> str:
    r"""Ruby の置換文字列の規則で `\1`・`\&`・`\0`・`` \` ``・`\'`・`\\`・`\k<name>` を展開する。

    それ以外の `\x` は Ruby と同じく2文字のまま残す。
    """

    def expand(e: re.Match[str]) -> str:
        c = e.group(1)
        if c.isdigit():
            n = int(c)
            if n > (m.re.groups or 0):
                return ""
            return m.group(n) or ""
        if c == "&":
            return m.group(0)
        if c == "`":
            return m.string[: m.start()]
        if c == "'":
            return m.string[m.end() :]
        if c == "\\":
            return "\\"
        if c.startswith("k<"):
            return m.group(e.group(2)) or ""
        return e.group(0)

    return _REPL_ESCAPE.sub(expand, repl)


def sub_first(pattern: str | re.Pattern[str], repl: str, s: str) -> str:
    """Ruby の `s.sub(pattern, repl)`（最初の一致だけを置換する）。"""
    rx = re.compile(pattern) if isinstance(pattern, str) else pattern
    m = rx.search(s)
    if m is None:
        return s
    return s[: m.start()] + _expand_replacement(repl, m) + s[m.end() :]


def gsub(
    pattern: str | re.Pattern[str], repl: str | Callable[[re.Match[str]], str], s: str
) -> str:
    """Ruby の `s.gsub(pattern, repl)`。"""
    rx = re.compile(pattern) if isinstance(pattern, str) else pattern
    if callable(repl):
        return rx.sub(repl, s)
    return rx.sub(lambda m: _expand_replacement(repl, m), s)


# --- sprintf ----------------------------------------------------------------


_SPEC = re.compile(r"%([-+ 0#]*)(\*|\d+)?(?:\.(\*|\d+))?([a-zA-Z%])")


def _pad_str(s: str, flags: str, width: str | None, prec: str | None) -> str:
    """`%-Ns`・`%Ns` の桁合わせを、文字数ではなくバイト数（UTF-8）で行う。

    tecsgen が CDL から読んだ文字列は、Ruby では既定でバイナリ（ASCII-8BIT）の String なので、
    sprintf の幅はバイト数で数えられる（attribute の文字列初期値の `%-40s` などで差が出る）。
    CDL の文字コードを Shift_JIS にしたとき（TECSGEN_FILE_LANG）は Shift_JIS の String になり、
    文字数で数えられる。
    """
    from tecsgen.context import get_context

    if prec is not None:
        s = s[: int(prec)]
    if width is None:
        return s
    ctx = get_context()
    if ctx.ruby19_file_encode == "ASCII-8BIT":
        n = len(s.encode(ctx.file_codec, "surrogateescape"))
    else:
        n = len(s)
    pad = int(width) - n
    if pad <= 0:
        return s
    return s + " " * pad if "-" in flags else " " * pad + s


def _sprintf_num(a: Any, conv: str) -> Any:
    """数値の変換（%d・%x・%f など）の引数を、Ruby と同じく数値に直す。

    Ruby の sprintf は整数の変換に `Integer()`、浮動小数点の変換に `Float()` を使うので、
    "10" のような文字列も受け付ける（factory の書式に属性の値を渡すときに使われる）。
    """
    if conv in "dixXobBu":
        if isinstance(a, float):
            return int(a)
        if isinstance(a, int):
            return a
        return rb_integer(a)
    if conv in "eEfgGaA":
        if isinstance(a, (int, float)) and not isinstance(a, bool):
            return float(a)
        if isinstance(a, str):
            try:
                return float(a.strip().replace("_", ""))
            except ValueError:
                raise RubyArgumentError(
                    f"invalid value for Float(): {_str_inspect(a)}"
                ) from None
        raise RubyTypeError(f"can't convert {class_name(type(a))} into Float")
    return a


def sprintf(fmt: str, *args: Any) -> str:
    """Ruby の `sprintf`。

    `%s` の引数は Ruby の `to_s` で文字列にし、幅は Ruby の String の数え方に合わせる（`_pad_str`）。
    それ以外の変換は Python の `%` 演算子に任せる。
    """
    if not args:
        return fmt % ()
    out: list[str] = []
    pos = 0
    it = iter(args)
    for m in _SPEC.finditer(fmt):
        out.append(fmt[pos : m.start()])
        pos = m.end()
        flags, width, prec, conv = m.groups()
        if conv == "%":
            out.append("%")
            continue
        try:
            if width == "*":
                width = str(next(it))
                if width.startswith("-"):  # 負の幅は左寄せ
                    flags += "-"
                    width = width[1:]
            if prec == "*":
                prec = str(next(it))
            a = next(it)
        except StopIteration:
            raise RubyArgumentError("too few arguments") from None
        if conv == "s":
            out.append(_pad_str(to_s(a), flags, width, prec))
        else:
            spec = "%" + flags + (width or "") + ("" if prec is None else "." + prec)
            out.append((spec + conv) % (_sprintf_num(a, conv),))
    out.append(fmt[pos:])
    return "".join(out)


# --- 標準出力 ---------------------------------------------------------------


def write_stdout(s: str, codec: str = "utf-8") -> None:
    """文字列を `codec` で符号化し、改行を変換せずに標準出力へ書く。

    テキスト層にたまっている出力を先に書き出してから、バイト層へ書く（出力順を保つため）。
    """
    data = s.encode(codec, errors="surrogateescape")
    out = sys.stdout
    buffer = getattr(out, "buffer", None)
    if buffer is None:
        out.write(data.decode(codec, errors="surrogateescape"))
        return
    out.flush()
    buffer.write(data)
    buffer.flush()


def puts_str(s: str) -> str:
    """Ruby の `puts` が1引数について書き出す文字列（末尾が改行でなければ改行を足す）。"""
    return s if s.endswith("\n") else s + "\n"


def rb_print(*strs: Any) -> None:
    """Ruby の `print`。"""
    write_stdout("".join(to_s(s) for s in strs))


def rb_puts(*objs: Any) -> None:
    """Ruby の `puts`。引数なしなら改行だけを書く。配列は要素ごとに1行にする。"""
    if not objs:
        write_stdout("\n")
        return
    parts: list[str] = []
    for o in objs:
        if isinstance(o, (list, tuple)):
            if not o:
                parts.append("\n")
            parts.extend(puts_str(to_s(e)) for e in o)
        else:
            parts.append(puts_str(to_s(o)))
    write_stdout("".join(parts))


# --- ファイル出力 -----------------------------------------------------------

# cp932 では表せるが Shift_JIS（JIS X 0208 の厳密な表）には無い文字のうち、Ruby の変換が通すもの
# （cp932 の 0x80・0xA0・0xFD〜0xFF の対応。Ruby 3.2.3 で cp932 の全文字を変換して確かめた）
_SHIFT_JIS_PASSTHROUGH = frozenset({0x80, 0xF8F0, 0xF8F1, 0xF8F2, 0xF8F3})


def _trail_byte(c: str) -> int | None:
    """surrogateescape の先頭バイトの次の文字が表す、元のバイト（無ければ None）。"""
    code = ord(c)
    if 0xDC80 <= code <= 0xDCFF:
        return code - 0xDC00
    try:
        return c.encode("cp932")[0]
    except UnicodeEncodeError:
        return None


def check_shift_jis(s: str) -> None:
    """Shift_JIS 指定で開いたファイルへ書く文字列が、Ruby の変換を通るか調べる。

    Ruby 版は CDL を Windows-31J で読み、Shift_JIS 指定で開いたファイルへ書くときに
    Windows-31J → UTF-8 → Shift_JIS と変換する。Windows-31J にあって Shift_JIS に無い文字
    （`～` U+FF5E・`∥`・`－` U+FF0D・丸数字・`㈱` など）があると `Encoding::UndefinedConversionError`
    になり、tecsgen は H1001 で止まる。

    surrogateescape の文字は、cp932 に対応する Unicode が無い2バイト（`81 AD` など。Windows-31J としては
    正しい並び）の先頭バイトで、Ruby 版では UTF-8 への変換ができず同じ例外になる。後続バイトは次の文字から戻す。
    """
    if s.isascii():
        return
    for i, c in enumerate(s):
        code = ord(c)
        if 0xDC80 <= code <= 0xDCFF:
            lead = code - 0xDC00
            trail = _trail_byte(s[i + 1]) if i + 1 < len(s) else None
            if trail is not None and 0x81 <= lead <= 0xFC:
                raise RubyEncodingError(
                    f'"\\x{lead:02X}\\x{trail:02X}" to UTF-8 in conversion from Windows-31J to UTF-8 to Shift_JIS'
                )
            continue
        if code < 0x80 or code in _SHIFT_JIS_PASSTHROUGH:
            continue
        try:
            c.encode("shift_jis")
        except UnicodeEncodeError:
            raise RubyEncodingError(
                f"U+{code:04X} to Shift_JIS in conversion from Windows-31J to UTF-8 to Shift_JIS"
            ) from None


class RubyIO:
    """Ruby の File オブジェクトのうち、tecsgen が使う出力メソッド（print・puts・printf）を持つ。

    文字列は `codec` と `surrogateescape` で符号化し、改行コードは変換しない。
    ファイルは `Host.open_write` で開く（差分テストでは記録を再生する Host が中身を受け取る）。
    """

    def __init__(self, path: str, mode: str, codec: str) -> None:
        from tecsgen.host import get_host

        if mode not in ("w", "a"):
            raise ValueError(f"unsupported mode: {mode}")
        self._file = get_host().open_write(path, append=mode == "a")
        self._codec = codec

    def write(self, s: str) -> None:
        if self._codec == "cp932":
            from tecsgen.context import get_context

            if get_context().ruby19_file_encode == "Shift_JIS":
                check_shift_jis(s)
        self._file.write(s.encode(self._codec, errors="surrogateescape"))

    def print(self, *strs: Any) -> None:
        self.write("".join(to_s(s) for s in strs))

    def puts(self, *objs: Any) -> None:
        if not objs:
            self.write("\n")
            return
        for o in objs:
            if isinstance(o, (list, tuple)):
                for e in o:
                    self.write(puts_str(to_s(e)))
            else:
                self.write(puts_str(to_s(o)))

    def printf(self, fmt: str, *args: Any) -> None:
        self.write(sprintf(fmt, *args))

    def close(self) -> None:
        self._file.close()

    @property
    def closed(self) -> bool:
        return self._file.closed

    def __enter__(self) -> Self:
        return self

    def __exit__(self, *exc: object) -> None:
        self.close()


# --- Symbol -----------------------------------------------------------------


class Symbol(str):
    """Ruby の Symbol。

    Ruby では `:abc == "abc"` は偽で、Hash のキーとしても別物になる。tecsgen は識別子を
    Symbol、文字列リテラルや連結の結果を String で持ち、両者を比べたり Hash を引いたりする
    箇所がある（意図せず一致しないものもある）。その挙動を再現するため、str の派生クラスに
    して、等値比較とハッシュ値だけを str と区別する。文字列としての操作（連結・書式化）の結果は
    str（Ruby の String）になる。
    """

    __slots__ = ()

    def __eq__(self, other: object) -> bool:
        return type(other) is Symbol and str.__eq__(self, other)

    def __ne__(self, other: object) -> bool:
        return not self.__eq__(other)

    def __hash__(self) -> int:
        return hash((Symbol, str.__str__(self)))

    def __repr__(self) -> str:
        return _symbol_inspect(self)


def sym(s: Any) -> Symbol:
    """Ruby の `to_sym`・`intern`・`:"..."`。"""
    if isinstance(s, Symbol):
        return s
    return Symbol(to_s(s))


class _SymbolLiterals:
    """Symbol のリテラル。Ruby の `:VAR` を `Y.VAR` と書く。"""

    def __getattr__(self, name: str) -> Symbol:
        return Symbol(name)


Y = _SymbolLiterals()


_SIMPLE_SYMBOL = re.compile(
    r"\A(?:[A-Za-z_][A-Za-z0-9_]*[?!=]?|\[\]=?|[-+*/%<>=!~^&|]+)\Z"
)


def _symbol_inspect(s: str) -> str:
    body = str.__str__(s)
    if _SIMPLE_SYMBOL.match(body):
        return ":" + body
    return ":" + _str_inspect(body)


class dualmethod:
    """Ruby の、同じ名前のクラスメソッドとインスタンスメソッド。

    Ruby では `Namespace.find(path)`（クラスメソッド）と `ns.find(name)`（インスタンスメソッド）が
    別のメソッドとして共存する。Python ではクラス属性が1つしか持てないので、クラスから引いたか
    インスタンスから引いたかで呼び分けるデスクリプタにする。

        @dualmethod
        def find(cls, path): ...      # Namespace.find
        @find.instance
        def find(self, name): ...     # ns.find

    子クラスで片方だけを上書きするときは、子クラスでも dualmethod を使い、もう片方を
    `parent_dual.cls_func` / `parent_dual.inst_func` で引き継ぐ。
    """

    def __init__(self, cls_func: Callable[..., Any]) -> None:
        self.cls_func = cls_func
        self.inst_func: Callable[..., Any] | None = None
        self.__doc__ = cls_func.__doc__

    def instance(self, inst_func: Callable[..., Any]) -> dualmethod:
        self.inst_func = inst_func
        return self

    def __get__(self, obj: Any, owner: type | None = None) -> Any:
        import types

        if obj is None:
            return types.MethodType(self.cls_func, owner)
        if self.inst_func is None:
            raise AttributeError(getattr(self.cls_func, "__name__", "dualmethod"))
        return types.MethodType(self.inst_func, obj)


def class_name(cls: type) -> str:
    """Ruby のクラス名（`obj.class.name`・`obj.class.to_s`）。"""
    name = cls.__dict__.get("RUBY_NAME")
    return name if isinstance(name, str) else cls.__name__


# --- 例外 -------------------------------------------------------------------


class RubyError(Exception):
    """Ruby の例外。`str()` は Ruby の例外の to_s（print_exception が出力する文字列）。"""


class RubyRuntimeError(RubyError):
    """`raise "message"`（RuntimeError）。"""


class RubyEncodingError(RubyError):
    """Encoding::UndefinedConversionError。"""


class RubyNoMethodError(RubyError):
    """NoMethodError。"""


class RubyNameError(RubyError):
    """NameError。"""


class RubyTypeError(RubyError):
    """TypeError。"""


class RubyArgumentError(RubyError):
    """ArgumentError。"""


def _recv_desc(recv: Any) -> str:
    if recv is None:
        return "nil:NilClass"
    if recv is True:
        return "true:TrueClass"
    if recv is False:
        return "false:FalseClass"
    if isinstance(recv, int):
        return f"{recv}:Integer"
    if isinstance(recv, float):
        return f"{_float_to_s(recv)}:Float"
    if isinstance(recv, Symbol):
        return f"{_symbol_inspect(recv)}:Symbol"
    if isinstance(recv, str):
        return f"{_str_inspect(recv)}:String"
    return f"an instance of {class_name(type(recv))}"


def no_method(name: str, recv: Any) -> RubyNoMethodError:
    """Ruby 3.2 の NoMethodError（"undefined method `x' for nil:NilClass"）。

    モデルクラスのインスタンスが受け手のときは、Ruby 3.2 のメッセージは
    `#<Class:0x...>` のようなアドレスを含むので一致しない（TBC）。
    """
    return RubyNoMethodError(f"undefined method `{name}' for {_recv_desc(recv)}")


# --- 数値変換 ---------------------------------------------------------------

_INT_PREFIX = re.compile(r"\A\s*([-+]?)(\d+(?:_\d+)*)")


def str_to_i(s: str) -> int:
    """Ruby の `String#to_i`（10進。先頭の空白と符号を許し、数字でない文字で止まる）。"""
    m = _INT_PREFIX.match(s)
    if m is None:
        return 0
    v = int(m.group(2).replace("_", ""))
    return -v if m.group(1) == "-" else v


_HEX_DIGITS = "0123456789abcdefABCDEF"


def _str_to_base(s: str, base: int) -> int:
    m = re.match(r"\A\s*([-+]?)", s)
    assert m is not None
    sign = -1 if m.group(1) == "-" else 1
    rest = s[m.end() :]
    digits = {16: _HEX_DIGITS, 8: "01234567", 2: "01"}[base]
    head = rest[:2]
    if base == 16 and head in ("0x", "0X"):
        rest = rest[2:]
    elif base == 8:
        # String#oct は 0x・0b・0o の接頭辞も解釈する
        if head in ("0x", "0X"):
            base, digits, rest = 16, _HEX_DIGITS, rest[2:]
        elif head in ("0b", "0B"):
            base, digits, rest = 2, "01", rest[2:]
        elif head in ("0o", "0O"):
            rest = rest[2:]
    out: list[str] = []
    prev_underscore = True
    for ch in rest:
        if ch in digits:
            out.append(ch)
            prev_underscore = False
        elif ch == "_" and not prev_underscore:
            prev_underscore = True
        else:
            break
    if not out:
        return 0
    return sign * int("".join(out), base)


def str_hex(s: str) -> int:
    """Ruby の `String#hex`。"""
    return _str_to_base(s, 16)


def str_oct(s: str) -> int:
    """Ruby の `String#oct`（0x・0b・0o の接頭辞も解釈する）。"""
    return _str_to_base(s, 8)


_FLOAT_PREFIX = re.compile(
    r"\A\s*[-+]?(?:\d+(?:_\d+)*(?:\.\d+(?:_\d+)*)?|\.\d+)(?:[eE][-+]?\d+)?"
)


def str_to_f(s: str) -> float:
    """Ruby の `String#to_f`（数値として読める先頭部分だけを読む）。"""
    m = _FLOAT_PREFIX.match(s)
    if m is None:
        return 0.0
    return float(m.group(0).replace("_", ""))


def rb_to_i(x: Any) -> int:
    """`x.to_i`（Integer・Float・String・nil、および to_i を持つモデルの値）。"""
    if x is None:
        return 0
    if isinstance(x, bool):
        raise no_method("to_i", x)
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            raise RubyError(_float_to_s(x))  # FloatDomainError
        return int(x)
    if isinstance(x, str):
        return str_to_i(x)
    method = getattr(x, "to_i", None)
    if callable(method):
        return method()
    raise no_method("to_i", x)


def rb_to_f(x: Any) -> float:
    """`x.to_f`。巨大な整数は Infinity になる。"""
    if x is None:
        return 0.0
    if isinstance(x, bool):
        raise no_method("to_f", x)
    if isinstance(x, int):
        try:
            return float(x)
        except OverflowError:
            return math.inf if x > 0 else -math.inf
    if isinstance(x, float):
        return x
    if isinstance(x, str):
        return str_to_f(x)
    method = getattr(x, "to_f", None)
    if callable(method):
        return method()
    raise no_method("to_f", x)


def rb_integer(x: Any) -> int:
    """`Kernel#Integer(x)`（Float は切り捨て、nil・true などは TypeError）。"""
    if x is None or isinstance(x, bool):
        cls = {None: "nil", True: "true", False: "false"}[x]
        raise RubyTypeError(f"can't convert {cls} into Integer")
    if isinstance(x, int):
        return x
    if isinstance(x, float):
        if math.isnan(x) or math.isinf(x):
            raise RubyError(_float_to_s(x))  # FloatDomainError
        return int(x)
    if isinstance(x, str):
        try:
            return int(x.strip().replace("_", ""), 0)
        except ValueError:
            raise RubyArgumentError(
                f"invalid value for Integer(): {_str_inspect(x)}"
            ) from None
    raise RubyTypeError(f"can't convert {class_name(type(x))} into Integer")


def rb_lshift(a: int, b: int) -> int:
    """Integer#<<（負のシフト量は右シフト）。"""
    return a << b if b >= 0 else a >> -b


def rb_rshift(a: int, b: int) -> int:
    """Integer#>>（負のシフト量は左シフト）。"""
    return a >> b if b >= 0 else a << -b


def rb_downcase(s: Any) -> str:
    """`x.to_s.downcase`（ASCII のみ）。"""
    return to_s(s).lower()
