"""MrubyBridgePlugin.rb の移植（内部仕様9.5節）。付与位置ごとに MrubyBridge*Plugin へ振り分ける MultiPlugin。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.MultiPlugin import MultiPlugin


class MrubyBridgePlugin(MultiPlugin):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        from tecsgen.context import dbg_print
        from tecsgen.core.plugin_module import _import_plugin_class

        if super_class is _import_plugin_class("SignaturePlugin"):
            dbg_print("MrubyBridgePlugin: SignaturePlugin")
            return _load("MrubyBridgeSignaturePlugin")
        if super_class is _import_plugin_class("CelltypePlugin"):
            dbg_print("MrubyBridgePlugin: CelltypePlugin")
            return _load("MrubyBridgeCelltypePlugin")
        if super_class is _import_plugin_class("CompositePlugin"):
            dbg_print("MrubyBridgePlugin: CompositePlugin")
            return _load("MrubyBridgeCompositePlugin")
        if super_class is _import_plugin_class("CellPlugin"):
            dbg_print("MrubyBridgePlugin: CellPlugin")
            return _load("MrubyBridgeCellPlugin")
        dbg_print("MrubyBridgePlugin: unsupported")
        return None


def _load(name: str) -> Any:
    """`require_tecsgen_lib` 相当。ロード時の副作用（Makefile への追加など）も実行回ごとに1回行う。"""
    from tecsgen.core.plugin_module import _import_plugin_class
    from tecsgen.plugin.MrubyBridgeSignaturePlugin import MrubyBridgeSignaturePlugin

    MrubyBridgeSignaturePlugin.on_load()
    return _import_plugin_class(name)
