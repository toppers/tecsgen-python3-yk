"""Ruby 版のグローバル変数を集約する設定オブジェクト（内部仕様12章）。

Ruby 版は `$force_overwrite`・`$CHARSET_FILE` などのグローバル変数で実行全体の状態を持つ。
Python 版ではそれらを `TecsgenContext` の属性へ集約し、`get_context()` で参照する。
属性名は Ruby の変数名を snake_case にしたもの（`$KCONV_CDL` → `kconv_cdl`）。

P1 では言語・文字コード・出力制御に関わる変数だけを定義する。残りは各フェーズの移植時に足す。
"""

from __future__ import annotations

from dataclasses import dataclass

# Ruby の Kconv 定数に相当する値。Kconv::BINARY は「変換しない」を表す
KCONV_EUC = "EUC"
KCONV_SJIS = "SJIS"
KCONV_UTF8 = "UTF8"
KCONV_BINARY = "BINARY"

# Kconv 定数 → Python のコーデック名。BINARY は変換しないため、バイト列を保存できる utf-8 を使う
KCONV_CODECS = {
    KCONV_EUC: "euc_jp",
    KCONV_SJIS: "cp932",
    KCONV_UTF8: "utf-8",
    KCONV_BINARY: "utf-8",
}


@dataclass
class TecsgenContext:
    # --- tecs_lang.rb: 言語と文字コード ---
    lang_file: str | None = "en_US"  # $LANG_FILE
    charset_file: str | None = None  # $CHARSET_FILE
    lang_console: str | None = "en_US"  # $LANG_CONSOLE
    charset_console: str | None = None  # $CHARSET_CONSOLE
    kconv_cdl: str = KCONV_BINARY  # $KCONV_CDL
    kconv_console: str = KCONV_BINARY  # $KCONV_CONSOLE
    kconv_tecsgen: str = KCONV_UTF8  # $KCONV_TECSGEN（定数）
    ruby19_file_encode: str = "ASCII-8BIT"  # $Ruby19_File_Encode
    in_exerb: bool = False  # $IN_EXERB（Python 版では常に偽）

    # --- tecsgen.rb: オプション ---
    kcode: str | None = None  # $kcode（-k）
    force_overwrite: bool = False  # $force_overwrite（-f）
    verbose: bool = False  # $verbose（-v）
    debug: bool = False  # $debug（-d）

    @property
    def file_codec(self) -> str:
        """CDL の読み込みと生成ファイルの書き出しに使うコーデック。"""
        if self.ruby19_file_encode == "Shift_JIS":
            return "cp932"
        return KCONV_CODECS[self.kconv_cdl]

    @property
    def console_codec(self) -> str:
        """Console クラスが標準出力へ書くときのコーデック。"""
        return KCONV_CODECS[self.kconv_console]


_context = TecsgenContext()


def get_context() -> TecsgenContext:
    return _context


def reset_context() -> TecsgenContext:
    """設定を初期値に戻す。1プロセスで複数回実行するテスト用。"""
    global _context
    _context = TecsgenContext()
    return _context


def dbg_print(s: str) -> None:
    """tecsgen.rb の dbgPrint。-d のときだけ標準出力へ書く。"""
    if _context.debug:
        from tecsgen.ruby_compat import rb_print

        rb_print(s)


def dbg_printf(fmt: str, *args: object) -> None:
    """tecsgen.rb の dbgPrintf。"""
    if _context.debug:
        from tecsgen.ruby_compat import rb_print, sprintf

        rb_print(sprintf(fmt, *args))
