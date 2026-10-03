"""tecsinfo.rb の移植。

`Namespace`・`Region`・`Celltype`・`Port`・`Cell`・`Signature`・`FuncHead`・`ParamDecl`・`Decl`・`Type`
を"再オープン"して `print_info`/`print_*_define` 系メソッドを追加する。移植規約は `core/generate.py`・
`core/optimize.py` と同じ（1 Ruby 再オープンクラス = 1 mixin クラス）。`TECSInfoPlugin`・
`TECSInfoCompoPlugin` から使われる。

Ruby の `class Region; def self.print_cell_define f; region.get_link_root... ; end; end`（クラスメ
ソッド版）は `region` という未定義のローカル変数/メソッド呼び出しに見え、実際どこからも呼ばれない
（`TECSInfoPlugin#gen_factory` は `Region.get_root.print_cell_define f` の形でインスタンスメソッド
版を呼ぶ）。このクラスメソッド版は移植しない。
"""

from __future__ import annotations

from typing import Any, cast

from tecsgen.ruby_compat import Y, sym, to_s, truthy

# これらの mixin は実クラス（Namespace・Region・Celltype・...）自身の base list に直接混ぜる
# （`core/generate.py`・`core/optimize.py` と同じ規約）。プラグイン系 mixin が使う
# `TYPE_CHECKING` の `_Base` トリックはここでは使えない（`class Namespace(NamespaceTECSInfo, ...)`
# に対して `NamespaceTECSInfo` が型検査時に `Namespace` を継承すると自己参照になり
# `cyclic-class-definition` になる）。self 経由で呼ぶメソッドは実クラス側にしかないため、
# 該当行は ty の unresolved-attribute 抑止コメントで明示的に抑止する。


def print_info(f: Any, region: Any) -> None:
    """TECSInfo モジュールの `print_info`。region は link root。"""
    from tecsgen.core.cdl_types import Type
    from tecsgen.core.componentobj.namespace import Namespace

    nest = region.gen_region_str_pre(f)
    indent0 = "    " * nest
    indent = "    " * (nest + 1)
    f.print(f"{indent0}region rTECSInfo {{\n")
    Type.reset_print_info()

    # mikan 全部生成するのではなく、region 下のセルのセルタイプと、そこから参照されるシグニチャ、
    # セルタイプに限定して出力すべき。しかし、意味解析後に出力するため、これは容易ではない。
    # 最適化とコード生成は、リンクルートごとに行われる。
    Namespace.print_info_root(f, indent)
    region.get_link_root().print_info(f, indent)

    f.print(f"\n{indent}/*** TYPE information cell ***/\n")
    Type.print_info_post(f, indent)

    f.print(f"\n{indent}/*** TECS information cell ***/\n")
    f.print(
        f"{indent}cell nTECSInfo::tTECSInfoSub TECSInfoSub {{\n"
        f"{indent}    cNamespaceInfo = _RootNamespaceInfo.eNamespaceInfo;\n"
        f"{indent}    cRegionInfo    = _LinkRootRegionInfo.eRegionInfo;\n"
        f"{indent}}} /* TECSInfoSub */;\n"
        f"{indent0}}}; /* rTECSInfo */\n"
    )
    region.gen_region_str_post(f)


