"""GenOpaqueMarshaler.rb の移植。`OpaqueRPCPlugin`・`SharedOpaqueRPCPlugin` 共通の要素を集めたモジュール。

`opaqueRPC`・`opaqueMarshaler`・`sharedOpaqueRPC` オラクルケースは実際に成功し `gen/` に実コードが
生成されるため（`GenTransparentMarshaler` とは異なり）コード生成メソッドもほぼ全量移植している。
`print_param`（単数）は `GenParamCopy` に既に移植済みで、そちらを呼ぶ。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.core.cdl_types import PtrType
from tecsgen.ruby_compat import Symbol, Y, sym, to_s, truthy, utf8_literal

# 型検査のときだけ Node の子として扱う（mixin から cdl_error を呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.syntaxobj.node import Node

    class _Base(Node):
        pass
else:
    _Base = object


class GenOpaqueMarshaler(_Base):
    # プラグイン引数名と処理（サブクラスが複製して追加する。OpaqueRPCPlugin.py 参照）
    RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    ##### プラグイン引数チェック関数 #####

    def set_taskPriority(self, rhs: Any) -> None:
        """プラグイン引数 taskPriority のチェック。"""
        self._taskPriority = rhs

    def set_serverChannelCelltype(self, rhs: Any) -> None:
        """プラグイン引数 serverChannelCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._serverChannelCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._serverChannelCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: serverChannelCelltype '$1' not celltype or not found",
                rhs,
            )

    def set_clientChannelCelltype(self, rhs: Any) -> None:
        """プラグイン引数 clientChannelCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._clientChannelCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._clientChannelCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: clientChannelCelltype '$1' not celltype or not found",
                rhs,
            )

    def set_serverChannelCell(self, rhs: Any) -> None:
        """プラグイン引数 serverChannelCell のチェック。"""
        import re

        self._serverChannelCell = sym(rhs)
        if not re.match(r"\A[a-zA-Z_]\w*", to_s(rhs)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: serverChannelCell '$1' unsuitable for identifier", rhs
            )

    def set_clientChannelCell(self, rhs: Any) -> None:
        """プラグイン引数 clientChannelCell のチェック。"""
        import re

        self._clientChannelCell = sym(rhs)
        if not re.match(r"\A[a-zA-Z_]\w*", to_s(rhs)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: clientChannelCell '$1' unsuitable for identifier", rhs
            )

    def set_serverChannelInitializer(self, rhs: Any) -> None:
        """プラグイン引数 serverChannelInitializer のチェック。"""
        self._serverChannelInitializer = sym(self.subst_name(rhs))  # type: ignore[attr-defined]

    def set_clientChannelInitializer(self, rhs: Any) -> None:
        """プラグイン引数 clientChannelInitializer のチェック。"""
        self._clientChannelInitializer = sym(self.subst_name(rhs))  # type: ignore[attr-defined]

    def set_taskCelltype(self, rhs: Any) -> None:
        """プラグイン引数 taskCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._taskCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._taskCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: taskCelltype '$1' not celltype or not found", rhs
            )

    def set_stackSize(self, rhs: Any) -> None:
        """プラグイン引数 stackSize のチェック。"""
        self._stackSize = rhs

    def set_PPAllocatorSize(self, rhs: Any) -> None:
        """プラグイン引数 PPAllocatorSize のチェック。"""
        self._PPAllocatorSize = rhs

    def set_TDRCelltype(self, rhs: Any) -> None:
        """プラグイン引数 TDRCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._TDRCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._TDRCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: TDRCelltype '$1' not celltype or not found", rhs
            )

    def set_substituteAllocator(self, rhs: Any) -> None:
        """プラグイン引数 substituteAllocator のチェック。

        ``substituteAllocator(Alloc.eAlloc=>Subst.eAlloc,Alloc2.eAlloc=>Subst2.eAlloc)`` の
        形式であることをチェックする。右辺のセルは前方参照のためここではチェックしない
        （Ruby 版もコメントアウトされている）。
        """
        import re

        ident_rexpr = re.compile(r"\A(\w[\w\d]*)")

        def optparse(
            state: list[str], regexp: re.Pattern[str], expected: str
        ) -> str | None:
            state[0] = state[0].lstrip()
            m = regexp.match(state[0])
            if not m:
                self.cdl_error(  # type: ignore[attr-defined]
                    f"syntax error in substituteAllocator option near '{state[0]}', expected '{expected}'"
                )
                return None
            token = m.group(0)
            state[0] = state[0][m.end() :]
            return token

        opt = [to_s(rhs)]

        while True:
            lhs_alloc_cell = optparse(opt, ident_rexpr, "allocator cell name")
            if not lhs_alloc_cell:
                break

            res = optparse(opt, re.compile(r"\A\."), ".")
            if not res:
                break

            lhs_alloc_ent = optparse(opt, ident_rexpr, "allocator cell entry name")
            if not lhs_alloc_ent:
                break

            res = optparse(opt, re.compile(r"\A=>"), "=>")
            if not res:
                break

            rhs_alloc_cell = optparse(opt, ident_rexpr, "allocator cell name")
            if not rhs_alloc_cell:
                break

            res = optparse(opt, re.compile(r"\A\."), ".")
            if not res:
                break

            rhs_alloc_ent = optparse(opt, ident_rexpr, "allocator cell entry name")
            if not rhs_alloc_ent:
                break

            self._substituteAllocator[sym(f"{lhs_alloc_cell}.{lhs_alloc_ent}")] = (  # type: ignore[attr-defined]
                lhs_alloc_cell,
                lhs_alloc_ent,
                rhs_alloc_cell,
                rhs_alloc_ent,
            )

            if opt[0] == "":
                break

            res = optparse(opt, re.compile(r"\A,"), ",")
            if not res:
                break

    def set_noServerChannelOpenerCode(self, rhs: Any) -> None:
        """プラグイン引数 noServerChannelOpenerCode のチェック。"""
        rhs_sym = sym(rhs)
        if rhs_sym == Symbol("true"):
            self._noServerChannelOpenerCode = True
        elif rhs_sym == Symbol("false"):
            self._noServerChannelOpenerCode = False
        else:
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: specify true or false for noServerChannelOpenerCode"
            )

    def set_clientSemaphoreCelltype(self, rhs: Any) -> None:
        """プラグイン引数 clientSemaphoreCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._semaphoreCelltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._semaphoreCelltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "OpaqueRPCPlugin: clientSemaphoreCelltype '$1' not celltype or not found",
                rhs,
            )

    def set_clientSemaphoreInitializer(self, rhs: Any) -> None:
        """プラグイン引数 clientSemaphoreInitializer のチェック。"""
        self._semaphoreInitializer = sym(rhs)

    def set_clientErrorHandler(self, rhs: Any) -> None:
        """プラグイン引数 clientErrorHandler のチェック。"""
        self._clientErrorHandler = rhs

    def set_serverErrorHandler(self, rhs: Any) -> None:
        """プラグイン引数 serverErrorHandler のチェック。"""
        self._serverErrorHandler = rhs

    ##### 情報取得 #####

    def get_cell_name(self) -> Any:
        """セルの名前を得る（ThroughPlugin::get_cell_name plugin.rb をオーバーライド）。"""
        return self._cell_name  # type: ignore[attr-defined]

    ##### 初期化・チェック #####

    def initialize_opaque_marshaler(self) -> None:
        """marshaler のセルタイプ名を設定する。"""
        from tecsgen.context import get_context

        self._taskPriority = 9
        self._stackSize = 4096
        self._serverChannelCelltype = sym("tSocketServer")
        self._clientChannelCelltype = sym("tSocketClient")
        self._serverChannelCell = sym(f"{to_s(self._cell_name)}Server")  # type: ignore[attr-defined]
        self._clientChannelCell = sym(f"{to_s(self._cell_name)}Client")  # type: ignore[attr-defined]
        self._serverChannelInitializer = sym(
            self.subst_name("portNo=8931+$count$;")  # type: ignore[attr-defined]
        )
        self._clientChannelInitializer = sym(
            self.subst_name('portNo=8931+$count$; serverAddr="127.0.0.1"; ')  # type: ignore[attr-defined]
        )
        self._taskCelltype = sym("tTask")
        self._PPAllocatorSize = None
        self._TDRCelltype = sym("tNBOTDR")
        self._substituteAllocator: dict[Any, Any] = {}
        self._noServerChannelOpenerCode = False
        self._semaphoreCelltype = sym("tSemaphore")
        self._semaphoreInitializer = sym(
            'initialCount = 1; attribute = C_EXP( "TA_NULL" ); '
        )
        self._clientErrorHandler = None
        self._serverErrorHandler = None
        self._b_genOpener = False
        self._taskMainCelltype = sym("tRPCDedicatedTaskMain")

        self._marshaler_celltype_name = sym(
            f"tOpaqueMarshaler_{to_s(self._signature.get_global_name())}"  # type: ignore[attr-defined]
        )
        self._unmarshaler_celltype_name = sym(
            f"tOpaqueUnmarshaler_{to_s(self._signature.get_global_name())}"  # type: ignore[attr-defined]
        )
        self._marshaler_celltype_file_name = (
            f"{get_context().gen}/{to_s(self._marshaler_celltype_name)}.cdl"
        )

        if self._signature.get_context() != "task":  # type: ignore[attr-defined]
            self.cdl_error(  # type: ignore[attr-defined]
                "OPQ9999 context of signature ($1) must be 'task'. $2 is not compatible with RPCPlugin",
                self._signature.get_name(),  # type: ignore[attr-defined]
                self._signature.get_context(),  # type: ignore[attr-defined]
            )

        # signature で対応できないものをチェック
        def _check(func_decl: Any, param_decl: Any) -> None:
            if param_decl.get_direction() == Y.OUT:
                if truthy(param_decl.get_count()) and not truthy(param_decl.get_size()):
                    self.cdl_error(  # type: ignore[attr-defined]
                        "$1.$2: size_is must be specified for out parameter of Opaque RPC",
                        self._signature.get_namespace_path(),  # type: ignore[attr-defined]
                        f"{to_s(func_decl.get_name())}.{to_s(param_decl.get_name())}",
                    )
                if param_decl.get_string() == -1:
                    self.cdl_error(  # type: ignore[attr-defined]
                        "$1.$2: string length must be specified for out parameter of Opaque RPC",
                        self._signature.get_namespace_path(),  # type: ignore[attr-defined]
                        f"{to_s(func_decl.get_name())}.{to_s(param_decl.get_name())}",
                    )

        self._signature.each_param(_check)  # type: ignore[attr-defined]

    def check_opener_code(self) -> None:
        """Opener Code の生成時のチェック。"""
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.componentobj.port import Port

        nsp = NamespacePath.analyze(to_s(self._serverChannelCelltype))
        scct = Namespace.find(nsp)
        if scct is not None:
            obj = scct.find(sym("eOpener"))
            if (
                isinstance(obj, Port)
                and sym(obj.get_signature().get_name())
                == Symbol("sServerChannelOpener")
                and self._noServerChannelOpenerCode is False
            ):
                self._b_genOpener = True
                self._taskMainCelltype = sym("tRPCDedicatedTaskMainWithOpener")
        if (
            self._noServerChannelOpenerCode is False
            and self._taskMainCelltype != Symbol("tRPCDedicatedTaskMainWithOpener")
        ):
            self.cdl_warning(  # type: ignore[attr-defined]
                "O9999 ServerChannelOpener code not generated, not found 'entry sServerChannelOpener eOpener'"
            )

    def check_PPAllocator(self) -> None:
        """PPAllocator の必要性をチェックする。"""
        if self._signature.need_PPAllocator(True) and self._PPAllocatorSize is None:  # type: ignore[attr-defined]
            self.cdl_error(  # type: ignore[attr-defined]
                "PPAllocatorSize must be speicified for size_is array"
            )

    #####

    def gen_marshaler_celltype(self) -> None:
        from tecsgen.core.plugin import CFile

        f = CFile.open(self._marshaler_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)

        alloc_call_port = (
            "  call sPPAllocator cPPAllocator;\n" if self._PPAllocatorSize else ""
        )

        f.print(
            f"// GenOpaqueMarshler0001\n"
            f"celltype {to_s(self._marshaler_celltype_name)} {{\n"
            f"  entry {to_s(self._signature.get_namespace_path())} eClientEntry;\n"  # type: ignore[attr-defined]
            "  call sTDR       cTDR;\n"
            "  [optional]\n"
            "    call sSemaphore cLockChannel;\n"
            "  [optional]\n"
            "    call sRPCErrorHandler cErrorHandler;\n"
            "};\n"
            f"celltype {to_s(self._unmarshaler_celltype_name)} {{\n"
            f"  call {to_s(self._signature.get_namespace_path())} cServerCall;\n"  # type: ignore[attr-defined]
            "  call  sTDR       cTDR;\n"
            "  [optional]\n"
            "    call sRPCErrorHandler cErrorHandler;\n"
            "  entry sUnmarshalerMain  eService;\n"
            f"{alloc_call_port}}};\n"
        )
        f.close()

    # ===  受け口関数の本体コードを生成（頭部と末尾は別途出力） #####

    def gen_ep_func_body(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: list[Any],
    ) -> None:
        if sym(ct_name) == self._unmarshaler_celltype_name:
            self.gen_ep_func_body_unmarshal(
                file,
                b_singleton,
                ct_name,
                global_ct_name,
                sig_name,
                ep_name,
                func_name,
                func_global_name,
                func_type,
                params,
            )
        else:
            self.gen_ep_func_body_marshal(
                file,
                b_singleton,
                ct_name,
                global_ct_name,
                sig_name,
                ep_name,
                func_name,
                func_global_name,
                func_type,
                params,
            )

    def gen_ep_func_body_marshal(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: list[Any],
    ) -> None:
        """marshal コードの生成。"""
        b_void = False
        b_ret_er = False

        type_ = func_type.get_type().get_original_type()

        file.print("\t// GenOpaqueMarshler0010\n")
        if not type_.is_void():
            file.print(f"\t{func_type.get_type().get_type_str()}\t\tretval_;\n")
            from tecsgen.core.cdl_types import DefinedType

            if isinstance(
                func_type.get_type(), DefinedType
            ) and func_type.get_type().get_type_str() in (
                "ER",
                "ER_INT",
            ):
                b_ret_er = True
        else:
            b_void = True

        file.print("\tER\t\tercd_;\n")
        file.print("\tint16_t\tstate_;\n")

        func_id = f"FUNCID_{to_s(self._signature.get_global_name())}_{to_s(func_name)}".upper()  # type: ignore[attr-defined]
        fid = self._signature.get_id_from_func_name(func_name)  # type: ignore[attr-defined]
        file.print(
            f"\tint16_t\tfunc_id_ = {func_id};\t/* (id of '{to_s(func_name)}') = {to_s(fid)}*/\n"
        )

        if not b_singleton:
            file.print(
                f"\t{to_s(ct_name)}_CB *p_cellcb;\n\n"
                "\tif( VALID_IDX( idx ) ){\n"
                f"\t\tp_cellcb = GET_CELLCB(idx);\n"
            )
            if b_ret_er:
                file.print("\t}else{\n\t\treturn ERCD( E_RPC, E_ID );\n\t}\n")
            else:
                file.print(
                    utf8_literal(
                        "\t}else{\n\t\t/* エラー処理コードをここに記述 */\n\t}\n\n"
                    )
                )

        if func_type.has_receive():
            file.print("\t/* initialize receive parameters */\n")
            for param in params:
                if param.get_direction() == Y.RECEIVE:
                    file.print(f"\t*{to_s(param.get_name())} = 0;\n")

        file.print(
            "\t/* Channel Lock (GenOpaqueMarshler0012) */\n"
            "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_GET_SEM );\n"
            "\tif( is_cLockChannel_joined() ){\n"
            "\t\tif( (ercd_=cLockChannel_wait()) != E_OK )\n"
            "\t\t\tgoto error_reset;\n"
            "\t}\n"
        )

        file.print(
            utf8_literal(
                "\t/* SOPの送出 (GenOpaqueMarshler0013) */\n"
                "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_SEND_SOP );\n"
                "\tif( ( ercd_ = cTDR_sendSOP( true ) ) != E_OK )\n"
                "\t\tgoto error_reset;\n"
            )
        )

        file.print(
            utf8_literal(
                "\t/* 関数 id の送出 (GenOpaqueMarshler0014) */\n"
                "\tif( ( ercd_ = cTDR_putInt16( func_id_ ) ) != E_OK )\n"
                "\t\tgoto error_reset;\n"
            )
        )

        b_get = False  # marshal なら put
        b_marshal = True  # marshal

        if func_type.has_inward():
            file.print(
                utf8_literal(
                    "\t/* 入力引数送出 (GenOpaqueMarshler0015) */\n"
                    "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_SEND_BODY );\n"
                )
            )
            self.print_params(
                params, file, 1, b_marshal, b_get, True, "eClientEntry", func_name
            )
            self.print_params(
                params, file, 1, b_marshal, b_get, False, "eClientEntry", func_name
            )
        self.print_out_nullable(params, file, 1, b_marshal)

        b_continue = "false" if func_type.is_oneway() else "true"
        file.print(
            utf8_literal(
                "\t/* EOPの送出（パケットの掃きだし）(GenOpaqueMarshler0016) */\n"
            )
            + "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_SEND_EOP );\n"
            f"\tif( (ercd_=cTDR_sendEOP({b_continue})) != E_OK )\n"
            "\t\tgoto error_reset;\n\n"
        )

        if func_type.has_send():
            file.print(
                "\t/* dealloc send parameter while executing (GenOpaqueMarshler0017) */\n"
                "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_EXEC );\n"
            )
            self.dealloc_for_params(
                params, file, 1, Y.SEND, f"eClientEntry_{to_s(func_name)}"
            )
            file.print("\n")

        if not func_type.is_oneway():
            file.print(
                utf8_literal(
                    "\t/* パケットの始まりをチェック (GenOpaqueMarshler0018) */\n"
                    "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_RECV_SOP );\n"
                    "\tif( (ercd_=cTDR_receiveSOP( true )) != E_OK )\n"
                    "\t\tgoto error_reset;\n"
                )
            )

            b_get = True  # marshaler は get
            file.print(
                utf8_literal("\t/* 戻り値の受け取り (GenOpaqueMarshler0019) */\n")
            )
            self.print_param(
                "retval_",
                func_type.get_type(),
                file,
                1,
                Y.RETURN,
                None,
                None,
                b_marshal,
                b_get,
            )

            if func_type.has_outward():
                if b_ret_er:
                    indent_level = 2
                    file.print("\tif( MERCD( retval_ ) != E_RPC ){\n")
                else:
                    indent_level = 1
                indent = "\t" * indent_level

                file.print(
                    f"{indent}"
                    + utf8_literal("/* 出力値の受け取り (GenOpaqueMarshler0020) */\n")
                    + f"{indent}SET_RPC_STATE( state_, RPCSTATE_CLIENT_RECV_BODY );\n"
                )
                self.print_params(
                    params,
                    file,
                    indent_level,
                    b_marshal,
                    b_get,
                    True,
                    "eClientEntry",
                    func_name,
                )
                self.print_params(
                    params,
                    file,
                    indent_level,
                    b_marshal,
                    b_get,
                    False,
                    "eClientEntry",
                    func_name,
                )

                if b_ret_er:
                    file.print("\t}\n")

            file.print(
                utf8_literal(
                    "\n\t/* パケットの終わりをチェック (GenOpaqueMarshler0021) */\n"
                    "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_RECV_EOP );\n"
                    "\tif( (ercd_=cTDR_receiveEOP(false)) != E_OK )\n"
                    "\t\tgoto error_reset;\n"
                )
            )

        file.print(
            "\t/* Channel Unlock (GenOpaqueMarshler0022) */\n"
            "\tSET_RPC_STATE( state_, RPCSTATE_CLIENT_RELEASE_SEM );\n"
            "\tif( is_cLockChannel_joined() ){\n"
            "\t\tif( (ercd_=cLockChannel_signal()) != E_OK )\n"
            "\t\t\tgoto error_reset;\n"
            "\t}\n"
        )

        file.print(
            "\t/* state_ is not used in normal case (GenOpaqueMarshler0023) */\n"
            "  /* below is to avoid 'set but not used' warnning */\n"
            "\t(void)state_;\n"
        )

        if b_void is False:
            file.print("\treturn retval_;\n")
        else:
            file.print("\treturn;\n")

        file.print("\nerror_reset:\n")

        if func_type.has_send():
            file.print("\t/* dealloc send parameter (GenOpaqueMarshler0024) */\n")
            file.print("\tif( state_ < RPCSTATE_CLIENT_EXEC ){\n")
            self.dealloc_for_params(
                params, file, 2, Y.SEND, f"eClientEntry_{to_s(func_name)}"
            )
            file.print("\t}\n")

        if func_type.has_receive():
            file.print("\t/* receive parameter (GenOpaqueMarshler0025) */\n")
            self.dealloc_for_params(
                params, file, 1, Y.RECEIVE, f"eClientEntry_{to_s(func_name)}", True
            )

        file.print("\tif( MERCD( ercd_ ) != E_RESET )\n\t\t(void)cTDR_reset();\n")

        file.print(
            "\t/* Channel Unlock (GenOpaqueMarshler0026) */\n"
            "\tif( is_cLockChannel_joined() )\n"
            "\t\tcLockChannel_signal();\n\n"
            "\tif( ercd_ != E_OK && is_cErrorHandler_joined() )\n"
            "\t\tcErrorHandler_errorOccured( func_id_, ercd_, state_ );\n"
        )

        if b_ret_er is not False:
            file.print(
                "\treturn ERCD( E_RPC, MERCD( ercd_ ) ); /* (GenOpaqueMarshler0027) */\n"
            )
        else:
            file.print("\treturn;/* (GenOpaqueMarshler0028) */\n")

    def gen_ep_func_body_unmarshal(
        self,
        file: Any,
        b_singleton: bool,
        ct_name: Any,
        global_ct_name: Any,
        sig_name: Any,
        ep_name: Any,
        func_name: Any,
        func_global_name: Any,
        func_type: Any,
        params: list[Any],
    ) -> None:
        """unmarshal コードの生成。"""
        b_ret_er = True

        file.print(
            "  /* (GenOpaqueMarshler0101) */\n"
            "\tint16_t\tfunc_id_;\n"
            "\tER\t\tercd_ = E_OK;\n"
            "\tint16_t\tstate_;\n\n"
            f"\t{to_s(ct_name)}_CB *p_cellcb;\n\n"
            "\tif( VALID_IDX( idx ) ){\n"
            "\t\tp_cellcb = GET_CELLCB(idx);\n"
        )

        if b_ret_er:
            file.print("\t}else{\n\t\treturn E_ID;\n\t}\n")
        else:
            file.print(
                utf8_literal("\t}else{\n\t\t/* エラー処理コードをここに記述 */\n\t}\n")
            )

        file.print(
            utf8_literal(
                "\n  /* (GenOpaqueMarshler0102) */\n"
                "#ifdef RPC_DEBUG\n"
                '\tsyslog(LOG_INFO, "Entering RPC service loop" );\n'
                "#endif\n\n"
                "\t/* SOPのチェック */\n"
                "\tSET_RPC_STATE( state_, RPCSTATE_SERVER_RECV_SOP );\n"
                "\tif( (ercd_=cTDR_receiveSOP( false )) != E_OK )\n"
                "\t\tgoto error_reset;\n"
                "\t/* func_id の取得 */\n"
                "\tif( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )\n"
                "\t\tgoto error_reset;\n\n"
                "#ifdef RPC_DEBUG\n"
                '\tsyslog(LOG_INFO, "unmarshaler task: func_id: %d", func_id_ );\n'
                "#endif\n"
                "  /* (GenOpaqueMarshler0103) */\n"
                "\tswitch( func_id_ ){\n"
            )
        )

        for f in self._signature.get_function_head_array():  # type: ignore[attr-defined]
            f_name = f.get_name()
            func_id = f"FUNCID_{to_s(self._signature.get_global_name())}_{to_s(f_name)}".upper()  # type: ignore[attr-defined]
            fid = self._signature.get_id_from_func_name(f_name)  # type: ignore[attr-defined]

            file.print(
                f"\tcase {func_id}:\t\t/* (id of '{to_s(f_name)}') = {to_s(fid)} */ \n"
                f"\t\tercd_ = tOpaqueUnmarshaler_{to_s(self._signature.get_global_name())}_{to_s(f_name)}( p_cellcb, &state_ );\n"  # type: ignore[attr-defined]
                "\t\tbreak;\n"
            )

        ppallocator_dealloc_str = (
            utf8_literal(
                "\t/* PPAllocator のすべてを解放 */\n\tcPPAllocator_dealloc_all();"
            )
            if self._PPAllocatorSize
            else ""
        )

        file.print(
            "  /* (GenOpaqueMarshler0104) */\n"
            "\tdefault:\n"
            '\t\tsyslog(LOG_INFO, "unmarshaler task: ERROR: unknown func_id: %d", func_id_ );\n'
            "\t\tercd_ = E_ID;\n"
            "\t};\n"
            f"error_reset:  /* OK cases also come here */\n{ppallocator_dealloc_str}\n"
            "\tif( ercd_ == E_OK )\n"
            "\t\treturn ercd_;\n"
            "\tif( is_cErrorHandler_joined() )\n"
            "\t\tercd_ = cErrorHandler_errorOccured( func_id_, ercd_, state_ );\n"
            "\tif( MERCD( ercd_ ) != E_RESET )\n"
            "\t\t(void)cTDR_reset();\n"
            "\treturn ercd_;\n"
        )

    # === PREAMBLE 部のコード生成 #####

    def gen_preamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """アンマーシャラセルタイプの場合、アンマーシャラ関数のプロトタイプ宣言を生成。"""
        if sym(ct_name) != self._unmarshaler_celltype_name:
            return

        file.print(
            utf8_literal(
                "/* header file (strlen, memset) (GenOpaqueMarshler0201) */\n"
                "#include\t<string.h>\n\n"
                "/* アンマーシャラ関数のプロトタイプ宣言 */\n"
            )
        )

        for f in self._signature.get_function_head_array():  # type: ignore[attr-defined]
            f_name = f.get_name()
            func_id = self._signature.get_id_from_func_name(f_name)  # type: ignore[attr-defined]
            file.print(
                f"static ER  tOpaqueUnmarshaler_{to_s(self._signature.get_global_name())}_{to_s(f_name)}"  # type: ignore[attr-defined]
                f"(CELLCB *p_cellcb, int16_t *state);\t/* func_id: {to_s(func_id)} */\n"
            )
        file.print("\n")

    # === POSTAMBLE 部のコード生成 #####

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        from tecsgen.core.cdl_types import ArrayType

        if sym(ct_name) != self._unmarshaler_celltype_name:
            return

        file.print(
            utf8_literal("\n/*** アンマーシャラ関数 (GenOpaqueMarshler0301) ***/\n\n")
        )
        for f in self._signature.get_function_head_array():  # type: ignore[attr-defined]
            f_name = f.get_name()
            f_type = f.get_declarator().get_type()
            fid = self._signature.get_id_from_func_name(f_name)  # type: ignore[attr-defined]

            b_ret_er = False
            init_retval = ""
            if f_type.get_type().is_void():
                b_void = True
            else:
                b_void = False
                if f_type.get_type().get_type_str() in ("ER", "ER_INT"):
                    b_ret_er = True
                    init_retval = " = E_OK"

            file.print(
                "/* (GenOpaqueMarshler0302)  */\n"
                "/*\n"
                f" * name:    {to_s(f_name)}\n"
                f" * func_id: {to_s(fid)} \n"
                " */\n"
                "static ER\n"
                f"tOpaqueUnmarshaler_{to_s(self._signature.get_global_name())}_{to_s(f_name)}(CELLCB *p_cellcb, int16_t *state_)\t\t\n"  # type: ignore[attr-defined]
                "{\n"
                "\tER      ercd_;\n"
            )

            params = f.get_declarator().get_type().get_paramlist().get_items()
            for par in params:
                name = par.get_name()
                type_ = par.get_type().get_original_type()

                dir_ = par.get_direction()
                if dir_ == Y.RECEIVE:
                    type_ = type_.get_type()
                init = " = 0" if dir_ in (Y.SEND, Y.RECEIVE) else ""

                if isinstance(type_, ArrayType):
                    type_ = type_.get_type()
                    aster = "(*"
                    aster2 = ")"
                else:
                    aster = ""
                    aster2 = ""

                import re

                type_str = re.sub(r"\bconst\b *", "", type_.get_type_str())
                file.printf(
                    "\t%-12s %s%s%s%s%s;\n",
                    type_str,
                    aster,
                    to_s(name),
                    aster2,
                    type_.get_type_str_post(),
                    init,
                )

                if dir_ == Y.OUT and type_.is_nullable():
                    file.print(f"\tint8_t\tb_{to_s(name)}_null_;\n")

            if not b_void:
                file.printf(
                    "\t%-12s retval_%s%s;\n",
                    f_type.get_type().get_type_str(),
                    f_type.get_type().get_type_str_post(),
                    init_retval,
                )

            file.print(
                utf8_literal(
                    "\n\t/* 入力引数受取 (GenOpaqueMarshler0303) */\n"
                    "\tSET_RPC_STATE( *state_, RPCSTATE_SERVER_RECV_BODY );\n"
                )
            )
            b_get = True  # unmarshal では get
            b_marshal = False
            self.print_params(
                params, file, 1, b_marshal, b_get, True, "cServerCall", f_name
            )
            self.print_params(
                params, file, 1, b_marshal, b_get, False, "cServerCall", f_name
            )
            self.print_out_nullable(params, file, 1, b_marshal)

            file.print(
                utf8_literal(
                    "\t/* パケット終わりをチェック (GenOpaqueMarshler0304) */\n"
                    "\tSET_RPC_STATE( *state_, RPCSTATE_SERVER_RECV_EOP );\n"
                )
            )
            b_continue = "false" if f_type.is_oneway() else "true"
            file.print(
                f"\tif( (ercd_=cTDR_receiveEOP({b_continue})) != E_OK )\n"
                "\t\tgoto error_reset;\n\n"
            )

            self.alloc_for_out_params(
                params, file, 1, Y.OUT, "cPPAllocator_alloc", None
            )

            file.print(
                utf8_literal(
                    "\t/* 対象関数の呼出し (GenOpaqueMarshler0305) */\n"
                    "\tSET_RPC_STATE( *state_, RPCSTATE_SERVER_EXEC );\n"
                )
            )
            if b_void:
                file.print(f"\tcServerCall_{to_s(f_name)}(")
            else:
                file.print(f"\tretval_ = cServerCall_{to_s(f_name)}(")

            delim = " "
            for par in params:
                file.print(delim)
                delim = ", "
                if par.get_direction() == Y.RECEIVE:
                    file.print("&")
                file.print(to_s(par.get_name()))
            file.print(" );\n")

            if not f.is_oneway():
                file.print(
                    utf8_literal(
                        "\n\t/* SOPの送出 (GenOpaqueMarshler0306) */\n"
                        "\tSET_RPC_STATE( *state_, RPCSTATE_SERVER_SEND_SOP );\n"
                        "\tif( ( ercd_ = cTDR_sendSOP( false ) ) != E_OK )\n"
                        "\t\tgoto error_reset;\n"
                    )
                )

                b_get = False  # unmarshaler は put
                if not b_void:
                    file.print(utf8_literal("\t/* 戻り値の送出 */\n"))
                    self.print_param(
                        "retval_",
                        f_type.get_type(),
                        file,
                        1,
                        Y.RETURN,
                        None,
                        None,
                        b_marshal,
                        b_get,
                    )

                if f_type.has_outward():
                    if b_ret_er:
                        indent_level = 2
                        file.print("\tif( MERCD( retval_ ) != E_RPC ){\n")
                    else:
                        indent_level = 1
                    indent = "\t" * indent_level

                    file.print(
                        f"{indent}"
                        + utf8_literal("/* 出力値の送出 (GenOpaqueMarshler0307) */\n")
                        + f"{indent}SET_RPC_STATE( *state_, RPCSTATE_SERVER_SEND_BODY );\n"
                    )
                    self.print_params(
                        params,
                        file,
                        indent_level,
                        b_marshal,
                        b_get,
                        True,
                        "cServerCall",
                        f_name,
                    )
                    self.print_params(
                        params,
                        file,
                        indent_level,
                        b_marshal,
                        b_get,
                        False,
                        "cServerCall",
                        f_name,
                    )

                    if f_type.has_receive():
                        file.print(f"{indent}/* dealloc receive parameter */\n")
                        self.dealloc_for_params(
                            params,
                            file,
                            indent_level,
                            Y.RECEIVE,
                            f"cServerCall_{to_s(f_name)}",
                        )

                    if b_ret_er:
                        file.print("\t}\n")

                file.print(
                    utf8_literal(
                        "\t/* パケットの終わり（掃きだし） (GenOpaqueMarshler0308) */\n"
                        "\tSET_RPC_STATE( *state_, RPCSTATE_SERVER_SEND_EOP );\n"
                        "\tif( (ercd_=cTDR_sendEOP(false)) != E_OK )\n"
                        "\t\tgoto error_reset;\n"
                    )
                )

            file.print("\treturn E_OK;\n")
            file.print("\nerror_reset:\n")

            if f_type.has_send():
                file.print("\t/* dealloc send parameter (GenOpaqueMarshler0309) */\n")
                file.print("\tif( *state_ < RPCSTATE_SERVER_EXEC ){\n")
                self.dealloc_for_params(
                    params, file, 2, Y.SEND, f"cServerCall_{to_s(f_name)}", True
                )
                file.print("\t}\n")

            if f_type.has_receive() and b_ret_er:
                file.print(
                    "\t/* dealloc receive parameter (GenOpaqueMarshler0310) */\n"
                )
                file.print("\tif( MERCD( retval_ ) != E_RPC ){\n")
                self.dealloc_for_params(
                    params, file, 2, Y.RECEIVE, f"cServerCall_{to_s(f_name)}"
                )
                file.print("\t}\n")

            file.print("\treturn ERCD( E_RPC, MERCD( ercd_ ) );\n")
            file.print("}\n\n")
            # ここ（個々の関数）ではエラーハンドラーは呼び出さない。呼び元（サーバーのメイン関数）で呼び出す。

    # b_marshal:: bool / b_get:: bool
    #  b_marshal = true  && b_get == false   :  マーシャラで入力引数送出
    #  b_marshal = true  && b_get == true    :  マーシャラで出力引数受取
    #  b_marshal = false && b_get == false   :  アンマーシャラで入力引数受取
    #  b_marshal = false && b_get == true    :  アンマーシャラで出力引数送出
    # b_referenced:: size_is, count_is, string で参照されているものを出力
    def print_params(
        self,
        params: list[Any],
        file: Any,
        nest: int,
        b_marshal: bool,
        b_get: bool,
        b_referenced: bool,
        port_name: str,
        func_name: Any,
    ) -> None:
        for param in params:
            if b_referenced != param.is_referenced():
                continue

            dir_ = param.get_direction()
            if (b_get is False and b_marshal is True) or (
                b_get is True and b_marshal is False
            ):
                if dir_ in (Y.IN, Y.INOUT):
                    self.print_param(
                        param.get_name(),
                        param.get_type(),
                        file,
                        nest,
                        dir_,
                        None,
                        None,
                        b_marshal,
                        b_get,
                        "cPPAllocator_alloc",
                        None,
                    )
                elif dir_ == Y.SEND:
                    alloc_cp = (
                        f"{port_name}_{to_s(func_name)}_{to_s(param.get_name())}_alloc"
                    )
                    self.print_param(
                        param.get_name(),
                        param.get_type(),
                        file,
                        nest,
                        dir_,
                        None,
                        None,
                        b_marshal,
                        b_get,
                        alloc_cp,
                        None,
                    )
            else:
                if dir_ in (Y.OUT, Y.INOUT):
                    self.print_param(
                        param.get_name(),
                        param.get_type(),
                        file,
                        nest,
                        dir_,
                        None,
                        None,
                        b_marshal,
                        b_get,
                        None,
                        None,
                    )
                elif dir_ == Y.RECEIVE:
                    alloc_cp = (
                        f"{port_name}_{to_s(func_name)}_{to_s(param.get_name())}_alloc"
                    )
                    if b_get:
                        outer = (
                            "(*"  # マーシャラ側では、ポインタが (send と比べ) 一つ多い
                        )
                        outer2 = ")"
                    else:
                        outer = None  # アンマーシャラ側では、ポインタが一つ外されている
                        outer2 = None
                    type_ = param.get_type().get_referto()
                    self.print_param(
                        param.get_name(),
                        type_,
                        file,
                        nest,
                        dir_,
                        outer,
                        outer2,
                        b_marshal,
                        b_get,
                        alloc_cp,
                        None,
                    )

    def alloc_for_out_params(
        self,
        params: list[Any],
        file: Any,
        nest: int,
        dir_: Any,
        alloc_cp: Any,
        alloc_cp_extra: Any,
    ) -> None:
        """アロケータコードを生成 (out のアンマーシャラ用)。"""
        for param in params:
            if param.get_direction() == Y.OUT:
                self.alloc_for_out_param(
                    param.get_name(),
                    param.get_type(),
                    file,
                    nest,
                    None,
                    None,
                    alloc_cp,
                    alloc_cp_extra,
                )

    def alloc_for_out_param(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        outer: str | None,
        outer2: str | None,
        alloc_cp: Any,
        alloc_cp_extra: Any,
    ) -> None:
        """アロケータコードを生成 (out のアンマーシャラ用個別パラメータの生成)。"""
        from tecsgen.core.cdl_types import IntType

        org_type = type_.get_original_type()
        o = outer or ""
        o2 = outer2 or ""
        if org_type.is_nullable():
            indent = "\t" * nest
            file.print(f"{indent}if( ! b_{to_s(name)}_null_  ){{\n")
            nest += 1

        if isinstance(org_type, PtrType):
            indent = "\t" * nest
            count = org_type.get_count()
            size = org_type.get_size()
            string = org_type.get_string()
            if truthy(count) or truthy(size) or truthy(string):
                loop_counter_type = IntType(
                    16
                )  # mikan 方を size_is, count_is の引数の型とする
                if truthy(count):
                    length = to_s(count)
                elif truthy(size):
                    length = to_s(size)
                else:
                    from tecsgen.core.expression import Expression

                    if isinstance(string, Expression):
                        length = to_s(string)
                    else:
                        raise RuntimeError(
                            f"unsuscripted string used for out parameter {to_s(name)}"
                        )

                if truthy(org_type.get_max()) and string is None:
                    file.print(
                        f"{indent}/* (GenOpaqueMarshler0401) */\n"
                        f"{indent}if( {length} > {to_s(org_type.get_max())} ){{\t/* GenOpaqueMarshaler max check 2 */\n"
                        f"{indent}\tercd_ = E_PAR;\n"
                        f"{indent}\tgoto error_reset;\n"
                        f"{indent}}}\n"
                    )

                elem_type = org_type.get_type()
                file.print(
                    f"{indent}/* (GenOpaqueMarshler0402) */\n"
                    f"{indent}if((ercd_={to_s(alloc_cp)}(sizeof({elem_type.get_type_str()}"
                    f"{elem_type.get_type_str_post()})*{length},(void **)&{o}{to_s(name)}{o2}"
                    f"{to_s(alloc_cp_extra)}))!=E_OK)\t/* GenOpaqueMarshaler 1 */\n"
                    f"{indent}\tgoto error_reset;\n"
                )

                if isinstance(elem_type, PtrType):
                    file.print(
                        f"{indent}{{  /* (GenOpaqueMarshler0403) */\n"
                        f"{indent}\t{loop_counter_type.get_type_str()}  i__{nest}, length__{nest} = {length};\n"
                        f"{indent}\tfor( i__{nest} = 0; i__{nest} < length__{nest}; i__{nest}++ ){{\n"
                    )
                    self.alloc_for_out_param(
                        name,
                        elem_type,
                        file,
                        nest + 2,
                        outer,
                        f"{o2}[i__{nest}]",
                        alloc_cp,
                        alloc_cp_extra,
                    )
                    file.print(f"{indent}\t}}\n{indent}}}\n")
            else:
                elem_type = org_type.get_type()
                file.print(
                    f"{indent}/* (GenOpaqueMarshler0404) */\n"
                    f"{indent}if((ercd_={to_s(alloc_cp)}(sizeof({elem_type.get_type_str()}"
                    f"{elem_type.get_type_str_post()}),(void **)&{o}{to_s(name)}{o2}"
                    f"{to_s(alloc_cp_extra)}))!=E_OK)\t/* GenOpaqueMarshaler 2 */\n"
                    f"{indent}\tgoto error_reset;\n"
                )

        if org_type.is_nullable():
            nest -= 1
            indent = "\t" * nest
            file.print(
                f"{indent}}} else {{\n{indent}\t{to_s(name)} = NULL;\n{indent}}}\n"
            )
            nest += 1

    def dealloc_for_params(
        self,
        params: list[Any],
        file: Any,
        nest: int,
        dir_: Any,
        dealloc_cp: str,
        b_reset: bool = False,
    ) -> None:
        """引数の一括デアロケートコードの生成。

        send：マーシャラの最後、receive：アンマーシャラの最後で一括して引数をデアロケートする
        """
        reset_str = "_reset" if b_reset else ""

        for param in params:
            if dir_ == param.get_direction():
                indent = "\t" * nest
                type_ = param.get_type().get_original_type()
                aster = ""
                if dir_ == Y.RECEIVE:
                    type_ = type_.get_type().get_original_type()  # ポインタを一つ外す
                    if b_reset:
                        aster = "*"
                count = type_.get_count()
                size = type_.get_size()
                if (truthy(size) or truthy(count)) and type_.get_type().has_pointer():
                    length = f", {to_s(count)}" if truthy(count) else f", {to_s(size)}"
                else:
                    length = ""
                cp = f"{dealloc_cp}_{to_s(param.get_name())}_dealloc{reset_str}".upper()
                file.print(f"{indent}{cp}({aster}{to_s(param.get_name())}{length});\n")

    def print_out_nullable(
        self, params: list[Any], file: Any, nest: int, b_marshal: bool
    ) -> None:
        """out で nullable な引数の情報を渡す。

        out nullable の場合、in, send, receive のように、値を渡す直前ではなく、呼出し時に渡す
        """
        indent = "\t" * nest
        for param in params:
            if param.get_direction() != Y.OUT:
                continue
            if not param.is_nullable():
                continue
            if b_marshal:
                file.print(
                    f"{indent}if( (ercd_=cTDR_putInt8( (int8_t)({to_s(param.get_name())} == NULL) )) != E_OK )\n"
                    f"{indent}\tgoto error_reset;\n"
                )
            else:
                # 呼び先は alloc_for_out_param で nullable の対応する
                file.print(
                    f"{indent}if( (ercd_=cTDR_getInt8( &b_{to_s(param.get_name())}_null_)) != E_OK )\n"
                    f"{indent}\tgoto error_reset;\n"
                )


