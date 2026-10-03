"""MrubyInfoBridgePlugin.rb の移植。付与位置ごとに MrubyInfoBridge*Plugin へ振り分ける MultiPlugin。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.MultiPlugin import MultiPlugin


class MrubyInfoBridgePlugin(MultiPlugin):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        from tecsgen.context import dbg_print
        from tecsgen.core.plugin_module import _import_plugin_class

        # case when (つまりは ===) では、期待したように一致しない模様
        if super_class is _import_plugin_class("SignaturePlugin"):
            dbg_print("MrubyInfoBridgePlugin: SignaturePlugin")
            from tecsgen.plugin.MrubyInfoBridgeSignaturePlugin import (
                MrubyInfoBridgeSignaturePlugin,
            )

            MrubyInfoBridgeSignaturePlugin.on_load()
            return _import_plugin_class("MrubyInfoBridgeSignaturePlugin")
        if super_class is _import_plugin_class("CellPlugin"):
            dbg_print("MrubyInfoBridgePlugin: CellPlugin")
            # Ruby 版のセルプラグインのファイルは、クラス本体で MrubyBridgeSignaturePlugin.rb を require する
            from tecsgen.plugin.MrubyBridgeSignaturePlugin import (
                MrubyBridgeSignaturePlugin,
            )

            MrubyBridgeSignaturePlugin.on_load()
            return _import_plugin_class("MrubyInfoBridgeCellPlugin")
        dbg_print("MrubyInfoBridgePlugin: unsupported")
        return None
