"""HRPSVCBodyCellPlugin.rb の移植（内部仕様9章）。拡張サービスコール本体側（カーネルドメイン）のセルを生成する cell プラグイン。

HRPSVCThroughPlugin が `generate( HRPSVCBodyCellPlugin, ... )` で起動する。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import sym, to_s, truthy


def _split(s: str, sep: str) -> list[str]:
    """Ruby の String#split（末尾の空要素を捨てる）。"""
    parts = s.split(sep)
    while parts and parts[-1] == "":
        parts.pop()
    return parts


class HRPSVCBodyCellPlugin(CellPlugin):
    # { :'cell_namespace_path.entry' => [ plugin, ... ], ... }  (添数は exportID)
    _cell_entry_export: ClassVar[dict[Any, list[Any]]] = {}
    # [ instanceOf(HRPSVCBodyCellPlugin), ... ]
    _plugin_list: ClassVar[list[Any]] = []

    ARG_PROC: ClassVar[dict[str, Any]] = {
        "exportEntryPort": lambda obj, rhs: obj.set_export_entry_port(rhs),
        "substRegion": lambda obj, rhs: obj.set_subst_region(rhs),
    }

    @classmethod
    def reset(cls) -> None:
        HRPSVCBodyCellPlugin._cell_entry_export = {}
        HRPSVCBodyCellPlugin._plugin_list = []

    def __init__(self, cell: Any, option: Any) -> None:
        """このメソッドは、セルの構文解析が終わったところで呼び出される（意味解析前）。"""
        dbg_print(f"HRPSVCBodyCellPlugin: cell={to_s(cell.get_name())}\n")
        super().__init__(cell, option)
        self._cell = cell
        self._caller_regions: dict[Any, list[str]] = {}
        self._export_id: Any = None

        self._plugin_arg_check_proc_tab = HRPSVCBodyCellPlugin.ARG_PROC
        self.parse_plugin_arg()
        HRPSVCBodyCellPlugin._plugin_list.append(self)
        if self._cell.get_region().get_domain_root() is None:
            # ドメイン指定されていない
            self.cdl_error(
                "HRPSB9999 $1 is in region not domain specified", self._cell.get_name()
            )
        elif (
            self._cell.get_region().get_domain_root().get_domain_type().get_option()
            != "kernel"
        ):
            # カーネルドメイン指定されていない
            self.cdl_error(
                "HRPSB9999 $1 is in region not specified kernel domain",
                self._cell.get_name(),
            )

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """後ろの CDL コードを生成。"""
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.plugin.HRPKernelObjectManager import HRPSVCManage

        cls.check_and_set_id()
        for ce, plugins in list(HRPSVCBodyCellPlugin._cell_entry_export.items()):
            path = _split(to_s(ce), ".")
            ep_name = sym(path[1])
            cell = plugins[0].get_cell()
            celltype = cell.get_celltype()
            if celltype is None:
                continue  # これまでに文法エラーが発生している
            ep = celltype.find(ep_name)
            if ep is None:
                continue  # entry port (エラーチェック済み)
            signature = ep.get_signature()
            if signature is None:
                continue  # これまでに文法エラーが発生している

            acpt = ""
            regions: list[str] = []
            for plugin in plugins:
                regions += plugin.get_caller_regions()[ep_name]
            uniq: list[str] = []
            for r in regions:
                if r not in uniq:
                    uniq.append(r)
            regions = uniq
            if "SHARED" in regions:
                acpt = 'C_EXP( "TACP_SHARED" )'
            else:
                region_list = []
                for rp in regions:
                    nsp = NamespacePath.analyze(rp)
                    region_list.append(Namespace.find(nsp))
                acpt = cls.regions_to_tacp(region_list)

            # --- Generate Kernel Domain Code ---#
            cell_name = sym(f"SVCBody_{to_s(cell.get_name())}_{to_s(ep_name)}")
            nest = cell.get_region().gen_region_str_pre(file)
            indent = "  " * nest
            file.print(
                f"{indent}cell tHRPSVCBody_{to_s(signature.get_global_name())} {to_s(cell_name)} {{\n"
                f"{indent}  cCall = {to_s(cell.get_name())}.{to_s(ep_name)};\n"
            )
            for func_head in signature.get_function_head_array():
                func_name = func_head.get_name()
                callable_domains = cell.get_restricted_regions(ep_name, func_name)
                if callable_domains is not None and len(callable_domains) > 0:
                    aacpt = cls.regions_to_tacp(callable_domains)
                elif callable_domains is not None and len(callable_domains) == 0:
                    aacpt = 'C_EXP( "TACP_KERNEL" )'
                else:
                    aacpt = acpt
                dbg_print(
                    f"HRPSVCBodyCellPlugin:regions_to_tacp:{to_s(cell.get_name())} {to_s(func_name)} {acpt} {aacpt}\n"
                )

                file.print(f"{indent}  restrict_acptn_{to_s(func_name)} = {acpt};\n")
            file.print(f"{indent}}};\n")
            cell.get_region().gen_region_str_post(file)

            rgn_nsp = cell.get_region().get_namespace_path()
            cell_nsp = rgn_nsp.append(cell_name)
            HRPSVCManage.add_cell(
                cell.get_region().get_node_root(), cell_nsp, signature
            )

    @classmethod
    def regions_to_tacp(cls, regions: list[Any]) -> str:
        acpt = ""
        delim = ""
        b_shared = False
        for region in regions:
            domain_type = region.get_domain_type()
            if truthy(domain_type):
                domain_option = domain_type.get_option()
            else:
                HRPSVCBodyCellPlugin._plugin_list[0].cdl_warning(
                    "HSW0002 HRPSVCBodyCellPlugin: region $1 not under domain",
                    region.get_namespace_path(),
                )
                domain_option = "kernel"
            if domain_option == "user":
                acpt += delim + "TACP(" + to_s(region.get_name()) + ")"
                delim = " | "
            elif domain_option == "OutOfDomain":
                b_shared = True
            elif domain_option == "kernel":
                pass
            else:
                raise RuntimeError("unkown domain option ")
        if b_shared:
            aacpt = 'C_EXP( "TACP_SHARED" )'
        elif acpt == "":
            aacpt = 'C_EXP( "TACP_KERNEL" )'
        else:
            aacpt = f'C_EXP( "{acpt}" )'
        return aacpt

    @classmethod
    def check_and_set_id(cls) -> None:
        # Ruby 版も、exportID を調べるだけで何もしない
        pass

    def get_export_id(self) -> Any:
        return self._export_id

    def get_cell(self) -> Any:
        return self._cell

    def get_caller_regions(self) -> dict[Any, list[str]]:
        return self._caller_regions

    # -----  オプション -----#
    def set_export_entry_port(self, rhs: str) -> None:
        """exportEntryPort='eEntry:rRegion1,rRegion2,...','eEntry2:rRegion1'"""
        from tecsgen.core.componentobj.port import Port

        rhs = re.sub(r":::", ":##", rhs)  # :: が : の直後にいた場合
        rhs = re.sub(r"::", "##", rhs)  # :: は ## に置き換える
        entry = _split(rhs, ":")  # : で区切る
        entry_port = sym(entry[0])
        # get_celltype は (celltype not found な時) nil を返す可能性があるが処置しない
        ep = self._cell.get_celltype().find(entry_port)
        if not isinstance(ep, Port) or ep.get_port_type() != sym("ENTRY"):
            self.cdl_error(
                "HRPSB9999 '$1' is not entry port or not found in $2",
                entry_port,
                self._cell.get_name(),
            )
        elif truthy(ep.get_array_size()):
            self.cdl_error(
                "HRPSB9999 '$1' is entry array which is not supported in current version",
                entry_port,
            )
        caller_regions = entry[1] if len(entry) > 1 else ""
        caller_regions = re.sub(r"##", "::", caller_regions)  # ## を :: に戻す
        dbg_print(
            f"set_export_entry_port: cell={to_s(self._cell.get_name())} entry={to_s(entry_port)} regions={caller_regions}\n"
        )
        if self._caller_regions.get(entry_port) is None:
            self._caller_regions[entry_port] = []
        for s in _split(caller_regions, ","):
            dbg_print(f"set_export_entry_port: {to_s(self._cell.get_name())}={s}\n")
            self._caller_regions[entry_port].append(s)  # region path str
            path = sym(f"{to_s(self._cell.get_namespace_path())}.{to_s(entry_port)}")
            if HRPSVCBodyCellPlugin._cell_entry_export.get(path) is not None:
                HRPSVCBodyCellPlugin._cell_entry_export[path].append(self)
            else:
                HRPSVCBodyCellPlugin._cell_entry_export[path] = [self]
            dbg_print(f"set_export_entry_port: {to_s(path)}\n")

    def set_subst_region(self, rhs: str) -> None:
        """substRegion='original_region:subst_region'

        original_region は domain 外、subst_region は domain 内。
        """
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.componentobj.region import Region

        entry = _split(rhs, ":")
        original_region_name = entry[0]
        subst_region_name = entry[1] if len(entry) > 1 else ""
        dbg_print(
            f"HRPSVCBodyCell: substRegion origin={original_region_name} subst={subst_region_name}\n"
        )

        # 変更前 (ドメイン外のリージョンであることを確認)
        nsp = NamespacePath.analyze(original_region_name)
        original_region = Namespace.find(nsp)
        if original_region is None or not isinstance(original_region, Region):
            self.cdl_error(
                "HRPSB9999 HRPSVCBodyCellPlugin: substRegion option: '$1': not exist or not region",
                original_region_name,
            )
        elif truthy(original_region.get_domain_type()):
            self.cdl_error(
                "HRPSB9999 HRPSVCBodyCellPlugin: substRegion option: '$1': under domain",
                original_region_name,
            )

        # 変更後 (ドメイン内のリージョンであることを確認)
        nsp = NamespacePath.analyze(subst_region_name)
        subst_region = Namespace.find(nsp)
        if subst_region is None or not isinstance(subst_region, Region):
            self.cdl_error(
                "HRPSB9999 HRPSVCBodyCellPlugin: substRegion option: '$1': not exist or not region",
                subst_region_name,
            )
        elif subst_region.get_domain_type() is None:
            self.cdl_error(
                "HRPSB9999 HRPSVCBodyCellPlugin: substRegion option: '$1': not under domain",
                subst_region_name,
            )
        if subst_region.get_node_root() is not self._cell.get_region().get_node_root():
            self.cdl_error(
                "HRPSB9999 HRPSVCBodyCellPlugin: substRegion option: '$1': not in the same node as '$2'",
                subst_region_name,
                self._cell.get_name(),
            )
