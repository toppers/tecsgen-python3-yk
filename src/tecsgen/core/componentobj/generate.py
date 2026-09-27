"""componentobj/generate.rb の移植。generate 文（signature, celltype, cell へのプラグインのロードと適用）。

core/generate.py（コード生成）とは別のモジュール。
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print
from tecsgen.core.plugin_module import PluginModule
from tecsgen.core.syntaxobj.node import Node
from tecsgen.ruby_compat import to_s, truthy


class Generate(PluginModule, Node):
    """@plugin_name:: Symbol / @object_nsp:: NamespacePath
    @option:: String '"', '"' で囲まれている / @plugin_object:: Plugin
    """

    def __init__(self, plugin_name: Any, object_nsp: Any, option: Any) -> None:
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.signature import Signature

        super().__init__()
        self._plugin_name = plugin_name
        self._object_nsp = object_nsp
        option = to_s(option)  # option は Token
        self._option = option
        self._plugin_object: Any = None

        dbg_print(f"generate: {to_s(plugin_name)} {to_s(object_nsp)} option={option}\n")

        obj = Namespace.find(object_nsp)
        if isinstance(obj, (Signature, Celltype, CompositeCelltype, Cell)):
            self._plugin_object = obj.apply_plugin(self._plugin_name, self._option)
        elif truthy(obj):
            # V1.5.0 以前の仕様では、signature のみ可能だった
            self.cdl_error(
                "S9999 generate: '$1' neither signature, celltype nor cell", object_nsp
            )
            return
        else:
            self.cdl_error("S9999 generate: signature '$1' not found", object_nsp)
