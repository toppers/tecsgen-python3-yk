"""FMPObjectPlugin.rb の移植（内部仕様9章）。FMP カーネルオブジェクト（タスク・セマフォなど）の CRE_* を生成する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.core.syntaxobj.cdlstring import CDLString
from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import Y, sym, to_s

# @@api: オブジェクト種別 => [ 引数を作るメソッド名, 静的APIの接尾辞, 属性名... ]
_API: dict[str, list[Any]] = {
    "TASK": ["cre_params_task", "TSK", Y.id, Y.attribute, Y.priority, Y.stackSize],
    "SEMAPHORE": ["cre_params", "SEM", Y.id, Y.attribute, Y.initialCount, Y.maxCount],
    "EVENTFLAG": ["cre_params", "FLG", Y.id, Y.attribute, Y.flagPattern],
    "DATAQUEUE": [
        "cre_params",
        "DTQ",
        Y.id,
        Y.attribute,
        Y.dataCount,
        Y.dataqueueManagementBuffer,
    ],
    "PRIORITY_DATAQUEUE": [
        "cre_params",
        "PDQ",
        Y.id,
        Y.attribute,
        Y.dataCount,
        Y.maxDataPriority,
        Y.priorityDataqueueManagementBuffer,
    ],
    "FIXED_SIZE_MEMORYPOOL": [
        "cre_params",
        "MPF",
        Y.id,
        Y.attribute,
        Y.blockCount,
        Y.blockSize,
        Y.memoryPool,
        Y.memoryPoolManagementBuffer,
    ],
    "MESSAGE_BUFFER": [
        "cre_params",
        "MBF",
        Y.id,
        Y.attribute,
        Y.maxMessageSize,
        Y.bufferSize,
        Y.mbfmb,
    ],
    "SPINLOCK": ["cre_params", "SPN", Y.id, Y.attribute],
    "MUTEX": ["cre_params_mutex", "MTX", Y.id, Y.attribute, Y.ceilingPriority],
    "KERNEL": ["cre_params_kernel", "SYS"],
}

_RX_TA_CEILING = re.compile(r"\bTA_CEILING\b")


class FMPObjectPlugin(CelltypePlugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: Celltype  セルタイプ（インスタンス）"""
        super().__init__(celltype, option)
        self._celltype = celltype
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}
        self._cell_list: list[Any] = []

    def print_cfg_cre(self, file: Any, cell: Any, indent: Any) -> None:
        """CRE_XXXの出力。

        file:: FILE    出力先ファイル
        indent:: string  インデント用のtab
        """
        dbg_print(f"print_cfg_cre: {to_s(cell.get_name())} {self._plugin_arg_str}")
        file.print(indent, f"/* FMPObjectPlugin: {to_s(cell.get_name())} */\n")
        if self._plugin_arg_str not in _API:
            raise RuntimeError(f"{self._plugin_arg_str} is unknown")
        params = _API[self._plugin_arg_str]
        file.print(indent)
        file.puts(f"CRE_{params[1]}({to_s(getattr(self, params[0])(cell, params))});")

    # ------  KERNEL  ------#
    def cre_params_kernel(self, cell: Any, params: list[Any]) -> Any:
        # tKernel セルタイプは、カーネルオブジェクトを生成する必要がない
        return None

    # ------  MUTEX  ------#
    def cre_params_mutex(self, cell: Any, params: list[Any]) -> str:
        celltype = cell.get_celltype()
        name_array = celltype.get_name_array(cell)

        if (
            _RX_TA_CEILING.search(
                to_s(celltype.get_cell_attr_var_init_str(cell, name_array, Y.attribute))
            )
            is None
        ):
            sliced = params[3:-1]  # :ceilingPriority を外す
        else:
            sliced = params[3:]
        arg_list = [
            to_s(celltype.get_cell_attr_var_init_str(cell, name_array, attr))
            for attr in sliced
        ]
        id_ = to_s(celltype.get_cell_attr_var_init_str(cell, name_array, Y.id))
        return f"{id_}, {{ {', '.join(arg_list)} }}"

    # ----- TASK ------#
    def cre_params_task(self, cell: Any, params: list[Any]) -> str:
        celltype = cell.get_celltype()
        name_array = celltype.get_name_array(cell)
        attr = params[3]
        arg_list = [
            to_s(celltype.get_cell_attr_var_init_str(cell, name_array, attr)),
            f"(intptr_t){to_s(name_array[7])}",
            "tTask_start",
        ]
        for attr in params[4:]:
            arg_list.append(
                to_s(celltype.get_cell_attr_var_init_str(cell, name_array, attr))
            )
        id_ = to_s(celltype.get_cell_attr_var_init_str(cell, name_array, Y.id))
        return f"{id_}, {{ {', '.join(arg_list)} }}"

    # ----- SEMAPHORE, EVENTFLAG, DATAQUEUE, PRIORITY_DATAQUEUE ------#
    # ----- FIXED_SIZE_MEMORYPOOL, MESSAGE_BUFFER -------#
    def cre_params(self, cell: Any, params: list[Any]) -> str:
        celltype = cell.get_celltype()
        name_array = celltype.get_name_array(cell)

        arg_list = [
            to_s(celltype.get_cell_attr_var_init_str(cell, name_array, attr))
            for attr in params[3:]
        ]
        id_ = to_s(celltype.get_cell_attr_var_init_str(cell, name_array, Y.id))
        return f"{id_}, {{ {', '.join(arg_list)} }}"

    def new_cell(self, cell: Any) -> None:
        """celltype プラグインを指定されたセルタイプのセルが生成された（新しいセルの報告）。"""
        self._cell_list.append(cell)
        root = cell.get_owner().get_class_root()
        if root is not None:
            class_type = root.get_class_type()
            if class_type is None:
                self.cdl_error2(
                    cell.get_locale(),
                    "FMP9999 $1: not in class region or no class specified region exists.",
                    cell.get_name(),
                )
        else:
            raise RuntimeError("root is nil")

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h に挿入するコードを生成する。"""
        from tecsgen.core.generate import AppFile

        f = AppFile.open(f"{get_context().gen}/tecsgen.cfg")
        f.print("/* Generated by FMPObjectPlugin */\n")
        cls_kernel_prev: Any = None
        for cell in self._cell_list:
            # Ruby のブロック内で初めて代入される局所変数なので、周回ごとに nil から始まる
            indent: Any = None
            root = cell.get_owner().get_class_root()

            class_type = root.get_class_type()
            if cell.get_celltype().is_active():
                cls_tecs = sym(class_type.get_option()[0])
                cls_kernel = class_type.get_plugin().get_PU_kernel_class()
            else:
                cls_tecs = sym(class_type.get_option()[1])
                cls_kernel = class_type.get_plugin().get_NPU_kernel_class()
            dbg_print(
                f"FMPObjectPlugin#gen_factory: option={to_s(cls_tecs)} class_in_kernel={to_s(cls_kernel)} cell={to_s(cell.get_name())}\n"
            )
            if cls_kernel != cls_kernel_prev:
                if cls_kernel_prev is not None and cls_kernel_prev != Y.root:
                    f.print("}\n")
                if cls_kernel != Y.root:
                    f.print(f"CLASS({to_s(cls_kernel)}){{\n")
                    indent = "  "
                else:
                    indent = ""
                cls_kernel_prev = cls_kernel
            self.print_cfg_cre(f, cell, indent)
        if cls_kernel_prev is not None and cls_kernel_prev != Y.root:
            # 実際のところ nil になることはないハズ
            f.print("}\n")
        f.close()

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """後ろの CDL コードを生成。"""
