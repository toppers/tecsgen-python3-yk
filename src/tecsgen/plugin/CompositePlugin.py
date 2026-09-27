"""CompositePlugin.rb の移植（内部仕様9章）。CompositeCelltype プラグインの共通の親クラス。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.plugin import Plugin
from tecsgen.core.syntaxobj.cdlstring import CDLString


class CompositePlugin(Plugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: CompositeCelltype   セルタイプ（インスタンス）"""
        super().__init__()
        self._celltype = celltype
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}

    def new_cell(self, cell: Any) -> None:
        """celltype プラグインを指定されたセルタイプのセルが生成された（セルタイププラグインに対する新しいセルの報告）。"""

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """後ろの CDL コードを生成する。

        複数のプラグインの post_code が一つのファイルに含まれるため、見出しをつけること。
        """
