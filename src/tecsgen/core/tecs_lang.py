"""tecs_lang.rb の移植。言語・文字コードの決定、メッセージ表の読み込み、Console。

Ruby 版はクラス本体が require 時に実行されて設定を決める。Python 版では、
オプション解析の後（Ruby と同じ順序）に `TECS_LANG.setup()` を呼ぶ。
"""

from __future__ import annotations

import importlib
import os
import re
import subprocess
from collections.abc import Mapping
from types import ModuleType
from typing import ClassVar

from tecsgen.context import (
    KCONV_BINARY,
    KCONV_EUC,
    KCONV_SJIS,
    KCONV_UTF8,
    TecsgenContext,
    dbg_print,
    get_context,
)
from tecsgen.ruby_compat import puts_str, rb_print, write_stdout

# デフォルトの設定（正規化済みのこと）
LANG_FILE_DEFAULT = "en_US"
CHARSET_FILE_DEFAULT = None
LANG_CONSOLE_DEFAULT = "en_US"
CHARSET_CONSOLE_DEFAULT = None

# -k で指定可能なコード
CODE_TYPE_ARRAY = ["euc", "sjis", "none", "utf8"]


class TecsLangError(SystemExit):
    """-k に不正な値が指定された（Ruby 版は `exit 1`）。"""


