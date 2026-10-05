"""GenTransparentMarshaler.rb の移植。`RPCPlugin` に mix-in される。

@task_priority:: int
@channelCelltype:: str
@channelCellName:: str
@PPAllocatorSize:: int | None

`RPCPlugin` を使うケース（`rpc`・`class`・`DataPumpHolder`）は、r3304 では
`TransparentRPCSignaturePlugin` が存在せず Ruby 版自身もコード生成の前に失敗していた
（[[tecsgen内部仕様 - 09 プラグイン機構#9.7.1]] の既知の問題）。コード生成部分は `SharedRPCPlugin`
（`sharedRPC` ケース、Ruby 版で成功する）が使うため P5j で全量移植した。tecsgen-rb で
`TransparentRPCSignaturePlugin` が追加され、これらのケースも成功するようになった
（`plugin/TransparentRPCSignaturePlugin.py`）。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.ruby_compat import Y, gsub, sym, to_s, truthy, utf8_literal

# 型検査のときだけ Node の子として扱う（mixin から cdl_error を呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.syntaxobj.node import Node

    class _Base(Node):
        pass
else:
    _Base = object


class GenTransparentMarshaler(_Base):
    # プラグイン引数名と処理（サブクラスが複製して追加する。RPCPlugin.py 参照）
    RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    def set_taskPriority(self, rhs: Any) -> None:
        """プラグイン引数 taskPriority のチェック。"""
        self._task_priority = rhs

    def set_channelCelltype(self, rhs: Any) -> None:
        """プラグイン引数 channelCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._channel_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._channel_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: channeclCelltype '$1' not celltype or not found", rhs
            )

    def set_TDRCelltype(self, rhs: Any) -> None:
        """プラグイン引数 TDRCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._tdr_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._tdr_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: TDRCelltype '$1' not celltype or not found", rhs
            )

    def set_channelCellName(self, rhs: Any) -> None:
        """プラグイン引数 channelCellName のチェック。"""
        import re

        self._channel_cell_name = rhs
        if not re.match(r"\A[a-zA-Z_]\w*", to_s(rhs)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: channeclCellName '$1' unsuitable for identifier", rhs
            )

    def set_PPAllocatorSize(self, rhs: Any) -> None:
        """プラグイン引数 PPAllocatorSize のチェック。"""
        self._pp_allocator_size = rhs

    def initialize_transparent_marshaler(self, cell_name: Any) -> None:
        """marshaler のセルタイプ名を設定する。"""
        from tecsgen.context import get_context

        # 他で初期化されてない場合に設定
        if getattr(self, "_task_priority", None) is None:
            self._task_priority = 8
        if getattr(self, "_channel_celltype", None) is None:
            self._channel_celltype = "tDataqueueOWChannel"
        if getattr(self, "_tdr_celltype", None) is None:
            self._tdr_celltype = "tTDR"
        if getattr(self, "_channel_cell_name", None) is None:
            self._channel_cell_name = f"{to_s(cell_name)}_Channel"
        if getattr(self, "_pp_allocator_size", None) is None:
            self._pp_allocator_size = None
        if getattr(self, "_b_datapumpholder", None) is None:
            self._b_datapumpholder = False

        marshaler_head_append = "DPH" if self._b_datapumpholder is True else ""
        self._marshaler_celltype_name = f"tMarshaler{marshaler_head_append}_{to_s(self._signature.get_global_name())}"
        self._unmarshaler_celltype_name = f"tUnmarshaler{marshaler_head_append}_{to_s(self._signature.get_global_name())}"
        self._marshaler_celltype_file_name = (
            f"{get_context().gen}/{self._marshaler_celltype_name}.cdl"
        )

        if self._signature.get_context() != "task":
            self.cdl_error(  # type: ignore[attr-defined]
                "RPC9999 context of signature ($1) must be 'task'. $2 is not compatible with RPCPlugin",
                self._signature.get_name(),
                self._signature.get_context(),
            )

    def gen_marshaler_celltype(self) -> None:
        """marshaler・unmarshaler のセルタイプを生成する。"""
        from tecsgen.core.plugin import CFile

        if truthy(self._pp_allocator_size):
            alloc_call_port = "  call sPPAllocator cPPAllocator;\n"
        else:
            alloc_call_port = ""

        f = CFile.open(self._marshaler_celltype_file_name, "w")
        # 同じ内容を二度書く可能性あり (AppFile は不可)
        sig_path = to_s(self._signature.get_namespace_path())  # type: ignore[attr-defined]
        f.print(
            "/*\n"
            " * generated by GenTransparentMarshaler invoked by TransparentChannelPlugin\n"
            "/ */\n"
            f"celltype {self._marshaler_celltype_name} {{\n"
            f"  entry {sig_path} eClientEntry;\n"
            "  call sTDR        cTDR;\n"
            "  call sEventflag  cEventflag;\n"
            "  [optional]\n"
            "    call sSemaphore cLockChannel;  // this port is eliminated by optimize\n"
            "};\n"
            f"celltype {self._unmarshaler_celltype_name} {{\n"
            f"  call {sig_path} cServerCall;\n"
            "  call sTDR        cTDR;\n"
            "  call sEventflag  cEventflag;\n"
            "  entry sUnmarshalerMain  eUnmarshalAndCallFunction;\n"
            f"{alloc_call_port}}};\n"
        )
        f.close()

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
        """受け口関数の本体コードを生成（頭部と末尾は別途出力）。"""
        # unmarshaler クラスか?
        if sym(ct_name) == sym(self._unmarshaler_celltype_name):
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
        from tecsgen.core.cdl_types import DefinedType, PtrType

        b_void = False
        b_ret_er = False

        # 関数の戻り値の元の型を得る(typedef されている場合)
        type_ = func_type.get_type().get_original_type()
        file.print("    /* (GenTransparentMarshler0101) */\n")
        # 戻り値記憶用の変数を出力（void 型の関数では出力しない）
        if not type_.is_void():
            ret_type = func_type.get_type()
            if isinstance(ret_type, DefinedType) and ret_type.get_type_str() in (
                "ER",
                "ER_INT",
            ):
                file.print(f"    {ret_type.get_type_str()}  retval_ = E_OK;\n")
                b_ret_er = True
            else:
                file.print(f"    {ret_type.get_type_str()}  retval_;\n")
        else:
            b_void = True

        file.print("    ER      ercd_;\n")
        file.print("    FLGPTN  flgptn;\n")

        # 呼び先の signature を取り出す
        signature = self._signature  # type: ignore[attr-defined]

        # 関数 ID （整数値）
        func_id = signature.get_id_from_func_name(func_name)
        file.print(
            f"    int16_t  func_id_ = {to_s(func_id)};    /* id of {to_s(func_name)}: {to_s(func_id)} */\n"
        )

        # シングルトンでないか？
        if not b_singleton:
            # singleton でなければ p_cellcb 取得コードを出力
            file.print(
                f"    {to_s(ct_name)}_CB *p_cellcb;\n\n"
                "    if( VALID_IDX( idx ) ){\n"
                "        p_cellcb = GET_CELLCB(idx);\n"
            )

            # エラーを返すか？
            if b_ret_er:
                file.print("    }else{\n         return ERCD( E_RPC, E_ID );\n    }\n")
            else:
                file.print(
                    utf8_literal(
                        "    }else{\n        /* エラー処理コードをここに記述 / */\n    }\n"
                    )
                )

        b_dph = self._b_datapumpholder
        if b_dph is False or func_name == sym("waitForReadDone"):
            # channel lock コード
            file.print(
                "    /* Channel Lock / */\n"
                "    if( is_cLockChannel_joined() )\n"
                "      cLockChannel_wait();\n\n"
            )

        if b_dph is False:
            # SOP を送信
            file.print(
                utf8_literal("    /* SOPの送出 (GenTransparentMarshler0102) */\n")
            )
            file.print("    if( ( ercd_ = cTDR_sendSOP( true ) ) != E_OK )\n")
            file.print("      goto error_reset;\n")
        elif func_name == sym("waitForReadDone"):
            file.print(
                utf8_literal("   /* SOP の送出 (GenTransparentMarshler0102_2) */\n")
            )
            file.print("   if( ( ercd_ = cTDR_putInt16(TDR_SOP_MAGIC1) ) != E_OK )\n")
            file.print("      goto error_reset;\n")

        # func_id を送信
        file.print(
            utf8_literal("    /* 関数 id の送出 (GenTransparentMarshler0103) */\n")
        )
        file.print("    if( ( ercd_ = cTDR_putInt16( func_id_ ) ) != E_OK )\n")
        file.print("        goto error_reset;\n")

        b_get = False  # marshal なら put
        b_marshal = True  # marshal

        # in 方向の入出力を出力
        file.print(
            utf8_literal("    /* 入力引数送出 (GenTransparentMarshler0104) */\n")
        )
        self.print_params(
            params, file, 1, b_marshal, b_get, True, func_type.is_oneway()
        )
        self.print_params(
            params, file, 1, b_marshal, b_get, False, func_type.is_oneway()
        )
        if not b_void and not func_type.is_oneway():
            ret_ptr_type = PtrType(func_type.get_type())
            self.print_param_nc(
                "retval_", ret_ptr_type, file, 1, Y.RETURN, "&", None, b_get
            )

        file.print(
            utf8_literal(
                "    /* EOPの送出（パケットの掃きだし）(GenTransparentMarshler0105) */\n"
            )
        )
        b_continue = "true" if not func_type.is_oneway() else "false"
        if b_dph is False or func_name == sym("newDataReady"):
            # EOP の送出
            file.print(f"    if( (ercd_=cTDR_sendEOP({b_continue})) != E_OK )\n")
            file.print("        goto error_reset;\n\n")

        if not func_type.is_oneway():
            file.print(
                "    if( (ercd_=cEventflag_wait( 0x01, TWF_ANDW, &flgptn )) != E_OK ){\n"
                "      ercd_ = ERCD(E_RPC,ercd_);\n"
                "      goto error_reset;\n"
                "    }\n"
                "    if( (ercd_=cEventflag_clear( 0x00 ) ) != E_OK ){\n"
                "      ercd_ = ERCD(E_RPC,ercd_);\n"
                "      goto error_reset;\n"
                "    }\n"
            )

        if b_dph is False or func_name == sym("newDataReady"):
            file.print(
                "    /* Channel Lock / */\n"
                "    if( is_cLockChannel_joined() )\n"
                "      cLockChannel_signal();\n"
            )

        if b_void is False:
            # 呼び元に戻り値をリターン
            file.print("    return retval_;\n")
        else:
            file.print("    return;\n")

        file.print(
            "\n"
            "error_reset:\n"
            "    if( ercd_ != ERCD( E_RPC, E_RESET ) )\n"
            "        (void)cTDR_reset();\n"
        )

        # channel lock コード
        if b_dph is False or func_name == sym("newDataReady"):
            file.print(
                "    /* Channel Lock / */\n"
                "    if( is_cLockChannel_joined() )\n"
                "      cLockChannel_signal();\n\n"
            )

        if b_ret_er is not False:
            # 呼び元に戻り値をリターン
            file.print("    return ercd_;\n")
        else:
            file.print("    return;\n")

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
        b_ret_er = False

        # func_id を得るコードを生成
        file.print(
            "    /* (GenTransparentMarshler0201) / */\n"
            "    int16_t   func_id_;\n"
            "    ER        ercd_;\n\n"
            f"    {to_s(ct_name)}_CB *p_cellcb;\n\n"
            "    if( VALID_IDX( idx ) ){\n"
            "        p_cellcb = GET_CELLCB(idx);\n"
        )

        if b_ret_er:
            file.print("    }else{\n        return ERCD( E_RPC, E_ID );\n    }\n")
        else:
            file.print(
                utf8_literal(
                    "    }else{\n        /* エラー処理コードをここに記述 / */\n    }\n"
                )
            )

        if self._b_datapumpholder is False:
            file.print(
                utf8_literal(
                    "\n"
                    "    /* SOPのチェック (GenTransparentMarshler0202) / */\n"
                    "    if( (ercd_=cTDR_receiveSOP( false )) != E_OK )\n"
                    "        goto error_reset;\n\n"
                    "    /* func_id の取得 / */\n"
                    "    if( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )\n"
                    "        goto error_reset;\n"
                )
            )
        else:
            file.print(
                utf8_literal(
                    "\n"
                    "    /* func_id 取得 or SOPの受信 (GenTransparentMarshler0203) / */\n"
                    "    if( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )\n"
                    "        goto error_reset;\n"
                    "    if( func_id_ == TDR_SOP_MAGIC1 ){\n"
                    "      /* SOP の後の func_id の取得 / */\n"
                    "      if( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )\n"
                    "          goto error_reset;\n"
                    "    }\n"
                )
            )

        file.print(
            "#ifdef RPC_DEBUG\n"
            '    syslog(LOG_INFO, "unmarshaler task: func_id: %d", func_id_ );\n'
            "#endif\n"
            "    switch( func_id_ ){\n"
        )
        # 呼び先の signature を取り出す
        signature = self._signature  # type: ignore[attr-defined]

        # through の signature に含まれる すべての関数について
        for f in signature.get_function_head_array():
            f_name = f.get_name()
            fid = signature.get_id_from_func_name(f_name)

            # パケットの終わりをチェック（未受け取りのデータが残っていないかチェック）
            file.print(f"    case {to_s(fid)}:       /*** {to_s(f_name)} ***/ \n")
            file.print(
                f"        if( tTransparentUnmarshaler_{to_s(signature.get_global_name())}_{to_s(f_name)}(p_cellcb) != E_OK )\n"
            )
            file.print("            goto error_reset;\n")
            file.print("        break;\n")

        if truthy(self._pp_allocator_size):
            ppallocator_dealloc_str = utf8_literal(
                "    /* PPAllocator のすべてを解放 */\n    cPPAllocator_dealloc_all();"
            )
        else:
            ppallocator_dealloc_str = ""

        file.print(
            "    default:\n"
            '        syslog(LOG_INFO, "unmarshaler task: ERROR: unknown func_id: %d", func_id_ );\n'
            "    };\n"
            f"{ppallocator_dealloc_str}\n"
            "    return E_OK;\n\n"
            "error_reset:\n"
            "    if( ercd_ != ERCD( E_RPC, E_RESET ) )\n"
            "        (void)cTDR_reset();\n"
            f"{ppallocator_dealloc_str}\n"
            "    return E_OK;\n"
        )

    # IN b_marshal, b_get
    #  b_marshal = true  && b_get == false   :  マーシャラで入力引数送出
    #  b_marshal = true  && b_get == true    :  マーシャラで出力引数受取
    #  b_marshal = false && b_get == true    :  アンマーシャラで入力引数受取
    #  b_marshal = false && b_get == get     :  アンマーシャラで出力引数送出
    def print_params(
        self,
        params: list[Any],
        file: Any,
        nest: int,
        b_marshal: Any,
        b_get: bool,
        b_referenced: bool,
        b_oneway: bool = False,
    ) -> None:
        from tecsgen.core.cdl_types import ArrayType, PtrType

        for param in params:
            if b_referenced != param.is_referenced():
                continue

            dir_ = param.get_direction()
            type_ = param.get_type()
            # Ruby の演算子の優先順位どおり (oneway && in && PtrType) || ArrayType
            if (
                b_oneway
                and dir_ == Y.IN
                and isinstance(type_.get_original_type(), PtrType)
            ) or isinstance(type_.get_original_type(), ArrayType):
                # oneway, in, PtrType の場合コピー
                alloc_cp = "cPPAllocator_alloc"
                alloc_cp_extra = None
                self.print_param(  # type: ignore[attr-defined]
                    param.get_name(),
                    type_,
                    file,
                    nest,
                    dir_,
                    None,
                    None,
                    b_marshal,
                    b_get,
                    alloc_cp,
                    alloc_cp_extra,
                )
            elif (b_get is False and truthy(b_marshal)) or (
                b_get is True and b_marshal is False
            ):
                if dir_ in (Y.IN, Y.INOUT, Y.OUT, Y.SEND, Y.RECEIVE):
                    self.print_param_nc(
                        param.get_name(),
                        type_,
                        file,
                        nest,
                        b_marshal,
                        None,
                        None,
                        b_get,
                    )

    def print_param_nc(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        b_marshal: Any,
        outer: str | None,
        outer2: str | None,
        b_get: bool,
    ) -> None:
        """コピーしない引数渡しコードの出力。"""
        from tecsgen.core.cdl_types import (
            ArrayType,
            BoolType,
            DefinedType,
            FloatType,
            IntType,
            PtrType,
            StructType,
        )

        o = outer or ""
        o2 = outer2 or ""

        if isinstance(type_, DefinedType):
            self.print_param_nc(
                name, type_.get_type(), file, nest, b_marshal, outer, outer2, b_get
            )
        elif isinstance(type_, (BoolType, IntType, FloatType, PtrType, ArrayType)):
            if isinstance(type_, BoolType):
                type_str = "Int8"
                cast_str = "int8_t"
            elif isinstance(type_, IntType):
                bit_size = type_.get_bit_size()
                sign_kind = type_.get_sign()
                if sign_kind == Y.UNSIGNED:
                    sign_c = "U"
                    sign = "u"
                elif sign_kind == Y.SIGNED:
                    if bit_size in (-1, -11):
                        # signed char の場合、signed を指定する
                        sign_c = "S"
                        sign = "s"
                    else:
                        sign_c = ""
                        sign = ""
                else:
                    sign_c = ""
                    sign = ""

                if bit_size in (-1, -11):  # -1: char_t, -11: char
                    type_str = f"{sign_c}Char"
                    cast_str = f"{sign}char_t"
                elif bit_size == -2:
                    type_str = f"{sign_c}Short"
                    cast_str = f"{sign}short_t"
                elif bit_size == -3:
                    type_str = f"{sign_c}Int"
                    cast_str = f"{sign}int_t"
                elif bit_size == -4:
                    type_str = f"{sign_c}Long"
                    cast_str = f"{sign}long_t"
                elif bit_size == -5:
                    type_str = "Intptr"
                    cast_str = "intptr_t"
                elif bit_size in (8, 16, 32, 64, 128):
                    type_str = f"{sign_c}Int{bit_size}"
                    cast_str = f"{sign}int{bit_size}_t"
                else:
                    raise RuntimeError(f"unknown bit_size '{bit_size}' for int type ")
            elif isinstance(type_, FloatType):
                if type_.get_bit_size() == 32:
                    type_str = "Float32"
                    cast_str = "float32_t"
                else:
                    type_str = "Double64"
                    cast_str = "double64_t"
            else:  # PtrType, ArrayType
                type_str = "Intptr"
                cast_str = "intptr_t"

            if type_.get_type_str() == cast_str:
                cast_str = ""
            else:
                cast_str = "(" + cast_str + ")"

            indent = "    " * nest
            if b_get:
                cast_str = gsub(r"\)$", "*)", cast_str)
                file.print(indent)
                file.print(
                    f"if( ( ercd_ = cTDR_get{type_str}( {cast_str}&({o}{to_s(name)}{o2}) ) ) != E_OK )\n"
                )
                file.print(indent)
                file.print("    goto error_reset;\n")
            else:
                file.print(indent)
                file.print(
                    f"if( ( ercd_ = cTDR_put{type_str}( {cast_str}{o}{to_s(name)}{o2} ) ) != E_OK )\n"
                )
                file.print(indent)
                file.print("    goto error_reset;\n")

        elif isinstance(type_, StructType):
            members_decl = type_.get_members_decl()
            for m in members_decl.get_items():
                if m.is_referenced():
                    self.print_param_nc(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest,
                        b_marshal,
                        f"{o}{to_s(name)}{o2}.",
                        None,
                        b_get,
                    )
            for m in members_decl.get_items():
                if not m.is_referenced():
                    self.print_param_nc(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest,
                        b_marshal,
                        f"{o}{to_s(name)}{o2}.",
                        None,
                        b_get,
                    )
        # VoidType・EnumType・FuncType は何も出力しない（Ruby 版も mikan）

    def gen_preamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """アンマーシャラセルタイプの場合、アンマーシャラ関数のプロトタイプ宣言を生成。"""
        if sym(ct_name) != sym(self._unmarshaler_celltype_name):
            return

        signature = self._signature  # type: ignore[attr-defined]
        file.print(
            utf8_literal(
                "/* アンマーシャラ関数のプロトタイプ宣言 (GenTransparentMarshler0301) */\n"
            )
        )
        # signature に含まれる すべての関数について
        for f in signature.get_function_head_array():
            f_name = f.get_name()
            fid = signature.get_id_from_func_name(f_name)
            file.print(
                f"static ER  tTransparentUnmarshaler_{to_s(signature.get_global_name())}_{to_s(f_name)}"
                f"(CELLCB *p_cellcb);\t/* func_id: {to_s(fid)} */\n"
            )
        file.print("\n")

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """アンマーシャラセルタイプの場合、アンマーシャラ関数の生成。"""
        from tecsgen.core.cdl_types import ArrayType, PtrType

        if sym(ct_name) != sym(self._unmarshaler_celltype_name):
            return

        signature = self._signature  # type: ignore[attr-defined]
        file.print(
            utf8_literal(
                "\n/*** アンマーシャラ関数 (GenTransparentMarshler0401) ***/\n\n"
            )
        )
        for f in signature.get_function_head_array():
            f_name = f.get_name()
            f_type = f.get_declarator().get_type()
            fid = signature.get_id_from_func_name(f_name)

            # 関数は返り値を持つか?
            b_void = bool(f_type.get_type().is_void())

            file.print(
                f"/*\n * name:    {to_s(f_name)}\n * func_id: {to_s(fid)} \n/ */\n"
            )
            file.print("static ER\n")
            file.print(
                f"tTransparentUnmarshaler_{to_s(signature.get_global_name())}_{to_s(f_name)}( CELLCB  *p_cellcb )\n"
            )
            file.print("{\n")
            file.print("\tER  ercd_;\n")

            # 引数を受取る変数の定義
            param_list = f.get_declarator().get_type().get_paramlist().get_items()
            for par in param_list:
                name = par.get_name()
                type_ = par.get_type()
                if isinstance(type_, ArrayType):
                    type_ = type_.get_type()
                    aster = "(*"
                    aster2 = ")"
                else:
                    aster = ""
                    aster2 = ""

                type_str = gsub(
                    r"\bconst\b *", "", type_.get_type_str()
                )  # "const" を外す

                file.printf(
                    "    %-12s %s%s%s%s;\n",
                    type_str,
                    aster,
                    to_s(name),
                    aster2,
                    type_.get_type_str_post(),
                )

            # 戻り値を受け取る変数の定義
            retval_ptr = ""
            if not b_void:
                if f.is_oneway():
                    retval_ptr = ""  # oneway の場合、受け取るが捨てられる
                else:
                    retval_ptr = "*"
                file.printf(
                    f"    %-12s {retval_ptr}retval_%s;\n",
                    f_type.get_type().get_type_str(),
                    f_type.get_type().get_type_str_post(),
                )

            # in 方向の入出力を入力
            file.print(
                utf8_literal(
                    "\n        /* 入力引数受取 (GenTransparentMarshler0402) */\n"
                )
            )
            b_get = True  # unmarshal では get
            b_marshal = False
            self.print_params(
                param_list, file, 1, b_marshal, b_get, True, f.is_oneway()
            )
            self.print_params(
                param_list, file, 1, b_marshal, b_get, False, f.is_oneway()
            )
            if not b_void and not f.is_oneway():
                ret_ptr_type = PtrType(f_type.get_type())
                self.print_param_nc(
                    "retval_", ret_ptr_type, file, 1, Y.RETURN, None, None, b_get
                )

            # パケットの受信完了
            file.print(
                utf8_literal(
                    "        /* パケット終わりをチェック (GenTransparentMarshler0403) */\n"
                )
            )
            b_continue = "true" if not f.is_oneway() else "false"
            if self._b_datapumpholder is False or f_name == sym("newDataReady"):
                file.print(f"    if( (ercd_=cTDR_receiveEOP({b_continue})) != E_OK )\n")
                file.print("        goto error_reset;\n\n")

            # 対象関数を呼出す
            file.print(
                utf8_literal(
                    "    /* 対象関数の呼出し (GenTransparentMarshler0404) */\n"
                )
            )
            if b_void:
                file.print(f"    cServerCall_{to_s(f_name)}(")
            else:
                file.print(f"    {retval_ptr}retval_ = cServerCall_{to_s(f_name)}(")

            delim = " "
            for par in param_list:
                file.print(delim)
                delim = ", "
                file.print(to_s(par.get_name()))
            file.print(" );\n")

            # oneway の場合出力、戻り値が無く、受取を待たない（非同期な呼出し）
            if not f.is_oneway():
                file.print(
                    utf8_literal(
                        "    /* 関数処理の終了を通知 (GenTransparentMarshler0405) / */\n"
                        "    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){\n"
                        "      goto error_reset;\n"
                        "    }\n"
                    )
                )
            file.print("    return E_OK;\nerror_reset:\n    return ercd_;\n}\n\n")


GenTransparentMarshaler.RPC_PLUGIN_ARG_PROC = {
    "taskPriority": lambda obj, rhs: obj.set_taskPriority(rhs),
    "channelCelltype": lambda obj, rhs: obj.set_channelCelltype(rhs),
    "TDRCelltype": lambda obj, rhs: obj.set_TDRCelltype(rhs),
    "channelCell": lambda obj, rhs: obj.set_channelCellName(rhs),
    "PPAllocatorSize": lambda obj, rhs: obj.set_PPAllocatorSize(rhs),
}
