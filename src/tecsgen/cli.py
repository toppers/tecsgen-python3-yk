"""tecsgen.rb（トップ）の移植。コマンドラインの解析と、TECSGEN の起動（内部仕様3章）。

Ruby 版の `TECSGEN.init`（`initialize_global_var`・`analyze_option`・`load_modules`・`setup`）を
モジュールの関数にした。CLI は Ruby 版と完全互換にする（[[tecsgen-python3 P0基本方針決定]]）。
"""

from __future__ import annotations

import os
import sys
from collections.abc import Mapping
from pathlib import Path

from tecsgen.context import (
    TecsgenContext,
    dbg_print,
    get_context,
    print_exception,
)
from tecsgen.host import get_host
from tecsgen.ruby_compat import rb_print, rb_puts
from tecsgen.ruby_optparse import HelpRequested, OptionParser, OptionParserError
from tecsgen.version import VERSION

# Ruby 版の $tecsgen_base_path（tecsgen.rb のあるディレクトリ）に当たる。同梱の CDL ライブラリ
# （tecs/）はこの下にある
PACKAGE_DIR = Path(__file__).resolve().parent.as_posix()

# optparse の program_name（Ruby は File.basename($0, '.*')）
PROGRAM_NAME = "tecsgen"


class TecsgenExit(Exception):
    """Ruby の `exit n`。main で終了コードに変える。"""

    def __init__(self, status: int) -> None:
        super().__init__(status)
        self.status = status


def _stderr(s: str) -> None:
    sys.stderr.flush()
    buf = getattr(sys.stderr, "buffer", None)
    if buf is None:
        sys.stderr.write(s)
        return
    sys.stdout.flush()
    buf.write(s.encode("utf-8", "surrogateescape"))
    buf.flush()


def initialize_global_var(ctx: TecsgenContext, environ: Mapping[str, str]) -> None:
    """グローバル変数の初期値（TECSGEN.initialize_global_var）。"""
    # コマンドライン引数 (Makefile.templ へ出力)
    ctx.arguments = "".join(" " + a for a in ctx.argv)

    ctx.unopt = False
    ctx.unopt_entry = False
    ctx.gen_base = "gen"
    ctx.gen = ctx.gen_base
    ctx.generate_all_template = False
    ctx.generate_no_template = False
    ctx.idx_is_id = False
    ctx.unique_id = False
    ctx.debug = False
    ctx.dryrun = False
    ctx.show_tree = False
    ctx.verbose = False
    ctx.yydebug = False
    ctx.run_dir = get_host().getcwd()
    ctx.base_dir = {}
    ctx.import_path = ["."]
    ctx.import_path_opt = []
    ctx.library_path = [ctx.tecsgen_base_path]
    ctx.define = []
    ctx.ram_initializer = False
    ctx.region_list = {}
    ctx.generating_region = None
    ctx.unit_test = False
    ctx.kcode = None
    ctx.force_overwrite = False
    ctx.no_banner = False
    ctx.print_version = False
    ctx.target = "tecs"
    ctx.no_default_import_path = False
    ctx.c_suffix = "c"
    ctx.h_suffix = "h"

    ctx.rom = not environ.get("TECSGEN_DEFAULT_RAM")
    ctx.b_cpp_specified = False
    if ctx.cpp is None:
        ctx.cpp = "gcc -E -DTECSGEN"
    if environ.get("TECS_CPP"):
        ctx.cpp = environ["TECS_CPP"]
        ctx.b_cpp_specified = True
    if environ.get("TECSPATH"):
        ctx.tecspath = environ["TECSPATH"]
    else:
        ctx.tecspath = f"{ctx.tecsgen_base_path}/tecs"


