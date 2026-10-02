"""FMPPlugin.rb の移植（内部仕様9章）。FMP カーネル用クラスプラグイン。

各メソッドの役割りは ClassPlugin.rb を参照のこと。クラスの定義は `__tool_info__( "FMP_class_def" )` から得る。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.tool_info import TOOL_INFO
from tecsgen.plugin.ClassPlugin import ClassPlugin
from tecsgen.plugin.HRPKernelObjectManager import HRPKernelObjectManager
from tecsgen.plugin.lib.GenAttMod import GenAttMod
from tecsgen.ruby_compat import Y, sym, to_s, truthy

CLASS_DEF_SCHEMA: dict[Any, Any] = {
    Y.FMP_class_def: {
        Y.class_def: [sym("class")],  # array
    },
    sym("class"): {
        Y.type: "class",  # fixed string (type name)
        Y.class_name: Y.string,  # "CLS_PRC1", "CLS_ALL_PRC1", "GLOBAL" (TECS でのクラス名)
        Y.processorID: Y.integer,  # 1, 2, 3...
        Y.locality: Y.string,  # "only", "all", "global"
    },
    Y.__class: {  # optional
        # "CLS_PRC1", "CLS_ALL_PRC1", "GLOBAL"
        # (HRMP3, FMP3 のクラス名; TECS と変えれるように設けている)
        Y.class_name_in_kernel: Y.string
    },
}


class FMPPlugin(GenAttMod, ClassPlugin):
    _class_info: ClassVar[dict[Any, Any] | None] = None
    CLASS_DEF_schema = CLASS_DEF_SCHEMA

    @classmethod
    def reset(cls) -> None:
        FMPPlugin._class_info = None

    def __init__(self, region: Any, name: Any, option: Any) -> None:
        super().__init__(region, name, option)
        dbg_print(
            f"FMPPlugin: initialize: region={to_s(region.get_name())}, className={to_s(name)}, option={to_s(option)}\n"
        )
        if FMPPlugin._class_info is None:
            self.validate_and_set_class_info()
        self._region = region
        self._name = name  # FMP
        self._class1 = sym(option)
        assert FMPPlugin._class_info is not None
        attr1 = FMPPlugin._class_info.get(self._class1)
        if attr1 is None:
            self.cdl_error(
                "FMP9999 $1 is not acceptable class in TECS", to_s(self._class1)
            )
            return

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        dbg_print(
            f"FMPPlugin: add_through_plugin: {to_s(current_region.get_name())}=>{to_s(next_region.get_name())}, "
            f"{to_s(join.get_owner().get_name())}.{to_s(join.get_definition().get_name())}=>"
            f"{to_s(join.get_cell().get_name())}.{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )

        # PU: Processing Unit, NPU: Non-Processing Unit
        # NPU の locality だけ見れば十分である
        # PU の情報は使用する必要がない
        # NPU が only なら PU は必ず only
        current_class_attr = (
            current_region.get_class_root().get_class_type().get_plugin().get_NPU_attr()
        )
        caller_prc_npu_cell = current_class_attr[Y.processorID]
        caller_locality_npu_cell = current_class_attr[Y.locality]

        next_class_attr = (
            next_region.get_class_root().get_class_type().get_plugin().get_NPU_attr()
        )
        callee_prc_npu_cell = next_class_attr[Y.processorID]
        callee_locality_npu_cell = next_class_attr[Y.locality]

        rhs_global_name = (
            join.get_cell().get_real_celltype(join.get_rhs_port1()).get_global_name()
        )
        dbg_print(
            "FMPPlugin: Join: "
            + to_s(rhs_global_name)
            + " current:"
            + to_s(current_class_attr[Y.class_name])
            + " next:"
            + to_s(next_class_attr[Y.class_name])
            + "\n"
        )

        if HRPKernelObjectManager.include_celltype(rhs_global_name):
            # 結合先がカーネルオブジェクトセル: 何もしないthrough
            dbg_print(
                f"***** {to_s(join.get_cell().get_celltype().get_name())} is kernel object\n"
            )
            return []
        elif callee_locality_npu_cell == "only" and (
            caller_locality_npu_cell != "only"
            or caller_prc_npu_cell != callee_prc_npu_cell
        ):
            # 呼び先は、特定プロセッサに限定されている場合
            # 呼び元が、特定プロセッサ限定ではない、または異なるプロセッサである場合 RPC
            # （Ruby 版も何も挿入しない）
            return []
        else:
            dbg_print("**** Direct Call\n")
            return []

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        dbg_print(
            f"FMPPlugin: joinable? from {to_s(current_region.get_name())} to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    def validate_and_set_class_info(self) -> None:
        """__tool_info__( "FMP_class_def" ) の JSON 形式のデータを検証する。"""
        validator = TOOL_INFO.VALIDATOR(Y.FMP_class_def, CLASS_DEF_SCHEMA)
        if validator.validate():
            FMPPlugin._class_info = {}
            info = TOOL_INFO.get_tool_info(Y.FMP_class_def)
            if info is None:
                self.cdl_error("FMP9999 not found __tool_info__( FMP_class_def )")
                return
            class_info = info[Y.class_def]
            for cls in class_info:
                attr: dict[Any, Any] = {}
                # TECS でのクラス名
                FMPPlugin._class_info[sym(cls[Y.class_name])] = attr
                attr[Y.processorID] = cls[Y.processorID]
                attr[Y.locality] = cls[Y.locality]
                attr[Y.class_name] = cls[Y.class_name]  # kernel でのクラス名
                if truthy(cls.get(Y.class_name_in_kernel)):
                    attr[Y.class_name] = cls[Y.class_name_in_kernel]
            FMPPlugin._class_info[Y.root] = {
                Y.processorID: 0,
                Y.class_name: "root",
                Y.locality: "root",
            }

    def get_PU_kernel_class(self) -> Any:
        """カーネル(FMP3)での処理単位のクラス名を得る。"""
        assert FMPPlugin._class_info is not None
        if FMPPlugin._class_info.get(self._class1) is not None:
            return FMPPlugin._class_info[self._class1][Y.class_name]
        return to_s(self._class1)

    def get_NPU_kernel_class(self) -> Any:
        assert FMPPlugin._class_info is not None
        if FMPPlugin._class_info.get(self._class1) is not None:
            return FMPPlugin._class_info[self._class1][Y.class_name]
        return to_s(self._class1)

    def get_PU_attr(self) -> Any:
        assert FMPPlugin._class_info is not None
        return FMPPlugin._class_info.get(self._class1)

    def get_NPU_attr(self) -> Any:
        assert FMPPlugin._class_info is not None
        return FMPPlugin._class_info.get(self._class1)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass

    def gen_factory(self, node_root: Any) -> None:
        """ATT_MODの生成。

        gen_factory実行時には，すべてのセルタイププラグインを生成済みのはずなので，
        カーネルAPIコードのメモリ保護を省略できる．
        """
        self.gen_include()
        self.gen_att_mod(node_root)

    @classmethod
    def get_prc_only(cls, prc_id: Any) -> Any:
        """プロセッサID が一致し、ローカリティが only であるクラスを探す。

        見つからない場合、プロセッサ ID が一致するクラスを仮で返す。
        """
        tmp: Any = ""
        assert FMPPlugin._class_info is not None
        for c, attr in FMPPlugin._class_info.items():
            if attr[Y.processorID] == prc_id:
                if attr[Y.locality] == "only":
                    return c
                tmp = c  # エラー時に返す仮の値
        return tmp
