"""Ruby の組み込み機能のうち、出力をバイト単位で一致させるのに必要な部分の再現。

- `to_s`: Ruby の `Object#to_s`（nil → ""、true → "true" など）
- `sub_first`: Ruby の `String#sub` （置換文字列中の `\\1`・`\\&`・`\\\\` などを Ruby の規則で解釈する）
- `truthy`: Ruby の真偽判定（nil と false だけが偽）
- `rb_print`・`rb_puts`: Ruby の `print`・`puts`（改行コードを変換せず、標準出力へバイト列で書く）

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
        return obj
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return _float_to_s(obj)
    if isinstance(obj, (list, tuple)):
        return inspect(obj)
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
    if isinstance(obj, str):
        return _str_inspect(obj)
    if isinstance(obj, int):
        return str(obj)
    if isinstance(obj, float):
        return _float_to_s(obj)
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


def sprintf(fmt: str, *args: Any) -> str:
    """Ruby の `sprintf`。

    `%s` の引数は Ruby の `to_s` で文字列にする。それ以外の変換は Python の `%` 演算子に任せる
    （数値書式の細かな違いは P4 で生成物と突き合わせて詰める — TBC）。
    """
    if not args:
        return fmt % ()
    converted: list[Any] = []
    specs = re.findall(r"%[-+ 0#]*(?:\*|\d+)?(?:\.(?:\*|\d+))?([a-zA-Z%])", fmt)
    it = iter(args)
    for conv in specs:
        if conv == "%":
            continue
        a = next(it)
        converted.append(to_s(a) if conv == "s" else a)
    converted.extend(it)
    return fmt % tuple(converted)


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


class RubyIO:
    """Ruby の File オブジェクトのうち、tecsgen が使う出力メソッド（print・puts・printf）を持つ。

    文字列は `codec` と `surrogateescape` で符号化し、改行コードは変換しない。
    """

    def __init__(self, path: str, mode: str, codec: str) -> None:
        if mode not in ("w", "a"):
            raise ValueError(f"unsupported mode: {mode}")
        self._file = open(path, mode + "b")  # noqa: SIM115  close() で閉じる
        self._codec = codec

    def write(self, s: str) -> None:
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
