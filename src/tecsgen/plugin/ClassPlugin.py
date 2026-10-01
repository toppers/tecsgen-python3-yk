"""ClassPlugin.rb の移植（内部仕様9.1節）。クラスプラグインの親クラス。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.plugin import Plugin
from tecsgen.ruby_compat import Y


class ClassPlugin(Plugin):
    def __init__(self, region: Any, name: Any, option: Any) -> None:
        """class 指定されたリージョンが定義された。

        option:: String  class 指定子の第二引数 (クラス名)
        """
        super().__init__()

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        """結合 join にプラグインを挿入する（説明は DomainPlugin#add_through_plugin を参照）。"""
        return None

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        return False

    def check_class(self, class_name: Any) -> bool:
        return False

    def get_class_name(self) -> Any:
        return Y.kernel

    def gen_factory(self, node_root: Any) -> None:
        """ClassPlugin の factory は特定のファイルへの出力が想定されていない。"""
