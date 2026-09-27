"""TECSInfoPlugin.rb の移植。`CelltypePlugin` for tTECSInfo（通常のセルタイプ側）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.CelltypePlugin import CelltypePlugin


class TECSInfoPlugin(CelltypePlugin):
    _cell_list: ClassVar[list[Any]] = []

    @classmethod
    def reset(cls) -> None:
        """`@@cell_list` 相当のクラス変数を初期化する（Ruby 版はプロセスごとに1回だけ実行するので
        この処理は無い。この移植のテストは1プロセスで何度も実行するため必要）。"""
        TECSInfoPlugin._cell_list = []

    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: Celltype   セルタイプ（インスタンス）"""
        super().__init__(celltype, option)
        from tecsgen.context import get_context

        ctx = get_context()
        if ctx.unopt_entry is False:
            self.cdl_info(
                "TIF0001 forcely set --unoptimize-entry by TECSInfoPlugin (by importing TECSInfo.cdl)"
            )
            ctx.unopt_entry = True

    def new_cell(self, cell: Any) -> None:
        """celltype プラグインを指定されたセルタイプのセルが生成された（セルタイププラグインに対する新しいセルの報告）。"""
        from tecsgen.context import get_context
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression
        from tecsgen.core.plugin import CFile
        from tecsgen.ruby_compat import sym, to_s

        type(self)._cell_list.append(cell)

        # TECSInfoSub セルのプロトタイプ宣言
        fn = f"{get_context().gen}/tmp_{to_s(cell.get_region().get_global_name())}_TECSInfoSub.cdl"
        f = CFile.open(fn, "w")
        f.print("/* prototype declaration of TECSInfoSub */\n")
        nest = cell.get_region().gen_region_str_pre(f)
        indent = "    " * nest
        f.print(
            f"{indent}[in_through()]\n"
            f"{indent}region rTECSInfo {{\n"
            f"{indent}    cell nTECSInfo::tTECSInfoSub TECSInfoSub;\n"
            f"{indent}}}; /* rTECSInfo}} */\n"
        )
        cell.get_region().gen_region_str_post(f)
        f.close()
        Import(fn)

        # セルに cTECSInfo の結合があるか？
        if cell.get_join_list().get_item(sym("cTECSInfo")) is None:
            # cTECSInfo = rTECSInfo::TECSInfosub.eTECSInfo; の追加
            nsp = NamespacePath(sym("rTECSInfo"), False)
            nsp.append_bang(sym("TECSInfoSub"))
            rhs = Expression.create_cell_join_expression(nsp, None, sym("eTECSInfo"))
            join = Join(sym("cTECSInfo"), None, rhs)
            cell.new_join(join)

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h に挿入するコードを生成する。

        file 以外の他のファイルにファクトリコードを生成してもよい。
        セルタイププラグインが指定されたセルタイプのみ呼び出される。
        """
        from tecsgen.context import get_context
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.generate import AppFile
        from tecsgen.ruby_compat import to_s

        ctx = get_context()

        f = CFile_open(f"{ctx.gen}/include_all_signature_header.h")
        f.print(
            "#ifndef include_all_signature_header_h\n"
            "#define include_all_signature_header_h\n\n"
        )

        def _print_include(sig: Any) -> None:
            f.print(f'#include "{to_s(sig.get_global_name())}_tecsgen.h"\n')

        Namespace.get_root().travers_all_signature(_print_include)
        f.print("\n#endif /* include_all_signature_header_h */\n")
        f.close()

        undefs2 = ["INITIALIZE_CB", "FOREACH_CELL", "END_FOREACH_CELL"]

        f2 = AppFile.open(f"{ctx.gen}/nTECSInfo_tVarDeclInfo_factory.h")
        Namespace.get_root().print_struct_define(f2)

        undefs = [
            "VALID_IDX",
            "GET_CELLCB",
            "CELLCB",
            "CELLIDX",
            "tVarDeclInfo_IDX",
            "ATTR_name",
            "ATTR_sizeIsExpr",
            "ATTR_declType",
            "ATTR_offset",
            "FOREACH_CELL",
        ]

        f2.print(
            "\n/***** Offset of attr & var of celltype  *****/\n"
            "#define TOPPERS_CB_TYPE_ONLY\n\n"
            "/* In case a celltype has 'inline' entry,\n"
            " * some macros are temporally defined\n"
            " * even if TOPPERS_CB_TYPE_ONLY is defined.\n"
            " * To avoid redefinition warning, undef these macros.\n"
            " */\n" + "".join(f"#undef {u}\n" for u in undefs) + "\n"
        )
        if ctx.ram_initializer:
            for u in undefs2:
                f2.print(f"#undef {u}\n")
        Namespace.get_root().print_celltype_define_offset(f2)
        f2.print(
            "\n/* redefine macros */\n"
            "#define tVarDeclInfo_IDX  nTECSInfo_tVarDeclInfo_IDX\n\n"
        )
        if ctx.ram_initializer:
            f2.print(
                "#define FOREACH_CELL(i,p_cb)   { (void)(i);\n"
                "#define END_FOREACH_CELL   }\n"
                "#define INITIALIZE_CB(p_that)   (void)(p_that);\n"
                "#define SET_CB_INIB_POINTER(i,p_that)\n"
            )
        f2.close()

        undefs = [
            "N_CP_cEntryInfo",
            "NCP_cEntryInfo",
            "N_CP_cCallInfo",
            "NCP_cCallInfo",
            "N_CP_cAttrInfo",
            "NCP_cAttrInfo",
            "N_CP_cVarInfo",
            "NCP_cVarInfo",
            "VALID_IDX",
            "GET_CELLCB",
            "CELLCB",
            "CELLIDX",
            "ATTR_name",
            "ATTR_b_singleton",
            "ATTR_b_IDX_is_ID_act",
            "ATTR_sizeOfCB",
            "ATTR_sizeOfINIB",
            "ATTR_n_cellInLinUnit",
            "ATTR_n_cellInSystem",
            "cEntryInfo_getName",
            "cEntryInfo_getNameLength",
            "cEntryInfo_getSignatureInfo",
            "cEntryInfo_getArraySize",
            "cEntryInfo_isInline",
            "cCallInfo_getName",
            "cCallInfo_getNameLength",
            "cCallInfo_getSignatureInfo",
            "cCallInfo_getArraySize",
            "cCallInfo_getSpecifierInfo",
            "cCallInfo_getInternalInfo",
            "cCallInfo_getLocationInfo",
            "cCallInfo_getOptimizeInfo",
            "cAttrInfo_getName",
            "cAttrInfo_getOffset",
            "cAttrInfo_getTypeInfo",
            "cAttrInfo_getSizeIsExpr",
            "cAttrInfo_getSizeIs",
            "cVarInfo_getName",
            "cVarInfo_getOffset",
            "cVarInfo_getTypeInfo",
            "cVarInfo_getSizeIsExpr",
            "cVarInfo_getSizeIs",
            "cEntryInfo_refer_to_descriptor",
            "cEntryInfo_ref_desc",
            "cCallInfo_refer_to_descriptor",
            "cCallInfo_ref_desc",
            "cAttrInfo_refer_to_descriptor",
            "cAttrInfo_ref_desc",
            "cVarInfo_refer_to_descriptor",
            "cVarInfo_ref_desc",
            "is_cEntryInfo_joined",
            "is_cCallInfo_joined",
            "is_cAttrInfo_joined",
            "is_cVarInfo_joined",
            "eCelltypeInfo_getName",
            "eCelltypeInfo_getNameLength",
            "eCelltypeInfo_getNAttr",
            "eCelltypeInfo_getAttrInfo",
            "eCelltypeInfo_getNVar",
            "eCelltypeInfo_getVarInfo",
            "eCelltypeInfo_getNCall",
            "eCelltypeInfo_getCallInfo",
            "eCelltypeInfo_getNEntry",
            "eCelltypeInfo_getEntryInfo",
            "eCelltypeInfo_isSingleton",
            "eCelltypeInfo_isIDX_is_ID",
            "eCelltypeInfo_hasCB",
            "eCelltypeInfo_hasINIB",
            "FOREACH_CELL",
            "END_FOREACH_CELL",
            "INITIALIZE_CB",
        ]

        f3 = AppFile.open(f"{ctx.gen}/nTECSInfo_tCelltypeInfo_factory.h")
        for u in undefs:
            f3.print(f"#undef {u}\n")
        f3.print("#define TOPPERS_CB_TYPE_ONLY\n")
        Namespace.get_root().print_celltype_define(f3)
        # FOREACH_CELL を出しなおす
        ct = Namespace.find(NamespacePath.analyze("::nTECSInfo::tCelltypeInfo"))
        ct.gen_ph_foreach_cell(f3)
        ct.gen_ph_cb_initialize_macro(f3)
        f3.print("\n")
        f3.close()

        undefs = [
            "VALID_IDX",
            "GET_CELLCB",
            "CELLCB",
            "CELLIDX",
            "tCallInfo_IDX",
            "ATTR_name",
            "ATTR_offset",
            "ATTR_b_inCB",
            "ATTR_b_optional",
            "ATTR_b_omit",
            "ATTR_b_dynamic",
            "ATTR_b_ref_desc",
            "ATTR_b_allocator_port",
            "ATTR_b_require_port",
            "ATTR_b_VMT_useless",
            "ATTR_b_skelton_useless",
            "ATTR_b_cell_unique",
            "cSignatureInfo_getName",
            "cSignatureInfo_getNameLength",
            "cSignatureInfo_getNFunction",
            "cSignatureInfo_getFunctionInfo",
            "cSignatureInfo_refer_to_descriptor",
            "cSignatureInfo_ref_desc",
            "eCallInfo_getName",
            "eCallInfo_getNameLength",
            "eCallInfo_getSignatureInfo",
            "eCallInfo_getArraySize",
            "eCallInfo_isOptional",
            "eCallInfo_isDynamic",
            "eCallInfo_isRefDesc",
            "eCallInfo_isOmit",
            "FOREACH_CELL",
        ]

        f4 = AppFile.open(f"{ctx.gen}/nTECSInfo_tCallInfo_factory.h")
        f4.print(
            "\n/***** Offset of attr & var of celltype  *****/\n"
            "#define TOPPERS_CB_TYPE_ONLY\n\n"
            "/* In case a celltype has 'inline' entry,\n"
            " * some macros are temporally defined\n"
            " * even if TOPPERS_CB_TYPE_ONLY is defined.\n"
            " * To avoid redefinition warning, undef these macros.\n"
            " */\n" + "".join(f"#undef {u}\n" for u in undefs) + "\n"
        )
        if ctx.ram_initializer:
            for u in undefs2:
                f4.print(f"#undef {u}\n")

        Namespace.get_root().print_call_define(f4)
        f4.print(
            "\n/* redefine macros */\n"
            "#define tCallInfo_IDX  nTECSInfo_tCallInfo_IDX\n\n"
        )
        if ctx.ram_initializer:
            f4.print(
                "#define FOREACH_CELL(i,p_cb)   { (void)(i);\n"
                "#define END_FOREACH_CELL   }\n"
                "#define INITIALIZE_CB(p_that)   (void)(p_that);\n"
                "#define SET_CB_INIB_POINTER(i,p_that)\n\n"
            )
        f4.close()

        f5 = AppFile.open(f"{ctx.gen}/nTECSInfo_tEntryInfo_factory.h")
        Namespace.get_root().print_entry_define(f5)
        f5.close()

        undefs = [
            "GET_CELLCB",
            "CELLCB",
            "CELLIDX",
            "ATTR_name",
            "INITIALIZE_CB",
            "FOREACH_CELL",
        ]
        f6 = AppFile.open(f"{ctx.gen}/nTECSInfo_tCellInfo_factory.h")
        for u in undefs:
            f6.print(f"#undef {u}\n")
        Region.get_root().print_cell_define(f6)
        # FOREACH_CELL を出しなおす
        ct6 = Namespace.find(NamespacePath.analyze("::nTECSInfo::tCellInfo"))
        ct6.gen_ph_foreach_cell(f6)
        ct6.gen_ph_cb_initialize_macro(f6)
        f6.close()

        f7 = AppFile.open(f"{ctx.gen}/nTECSInfo_tRawEntryDescriptorInfo_factory.h")
        Region.get_root().print_entry_descriptor_define(f7)
        f7.close()

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """後ろの CDL コードを生成する。

        複数のプラグインの post_code が一つのファイルに含まれるため、見出しをつける。
        """
        from tecsgen.core import tecsinfo
        from tecsgen.core.generator import Generator
        from tecsgen.ruby_compat import class_name

        if Generator.get_n_error() > 0:
            Generator.info(
                "I9999 TECSInfoPlugin does not generate TECSInfo code because of early error"
            )
            return
        file.print(f"/*------------ {class_name(cls)} post code ------------*/\n")
        for cell in cls._cell_list:
            root = cell.get_region()
            tecsinfo.print_info(file, root)

    @classmethod
    def get_post_code_priority(cls) -> int:
        from tecsgen.context import dbg_print
        from tecsgen.core.plugin_module import PluginModule

        prio = PluginModule.SIGNATURE_PLUGIN_POST_CODE_PRIORITY + 1000
        dbg_print(f"TECSInfoPlugin: get_post_code_priority: {prio}\n")
        return prio


def CFile_open(name: str) -> Any:
    """`AppFile.open` と同じ役割（`include_all_signature_header.h` は Ruby 版も毎回上書きで開く）。"""
    from tecsgen.core.plugin import CFile

    return CFile.open(name, "w")
