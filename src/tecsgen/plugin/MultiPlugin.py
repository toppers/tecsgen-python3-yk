"""MultiPlugin.rb の移植（内部仕様9.5節）。

CDL上の付与位置ごとに別の具象クラスへ振り分けられるプラグインファミリーの基底クラス。
"""

from __future__ import annotations

from typing import Any

from tecsgen.core.syntaxobj.node import Node


class MultiPlugin(Node):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        from tecsgen.core.plugin_module import _import_plugin_class

        if super_class is _import_plugin_class("SignaturePlugin"):
            return _import_plugin_class("SignaturePlugin")
        if super_class is _import_plugin_class("CelltypePlugin"):
            return _import_plugin_class("CelltypePlugin")
        if super_class is _import_plugin_class("CellPlugin"):
            return _import_plugin_class("CellPlugin")
        if super_class is _import_plugin_class("ThroughPlugin"):
            return _import_plugin_class("ThroughPlugin")
        return None  # DomainPlugin や、それ以外の基底クラスは非対応
