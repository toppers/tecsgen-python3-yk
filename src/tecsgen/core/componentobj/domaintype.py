"""domaintype.rb の移植。region の domain を記憶するクラス（`DomainType`）。

ドメインプラグイン（HRP2Plugin など）は P5 で移植する。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.plugin_module import PluginModule
from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import Y, class_name, rb_print, rb_puts, sym, to_s, truthy


class DomainType(PluginModule, Node):
    """@name::Symbol / @region::Region / @plugin_name::Symbol / @option::String
    @plugin::DomainPlugin の子クラス / @node_root::Region
    """

    # ドメインに属する region の Hash  { node_root => { :domain_type => [ region, ... ] } }
    _domain_regions: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        DomainType._domain_regions = {}

    def __init__(self, region: Any, name: Any, option: Any, node_root: Any) -> None:
        super().__init__()
        self._name = name
        self._plugin_name = sym(to_s(name) + "Plugin")
        self._pluginClass = self.load_plugin(self._plugin_name, "DomainPlugin")
        self._region = region
        self._option = option
        self._plugin: Any = None
        self._node_root = node_root

        if not truthy(DomainType._domain_regions.get(node_root)):
            DomainType._domain_regions[node_root] = {}
        regions = DomainType._domain_regions[node_root]
        if truthy(regions.get(name)):
            if not any(r is region for r in regions[name]):
                regions[name].append(region)
        else:
            regions[name] = [region]

    def create_domain_plugin(self) -> None:
        if not truthy(self._plugin):
            dbg_print(
                f"create_domain_plugin: plugin_name={to_s(self._plugin_name)} "
                f"class={class_name(self._pluginClass) if self._pluginClass is not None else ''} "
                f"region={to_s(self._region.get_name())} option={to_s(self._option)}\n"
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
        return self._plugin.joinable(from_region, to_region, through_type)

    def get_name(self) -> Any:
        return self._name

    @classmethod
    def get_domain_regions(cls, node_root: Any) -> Any:
        """リージョンの Hash を得る。"""
        if not truthy(DomainType._domain_regions.get(node_root)):
            return {}
        return DomainType._domain_regions[node_root]

    def get_regions(self, node_root: Any) -> Any:
        return DomainType._domain_regions[node_root].get(self._name)

    def get_option(self) -> Any:
        return self._option

    def get_kind(self) -> Any:
        """ドメイン種別を得る（:kernel, :user, :OutOfDomain）。"""
        dbg_print(
            f"DomainType#get_kind plugin_name={to_s(self._plugin_name)} plugin=#<Plugin> DomainType=#<DomainType>\n"
        )
        if truthy(self._plugin):
            return self._plugin.get_kind()
        return Y.OutOfDomain  # domain 指定されていないケース

    def show_tree(self, indent: int) -> None:
        rb_print("  " * (indent + 1))
        rb_puts(
            f"domain: name={to_s(self._name)} plugin={to_s(self._plugin_name)} option={to_s(self._option)}"
        )
