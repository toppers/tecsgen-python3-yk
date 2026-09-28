"""SharedRPCPlugin.rb の移植（内部仕様9章）。

1つの通信チャンネル（channelCell）を複数の結合で共有する Transparent RPC プラグイン。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.lib.GenTransparentMarshaler import GenTransparentMarshaler
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import class_name, sym, to_s


class SharedRPCPlugin(GenParamCopy, GenTransparentMarshaler, ThroughPlugin):
    # チャンネルセル名 → そのチャンネルを共有するプラグインインスタンスのリスト（@@shared_channel_list）
    _shared_channel_list: ClassVar[dict[Any, list[Any]]] = {}

    @classmethod
    def reset(cls) -> None:
        """`@@shared_channel_list` を初期化する（1プロセスで何度も実行するテスト用）。"""
        SharedRPCPlugin._shared_channel_list = {}

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
        self.initialize_transparent_marshaler(cell_name)

        # オプション：GenTransparentMarshaler 参照
        self._plugin_arg_check_proc_tab = GenTransparentMarshaler.RPC_PLUGIN_ARG_PROC
        self._channel_cell_name = ""  # nil にしておく
        self.parse_plugin_arg()

        gen = get_context().gen
        self._shared_channel_ct_name = sym(
            f"tSharedRPCPlugin_{to_s(self._channel_celltype)}"
        )
        self._shared_channel_ct_file_name = (
            f"{gen}/{to_s(self._shared_channel_ct_name)}.cdl"
        )
        self._rpc_channel_celltype_name = sym(
            f"tSharedRPCPlugin_{to_s(self._tdr_celltype)}_{to_s(self._channel_celltype)}_"
            f"{to_s(self._signature.get_global_name())}"
        )
        self._rpc_channel_celltype_file_name = (
            f"{gen}/{to_s(self._rpc_channel_celltype_name)}.cdl"
        )

        self._shared_channel_cell = self._channel_cell_name
        if self._shared_channel_cell == "":
            self.cdl_error("SharedRPCPlugin: need channelCellName option")

        lst = SharedRPCPlugin._shared_channel_list
        if lst.get(self._shared_channel_cell) is None:
            # 初出
            lst[self._shared_channel_cell] = [self]
        else:
            # 二番目以降
            lst[self._shared_channel_cell].append(self)
        self._sub_channel_no = len(lst[self._shared_channel_cell]) - 1

        first_region = lst[self._shared_channel_cell][0]._region
        if self._region != first_region:
            # 初出とリージョン不一致 (初出は、自分自身とチェックされる。無駄だが小さいので放置)
            self.cdl_error(
                "SharedRPCPlugin: preferred region mismatch current: "
                f"{to_s(self._region.get_name())} previous: {to_s(first_region.get_name())}"
            )

        if self._signature.need_PPAllocator() and self._pp_allocator_size is None:
            self.cdl_error("PPAllocatorSize must be speicified for oneway [in] array")

    def gen_plugin_decl_code(self, file: Any) -> None:
        from tecsgen.context import get_context
        from tecsgen.core.plugin import CFile

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        # （登録するだけで、生成済みでも以下を出力し直す。Ruby 版どおり）
        generated = ThroughPlugin._generated_celltype
        for name in (self._shared_channel_ct_name, self._ct_name):
            if generated.get(name) is None:
                generated[name] = [self]
            else:
                generated[name].append(self)

        self.gen_marshaler_celltype()
        # 同じ内容を二度書く可能性あり (AppFile は不可)

        if self._signature.need_PPAllocator():
            alloc_call_port = "  call sPPAllocator cPPAllocator;\n"
            alloc_call_port_join = "  cPPAllocator => composite.cPPAllocator;\n"
        else:
            alloc_call_port = ""
            alloc_call_port_join = ""

        sig_path = to_s(self._signature.get_namespace_path())
        sig_gname = to_s(self._signature.get_global_name())
        f = CFile.open(self._rpc_channel_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            f'import( "{self._marshaler_celltype_file_name}" );\n\n'
            f"composite {to_s(self._rpc_channel_celltype_name)} {{\n"
            "  /* Interface */\n"
            f"  call  {sig_path} {to_s(self._call_port_name)};\n"
            f"  entry {sig_path} eThroughEntry;\n"
            "  call  sTDR       cTDR;\n"
            "  call  sEventflag cEventflag;\n"
            "  entry sUnmarshalerMain  eUnmarshalAndCallFunction;\n"
            f"{alloc_call_port}\n"
            "  [optional]\n"
            "    call sSemaphore cLockChannel;\n\n"
            "  /* Implementation */\n"
            f"  cell {self._marshaler_celltype_name} {sig_gname}_marshaler{{\n"
            "    cTDR         => composite.cTDR;\n"
            "    cEventflag   => composite.cEventflag;\n"
            "    cLockChannel => composite.cLockChannel;\n"
            "  };\n"
            f"  cell {self._unmarshaler_celltype_name} {sig_gname}_unmarshaler{{\n"
            "    cTDR         => composite.cTDR;\n"
            "    cEventflag   => composite.cEventflag;\n"
            f"    cServerCall  => composite.{to_s(self._call_port_name)};\n"
            f"{alloc_call_port_join}  }};\n"
            f"  composite.eThroughEntry => {sig_gname}_marshaler.eClientEntry;\n"
            f"  composite.eUnmarshalAndCallFunction => {sig_gname}_unmarshaler.eUnmarshalAndCallFunction;\n"
            "};\n"
        )
        # mikan stackSize option & 最新 tecs_package 対応
        f.close()

        f = CFile.open(
            f"{get_context().gen}/{to_s(self._shared_channel_ct_name)}.cdl", "w"
        )
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            "[active]\n"
            f"composite {to_s(self._shared_channel_ct_name)} {{\n"
            "  /* Interface */\n"
            "  entry  sSemaphore eSemaphore[];\n"
            "  call   sUnmarshalerMain  cUnmarshalAndCallFunction[];\n\n"
            "  entry  sDataqueue eDataqueue;\n"
            "  entry  sTDR       eTDR;\n"
            "  entry  sEventflag eEventflag;\n\n"
            "  attr {\n"
            "    PRI    priority;\n"
            "  };\n\n"
            "  /* Implementation */\n"
            f"  cell {to_s(self._channel_celltype)} Channel{{\n"
            "  };\n"
            '  cell tSemaphore Semaphore {initialCount = 1; attribute = C_EXP("TA_NULL");};\n'
            "  cell tRPCSharedTaskMain RPCSharedTaskMain {\n"
            "    cUnmarshalAndCallFunction => composite.cUnmarshalAndCallFunction;\n"
            "    cServerSideTDR            = Channel.eTDR;\n"
            "  };\n"
            "  cell tRPCSharedChannelMan RPCChannelMan {\n"
            "    cSemaphore                = Semaphore.eSemaphore;\n"
            "    cClientSideTDR            = Channel.eTDR;\n"
            "  };\n"
            "  cell tTask RPCSharedTask {\n"
            "    cTaskBody = RPCSharedTaskMain.eMain;\n"
            '    attribute = C_EXP("TA_ACT");\n'
            "    stackSize = 4096;\n"
            "    priority = composite.priority;\n"
            "  };\n"
            "  composite.eTDR           => Channel.eTDR;\n"
            "  composite.eEventflag     => Channel.eEventflag;\n"
            "  composite.eSemaphore     => RPCChannelMan.eSemaphore;\n"
            "  composite.eDataqueue     => Channel.eDataqueue;\n"
            "};\n"
        )
        f.close()

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        from tecsgen.context import get_context
        from tecsgen.core.componentobj.namespace import Namespace

        self.gen_plugin_decl_code(file)

        file.print(
            f'import( "{self._rpc_channel_celltype_file_name}" );\n'
            f'import( "{get_context().gen}/{to_s(self._shared_channel_ct_name)}.cdl" );\n'
        )

        nest = self._region.gen_region_str_pre(file)
        indent_str = "  " * nest
        if self._next_cell_port_subscript is not None:
            subscript = "[" + to_s(self._next_cell_port_subscript) + "]"
        else:
            subscript = ""

        # セルを探す
        cell = Namespace.find(self._next_cell.get_namespace_path())

        # PPAllocator が必要か?
        if self._signature.need_PPAllocator():
            if self._sub_channel_no == 0:
                file.print(
                    f"{indent_str}cell tPPAllocator PPAllocator_{to_s(self._shared_channel_cell)}{{\n"
                    f"{indent_str}  heapSize = {to_s(self._pp_allocator_size)};\n"
                    f"{indent_str}}};\n"
                )
            ppallocator_join = f"{indent_str}  cPPAllocator = PPAllocator_{to_s(self._shared_channel_cell)}.ePPAllocator;\n"
        else:
            ppallocator_join = ""

        # 共有される通信チャンネルの生成のプロトタイプ宣言
        file.print(
            f"{indent_str}cell {to_s(self._shared_channel_ct_name)} {to_s(self._shared_channel_cell)};\n"
        )

        # ここから各結合ごとのセルを生成

        # アロケータの指定があるか？
        if len(cell.get_allocator_list()) > 0:
            file.print(f"{indent_str}[allocator(")

            delim = ""
            for _type, eport, subsc, func, buf, alloc in cell.get_allocator_list():
                file.print(delim)
                delim = f",\n{indent_str}           "  # 最終行には出さない

                # Ruby 版は単一引用符の '[#{subsc}]' なので、式展開されずそのまま出る
                subsc_str = (
                    "[#{subsc}]" if subsc is not None and subsc is not False else ""
                )

                eport = "eThroughEntry"  # RPCの受け口名に変更
                file.print(
                    f"{eport}{subsc_str}.{to_s(func)}.{to_s(buf)} = {to_s(alloc)}"
                )

            file.puts(")]")

        # セル本体の生成
        sc = to_s(self._shared_channel_cell)
        file.print(
            f"{indent_str}cell {to_s(self._rpc_channel_celltype_name)} {to_s(self._cell_name)} {{\n"
            f"{indent_str}  {to_s(self._call_port_name)} = {to_s(self._next_cell.get_name())}."
            f"{to_s(self._next_cell_port_name)}{subscript};\n"
            f"{indent_str}  cTDR         = {sc}.eTDR;\n"
            f"{indent_str}  cEventflag   = {sc}.eEventflag;\n"
            f"{indent_str}  cLockChannel =  {sc}.eSemaphore[{self._sub_channel_no}];\n"
            f"{ppallocator_join}{indent_str}}};\n"
        )
        self._region.gen_region_str_post(file)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """プラグインの後ろのコードを生成する。"""
        file.print(f"/* '{class_name(cls)}' post code */\n")
        for plugin_obj in SharedRPCPlugin._shared_channel_list.values():
            plugin_obj[0].gen_post_code_channel(file, plugin_obj)

    def gen_post_code_channel(self, file: Any, plugin_obj: list[Any]) -> None:
        """後ろのコードを生成する（Ruby のインスタンスメソッド gen_post_code）。

        plugin_obj[0] が代表して出力する（インスタンス変数にアクセスしたいため）。
        """
        chan_name = to_s(self._shared_channel_cell)

        nest = self._region.gen_region_str_pre(file)
        indent_str = "  " * nest

        # 共有されている通信チャンネルの生成
        # 各プラグインインスタンスでは @shared_channel_ct_name として記憶している
        file.print(
            f"{indent_str}cell tSharedRPCPlugin_{to_s(self._channel_celltype)} {chan_name} {{\n"
        )
        for _po in plugin_obj:
            # Ruby 版どおり、各インスタンスではなく代表（self）の @cell_name を出す
            file.print(
                f"{indent_str}    cUnmarshalAndCallFunction[] = {to_s(self._cell_name)}.eUnmarshalAndCallFunction;\n"
            )
        file.print(
            f"{indent_str}    priority = {to_s(self._task_priority)};\n{indent_str}}};\n"
        )
        self._region.gen_region_str_post(file)
