"""CellPlugin.rb の移植（内部仕様9.1節）。cell プラグインの共通の親クラス。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.plugin import Plugin
from tecsgen.core.syntaxobj.cdlstring import CDLString


class CellPlugin(Plugin):
    def __init__(self, cell: Any, option: Any) -> None:
        """このメソッドは、セルの構文解析が終わったところで呼び出される。この段階では意味解析が終わっていない。

        cell:: Cell   セル（インスタンス）
        """
        super().__init__()
        self._cell = cell
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """プラグインの後ろの CDL コードを生成する。

        複数のプラグインの post_code が一つのファイルに含まれるため、見出しをつけること。
        """