class NamespaceTECSInfo:
    """tecsinfo.rb の `class Namespace` 再オープン部分。"""

    _name: Any
    _global_name: Any
    _signature_list: list[Any]
    _celltype_list: list[Any]
    _namespace_list: list[Any]
    _struct_tag_list: Any

    def print_info_ns_sub(self, f: Any, indent: str) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        name = "_Root" if to_s(self._name) == "::" else to_s(self._global_name)
        f.print(
            f"\n{indent}/*** {to_s(self.get_namespace_path())} namespace information cell ***/\n"  # ty: ignore[unresolved-attribute]
        )
        f.print(f"{indent}cell nTECSInfo::tNamespaceInfo {name}NamespaceInfo{{\n")
        f.print(f'{indent}    name = "{to_s(self._name)}";\n')

        if len(self._signature_list) > 0:
            f.print(f"\n{indent}    /* SIGNATURE info */\n")
        for sig in self._signature_list:
            f.print(
                f"{indent}    cSignatureInfo[] = {to_s(sig.get_global_name())}SignatureInfo.eSignatureInfo;\n"
            )

        if len(self._celltype_list) > 0:
            f.print(f"\n{indent}    /* CELLTYPE info */\n")
        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                f.print(
                    f"{indent}    cCelltypeInfo[] = {to_s(ct.get_global_name())}CelltypeInfo.eCelltypeInfo;\n"
                )

        if len(self._namespace_list) > 0:
            f.print(f"\n{indent}    /* NAMESPACE info */\n")
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:
                f.print(
                    f"{indent}    cNamespaceInfo[] = {to_s(ns.get_global_name())}NamespaceInfo.eNamespaceInfo;\n"
                )

        f.print(
            f"{indent}}};   /* cell nTECSInfo::tNamespaceInfo {name}NamespaceInfo */\n"
        )

    def print_info_ns(self, f: Any, indent: str) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        self.print_info_ns_sub(f, indent)
        for sig in self._signature_list:
            sig.print_info(f, indent)
        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                ct.print_info(f, indent)
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:  # region を含めない
                ns.print_info_ns(f, indent)

    @classmethod
    def print_info_root(cls, f: Any, indent: str) -> None:
        """Ruby の `Namespace.self.print_info`（クラスメソッド）。`Region#print_info`（インスタンス
        メソッド）とは Ruby では名前空間が別だが、Python では同名衝突を避けて別名にする。"""
        from tecsgen.core.componentobj.namespace import Namespace

        Namespace.get_root().print_info_ns(f, indent)

    def print_struct_define(self, f: Any) -> None:
        """構造体メンバーのオフセット定義。"""
        f.print("\n/***** Offset of members of structures  *****/\n")
        for tag in self._struct_tag_list.get_items():
            for decl in tag.get_members_decl().get_items():
                f.printf(
                    "#define OFFSET_OF_%-30s  (%s)\n",
                    f"{tag.get_id_str()}_{to_s(decl.get_name())}",
                    f"(uint32_t)(intptr_t)&((({tag.get_type_str()}{tag.get_type_str_post()}*)0)->"
                    f"{to_s(decl.get_name())})",
                )
                f.printf(
                    "#define PLACE_OF_%-30s  (%s)\n",
                    f"{tag.get_id_str()}_{to_s(decl.get_name())}",
                    "VARDECL_PLACE_STRUCT",
                )

    def print_celltype_define_offset(self, f: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                ct.print_define_offset(f)
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:
                ns.print_celltype_define_offset(f)

    def print_celltype_define(self, f: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                ct.print_celltype_define(f)
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:
                ns.print_celltype_define(f)

    def print_call_define(self, f: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                ct.print_call_define(f)
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:
                ns.print_call_define(f)

    def print_entry_define(self, f: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        for ct in self._celltype_list:
            if len(ct.get_cell_list()) > 0:
                ct.print_entry_define(f)
        for ns in self._namespace_list:
            if isinstance(ns, Namespace) and type(ns) is Namespace:
                ns.print_entry_define(f)


class RegionTECSInfo:
    """tecsinfo.rb の `class Region` 再オープン部分。"""

    _name: Any
    _global_name: Any
    _cell_list: list[Any]
    _namespace_list: list[Any]

    def print_info_region_sub(self, f: Any, indent: str) -> None:
        from tecsgen.core.componentobj.region import Region

        name = "_LinkRoot" if self.get_link_root() is self else to_s(self._global_name)  # ty: ignore[unresolved-attribute]
        f.print(
            f"\n{indent}/*** {to_s(self.get_namespace_path())} region information cell ***/\n"  # ty: ignore[unresolved-attribute]
        )
        f.print(f"{indent}cell nTECSInfo::tRegionInfo {name}RegionInfo{{\n")
        f.print(f'{indent}    name = "{to_s(self._name)}";\n')

        for cell in self._cell_list:
            if not cell.exclude_info():
                f.print(
                    f"{indent}    cCellInfo[] = {to_s(cell.get_global_name())}CellInfo.eCellInfo;\n"
                )
        for region in self._namespace_list:
            if isinstance(region, Region):
                f.print(
                    f"{indent}    cRegionInfo[] = {to_s(region.get_global_name())}RegionInfo.eRegionInfo;\n"
                )
        f.print(f"{indent}}};\n")
        for cell in self._cell_list:
            if not cell.exclude_info():
                cell.print_info(f, indent)

    def print_info_region(self, f: Any, indent: str) -> None:
        from tecsgen.core.componentobj.region import Region

        self.print_info_region_sub(f, indent)
        for region in self._namespace_list:
            if isinstance(region, Region):
                region.print_info_region(f, indent)

    def print_info(self, f: Any, indent: str) -> None:
        self.print_info_region(f, indent)

    def print_cell_define(self, f: Any) -> None:
        from tecsgen.core.componentobj.region import Region

        ct_list: dict[Any, bool] = {}
        for cell in self._cell_list:
            if cell.exclude_info_factory():
                continue
            ct_list[cell.get_celltype()] = True

        f.print("#define TOPPERS_CB_TYPE_ONLY\n")
        for ct in ct_list:
            f.print(f'#include "{to_s(ct.get_global_name())}_tecsgen.h"\n')
        f.print("\n")

        for cell in self._cell_list:
            if cell.exclude_info_factory():
                continue
            name_array = cell.get_celltype().get_name_array(cell)
            if cell.get_celltype().has_CB():
                cb = f"(void*){to_s(name_array[8])}"
                cb_proto = f"extern {to_s(cell.get_celltype().get_global_name())}_CB {to_s(name_array[4])};\n"
            else:
                cb = "0"
                cb_proto = ""
            if cell.get_celltype().has_INIB():
                inib = f"(void*)&{to_s(name_array[5])}"
                inib_proto = f"extern {to_s(cell.get_celltype().get_global_name())}_INIB {to_s(name_array[11])};\n"
            else:
                inib = "0"
                inib_proto = ""
            f.print(
                f"{cb_proto}#define  {to_s(cell.get_global_name())}__CBP   {cb}\n"
                f"{inib_proto}#define  {to_s(cell.get_global_name())}__INIBP {inib}\n"
            )

        for region in self._namespace_list:
            if isinstance(region, Region):
                region.print_cell_define(f)

    def print_entry_descriptor_define(self, f: Any) -> None:
        from tecsgen.core.componentobj.region import Region

        for cell in self._cell_list:
            if cell.exclude_info_factory():
                continue

            signatures: dict[Any, bool] = {}
            for port in cell.get_celltype().get_port_list():
                if port.get_port_type() != Y.ENTRY:
                    continue

                # Ruby 版は signatures に登録しないので、同じシグニチャの受け口が続いても
                # include を毎回出力する（そのまま再現する）
                if signatures.get(port.get_signature()) is None:
                    f.print(
                        f'#include "{to_s(port.get_signature().get_global_name())}_tecsgen.h"\n'
                    )

                if cell.get_celltype().get_global_name() == sym(
                    "nTECSInfo_tRawEntryDescriptorInfo"
                ):
                    f.print(
                        f"const struct tag_{to_s(cell.get_celltype().get_global_name())}_{to_s(port.get_name())}_DES "
                    )
                    f.print(
                        f"{to_s(cell.get_global_name())}_{to_s(port.get_name())}_des;\n"
                    )
                else:
                    size = port.get_array_size()
                    if size is None:
                        size = 1
                    elif size == "[]":
                        size = cell.get_entry_port_max_subscript(port)
                    if not port.is_omit():
                        if size == 1:
                            f.print(
                                f"extern struct tag_{to_s(port.get_signature().get_global_name())}_VDES "
                            )
                            f.print(
                                f"{to_s(cell.get_global_name())}_{to_s(port.get_name())}_des;\n"
                            )
                        else:
                            for i in range(size):
                                f.print(
                                    f"extern struct tag_{to_s(port.get_signature().get_global_name())}_VDES "
                                )
                                f.print(
                                    f"{to_s(cell.get_global_name())}_{to_s(port.get_name())}_des{i};\n"
                                )

        for region in self._namespace_list:
            if isinstance(region, Region):
                region.print_entry_descriptor_define(f)


class CelltypeTECSInfo:
    """tecsinfo.rb の `class Celltype` 再オープン部分。"""

    _name: Any
    _global_name: Any
    _cell_list: list[Any]
    _port: list[Any]
    _attribute: list[Any]
    _var: list[Any]
    _singleton: bool
    _n_cell_gen: int
    _idx_is_id_act: bool

    def print_info(self, f: Any, indent: str) -> None:
        f.print(
            f"{indent}cell nTECSInfo::tCelltypeInfo {to_s(self._global_name)}CelltypeInfo {{\n"
            f'{indent}    name             = "{to_s(self._name)}";\n'
            f"{indent}    b_singleton      = {to_s(self._singleton)};\n"
            f'{indent}    b_IDX_is_ID_act  = C_EXP( "{to_s(self._global_name)}__IDX_is_ID_act" );\n'
            f'{indent}    sizeOfCB         = C_EXP( "{to_s(self._global_name)}__sizeOfCB" );\n'
            f'{indent}    sizeOfINIB       = C_EXP( "{to_s(self._global_name)}__sizeOfINIB" );\n'
            f'{indent}    n_cellInLinkUnit = C_EXP( "{to_s(self._global_name)}__NCELLINLINKUNIT" );\n'
            f"{indent}    n_cellInSystem   = {len(self._cell_list)};\n"
        )
        for port in self._port:
            if port.get_port_type() == Y.ENTRY:
                f.print(
                    f"{indent}    cEntryInfo[]    = {to_s(self._global_name)}_{to_s(port.get_name())}EntryInfo.eEntryInfo;\n"
                )
        for port in self._port:
            if port.get_port_type() == Y.CALL:
                f.print(
                    f"{indent}    cCallInfo[]     = {to_s(self._global_name)}_{to_s(port.get_name())}CallInfo.eCallInfo;\n"
                )
        for decl in self._attribute:
            f.print(
                f"{indent}    cAttrInfo[]     = {to_s(self._global_name)}_{to_s(decl.get_name())}VarDeclInfo.eVarDeclInfo;\n"
            )
        for decl in self._var:
            f.print(
                f"{indent}    cVarInfo[]      = {to_s(self._global_name)}_{to_s(decl.get_name())}VarDeclInfo.eVarDeclInfo;\n"
            )
        f.print(f"{indent}}};\n")

        for port in self._port:
            if port.get_port_type() == Y.ENTRY:
                port.print_info(f, self._global_name, indent)
        for port in self._port:
            if port.get_port_type() == Y.CALL:
                port.print_info(f, self._global_name, indent)
        for decl in self._attribute:
            decl.print_info(f, self._global_name, indent, Y.DECLTYPE_ATTR)
        for decl in self._var:
            decl.print_info(f, self._global_name, indent, Y.DECLTYPE_VAR)

    def print_define_offset(self, f: Any) -> None:
        # intptr_t に一回キャストするのは 64bit 版を考量してのこと。しかし 32bit としているので
        # 4GB を超える構造体等は扱えない
        if self._n_cell_gen > 0:
            f.print(f'\n#include "{to_s(self._global_name)}_tecsgen.h"\n')
            for decl in self._attribute:
                inib_cb = "INIB" if self.has_INIB() else "CB"  # ty: ignore[unresolved-attribute]
                if not decl.is_omit():
                    offset = (
                        f"(uint32_t)(intptr_t)&((({to_s(self._global_name)}_{inib_cb}*)0)->"
                        f"{to_s(decl.get_name())})"
                    )
                    place = inib_cb
                else:
                    offset = "0xffffffff"
                    place = "NON"
                f.printf(
                    "#define OFFSET_OF_%-30s  (%s)\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    offset,
                )
                f.printf(
                    "#define PLACE_OF_%-30s  VARDECL_PLACE_%s\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    place,
                )
            for decl in self._var:
                if truthy(decl.get_size_is()) and self.has_INIB():  # ty: ignore[unresolved-attribute]
                    inib_cb = "INIB"
                else:
                    inib_cb = "CB"
                place = inib_cb
                f.printf(
                    "#define OFFSET_OF_%-30s  (%s)\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    f"(uint32_t)(intptr_t)&((({to_s(self._global_name)}_{inib_cb}*)0)->{to_s(decl.get_name())})",
                )
                f.printf(
                    "#define PLACE_OF_%-30s  VARDECL_PLACE_%s\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    place,
                )
        else:
            f.print(
                f'\n// #include "{to_s(self._global_name)}_tecsgen.h"   // no cell exist\n'
            )
            # 生成されないセルタイプ
            for decl in self._attribute:
                f.printf(
                    "#define OFFSET_OF_%-30s  (%s)\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    "0xffffffff",
                )
                f.printf(
                    "#define PLACE_OF_%-30s   VARDECL_PLACE_NON\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                )
            for decl in self._var:
                f.printf(
                    "#define OFFSET_OF_%-30s  (%s)\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                    "0xffffffff",
                )
                f.printf(
                    "#define PLACE_OF_%-30s   VARDECL_PLACE_NON\n",
                    f"{to_s(self._global_name)}_{to_s(decl.get_name())}",
                )

    def print_celltype_define(self, f: Any) -> None:
        size_INIB = (
            f"(sizeof({to_s(self._global_name)}_INIB))"
            if self.has_INIB()  # ty: ignore[unresolved-attribute]
            else "(0)"
        )
        size_CB = (
            f"(sizeof({to_s(self._global_name)}_CB))"
            if self.has_CB()  # ty: ignore[unresolved-attribute]
            else "(0)"
        )

        if self._n_cell_gen > 0:
            f.printf(f'\n#include "{to_s(self._global_name)}_tecsgen.h"\n')
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}__IDX_is_ID_act",
                to_s(self._idx_is_id_act),
            )
            f.printf(
                "#define %-50s (%s)\n", f"{to_s(self._global_name)}__sizeOfCB", size_CB
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}__sizeOfINIB",
                size_INIB,
            )
            f.printf(
                "#define %-30s (%d)\n",
                f"{to_s(self._global_name)}__NCELLINLINKUNIT",
                self._n_cell_gen,
            )
        else:
            f.printf(
                "#define %-50s (false)\n", f"{to_s(self._global_name)}__IDX_is_ID_act"
            )
            f.printf("#define %-50s (0)\n", f"{to_s(self._global_name)}__sizeOfCB")
            f.printf("#define %-50s (0)\n", f"{to_s(self._global_name)}__sizeOfINIB")
            f.printf(
                "#define %-30s (%d)\n",
                f"{to_s(self._global_name)}__NCELLINLINKUNIT",
                self._n_cell_gen,
            )

    def print_call_define(self, f: Any) -> None:
        if self._n_cell_gen > 0:
            f.print(f'\n#include "{to_s(self._global_name)}_tecsgen.h"\n')
        else:
            f.print(
                f'\n// #include "{to_s(self._global_name)}_tecsgen.h"   // no cell exist\n'
            )

        for port in self._port:
            if port.get_port_type() == Y.ENTRY:
                continue
            if (
                port.is_omit()
                or (port.is_VMT_useless() and port.is_cell_unique())
                or self._n_cell_gen == 0
            ):
                place = "CALL_PLACE_NON"
            elif port.is_dynamic():
                place = (
                    "CALL_PLACE_INIB_DES"
                    if truthy(port.get_array_size())
                    else "CALL_PLACE_CB_DES"
                )
            elif not self.has_INIB():  # ty: ignore[unresolved-attribute]
                place = (
                    "CALL_PLACE_CB_IDX"
                    if port.is_VMT_useless()
                    else "CALL_PLACE_CB_DES"
                )
            else:
                place = (
                    "CALL_PLACE_INIB_IDX"
                    if port.is_VMT_useless()
                    else "CALL_PLACE_INIB_DES"
                )

            if (
                (port.is_VMT_useless() and port.is_cell_unique())
                or port.is_omit()
                or self._n_cell_gen == 0
            ):
                offset = "0xffffffff"
            else:
                cb_inib = "CB" if (port.is_dynamic() or not self.has_INIB()) else "INIB"  # ty: ignore[unresolved-attribute]
                offset = f"(uint32_t)(intptr_t)&(({to_s(self._global_name)}_{cb_inib}*)0)->{to_s(port.get_name())}"

            array_size = port.get_array_size()
            if array_size == "[]":
                array_size = "0xffffffff"
            elif array_size is None:
                array_size = "0"

            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__offset",
                offset,
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__array_size",
                to_s(array_size),
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__place",
                place,
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__b_VMT_useless",
                to_s(port.is_VMT_useless()),
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__b_skelton_useless",
                to_s(port.is_skelton_useless()),
            )
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__b_cell_unique",
                to_s(port.is_cell_unique()),
            )

    def print_entry_define(self, f: Any) -> None:
        for port in self._port:
            if port.get_port_type() == Y.CALL:
                continue
            array_size = port.get_array_size()
            if array_size == "[]":
                array_size = "0xffffffff"
            elif array_size is None:
                array_size = "0"
            f.printf(
                "#define %-50s (%s)\n",
                f"{to_s(self._global_name)}_{to_s(port.get_name())}__array_size",
                to_s(array_size),
            )


