"""MrubyBridgeCompositePlugin.rb の移植。composite セルタイプのセルごとに MrubyBridgeCellPlugin を適用する。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.CompositePlugin import CompositePlugin
from tecsgen.plugin.lib.MrubyBridgeCelltypePluginModule import (
    MrubyBridgeCelltypePluginModule,
)


class MrubyBridgeCompositePlugin(MrubyBridgeCelltypePluginModule, CompositePlugin):
    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        MrubyBridgeCelltypePluginModule.gen_post_code_module(file)
