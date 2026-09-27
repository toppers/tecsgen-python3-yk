"""generate.rb の Celltype 再オープン部分のうち、セルタイプヘッダ（`<celltype>_tecsgen.h`）と
factory ヘッダ（`<celltype>_factory.h`）の生成（`gen_ph_*`）。

mixin のメソッドは、モデルの属性を Ruby と同じ名前（`@x` → `self._x`）で参照するため、
`self` を `Any` と注釈している。
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import get_context
from tecsgen.core.generate import (
    AppFile,
    begin_extern_C,
    end_extern_C,
    endif_cb_type_only,
    endif_macro_only,
    ifdef_cb_type_only,
    ifndef_cb_type_only,
    ifndef_macro_only,
    print_note,
)
from tecsgen.ruby_compat import RubyRuntimeError, Y, sym, to_s, truthy


def _msg(key: str) -> str:
    from tecsgen.core.messages import TECSMsg

    return TECSMsg.get(key)


class CelltypeGeneratePH:
    """セルタイプヘッダ・factory ヘッダの生成。"""

    def generate_private_header(self: Any) -> None:
        ctx = get_context()
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_tecsgen.{ctx.h_suffix}")

        print_note(f)

        self.gen_ph_guard(f)
        self.gen_ph_info(f)
        self.gen_ph_include(f)
        ifndef_macro_only(f)
        begin_extern_C(f)
        self.gen_ph_cell_cb_type(f)
        self.gen_ph_INIB_as_CB(f)
        self.gen_ph_extern_cell(f)  # セルタイプグルコード以外は参照しない
        self.gen_ph_typedef_idx(f)  # mikan 参照するものができていない
        self.gen_ph_ep_fun_prototype(f)
        end_extern_C(f)
        endif_macro_only(f)
        self.gen_ph_include_cb_type(f)

        if self._n_entry_port_inline == 0:
            # inline がなければ CB_TYPE_ONLY とする
            # inline ありの場合、いったん define しておいて、後ですべて undef する
            ifndef_cb_type_only(f)

        self.gen_ph_base(f)
        self.gen_ph_valid_idx(f)
        if self._n_call_port_array > 0:
            self.gen_ph_n_cp(f)
        if self._n_entry_port_array > 0:
            self.gen_ph_n_ep(f)
        self.gen_ph_test_optional_call_port(f)
        self.gen_ph_get_cellcb(f)
        if self._n_attribute_rw > 0 or self._n_attribute_ro > 0 or self._n_var > 0:
            self.gen_ph_attr_access(f)
        f.print("#ifndef TECSFLOW\n")
        if self._n_call_port > 0:
            self.gen_ph_cp_fun_macro(f, False)
        f.print("#else  /* TECSFLOW */\n")
        if self._n_call_port > 0:
            self.gen_ph_cp_fun_macro(f, True)
        f.print("#endif /* TECSFLOW */\n")

        if self._n_entry_port_inline == 0:
            endif_cb_type_only(f)

        ifndef_macro_only(f)
        begin_extern_C(f)
        self.gen_ph_ep_skel_prototype(f)

        # --- CB_TYPE_ONLY の場合、ref_desc, set_desc 関数は含めない (マクロ参照するため)
        if self._n_entry_port_inline == 0:
            ifndef_cb_type_only(f)
        self.gen_ph_ref_desc_func(f)
        self.gen_ph_set_desc_func(f)
        if self._n_entry_port_inline == 0:
            endif_cb_type_only(f)
        end_extern_C(f)
        endif_macro_only(f)

        # 短縮形などのマクロ出力
        if self._n_entry_port_inline == 0:
            ifndef_cb_type_only(f)
        self.gen_ph_valid_idx_abbrev(f)
        self.gen_ph_get_cellcb_abbrev(f)
        if self._n_attribute_rw > 0 or self._n_attribute_ro > 0 or self._n_var > 0:
            self.gen_ph_attr_access_abbrev(f)
        if self._n_call_port > 0:
            self.gen_ph_cp_fun_macro_abbrev(f)
        self.gen_ph_ref_desc_macro_abbrev(f)
        self.gen_ph_set_desc_macro_abbrev(f)
        self.gen_ph_test_optional_call_port_abbrev(f)
        if self._n_entry_port > 0:
            self.gen_ph_ep_fun_macro(f)
        self.gen_ph_foreach_cell(f)  # FOREACH マクロの出力
        # CB 初期化マクロの出力．消費しないので ram_initializer フラグに関わらず出力
        self.gen_ph_cb_initialize_macro(f)
        self.gen_ph_dealloc_code(f, "")
        self.gen_ph_dealloc_code(f, "_RESET")
        if self._n_entry_port_inline == 0:
            endif_cb_type_only(f)

        f.close()

    def generate_private_header_post(self: Any) -> None:
        ctx = get_context()
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_tecsgen.{ctx.h_suffix}")

        ifndef_macro_only(f)
        self.gen_ph_inline(f)
        endif_macro_only(f)

        if self._n_entry_port_inline > 0:
            ifdef_cb_type_only(f)
            self.gen_ph_undef(f)
            endif_cb_type_only(f)

        self.gen_ph_endif(f)

        f.close()

    #####  celltype header

    def gen_ph_guard(self: Any, f: Any, post: str = "TECSGEN") -> None:
        gn = to_s(self._global_name)
        f.print(f"#ifndef {gn}_{post}_H\n")
        f.print(f"#define {gn}_{post}_H\n\n")

    def gen_ph_info(self: Any, f: Any) -> None:
        ctx = get_context()

        def yn(b: Any) -> str:
            return "yes" if truthy(b) else "no"

        f.print(
            f"""/*
 * celltype          :  {to_s(self._name)}
 * global name       :  {to_s(self._global_name)}
 * multi-domain      :  {yn(self.multi_domain())}
 * idx_is_id(actual) :  {yn(self._idx_is_id)}({yn(self._idx_is_id_act)})
 * singleton         :  {yn(self._singleton)}
 * has_CB            :  {yn(self.has_CB())}
 * has_INIB          :  {yn(self.has_INIB())}
 * rom               :  {yn(ctx.rom)}
 * CB initializer    :  {yn(self.need_CB_initializer())}
 */

