"""HRP2RPCPlugin.rb の移植（内部仕様9章）。RPC を用いたドメイン間通信の through プラグイン。

HRP2 ドメインプラグインによって挿入される。Transparent RPC のチャンネルを、HRP2 のメッセージバッファ
（`GenHRP2Marshaler`）で生成する。

mikan through plugin: namespace が考慮されていない

以下を仮定（制限事項）:
  呼び元、呼び先のエンディアン、char, short, int_t, long_t, intptr_t のサイズが同じ
  有符号、無符号でサイズが同じ
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import get_context
from tecsgen.core.plugin import CFile
from tecsgen.plugin.lib.GenHRP2Marshaler import GenHRP2Marshaler
from tecsgen.plugin.lib.GenTransparentMarshaler import GenTransparentMarshaler
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import Symbol, sym, to_s, truthy


class HRP2RPCPlugin(GenHRP2Marshaler, ThroughPlugin):
    # RPCPlugin 専用のオプション（GenTransparentMarshaler.RPC_PLUGIN_ARG_PROC の複製 + 追加）
    TRANSPARENT_RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

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
        self._b_no_client_semaphore = False
        self._semaphore_celltype = "tSemaphore"
        self.initialize_transparent_marshaler(cell_name)

        # オプション：GenTransparentMarshaler 参照
        self._plugin_arg_check_proc_tab = HRP2RPCPlugin.TRANSPARENT_RPC_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        self._rpc_channel_celltype_name = (
            f"tRPCPlugin_{to_s(self._tdr_celltype)}_{to_s(self._channel_celltype)}_"
            f"{to_s(self._signature.get_name())}"
        )
        self._rpc_channel_celltype_file_name = (
            f"{get_context().gen}/{self._rpc_channel_celltype_name}.cdl"
        )

        if self._signature.need_PPAllocator() and self._pp_allocator_size is None:
            self.cdl_error("PPAllocatorSize must be speicified for oneway [in] array")

    def gen_plugin_decl_code(self, file: Any) -> None:
        """plugin の宣言コード (celltype の定義) 生成。"""
        ct_name = f"{to_s(self._ct_name)}_{to_s(self._channel_celltype)}"

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if ThroughPlugin._generated_celltype.get(ct_name) is None:
            ThroughPlugin._generated_celltype[ct_name] = [self]
        else:
            ThroughPlugin._generated_celltype[ct_name].append(self)
            return

        self.gen_marshaler_celltype()

        if truthy(self._pp_allocator_size):
            alloc_cell = (
                "  cell tPPAllocator PPAllocator {\n"
                f"    heapSize = {to_s(self._pp_allocator_size)};\n"
                "  };\n"
            )
            alloc_call_port_join = "    cPPAllocator = PPAllocator.ePPAllocator;\n"
        else:
            alloc_cell = ""
            alloc_call_port_join = ""

        if self._b_no_client_semaphore is False:
            semaphore1 = (
                '  // Semaphore for Multi-task use ("specify noClientSemaphore" option to delete this)\n'
                f"  cell {to_s(self._semaphore_celltype)} Semaphore {{\n"
                "    count = 1;\n"
                '    attribute = C_EXP( "TA_NULL" );\n'
                "  };\n"
            )
            semaphore2 = "    cLockChannel = Semaphore.eSemaphore;\n"
        else:
            semaphore1 = ""
            semaphore2 = ""

        sig = to_s(self._signature.get_name())
        name = self._rpc_channel_celltype_name
        f = CFile.open(self._rpc_channel_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        f.print(
            f'import( "{self._marshaler_celltype_file_name}" );\n'
            "\n"
            f"composite {name}Client {{\n"
            "  /* Interface */\n"
            f"  entry {sig} eThroughEntry;\n"
            "  //call sTDR       cTDR;\n"
            "  call sEventflag cEventflag;\n"
            "  call sSemaphore cSemaphore;\n"
            "  call sMessageBuffer cMessageBuffer;\n"
            "\n"
            "  /* Implementation */\n"
            f"{semaphore1}\n"
            f"  cell {self._marshaler_celltype_name} {sig}_marshaler{{\n"
            "    //cTDR         => composite.cTDR;\n"
            "    cEventflag   => composite.cEventflag;\n"
            "    cSemaphore   => composite.cSemaphore;\n"
            "    cMessageBuffer => composite.cMessageBuffer;\n"
            f"{semaphore2}  }};\n"
            f"  composite.eThroughEntry => {sig}_marshaler.eClientEntry;\n"
            "};\n"
            "\n"
            "[active]\n"
            f"composite {name}Server {{\n"
            "  /* Interface */\n"
            "  attr {\n"
            "    PRI taskPriority;\n"
            "  };\n"
            f"  call {sig} {to_s(self._call_port_name)};\n"
            "  //call sTDR       cTDR;\n"
            "  call sEventflag cEventflag;\n"
            "  call sSemaphore cSemaphore;\n"
            "  call sMessageBuffer cMessageBuffer;\n"
            "\n"
            "  /* Implementation */\n"
            f"{alloc_cell}  cell {self._unmarshaler_celltype_name} {sig}_unmarshaler{{\n"
            "    //cTDR        => composite.cTDR;\n"
            "    cEventflag  => composite.cEventflag;\n"
            "    cSemaphore  => composite.cSemaphore;\n"
            "    cMessageBuffer => composite.cMessageBuffer;\n"
            f"    cServerCall => composite.{to_s(self._call_port_name)};\n"
            f"{alloc_call_port_join}  }};\n"
            "  cell tRPCDedicatedTaskMain RPCTaskMain{\n"
            f"    cMain = {sig}_unmarshaler.eUnmarshalAndCallFunction;\n"
            "  };\n"
            "  cell tTask Task {\n"
            "    cBody     = RPCTaskMain.eMain;\n"
            "    priority  = taskPriority;\n"
            '    taskAttribute = C_EXP( "TA_ACT" );  /* mikan : marshaler starts at the beginning */\n'
            "    //stackSize     = 4096;\n"
            "    userStackSize     = 4096;\n"
            "  };\n"
            "};\n"
        )
        # mikan stackSize option & 最新 tecs_package 対応
        f.close()

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        from tecsgen.core.componentobj.namespace import Namespace

        self.gen_plugin_decl_code(file)

        # セルを探す
        cell = Namespace.find(self._next_cell.get_namespace_path())

        file.print(f'import( "{self._rpc_channel_celltype_file_name}" );\n')

        indent_str = ""
        chan_cell = to_s(self._channel_cell_name)
        file.print(
            f"{indent_str}// one way channel cell\n"
            f"{indent_str}cell {to_s(self._channel_celltype)} {chan_cell} {{\n"
            f"{indent_str}}};\n"
            "\n"
            f"{indent_str}// RPC channel cell\n"
        )

        nest = self._start_region.gen_region_str_pre(file)
        indent_str = "  " * nest

        # #473 が解決された場合、composite リレーアロケータに変更すべき
        # アロケータの指定があるか？
        if len(cell.get_allocator_list()) > 0:
            file.print(f"{indent_str}[allocator(")

            delim = ""
            for _type, eport, subsc, func, buf, alloc in cell.get_allocator_list():
                file.print(delim)
                delim = f",\n{indent_str}           "  # 最終行には出さない

                # Ruby 版は単一引用符なので、"#{subsc}" がそのまま出る
                subsc_str = "[#{subsc}]" if subsc else ""

                eport = "eThroughEntry"  # RPCの受け口名に変更
                file.print(
                    f"{eport}{subsc_str}.{to_s(func)}.{to_s(buf)} = {to_s(alloc)}"
                )

            file.puts(")]")

        name = self._rpc_channel_celltype_name
        file.print(
            f"{indent_str}cell {name}Client {to_s(self._cell_name)} {{\n"
            f"{indent_str}  //cTDR         = {chan_cell}.eTDR;\n"
            f"{indent_str}  cEventflag   = {chan_cell}.eEventflag;\n"
            f"{indent_str}  cSemaphore   = {chan_cell}.eSemaphore;\n"
            f"{indent_str}  cMessageBuffer   = {chan_cell}.eMessageBuffer;\n"
            f"{indent_str}}};\n"
        )

        self._start_region.gen_region_str_post(file)

        nest = self._end_region.gen_region_str_pre(file)
        indent_str = "  " * nest
        if truthy(self._next_cell_port_subscript):
            subscript = "[" + to_s(self._next_cell_port_subscript) + "]"
        else:
            subscript = ""

        call_port = to_s(self._call_port_name)
        file.print(
            f"{indent_str}cell {name}Server {to_s(self._cell_name)}Body {{\n"
            f"{indent_str}    {call_port} = {self._next_cell.get_namespace_path().get_path_str()}.{to_s(self._next_cell_port_name)}{subscript};\n"
            f"//{indent_str}    {call_port} = {to_s(self._next_cell.get_name())}.{to_s(self._next_cell_port_name)};\n"
            f"{indent_str}  //cTDR         = {chan_cell}.eTDR;\n"
            f"{indent_str}  cEventflag   = {chan_cell}.eEventflag;\n"
            f"{indent_str}  cSemaphore   = {chan_cell}.eSemaphore;\n"
            f"{indent_str}  cMessageBuffer  = {chan_cell}.eMessageBuffer;\n"
            f"{indent_str}  taskPriority = {to_s(self._task_priority)};\n"
            f"{indent_str}}};\n"
        )

        self._end_region.gen_region_str_post(file)

    def set_noClientSemaphore(self, rhs: Any) -> None:
        """プラグイン引数 noClientSemaphore のチェック。"""
        rhs_sym = sym(rhs)
        if rhs_sym == Symbol("true"):
            self._b_no_client_semaphore = True
        elif rhs_sym == Symbol("false"):
            self._b_no_client_semaphore = False
        else:
            self.cdl_error("RPCPlugin: specify true or false for noClientSemaphore")

    def set_semaphoreCelltype(self, rhs: Any) -> None:
        """プラグイン引数 semaphoreCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._semaphore_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._semaphore_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(
                "RPCPlugin: semaphoreCelltype '$1' not celltype or not defined", rhs
            )

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._start_region.get_namespace_path()
        return nsp.append(self._cell_name)


HRP2RPCPlugin.TRANSPARENT_RPC_PLUGIN_ARG_PROC = {
    **GenTransparentMarshaler.RPC_PLUGIN_ARG_PROC,
    "noClientSemaphore": lambda obj, rhs: obj.set_noClientSemaphore(rhs),
    "semaphoreCelltype": lambda obj, rhs: obj.set_semaphoreCelltype(rhs),
}
