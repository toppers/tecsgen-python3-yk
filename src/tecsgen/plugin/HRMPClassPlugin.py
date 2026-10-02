"""HRMPClassPlugin.rb の移植（内部仕様9章）。HRMP カーネル用クラスプラグイン。

各メソッドの役割りは ClassPlugin.rb を参照のこと。クラスの定義は `__tool_info__( "HRMP_class_def" )` から得る。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.tool_info import TOOL_INFO
from tecsgen.plugin.ClassPlugin import ClassPlugin
from tecsgen.plugin.HRMPPlugin import HRMPJoinManager
from tecsgen.ruby_compat import Y, sym, to_s, truthy

# クラス定義(.cdf) の JSON スキーマ
CLASS_DEF_SCHEMA: dict[Any, Any] = {
    Y.HRMP_class_def: {
        Y.class_def: [sym("class")],  # array
    },
    sym("class"): {
        Y.type: "class",  # fixed string (type name)
        Y.class_name: Y.string,  # "CLS_PRC1", "CLS_ALL_PRC1", ":root" (TECS でのクラス名)
        Y.processorID: Y.integer,  # 1, 2, 3...
        Y.locality: Y.string,  # "only", "all", "root"
    },
    sym("__class"): {  # optional
        # "CLS_PRC1", "CLS_ALL_PRC1", ":root"
        # (HRMP3, FMP3 のクラス名; TECS と変えれるように設けている)
        Y.class_name_in_kernel: Y.string
    },
}


class HRMPClassPlugin(HRMPJoinManager, ClassPlugin):
    CLASS_DEF_schema = CLASS_DEF_SCHEMA

    # nTECSGENConfig::tClassConfig セルタイプのセル
    # { class_name_in_TECS => {:processorID=>processor_No, :class_name=>class_name_in_HRMP3, :locality=>locality_str}}
    _class_info: ClassVar[dict[Any, Any] | None] = None

    @classmethod
    def reset(cls) -> None:
        HRMPClassPlugin._class_info = None

    def __init__(self, region: Any, name: Any, option: Any) -> None:
        super().__init__(region, name, option)
        if HRMPClassPlugin._class_info is None:
            self.validate_and_set_class_info()
        dbg_print(
            f"HRMPClassPlugin: initialize: region={to_s(region.get_name())}, className={to_s(name)}, option={to_s(option)}\n"
        )
        self._region = region
        self._name = name  # HRMP
        self._class1: Any = sym(option)
        self._class_specified = self._class1
        assert HRMPClassPlugin._class_info is not None
        attr1 = HRMPClassPlugin._class_info.get(self._class1)
        if attr1 is None:
            self.cdl_error(
                "HRMP9999 $1 is not acceptable class in TECS", to_s(self._class1)
            )
            self._class1 = "root"  # root に置き換えて置く
            return

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        dbg_print(
            f"HRMPClassPlugin: joinable? from {to_s(current_region.get_name())} to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    def validate_and_set_class_info(self) -> None:
        """__tool_info__( "HRMP_class_def" ) の JSON 形式のデータを検証する。"""
        validator = TOOL_INFO.VALIDATOR(Y.HRMP_class_def, CLASS_DEF_SCHEMA)
        if validator.validate():
            HRMPClassPlugin._class_info = {}
            info = TOOL_INFO.get_tool_info(Y.HRMP_class_def)
            if info is None:
                self.cdl_error("HRMP9999 not found __tool_info__( HRMP_class_def )")
            class_info = info[Y.class_def]
            for cls in class_info:
                attr: dict[Any, Any] = {}
                # TECS でのクラス名
                HRMPClassPlugin._class_info[sym(cls[Y.class_name])] = attr
                attr[Y.processorID] = cls[Y.processorID]
                attr[Y.locality] = cls[Y.locality]
                attr[Y.class_name] = cls[Y.class_name]  # kernel でのクラス名
                if truthy(cls.get(Y.class_name_in_kernel)):
                    attr[Y.class_name] = cls[Y.class_name_in_kernel]
            HRMPClassPlugin._class_info[Y.root] = {
                Y.processorID: 0,
                Y.class_name: "root",
                Y.locality: "root",
            }

    def check_class(self, class_name: Any) -> bool:
        """クラス名が有効かチェックする。"""
        assert HRMPClassPlugin._class_info is not None
        return HRMPClassPlugin._class_info.get(sym(class_name)) is not None

    def get_PU_kernel_class(self) -> Any:  # PU: Processing Unit
        """カーネル(HRMP3)での処理単位のクラス名を得る。"""
        assert HRMPClassPlugin._class_info is not None
        if HRMPClassPlugin._class_info.get(self._class1) is not None:
            return HRMPClassPlugin._class_info[self._class1][Y.class_name]
        return to_s(self._class1)

    def get_PU_attr(self) -> Any:  # attr for Processing Unit
        assert HRMPClassPlugin._class_info is not None
        return HRMPClassPlugin._class_info.get(self._class1)

    def get_NPU_attr(self) -> Any:  # attr for Non-Processing Unit
        """当初は PU と NPU で分けていたが、現在は分けていない。"""
        assert HRMPClassPlugin._class_info is not None
        return HRMPClassPlugin._class_info.get(self._class1)

    def get_class_name(self) -> Any:
        return self.get_PU_kernel_class()

    def get_processorID(self) -> Any:
        assert HRMPClassPlugin._class_info is not None
        return HRMPClassPlugin._class_info[self._class1][Y.processorID]

    @classmethod
    def get_processorID_of(cls, class_name: Any) -> Any:  # Ruby: self.get_processorID
        assert HRMPClassPlugin._class_info is not None
        return HRMPClassPlugin._class_info[sym(class_name)][Y.processorID]

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass

    def gen_factory(self, node_root: Any) -> None:
        pass