class PortTECSInfo:
    """tecsinfo.rb の `class Port` 再オープン部分。"""

    _name: Any
    _port_type: Any
    _signature: Any
    _b_inline: bool
    _b_optional: bool
    _b_omit: bool
    _b_dynamic: bool
    _b_ref_desc: bool
    _allocator_port: Any
    _b_require: bool

    def print_info(self, f: Any, ct_global: Any, indent: str) -> None:
        if self._signature is None:  # signature not found error in cdl
            return
        if self._port_type == Y.ENTRY:
            f.print(
                f"{indent}cell nTECSInfo::tEntryInfo {to_s(ct_global)}_{to_s(self._name)}EntryInfo{{\n"
                f'{indent}    name            = "{to_s(self._name)}";\n'
                f"{indent}    cSignatureInfo  = {to_s(self._signature.get_global_name())}SignatureInfo.eSignatureInfo;\n"
                f"{indent}    b_inline        = {to_s(self._b_inline)};\n"
                f'{indent}    array_size      = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__array_size" );\n'
                f"{indent}}};\n"
            )
        else:
            f.print(
                f"{indent}cell nTECSInfo::tCallInfo {to_s(ct_global)}_{to_s(self._name)}CallInfo{{\n"
                f'{indent}    name            = "{to_s(self._name)}";\n'
                f"{indent}    cSignatureInfo  = {to_s(self._signature.get_global_name())}SignatureInfo.eSignatureInfo;\n"
                f'{indent}    offset            = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__offset" );\n'
                f'{indent}    array_size        = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__array_size" );\n'
                f"{indent}    b_optional        = {to_s(self._b_optional)};\n"
                f"{indent}    b_omit            = {to_s(self._b_omit)};\n"
                f"{indent}    b_dynamic         = {to_s(self._b_dynamic)};\n"
                f"{indent}    b_ref_desc        = {to_s(self._b_ref_desc)};\n"
                f"{indent}    b_allocator_port  = {to_s(self._allocator_port is not None)};\n"
                f"{indent}    b_require_port    = {to_s(self._b_require)};\n"
                f'{indent}    place             = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__place" );\n'
                f'{indent}    b_VMT_useless     = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__b_VMT_useless" );\n'
                f'{indent}    b_skelton_useless = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__b_skelton_useless" );\n'
                f'{indent}    b_cell_unique     = C_EXP( "{to_s(ct_global)}_{to_s(self._name)}__b_cell_unique" );\n'
                "\n"
                f"{indent}}};\n"
            )