class TECS_LANG:  # Ruby と同名
    # ハッシュのタグは case insensitive のため、大文字の文字列とする
    CHARSET_ALIAS: ClassVar[dict[str, str]] = {
        "UJIS": "eucJP",
        "UTF-8": "utf8",
        "EUCJP": "eucJP",
        "SJIS": "sjis",
        "UTF8": "utf8",
        "ISO8859-1": "iso8859-1",
    }
    LANG_ALIAS: ClassVar[dict[str, str]] = {
        "C": "en_US",
        "EN_US": "en_US",
        "JA_JP": "ja_JP",
    }
    SUITABLE_CHARSET: ClassVar[dict[str, list[str | None]]] = {
        "ja_JP": ["eucJP", "sjis", "utf8"],
        "en_US": ["iso8859-1", "utf8", None],
    }

    _LANG_RE = re.compile(r"([^\.@]*)(\.([^@]*))?(@(.*))?")

    @staticmethod
    def parse_lang(lang: str) -> tuple[str | None, str | None, str | None]:
        """LANG のパース。"ja_JP.eucJP@cjknarrow" → ("ja_JP", "eucJP", "cjknarrow")"""
        m = TECS_LANG._LANG_RE.match(lang)
        assert m is not None  # 空文字列にも一致する
        lang_terri = m.group(1) or None
        codeset = m.group(3) or None
        modifier = m.group(5) or None
        return lang_terri, codeset, modifier

    @classmethod
    def resolve_alias_and_check(
        cls, lang: str | None, charset: str | None
    ) -> tuple[str | None, str | None, bool]:
        """lang, charset の別名解決および妥当性のチェック。"""
        ln = cls.LANG_ALIAS.get(_upcase(lang), lang)
        cs = cls.CHARSET_ALIAS.get(_upcase(charset), charset)
        suitable = cls.SUITABLE_CHARSET.get(ln) if ln is not None else None
        res = suitable is not None and cs in suitable
        return ln, cs, res

    @staticmethod
    def get_win_codepage() -> str | None:
        """codepage を取り出す（3〜5桁の整数と仮定）。"""
        out = subprocess.run(
            ["cmd", "/c", "chcp"], capture_output=True, text=True, check=False
        ).stdout
        m = re.search(r"([0-9]{3,5})", out)
        return m.group(1) if m else None

    @staticmethod
    def codepage_to_lang(cp: str | None) -> str:
        return "ja_JP.sjis" if cp == "932" else "en_US"

    @classmethod
    def set_lang_var(cls, ctx: TecsgenContext, environ: Mapping[str, str]) -> None:
        """言語、文字コードに関する変数を設定する。

        デフォルト → codepage（exerb 版のみ）→ LANG → TECSGEN_LANG → TECSGEN_FILE_LANG → -k
        の順に見て、最後に設定された値を採用する。
        """
        if ctx.in_exerb and environ.get("TERM") in (None, "cygwin"):
            lang = cls.codepage_to_lang(cls.get_win_codepage())
            ctx.lang_file, ctx.charset_file, _ = cls.parse_lang(lang)
            ctx.lang_console = ctx.lang_file
            ctx.charset_console = ctx.charset_file
        elif environ.get("LANG") is not None:
            ctx.lang_file, ctx.charset_file, _ = cls.parse_lang(environ["LANG"])
            ctx.lang_console = ctx.lang_file
            ctx.charset_console = ctx.charset_file

        if environ.get("TECSGEN_LANG") is not None:
            ctx.lang_file, ctx.charset_file, _ = cls.parse_lang(environ["TECSGEN_LANG"])
            ctx.lang_console = ctx.lang_file
            ctx.charset_console = ctx.charset_file

        if environ.get("TECSGEN_FILE_LANG") is not None:
            ctx.lang_file, ctx.charset_file, _ = cls.parse_lang(
                environ["TECSGEN_FILE_LANG"]
            )

        cls.set_lang_by_option(ctx)

    @staticmethod
    def set_lang_by_option(ctx: TecsgenContext) -> None:
        """-k オプションからファイル用の言語、文字コード変数を設定する。"""
        code = ctx.kcode
        if code is None:
            return
        if code not in CODE_TYPE_ARRAY:
            rb_print(f"-k: illegal kcode type {code}. ({', '.join(CODE_TYPE_ARRAY)})\n")
            raise TecsLangError(1)

        if code == "euc":
            ctx.charset_file, ctx.lang_file = "eucJP", "ja_JP"
        elif code == "sjis":
            ctx.charset_file, ctx.lang_file = "sjis", "ja_JP"
        elif code == "utf8":
            ctx.charset_file, ctx.lang_file = "utf8", "ja_JP"
        elif code == "none":
            ctx.charset_file, ctx.lang_file = None, "en_US"

    @staticmethod
    def set_kconv_var(ctx: TecsgenContext) -> None:
        """言語情報から Kconv に関する変数を設定する。"""
        if ctx.charset_file == "eucJP":
            ctx.kconv_cdl, ctx.ruby19_file_encode = KCONV_EUC, "ASCII-8BIT"
        elif ctx.charset_file == "sjis":
            ctx.kconv_cdl, ctx.ruby19_file_encode = KCONV_SJIS, "Shift_JIS"
        elif ctx.charset_file == "utf8":
            ctx.kconv_cdl, ctx.ruby19_file_encode = KCONV_UTF8, "ASCII-8BIT"
        else:
            ctx.kconv_cdl, ctx.ruby19_file_encode = KCONV_BINARY, "ASCII-8BIT"

        ctx.kconv_console = {
            "eucJP": KCONV_EUC,
            "sjis": KCONV_SJIS,
            "utf8": KCONV_UTF8,
        }.get(ctx.charset_console or "", KCONV_BINARY)

        ctx.kconv_tecsgen = KCONV_UTF8

    @classmethod
    def setup(
        cls, ctx: TecsgenContext | None = None, environ: Mapping[str, str] | None = None
    ) -> None:
        """tecs_lang.rb のクラス本体に相当する初期化。

        言語を決め、メッセージ表を読み込み、Kconv 用の変数を設定する。
        """
        from tecsgen.core.messages import TECSMsg

        if ctx is None:
            ctx = get_context()
        if environ is None:
            environ = os.environ

        ctx.lang_file, ctx.charset_file = LANG_FILE_DEFAULT, CHARSET_FILE_DEFAULT
        ctx.lang_console, ctx.charset_console = (
            LANG_CONSOLE_DEFAULT,
            CHARSET_CONSOLE_DEFAULT,
        )

        cls.set_lang_var(ctx, environ)

        # 言語、コードのチェックと正規化
        lang_file, charset_file, res = cls.resolve_alias_and_check(
            ctx.lang_file, ctx.charset_file
        )
        if not res:
            lang_file, charset_file = LANG_FILE_DEFAULT, CHARSET_FILE_DEFAULT
        lang_console, charset_console, res = cls.resolve_alias_and_check(
            ctx.lang_console, ctx.charset_console
        )
        if not res:
            lang_console, charset_console = (
                LANG_CONSOLE_DEFAULT,
                CHARSET_CONSOLE_DEFAULT,
            )

        # メッセージモジュールをロード
        console_mod = _load_messages(f"console_{lang_console}")
        if console_mod is None:
            console_mod = _load_messages(f"console_{LANG_CONSOLE_DEFAULT}", fatal=True)
            ctx.lang_console, ctx.charset_console = (
                LANG_CONSOLE_DEFAULT,
                CHARSET_CONSOLE_DEFAULT,
            )
        else:
            ctx.lang_console, ctx.charset_console = lang_console, charset_console
        file_mod = _load_messages(f"file_{lang_file}")
        if file_mod is None:
            file_mod = _load_messages(f"file_{LANG_FILE_DEFAULT}", fatal=True)
            ctx.lang_file, ctx.charset_file = LANG_FILE_DEFAULT, CHARSET_FILE_DEFAULT
        else:
            ctx.lang_file, ctx.charset_file = lang_file, charset_file
        assert console_mod is not None and file_mod is not None
        TECSMsg.load(console_mod)
        TECSMsg.load(file_mod)

        cls.set_kconv_var(ctx)

        dbg_print(
            f"LANG_FILE={_s(ctx.lang_file)}.{_s(ctx.charset_file)}, "
            f"LANG_CONSOLE={_s(ctx.lang_console)}.{_s(ctx.charset_console)}\n"
        )
        dbg_print(f"Ruby19_File_Encode={ctx.ruby19_file_encode}\n")


def _upcase(s: str | None) -> str:
    return "" if s is None else s.upper()


def _s(s: str | None) -> str:
    return "" if s is None else s


def _load_messages(suffix: str, fatal: bool = False) -> ModuleType | None:
    """require_tecsgen_lib( "tecslib/messages/messages_#{suffix}.rb", fatal ) に相当。"""
    name = f"tecsgen.messages.messages_{suffix}"
    try:
        return importlib.import_module(name)
    except ModuleNotFoundError as e:
        if e.name != name:
            raise
        if fatal:
            raise
        return None


class Console:
    """文字コードを変換して標準出力へ書く。"""

    @staticmethod
    def print(s: str) -> None:
        write_stdout(s, get_context().console_codec)

    @staticmethod
    def puts(s: str) -> None:
        write_stdout(puts_str(s), get_context().console_codec)