"""
        )

    def gen_ph_include(self: Any, f: Any) -> None:
        ctx = get_context()
        # グローバルヘッダの include
        f.printf(_msg("IGH_comment"), "#_IGH_#")
        f.print(f'#include "global_tecsgen.{ctx.h_suffix}"\n\n')

        # シグニチャヘッダの include
        f.printf(_msg("ISH_comment"), "#_ISH_#")
        for p in self._port:
            if p.is_omit():
                continue
            hname = sym(
                f"{to_s(p.get_signature().get_global_name())}_tecsgen.{ctx.h_suffix}"
            )
            if self.header_included(hname) is False:
                f.print(f'#include "{hname}"\n')
        f.print("\n")

    def gen_ph_include_cb_type(self: Any, f: Any) -> None:
        ctx = get_context()
        if not truthy(self._b_cp_optimized):
            return

        gn = to_s(self._global_name)
        # 最適化のため参照するセルタイプの CB 型の定義を取込む
        # _CB_TYPE_ONLY を定義した上で include する
        f.printf(_msg("ICT_comment"), "#_ICT_#")

        f.print("#ifndef  TOPPERS_CB_TYPE_ONLY\n")
        f.print(f"#define  {gn}_CB_TYPE_ONLY\n")
        f.print("#define TOPPERS_CB_TYPE_ONLY\n")
        f.print("#endif  /* TOPPERS_CB_TYPE_ONLY */\n")

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
                    hname = sym(f"{to_s(ct.get_global_name())}_tecsgen.{ctx.h_suffix}")
                    if self.header_included(hname) is False:
                        f.print(f'#include "{hname}"\n')
        f.print(f"#ifdef  {gn}_CB_TYPE_ONLY\n")
        f.print("#undef TOPPERS_CB_TYPE_ONLY\n")
        f.print(f"#endif /* {gn}_CB_TYPE_ONLY */\n")

    def gen_ph_base(self: Any, f: Any) -> None:
        if truthy(self._singleton):
            return
        gn = to_s(self._global_name)
        # ID の基数および個数の define を出力
        f.printf(
            "#define %-20s %10s  /* %s #_NIDB_# */\n",
            f"{gn}_ID_BASE",
            f"({to_s(self._id_base)})",
            _msg("NIDB_comment"),
        )
        f.printf(
            "#define %-20s %10s  /* %s  #_NCEL_# */\n\n",
            f"{gn}_N_CELL",
            f"({to_s(self._n_cell_gen)})",
            _msg("NCEL_comment"),
        )

    def gen_ph_valid_idx(self: Any, f: Any) -> None:
        if truthy(self._singleton):
            return
        gn = to_s(self._global_name)
        # IDX 正当性チェックマクロの出力
        f.printf(_msg("CVI_comment"), "#_CVI_#")
        if truthy(self._idx_is_id_act):
            f.print(
                f"#define {gn}_VALID_IDX(IDX) ({gn}_ID_BASE <= (IDX) && (IDX) < {gn}_ID_BASE+{gn}_N_CELL)\n\n"
            )
        else:
            f.print(f"#define {gn}_VALID_IDX(IDX) (1)\n\n")

    def gen_ph_valid_idx_abbrev(self: Any, f: Any) -> None:
        if truthy(self._singleton):
            return
        # IDX 正当性チェックマクロ（短縮形）の出力
        f.printf(_msg("CVIA_comment"), "#_CVIA_#")
        f.print(f"#define VALID_IDX(IDX)  {to_s(self._global_name)}_VALID_IDX(IDX)\n\n")

    def _inib_single_or_multi(self: Any) -> str:
        """呼び口・属性の参照先（singleton なら INIB/CB、そうでなければ ->_inib/""）。"""
        if truthy(self._singleton):
            return "INIB" if self.has_INIB() else "CB"
        return "->_inib" if self.has_CB() and self.has_INIB() else ""

    def gen_ph_n_cp(self: Any, f: Any) -> None:
        """呼び口配列の大きさを得るマクロの出力。"""
        gn = to_s(self._global_name)
        b_comment = False
        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if p.is_omit():
                continue
            if p.get_array_size() is None:
                continue

            if not b_comment:
                f.printf(_msg("NCPA_comment"), "#_NCPA_#")
                b_comment = True

            pn = to_s(p.get_name())
            asz = to_s(p.get_array_size())
            if p.get_array_size() != "[]":  # 固定長配列
                f.print(f"#define N_CP_{pn}    ({asz})\n")
                f.print(f"#define NCP_{pn}     ({asz})\n")
            else:  # 可変長配列
                inib = self._inib_single_or_multi()
                if truthy(self._singleton):
                    f.print(f"#define N_CP_{pn}  ({gn}_SINGLE_CELL_{inib}.n_{pn})\n")
                    f.print(f"#define NCP_{pn}   ({gn}_SINGLE_CELL_{inib}.n_{pn})\n")
                    # mikan singleton ならば、固定長化できる
                else:
                    f.print(f"#define N_CP_{pn}(p_that)  ((p_that){inib}->n_{pn})\n")
                    f.print(f"#define NCP_{pn}           (N_CP_{pn}(p_cellcb))\n")

    def gen_ph_n_ep(self: Any, f: Any) -> None:
        """受け口配列の大きさを得るマクロの出力。"""
        gn = to_s(self._global_name)
        b_comment = False
        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.get_array_size() is None:
                continue

            if not b_comment:
                f.printf(_msg("NEPA_comment"), "#_NEPA_#")
                b_comment = True

            pn = to_s(p.get_name())
            if p.get_array_size() != "[]":  # 固定長配列
                f.print(f"#define NEP_{pn}     ({to_s(p.get_array_size())})\n")
            else:  # 可変長配列
                inib = self._inib_single_or_multi()
                if truthy(self._singleton):
                    f.print(f"#define NEP_{pn}   ({gn}_SINGLE_CELL_{inib}.n_{pn})\n")
                else:
                    f.print(f"#define NEP_{pn}           ((p_cellcb){inib}->n_{pn})\n")

    def gen_ph_test_optional_call_port(self: Any, f: Any) -> None:
        """optional な呼び口が結合されているかテストするコードの生成。"""
        gn = to_s(self._global_name)
        b_comment = False
        singleton = truthy(self._singleton)
        inib = self._inib_single_or_multi()

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_optional():
                continue

            if b_comment is False:
                f.printf(_msg("TOCP_comment"), "#_TOCP_#")
                b_comment = True

            if singleton:
                param = ""
                delim = ""
            else:
                param = "p_that"
                delim = ","
            if p.get_array_size() is not None:
                param = param + delim + "subscript"
            pn = to_s(p.get_name())
            f.print(f"#define {gn}_is_{pn}_joined({param}) \\\n")

            if p.is_omit():
                f.print(f"   omit  is_{pn}_joined\n")
                continue

            if not p.is_VMT_useless():
                if p.is_dynamic():
                    inib_tmp = "CB" if singleton else ""
                else:
                    inib_tmp = inib

                # 標準コード
                if p.get_array_size() is None:
                    if singleton:
                        f.print(f"\t  ({gn}_SINGLE_CELL_{inib_tmp}.{pn}!=0)\n")
                    else:
                        f.print(f"\t  ((p_that){inib_tmp}->{pn}!=0)\n")
                else:
                    # 配列の場合
                    if singleton:
                        f.print(f"\t  (({gn}_SINGLE_CELL_{inib_tmp}.{pn}!=0) \\\n")
                        f.print(
                            f"\t  &&({gn}_SINGLE_CELL_{inib_tmp}.{pn}[subscript]!=0))\n"
                        )
                    else:
                        f.print(f"\t  (((p_that){inib_tmp}->{pn}!=0)\\\n")
                        f.print(f"\t  &&((p_that){inib_tmp}->{pn}[subscript]!=0))\n")
            else:
                # 最適化コード (optimize) # VMT 不要（配列要素すべて同じ）
                p2 = p.get_real_callee_port()
                if truthy(p2):
                    # 受け口関数・受け口スケルトン関数を直接呼出す
                    f.print("\t  (1)\n")
                else:
                    # optional で未結合
                    f.print("\t  (0)    /* not joined */\n")

    def gen_ph_test_optional_call_port_abbrev(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        b_comment = False

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_optional():
                continue

            if b_comment is False:
                f.printf(_msg("TOCPA_comment"), "#_TOCPA_#")
                b_comment = True

            if truthy(self._singleton):
                param = ""
                delim = ""
            else:
                param = "p_cellcb"
                delim = ","

            if p.get_array_size() is None:
                subscript = ""
            else:
                subscript = "subscript"
                param = param + delim + subscript
            pn = to_s(p.get_name())
            f.print(
                f"#define is_{pn}_joined({subscript})\\\n\t\t{gn}_is_{pn}_joined({param})\n"
            )

    def gen_ph_get_cellcb(self: Any, f: Any) -> None:
        """CELLCB へのポインタを得るマクロを出力。"""
        gn = to_s(self._global_name)
        f.printf(_msg("GCB_comment"), "#_GCB_#")
        if (not self.has_CB() and not self.has_INIB()) or truthy(self._singleton):
            f.print(f"#define {gn}_GET_CELLCB(idx) ((void *)0)\n")
        elif truthy(self._idx_is_id_act):
            f.print(
                f"#define {gn}_GET_CELLCB(idx) ({gn}_CB_ptab[(idx) - {gn}_ID_BASE])\n"
            )
        else:
            f.print(f"#define {gn}_GET_CELLCB(idx) (idx)\n")

    def gen_ph_get_cellcb_abbrev(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        f.printf(_msg("GCBA_comment"), "#_GCBA_#")
        f.print(f"#define GET_CELLCB(idx)  {gn}_GET_CELLCB(idx)\n\n")

        f.printf(_msg("CCT_comment"), "#_CCT_#")
        f.print(f"#define CELLCB\t{gn}_CB\n\n")

        f.printf(_msg("CTIXA_comment"), "#_CTIXA_#")
        f.print(f"#define CELLIDX\t{gn}_IDX\n\n")

        if self._name != self._global_name:
            f.print(f"#define {to_s(self._name)}_IDX  {gn}_IDX\n")

    def gen_ph_attr_access(self: Any, f: Any) -> None:
        """attribute, var をアクセスするマクロを出力。"""
        gn = to_s(self._global_name)
        singleton = truthy(self._singleton)
        if self._n_attribute_rw > 0 or self._n_attribute_ro > 0:
            f.printf(_msg("AAM_comment"), "#_AAM_#")

        for a in self._attribute:
            if a.is_omit():
                continue
            an = to_s(a.get_name())
            f.print("#define ")
            if singleton:
                inib = "INIB" if self.has_INIB() else "CB"
                f.printf("%-20s", f"{gn}_ATTR_{an}")
                f.print(f"\t({gn}_SINGLE_CELL_{inib}.{an})\n")
            else:
                inib = (
                    "->_inib"
                    if not a.is_rw() and self.has_CB() and self.has_INIB()
                    else ""
                )
                f.printf("%-20s", f"{gn}_ATTR_{an}( p_that )")
                f.print(f"\t((p_that){inib}->{an})\n")
        f.print("\n")

        for a in self._attribute:
            if a.is_omit():
                continue
            an = to_s(a.get_name())
            if singleton:
                inib = "INIB" if self.has_INIB() else "CB"
            else:
                inib = (
                    "->_inib"
                    if not a.is_rw() and self.has_CB() and self.has_INIB()
                    else ""
                )

            f.print("#define ")
            if singleton:
                f.printf("%-20s", f"{gn}_GET_{an}()")
                f.print(f"\t({gn}_SINGLE_CELL_{inib}.{an})\n")
            else:
                f.printf("%-20s", f"{gn}_GET_{an}(p_that)")
                f.print(f"\t((p_that){inib}->{an})\n")

            if a.is_rw():
                f.print("#define ")
                if singleton:
                    f.printf("%-20s", f"{gn}_SET_{an}(val)")
                    f.print(f"\t({gn}_SINGLE_CELL_{inib}.{an} = (val))\n")
                else:
                    f.printf("%-20s", f"{gn}_SET_{an}(p_that,val)")
                    f.print(f"\t((p_that){inib}->{an}=(val))\n")
        f.print("\n")

        if self._n_var > 0:
            f.printf(_msg("VAM_comment"), "#_VAM_#")

        for v in self._var:
            if v.is_omit():
                continue
            vn = to_s(v.get_name())
            if singleton:
                inib = "INIB" if truthy(v.get_size_is()) and self.has_INIB() else "CB"
            else:
                inib = (
                    "->_inib"
                    if truthy(v.get_size_is()) and self.has_CB() and self.has_INIB()
                    else ""
                )

            f.print("#define ")
            if singleton:
                f.printf("%-20s", f"{gn}_VAR_{vn}")
                f.print(f"\t({gn}_SINGLE_CELL_{inib}.{vn})\n")
            else:
                f.printf("%-20s", f"{gn}_VAR_{vn}(p_that)")
                f.print(f"\t((p_that){inib}->{vn})\n")
        f.print("\n")
        for v in self._var:
            if v.is_omit():
                continue
            vn = to_s(v.get_name())
            f.print("#define ")
            if singleton:
                f.printf("%-20s", f"{gn}_GET_{vn}()")
                f.print(f"\t({gn}_SINGLE_CELL_CB.{vn})\n")
            else:
                f.printf("%-20s", f"{gn}_GET_{vn}(p_that)")
                f.print(f"\t((p_that)->{vn})\n")

            f.print("#define ")
            if singleton:
                f.printf("%-20s", f"{gn}_SET_{vn}(val)")
                f.print(f"\t({gn}_SINGLE_CELL_CB.{vn}=(val))\n")
            else:
                f.printf("%-20s", f"{gn}_SET_{vn}(p_that,val)")
                f.print(f"\t((p_that)->{vn}=(val))\n")
        f.print("\n")

    def gen_ph_attr_access_abbrev(self: Any, f: Any) -> None:
        """attribute/var アクセスマクロ（短縮形）コードの生成。"""
        gn = to_s(self._global_name)
        if self._n_attribute_rw > 0 or self._n_attribute_ro > 0:
            f.printf(_msg("AAMA_comment"), "#_AAMA_#")

        for a in self._attribute:
            if a.is_omit():
                continue
            an = to_s(a.get_name())
            f.print("#define ")
            f.printf("%-20s", f"ATTR_{an}")
            f.print(f" {gn}_ATTR_{an}")
            if not truthy(self._singleton):
                f.print("( p_cellcb )")
            f.print("\n")
        f.print("\n")

        if self._n_var > 0:
            f.printf(_msg("VAMA_comment"), "#_VAMA_#")

        for v in self._var:
            if v.is_omit():
                continue
            vn = to_s(v.get_name())
            f.print("#define ")
            f.printf("%-20s", f"VAR_{vn}")
            f.print(f" {gn}_VAR_{vn}")
            if not truthy(self._singleton):
                f.print("( p_cellcb )")
            f.print("\n")
        f.print("\n")

    def gen_ph_cp_fun_macro(self: Any, f: Any, b_flow: bool) -> None:
        gn = to_s(self._global_name)
        singleton = truthy(self._singleton)
        if self._n_call_port > 0 and b_flow is False:
            f.printf(_msg("CPM_comment"), "#_CPM_#")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            has_array = p.get_array_size() is not None

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                if singleton:
                    inib = "INIB" if self.has_INIB() else "CB"
                    if p.is_dynamic() and not has_array:
                        # dynamic call port (not array)
                        inib = "CB"
                else:
                    inib = "->_inib" if self.has_CB() and self.has_INIB() else ""
                    if p.is_dynamic() and not has_array:
                        # dynamic call port (not array)
                        inib = ""

                f.print(f"#define {gn}_{pn}_{fn}(")
                ft = fun.get_declarator().get_type()
                delim = ""

                if not singleton:
                    f.print(f"{delim} p_that")
                    delim = ","

                if has_array:
                    f.print(f"{delim} subscript")
                    delim = ","

                for param in ft.get_paramlist().get_items():
                    f.print(f"{delim} {to_s(param.get_name())}")
                    delim = ","
                f.print(" ) \\\n")

                subsc = "[subscript]" if has_array else ""
                delim = ""

                # 関数名の出力(標準：受け口ディスクリプタから VMT の関数名、最適化：受け口関数 or 受け口ディスクリプタ)
                if b_flow:
                    f.print(f"\t  (p_that)->{pn}{subsc}.{fn}__T( \\\n")
                elif not p.is_VMT_useless():
                    # 標準コード
                    if singleton:
                        f.print(f"\t  {gn}_SINGLE_CELL_{inib}.{pn}")
                    else:
                        f.print(f"\t  (p_that){inib}->{pn}")
                    f.print(f"{subsc}->VMT->{fn}__T( \\\n")
                else:
                    # 最適化コード (optimize) # VMT 不要
                    p2 = p.get_real_callee_port()
                    if truthy(p2):
                        ct = p2.get_celltype()
                        if p.is_skelton_useless():
                            # 受け口関数を直接呼出す
                            f.print(
                                f"\t  {to_s(ct.get_global_name())}_{to_s(p2.get_name())}_{fn}( \\\n"
                            )
                        else:
                            # 受け口スケルトン関数を直接呼出す
                            f.print(
                                f"\t  {to_s(ct.get_global_name())}_{to_s(p2.get_name())}_{fn}_skel( \\\n"
                            )
                    else:
                        # optional で未結合
                        rt = fun.get_declarator().get_type().get_type()
                        f.print(f"\t  (({to_s(rt.get_type_str())} (*)()")
                        f.print(f"{to_s(rt.get_type_str_post())})0)()\n")
                        f.print("\t  /* optional no entry port joined */\n")
                        if not p.is_optional():
                            raise RubyRuntimeError(
                                f"unjoined but not optional celltype: {to_s(self._name)} {pn}"
                            )

                b_join = True  # optional で結合していない場合 false

                # 受け口情報の出力(標準：受け口ディスクリプタ、最適化：IDX など)
                if b_flow:
                    pass
                elif not p.is_skelton_useless() and not p.is_cell_unique():
                    # 標準コード
                    if singleton:
                        f.print(f"\t  {gn}_SINGLE_CELL_{inib}.{pn}{subsc}")
                    else:
                        f.print(f"\t   (p_that){inib}->{pn}{subsc}")
                    delim = ","
                else:
                    # 最適化コード (optimize) # スケルトン不要
                    c2 = p.get_real_callee_cell()  # 唯一のセル(でない場合もある)
                    p2 = p.get_real_callee_port()  # 唯一のポート(でない場合は、ない)
                    if truthy(p2):
                        ct = p2.get_celltype()  # 呼び先のセルタイプ
                        if not truthy(ct.is_singleton()):
                            if ct.has_CB() or ct.has_INIB():
                                if p.is_cell_unique():
                                    name_array = ct.get_name_array(c2)
                                    f.print(f"\t   {to_s(name_array[7])}")
                                else:
                                    # CELLCB IDX を渡す (標準コードと同じだが、扱う型は異なる)
                                    f.print(f"\t   (p_that){inib}->{pn}{subsc}")
                            else:
                                f.print(f"\t   ({to_s(ct.get_global_name())}_IDX)0")
                            delim = ","
                        else:
                            f.print("\t   ")
                    else:
                        # optional で未結合
                        b_join = False

                if b_join:
                    for param in ft.get_paramlist().get_items():
                        f.print(f"{delim} ({to_s(param.get_name())})")
                        delim = ","
                    f.print(" )\n")
        f.print("\n")

    def gen_ph_ref_desc_func(self: Any, f: Any) -> None:
        """ref_desc 指定された呼び口に対するディスクリプタ参照関数の生成。"""
        gn = to_s(self._global_name)
        if self._n_call_port_ref_desc > 0:
            f.printf(_msg("CRD_comment"), "#_CRD_#")

        inib = "->_inib" if self.has_CB() and self.has_INIB() else ""
        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_ref_desc():
                continue
            pn = to_s(p.get_name())

            if truthy(self._singleton):
                p_that = ""
                p_cellcb = ""
                delim = ""
                if self.has_INIB():
                    cb = f"{gn}_SINGLE_CELL_INIB."
                else:
                    cb = f"{gn}_SINGLE_CELL_CB."
            else:
                p_that = f"{gn}_CB  *p_that"
                p_cellcb = f"    {gn}_CB *p_cellcb = p_that;\n"
                delim = ", "
                cb = f"p_cellcb{inib}->"

            if p.get_array_size() is not None:
                array = f"{delim}int_t  i "
                array2 = "[ i ]"
                assert_ = f"    assert( 0 <= i && i < NCP_{pn} );\n"
            else:
                array = ""
                array2 = ""
                assert_ = ""
            sgn = to_s(p.get_signature().get_global_name())
            f.print(
                f"""/* [ref_desc] {pn} */
