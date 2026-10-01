"""lib/GenAttMod.rb の移植。HRP3・HRMP3 の ATT_MOD と DEF_SVC を生成する（`HRPPlugin` などが include する）。

生成先のファイルは、ドメイン、クラスに分けて generate.rb で生成される。
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.ruby_compat import Y, rb_print, to_s, truthy


class GenAttMod:
    def gen_include(self) -> None:
        """tecsgen.cfg の INCLUDE を生成する。

        すべてのドメインに対する cfg を先に生成しておく。もし、ドメインに属する
        カーネルオブジェクトも、モジュールもない場合でも、cfg が出力される。
        """
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.generate import AppFile

        gen = get_context().gen
        regions = list(Celltype.get_domain_class_roots_total().keys())
        file = AppFile.open(f"{gen}/tecsgen.cfg")
        file.print("/* GenAttMod 001 */\n")
        for region in regions:
            if region.is_root():
                continue
            nsp = to_s(region.get_global_name())
            file2 = AppFile.open(f"{gen}/tecsgen_{nsp}.cfg")
            file2.close()
            if truthy(region.get_domain_root().get_domain_type()):
                kind = region.get_domain_root().get_domain_type().get_kind()
                if kind == Y.kernel:
                    pre = "KERNEL_DOMAIN{ "
                    post = "}"
                    indent = "  "
                elif kind == Y.user:
                    pre = f"DOMAIN({to_s(region.get_domain_root().get_name())}){{ "
                    post = "}"
                    indent = "  "
                elif kind == Y.OutOfDomain:
                    pre = ""
                    post = ""
                    indent = ""
                else:
                    # Ruby の case は該当なしだと pre などが前の周回の値のまま（想定外）
                    raise NotImplementedError("GenAttMod: unknown domain kind")
            else:
                pre = ""
                post = ""
                indent = ""
            if truthy(region.get_class_root().get_class_type()):
                opt_non_pu = region.get_class_root().get_class_type().get_option()
                if opt_non_pu != Y.root:
                    cr = "" if indent == "" else "\n"
                    pre2 = f"{cr}{indent}CLASS({to_s(opt_non_pu)}){{"
                    post2 = f"{indent}}}{cr}"
                    indent = f"{indent}  "
                else:
                    pre2 = ""
                    post2 = ""
            else:
                pre2 = ""
                post2 = ""

            file.puts(
                f'{pre}{pre2}\n{indent}INCLUDE("{gen}/tecsgen_{nsp}.cfg");\n{post2}{post}\n'
            )
        file.print("/* GenAttMod 001 end */\n\n")
        file.close()

    def gen_att_mod(self, node_root: Any) -> None:
        """ATT_MOD の生成。"""
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.generate import AppFile

        ctx = get_context()
        gen = ctx.gen
        dbg_print(f"gen_att_mod root={to_s(node_root.get_namespace_path())}\n")
        check_celltype_list: list[Any] = []

        for cell in Cell.get_cell_list2():
            # すべてのセルを走査してセルタイプをチェック
            ct = cell.get_celltype()
            if type(ct) is not Celltype or any(ct is c for c in check_celltype_list):
                continue
            roots = ct.get_domain_roots()
            if roots.get(Y.HRMP) is None and roots.get(Y.HRP) is None:
                # FMP3 は、対象外となる
                continue
            # チェック済みセルタイプに登録
            check_celltype_list.append(ct)
            dbg_print(f"att_mod:  celltype: {to_s(ct.get_name())}\n")

            # 必要のないセルタイプのコード，データはメモリ保護しない
            if not ct.need_generate():
                continue

            # HRMPのドメインリージョンを取得
            regions_hrmp = list(ct.get_domain_class_roots2().keys())
            if truthy(ctx.debug):
                rb_print(f"ATT_MOD domain in {to_s(ct.get_name())}: ")
                for reg in regions_hrmp:
                    rb_print(to_s(reg.get_name()))
                rb_print("\n")
            node_root = regions_hrmp[0].get_node_root()
            has_root = any(r is node_root for r in regions_hrmp)

            # セル管理ブロックとスケルトンのメモリ保護
            # gen_celltype_names_domain 相当の処理
            if not has_root and len(regions_hrmp) > 1:
                # ドメインが複数で，OutOfDomainにセルが存在しないセルタイプの場合
                # 共有のセル管理ブロックとスケルトンコードを登録する
                file = AppFile.open(f"{gen}/tecsgen.cfg")
                file.printf(
                    "%-60s/* GenAttMod 002 */\n",
                    f'ATT_MOD("{to_s(ct.get_global_name())}_tecsgen.o");',
                )
                file.close()

            for reg in regions_hrmp:
                nsp = "" if reg.is_root() else f"_{to_s(reg.get_global_name())}"
                file = AppFile.open(f"{gen}/tecsgen{nsp}.cfg")
                file.printf(
                    "%-60s/* GenAttMod 003 */\n",
                    f'ATT_MOD("{to_s(ct.get_global_name())}{nsp}_tecsgen.o");',
                )
                file.close()

            # セルタイプコードがない場合はスキップ
            if ct.is_all_entry_inline() and not truthy(ct.is_active()):
                continue

            # セルタイプコードのメモリ保護
            # gen_celltype_names_domain2 相当の処理
            if has_root or len(regions_hrmp) > 1:
                # OutOfDomainにセルが存在するセルタイプの場合
                # または，複数のドメインにセルが存在するセルタイプの場合
                # セルタイプコードを共有するように登録する
                file = AppFile.open(f"{gen}/tecsgen.cfg")
            else:
                # OutOfDomainでない単一のドメインにセルが存在するセルタイプの場合
                # セルタイプコードを専有するように登録する
                file = AppFile.open(
                    f"{gen}/tecsgen_{to_s(regions_hrmp[0].get_global_name())}.cfg"
                )

            file.printf(
                "%-60s/* GenAttMod 004 */\n",
                f'ATT_MOD("{to_s(ct.get_global_name())}.o");',
            )
            file.close()


class GenDefSvc:
    def gen_def_svc(self, node_root: Any) -> None:
        """拡張サービスコールの登録。"""
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.generate import AppFile
        from tecsgen.plugin.HRPKernelObjectManager import HRPSVCManage

        gen = get_context().gen
        file2 = AppFile.open(f"{gen}/tecsgen.cfg")
        file2.print("\n/* HRP010 HRPPlugin */\n")
        for cell_nsp, signature in HRPSVCManage.get_list(node_root).items():
            dbg_print(f"RPPPlugin: cell_nsp={to_s(cell_nsp)}\n")
            cell = Namespace.find(cell_nsp)
            sgn = to_s(signature.get_global_name())
            cname = to_s(cell.get_name())
            file2.print(
                f'#include "{sgn}_tecsgen.h"\n'
                f'#include "tHRPSVCCaller_{sgn}_factory.h"\n'
                f'#include "tHRPSVCBody_{sgn}_factory.h"\n'
            )
            for func_head in signature.get_function_head_array():
                fname = to_s(func_head.get_name())
                file2.print(
                    "  KERNEL_DOMAIN{\n"
                    f"    DEF_SVC( TFN_{cname.upper()} + FUNCID_{sgn.upper()}_{fname.upper()}-1, "
                    f"{{ TA_NULL, {to_s(cell.get_global_name())}_{fname}, "
                    f"SSZ_{cname}_{fname} }} );\n"
                    "  }\n"
                )
        file2.print("/****/\n\n")
        file2.close()

        for cell_nsp, signature in HRPSVCManage.get_list(node_root).items():
            cell = Namespace.find(cell_nsp)
            ct = cell.get_celltype()
            file2 = AppFile.open(f"{gen}/{to_s(ct.get_global_name())}.c")
            file2.print("/* GenAttMod 005 */\n\n")
            for func_head in signature.get_function_head_array():
                fname = to_s(func_head.get_name())
                file2.print(
                    "\nER_UINT\n"
                    f"{to_s(cell.get_global_name())}_{fname}(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid)\n"
                    "{\n"
                    f"CELLIDX idx = {to_s(ct.get_name_array(cell)[7])};\n"
                    f"return {to_s(ct.get_name())}_{fname}(idx, par1, par2, par3, par4, par5, cdmid);\n"
                    "}\n"
                )
            file2.close()

        val = "TFN_TECSGEN_ORIGIN"
        offset = 0
        for cell_nsp, signature in HRPSVCManage.get_list(node_root).items():
            cell = Namespace.find(cell_nsp)
            sgn = to_s(signature.get_global_name())
            cname = to_s(cell.get_name())
            file2 = AppFile.open(f"{gen}/tHRPSVCCaller_{sgn}_id.h")
            file2.print(
                "/* HRP012 HRPPlugin gen_factory */\n"
                f"#ifndef  TFN_{cname.upper()}\n"
                '#include "extsvc_fncode.h"\n'
                f"#define  TFN_{cname.upper()}    ({val}+{offset})\n"
                "#endif\n"
            )
            file2.close()

            file2 = AppFile.open(f"{gen}/tHRPSVCBody_{sgn}_factory.h")
            for func_head in signature.get_function_head_array():
                fname = to_s(func_head.get_name())
                file2.print(
                    "/* HRP013 */\n"
                    f'#include "tHRPSVCCaller_{sgn}_id.h"\n'
                    "\n"
                    f"#ifndef SSZ_{cname}_{fname}\n"
                    f"#define SSZ_{cname}_{fname} DefaultExtsvcStackSize\n"
                    f"#endif /* SSZ_{cname}_{fname} */\n"
                    f"ER_UINT {to_s(cell.get_global_name())}_{fname}(intptr_t par1, intptr_t par2, intptr_t par3, intptr_t par4, intptr_t par5, ID cdmid);\n"
                    "\n"
                )
            file2.close()
            offset += len(signature.get_function_head_array())