class CellTECSInfo:
    """tecsinfo.rb の `class Cell` 再オープン部分。"""

    _name: Any
    _global_name: Any
    _celltype: Any
    _join_list: Any
    _entry_array_max_subscript: dict[Any, Any]
    _b_defined: bool

    def print_info(self, f: Any, indent: str) -> None:
        if self.exclude_info():
            return
        f.print(
            f"\n{indent}/*** {to_s(self._global_name)} cell information ****/\n"
            f"{indent}cell nTECSInfo::tCellInfo {to_s(self._global_name)}CellInfo {{\n"
            f'{indent}    name            = "{to_s(self._name)}";\n'
            f'{indent}    cbp             = C_EXP( "{to_s(self._global_name)}__CBP" );\n'
            f'{indent}    inibp           = C_EXP( "{to_s(self._global_name)}__INIBP" );\n'
            f"{indent}    cCelltypeInfo   = {to_s(self._celltype.get_global_name())}CelltypeInfo.eCelltypeInfo;\n"
        )
        for port in self._celltype.get_port_list():
            if port.get_port_type() != Y.ENTRY:
                continue
            f.print(
                f"{indent}    cRawEntryDescriptor[] = {to_s(self._global_name)}_{to_s(port.get_name())}RawEntryDescriptorInfo.eRawEntryDescriptor;\n"
            )
        f.print(f"{indent}}};\n")

        # RawEntryDescriptorInfo cells
        for port in self._celltype.get_port_list():
            if port.get_port_type() != Y.ENTRY:
                continue

            size = port.get_array_size()
            if size is None:
                size = 1
            elif size == "[]":
                size = self._entry_array_max_subscript.get(port)
            if not port.is_omit():
                if size == 1:
                    red = f'C_EXP( "&{to_s(self._global_name)}_{to_s(port.get_name())}_des" )'
                else:
                    parts = [
                        f'C_EXP( "&{to_s(self._global_name)}_{to_s(port.get_name())}_des{i}" )'
                        for i in range(size)  # ty: ignore[invalid-argument-type]
                    ]
                    red = ", ".join(parts)
            else:
                red = "(void *)0"
            f.print(
                f"{indent}cell nTECSInfo::tRawEntryDescriptorInfo {to_s(self._global_name)}_{to_s(port.get_name())}RawEntryDescriptorInfo {{\n"
                f"{indent}   size = {size};\n"
                f"{indent}   rawEntryDescriptor = {{ {red} }};\n"
            )
            f.print(f"{indent}}};\n")

    def exclude_info(self) -> bool:
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        return (
            self._celltype is None
            or isinstance(self._celltype, CompositeCelltype)
            or self.is_of_composite()  # ty: ignore[unresolved-attribute]
            or self._celltype.get_global_name() == sym("nTECSInfo_tTECSInfoSub")
            or self.post_code_generated()  # ty: ignore[unresolved-attribute]
            or self._b_defined is False
        )

    def exclude_info_factory(self) -> bool:
        return (
            self._celltype is None
            or self.is_of_composite()  # ty: ignore[unresolved-attribute]
            or self._celltype.get_global_name() == sym("nTECSInfo_tTECSInfoSub")
            or not self._celltype.need_generate()
        )


