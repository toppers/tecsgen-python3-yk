"""classtype.rb の移植。region の class を記憶するクラス（`ClassType`）。

クラスプラグイン（FMPPlugin など）は P5 で移植する。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.plugin_module import PluginModule
from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import rb_print, rb_puts, sym, to_s, truthy


class ClassType(PluginModule, Node):
    """@name::Symbol / @region::Region / @plugin_name::Symbol / @option::String クラス名 | :global
    @plugin::ClassPlugin の子クラス / @node_root::Region
    """

    # {:node_root => { :class_type => [ region, ... ] } }
    _class_regions: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        ClassType._class_regions = {}

    def __init__(self, region: Any, name: Any, option: Any, node_root: Any) -> None:
        super().__init__()
        dbg_print(
            f"ClassType.new: region={to_s(region.get_name())} class_name={to_s(name)} "
            f"option={to_s(option)} node_root={to_s(node_root.get_name())}\n"
        )
        self._name = name
        self._plugin_name = sym(to_s(name) + "Plugin")
        self._pluginClass = self.load_plugin(self._plugin_name, "ClassPlugin")
        self._region = region
        self._option = option
        self._node_root = node_root

        if ClassType._class_regions.get(node_root) is None:
            ClassType._class_regions[node_root] = {}
        regions = ClassType._class_regions[node_root]
        if truthy(regions.get(name)):
            if not any(r is region for r in regions[name]):
                regions[name].append(region)
        else:
            regions[name] = [region]

    def create_class_plugin(self) -> None:
        if not truthy(self._plugin):
            dbg_print(
                f"create_class_plugin region={to_s(self._region.get_name())} name={to_s(self._name)} "
                f"option={to_s(self._option)}\n"
            )
            if self._pluginClass is None:
                return
            self._plugin = self._pluginClass(self._region, self._name, self._option)
            self._plugin.set_locale(self._locale)

    def add_through_plugin(
        self, join: Any, from_region: Any, to_region: Any, through_type: Any
    ) -> Any:
        return self._plugin.add_through_plugin(
            join, from_region, to_region, through_type
        )

    def joinable(
        self, from_region: Any, to_region: Any, through_type: Any
    ) -> Any:  # Ruby: joinable?
        dbg_print(
            f"ClassType.joinable?: from_region={to_s(from_region.get_name())} "
            f"to_region=#<Region> through_type={to_s(through_type)}\n"
        )
        return self._plugin.joinable(from_region, to_region, through_type)

    def check_class(self, class_name: Any) -> None:
        dbg_print(f"ClassType#check_class class_name={to_s(class_name)}\n")
        if self._plugin is None or self._plugin.check_class(class_name) is False:
            self.cdl_error("S9999 '$1': invalide class name", class_name)

    def get_name(self) -> Any:
        return self._name

    def get_plugin(self) -> Any:
        return self._plugin

    @classmethod
    def get_class_regions(cls, node_root: Any) -> Any:
        if truthy(ClassType._class_regions.get(node_root)):
            return ClassType._class_regions[node_root]
        return {}

    def get_regions(self, node_root: Any) -> Any:
        return ClassType._class_regions[node_root].get(self._name)

    def get_option(self) -> Any:
        dbg_print(f"ClassType: get_option: {to_s(self._option)}\n")
        return self._option

    def get_kind(self) -> Any:
        """ドメイン種別を得る。"""
        dbg_print(
            f"ClassType#get_kind plugin_name={to_s(self._plugin_name)} plugin=#<Plugin> DomainType=#<ClassType>\n"
        )
        return self._plugin.get_kind()

    def show_tree(self, indent: int) -> None:
        rb_print("  " * (indent + 1))
        rb_puts(
            f"class: name={to_s(self._name)} plugin={to_s(self._plugin_name)} option={to_s(self._option)}"
        )
