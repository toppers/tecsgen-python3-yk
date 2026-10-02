"""test/ErrorCase/MyDomainPlugin.rb の Python 版。"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.DomainPlugin import DomainPlugin


class MyDomainPlugin(DomainPlugin):
    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass
