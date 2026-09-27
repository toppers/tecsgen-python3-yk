"""generate.rb の Celltype 再オープン部分のうち、テンプレートコード（`_templ.c`・`_inline_templ.h`）、
factory による出力（`tecsgen.cfg` など）、Makefile 類、dealloc コード、名前の置換の生成。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import get_context, print_exception
from tecsgen.core.generate import AppFile, print_note
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    gsub,
    rb_print,
    rb_puts,
    to_s,
    truthy,
)


def _msg(key: str) -> str:
    from tecsgen.core.messages import TECSMsg

    return TECSMsg.get(key)


def _rx(pattern: str) -> re.Pattern[str]:
    # Ruby の正規表現の ^・$ は行頭・行末に一致する
    return re.compile(pattern, re.MULTILINE)


_RX_CT = _rx(r"(^|[^\$])\$ct\$")
_RX_CT_GLOBAL = _rx(r"(^|[^\$])\$ct_global\$")
_RX_CELL = _rx(r"(^|[^\$])\$cell\$")
_RX_CB = _rx(r"(^|[^\$])\$cb\$")
_RX_ID = _rx(r"(^|[^\$])\$id\$")
_RX_CB_PROTO = _rx(r"(^|[^\$])\$cb_proto\$")
_RX_ID_NUM = _rx(r"(^|[^\$])\$ID\$")
_RX_IDX = _rx(r"(^|[^\$])\$idx\$")
_RX_CBP = _rx(r"(^|[^\$])\$cbp\$")
_RX_CELL_GLOBAL = _rx(r"(^|[^\$])\$cell_global\$")
_RX_DOLLAR2 = _rx(r"\$\$")
_RX_BACKSLASH_NL = _rx(r"\\\n")


class CelltypeGenerateTempl:
    """テンプレートコード・factory・Makefile 類の生成。"""

    def _gen_ep_func(self: Any) -> bool:
        """`@plugin && @plugin.gen_ep_func?`"""
        return truthy(self._plugin) and truthy(self._plugin.gen_ep_func())

    def generate_template_code(self: Any) -> None:
        ctx = get_context()
        gn = to_s(self._global_name)
        if self.is_all_entry_inline():
            return
        if truthy(self._b_reuse) and not ctx.generate_all_template:
            return
        if not self._gen_ep_func():
            if ctx.generate_no_template:  # $generate_all_template より優先される
                return
            # 参考として出力するテンプレートファイルであることを示すために "_templ" を付加する
            fname = f"{ctx.gen}/{gn}_templ.{ctx.c_suffix}"
        else:
            # Plugin により生成されたセルタイプについては、修正不要なセルタイプの実装コードを生成する．
            fname = f"{ctx.gen}/{gn}.{ctx.c_suffix}"

        f = AppFile.open(fname)

        if not self._gen_ep_func():
            f.printf(_msg("template_note"), self._name, self._name)
        else:
            print_note(f, True)

        f.print(_msg("preamble_note"))
        self.gen_template_attr_access(f)
        self.gen_template_cp_fun(f)
        f.print(" *\n * #[</PREAMBLE>]# */\n\n")
        f.printf(_msg("PAC_comment"), "#_PAC_#")

        self.gen_template_private_header(f)
        if truthy(self._plugin):
            # このメソッドの引数は plugin.rb の説明を見よ
            self._plugin.gen_preamble(f, self._singleton, self._name, self._global_name)

        self.gen_template_ep_fun(f)

        f.print(_msg("postamble_note"))

        if truthy(self._plugin):
            self._plugin.gen_postamble(
                f, self._singleton, self._name, self._global_name
            )

        f.close()

    #####  celltype template

    def gen_template_private_header(self: Any, f: Any) -> None:
        f.print(
            f'#include "{to_s(self._global_name)}_tecsgen.{get_context().h_suffix}"\n\n'
        )
        f.print(
            "#ifndef E_OK\n"
            "#define\tE_OK\t0\t\t/* success */\n"
            "#define\tE_ID\t(-18)\t/* illegal ID */\n"
            "#endif\n"
            "\n"
        )

    def gen_template_attr_access(self: Any, f: Any) -> None:
        if self._n_attribute_rw > 0 or self._n_attribute_ro > 0 or self._n_var > 0:
            f.printf(_msg("CAAM_comment"), "#_CAAM_#")

        for a in self._attribute:
            if a.is_omit():
                continue
            f.printf(
                " * %-16s %-16s %-16s\n",
                a.get_name(),
                f"{to_s(a.get_type().get_type_str())} {to_s(a.get_type().get_type_str_post())}",
                f"ATTR_{to_s(a.get_name())}",
            )

        for v in self._var:
            if v.is_omit():
                continue
            f.printf(
                " * %-16s %-16s %-16s\n",
                v.get_name(),
                f"{to_s(v.get_type().get_type_str())} {to_s(v.get_type().get_type_str_post())}",
                f"VAR_{to_s(v.get_name())}",
            )

    def gen_template_types(self: Any, f: Any) -> None:
        f.printf(
            _msg("TYP_comment"),
            "#_TYP_#",
            f"{to_s(self._global_name)}_CB",
            f"{to_s(self._name)}_IDX",
        )

    def gen_template_cp_fun(self: Any, f: Any) -> None:
        if self._n_call_port > 0:
            f.print(" *\n")
            f.printf(_msg("TCPF_comment"), "#_TCPF_#")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            pn = to_s(p.get_name())
            has_array = p.get_array_size() is not None

            sig_name = to_s(p.get_signature().get_global_name())
            con_tmp = p.get_signature().get_context()
            context = f" context:{to_s(con_tmp)}" if truthy(con_tmp) else ""

            if p.is_optional():
                optional = " optional:true"
                if has_array:
                    is_join = f" *   bool_t     is_{pn}_joined(int subscript)        check if joined\n"
                else:
                    is_join = f" *   bool_t     is_{pn}_joined()                     check if joined\n"
            else:
                optional = ""
                is_join = ""

            omit = " omit:true" if p.is_omit() else ""

            if p.is_allocator_port():
                f.print(
                    f" * allocator port for {to_s(p.get_port_type()).lower()} "
                    f"port:{to_s(p.get_allocator_port().get_name())} "
                    f"func:{to_s(p.get_allocator_func_decl().get_name())} "
                    f"param: {to_s(p.get_allocator_param_decl().get_name())}\n"
                )
            elif not p.is_require():
                f.print(
                    f" * call port: {pn} signature: {sig_name}{context}{optional}{omit}\n{is_join}"
                )
            else:
                f.print(f" * require port: signature:{sig_name}{context}\n")

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                ft = fun.get_declarator().get_type()

                f.printf(" *   %-14s ", ft.get_type().get_type_str())
                if not p.is_require() or p.has_name():
                    f.print(f"{pn}_{fn}(")
                else:
                    f.print(f"{fn}(")
                delim = ""

                if has_array:
                    f.print(f"{delim} subscript")
                    delim = ","

                for param in ft.get_paramlist().get_items():
                    f.print(f"{delim} {to_s(param.get_type().get_type_str())}")
                    f.print(
                        f" {to_s(param.get_name())}{to_s(param.get_type().get_type_str_post())}"
                    )
                    delim = ","
                f.print(" );\n")

            if has_array:
                f.print(f" *       subscript:  0...(NCP_{pn}-1)\n")

            sgn = to_s(p.get_signature().get_global_name())
            if p.is_ref_desc():
                subsc = " int_t subscript " if has_array else ""
                f.print(" *   [ref_desc]\n")
                f.printf(
                    " *      %-14s %s;\n",
                    f"Descriptor( {sgn} )",
                    f"{pn}_refer_to_descriptor({subsc})",
                )
                f.printf(
                    " *      %-14s %s;\n",
                    f"Descriptor( {sgn} )",
                    f"{pn}_ref_desc({subsc})      (same as above; abbreviated version)",
                )
            if p.is_dynamic():
                subsc = "int_t subscript, " if has_array else ""
                subsc2 = " int_t subscript" if has_array else ""
                if p.is_optional():
                    f.print(" *   [dynamic, optional]\n")
                else:
                    f.print(" *   [dynamic]\n")
                f.printf(
                    " *      %-14s %s;\n",
                    "void",
                    f"{pn}_set_descriptor( {subsc}Descriptor( {sgn} ) desc )",
                )
                if p.is_optional():
                    f.printf(" *      %-14s %s;\n", "void", f"{pn}_unjoin( {subsc2} )")

    def gen_template_ep_fun(self: Any, f: Any, b_inline: bool = False) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("TEPF_comment"), "#_TEPF_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            if b_inline and not p.is_inline():  # inline ポート
                continue
            if not b_inline and p.is_inline():  # 非 inline ポート
                continue
            pn = to_s(p.get_name())

            inline_prefix = ""
            nCELLIDX = "CELLIDX"
            nCELLCB = "CELLCB"
            nGET_CELLCB = "GET_CELLCB"

            f.print(
                f"""/* #[<ENTRY_PORT>]# {pn}
 * entry port: {pn}
 * signature:  {to_s(p.get_signature().get_global_name())}
 * context:    {to_s(p.get_signature().get_context())}
"""
            )

            if p.get_array_size() is not None:
                f.print(f" * entry port array size:  NEP_{pn}\n")

            f.print(" * #[</ENTRY_PORT>]# */\n\n")

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                f.print(
                    f"""/* #[<ENTRY_FUNC>]# {pn}_{fn}
 * name:         {pn}_{fn}
 * global_name:  {gn}_{pn}_{fn}
 * oneway:       {to_s(fun.is_oneway())}
 * #[</ENTRY_FUNC>]# */
"""
                )

                if b_inline:
                    f.print("Inline ")
                functype = fun.get_declarator().get_type()
                f.printf("%s\n", functype.get_type_str())
                f.print(f"{inline_prefix}{pn}_{fn}(")
                if truthy(self._singleton):
                    delim = ""
                else:
                    f.print(f"{nCELLIDX} idx")
                    delim = ", "

                if p.get_array_size() is not None:
                    f.print(f"{delim}int_t subscript")
                    delim = ", "

                if truthy(functype.get_paramlist()):
                    items = functype.get_paramlist().get_items()
                else:
                    # ここで nil になるのは、引数なしの時に void がなかった場合
                    items = []

                for param in items:
                    f.print(delim)
                    delim = ", "
                    f.print(param.get_type().get_type_str())
                    f.print(" ")
                    f.print(param.get_name())
                    f.print(param.get_type().get_type_str_post())
                f.print(")\n")

                f.print("{\n")

                if self._gen_ep_func():
                    # このメソッドの引数は plugin.rb の説明を見よ
                    self._plugin.gen_ep_func_body(
                        f,
                        self._singleton,
                        self._name,
                        self._global_name,
                        p.get_signature().get_global_name(),
                        p.get_name(),
                        fun.get_name(),
                        f"{gn}_{pn}_{fn}",
                        functype,
                        items,
                    )
                elif not truthy(self._singleton):
                    from tecsgen.core.cdl_types import DefinedType

                    rt = functype.get_type()
                    if isinstance(rt, DefinedType) and (
                        rt.get_type_str() == "ER" or rt.get_type_str() == "ER_UINT"
                    ):
                        if not fun.is_oneway():
                            f.print("\tER\t\tercd = E_OK;\n")
                            ret_cd: str | None = "return(ercd);"
                        else:
                            ret_cd = f"{_msg('oneway_ercd_note')}\n\treturn(E_OK);"
                    else:
                        ret_cd = None
                    f.print(f"\t{nCELLCB}\t*p_cellcb = {nGET_CELLCB}(idx);\n\n")
                    f.printf(_msg("TEFB_comment"), "#_TEFB_#")
                    f.printf(
                        f"#warning \"'{pn}_{fn}' needs to be edited.\"   /* delete this line after edit */\n"
                    )
                    f.printf("\n")

                    if ret_cd is not None:
                        f.print(f"\t{ret_cd}\n")

                f.print("}\n\n")

    def generate_inline_template_code(self: Any) -> None:
        ctx = get_context()
        gn = to_s(self._global_name)
        if self._n_entry_port_inline == 0:
            return
        if truthy(self._b_reuse) and not ctx.generate_all_template:
            return
        if not self._gen_ep_func():
            if ctx.generate_no_template:  # $generate_all_template より優先される
                return
            # 参考として出力するテンプレートファイルであることを示すために "_templ" を付加する
            fname = f"{ctx.gen}/{gn}_inline_templ.{ctx.h_suffix}"
        else:
            fname = f"{ctx.gen}/{gn}_inline.{ctx.h_suffix}"
        f = AppFile.open(fname)

        self.gen_ph_guard(f, "_INLINE")

        if not self._gen_ep_func():
            f.printf(_msg("inline_template_note"), self._name, self._name)
        else:
            print_note(f, True)

        f.print(_msg("preamble_note"))
        self.gen_template_attr_access(f)
        self.gen_template_cp_fun(f)
        f.print(" *\n * #[</PREAMBLE>]# */\n\n")

        self.gen_template_ep_fun(f, True)

        f.print(_msg("postamble_note"))

        if truthy(self._plugin):
            self._plugin.gen_postamble(
                f, self._singleton, self._name, self._global_name
            )

        f.print("\n")
        self.gen_ph_endif(f, "INLINE")
        f.close()

    ##### generate tecsgen.cfg

    def generate_celltype_factory_code(self: Any) -> None:
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        ctx = get_context()
        name = to_s(self._name)
        gname = to_s(self._global_name)
        for fa in self._ct_factory_list:
            if fa.get_name() != Y.write:
                continue
            # 前後の " を取り除く
            file_name = CDLString.remove_dquote(fa.get_file_name())
            fmt = CDLString.remove_dquote(fa.get_format())
            fmt = gsub(_RX_BACKSLASH_NL, "\n", fmt)  # \\\n => \n

            # mikan 以下は subst_name で置換するように変更すべき
            file_name = gsub(
                _RX_CT, "\\1" + name, file_name
            )  # $ct$ をセルタイプ名に置換
            file_name = gsub(_RX_CT_GLOBAL, "\\1" + gname, file_name)
            fmt = gsub(_RX_CT, "\\1" + name, fmt)
            fmt = gsub(_RX_CT_GLOBAL, "\\1" + gname, fmt)
            fmt = gsub(_RX_DOLLAR2, "$", fmt)  # $$ を $ に置換

            if file_name[0:1] != "/":
                file_name = f"{ctx.gen}/{file_name}"

            try:
                cfg_file = AppFile.open(file_name)
                if ctx.debug:
                    rb_print(f"'{name}' : celltype factory format: ")
                    rb_puts(fmt)
                # format 中の \n, \r, \t, \f と \" などを置換
                cfg_file.print(CDLString.escape(fmt))
                cfg_file.puts("\n")
                cfg_file.close()
            except Exception as evar:  # noqa: BLE001  Ruby の rescue => evar
                from tecsgen.core.generate import reraise_if_not_standard_error

                reraise_if_not_standard_error(evar)
                self.cdl_error(
                    "H1004 '$1' : write error while writing factory (specify -t to get more info)",
                    file_name,
                )
                print_exception(evar)

    def generate_cell_factory_code(self: Any) -> None:
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        ctx = get_context()
        for c in self._ordered_cell_list:
            # cell のプロトタイプ宣言なら無視
            if not c.is_generate():
                continue

            name_array = self.get_name_array(c)

            for fa in self._factory_list:
                if fa.get_name() != Y.write:
                    continue
                # 前後の " を取り除く
                file_name = CDLString.remove_dquote(fa.get_file_name())
                file_name = self.subst_name(file_name, name_array)
                fmt = CDLString.remove_dquote(fa.get_format())
                fmt = gsub(_RX_BACKSLASH_NL, "\n", fmt)  # \\\n => \n

                fmt = self.subst_name(fmt, name_array)

                arg_list = fa.get_arg_list()

                if file_name[0:1] != "/":
                    file_name = f"{ctx.gen}/{file_name}"

                na: list[Any] = []  # シンボルを attribute の値に置き換えた後の引数
                if truthy(arg_list):
                    for a in arg_list:
                        if a[0] == Y.STRING_LITERAL:  # 文字列定数
                            s = CDLString.remove_dquote(a[1])
                            s = self.subst_name(s, name_array)
                            na.append(s)
                        elif a[0] == Y.IDENTIFIER:
                            param_name = a[1]  # 識別子（属性の名前）
                            attr = self.find(param_name)
                            init = attr.get_initializer()  # celltype で指定された初期値

                            # cell の join のリストから名前を探す
                            j = c.get_join_list().get_item(param_name)
                            if truthy(j):  # param_name の cell のジョインがあるか
                                init = j.get_rhs()  # cell で指定された初期値を優先

                            s = self.gen_cell_cb_init(
                                None,
                                c,
                                name_array,
                                attr.get_type(),
                                init,
                                attr.get_identifier(),
                                0,
                                True,
                            )
                            s = CDLString.remove_dquote(s)
                            na.append(s)

                try:
                    cfg_file = AppFile.open(file_name)

                    if ctx.debug:
                        rb_print(f"'{to_s(c.get_name())}' : factory format: ")
                        rb_print(fmt)
                        rb_print(" arg: ")
                        for n in na:
                            rb_print(f"'{to_s(n)}' ")
                        rb_print("\n")

                    # format 中の \n, \r, \t, \f と \" などを置換
                    cfg_file.printf(CDLString.escape(fmt), *na)
                    cfg_file.puts("\n")
                    cfg_file.close()
                except Exception as evar:  # noqa: BLE001  Ruby の rescue => evar
                    from tecsgen.core.generate import reraise_if_not_standard_error

                    reraise_if_not_standard_error(evar)
                    self.cdl_error(
                        "H1005 '$1' : write error while writing factory (specify -t to get more info)",
                        file_name,
                    )
                    print_exception(evar)

    def generate_makefile(self: Any) -> None:
        self.generate_makefile_template()
        self.generate_makefile_depend()

    def generate_makefile_template(self: Any) -> None:
        ctx = get_context()
        if ctx.generate_no_template:
            return

        # Makefile.templ の生成（追記）
        gn = to_s(self._global_name)
        f = AppFile.open(f"{ctx.gen}/Makefile.templ")
        f.print(
            f"$(_TECS_OBJ_DIR){gn}.o : {gn}.{ctx.c_suffix}\n"
            "\t$(CC) -c $(CFLAGS) -o $@ $<\n"
            " \n"
        )
        f.close()

    def generate_makefile_depend(self: Any) -> None:
        ctx = get_context()
        gn = to_s(self._global_name)
        h = ctx.h_suffix
        headers: list[str] = [
            f"$(GEN_DIR)/{gn}_tecsgen.{h}",
            f"$(GEN_DIR)/{gn}_factory.{h}",
            f"$(GEN_DIR)/global_tecsgen.{h}",
        ]

        # inline 受け口を持つか？
        if self._n_entry_port_inline > 0:
            headers.append(f"{gn}_inline.{h}")

        # 呼び口または受け口のシグニチャのヘッダ
        for p in self._port:
            if p.is_omit():
                continue
            headers.append(
                f"$(GEN_DIR)/{to_s(p.get_signature().get_global_name())}_tecsgen.{h}"
            )

        headers += self.get_depend_header_list()
        headers.sort()
        uniq: list[str] = []
        for x in headers:
            if x not in uniq:
                uniq.append(x)
        headers_s = " ".join(uniq)

        f = AppFile.open(f"{ctx.gen}/Makefile.depend")
        c = ctx.c_suffix
        f.print(
            f"""# Celltype: {to_s(self._name)}  #_MDEP_#
$(_TECS_OBJ_DIR){gn}_tecsgen.o : {gn}_tecsgen.{c} {headers_s}
$(_TECS_OBJ_DIR){gn}_templ.o : {gn}_templ.{c} {headers_s}
$(_TECS_OBJ_DIR){gn}.o : {gn}.{c} {headers_s}

"""
        )
        f.close()

    def gen_dealloc_code_for_type(
        self: Any,
        f: Any,
        type_: Any,
        dealloc_func_name: str,
        pre: str,
        name: Any,
        post: str,
        level: int,
        b_reset: bool,
        count_str: str | None = None,
    ) -> None:
        """decl 用の dealloc コードを生成。

        b_reset:: Bool:  リセット用の dealloc コードの生成 (NULL ポインタの場合 dealloc しない)
        このメソッドでは、行を出力する直前に " \\\\\\n" を出力し、行末で改行文字を出力しない。
        """
        from tecsgen.core.cdl_types import ArrayType, PtrType, StructType

        type_ = type_.get_original_type()
        indent = "\t" + "  " * (level + 1)
        if not type_.has_pointer():
            return
        elif isinstance(type_, ArrayType):
            if type_.get_type().has_pointer():
                loop_str = f"i{level}__"
                count_str = to_s(type_.get_subscript().eval_const(None))
                f.print(" \\\n")
                f.print(f"{indent}{{ int_t  {loop_str};")
                f.print(" \\\n")
                f.print(
                    f"{indent}  for( {loop_str} = 0; {loop_str} < {count_str}; {loop_str}++ ){{ "
                )

                self.gen_dealloc_code_for_type(
                    f,
                    type_.get_type(),
                    dealloc_func_name,
                    pre,
                    name,
                    f"{post}[{loop_str}]",
                    level + 2,
                    b_reset,
                )

                f.print(" \\\n")
                f.print(f"{indent}  }}")
                f.print(" \\\n")
                f.print(f"{indent}}}")
        elif isinstance(type_, StructType):
            members_decl = type_.get_members_decl()
            for md in members_decl.get_items():
                pre2 = pre + to_s(name) + post + "."
                name2 = md.get_name()
                post2 = ""
                type2 = md.get_type().get_original_type()
                cs: str | None
                if isinstance(type2, PtrType):  # mikan typedef された型
                    if truthy(type2.get_count()):
                        cs = type2.get_count().to_str(members_decl, pre2, post2)
                    elif truthy(type2.get_size()):
                        cs = type2.get_size().to_str(members_decl, pre2, post2)
                    else:
                        cs = None
                else:
                    cs = None
                self.gen_dealloc_code_for_type(
                    f,
                    md.get_type(),
                    dealloc_func_name,
                    pre2,
                    name2,
                    post2,
                    level,
                    b_reset,
                    cs,
                )
        elif isinstance(type_, PtrType):
            nm = to_s(name)
            if b_reset or type_.is_nullable():
                nullable = ""
                if not b_reset and type_.is_nullable():
                    nullable = "\t/* nullable */"
                level2 = level + 1
                indent2 = indent + "  "
                f.print(" \\\n")
                f.print(f"{indent}if( {pre}{nm}{post} ){{{nullable}")
            else:
                level2 = level
                indent2 = indent

            if type_.get_type().has_pointer():
                if truthy(count_str):
                    loop_str = f"i{level}__"
                    f.print(" \\\n")
                    f.print(f"{indent2}{{ int_t  {loop_str};")
                    f.print(" \\\n")
                    f.print(
                        f"{indent2}  for( {loop_str} = 0; {loop_str} < {count_str}; {loop_str}++ ){{ "
                    )

                    self.gen_dealloc_code_for_type(
                        f,
                        type_.get_type(),
                        dealloc_func_name,
                        pre,
                        name,
                        f"{post}[{loop_str}]",
                        level2 + 2,
                        b_reset,
                    )

                    f.print(" \\\n")
                    f.print(f"{indent2}  }}")
                    f.print(" \\\n")
                    f.print(f"{indent2}}}")
                else:
                    self.gen_dealloc_code_for_type(
                        f,
                        type_.get_type(),
                        dealloc_func_name,
                        f"(*{pre}",
                        name,
                        f"{post})",
                        level2,
                        b_reset,
                    )
            f.print(" \\\n")
            f.print(f"{indent2}{dealloc_func_name}( {pre}{nm}{post} ); ")

            if b_reset or type_.is_nullable():
                f.print(" \\\n")
                f.print(f"{indent}}}")
        else:
            raise RubyRuntimeError("UnknownType")

    def get_depend_header_list(self: Any) -> list[str]:
        return self.get_depend_header_list_([])

    def get_depend_header_list_(self: Any, celltype_list: list[Any]) -> list[str]:
        h = get_context().h_suffix
        headers: list[str] = []

        if any(ct is self for ct in celltype_list):
            return headers
        celltype_list.append(self)

        # 呼び口の結合先のセルタイプのヘッダ（最適化の場合のみ）
        # 結合先の受け口が inline の場合、inline ヘッダも
        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if p.is_omit():
                continue

            if p.is_skelton_useless() or p.is_cell_unique() or p.is_VMT_useless():
                # 最適化コード (optimize) # スケルトン不要など
                p2 = p.get_real_callee_port()
                if truthy(p2):
                    ct = p2.get_celltype()
                    headers.append(
                        f" $(GEN_DIR)/{to_s(ct.get_global_name())}_tecsgen.{h}"
                    )
                    if p2.is_inline():
                        headers.append(f" {to_s(ct.get_global_name())}_inline.{h}")
                    headers += ct.get_depend_header_list_(celltype_list)
        return headers

    def subst_name(self: Any, s: str, name_array: list[Any]) -> str:
        """$id$, $ct$, $cb$, $idx$ 置換。

        $ct$ ⇒ セルタイプ名 / $cell$ ⇒ セル名（cell が nil ならば以下の置換は行われない）/
        $cb$ ⇒ CB の C 言語名 / $cbp$ ⇒ CB へのポインタ / $cb_proto$ ⇒ CB の C 言語名プロトタイプ宣言用 /
        $id$ ⇒ $ct$_$cell_global$ / $idx$ ⇒ idx / $ID$ ⇒ id (整数の番号) /
        $ct_global$ ⇒ セルタイプ名 / $cell_global$ ⇒ セル名 / $$ ⇒ $
        """
        ct = to_s(name_array[0])  # celltype name
        cell = name_array[1]  # cell name
        cb = to_s(name_array[2])  # cell CB name
        cb_proto = to_s(name_array[4])  # cell CB name for prototype
        id_ = to_s(name_array[6])  # cell ID
        idx = to_s(name_array[7])
        cbp = to_s(name_array[8])  # cell CB pointer
        ct_global = to_s(name_array[9])
        cell_global = to_s(name_array[10])

        s = gsub(_RX_CT, "\\1" + ct, s)
        s = gsub(_RX_CT_GLOBAL, "\\1" + ct_global, s)
        if truthy(cell):
            cell_s = to_s(cell)
            s = gsub(_RX_CELL, "\\1" + cell_s, s)
            s = gsub(_RX_CB, "\\1" + cb, s)
            s = gsub(_RX_ID, "\\1" + f"{ct}_{cell_global}", s)
            s = gsub(_RX_CB_PROTO, "\\1" + cb_proto, s)
            s = gsub(_RX_ID_NUM, "\\1" + id_, s)
            s = gsub(_RX_IDX, "\\1" + idx, s)
            s = gsub(_RX_CBP, "\\1" + cbp, s)
            s = gsub(_RX_CELL_GLOBAL, "\\1" + cell_global, s)
        s = gsub(_RX_DOLLAR2, "$", s)  # $$ を $ に置換

        return s
