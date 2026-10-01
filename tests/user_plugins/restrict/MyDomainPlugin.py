"""test/restrict/MyDomainPlugin.rb の Python 版（restrict テスト用ドメインプラグイン）。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.DomainPlugin import DomainPlugin
from tecsgen.ruby_compat import sym


class MyDomainPlugin(DomainPlugin):
    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        return [sym("MyTracePlugin"), ""]

    # require の結合
    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:  # Ruby: joinable?
        # Ruby の `next_region.get_name == "::"`。Symbol と String は等しくない（そのまま比べる）
        if next_region.get_name() == "::":
            return True
        return None

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass
