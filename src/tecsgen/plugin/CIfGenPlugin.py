"""CIfGenPlugin.rb の移植（内部仕様9.5節）。付与位置ごとに CIfGen*Plugin へ振り分ける MultiPlugin。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.MultiPlugin import MultiPlugin


class CIfGenPlugin(MultiPlugin):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        from tecsgen.core.plugin_module import _import_plugin_class

        if super_class is _import_plugin_class("CelltypePlugin"):
            return _import_plugin_class("CIfGenCelltypePlugin")
        if super_class is _import_plugin_class("CellPlugin"):
            return _import_plugin_class("CIfGenCellPlugin")
        return None  # SignaturePlugin・ThroughPlugin・DomainPlugin には非対応