class SignatureTECSInfo:
    """tecsinfo.rb の `class Signature` 再オープン部分。"""

    _name: Any
    _global_name: Any
    _function_head_list: Any

    def print_info(self, f: Any, indent: str) -> None:
        f.print(
            f"\n{indent}/*** {to_s(self._global_name)} signature information ****/\n"
            f"{indent}cell nTECSInfo::tSignatureInfo {to_s(self._global_name)}SignatureInfo {{\n"
            f'{indent}    name            = "{to_s(self._name)}";\n'
        )
        for fh in self._function_head_list.get_items():
            f.print(
                f"{indent}    cFunctionInfo[] = {to_s(self._global_name)}_{to_s(fh.get_name())}FunctionInfo.eFunctionInfo;\n"
            )
        f.print(f"{indent}}};\n")
        for fh in self._function_head_list.get_items():
            fh.print_info(f, indent)


class FuncHeadTECSInfo:
    """tecsinfo.rb の `class FuncHead` 再オープン部分。"""

    def print_info(self, f: Any, indent: str) -> None:
        sig_name = to_s(self.get_owner().get_global_name())  # ty: ignore[unresolved-attribute]
        func_name = to_s(self.get_name())  # ty: ignore[unresolved-attribute]
        f.print(
            f"{indent}cell nTECSInfo::tFunctionInfo {sig_name}_{func_name}FunctionInfo {{\n"
            f'{indent}    name            = "{func_name}";\n'
            f"{indent}    bOneway         = {to_s(self.is_oneway())};\n"  # ty: ignore[unresolved-attribute]
        )
        for param in self.get_paramlist().get_items():  # ty: ignore[unresolved-attribute]
            f.print(
                f"{indent}    cParamInfo[]    = {sig_name}_{func_name}_{to_s(param.get_name())}ParamInfo.eParamInfo;\n"
            )
        f.print(
            f"{indent}    cReturnTypeInfo = {self.get_return_type().get_id_str()}TypeInfo.eTypeInfo;\n"  # ty: ignore[unresolved-attribute]
            f"{indent}}};\n"
        )
        for param in self.get_paramlist().get_items():  # ty: ignore[unresolved-attribute]
            param.print_info(f, sig_name, func_name, self.get_paramlist(), indent)  # ty: ignore[unresolved-attribute]
        self.get_return_type().print_info(f, indent)  # ty: ignore[unresolved-attribute]