GenOpaqueMarshaler.RPC_PLUGIN_ARG_PROC = {
    "clientChannelCelltype": lambda obj, rhs: obj.set_clientChannelCelltype(rhs),
    "serverChannelCelltype": lambda obj, rhs: obj.set_serverChannelCelltype(rhs),
    "clientChannelCell": lambda obj, rhs: obj.set_clientChannelCell(rhs),
    "serverChannelCell": lambda obj, rhs: obj.set_serverChannelCell(rhs),
    "clientChannelInitializer": lambda obj, rhs: obj.set_clientChannelInitializer(rhs),
    "serverChannelInitializer": lambda obj, rhs: obj.set_serverChannelInitializer(rhs),
    "clientSemaphoreCelltype": lambda obj, rhs: obj.set_clientSemaphoreCelltype(rhs),
    "clientSemaphoreInitializer": lambda obj, rhs: obj.set_clientSemaphoreInitializer(
        rhs
    ),
    "clientErrorHandler": lambda obj, rhs: obj.set_clientErrorHandler(rhs),
    "serverErrorHandler": lambda obj, rhs: obj.set_serverErrorHandler(rhs),
    "TDRCelltype": lambda obj, rhs: obj.set_TDRCelltype(rhs),
    "PPAllocatorSize": lambda obj, rhs: obj.set_PPAllocatorSize(rhs),
    "substituteAllocator": lambda obj, rhs: obj.set_substituteAllocator(rhs),
    "noServerChannelOpenerCode": lambda obj, rhs: obj.set_noServerChannelOpenerCode(
        rhs
    ),
    "taskCelltype": lambda obj, rhs: obj.set_taskCelltype(rhs),
    "taskPriority": lambda obj, rhs: obj.set_taskPriority(rhs),
    "stackSize": lambda obj, rhs: obj.set_stackSize(rhs),
}
