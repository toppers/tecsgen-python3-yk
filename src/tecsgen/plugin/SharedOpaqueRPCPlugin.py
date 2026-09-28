"""SharedOpaqueRPCPlugin.rb の移植（内部仕様9章）。

1つの通信チャンネル（sharedChannelName）を複数の結合で共有する Opaque RPC プラグイン。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenOpaqueMarshaler import GenOpaqueMarshaler
from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import class_name, sym, to_s, truthy


class SharedOpaqueRPCPlugin(GenParamCopy, GenOpaqueMarshaler, ThroughPlugin):
    # チャンネルを共有するプラグインオブジェクトへのハッシュリスト
    # { chan_name => [ Plugin_obj0, Plugin_Obj1, ... ] }（@@shared_channel_list）
    _shared_channel_list: ClassVar[dict[Any, list[Any]]] = {}

    # SharedOpaqueRPCPlugin 専用のオプション（GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC の複製 + 追加）
    SHARED_OPAQUE_RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        """`@@shared_channel_list` を初期化する（1プロセスで何度も実行するテスト用）。"""
        SharedOpaqueRPCPlugin._shared_channel_list = {}

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
        from tecsgen.context import get_context

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
        self.initialize_opaque_marshaler()
        self._entry_port_name = sym(
            "eClientEntry"
        )  # Marshaler の受け口名 (through セルの入り口)

        # オプション：GenOpaqueMarshaler 参照
        self._plugin_arg_check_proc_tab = (
            SharedOpaqueRPCPlugin.SHARED_OPAQUE_RPC_PLUGIN_ARG_PROC
        )
        self._sharedChannelName: Any = None
        self.parse_plugin_arg()
        self.check_opener_code()
        self.check_PPAllocator()

        self._shared_channel_ct_name = sym("tSharedOpaqueRPCPluginChannel_tTDR")
        self._shared_channel_server_ct_name = sym(
            f"{to_s(self._shared_channel_ct_name)}_Server"
        )
        self._shared_channel_client_ct_name = sym(
            f"{to_s(self._shared_channel_ct_name)}_Client"
        )
        self._shared_channel_ct_file_name = (
            f"{get_context().gen}/{to_s(self._shared_channel_ct_name)}.cdl"
        )
        # Ruby 版では sharedChannelName が無いとき @shared_channel_cell は nil のまま使われる
        self._shared_channel_cell: Any = None
        if self._sharedChannelName is None:
            self.cdl_error("'sharedChannelName' option: mandatory")
        else:
            self._shared_channel_cell = self._sharedChannelName

        lst = SharedOpaqueRPCPlugin._shared_channel_list
        if lst.get(self._shared_channel_cell) is None:
            lst[self._shared_channel_cell] = [self]
        else:
            lst[self._shared_channel_cell].append(self)
        self._sub_channel_no = len(lst[self._shared_channel_cell]) - 1

        prev_start = lst[self._shared_channel_cell][0]._start_region
        if self._start_region != prev_start:
            # 初出と start リージョン不一致 (初出は、自分自身とチェックされる。無駄だが小さいので放置)
            self.cdl_error(
                "SharedRPCPlugin: start region mismatch current: "
                f"{to_s(self._region.get_name())} previous: {to_s(prev_start.get_name())}"
            )

        prev_end = lst[self._shared_channel_cell][0]._end_region
        if self._end_region != prev_end:
            # 初出と end リージョン不一致  (初出は、自分自身とチェックされる。無駄だが小さいので放置)
            self.cdl_error(
                "SharedRPCPlugin: end region mismatch current: "
                f"{to_s(self._region.get_name())} previous: {to_s(prev_end.get_name())}"
            )

    def set_sharedChannelName(self, rhs: Any) -> None:
        """プラグイン引数 sharedChannelCell のチェック。"""
        self._sharedChannelName = rhs

    def gen_plugin_decl_code(self, file: Any) -> None:
        from tecsgen.core.plugin import CFile

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        # （登録するだけで、生成済みでも以下を出力し直す。Ruby 版どおり）
        generated = ThroughPlugin._generated_celltype
        name = self._shared_channel_server_ct_name
        if generated.get(name) is None:
            generated[name] = [self]
        else:
            generated[name].append(self)

        self.gen_marshaler_celltype()

        # 同じ内容を二度書く可能性あり (AppFile は不可)
        # （Ruby 版は alloc_call_port・alloc_call_port_join を作るが使っていない）

        client = to_s(self._shared_channel_client_ct_name)
        server = to_s(self._shared_channel_server_ct_name)
        f = CFile.open(self._shared_channel_ct_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            "\n"
            "/* Shared Channel Celltype for Client */\n"
            f"composite {client} {{\n"
            "  entry  sTDR       eTDR;\n"
            "  entry  sSemaphore eSemaphore[];\n"
            "  call   sChannel   cClientChannel;\n\n"
            "  cell tTDR TDR {\n"
            "    cChannel => composite.cClientChannel;\n"
            "  };\n"
            "  cell tSemaphore Semaphore {\n"
            "    initialCount = 1;\n"
            '    attribute = C_EXP("TA_NULL");\n'
            "  };\n"
            "  cell tRPCSharedChannelMan SharedChannelMan{\n"
            "    cSemaphore             = Semaphore.eSemaphore;\n"
            "    cClientSideTDR         = TDR.eTDR;\n"
            "  };\n"
            "  composite.eSemaphore     => SharedChannelMan.eSemaphore;\n"
            "  composite.eTDR           => TDR.eTDR;\n"
            "};\n\n"
            "/* Shared Channel Celltype for Server */\n"
            "[active]\n"
            f"composite {server} {{\n"
            "  entry  sTDR       eTDR;\n"
            "  call   sChannel   cServerChannel;\n"
            "  call   sUnmarshalerMain  cUnmarshalAndCallFunction[];\n"
            "  call   sServerChannelOpener cOpener;\n"
            "  attr {\n"
            "    PRI    priority;\n"
            "  };\n\n"
            "  cell tTDR TDR {\n"
            "    cChannel => composite.cServerChannel;\n"
            "  };\n"
            "  cell tRPCSharedTaskMainWithOpener RPCSharedTaskMain {\n"
            "    cUnmarshalAndCallFunction => composite.cUnmarshalAndCallFunction;\n"
            "    cServerSideTDR = TDR.eTDR;\n"
            "    cOpener => composite.cOpener;\n"
            "  };\n"
            "  cell tTask Task {\n"
            "    cTaskBody = RPCSharedTaskMain.eMain;\n"
            '    attribute = C_EXP("TA_ACT");\n'
            "    stackSize = 4096;\n"
            "    priority = composite.priority;\n"
            "  };\n"
            "  composite.eTDR           => TDR.eTDR;\n"
            "};\n\n"
        )
        f.close()

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        from tecsgen.core.componentobj.namespace import Namespace

        self.gen_plugin_decl_code(file)

        file.print(
            "\n"
            f'import( "{self._marshaler_celltype_file_name}" );\n'
            f'import( "{self._shared_channel_ct_file_name}" );\n'
        )

        nest = self._start_region.gen_region_str_pre(file)
        indent_str = "  " * nest
        if self._next_cell_port_subscript is not None:
            subscript = "[" + to_s(self._next_cell_port_subscript) + "]"
        else:
            subscript = ""

        # セルを探す
        cell = Namespace.find(self._next_cell.get_namespace_path())

        sc = to_s(self._shared_channel_cell)
        # 共有される通信チャンネルの生成のプロトタイプ宣言
        file.print(
            f"{indent_str}cell {to_s(self._shared_channel_client_ct_name)} {sc};\n"
        )

        # マーシャラセルの生成（アロケータコードの生成から）
        # アロケータの指定があるか？
        if len(cell.get_allocator_list()) > 0:
            file.print(f"{indent_str}[allocator(")

            delim = ""
            for _type, eport, subsc, func, buf, alloc in cell.get_allocator_list():
                alloc_str = to_s(alloc)
                subst = self._substituteAllocator.get(sym(alloc_str))
                if subst:
                    alloc_str = to_s(subst[2]) + "." + to_s(subst[3])

                file.print(delim)
                delim = f",\n{indent_str}           "  # 最終行には出さない

                # Ruby 版は単一引用符の '[#{subsc}]' なので、式展開されずそのまま出る
                subsc_str = (
                    "[#{subsc}]" if subsc is not None and subsc is not False else ""
                )

                eport = to_s(self._entry_port_name)  # RPCの受け口名に変更
                file.print(f"{eport}{subsc_str}.{to_s(func)}.{to_s(buf)} = {alloc_str}")

            file.puts(")]")

        # マーシャラセル本体生成
        file.print(
            "/* OpaqueRPC Marshaler Cell */\n"
            f"{indent_str}cell {to_s(self._marshaler_celltype_name)} {to_s(self._cell_name)} {{\n"
            f"{indent_str}  cTDR         = {sc}.eTDR;\n"
            f"{indent_str}  cLockChannel = {sc}.eSemaphore[{self._sub_channel_no}];\n"
            f"{indent_str}}};\n"
        )
        self._start_region.gen_region_str_post(file)

        # アンマーシャラセルの出力
        # セル本体の生成（Ruby 版どおり、インデントは start_region のものを使い続ける）
        self._end_region.gen_region_str_pre(file)

        file.print(
            "/* Server Channel Cell prototype */\n"
            f"{indent_str}cell {to_s(self._shared_channel_server_ct_name)} "
            f"{to_s(self._sharedChannelName)}_Server;\n\n"
        )

        # PPAllocator が必要か?
        if truthy(self._PPAllocatorSize):
            if self._sub_channel_no == 0:
                file.print(
                    f"{indent_str}cell tPPAllocator PPAllocator_{sc}{{\n"
                    f"{indent_str}  heapSize = {to_s(self._PPAllocatorSize)};\n"
                    f"{indent_str}}};\n"
                )
            ppallocator_join = (
                f"{indent_str}  cPPAllocator = PPAllocator_{sc}.ePPAllocator;\n"
            )
        else:
            ppallocator_join = ""

        file.print(
            f"{indent_str}cell {to_s(self._unmarshaler_celltype_name)} {to_s(self._cell_name)}_Server {{\n"
            f"{indent_str}  cTDR         = {sc}_Server.eTDR;\n"
            f"{indent_str}  cServerCall  = {self._next_cell.get_namespace_path().get_path_str()}."
            f"{to_s(self._next_cell_port_name)}{subscript};\n"
            f"{ppallocator_join}{indent_str}}};\n"
        )
        self._end_region.gen_region_str_post(file)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """post コード(CDL) を生成する。"""
        file.print(f"/* '{class_name(cls)}' post code */\n")

        for (
            chan_name,
            plugin_obj_array,
        ) in SharedOpaqueRPCPlugin._shared_channel_list.items():
            file.print(f"/* '{to_s(chan_name)}' shared channel */\n")
            plugin_obj_array[0].gen_post_code_channel(file, plugin_obj_array)

    def gen_post_code_channel(self, file: Any, plugin_obj_array: list[Any]) -> None:
        """共有チャンネルを生成する（Ruby のインスタンスメソッド gen_post_code）。

        このメソッドは、チャンネルを共有する最初のプラグインオブジェクトのみ呼び出される。
        """
        name = to_s(self._sharedChannelName)

        # 共有されている通信チャンネルの生成
        nest = self._start_region.gen_region_str_pre(file)
        indent_str = "  " * nest
        file.print(
            f"{indent_str}cell {to_s(self._shared_channel_client_ct_name)} {name} {{\n"
            f"{indent_str}    cClientChannel = {to_s(self._clientChannelCell)}.eC0;\n"
            f"{indent_str}}};\n"
        )
        self._start_region.gen_region_str_post(file)

        nest = self._end_region.gen_region_str_pre(file)
        indent_str = "  " * nest
        file.print(
            f"{indent_str}cell {to_s(self._shared_channel_server_ct_name)} {name}_Server {{\n"
        )
        file.print(
            f"{indent_str}    cServerChannel = {to_s(self._serverChannelCell)}.eC1;\n"
            f"{indent_str}    cOpener        = {to_s(self._serverChannelCell)}.eOpener;\n"
        )
        for po in plugin_obj_array:
            file.print(
                f"{indent_str}    cUnmarshalAndCallFunction[] = {to_s(po._cell_name)}_Server.eService;\n"
            )
        file.print(
            f"{indent_str}    priority = {to_s(self._taskPriority)};\n{indent_str}}};\n"
        )
        self._end_region.gen_region_str_post(file)


SharedOpaqueRPCPlugin.SHARED_OPAQUE_RPC_PLUGIN_ARG_PROC = {
    **GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC,
    "sharedChannelName": lambda obj, rhs: obj.set_sharedChannelName(rhs),
}