class ParamDeclTECSInfo:
    """tecsinfo.rb の `class ParamDecl` 再オープン部分。"""

    _size: Any
    _count: Any
    _string: Any
    _direction: Any

    def print_info(
        self,
        f: Any,
        signature_global_name: Any,
        func_name: Any,
        paramdecl_list: Any,
        indent: str,
    ) -> None:
        if truthy(self._size):
            size = f'"{self._size.get_rpn(paramdecl_list)}"'
        else:
            size = "(char_t*)0"
        if truthy(self._count):
            count = f'"{self._count.get_rpn(paramdecl_list)}"'
        else:
            count = "(char_t*)0"
        if truthy(self._string):
            if self._string == -1:
                string = '""'
            else:
                string = f'"{self._string.get_rpn(paramdecl_list)}"'
        else:
            string = "(char_t*)0"
        f.print(
            f"{indent}cell nTECSInfo::tParamInfo {to_s(signature_global_name)}_{to_s(func_name)}_{to_s(self.get_name())}ParamInfo {{\n"  # ty: ignore[unresolved-attribute]
            f'{indent}    name            = "{to_s(self.get_name())}";\n'  # ty: ignore[unresolved-attribute]
            f"{indent}    dir             = PARAM_DIR_{to_s(self._direction)};\n"
            f"{indent}    sizeIsExpr      = {size};\n"
            f"{indent}    countIsExpr     = {count};\n"
            f"{indent}    stringExpr      = {string};\n"
            f"{indent}    cTypeInfo       = {self.get_type().get_id_str()}TypeInfo.eTypeInfo;\n"  # ty: ignore[unresolved-attribute]
            f"{indent}}};\n"
        )
        self.get_type().print_info(f, indent)  # ty: ignore[unresolved-attribute]


