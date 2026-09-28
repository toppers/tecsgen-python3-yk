"""MrubyBridgeCelltypePlugin.rb の移植。

Ruby 版はクラス名に反して `CompositePlugin` の子として定義されている（CelltypePlugin 版はコメント
アウトされている）。そのため通常のセルタイプに `generate( MrubyBridgeCelltypePlugin, ... )` を
指定すると `P2002 not kind of CelltypePlugin` になる（正解データでも同じ。そのまま再現する）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.CompositePlugin import CompositePlugin
from tecsgen.plugin.lib.MrubyBridgeCelltypePluginModule import (
    MrubyBridgeCelltypePluginModule,
)


class MrubyBridgeCelltypePlugin(MrubyBridgeCelltypePluginModule, CompositePlugin):
    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        MrubyBridgeCelltypePluginModule.gen_post_code_module(file)
