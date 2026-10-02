"""Ruby 版のグローバル変数を集約する設定オブジェクト（内部仕様12章）。

Ruby 版は `$force_overwrite`・`$CHARSET_FILE` などのグローバル変数で実行全体の状態を持つ。
Python 版ではそれらを `TecsgenContext` の属性へ集約し、`get_context()` で参照する。
属性名は Ruby の変数名を snake_case にしたもの（`$KCONV_CDL` → `kconv_cdl`）。

P1 で言語・文字コード・出力制御、P3 でオプションと import パスに関わる変数を定義した。
残りは各フェーズの移植時に足す。
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any

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

    # --- tecsgen.rb: オプション（initialize_global_var・analyze_option） ---
    kcode: str | None = None  # $kcode（-k）
    force_overwrite: bool = False  # $force_overwrite（-f）
    verbose: bool = False  # $verbose（-v、-t）
    debug: bool = False  # $debug（-t）
    arguments: str = ""  # $arguments（コマンドライン引数を空白区切りで連結したもの）
    unopt: bool = False  # $unopt（-U）
    unopt_entry: bool = False  # $unopt_entry（--unoptimize-entry）
    gen_base: str = "gen"  # $gen_base（-g）
    gen: str = "gen"  # $gen（-g。生成中の region によって変わる）
    generate_all_template: bool = False  # $generate_all_template
    generate_no_template: bool = False  # $generate_no_template
    idx_is_id: bool = False  # $idx_is_id（-i）
    unique_id: bool = False  # $unique_id（-u）
    dryrun: bool = False  # $dryrun（-d）
    show_tree: bool = False  # $show_tree（-s）
    yydebug: bool = False  # $yydebug（-y）
    run_dir: str = ""  # $run_dir（起動時の Dir.pwd）
    base_dir: dict[str, bool] = field(default_factory=dict)  # $base_dir
    import_path: list[str] = field(default_factory=lambda: ["."])  # $import_path（-I）
    import_path_opt: list[str] = field(default_factory=list)  # $import_path_opt
    library_path: list[str] = field(default_factory=list)  # $library_path（-L）
    define: list[str] = field(default_factory=list)  # $define（-D）
    ram_initializer: bool = False  # $ram_initializer（-R）
    region_list: dict[str, bool] = field(default_factory=dict)  # $region_list（-G）
    generating_region: Any = None  # $generating_region
    unit_test: bool = False  # $unit_test（--unit-test）
    no_banner: bool = False  # $no_banner
    print_version: bool = False  # $print_version
    target: str = "tecs"  # $target
    no_default_import_path: bool = False  # $no_default_import_path
    c_suffix: str = "c"  # $c_suffix
    h_suffix: str = "h"  # $h_suffix
    rom: bool = True  # $rom（-r で偽）
    b_cpp_specified: bool = False  # $b_cpp_specified
    b_force_apply_tool_info: bool = (
        False  # $b_force_apply_tool_info（どこでも設定されない）
    )
    cpp: str | None = None  # $cpp（-c、TECS_CPP）
    tecspath: str = ""  # $tecspath（TECSPATH）
    tecsgen_base_path: str = ""  # $tecsgen_base_path（tecsgen.rb のあるディレクトリ）
    title: str | None = None  # $title（tecsgen 以外の名前で起動するツール用）
    tool_version: str | None = None  # $tool_version
    b_no_gcc_extension_support: bool = False  # $b_no_gcc_extension_support
    tecsflow: bool = False  # $TECSFLOW（Python 版では常に偽）
    # ARGV（オプションを取り除いた残り）。Ruby 版は ARGV を書き換えて使う
    argv: list[str] = field(default_factory=list)

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


def ruby_exception_message(evar: BaseException) -> str:
    """Python の例外を、Ruby 版で同じ状況に出る例外の to_s に近い文字列にする（TBC）。

    Ruby の例外メッセージは版によって書式が変わる。正解データの Ruby 3.2 に合わせている。
    """
    if isinstance(evar, FileNotFoundError):
        return f"No such file or directory @ rb_sysopen - {evar.filename}"
    if isinstance(evar, IsADirectoryError):
        return f"Is a directory @ io_fread - {evar.filename}"
    if isinstance(evar, PermissionError):
        return f"Permission denied @ rb_sysopen - {evar.filename}"
    if type(evar).__name__ == "LexError":
        # 字句解析でどの正規表現にも当たらなかったとき、Ruby 版は $' が nil になる
        return "undefined method `empty?' for nil:NilClass"
    return str(evar)


def print_exception(evar: BaseException) -> None:
    """tecsgen.rb の print_exception。Ruby の例外メッセージを出力する。"""
    from tecsgen.ruby_compat import rb_print, rb_puts

    rb_print("*** Begin Ruby exception message ***\n")
    rb_puts(ruby_exception_message(evar))
    if _context.debug:
        import traceback

        rb_puts("#### stack trace ####")
        rb_print("".join(traceback.format_tb(evar.__traceback__)))
    rb_print("*** End Ruby exception message ***\n")
