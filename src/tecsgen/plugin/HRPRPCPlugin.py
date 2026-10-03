"""HRPRPCPlugin.rb の移植（内部仕様9章）。HRP の別ユーザドメイン間の結合に HRPPlugin が挿入する RPC。

スループラグイン (through)。OpaqueMarshalerPlugin を使用してマーシャラセルタイプを生成し、
マーシャラ、TDR、チャンネル、メッセージバッファを生成する。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.lib.GenOpaqueMarshaler import GenOpaqueMarshaler
from tecsgen.plugin.lib.GenParamCopy import GenParamCopy
from tecsgen.plugin.ThroughPlugin import ThroughPlugin
from tecsgen.ruby_compat import Symbol, Y, sym, to_s, truthy


class HRPRPCPlugin(GenParamCopy, GenOpaqueMarshaler, ThroughPlugin):
    # RPCPlugin 専用のオプション（GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC の複製 + 追加）
    HRP_RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

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
        self._b_noClientSemaphore = False
        self._semaphoreCelltype = "tSemaphore"
        self.initialize_opaque_marshaler()

        # オプション：GenOpaqueMarshaler 参照
        self._plugin_arg_check_proc_tab = HRPRPCPlugin.HRP_RPC_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        # Ruby 版の @channelCelltype は、どこでも設定されず nil（空文字列になる）
        channel_celltype = getattr(self, "_channelCelltype", None)
        self._rpc_channel_celltype_name = (
            f"tRPCPlugin_{to_s(self._TDRCelltype)}_{to_s(channel_celltype)}_"
            f"{to_s(self._signature.get_name())}"
        )
        self._rpc_channel_celltype_file_name = (
            f"{get_context().gen}/{self._rpc_channel_celltype_name}.cdl"
        )

        if self._signature.get_context() == "non-task":
            self.cdl_error(
                "HRP9999 RPC cannot be applied to non-task context signature '$1'",
                self._signature.get_name(),
            )
        elif self._signature.get_context() == "any":
            self.cdl_info(
                "HRP9999 RPC is applied to any context signature '$1'",
                self._signature.get_name(),
            )

        if self._signature.need_PPAllocator(True):
            if self._PPAllocatorSize is None:
                self.cdl_error(
                    "HRP9999 PPAllocatorSize must be speicified for pointer argments"
                )
        elif self._PPAllocatorSize:
            self.cdl_warning(
                "HRP9999 PPAllocatorSize speicified in spite of PPAllocator unnecessary"
            )
            self._PPAllocatorSize = None

    def gen_plugin_decl_code(self, file: Any) -> None:
        """plugin の宣言コード (celltype の定義) 生成。"""
        from tecsgen.core.plugin import CFile

        ct_name = (
            f"{to_s(self._ct_name)}_{to_s(getattr(self, '_channelCelltype', None))}"
        )

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if ThroughPlugin._generated_celltype.get(ct_name) is None:
            ThroughPlugin._generated_celltype[ct_name] = [self]
        else:
            ThroughPlugin._generated_celltype[ct_name].append(self)
            return

        f = CFile.open(self._rpc_channel_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        sig_path = to_s(self._signature.get_namespace_path())
        gname = to_s(self._signature.get_global_name())
        f.print(
            "/* HRPRPCPlugin:000 */\n"
            "import( <rpc.cdl> );\n"
            "import( <tMessageBufferCEP.cdl> );\n"
            f'generate( OpaqueMarshalerPlugin, {sig_path}, "" );\n'
            "\n"
            f"composite tOpaqueMarshaler_{gname}_through {{\n"
            f"  entry {sig_path} eThroughEntry;\n"
            "  call sTDR       cTDR;\n"
            "  [optional]\n"
            "    call sSemaphore cLockChannel;\n"
            "  [optional]\n"
            "    call sRPCErrorHandler cErrorHandler;\n"
            "\n"
            f"  cell tOpaqueMarshaler_{gname} Marshaler{{\n"
            "    cTDR          => composite.cTDR;\n"
            "    cLockChannel  => composite.cLockChannel;\n"
            "    cErrorHandler => composite.cErrorHandler;\n"
            "  };\n"
            "  composite.eThroughEntry => Marshaler.eClientEntry;\n"
            "};\n"
            "\n"
        )
        f.close()

    def gen_through_cell_code(self, file: Any) -> None:
        """through cell コードを生成。"""
        self.gen_plugin_decl_code(file)

        file.print(
            "/* HRPRPCPlugin:000\n"
            f" * caller_cell:{to_s(self._caller_cell.get_namespace_path())}\n"
            f" * next_cell:{to_s(self._next_cell.get_namespace_path())}\n"
            " */ \n"
            f"import( <{self._rpc_channel_celltype_file_name}> );\n"
        )

        # MessageBuffer チャンネルの生成 (OutOfDomain に生成)
        # アクセス許可ベクタの作成 (呼び元、呼び先のドメインからアクセス可能)
        start_root = self._start_region.get_domain_root()
        kind = start_root.get_domain_type().get_kind()
        tacp_str = ""
        if kind == Y.kernel:
            tacp_str = '"TACP_KERNEL'
        elif kind == Y.user:
            tacp_str = f'"TACP({to_s(start_root.get_name())})'
        elif kind == Y.OutOfDomain:
            tacp_str = '"TACP_SHARED'
        end_root = self._end_region.get_domain_root()
        kind = end_root.get_domain_type().get_kind()
        if kind == Y.kernel:
            tacp_str += '|TACP_KERNEL"'
        elif kind == Y.user:
            tacp_str += f'|TACP({to_s(end_root.get_name())})"'
        elif kind == Y.OutOfDomain:
            tacp_str += '|TACP_SHARED"'

        node_root = self._end_region.get_node_root()
        nest = node_root.gen_region_str_pre(file)
        nest = self.print_class_region_str_pre(node_root, file, nest)
        nest_str = "    " * nest

        client_cell = to_s(self._clientChannelCell)
        server_cell = to_s(self._serverChannelCell)

        # MessageBuffer Client->Server
        file.print(
            f"{nest_str}/* HRPRPCPlugin001 */\n"
            f"{nest_str}//  MessageBuffer client=>server\n"
            f"{nest_str}cell tMessageBuffer {client_cell}Body0{{\n"
            f"{nest_str}    maxMessageSize = 64;      /* This value must be same as MessageBufferCEP's buffer size */\n"
            f"{nest_str}    bufferSize     = 128;\n"
            f"{nest_str}    accessPattern1 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern2 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern3 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern4 = C_EXP( {tacp_str} );\n"
            f"{nest_str}}};\n"
        )
        # MessageBuffer Server->Client
        file.print(
            "\n"
            f"{nest_str}/* HRPRPCPlugin002 */\n"
            f"{nest_str}//  MessageBuffer server=>client\n"
            f"{nest_str}cell tMessageBuffer {client_cell}Body1{{\n"
            f"{nest_str}    maxMessageSize = 64;      /* This value must be same as MessageBufferCEP's buffer size */\n"
            f"{nest_str}    bufferSize     = 128;\n"
            f"{nest_str}    accessPattern1 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern2 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern3 = C_EXP( {tacp_str} );\n"
            f"{nest_str}    accessPattern4 = C_EXP( {tacp_str} );\n"
            f"{nest_str}}};\n"
        )
        nest -= 1
        self.print_class_region_str_post(node_root, file, nest)
        node_root.gen_region_str_post(file)

        ##### クライアント側のセルの生成 #####
        nest = self._start_region.gen_region_str_pre(file)
        nest = self.print_class_region_str_pre(self._start_region, file, nest)
        nest_str = "    " * nest

        # セマフォの生成
        if self._b_noClientSemaphore is False:
            file.print(
                "\n"
                "/* HRPRPCPlugin003 */\n"
                f'{nest_str}//  Semaphore for Multi-task use ("specify noClientSemaphore" option to delete this)\n'
                f"{nest_str}cell {to_s(self._semaphoreCelltype)} {server_cell}_Semaphore{{\n"
                f"{nest_str}    initialCount = 1;\n"
                f"{nest_str}}};\n"
            )

        # クライアント側チャンネル (tMessageBufferCEP)の生成
        # チャンネルは必ずリージョン下にあるので、 '::' でつなぐ (でなければ、ルートリージョンにないかチェックが必要）

        # node_root が OutOfDomain でない場合、恐らく問題がある ***
        class_path = self.get_default_class_region_path(
            self._end_region.get_node_root()
        )
        file.print(
            "/* HRPRPCPlugin004 */\n"
            f"{nest_str}//  Client Side Channel\n"
            f"{nest_str}cell tMessageBufferCEP {client_cell}_CEP{{\n"
            f"{nest_str}    cMessageBuffer0 = {class_path}{client_cell}Body0.eMessageBuffer;\n"
            f"{nest_str}    cMessageBuffer1 = {class_path}{client_cell}Body1.eMessageBuffer;\n"
            f"{nest_str}}};\n"
            "\n"
            f"{nest_str}//  Client Side TDR\n"
            f"{nest_str}cell tTDR {client_cell}_TDR{{\n"
            f"{nest_str}    cChannel = {client_cell}_CEP.eChannel;\n"
            f"{nest_str}}};\n"
            "\n"
            f"{nest_str}  //  Marshaler\n"
        )

        # セマフォの結合文
        if self._b_noClientSemaphore is False:
            semaphore = (
                f"{nest_str}    cLockChannel = {server_cell}_Semaphore.eSemaphore;\n"
            )
        else:
            semaphore = ""

        ### クライアント側チャンネル (マーシャラ+TDR)の生成 ###
        cell = self._next_cell
        # アロケータの指定があるか？
        if len(cell.get_allocator_list()) > 0:
            file.print(nest_str)
            file.print("[allocator(")

            delim = ""
            for _type, eport, subsc, func, buf, alloc in cell.get_allocator_list():
                alloc_str = to_s(alloc)
                subst = self._substituteAllocator.get(sym(alloc_str))
                if subst:
                    alloc_str = f"{subst[2]}.{subst[3]}"

                file.print(delim)
                delim = ",\n"  # 最終行には出さない

                # Ruby 版は単一引用符なので、"#{subsc}" がそのまま出る
                subsc_str = "[#{subsc}]" if subsc else ""

                eport = "eThroughEntry"  # RPCの受け口名に変更
                file.print(nest_str)
                file.print(f"{eport}{subsc_str}.{to_s(func)}.{to_s(buf)} = {alloc_str}")

            file.puts(")]")

        if self._clientErrorHandler:
            client_error_handler_str = (
                f"{nest_str}    cErrorHandler = {to_s(self._clientErrorHandler)};\n"
            )
        else:
            client_error_handler_str = ""

        gname = to_s(self._signature.get_global_name())
        file.print(
            "/* HRPRPCPlugin005 */\n"
            f"{nest_str}cell tOpaqueMarshaler_{gname}_through {to_s(self._cell_name)} {{\n"
            f"{nest_str}    cTDR = {client_cell}_TDR.eTDR;\n"
            f"{client_error_handler_str}{semaphore}{nest_str}}};\n"
        )

        ### END: クライアント側チャンネル (マーシャラ+TDR)の生成 ###
        nest -= 1
        self.print_class_region_str_post(self._start_region, file, nest)
        self._start_region.gen_region_str_post(file)
        file.print("\n\n")

        ##### サーバー側のセルの生成 #####
        nest = self._end_region.gen_region_str_pre(file)
        nest = self.print_class_region_str_pre(self._end_region, file, nest)
        nest_str = "    " * nest

        if self._serverErrorHandler:
            server_error_handler_str = (
                f"{nest_str}    cErrorHandler = {to_s(self._serverErrorHandler)};\n"
            )
        else:
            server_error_handler_str = ""

        if self._b_genOpener:
            opener = f"{nest_str}    cOpener       = {server_cell}.eOpener;\n"
        else:
            opener = ""

        # サーバー側チャンネル (tMessageBufferCEP)
        if self._PPAllocatorSize:
            alloc_cell = (
                "\n"
                f"{nest_str}cell tPPAllocator {server_cell}_PPAllocator {{\n"
                f"{nest_str}    heapSize = {to_s(self._PPAllocatorSize)};\n"
                f"{nest_str}}};\n"
            )
            alloc_call_port_join = f"{nest_str}    cPPAllocator = {server_cell}_PPAllocator.ePPAllocator;\n"
        else:
            alloc_cell = ""
            alloc_call_port_join = ""

        file.print(
            "/* HRPRPCPlugin006 */\n"
            f"{nest_str}//  Server Side Channel\n"
            f"{nest_str}cell tMessageBufferCEP {server_cell}_CEP{{\n"
            f"{nest_str}    cMessageBuffer0 = {class_path}{client_cell}Body1.eMessageBuffer;\n"
            f"{nest_str}    cMessageBuffer1 = {class_path}{client_cell}Body0.eMessageBuffer;\n"
            f"{nest_str}}};\n"
        )

        # サーバー側TDR
        file.print(
            "\n"
            "/* HRPRPCPlugin007 */\n"
            f"{nest_str}//  Server Side TDR\n"
            f"{nest_str}cell tTDR {server_cell}_TDR{{\n"
            f"{nest_str}    cChannel = {server_cell}_CEP.eChannel;\n"
            f"{nest_str}}};\n"
            "\n"
        )

        if truthy(self._next_cell_port_subscript):
            subscript = "[" + to_s(self._next_cell_port_subscript) + "]"
        else:
            subscript = ""

        # サーバー側チャンネル (アンマーシャラ)
        file.print(
            f"/* HRPRPCPlugin008 */{alloc_cell}\n"
            f"{nest_str}//  Unmarshaler\n"
            f"{nest_str}cell tOpaqueUnmarshaler_{gname} {server_cell}_Unmarshaler {{\n"
            f"{nest_str}    cTDR        = {server_cell}_TDR.eTDR;\n"
            f"{nest_str}    cServerCall = {self._next_cell.get_namespace_path().get_path_str()}.{to_s(self._next_cell_port_name)}{subscript};\n"
            f"{alloc_call_port_join}{server_error_handler_str}{nest_str}}};\n"
        )

        # サーバー側タスクメイン
        file.print(
            "\n"
            "/* HRPRPCPlugin009 */\n"
            f"{nest_str}//  Unmarshaler Task Main\n"
            f"{nest_str}cell {to_s(self._taskMainCelltype)} {server_cell}_TaskMain {{\n"
            f"{nest_str}    cMain         = {server_cell}_Unmarshaler.eService;\n"
            f"{opener}{nest_str}}};\n"
        )

        # サーバー側タスク
        file.print(
            "\n"
            "/* HRPRPCPlugin010 */\n"
            f"{nest_str}//  Unmarshaler Task\n"
            f"{nest_str}cell {to_s(self._taskCelltype)} {server_cell}_Task {{\n"
            f"{nest_str}    cTaskBody = {server_cell}_TaskMain.eMain;\n"
            f"{nest_str}    priority  = {to_s(self._taskPriority)};\n"
            f"{nest_str}    stackSize = {to_s(self._stackSize)};\n"
            f'{nest_str}    attribute = C_EXP( "TA_ACT" );  /* mikan : marshaler task starts at beginning */\n'
            f"{nest_str}}};\n"
        )
        nest -= 1
        self.print_class_region_str_post(self._end_region, file, nest)
        self._end_region.gen_region_str_post(file)

    def get_default_class_and_region(self, region: Any) -> tuple[str, str]:
        """デフォルトのクラス名、クラスリージョン名を返す。

        デフォルトのクラス名は "CLS_PRC1"、デフォルトのクラスリージョン名は "__CLS_P1_GLOBAL"
        """
        class_type = region.get_class_root().get_class_type()
        if class_type is None:
            return "", ""
        return "CLS_PRC1", "__CLS_P1_GLOBAL"

    def get_default_class_region_path(self, region: Any) -> str:
        """OutofDomain なクラスへのパス。"""
        _class_name, class_region = self.get_default_class_and_region(region)
        if class_region != "":
            if region.is_root():
                return "::" + class_region + "::"
            return to_s(region.get_namespace_path()) + "::" + class_region + "::"
        return ""

    def print_class_region_str_pre(self, region: Any, file: Any, nest: int) -> int:
        """ファイルにクラスリージョンの CDL での定義を出力する。"""
        from tecsgen.context import dbg_print
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.ruby_compat import rb_print

        class_type = region.get_class_root().get_class_type()
        if class_type is None:
            return nest
        klass = class_type.get_option()
        dbg_print(
            f"HRPRPCPlugin#print_class_region_str_pre class_type={to_s(class_type.get_name())} class={to_s(klass)}\n"
        )
        rb_print(
            f"HRPRPCPlugin#print_class_region_str_pre class_type={to_s(class_type.get_name())} class={to_s(klass)}\n"
        )

        nest_str = "    " * nest
        if klass == Y.root:
            klass, region_name = self.get_default_class_and_region(region)
        else:
            return nest
        region_name = to_s(region_name)
        if region.is_root():
            nsp = "::" + region_name
        else:
            nsp = to_s(region.get_namespace_path()) + "::" + region_name
        file.print(f"{nest_str}/* HRPRPCPlugin011 */\n")
        region_namespacepath = NamespacePath.analyze(nsp)
        first = False
        if Namespace.find(region_namespacepath) is None:
            file.print(f'{nest_str}[class({to_s(class_type.get_name())},"{klass}")]\n')
            first = True
        dbg_print(
            f"HRPRPCPlugin: In class class_type={type(class_type).__name__} class={klass} "
            f"region={to_s(region.get_class_root().get_name())} nsp={nsp} first={first}\n"
        )
        file.print(f"{nest_str}region {region_name}{{\n")
        return nest + 1

    def print_class_region_str_post(self, region: Any, file: Any, nest: int) -> None:
        class_type = region.get_class_root().get_class_type()
        if class_type is None:
            return
        klass = class_type.get_option()
        if klass != Y.root:
            return
        nest_str = "    " * nest
        file.print(f"{nest_str}}};\n")

    def set_noClientSemaphore(self, rhs: Any) -> None:
        """プラグイン引数 noClientSemaphore のチェック。"""
        rhs_sym = sym(rhs)
        if rhs_sym == Symbol("true"):
            self._b_noClientSemaphore = True
        elif rhs_sym == Symbol("false"):
            self._b_noClientSemaphore = False
        else:
            self.cdl_error("RPCPlugin: specify true or false for noClientSemaphore")

    def set_semaphoreCelltype(self, rhs: Any) -> None:
        """プラグイン引数 semaphoreCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._semaphoreCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._semaphoreCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(
                "RPCPlugin: semaphoreCelltype '$1' not celltype or not defined", rhs
            )

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._start_region.get_namespace_path()
        _class_path, class_region = self.get_default_class_and_region(
            self._start_region
        )
        if class_region != "":
            nsp = nsp.append(sym(class_region))
        return nsp.append(self._cell_name)


HRPRPCPlugin.HRP_RPC_PLUGIN_ARG_PROC = {
    **GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC,
    "noClientSemaphore": lambda obj, rhs: obj.set_noClientSemaphore(rhs),
    "semaphoreCelltype": lambda obj, rhs: obj.set_semaphoreCelltype(rhs),
}