class DeclTECSInfo:
    """tecsinfo.rb の `class Decl` 再オープン部分。"""

    _size_is: Any

    def print_info(
        self, f: Any, parent_ID_str: Any, indent: str, decl_type: Any
    ) -> None:
        size = '"mikan"' if truthy(self._size_is) else "(char_t*)0"
        name = to_s(self.get_name())  # ty: ignore[unresolved-attribute]
        f.print(
            f"{indent}cell nTECSInfo::tVarDeclInfo {to_s(parent_ID_str)}_{name}VarDeclInfo {{\n"
            f'{indent}    name            = "{name}";\n'
            f"{indent}    sizeIsExpr      = {size};\n"
            f"{indent}    declType        = {to_s(decl_type)};\n"
            f'{indent}    offset          = C_EXP( "OFFSET_OF_{to_s(parent_ID_str)}_{name}" );\n'
            f'{indent}    place           = C_EXP( "PLACE_OF_{to_s(parent_ID_str)}_{name}" );\n'
            f"{indent}    cTypeInfo       = {self.get_type().get_id_str()}TypeInfo.eTypeInfo;\n"  # ty: ignore[unresolved-attribute]
            f"{indent}}};\n"
        )
        self.get_type().print_info(f, indent)  # ty: ignore[unresolved-attribute]


