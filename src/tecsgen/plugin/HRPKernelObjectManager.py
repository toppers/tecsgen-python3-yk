"""HRPKernelObjectManager.rb の移植。HRP カーネルが管理するカーネルオブジェクトのセルタイプ一覧と、
拡張サービスコール（`HRPSVCManage`）の登録を持つ（インスタンスを持たない仮想的なクラス）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.ruby_compat import class_name, sym, to_s


class HRPKernelObjectManager:
    _kernel_objs: ClassVar[list[Any]] = [
        sym(n)
        for n in (
            "tKernel",
            "tTask",
            "tSemaphore",
            "tEventflag",
            "tDataqueue",
            "tPriorityDataqueue",
            "tMutex",
            "tFixedSizeMemoryPool",
            "tTimeEventHandler",
            "tCyclicNotifier",
            "tAlarmNotifier",
            "tInterruptRequest",
            "tISR",
            "tInterruptHandler",
            "tCpuExceptionHandler",
            "tInitializeRoutine",
            "tTerminateRoutine",
            "tMessageBuffer",
        )
    ]

    def __init__(self) -> None:
        # 本クラスはインスタンスを持たない仮想的なクラスである
        raise RuntimeError(f"class {class_name(type(self))} shall not have instances")

    @classmethod
    def include_celltype(cls, name: Any) -> bool:  # Ruby: include_celltype?
        return name in HRPKernelObjectManager._kernel_objs


class HRPSVCManage:
    """@@func_ids: 拡張サービスコールの関数名と拡張サービスコールIDを対応づけるハッシュ

    TECSのプラグインで生成した拡張サービスコールに割り当てるidは、実際には TFN_TECSGEN_ORIGIN で
    下駄を履かせた値となる（hrp3/include/extsvc_fncode.h で定義される）。
    """

    _func_ids: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        HRPSVCManage._func_ids = {}

    def __init__(self) -> None:
        raise RuntimeError(f"class {class_name(type(self))} shall not have instances")

    @classmethod
    def add_cell(cls, node_root: Any, cell_nsp: Any, signature: Any) -> None:
        dbg_print(
            f"HRPSVCManage: add_cell cell={to_s(cell_nsp)} node_root={to_s(node_root.get_name())} "
            f"signature={to_s(signature.get_name())}\n"
        )
        if HRPSVCManage._func_ids.get(node_root) is None:
            HRPSVCManage._func_ids[node_root] = {}
        HRPSVCManage._func_ids[node_root][cell_nsp] = signature

    @classmethod
    def get_list(cls, node_root: Any) -> Any:
        if HRPSVCManage._func_ids.get(node_root) is None:
            HRPSVCManage._func_ids[node_root] = {}
        return HRPSVCManage._func_ids[node_root]
