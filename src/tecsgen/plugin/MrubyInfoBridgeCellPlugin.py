"""MrubyInfoBridgeCellPlugin.rb の移植。全シグニチャに MrubyInfoBridgeSignaturePlugin を generate する。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import to_s

_RX_INFO = re.compile(r"nMrubyInfo::")


class MrubyInfoBridgeCellPlugin(CellPlugin):
    def __init__(self, cell: Any, option: Any) -> None:
        """このメソッドは、セルの構文解析が終わったところで呼び出される（意味解析は終わっていない）。"""
        from tecsgen.core.syntaxobj.cdlstring import CDLString
        from tecsgen.plugin.MrubyBridgeSignaturePlugin import MrubyBridgeSignaturePlugin

        # Ruby 版はクラス定義の中で MrubyBridgeSignaturePlugin.rb を require する
        MrubyBridgeSignaturePlugin.on_load()
        super().__init__(cell, option)
        self._cell = cell
        self._plugin_arg_str = CDLString.remove_dquote(option)
        self._plugin_arg_list = {}

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """後ろの CDL コードを生成する。"""
        from tecsgen.core.componentobj.namespace import Namespace

        # Ruby 版は self.class.name と書いているが、self はクラスなので "Class" になる
        file.print("/* 'Class' post code */\n")
        cls.gen_signature_cdl(file, Namespace.get_root())

    @classmethod
    def gen_signature_cdl(cls, file: Any, namespace: Any) -> None:
        for sig in namespace.get_signature_list():
            if _RX_INFO.search(to_s(sig.get_namespace_path())):
                pass  # ignnore these signatures
            else:
                file.print(
                    f"    generate( MrubyInfoBridgeSignaturePlugin, {to_s(sig.get_namespace_path())}, "
                    '"auto_exclude=true" );\n'
                )
        for ns in namespace.get_namespace_list():
            cls.gen_signature_cdl(file, ns)
