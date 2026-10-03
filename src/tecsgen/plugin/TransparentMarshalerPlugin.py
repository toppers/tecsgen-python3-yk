"""TransparentMarshalerPlugin.rb の移植（内部仕様9章）。

Transparent RPC 用のマーシャラ、アンマーシャラセルタイプを生成するシグニチャプラグイン。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.lib.GenTransparentMarshaler import GenTransparentMarshaler
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import Symbol, rb_print, sym, to_s


class TransparentMarshalerPlugin(
    GenParamCopy, GenTransparentMarshaler, SignaturePlugin
):
    TRANSPARENT_MARSHALER_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    def __init__(self, signature: Any, option: Any) -> None:
        super().__init__(signature, option)
        self._b_noClientSemaphore = False
        self._noServerChannelOpenerCode = True
        self.initialize_transparent_marshaler(signature.get_name())

        self._plugin_arg_check_proc_tab = (
            TransparentMarshalerPlugin.TRANSPARENT_MARSHALER_PLUGIN_ARG_PROC
        )
        self.parse_plugin_arg()
        # check_PPAllocator
        if self._signature.need_PPAllocator(True):
            self._pp_allocator_size = (
                1  # PPAllocatorの必要性有のために設定 (サイズは使われない)
            )
            necessity = "Necessary"
        else:
            necessity = "Unnecessary"

        rb_print(
            f"TransparentMarshalerPlugin: signature={to_s(signature.get_namespace_path())}, "
            f"PPAllocator={necessity}\n"
        )

    def gen_cdl_file(self, file: Any) -> None:
        self.gen_marshaler_celltype()
        file.print(f'import( "{self._marshaler_celltype_file_name}" );\n')

    def subst_name(self, val: Any) -> Symbol:
        return sym("_")
