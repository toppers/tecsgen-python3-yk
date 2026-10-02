"""test/domainPlugin/MyDomainPlugin.rb の Python 版。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.DomainPlugin import DomainPlugin
from tecsgen.ruby_compat import rb_print, sym, to_s


class MyDomainPlugin(DomainPlugin):
    def __init__(self, region: Any, domain_type_name: Any, option: Any) -> None:
        super().__init__(region, domain_type_name, option)
        rb_print(
            f"MyDomainPlugin: initialize: region={to_s(region.get_name())}, "
            f"domainTypeName={to_s(domain_type_name)}, option={to_s(option)}\n"
        )

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        rb_print(
            f"MyDomainPlugin: add_through_plugin: {to_s(current_region.get_name())}"
            f"=>{to_s(next_region.get_name())}, {to_s(join.get_owner().get_name())}."
            f"{to_s(join.get_definition().get_name())}=>{to_s(join.get_cell().get_name())}."
            f"{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )
        return [sym("TracePlugin"), ""]

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        rb_print(
            f"MyDomainPlugin: joinable? from {to_s(current_region.get_name())} "
            f"to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass

    def get_kind(self) -> Any:
        return sym("OutOfDomain")