class TypeTECSInfo:
    """tecsinfo.rb の `class Type` 再オープン部分。

    `_typeinfo_printed` は `cdl_types.py` の `Type` 本体で `ClassVar[dict]` として既に用意されている。
    """

    def print_info(self, f: Any, indent: str) -> None:
        """Type の info は、最後にまとめて出力するので、ここでは記録するだけ。"""
        from tecsgen.core.cdl_types import (
            ArrayType,
            DefinedType,
            PtrType,
            StructType,
            Type,
        )

        s = cast(Any, self)
        id_str = s.get_id_str()
        if Type._typeinfo_printed.get(id_str) is not None:
            return
        Type._typeinfo_printed[id_str] = self

        if isinstance(self, PtrType):
            s.get_referto().print_info(f, indent)
        elif isinstance(self, (ArrayType, DefinedType)):
            s.get_type().print_info(f, indent)
        elif isinstance(self, StructType):
            for decl in s.get_members_decl().get_items():
                decl.print_info(f, id_str, indent, Y.DECLTYPE_STMEMBER)

    @classmethod
    def reset_print_info(cls) -> None:
        from tecsgen.core.cdl_types import Type

        Type._typeinfo_printed = {}

    @classmethod
    def print_info_post(cls, f: Any, indent: str) -> None:
        from tecsgen.core.cdl_types import Type

        for type_ in Type._typeinfo_printed.values():
            type_.print_info_post_instance(f, indent)

    def print_info_post_instance(self, f: Any, indent: str) -> None:
        from tecsgen.core.cdl_types import (
            ArrayType,
            DefinedType,
            DescriptorType,
            PtrType,
            StructType,
            Type,
        )

        # Ruby 版は types.rb のクラス（superclass が Type）と ctypes.rb のクラス（superclass が
        # types.rb のクラス、`C{X}Type < {X}Type` で `include CType`）の2階層がある。この移植の
        # mixin 規約は「実クラス（Ruby の実の superclass 相当）を bases の最後に置く」なので、
        # `__bases__[-1]` が Ruby の superclass に対応する（`HasType`・`CType` 等はここでは mixin）。
        s = cast(Any, self)
        real_super = type(self).__bases__[-1]
        if real_super is Type:  # 親クラスが Type の場合 types.rb のクラス
            type_name = type(self).__name__
        else:  # ctypes.rb のクラス（親クラスが types.rb のクラス）
            type_name = real_super.__name__

        f.print(
            f"{indent}cell nTECSInfo::t{type_name}Info {s.get_id_str()}TypeInfo{{\n"
            f'{indent}    name           = "{to_s(s.get_type_str())}{to_s(s.get_type_str_post())}";\n'
            f"{indent}    typeKind       = TECSTypeKind_{type_name};\n"
        )
        if type_name != "FuncType":
            f.print(
                f'{indent}    size           = C_EXP( "sizeof({to_s(s.get_type_str())}{to_s(s.get_type_str_post())})" );\n'
                f"{indent}    b_const        = {to_s(s.is_const())};\n"
                f"{indent}    b_volatile     = {to_s(s.is_volatile())};\n"
            )

        if isinstance(self, PtrType):
            f.print(
                f"{indent}    cTypeInfo        = {s.get_referto().get_id_str()}TypeInfo.eTypeInfo;\n"
            )
        elif isinstance(self, (ArrayType, DefinedType)):
            f.print(
                f"{indent}    cTypeInfo        = {s.get_type().get_id_str()}TypeInfo.eTypeInfo;\n"
            )
        elif isinstance(self, StructType):
            for decl in s.get_members_decl().get_items():
                f.print(
                    f"{indent}    cVarDeclInfo[] = {s.get_id_str()}_{to_s(decl.get_name())}VarDeclInfo.eVarDeclInfo;\n"
                )
        elif isinstance(self, DescriptorType):
            f.print(
                f"{indent}    cSignatureInfo   = {to_s(s.get_signature().get_global_name())}SignatureInfo.eSignatureInfo;\n"
            )

        f.print(f"{indent}}};\n")

    def get_id_str(self) -> str:
        """型文字列の識別子化（Ruby: `get_ID_str`）。

        型文字列に含まれる識別子として用いることのできない文字を用いることのできる文字列に置き換える。
        空白 => __ / \\* => _Ptr_ / [] => _Array_ / Descriptor() => Descriptor_of_
        """
        from tecsgen.core.cdl_types import (
            ArrayType,
            DescriptorType,
            FuncType,
            PtrType,
            StructType,
        )

        obj = cast(Any, self)
        if isinstance(self, PtrType):
            s = f"{obj.get_referto().get_id_str()}_Ptr_"
        elif isinstance(self, ArrayType):
            subsc = obj.get_subscript()
            if truthy(subsc):
                s = f"{obj.get_type().get_id_str()}_Array{to_s(subsc.eval_const(None))}_"
            else:
                s = f"{obj.get_type().get_id_str()}_Array_"
        elif isinstance(self, StructType):
            s = f"struct {to_s(obj._tag)}"
        elif isinstance(self, DescriptorType):
            s = f"Descriptor_of_{to_s(obj.get_signature().get_global_name())}"
        elif isinstance(self, FuncType):
            s = f"function_{obj.get_type().get_id_str()}"
            if truthy(obj.get_paramlist()):
                for param in obj.get_paramlist().get_items():
                    s += f"__{param.get_declarator().get_type().get_id_str()}"
        else:
            s = f"{to_s(obj.get_type_str())}{to_s(obj.get_type_str_post())}"

        return s.replace(" ", "__")
