"""CelltypePlugin.rb の移植（内部仕様9.1節）。

セルタイププラグインを実装する場合の親クラス。このクラスの親クラスで定義されている
各メソッドも呼び出される、または呼び出せる。
"""

from __future__ import annotations

from typing import Any

from tecsgen.core.plugin import Plugin
from tecsgen.core.syntaxobj.cdlstring import CDLString


class CelltypePlugin(Plugin):
    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: Celltype   セルタイプ（インスタンス）"""
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

    # ------ コード生成段階で呼び出されるメソッド --------

    def gen_factory(self, file: Any) -> None:
        """tCelltype_factory.h に挿入するコードを生成する。

        file 以外の他のファイルにファクトリコードを生成してもよい。
        セルタイププラグインが指定されたセルタイプのみ呼び出される。
        """
