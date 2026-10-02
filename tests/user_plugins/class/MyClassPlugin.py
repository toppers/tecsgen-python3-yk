"""test/class/MyClassPlugin.rb の Python 版（クラスプラグインの実例）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.core.tool_info import TOOL_INFO
from tecsgen.plugin.ClassPlugin import ClassPlugin
from tecsgen.ruby_compat import Y, rb_print, sym, to_s, truthy

# クラス定義(.cdf) の JSON スキーマ
CLASS_DEF_SCHEMA: dict[Any, Any] = {
    sym("MyClass_class_def"): {
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


class MyClassPlugin(ClassPlugin):
    CLASS_DEF_schema = CLASS_DEF_SCHEMA

    # nTECSGENConfig::tClassConfig セルタイプのセル
    # { class_name_in_TECS => {:processorID=>.., :class_name=>.., :locality=>..}}
    _class_info: ClassVar[dict[Any, Any] | None] = None

    def __init__(self, region: Any, class_type_name: Any, option: Any) -> None:
        super().__init__(region, class_type_name, option)
        if MyClassPlugin._class_info is None:
            self.validate_and_set_class_info()
        rb_print(
            f"MyClassPlugin: initialize: region={to_s(region.get_name())}, "
            f"classTypeName={to_s(class_type_name)}, option={to_s(option)}\n"
        )

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        rb_print(
            f"MyClassPlugin: add_through_plugin: {to_s(current_region.get_name())}"
            f"=>{to_s(next_region.get_name())}, {to_s(join.get_owner().get_name())}."
            f"{to_s(join.get_definition().get_name())}=>{to_s(join.get_cell().get_name())}."
            f"{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )
        return [sym("TracePlugin"), ""]

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        rb_print(
            f"MyClassPlugin: joinable? from {to_s(current_region.get_name())} "
            f"to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass

    def get_kind(self) -> Any:
        return Y.kernel

    def validate_and_set_class_info(self) -> None:
        """__tool_info__( "MyClass_class_def" ) の JSON 形式のデータを検証する。"""
        validator = TOOL_INFO.VALIDATOR(sym("MyClass_class_def"), CLASS_DEF_SCHEMA)
        if validator.validate():
            MyClassPlugin._class_info = {}
            info = TOOL_INFO.get_tool_info(sym("MyClass_class_def"))
            if info is None:
                self.cdl_error(
                    "MyClass9999 not found __tool_info__( MyClass_class_def )"
                )
            for cls in info[Y.class_def]:
                attr: dict[Any, Any] = {}
                # TECS でのクラス名
                MyClassPlugin._class_info[sym(cls[Y.class_name])] = attr
                attr[Y.processorID] = cls[Y.processorID]
                attr[Y.locality] = cls[Y.locality]
                attr[Y.class_name] = cls[Y.class_name]  # kernel でのクラス名
                if truthy(cls.get(Y.class_name_in_kernel)):
                    attr[Y.class_name] = cls[Y.class_name_in_kernel]

    def check_class(self, class_name: Any) -> bool:
        rb_print(f"MyClassPlugin#check_class {to_s(class_name)}\n")
        assert MyClassPlugin._class_info is not None
        return bool(MyClassPlugin._class_info.get(sym(class_name)))
