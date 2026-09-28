"""OpaqueMarshalerPlugin.rb の移植（内部仕様9章）。

OpaqueRPC 用のマーシャラ、アンマーシャラセルタイプを生成するシグニチャプラグイン。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenOpaqueMarshaler import GenOpaqueMarshaler
from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import Symbol, sym


class OpaqueMarshalerPlugin(GenParamCopy, GenOpaqueMarshaler, SignaturePlugin):
    OPAQUE_MARSHALER_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)
        # Ruby 版では SignaturePlugin に @cell_name は無く nil のまま参照される
        # （initialize_opaque_marshaler のチャンネルセル名が "Server"・"Client" になる）
        self._cell_name = None
        self._b_noClientSemaphore = False
        self._noServerChannelOpenerCode = True
        self.initialize_opaque_marshaler()

        self._plugin_arg_check_proc_tab = (
            OpaqueMarshalerPlugin.OPAQUE_MARSHALER_PLUGIN_ARG_PROC
        )
        self.parse_plugin_arg()
        # check_PPAllocator
        if self._signature.need_PPAllocator(True):
            self._PPAllocatorSize = (
                1  # PPAllocatorの必要性有のために設定 (サイズは使われない)
            )

    def gen_cdl_file(self, file: Any) -> None:
        self.gen_marshaler_celltype()
        file.print(f'import( "{self._marshaler_celltype_file_name}" );\n')

    def subst_name(self, val: Any) -> Symbol:
        return sym("_")