Inline Descriptor( {sgn} )
{gn}_{pn}_refer_to_descriptor( {p_that}{array} )
{{
    Descriptor( {sgn} )  des;
{p_cellcb}    /* cast is ncecessary for removing 'const'  */
{assert_}    des.vdes = (struct tag_{sgn}_VDES *){cb}{pn}{array2};
    return des;
}}

"""
            )

    def gen_ph_set_desc_func(self: Any, f: Any) -> None:
        """dynamic 指定された呼び口に対するディスクリプタ設定関数の生成。"""
        ctx = get_context()
        gn = to_s(self._global_name)
        if self._n_call_port_dynamic > 0:
            f.printf(_msg("SDF_comment"), "#_SDF_#")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_dynamic():
                continue
            pn = to_s(p.get_name())
            has_array = p.get_array_size() is not None
            inib = "->_inib" if self.has_CB() and self.has_INIB() and has_array else ""
            if truthy(self._singleton):
                p_that = ""
                p_that2 = ""
                p_cellcb = ""
                if has_array and ctx.rom:
                    cb = f"{gn}_SINGLE_CELL_INIB."
                else:
                    cb = f"{gn}_SINGLE_CELL_CB."
            else:
                p_that = f"{gn}_CB  *p_that, "
                p_that2 = f"{gn}_CB  *p_that "
                p_cellcb = f"    {gn}_CB *p_cellcb = p_that;\n"
                cb = f"(p_cellcb)->{inib}"

            if has_array:
                array = "int_t  i, "
                array2 = "[ i ]"
                array3 = " int_t  i "
                assert2 = f"    assert( 0 <= i && i < NCP_{pn} );\n"
            else:
                array = ""
                array2 = ""
                array3 = ""
                assert2 = ""
            sgn = to_s(p.get_signature().get_global_name())
            f.print(
                f"""/* [dynamic] {pn} */
