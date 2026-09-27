"""celltypeModule.rb の移植。セルタイププラグイン (generate 指定子) を扱う mixin。"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tecsgen.context import get_context, print_exception
from tecsgen.core.plugin_module import PluginNotPorted
from tecsgen.ruby_compat import RubyRuntimeError, class_name, rb_print, to_s

# 型検査のときだけ Node の子として扱う（mixin から cdl_error などを呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.plugin_module import PluginModule
    from tecsgen.core.syntaxobj.node import Node

    class _Base(PluginModule, Node):
        pass
else:
    _Base = object


class CelltypePluginModule(_Base):
    _generate: Any
    _generate_list: list[Any]
    _cell_list: list[Any]
    _name: Any
    _locale: Any

    def celltype_plugin(self) -> None:
        """セルタイププラグイン (generate 指定子)。"""
        plugin_name = self._generate[0]
        option = self._generate[1]
        result = self.apply_plugin(plugin_name, option)
        while len(self._generate) < 3:
            self._generate.append(None)
        self._generate[2] = result

    def apply_plugin(self, plugin_name: Any, option: Any) -> Any:
        """セルタイププラグインをこのセルタイプに適用する。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if isinstance(self, Celltype):
            plugin_class: Any = "CelltypePlugin"
        elif isinstance(self, CompositeCelltype):
            plugin_class = "CompositePlugin"
        else:
            raise RubyRuntimeError(f"unknown class {class_name(type(self))}")

        pl_class = self.load_plugin(plugin_name, plugin_class)
        if pl_class is None:
            return None
        if get_context().verbose:
            rb_print(
                f"new celltype plugin: plugin_object = {class_name(type(pl_class))}.new( "
                f"{to_s(self._name)}, {to_s(option)} )\n"
            )

        plugin_object = None
        try:
            plugin_object = pl_class(self, option)
            self._generate_list.append([plugin_name, option, plugin_object])
            plugin_object.set_locale(self._locale)
            self.generate_and_parse(plugin_object)
        except PluginNotPorted:
            raise
        except Exception as evar:  # noqa: BLE001  Ruby の rescue Exception
            self.cdl_error("S1023 $1: fail to new", plugin_name)
            print_exception(evar)

        # 既に存在するセルに new_cell を適用
        for cell in self._cell_list:
            self.apply_plugin_cell(plugin_object, cell)

        return plugin_object

    def apply_plugin_cell(self, plugin: Any, cell: Any) -> None:
        try:
            plugin.new_cell(cell)
        except PluginNotPorted:
            raise
        except Exception as evar:  # noqa: BLE001
            self.cdl_error(
                "S1037 $1: celltype plugin fail to new_cell", class_name(type(plugin))
            )
            print_exception(evar)

    def celltype_plugin_new_cell(self, cell: Any) -> None:
        for generate in self._generate_list:
            celltype_plugin = generate[2]
            try:
                celltype_plugin.new_cell(cell)
            except PluginNotPorted:
                raise
            except Exception as evar:  # noqa: BLE001
                self.cdl_error(
                    "S1037 $1: celltype plugin fail to new_cell",
                    class_name(type(celltype_plugin)),
                )
                print_exception(evar)