def make_option_parser(ctx: TecsgenContext) -> OptionParser:
    parser = OptionParser()
    parser.banner = "Usage: tecsgen [options] files"

    def define(v: str) -> None:
        ctx.define.append(v)

    def generate_region(path: str) -> None:
        gen_path = path if path.startswith("::") else "::" + path
        ctx.region_list[gen_path] = True

    def import_path(path: str) -> None:
        ctx.import_path.append(path)
        ctx.import_path_opt.append(path)

    def library_path(path: str) -> None:
        ctx.library_path.append(path)

    def setter(name: str, value: object = True):
        def f() -> None:
            setattr(ctx, name, value)

        return f

    def cpp(arg: str) -> None:
        ctx.cpp = arg
        ctx.b_cpp_specified = True

    def gen(d: str) -> None:
        ctx.gen = ctx.gen_base = d

    def kcode(code: str) -> None:
        ctx.kcode = code

    def debug() -> None:
        ctx.debug = True
        ctx.verbose = True

    def c_suffix(s: str) -> None:
        ctx.c_suffix = s

    def h_suffix(s: str) -> None:
        ctx.h_suffix = s

    on = parser.on
    on("-D", "--define=def", "define cpp symbol for import_C", handler=define)
    on("-G", "--generate-region=path", "generate region", handler=generate_region)
    on("-I", "--import-path=path", "imoprt/import_C path", handler=import_path)
    on(
        "-L",
        "--library-path=path",
        "path to dir where tecsgen.rb (obsolete, unnecessary to specify -L, those passes are gotten from tecsgen.rb",
        handler=library_path,
    )
    on(
        "-R",
        "--RAM-initializer",
        "generate RAM initializer. INITIALIZE_TECS() must be called before running any TECS code.",
        handler=setter("ram_initializer"),
    )
    on("-U", "--unoptimize", "unoptimize", handler=setter("unopt"))
    on("--unoptimize-entry", "unoptimize entry port", handler=setter("unopt_entry"))
    on(
        "-c",
        "--cpp=cpp_cmd",
        "C pre-processor command used import_C (default: gcc -E -DTECSGEN), you can also specify by environment variable TECS_CPP",
        handler=cpp,
    )
    on("-d", "--dryrun", "dryrun", handler=setter("dryrun"))
    on(
        "-f",
        "--force-overwrite",
        "force overwrite all files",
        handler=setter("force_overwrite"),
    )
    on("-g", "--gen=dir", "generate dir", handler=gen)
    on(
        "-i",
        "--idx_is_id",
        "set idx_is_id to all celltypes",
        handler=setter("idx_is_id"),
    )
    on("-k", "--kcode=code", "set kanji code: euc|sjis|none|utf8", handler=kcode)
    on("-r", "--ram", "RAM only", handler=setter("rom", False))
    on("-s", "--show-tree", "show parsing tree", handler=setter("show_tree"))
    on("-t", "--generator-debug", "generator debug", handler=debug)
    on(
        "-u",
        "--unique-id",
        "assign unique id for each cell",
        handler=setter("unique_id"),
    )
    on("-v", "--verbose", "verbose mode", handler=setter("verbose"))
    on("-y", "--yydebug", "yydebug", handler=setter("yydebug"))
    on("--no-banner", "not display banner", handler=setter("no_banner"))
    on("--version", "print version", handler=setter("print_version"))
    on(
        "--unit-test",
        "unit verification (test tecsgen itself)",
        handler=setter("unit_test"),
    )
    on(
        "--generate-all-template",
        "generate all celltypes' templates",
        handler=setter("generate_all_template"),
    )
    on(
        "--generate-no-template",
        "generate no template",
        handler=setter("generate_no_template"),
    )
    on(
        "--no-default-import-path",
        "no default import path",
        handler=setter("no_default_import_path"),
    )
    on("--c-suffix=c", "C program suffix (default: c)", handler=c_suffix)
    on("--h-suffix=h", "C program header suffix (default: h)", handler=h_suffix)
    parser.version = VERSION
    parser.release = None
    return parser


def analyze_option(ctx: TecsgenContext) -> None:
    """tecsgen コマンドオプション解析（TECSGEN.analyze_option）。

    Ruby の `ARGV.options { ... parser.parse! }` は、解析エラー（OptionParser::ParseError）を
    捕まえて "tecsgen: invalid option: -x" を標準エラー出力に書き、処理を続ける。その時点で
    ARGV に残っているのは、エラーになった引数より後ろの引数だけ（それより前のオプションで
    ない引数は失われる）。これも再現する。
    """
    parser = make_option_parser(ctx)
    try:
        ctx.argv = parser.parse(ctx.argv)
    except HelpRequested:
        rb_print(parser.help())
        raise TecsgenExit(0) from None
    except OptionParserError as e:
        _stderr(f"{PROGRAM_NAME}: {e}\n")
        ctx.argv = parser.remaining

    if (
        not ctx.argv
        and not ctx.print_version
        and not ctx.unit_test
        and not ctx.tecsflow
    ):
        rb_puts(parser.help())
        raise TecsgenExit(1)


