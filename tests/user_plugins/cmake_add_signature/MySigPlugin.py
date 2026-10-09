from __future__ import annotations

from typing import Any

from tecsgen.core.tecsgen import CMake
from tecsgen.plugin.SignaturePlugin import SignaturePlugin


class MySigPlugin(SignaturePlugin):
    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)
        CMake.add_source("signature_plugin.c")
        CMake.add_define("K_SIGNATURE=1")
        CMake.add_include("inc_signature")
        CMake.add_line("# from signature")
