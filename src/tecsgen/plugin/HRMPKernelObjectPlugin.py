"""HRMPKernelObjectPlugin.rb の移植（内部仕様9章）。HRMP カーネルオブジェクトとハンドラの静的 API を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.core.syntaxobj.cdlstring import CDLString
from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import Y, sym, to_s

# "Kernel_Object_type" => [ クラス内かどうか、ドメイン内かどうか、オブジェクトタイプ略名、静的API生成文字列]
_API: dict[str, list[Any]] = {
    "TASK": [
        Y.InClass,
        Y.InDomain,
        "TSK",
        "CRE_TSK( {{id}}, { {{attribute}}, $cbp$, tTask_start, {{priority}}, {{stackSize}} } )",
    ],
    "SEMAPHORE": [
        Y.InClass,
        Y.Any,
        "SEM",
        "CRE_SEM( {{id}}, { {{attribute}}, {{initialCount}}, {{maxCount}} })",
    ],
    "EVENTFLAG": [
        Y.InClass,
        Y.Any,
        "FLG",
        "CRE_FLG( {{id}}, { {{attribute}}, {{flagPattern}} } )",
    ],
    "DATAQUEUE": [
        Y.InClass,
        Y.Any,
        "DTQ",
        "CRE_DTQ( {{id}}, { {{attribute}}, {{dataCount}}, {{dataqueueManagementBuffer}} })",
    ],
    "PRIORITY_DATAQUEUE": [
        Y.InClass,
        Y.Any,
        "PDQ",
        "CRE_PDQ( {{id}}, { {{attribute}}, {{dataCount}}, {{maxDataPriority}}, {{priorityDataqueueManagementBuffer}} })",
    ],
    "FIXED_SIZE_MEMORYPOOL": [
        Y.InClass,
        Y.Any,
        "MPF",
        "CRE_MPF( {{id}}, { {{attribute}}, {{blockCount}}, {{blockSize}}, {{memoryPool}}, {{memoryPoolManagementBuffer}} })",
    ],
    "MESSAGE_BUFFER": [
        Y.InClass,
        Y.Any,
        "MBF",
        "CRE_MBF( {{id}}, { {{attribute}}, {{maxMessageSize}}, {{bufferSize}}, {{messageBufferManagementBuffer}} })",
    ],
    "SPINLOCK": [Y.InClass, Y.Any, "SPN", "CRE_SPN( {{id}}, { {{attribute}} })"],
    "MUTEX": [
        Y.InClass,
        Y.Any,
        "MTX",
        "CRE_MTX( {{id}}, { {{attribute}}, {{ceilingPriority}} })",
    ],
    "KERNEL": [Y.InClass, Y.Any, "SYS", "CRE_SYS"],
    # ######### Handlers #########
    "INT_REQUEST": [
        Y.InClass,
        Y.kernel,
        "INT",
        "CFG_INT( {{interruptNumber}}, { {{attribute}}, {{interruptPriority}} })",
    ],
    "INT_SERVICE_ROUTINE": [
        Y.InClass,
        Y.kernel,
        "ISR",
        "CRE_ISR( {{id}}, { {{attribute}}, $cbp$, {{interruptNumber}}, tISR_start, {{isrPriority}} })",
    ],
    "INT_HANDLER": [
        Y.InClass,
        Y.kernel,
        "INH",
        "DEF_INH( {{interruptHandlerNumber}}, { {{attribute}}, $id$_start})",
    ],
    "CPU_EXCEPTION_HANDLER": [
        Y.InClass,
        Y.kernel,
        "EXC",
        "DEF_EXC( {{cpuExceptionHandlerNumber}}, { {{attribute}}, $id$_start})",
    ],
    "INIT_ROUTINE": [
        Y.any,
        Y.kernel,
        "INI",
        "ATT_INI({ {{attribute}}, $cbp$, tInitializeRoutine_start })",
    ],
    "TERM_ROUTINE": [
        Y.any,
        Y.kernel,
        "TER",
        "ATT_TER({ {{attribute}}, $cbp$, tTerminateRoutine_start })",
    ],
}

_RX_PLACEHOLDER = re.compile(r"\{\{([a-zA-Z0-9_]*?)\}\}")


class HRMPKernelObjectPlugin(CelltypePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: Celltype  セルタイプ（インスタンス）"""
        super().__init__(celltype, option)
        self._celltype = celltype
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}
        self._cell_list: list[Any] = []

    def new_cell(self, cell: Any) -> None:
        """celltype プラグインを指定されたセルタイプのセルが生成された（新しいセルの報告）。"""
        self._cell_list.append(cell)
        if self._plugin_arg_str not in _API:
            raise RuntimeError(f"{self._plugin_arg_str} is unknown")
        api = _API[self._plugin_arg_str]

        # class check
        root = cell.get_owner().get_class_root()
        if root is None:
            raise RuntimeError("root is nil")
        class_type = root.get_class_type()
        if class_type is None:
            self.cdl_error2(
                cell.get_locale(), "HRMP9999 $1: not in class region", cell.get_name()
            )
        elif api[0] == Y.InClass and to_s(class_type.get_option()) == "root":
            self.cdl_error2(
                cell.get_locale(),
                "HRMP9999 $1: cannot be placed in out-of-class region",
                cell.get_name(),
            )

        # domain check
        root = cell.get_owner().get_domain_root()
        if root is None:
            raise RuntimeError("root is nil")
        domain_type = root.get_domain_type()
        if domain_type is None:
            self.cdl_error2(
                cell.get_locale(), "HRMP9999 $1: not in domain region", cell.get_name()
            )
        elif api[1] == Y.InDomain:
            if domain_type.get_option() == "OutOfDomain":
                self.cdl_error2(
                    cell.get_locale(),
                    "HRMP9999 $1: not place out of domain region",
                    cell.get_name(),
                )
        elif api[1] == sym("Kernel") and domain_type.get_option() != "kernel":
            self.cdl_error2(
                cell.get_locale(),
                "HRMP9999 $1: not place out of kernel domain region",
                cell.get_name(),
            )

    def print_cfg_cre(self, file: Any, cell: Any, indent: str) -> None:
        """CRE_XXXの出力。"""
        if self._plugin_arg_str not in _API:
            raise RuntimeError(f"{self._plugin_arg_str} is unknown")
        cfg_str = _API[self._plugin_arg_str][3]
        file.print(indent)

        celltype = cell.get_celltype()
        name_array = celltype.get_name_array(cell)

        # {{attribute}} の置換
        def repl(m: re.Match[str]) -> str:
            return to_s(self.get_attr_var_val(cell, name_array, sym(m.group(1))))

        cfg_str2 = _RX_PLACEHOLDER.sub(repl, cfg_str)

        # $xxx$ の置換
        cfg_str3 = celltype.subst_name(cfg_str2, name_array)

        file.print(cfg_str3, ";\n")

    def print_cfg_sac(self, file: Any, cell: Any, indent: str) -> None:
        from tecsgen.plugin.HRMPDomainPlugin import HRMPDomainPlugin

        celltype = cell.get_celltype()
        if celltype.find(Y.accessPattern1) is not None:
            sac_str = HRMPDomainPlugin.get_sac_str(cell)

            if self._plugin_arg_str not in _API:
                raise RuntimeError(f"{self._plugin_arg_str} is unknown")
            elif self._plugin_arg_str != "KERNEL":
                name_array = celltype.get_name_array(cell)
                file.puts(
                    f"{indent}SAC_{_API[self._plugin_arg_str][2]}"
                    f"({to_s(self.get_attr_var_val(cell, name_array, Y.id))}, {sac_str});"
                )
            else:
                file.puts(f"{indent}SAC_{_API[self._plugin_arg_str][2]}({sac_str});")

    def get_attr_var_val(self, cell: Any, name_array: list[Any], attr: Any) -> Any:
        celltype = cell.get_celltype()
        s = celltype.get_cell_attr_var_init_str(cell, name_array, attr)
        return celltype.subst_name(s, name_array)

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h に挿入するコードを生成する。"""
        from tecsgen.core.generate import AppFile

        f = AppFile.open(f"{get_context().gen}/tecsgen.cfg")
        f.print("/* generated by HRMPKernelObjectPlugin */\n")
        for cell in self._cell_list:
            region = cell.get_owner()
            croot = region.get_class_root()
            class_type = croot.get_class_type()
            coption = class_type.get_plugin().get_PU_kernel_class()

            droot = region.get_domain_root()
            domain_type = droot.get_domain_type()
            doption = domain_type.get_option()

            indent = ""
            if doption == "kernel":
                f.print("KERNEL_DOMAIN{\n")
                indent = "  "
            elif doption == "user":
                f.print(f"DOMAIN({to_s(droot.get_name())}){{\n")
                indent = "  "
            elif doption == "OutOfDomain":
                pass
            else:
                raise RuntimeError("unknown")
            dbg_print(
                f"HRMPKernelObjectPlugin: cell={to_s(cell.get_name())} celltype={to_s(cell.get_celltype().get_name())} coption={to_s(coption)}\n"
            )
            indent2 = indent
            if coption != "root":
                f.print(f"{indent}CLASS({to_s(coption)}){{\n")
                indent2 = indent + "  "
            self.print_cfg_cre(f, cell, indent2)
            self.print_cfg_sac(f, cell, indent2)

            if coption != "root":
                f.print(f"{indent}}}\n")
            if doption != "OutOfDomain":
                f.print("}\n")
        f.close()
