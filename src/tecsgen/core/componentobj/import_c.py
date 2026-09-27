"""import_c.rb の移植。import_C（C のヘッダを C プリプロセッサに通して取り込む。`Import_C`）。"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.context import get_context, print_exception
from tecsgen.core.componentobj.importable import Importable
from tecsgen.core.syntaxobj.node import Node
from tecsgen.host import get_host
from tecsgen.ruby_compat import gsub, rb_print, rb_puts, to_s, truthy

_GCC_EXTENSION_DEFINES = """
#ifndef TECS_NO_GCC_EXTENSION_SUPPORT

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
#define __builtin_va_list va_list
#endif

#if 0
#ifndef __asm__
#define __asm__(x)
#endif
#endif /* 0 */

#ifndef restrict
#define restrict
#endif

#endif /* ifdef __GNUC__ */
#endif /* TECS_NO_GCC_EXTENSION_SUPPORT */
"""

_VA_LIST_DEFINES = """#ifndef NO_TECSGEN_VA_LIST
/* va_list is not supported in C_parser.y.rb */
typedef struct { int dummy; } va_list;
#endif /* NO_TECSGEN_VA_LIST */

"""

# cpp の出力の行指示（# 1 "file" など）をコメントにする（Ruby の ^・$ は行頭・行末）
_CPP_DIRECTIVE = re.compile(rb"^#(.*)$", re.MULTILINE)


class Import_C(Importable, Node):
    # ヘッダの名前文字列のリスト
    _header_list: ClassVar[dict[Any, Any]] = {}
    _header_list2: ClassVar[list[Any]] = []
    _define_list: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        Import_C._header_list = {}
        Import_C._header_list2 = []
        Import_C._define_list = {}

    def __init__(self, header: Any, define: Any = None) -> None:
        """import_C の生成（ヘッダファイルを取込む）。

        header:: Token : import_C の第一引数文字列リテラルトークン
        define:: Token : import_C の第二引数文字列リテラルトークン
        """
        from tecsgen.core.syntaxobj.cdlstring import CDLString
        from tecsgen.syntax.cdecl_parser import CdeclParser

        super().__init__()
        # ヘッダファイル名文字列から前後の "" を取り除く
        header = CDLString.remove_dquote(to_s(header))
        ctx = get_context()
        host = get_host()

        def_opt: Any = None
        if truthy(define):
            # 前後の "" を取り除く
            def_opt = CDLString.remove_dquote(to_s(define))
            # "," を -D に置き換え
            def_opt = gsub(r",", " -D ", def_opt)
            # 先頭に -D を挿入 # mikan 不適切な define 入力があった場合、CPP 時にエラー
            def_opt = gsub(re.compile(r"^", re.MULTILINE), "-D ", def_opt)

        # コマンドライン指定された DEFINE
        for d in ctx.define:
            if ctx.in_exerb:
                q = ""
            elif "'" in d:
                q = '"'
            else:
                q = "'"
            def_opt = f"{to_s(def_opt)} -D {q}{d}{q}"

        header_path = self.find_file(header)

        if header_path is None:
            self.cdl_error("S1142 $1 not found in search path", header)
            return

        base_dir = self.get_base_dir()
        base = base_dir + "/" if truthy(base_dir) else ""
        include_opt = ""
        for path in ctx.import_path:
            include_opt = f"{include_opt} -I {base}{path}"

        # 読込み済み？
        if truthy(Import_C._header_list.get(header)):
            # 第二引数 define が以前と異なる
            if to_s(Import_C._define_list.get(header)) != to_s(define):
                self.cdl_error("S1143 import_C: arg2: mismatch with previous one")
            # いずれにせよ読み込まない
            return

        # ヘッダのリストを記録
        Import_C._header_list[header] = header_path
        Import_C._header_list2.append(header)
        Import_C._define_list[header] = define

        if ctx.verbose:
            rb_print(f"import_C header={header_path}, define={to_s(define)}\n")

        tmp_c = f"{ctx.gen}/tmp_C_src.c"
        src = ""
        if not ctx.b_no_gcc_extension_support:
            src += _GCC_EXTENSION_DEFINES
        src += _VA_LIST_DEFINES
        src += f'#include "{header}"\n'
        try:
            host.write_bytes(tmp_c, src.encode("utf-8", "surrogateescape"))
        except OSError as evar:
            self.cdl_error("S1144 $1: temporary C source: open error", tmp_c)
            print_exception(evar)

        # CPP 出力用 tmp ファイル名
        tmp_header = f"{ctx.gen}/tmp_{header.replace('/', '_')}"

        # CPP コマンドラインを作成
        cmd = f"{to_s(ctx.cpp)} {to_s(def_opt)} {include_opt} {tmp_c}"

        try:
            if ctx.verbose:
                rb_puts(f"CPP: {cmd}")
            # プリプロセッサコマンドを pipe として開く
            out = host.popen_read(cmd)
            try:
                host.write_bytes(tmp_header, _convert_cpp_output(out))
            except OSError as evar:
                self.cdl_error(
                    "S1146 $1: error occured while CPP （C-PreProcessor）, check C-compiler path or command line ooptions",
                    header,
                )
                print_exception(evar)
        except OSError as evar:
            self.cdl_error(
                "S1147 $1: popen for CPP（C-PreProcessor） failed, check C-compiler path or command line ooptions",
                header,
            )
            print_exception(evar)

        # C 言語のパーサインスタンスを生成
        c_parser = CdeclParser(_host_reader)

        # tmp_header をパース
        c_parser.parse([tmp_header])

        # 終期化　パーサスタックを戻す
        c_parser.finalize()

    @classmethod
    def get_header_list(cls) -> dict[Any, Any]:
        return Import_C._header_list

    @classmethod
    def get_header_list2(cls) -> list[Any]:
        return Import_C._header_list2


def _convert_cpp_output(data: bytes) -> bytes:
    """cpp の出力を1行ずつ読み、行指示をコメントにして puts した結果（tmp_*.h の中身）。"""
    out = []
    start = 0
    while start < len(data):
        end = data.find(b"\n", start)
        line = data[start:] if end < 0 else data[start : end + 1]
        start = len(data) if end < 0 else end + 1
        line = _CPP_DIRECTIVE.sub(rb"/* \1 */", line)
        if not line.endswith(b"\n"):
            line += b"\n"  # puts は末尾が改行でなければ改行を足す
        out.append(line)
    return b"".join(out)


def _host_reader(file: str) -> bytes:
    return get_host().read_bytes(file)
