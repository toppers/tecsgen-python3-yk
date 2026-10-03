"""`-k euc`・`-k sjis` の出力を、Ruby 版（3.2.3）で確かめた挙動に合わせる処理の単体テスト。

期待値は、WSL の Ruby 3.2.3 で同じ入力を実行して得た結果（2026-10-03・04）。
"""

from __future__ import annotations

import pytest

from tecsgen.context import TecsgenContext
from tecsgen.ruby_compat import RubyEncodingError, check_shift_jis, utf8_literal
from tecsgen.syntax.cdl_lexer import InvalidByteSequence, LexError, _lines


def _use_sjis(ctx: TecsgenContext) -> None:
    ctx.ruby19_file_encode = "Shift_JIS"
    ctx.kcode = "sjis"


# --- utf8_literal -----------------------------------------------------------


def test_utf8_literal_keeps_utf8_bytes_for_other_kcodes(
    fresh_state: TecsgenContext,
) -> None:
    # Ruby は -k euc でも、プラグインの UTF-8 のリテラルを UTF-8 のバイト列のまま書く
    s = utf8_literal("日本語")
    assert s.encode("utf-8", "surrogateescape") == "日本語".encode()
    assert s.encode("euc_jp", "surrogateescape") == "日本語".encode()


def test_utf8_literal_is_converted_for_sjis(fresh_state: TecsgenContext) -> None:
    # Ruby は Shift_JIS 指定のファイルへ書くときにリテラルも Shift_JIS へ変換する
    _use_sjis(fresh_state)
    assert utf8_literal("日本語") == "日本語"


# --- check_shift_jis --------------------------------------------------------


@pytest.mark.parametrize(
    "text",
    [
        "ascii only",
        "日本語表示ソ",  # JIS X 0208（「ソ」は2バイト目が 0x5C）
        "ｱｲｳ",  # 半角カナ
        "＼",  # U+FF3C
        "―",  # U+2015
        "∵",
        "\x80",  # cp932 の 0x80（Ruby は通す）
        "",  # cp932 の 0xA0・0xFD〜0xFF
    ],
)
def test_check_shift_jis_accepts(text: str) -> None:
    check_shift_jis(text)


@pytest.mark.parametrize(
    "char",
    ["～", "∥", "－", "￠", "￡", "￢", "￤", "①", "㈱", "Ⅰ", "髙"],
)
def test_check_shift_jis_rejects_cp932_only_characters(char: str) -> None:
    # Windows-31J にあって Shift_JIS に無い文字（～ ∥ － ￠ ￡ ￢ ¦ 丸数字 ㈱ ローマ数字 髙）
    with pytest.raises(RubyEncodingError) as e:
        check_shift_jis("表示" + char)
    assert str(e.value) == (
        f"U+{ord(char):04X} to Shift_JIS in conversion from Windows-31J to UTF-8 to Shift_JIS"
    )


def test_check_shift_jis_rejects_cp932_undefined_pair() -> None:
    # 81 AD は Windows-31J として正しい並びだが、対応する Unicode が無い。
    # Python の cp932 は先頭を surrogateescape にし、後続の AD は半角カナ「ｭ」になる
    text = b"\x81\xad".decode("cp932", "surrogateescape")
    assert text == "\udc81ｭ"
    with pytest.raises(RubyEncodingError) as e:
        check_shift_jis(text)
    assert str(e.value) == (
        '"\\x81\\xAD" to UTF-8 in conversion from Windows-31J to UTF-8 to Shift_JIS'
    )


# --- 字句解析の入力 ----------------------------------------------------------


def test_lines_rejects_invalid_windows_31j(fresh_state: TecsgenContext) -> None:
    _use_sjis(fresh_state)
    # コメント中の UTF-8（cp932 としては不正）。Ruby は G1014（C ヘッダは B1002）にする
    with pytest.raises(
        InvalidByteSequence, match="invalid byte sequence in Windows-31J"
    ):
        list(_lines("x", lambda _f: "/* 日本語 */\n".encode()))


@pytest.mark.parametrize(
    "data",
    [b"/* \x81\n", b"a\x80b\n", b"\xfd\n", b"\xa0\n"],
)
def test_lines_rejects_structurally_invalid_bytes(
    fresh_state: TecsgenContext, data: bytes
) -> None:
    # 行末の孤立した先頭バイト、0x80・0xA0・0xFD〜0xFF は Ruby では不正
    _use_sjis(fresh_state)
    with pytest.raises(LexError):
        list(_lines("x", lambda _f: data))


def test_lines_accepts_valid_but_unmapped_pair(fresh_state: TecsgenContext) -> None:
    # 81 AD は Ruby では正しい並び（変換で初めて失敗する）。字句解析は通す
    _use_sjis(fresh_state)
    assert list(_lines("x", lambda _f: b'msg = "\x81\xad";\n')) == [
        'msg = "\udc81ｭ";\n'
    ]


def test_lines_reports_the_failing_line_after_earlier_lines(
    fresh_state: TecsgenContext,
) -> None:
    # 不正な行より前の行は、先に返される（Ruby 版は前の行まで字句解析してから例外になる）
    _use_sjis(fresh_state)
    it = _lines("x", lambda _f: b"ok\nbad \x80\n")
    assert next(it) == "ok\n"
    with pytest.raises(LexError):
        next(it)


def test_lines_does_not_validate_other_kcodes(fresh_state: TecsgenContext) -> None:
    # -k euc などは ASCII-8BIT（バイト列のまま）で読むので、検査しない
    assert list(_lines("x", lambda _f: b"\x80\xff\n")) == ["\x80\xff\n"]
