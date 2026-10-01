"""DomainPlugin.rb の移植（内部仕様9.1節）。ドメインプラグインの親クラス。"""

from __future__ import annotations

from typing import Any

from tecsgen.core.plugin import Plugin
from tecsgen.ruby_compat import Y


class DomainPlugin(Plugin):
    def __init__(self, region: Any, domain_type_name: Any, option: Any) -> None:
        """domain 指定されたリージョンが定義された。

        domain_type_name:: Symbol  domain 指定子の第一引数
        option:: String            domain 指定子の第二引数
        """
        super().__init__()

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        """結合 join にプラグインを挿入する。

        return:: [ plugin_name, option ] / [] (プラグイン挿入無しで結合可) / None (region 間の結合禁止)
        """
        return None

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        return False

    def get_kind(self) -> Any:
        """ドメイン種別を返す（:kernel, :user, :OutOfDomain）。"""
        return Y.kernel

    def gen_factory(self, node_root: Any) -> None:
        """DomainPlugin の factory は特定のファイルへの出力が想定されていない。"""
