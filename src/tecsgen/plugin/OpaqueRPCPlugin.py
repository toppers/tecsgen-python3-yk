"""OpaqueRPCPlugin.rb の移植（内部仕様9章）。Opaque RPC チャンネルを生成するプラグイン。

以下を仮定（制限事項）:
  呼び元、呼び先のエンディアン、char, short, int_t, long_t, intptr_t のサイズが同じ
  有符号、無符号でサイズが同じ
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenOpaqueMarshaler import GenOpaqueMarshaler
from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import Symbol, sym, to_s


class OpaqueRPCPlugin(ThroughPlugin, GenOpaqueMarshaler, GenParamCopy):
    # OpaqueRPCPlugin 専用のオプション（GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC の複製 + 追加）
    OPAQUE_RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    def __init__(
        self,
        cell_name: Any,
        plugin_arg: Any,
        next_cell: Any,
        next_cell_port_name: Any,
        next_cell_port_subscript: Any,
        signature: Any,
        celltype: Any,
        caller_cell: Any,
    ) -> None:
        """説明は ThroughPlugin (plugin.rb) を参照。"""
        super().__init__(
            cell_name,
            plugin_arg,
            next_cell,
            next_cell_port_name,
            next_cell_port_subscript,
            signature,
            celltype,
            caller_cell,
        )
        self._b_noClientSemaphore = False
        self.initialize_opaque_marshaler()

        self._plugin_arg_check_proc_tab = OpaqueRPCPlugin.OPAQUE_RPC_PLUGIN_ARG_PROC
        self.parse_plugin_arg()
        self.check_opener_code()
        self.check_PPAllocator()

        from tecsgen.ruby_compat import rb_print

        rb_print(f"OpaqueRPCPlugin: {to_s(self._clientChannelCell)}\n")

        from tecsgen.context import get_context

        self._rpc_server_channel_celltype_name = (
            f"tOpaqueRPCPlugin_{to_s(self._TDRCelltype)}_{to_s(self._serverChannelCelltype)}_"
            f"{to_s(self._signature.get_global_name())}"
        )
        self._rpc_server_channel_celltype_file_name = (
            f"{get_context().gen}/{self._rpc_server_channel_celltype_name}.cdl"
        )
        self._rpc_client_channel_celltype_name = (
            f"tOpaqueRPCPlugin_{to_s(self._TDRCelltype)}_{to_s(self._clientChannelCelltype)}_"
            f"{to_s(self._signature.get_global_name())}"
        )
        self._rpc_client_channel_celltype_file_name = (
            f"{get_context().gen}/{self._rpc_client_channel_celltype_name}.cdl"
        )

    def gen_plugin_decl_code(self, file: Any) -> None:
        from tecsgen.core.plugin import CFile

        self.gen_marshaler_celltype()

        # チャンネル composite セルタイプの生成
        #  ここで生成された CDL ファイルは、tecsgen が直接 import するのではなく
        #  セルコードの CDL から import される

        f = CFile.open(self._rpc_client_channel_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            f'import( "{self._marshaler_celltype_file_name}" );\n\n'
            "/* RPC Client side composite celltype */\n"
            f"composite {self._rpc_client_channel_celltype_name} {{\n"
            "  /* marshaler entry port */\n"
            f"  entry {to_s(self._signature.get_namespace_path())} eThroughEntry;\n"
            "  call  sChannel cChannel;\n"
            "  [optional]\n"
            "    call sRPCErrorHandler cErrorHandler;\n"
            "  [optional]\n"
            "    call sSemaphore cLockChannel;\n\n"
            f"  cell {to_s(self._TDRCelltype)} TDR {{\n"
            "    cChannel => composite.cChannel;\n"
            "  };\n"
            f"  cell {to_s(self._marshaler_celltype_name)} Marshaler{{\n"
            "    cTDR = TDR.eTDR;\n"
            "    cErrorHandler => composite.cErrorHandler;\n"
            "    cLockChannel  => composite.cLockChannel;\n"
            "  };\n\n"
            "  composite.eThroughEntry => Marshaler.eClientEntry;\n"
            "};\n"
        )
        f.close()

        if self._PPAllocatorSize:
            alloc_cell = (
                f"  cell tPPAllocator PPAllocator {{\n"
                f"    heapSize = {to_s(self._PPAllocatorSize)};\n"
                "  };\n"
            )
            alloc_call_port_join = "    cPPAllocator = PPAllocator.ePPAllocator;\n"
        else:
            alloc_cell = ""
            alloc_call_port_join = ""

        f = CFile.open(self._rpc_server_channel_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            f'import( "{self._marshaler_celltype_file_name}" );\n\n'
            "/* RPC Server side composite celltype */\n"
            f"composite {self._rpc_server_channel_celltype_name} {{\n"
            "  /* Interface */\n"
            f"  call  {to_s(self._signature.get_namespace_path())} {to_s(self._call_port_name)};\n"
            "  call  sChannel   cChannel;\n"
            "  [optional]\n"
            "    call sRPCErrorHandler cErrorHandler;\n"
            "  entry sUnmarshalerMain  eService;\n\n"
            "  /* Implementation */\n"
            f"  cell {to_s(self._TDRCelltype)} TDR {{\n"
            "    cChannel => composite.cChannel;\n"
            "  };\n"
            f"{alloc_cell}  cell {to_s(self._unmarshaler_celltype_name)} Unmarshaler{{\n"
            "    cTDR        = TDR.eTDR;\n"
            "    cErrorHandler => composite.cErrorHandler;\n"
            f"    cServerCall => composite.{to_s(self._call_port_name)};\n"
            f"{alloc_call_port_join}  }};\n"
            "  composite.eService => Unmarshaler.eService;\n"
            "};\n"
        )
        f.close()

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        from tecsgen.core.componentobj.namespace import Namespace

        self.gen_plugin_decl_code(file)

        cell = Namespace.find(self._next_cell.get_namespace_path())

        file.print(
            f'import( "{self._rpc_client_channel_celltype_file_name}" );\n'
            f'import( "{self._rpc_server_channel_celltype_file_name}" );\n\n'
        )

        ##### クライアント側のセルの生成 #####
        nest = self._start_region.gen_region_str_pre(file)
        nest_str = "  " * nest

        # セマフォの生成
        if self._b_noClientSemaphore is False:
            file.print(
                "\n"
                f'{nest_str}  //  Semaphore for Multi-task use ("specify noClientSemaphore" option to delete this)\n'
                f"{nest_str}  cell {to_s(self._semaphoreCelltype)} {to_s(self._serverChannelCell)}_Semaphore{{\n"
                f"{nest_str}    {to_s(self._semaphoreInitializer)}\n"
                f"{nest_str}  }};\n"
            )

        # クライアント側チャンネル (TINET, Socket など)の生成
        file.print(
            f"{nest_str}  //  Client Side Channel\n"
            f"{nest_str}  cell {to_s(self._clientChannelCelltype)} {to_s(self._clientChannelCell)}{{\n"
            f"{nest_str}    {to_s(self._clientChannelInitializer)}\n"
            f"{nest_str}  }};\n\n"
            f"{nest_str}  //  Marshaler\n"
        )

        # セマフォの結合文
        if self._b_noClientSemaphore is False:
            semaphore = f"{nest_str}    cLockChannel = {to_s(self._serverChannelCell)}_Semaphore.eSemaphore;\n"
        else:
            semaphore = ""

        ### クライアント側チャンネル (マーシャラ+TDR)の生成 ###
        # アロケータの指定があるか？
        if len(cell.get_allocator_list()) > 0:
            file.print(nest_str)
            file.print("[allocator(")

            delim = ""
            for type_, eport, subsc, func, buf, alloc in cell.get_allocator_list():
                alloc_str = to_s(alloc)
                subst = self._substituteAllocator.get(sym(alloc_str))
                if subst:
                    alloc_str = f"{subst[2]}.{subst[3]}"

                file.print(delim)
                delim = ",\n"  # 最終行には出さない

                subsc_str = f"[{to_s(subsc)}]" if subsc else ""

                eport = "eThroughEntry"  # RPCの受け口名に変更
                file.print(nest_str)
                file.print(f"{eport}{subsc_str}.{to_s(func)}.{to_s(buf)} = {alloc_str}")

            file.puts(")]")

        if self._clientErrorHandler:
            clientErrorHandler_str = (
                f"{nest_str}    cErrorHandler = {to_s(self._clientErrorHandler)};\n"
            )
        else:
            clientErrorHandler_str = ""

        file.print(
            f"{nest_str}  cell {self._rpc_client_channel_celltype_name} {to_s(self._cell_name)} {{\n"
            f"{nest_str}    cChannel = {to_s(self._clientChannelCell)}.eC0;\n"
            f"{clientErrorHandler_str}{semaphore}{nest_str}  }};\n\n"
        )
        ### END: クライアント側チャンネル (マーシャラ+TDR)の生成 ###

        self._start_region.gen_region_str_post(file)
        file.print("\n\n")

        ##### サーバー側のセルの生成 #####
        nest = self._end_region.gen_region_str_pre(file)
        nest_str = "  " * nest
        subscript = (
            f"[{to_s(self._next_cell_port_subscript)}]"
            if self._next_cell_port_subscript
            else ""
        )

        if self._serverErrorHandler:
            serverErrorHandler_str = (
                f"{nest_str}    cErrorHandler = {to_s(self._serverErrorHandler)};\n"
            )
        else:
            serverErrorHandler_str = ""

        if self._b_genOpener:
            opener = f"{nest_str}    cOpener       = {to_s(self._serverChannelCell)}.eOpener;\n"
        else:
            opener = ""

        # サーバー側チャンネル (TINET, Socket など)
        file.print(
            "\n"
            f"{nest_str}  //  Server Side Channel\n"
            f"{nest_str}  cell {to_s(self._serverChannelCelltype)} {to_s(self._serverChannelCell)}{{\n"
            f"{nest_str}    {to_s(self._serverChannelInitializer)}\n"
            f"{nest_str}  }};\n"
        )

        # サーバー側チャンネル (アンマーシャラ+TDR)
        file.print(
            "\n"
            f"{nest_str}  //  Unmarshaler\n"
            f"{nest_str}  cell {self._rpc_server_channel_celltype_name} {to_s(self._serverChannelCell)}_Unmarshaler {{\n"
            f"{nest_str}    cChannel = {to_s(self._serverChannelCell)}.eC1;\n"
            f"{nest_str}    {to_s(self._call_port_name)} = {self._next_cell.get_namespace_path().get_path_str()}."
            f"{to_s(self._next_cell_port_name)}{subscript};\n"
            f"{serverErrorHandler_str}{nest_str}  }};\n"
        )

        # サーバー側タスクメイン
        file.print(
            "\n"
            f"{nest_str}  //  Unmarshaler Task Main\n"
            f"{nest_str}  cell {to_s(self._taskMainCelltype)} {to_s(self._serverChannelCell)}_TaskMain {{\n"
            f"{nest_str}    cMain         = {to_s(self._serverChannelCell)}_Unmarshaler.eService;\n"
            f"{opener}{nest_str}  }};\n"
        )

        # サーバー側タスク
        file.print(
            "\n"
            f"{nest_str}  //  Unmarshaler Task\n"
            f"{nest_str}  cell {to_s(self._taskCelltype)} {to_s(self._serverChannelCell)}_Task {{\n"
            f"{nest_str}    cTaskBody         = {to_s(self._serverChannelCell)}_TaskMain.eMain;\n"
            f"{nest_str}    priority      = {to_s(self._taskPriority)};\n"
            f"{nest_str}    stackSize     = {to_s(self._stackSize)};\n"
            f'{nest_str}    attribute     = C_EXP( "TA_ACT" );  /* mikan : marshaler task starts at beginning */\n'
            f"{nest_str}  }};\n"
        )
        self._end_region.gen_region_str_post(file)

    def set_noClientSemaphore(self, rhs: Any) -> None:
        """プラグイン引数 noClientSemaphore のチェック。"""
        rhs_sym = sym(rhs)
        if rhs_sym == Symbol("true"):
            self._b_noClientSemaphore = True
        elif rhs_sym == Symbol("false"):
            self._b_noClientSemaphore = False
        else:
            self.cdl_error("RPCPlugin: specify true or false for noClientSemaphore")


OpaqueRPCPlugin.OPAQUE_RPC_PLUGIN_ARG_PROC = {
    **GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC,
    "noClientSemaphore": lambda obj, rhs: obj.set_noClientSemaphore(rhs),
}