def load_modules(ctx: TecsgenContext, environ: Mapping[str, str]) -> None:
    """tecsgen モジュールのロード（TECSGEN.load_modules）。

    Python 版はモジュールを import 文で読み込むので、Ruby 版のうち、バナーの表示と
    言語の設定（tecs_lang.rb の読み込み時の処理）だけを行う。
    """
    from tecsgen.core.tecs_lang import TECS_LANG

    if ctx.title is not None:
        _stderr(
            f"{ctx.title} version {ctx.tool_version} (tecsgen version {VERSION})  \n"
        )
    elif not ctx.no_banner or ctx.print_version:
        _stderr(f"tecsgen  version {VERSION}  \n")
    if ctx.verbose:
        # Ruby 版は "ruby 3.2.3 (2024-01-18 patchlevel 157) [x86_64-linux-gnu]"（Ruby 版との差異）
        v = sys.version_info
        _stderr(f"python {v.major}.{v.minor}.{v.micro} [{sys.platform}]\n")
    if ctx.print_version and not ctx.argv and not ctx.tecsflow:
        raise TecsgenExit(0)

    # 文字コード決定のため最初に読みこむ
    TECS_LANG.setup(ctx, environ)

    if ctx.unit_test:
        raise TecsgenExit(1)


def setup(ctx: TecsgenContext) -> None:
    """$import_path・$tecspath・$target の調整と gen ディレクトリの作成（TECSGEN.setup）。"""
    from tecsgen.core.tecsgen import TECSGEN

    host = get_host()
    TECSGEN.adjust_exerb_path()

    # $import_path に環境変数 $TECSGEN およびその直下を追加
    if not ctx.no_default_import_path and ctx.tecspath != ".":
        TECSGEN.add_import_path(ctx.tecspath)
        try:
            for f in host.listdir(ctx.tecspath):
                if f not in (".", "..") and host.is_directory(ctx.tecspath + "/" + f):
                    TECSGEN.add_import_path(ctx.tecspath + "/" + f)
        except OSError:
            pass  # 無視

    # デフォルト設定
    TECSGEN.set_default_config()

    # $target の設定
    target = ctx.argv[0]
    pos = max(target.rfind(":"), target.rfind("\\"), target.rfind("/"))
    if pos >= 0:
        target = target[pos + 1 :]  # ディレクトリ区切りを除いた文字列
    pos = target.rfind(".")
    if pos >= 0:
        # Ruby の $target[0..pos-1]。pos == 0 なら 0..-1 で文字列全体になる
        target = target[:pos] if pos > 0 else target
    ctx.target = target

    # gen ディレクトリの作成
    try:
        if not host.is_directory(ctx.gen_base):
            host.mkdir(ctx.gen_base)
    except OSError:
        rb_print(
            f"Cannot mkdir {ctx.gen_base}. If the path has hierarchy, please create directory by manual.\n"
        )
        raise TecsgenExit(1) from None


def init(ctx: TecsgenContext, environ: Mapping[str, str]) -> None:
    """TECSGEN.init。"""
    initialize_global_var(ctx, environ)
    analyze_option(ctx)
    load_modules(ctx, environ)
    if not ctx.tecsflow:
        setup(ctx)
    dbg_print(f"tecspath: {ctx.tecspath}, __FILE__={PACKAGE_DIR}/cli.py\n")
    dbg_print(f"ARGV(remained): {ctx.argv}, argments={ctx.arguments}\n")


def run(
    argv: list[str],
    environ: Mapping[str, str] | None = None,
    *,
    base_path: str | None = None,
) -> int:
    """tecsgen を実行し、終了コードを返す。

    base_path は Ruby 版の $tecsgen_base_path（差分テストで Ruby 版の値を与えるために使う）。
    """
    from tecsgen.core.tecsgen import TECSGEN

    if environ is None:
        environ = os.environ
    ctx = get_context()
    ctx.argv = list(argv)
    ctx.tecsgen_base_path = base_path if base_path is not None else PACKAGE_DIR
    try:
        try:
            init(ctx, environ)
            tecsgen = TECSGEN()
            tecsgen.run1()
            tecsgen.run2()
            tecsgen.dump_tecsgen_rbdmp()
        except RecursionError:
            # Ruby の SystemStackError は StandardError ではないので、下の rescue に捕まらず、
            # Ruby 本体がメッセージとバックトレースを出して終了コード 1 で終わる
            sys.stdout.flush()
            _stderr(f"{PROGRAM_NAME}: stack level too deep (SystemStackError)\n")
            return 1
        except TecsgenExit:
            raise
        except Exception as evar:  # noqa: BLE001  Ruby の rescue => evar
            print_exception(evar)
            _stderr("tecsgen: exit because of unrecoverble error.\n")
            _stderr("   please retry after resolve early error.\n")
            _stderr(
                "   if no error has occured, please report to TOPPERS TECS WG (users@toppers.jp or com-wg@toppers.jp).\n"
            )
            return 1
    except TecsgenExit as e:
        sys.stdout.flush()
        return e.status
    sys.stdout.flush()
    return 0


def main() -> None:
    sys.exit(run(sys.argv[1:]))