Inline void
{gn}_{pn}_set_descriptor( {p_that}{array}Descriptor( {sgn} ) des )
{{
{p_cellcb}    assert( des.vdes != NULL );
{assert2}    {cb}{pn}{array2} = des.vdes;
}}

"""
            )

            if p.is_optional():
                delim = ", " if p_that2 != "" and array3 != "" else ""
                f.print(
                    f"""/* [dynamic,optional] {pn} */
Inline void
{gn}_{pn}_unjoin( {p_that2}{delim}{array3} )
{{
{p_cellcb}    {cb}{pn}{array2} = NULL;
}}

"""
                )

    def gen_ph_dealloc_code(
        self: Any, f: Any, append_name: str, b_undef: bool = False
    ) -> None:
        """send/receive で受け取ったメモリ領域を dealloc するマクロコード。

        b_undef:: bool : true = #undef コードの生成,  false = #define コードの生成
        """
        state = {"b_msg": False}
        for p in self._port:
            if p.is_omit():
                continue

            def visit(port: Any, fd: Any, par: Any) -> None:
                d = par.get_direction()  # 引数の方向指定子
                if d == Y.SEND:
                    type_ = par.get_declarator().get_type()
                    pre = "("
                    post = ")"
                elif d == Y.RECEIVE:
                    type_ = par.get_declarator().get_type().get_type()
                    pre = "("
                    post = ")"
                else:
                    return

                #                      ポート名         関数名         パラメータ名
                dealloc_func_name = f"{to_s(port.get_name())}_{to_s(fd.get_name())}_{to_s(par.get_name())}_dealloc"
                dealloc_macro_name = dealloc_func_name.upper()
                name = to_s(par.get_name())

                if b_undef is False:
                    if (
                        truthy(type_.get_size()) or truthy(type_.get_count())
                    ) and type_.get_type().has_pointer():
                        count_str: str | None = "count__"
                        count_str2 = ", count__"
                    else:
                        count_str = None
                        count_str2 = ""
                    if not state["b_msg"]:
                        f.print("\n")
                        f.printf(_msg("DAL_comment"), f"#_DAL_#  {append_name}")
                        state["b_msg"] = True
                    f.print(
                        f"#define {dealloc_macro_name}{append_name}({name}{count_str2})"
                    )
                    self.gen_dealloc_code_for_type(
                        f,
                        type_,
                        dealloc_func_name,
                        pre,
                        name,
                        post,
                        0,
                        append_name == "_RESET",
                        count_str,
                    )
                    f.print("\n")
                else:
                    f.print(f"#undef {dealloc_macro_name}{append_name}\n")

            p.each_param(visit)

    def gen_ph_cp_fun_macro_abbrev(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        singleton = truthy(self._singleton)
        if self._n_call_port > 0:
            f.printf(_msg("CPMA_comment"), "#_CPMA_#")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            # omit でも、呼び出すとエラーを起こすコードを生成
            pn = to_s(p.get_name())
            has_array = p.get_array_size() is not None

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                if p.is_VMT_useless() and not singleton:
                    dummy_pre = "((void)p_cellcb, "
                    dummy_post = ")"
                else:
                    dummy_pre = ""
                    dummy_post = ""

                if not p.is_require() or p.has_name():
                    f.print(f"#define {pn}_{fn}(")
                else:
                    f.print(f"#define {fn}(")
                ft = fun.get_declarator().get_type()
                delim = ""

                if has_array:
                    f.print(f"{delim} subscript")
                    delim = ","

                for param in ft.get_paramlist().get_items():
                    f.print(f"{delim} {to_s(param.get_name())}")
                    delim = ","
                f.print(" ) \\\n")

                if p.is_omit():
                    f.print(f"          {dummy_pre}omitted {pn}_{fn}(")
                else:
                    f.print(f"          {dummy_pre}{gn}_{pn}_{fn}(")
                delim = ""

                if not singleton:
                    f.print(f"{delim} p_cellcb")
                    delim = ","

                if has_array:
                    f.print(f"{delim} subscript")
                    delim = ","

                for param in ft.get_paramlist().get_items():
                    f.print(f"{delim} {to_s(param.get_name())}")
                    delim = ","
                f.print(f" ){dummy_post}\n")
        f.print("\n")

    def gen_ph_ref_desc_macro_abbrev(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_call_port_ref_desc > 0:
            f.printf(_msg("CRDA_comment"), "#_CRDA_#")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_ref_desc():
                continue

            if truthy(self._singleton):
                p_cellcb = ""
                delim = ""
            else:
                p_cellcb = "p_cellcb"
                delim = ", "

            if p.get_array_size() is not None:
                array = " i "
                array2 = f"{delim}i"
            else:
                array = ""
                array2 = ""
            pn = to_s(p.get_name())
            f.printf(
                f"#define %s_refer_to_descriptor({array})\\\n          %s_refer_to_descriptor( {p_cellcb}{array2} )\n",
                pn,
                f"{gn}_{pn}",
            )
            f.printf(
                f"#define %s_ref_desc({array})\\\n          %s_refer_to_descriptor({array})\n",
                pn,
                pn,
            )
        f.print("\n")

    def gen_ph_set_desc_macro_abbrev(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_call_port_dynamic > 0:
            f.printf(_msg("SDMA_comment"), "#_SDMA_#")

        if truthy(self._singleton):
            p_cellcb = ""
            delim = ""
        else:
            p_cellcb = "p_cellcb"
            delim = ", "
        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if not p.is_dynamic():
                continue

            if p.get_array_size() is not None:
                subsc = "i, "
                subsc2 = "i"
                subsc3 = delim + subsc2
            else:
                subsc = ""
                subsc2 = ""
                subsc3 = ""
            pn = to_s(p.get_name())
            f.printf(
                f"#define %s_set_descriptor( {subsc}desc )\\\n          %s_set_descriptor( {p_cellcb}{delim}{subsc}desc )\n",
                pn,
                f"{gn}_{pn}",
            )
            f.printf(
                f"#define %s_unjoin( {subsc2} )\\\n          %s_unjoin( {p_cellcb}{subsc3} )\n",
                pn,
                f"{gn}_{pn}",
            )
        f.print("\n")

    def gen_ph_ep_fun_macro(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EPM_comment"), "#_EPM_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                f.printf("#define %-16s %s\n", f"{pn}_{fn}", f"{gn}_{pn}_{fn}")
        f.print("\n")

    def gen_ph_typedef_idx(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        f.printf(_msg("CTIX_comment"), "#_CTIX_#")
        if truthy(self._idx_is_id_act):
            f.print(f"typedef ID {gn}_IDX;\n")
        elif self.has_CB():
            f.print(f"typedef struct tag_{gn}_CB *{gn}_IDX;\n")
        elif self.has_INIB():
            f.print(f"typedef const struct tag_{gn}_INIB *{gn}_IDX;\n")
        else:
            f.print(f"typedef int   {gn}_IDX;\n")

    def gen_ph_idx_type(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if truthy(self._idx_is_id_act):
            f.print("ID")
        elif self.has_CB():
            f.print(f"struct tag_{gn}_CB *")
        elif self.has_INIB():
            f.print(f"const struct tag_{gn}_INIB *")
        else:
            f.print("int")

    def _print_params(self: Any, f: Any, functype: Any, delim: str) -> None:
        if truthy(functype.get_paramlist()):
            items = functype.get_paramlist().get_items()
        else:
            # ここで nil になるのは、引数なしの時に void がなかった場合
            items = []
        for param in items:
            f.print(f"{delim} ")
            delim = ","
            f.print(param.get_type().get_type_str())
            f.print(" ")
            f.print(param.get_name())
            f.print(param.get_type().get_type_str_post())

    def gen_ph_ep_fun_prototype(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EPP_comment"), "#_EPP_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue

            f.print(f"/* {to_s(p.get_signature().get_global_name())} */\n")

            for fun in p.get_signature().get_function_head_array():
                if p.is_inline():
                    f.print("Inline ")
                functype = fun.get_declarator().get_type()
                f.printf("%-12s", functype.get_type_str())

                f.print(f" {gn}_{to_s(p.get_name())}_{to_s(fun.get_name())}(")
                if truthy(self._singleton):
                    delim = ""
                else:
                    f.print(f"{gn}_IDX idx")
                    delim = ","

                if p.get_array_size() is not None:
                    f.print(
                        f"{delim} int_t subscript"
                    )  # mikan singleton 時の ',' の始末
                    delim = ","

                self._print_params(f, functype, delim)
                f.print(");\n")

    def gen_ph_ep_skel_prototype(self: Any, f: Any) -> None:
        # 受け口スケルトン関数のプロトタイプ宣言を出力
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EPSP_comment"), "#_EPSP_#")
        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            if p.is_skelton_useless():  # 受け口最適化
                continue

            f.print(f"/* {to_s(p.get_name())} */\n")

            for fun in p.get_signature().get_function_head_array():
                functype = fun.get_declarator().get_type()
                f.printf("%-14s", functype.get_type_str())

                f.print(f" {gn}_{to_s(p.get_name())}_{to_s(fun.get_name())}_skel(")
                f.print(
                    f" const struct tag_{to_s(p.get_signature().get_global_name())}_VDES *epd"
                )
                self._print_params(f, functype, ",")
                f.print(");\n")
        f.print("\n")

    def gen_ph_cell_cb_type(self: Any, f: Any) -> None:
        ctx = get_context()
        gn = to_s(self._global_name)
        if ctx.rom:
            # 定数部は ROM, 変数部は RAM
            if self.has_INIB():
                f.printf(_msg("CIP_comment"), "#_CIP_#")
                f.print(f"typedef const struct tag_{gn}_INIB {{\n")

                self.gen_cell_cb_type_port(f, Y.INIB)
                self.gen_cell_cb_type_attribute(f, Y.INIB)

                f.print(f"}}  {gn}_INIB;\n")

            if self.has_CB():
                f.printf(_msg("CCTPA_comment"), "#_CCTPA_#")
                f.print(f"typedef struct tag_{gn}_CB {{\n")
                if self.has_INIB():
                    f.print(f"    {gn}_INIB  *_inib;\n")
                self.gen_cell_cb_type_port(f, Y.CB_DYNAMIC)
                self.gen_cell_cb_type_attribute(f, Y.CB)
                self.gen_cell_cb_type_var(f)
                f.print(f"}}  {gn}_CB;\n")

            if not self.has_CB() and not self.has_INIB():
                f.printf(_msg("CCDP_comment"), "#_CCDP_#")
                f.print(f"typedef struct tag_{gn}_CB {{\n")
                f.print("    int  dummy;\n")
                f.print(f"}} {gn}_CB;\n")
        else:
            # 全て RAM
            f.printf(_msg("CCTPO_comment"), "#_CCTPO_#")

            f.print(f"typedef struct tag_{gn}_CB {{\n")

            self.gen_cell_cb_type_port(f, Y.CB)
            self.gen_cell_cb_type_attribute(f, Y.CB)
            self.gen_cell_cb_type_var(f)

            f.print(f"}}  {gn}_CB;\n")

    def gen_cell_cb_type_attribute(self: Any, f: Any, inib_cb: Any) -> None:
        """attribute の型宣言出力。inib_cb::  :INIB または :CB"""
        from tecsgen.core.cdl_types import PtrType

        ctx = get_context()
        if inib_cb == Y.INIB and self._n_attribute_ro > 0:
            f.print("    /* attribute(RO) #_ATO_# */ \n")
        elif inib_cb == Y.CB:
            if ctx.rom:
                if self._n_attribute_rw > 0:
                    f.print("    /* attribute(RW) #_ATW_# */ \n")
            elif self._n_attribute_rw > 0 or self._n_attribute_ro > 0:
                f.print("    /* attribute #_AT_# */ \n")

        for a in self._attribute:
            if a.is_omit():
                continue
            if inib_cb == Y.INIB and a.is_rw():
                continue
            if self.has_INIB() and inib_cb == Y.CB and not a.is_rw():
                continue

            if (
                isinstance(a.get_type(), PtrType)
                and not a.get_type().is_const()
                and truthy(a.get_size_is())
            ):
                const_str = "const "
            else:
                const_str = ""
            f.print("    ")
            f.printf(f"{const_str}%-14s", a.get_type().get_type_str())
            f.print(f" {to_s(a.get_name())}{to_s(a.get_type().get_type_str_post())};\n")
        for v in self._var:
            if v.is_omit():
                continue
            if v.get_size_is() is None:
                continue
            if (
                ctx.rom and inib_cb == Y.CB
            ):  # size_is 指定されたものは INIB にのみ出力する
                continue

            f.print("    ")
            f.printf("%-14s", v.get_type().get_type_str())
            f.print(f" {to_s(v.get_name())}{to_s(v.get_type().get_type_str_post())};\n")

    def gen_cell_cb_type_var(self: Any, f: Any) -> None:
        # 変数の出力
        if self._n_var > 0:
            f.print("    /* var #_VA_# */ \n")

        for v in self._var:
            if v.is_omit():
                continue
            if (
                v.get_size_is() is not None
            ):  # size_is 指定された var は attribute へ出力する
                continue

            f.print("    ")
            f.printf("%-14s", v.get_type().get_type_str())
            f.print(f" {to_s(v.get_name())}{to_s(v.get_type().get_type_str_post())};\n")

    def gen_cell_cb_type_port(self: Any, f: Any, inib_cb: Any) -> None:
        self.gen_cell_cb_type_call_port(f, inib_cb)
        self.gen_cell_cb_type_entry_port(f, inib_cb)

    def gen_cell_cb_type_call_port(self: Any, f: Any, inib_cb: Any) -> None:
        ctx = get_context()
        # 呼び口
        if self._n_call_port > 0:
            f.print("    /* call port #_TCP_# */\n")

        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            if p.is_omit():
                continue
            has_array = p.get_array_size() is not None
            if (
                inib_cb == Y.INIB
                and p.is_dynamic()
                and not has_array
                and not ctx.ram_initializer
            ):
                continue
            if inib_cb == Y.CB_DYNAMIC and (not p.is_dynamic() or has_array):
                continue

            ptr = "*" if has_array else ""
            pn = to_s(p.get_name())

            if not p.is_cell_unique():
                const = "" if p.is_dynamic() else "const"
                if (
                    inib_cb == Y.INIB
                    and p.is_dynamic()
                    and not has_array
                    and ctx.ram_initializer
                ):
                    init = "_init_"
                    const2 = "const"
                else:
                    init = ""
                    const2 = "const"

                sgn = to_s(p.get_signature().get_global_name())
                if not p.is_skelton_useless():
                    # 標準形
                    if (
                        inib_cb == Y.INIB
                        and p.is_dynamic()
                        and has_array
                        and ctx.ram_initializer
                    ):
                        f.print(
                            f"    struct tag_{sgn}_VDES {ptr}{const2}*{pn}_init_; /* TCP_1 */\n"
                        )
                    f.print(
                        f"    struct tag_{sgn}_VDES {ptr}{const}*{pn}{init}; /* TCP_2 */\n"
                    )
                    if p.get_array_size() == "[]":
                        f.print(f"    int_t n_{pn};  /* TCP_3 */\n")
                else:
                    # 最適化 skelton 関数を呼出さない(受け口関数を直接呼出す)
                    # 呼び先セルタイプの CB の IDX 型
                    if truthy(p.get_real_callee_cell()):
                        f.print("    ")
                        p.get_real_callee_cell().get_celltype().gen_ph_idx_type(f)
                        f.print(f" {const} {ptr}{pn};  /* TCP_4 */\n")
                        # 相互参照に備えて、typedef した型を使わない
                        if p.get_array_size() == "[]":
                            f.print(f"    int_t n_{pn};  /* TCP_5 */\n")

    def gen_cell_cb_type_entry_port(self: Any, f: Any, inib_cb: Any) -> None:
        """受け口配列添数を記憶する変数の定義。"""
        if self._n_entry_port > 0:
            f.print("    /* call port #_NEP_# */ \n")

        for p in self._port:
            # 受け口配列の個数は省略しない
            if p.get_port_type() == Y.ENTRY and p.get_array_size() == "[]":
                f.print(f"    int_t n_{to_s(p.get_name())};\n")

    def gen_ph_extern_cell(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if truthy(self._singleton):
            f.printf(_msg("SCP_comment"), "#_SCP_#")
            if self.has_CB():
                f.print(f"extern  {gn}_CB  {gn}_SINGLE_CELL_CB;\n")
            if self.has_INIB():
                f.print(f"extern  {gn}_INIB  {gn}_SINGLE_CELL_INIB;\n")
            f.print("\n")
        elif truthy(self._b_need_ptab):
            f.printf(_msg("SCP_comment"), "#_MCPP_#")
            if self.has_CB():
                f.print(f"extern {gn}_CB  *const {gn}_CB_ptab[];\n")
                for c in self._ordered_cell_list:
                    if c.is_generate():  # 生成対象か？
                        name_array = self.get_name_array(c)
                        f.print(f"extern {gn}_CB  {to_s(name_array[4])};\n")
            elif self.has_INIB():
                f.print(f"extern {gn}_INIB  *const {gn}_INIB_ptab[];\n")
                for c in self._ordered_cell_list:
                    if c.is_generate():  # 生成対象か？
                        name_array = self.get_name_array(c)
                        f.print(f"extern {gn}_INIB  {to_s(name_array[11])};\n")
        else:
            f.printf(_msg("SCP_comment"), "#_MCPB_#")
            if self.has_CB():
                f.print(f"extern {gn}_CB  {gn}_CB_tab[];\n")
            elif self.has_INIB():
                f.print(f"extern {gn}_INIB  {gn}_INIB_tab[];\n")

    def gen_ph_INIB_as_CB(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        # ここは、手抜きである。本来なら INIB を出力すべき
        if not self.has_CB() and self.has_INIB():
            f.printf(_msg("DCI_comment"), "#_DCI_#")
            if truthy(self._singleton):
                f.print(f"#define {gn}_SINGLE_CELL_CB   {gn}_SINGLE_CELL_INIB\n")
            elif truthy(self._b_need_ptab):
                f.print(f"#define {gn}_CB_ptab           {gn}_INIB_ptab\n")
            else:
                f.print(f"#define {gn}_CB_tab           {gn}_INIB_tab\n")
            f.print(f"#define {gn}_CB               {gn}_INIB\n")
            f.print(f"#define tag_{gn}_CB           tag_{gn}_INIB\n")
            f.print("\n")

    def gen_ph_foreach_cell(self: Any, f: Any) -> None:
        """イテレータコード (FOREACH_CELL)の生成。singleton では出力しない。"""
        if truthy(self._singleton):
            return
        gn = to_s(self._global_name)

        if self.has_CB() or self.has_INIB():
            necessity = "" if truthy(self.need_CB_initializer()) else "//"

            f.printf(_msg("FEC_comment"), "#_FEC_#")

            if truthy(self._b_need_ptab):
                amp = ""
                tab = "ptab"
            else:
                amp = "&"
                tab = "tab"
            f.print(
                f"""#define FOREACH_CELL(i,p_cb)   \\
    for( (i) = 0; (i) < {gn}_N_CELL; (i)++ ){{ \\
       {necessity}(p_cb) = {amp}{gn}_CB_{tab}[i];

#define END_FOREACH_CELL   }}

"""
            )
        else:
            f.printf(_msg("NFEC_comment"), "#_NFEC_#")
            f.print(
                """#define FOREACH_CELL(i,p_cb)   \\
    for((i)=0;(i)<0;(i)++){

#define END_FOREACH_CELL   }

"""
            )

    def gen_ph_cb_initialize_macro(self: Any, f: Any) -> None:
        """変数var初期化コード。"""
        from tecsgen.core.cdl_types import ArrayType, PtrType, StructType
        from tecsgen.core.expression import C_EXP, Expression

        ctx = get_context()
        gn = to_s(self._global_name)
        f.printf(_msg("CIM_comment"), "#_CIM_#")

        for v in self._var:
            init = v.get_initializer()
            if type(init) is list:
                type_ = v.get_type()
                if isinstance(type_, PtrType):
                    # PtrType は ArrayType にすり替える
                    # 初期化子の要素数とする (後は 0 である)
                    t2 = ArrayType(Expression.create_integer_constant(len(init), None))
                    t2.set_type(type_.get_type())
                    type_ = t2
                f.print(
                    f"extern const {to_s(type_.get_type_str())} {gn}_{to_s(v.get_name())}_VAR_INIT"
                    f"{to_s(type_.get_type_str_post())};\n"
                )
        if truthy(self._singleton):
            arg = "()"
            p_that = ""
            that = f"{gn}_SINGLE_CELL_CB."
        else:
            arg = "(p_that)"
            p_that = "(p_that)"
            that = "(p_that)->"

        if self._n_cell_gen > 0 and truthy(self.need_CB_initializer()):
            b_var_init = False
            f.print(f"#define INITIALIZE_CB{arg}")
            for v in self._var:
                init = v.get_initializer()
                if init is None:
                    continue

                b_var_init = True
                type_ = v.get_type().get_original_type()
                f.print("\\\n")
                vn = to_s(v.get_name())
                if type(init) is list:
                    pre: str | None = None
                    post: str | None = None
                    if isinstance(type_, (ArrayType, PtrType)):
                        pre = "&"
                        post = "[0]"
                    elif isinstance(type_, StructType):
                        pre = "&"
                        post = ""
                    f.print(
                        f"\tmemcpy((void*){to_s(pre)}{gn}_VAR_{vn}{p_that}{to_s(post)}, "
                    )
                    f.print(
                        f"(void*){to_s(pre)}{gn}_{vn}_VAR_INIT{to_s(post)}, sizeof({gn}_{vn}_VAR_INIT));"
                    )
                elif type(init) is C_EXP:
                    f.print(f"\t{that}{vn} = {to_s(init.get_c_exp_string())};")
                else:
                    pre2 = f"{to_s(self.get_global_name())}_ATTR_"
                    post2 = "" if truthy(self._singleton) else f"{p_that}"
                    f.print(
                        f"\t{that}{vn} = {to_s(init.to_str(self._name_list, pre2, post2))};"
                    )

            # dynamic call port の初期化コード
            b_dyn_port = False
            for p in self._port:
                if p.get_port_type() != Y.CALL:
                    continue
                if p.is_dynamic() and ctx.ram_initializer:
                    pn = to_s(p.get_name())
                    if p.get_array_size() is None:
                        f.print(f"\\\n\t{that}{pn} = {that}_inib->{pn}_init_;")
                    else:
                        if truthy(self._singleton) or p.get_array_size() != "[]":
                            p_that = ""
                        else:
                            p_that = "(p_that)"
                        if truthy(self._singleton):
                            that = f"{gn}_SINGLE_CELL_INIB."
                        else:
                            that = "(p_that)->"
                        init_s = "_init->" if self.has_CB() else ""
                        f.printf("\\\n%-80s\\\n", "     {")
                        f.printf("%-80s\\\n", "        int_t   j;")
                        f.printf(
                            "%-80s\\\n",
                            f"        for( j = 0; j < N_CP_{pn}{p_that}; j++ ){{",
                        )
                        f.printf(
                            "%-80s\\\n",
                            f"            {that}{pn}[j] = {that}{init_s}{pn}_init_[j];",
                        )
                        f.printf("%-80s\\\n", "        }")
                        f.printf("%-80s", "       }")
                    b_dyn_port = True
            if b_dyn_port:
                f.print("\n")

            if (
                b_var_init is False
                and b_dyn_port is False
                and not truthy(self._singleton)
            ):
                f.print("\t(void)(p_that);")
            f.print("\n")

            f.print("#define SET_CB_INIB_POINTER(i,p_that)\\\n")
            if self.has_CB() and self.has_INIB():
                if truthy(self._singleton):
                    f.print(f"\t{that}_inib = &{gn}_SINGLE_CELL_INIB;\n\n")
                elif truthy(self._b_need_ptab):
                    f.print(f"\t{that}_inib = {gn}_INIB_ptab[(i)];\n\n")
                else:
                    f.print(f"\t{that}_inib = &{gn}_INIB_tab[(i)];\n\n")
            else:
                f.print("\t/* empty */\n")

    def gen_ph_inline(self: Any, f: Any) -> None:
        ctx = get_context()
        # inline ポートが一つでもあれば、inline.h の include
        if self._n_entry_port_inline > 0:
            f.printf(_msg("INL_comment"), "#_INL_#")
            f.print(f'#include "{to_s(self._global_name)}_inline.{ctx.h_suffix}"\n\n')

    def gen_ph_undef(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        f.printf(_msg("UDF_comment"), "#_UDF_#")
        f.print("#undef VALID_IDX\n")
        f.print("#undef GET_CELLCB\n")
        f.print("#undef CELLCB\n")
        f.print("#undef CELLIDX\n")
        f.print(f"#undef {to_s(self._name)}_IDX\n")

        f.print("#undef FOREACH_CELL\n")
        f.print("#undef END_FOREACH_CELL\n")
        f.print("#undef INITIALIZE_CB\n")
        f.print("#undef SET_CB_INIB_POINTER\n")

        for a in self._attribute:
            an = to_s(a.get_name())
            f.print(f"#undef ATTR_{an}\n")
            f.print(f"#undef {gn}_ATTR_{an}\n")
            f.print(f"#undef {gn}_GET_{an}\n")
        for v in self._var:
            vn = to_s(v.get_name())
            f.print(f"#undef VAR_{vn}\n")
            f.print(f"#undef VAR_{vn}\n")
            f.print(f"#undef {gn}_VAR_{vn}\n")
            f.print(f"#undef {gn}_GET_{vn}\n")
            f.print(f"#undef {gn}_SET_{vn}\n")
        for p in self._port:
            if p.get_port_type() != Y.CALL:
                continue
            pn = to_s(p.get_name())

            # is_...joined は omit するケースでも出力されるため、omit を検査する前に出力
            if p.is_optional():
                f.print(f"#undef is_{pn}_joined\n")

            if p.is_omit():
                continue

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                f.print(f"#undef {gn}_{pn}_{fn}\n")
                if not p.is_require() or p.has_name():
                    f.print(f"#undef {pn}_{fn}\n")
                else:
                    f.print(f"#undef {fn}\n")
            if p.is_dynamic():
                f.print(f"#undef {pn}_set_descriptor\n")
                if p.is_optional():
                    f.print(f"#undef {pn}_unjoin\n")
            elif p.is_ref_desc():
                f.print(f"#undef {pn}_refer_to_descriptor\n")
                f.print(f"#undef {pn}_ref_desc\n")
        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            for fun in p.get_signature().get_function_head_array():
                f.print(f"#undef {pn}_{to_s(fun.get_name())}\n")
            if p.get_array_size() is not None:
                f.print(f"#undef NEP_{pn}\n")

        self.gen_ph_dealloc_code(f, "", True)
        self.gen_ph_dealloc_code(f, "_RESET", True)

    def gen_ph_endif(self: Any, f: Any, post: str = "TECSGEN") -> None:
        f.print(f"#endif /* {to_s(self._global_name)}_{post}H */\n")

    ##### celltype factory header

    def generate_factory_header(self: Any) -> None:
        ctx = get_context()
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_factory.{ctx.h_suffix}")
        f.print(f"#ifndef {to_s(self._name)}_FACTORY_H\n")
        f.print(f"#define {to_s(self._name)}_FACTORY_H\n")
        f.close()

    def generate_factory_header_post(self: Any) -> None:
        ctx = get_context()
        f = AppFile.open(f"{ctx.gen}/{to_s(self._global_name)}_factory.{ctx.h_suffix}")

        # generate 文指定によるプラグイン適用
        for generate in self._generate_list:
            if truthy(generate[2]):
                generate[2].gen_factory(f)

        f.print(f"#endif /* {to_s(self._name)}_FACTORY_H */\n")
        f.close()
