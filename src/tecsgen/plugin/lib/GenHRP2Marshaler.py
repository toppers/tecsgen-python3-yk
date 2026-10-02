"""GenHRP2Marshaler.rb の移植。`HRP2RPCPlugin` に mix-in される。

Ruby 版のこのファイルは `module GenTransparentMarshaler` を**再オープン**して、同じ名前のメソッドを
HRP2 向け（メッセージバッファで送る）に差し替える。そのため Ruby では、このファイルを読み込んだ後は
`GenTransparentMarshaler` を使う他のプラグインにも差し替え後のメソッドが効く。この移植は
`GenTransparentMarshaler` を継承した別クラスにして、`HRP2RPCPlugin` だけが使う（`RPCPlugin` などと
同じ実行で併用したときの影響は再現しない）。

メッセージバッファに載せる引数は、ビット幅が決まる整数（8・16・32・64・128 ビット）の値渡しだけで、
ポインタ・配列・bool などは `HRP2 RPC supports only specified bit_size` の例外になる（Ruby 版の振る舞い。
例外の前に、その引数のコードまで出力される）。

プラグインのソース（UTF-8）に書かれた日本語のリテラルは、`-k euc` のときも UTF-8 のバイト列のまま
ファイルに出る（`utf8_literal`）。
"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.lib.GenTransparentMarshaler import GenTransparentMarshaler
from tecsgen.ruby_compat import Y, gsub, no_method, sym, to_s, truthy, utf8_literal


class GenHRP2Marshaler(GenTransparentMarshaler):
    def initialize_transparent_marshaler(self, cell_name: Any) -> None:
        """marshaler のセルタイプ名を設定する。"""
        from tecsgen.context import get_context

        self._task_priority = 8
        self._channel_celltype = "tDataqueueOWChannel"
        self._tdr_celltype = "tTDR"
        self._channel_cell_name = f"{to_s(cell_name)}_Channel"
        self._pp_allocator_size = None

        sig_name = to_s(self._signature.get_name())
        self._marshaler_celltype_name = f"tMarshaler_{sig_name}"
        self._unmarshaler_celltype_name = f"tUnmarshaler_{sig_name}"
        self._marshaler_celltype_file_name = (
            f"{get_context().gen}/{self._marshaler_celltype_name}.cdl"
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
        sig = to_s(self._signature.get_name())
        # modified by ishikawa
        f.print(
            "\n"
            f"celltype {self._marshaler_celltype_name} {{\n"
            f"  entry {sig} eClientEntry;\n"
            "  call sEventflag  cEventflag;\n"
            "  call sSemaphore  cSemaphore;\n"
            "  call sMessageBuffer cMessageBuffer;\n"
            "  //[optional]\n"
            "  //  call sSemaphore cLockChannel;  // this port is eliminated by optimize\n"
            "};\n"
            f"celltype {self._unmarshaler_celltype_name} {{\n"
            f"  call {sig} cServerCall;\n"
            "  call sEventflag  cEventflag;\n"
            "  call sSemaphore  cSemaphore;\n"
            "  call sMessageBuffer cMessageBuffer;\n"
            "  entry sTaskBody  eUnmarshalAndCallFunction;\n"
            f"{alloc_call_port}\n"
            "  FACTORY{\n"
            '    write("$ct$_factory.h", "#include <t_syslog.h>");\n'
            "  };\n"
            "};\n"
        )
        f.close()

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
        from tecsgen.core.cdl_types import DefinedType, VoidType

        b_void = False
        b_ret_er = False

        # 関数の戻り値の元の型を得る(typedef されている場合)
        type_ = func_type.get_type().get_original_type()

        # 戻り値記憶用の変数を出力（void 型の関数では出力しない）
        if not isinstance(type_, VoidType):
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

        file.print("    uint8_t  msg[256];\n")

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
                    "    }else{\n"
                    + utf8_literal("        /* エラー処理コードをここに記述 */\n")
                    + "    }\n"
                )

        # channel lock コード
        file.print(
            "    ///* Channel Lock */\n"
            "    //if( is_cLockChannel_joined() )\n"
            "    //  cLockChannel_wait();\n\n"
        )

        # func_id を送信
        file.print(utf8_literal("    /* 関数 id の送出 */\n"))
        file.print("    *((int16_t *)(&msg[0])) = func_id_;\n")

        b_get = False  # marshal なら put
        b_marshal = True  # marshal

        # in 方向の入出力を出力
        self._index = 2
        file.print(utf8_literal("    /* 入力引数送出 */\n"))
        self.print_params(
            params, file, 1, b_marshal, b_get, True, func_type.is_oneway()
        )
        self.print_params(
            params, file, 1, b_marshal, b_get, False, func_type.is_oneway()
        )

        file.print(utf8_literal("    /* EOPの送出（パケットの掃きだし） */\n"))
        file.print(
            f"    if( (ercd_=cMessageBuffer_send(msg, {self._index})) != E_OK )\n"
        )
        file.print("        goto error_reset;\n\n")

        file.print("        cSemaphore_signal();\n\n")

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

        file.print(
            "    ///* Channel Lock */\n"
            "    //if( is_cLockChannel_joined() )\n"
            "    //  cLockChannel_signal();\n"
        )

        if b_void is False:
            # 呼び元に戻り値をリターン
            file.print("    cMessageBuffer_receive(&retval_);\n")
            file.print("    return retval_;\n")
        else:
            file.print("    return;\n")

        file.print(
            "\n"
            "error_reset:\n"
            "#if 0\n"
            "    if( ercd_ != ERCD( E_RPC, E_RESET ) )\n"
            "        (void)cTDR_reset();\n"
            "#endif\n"
        )

        # channel lock コード
        file.print(
            "    ///* Channel Lock */\n"
            "    //if( is_cLockChannel_joined() )\n"
            "    //  cLockChannel_signal();\n\n"
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
            "\n"
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
                "    }else{\n"
                + utf8_literal("        /* エラー処理コードをここに記述 */\n")
                + "    }\n"
            )

        file.print("\n    cSemaphore_wait();\n\n#if 0\n")
        file.print(utf8_literal("    /* SOPのチェック */\n"))
        file.print(
            "    if( (ercd_=cTDR_receiveSOP( false )) != E_OK )\n"
            "        goto error_reset;\n"
        )
        file.print(utf8_literal("    /* func_id の取得 */\n"))
        file.print(
            "    if( (ercd_=cTDR_getInt16( &func_id_ )) != E_OK )\n"
            "        goto error_reset;\n"
            "#endif\n\n"
            "    if( (ercd_ = cMessageBuffer_receive(msg) < 0 ) )\n"
            "        goto error_reset;\n"
            "    func_id_ = ((int16_t *)msg)[0];\n\n"
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
                f"        if( tTransparentUnmarshaler_{to_s(signature.get_name())}_{to_s(f_name)}() != E_OK )\n"
            )
            file.print("            goto error_reset;\n")
            file.print("        break;\n")

        if truthy(self._pp_allocator_size):
            ppallocator_dealloc_str = (
                utf8_literal("    /* PPAllocator のすべてを解放 */\n")
                + "    cPPAllocator_dealloc_all();"
            )
        else:
            ppallocator_dealloc_str = ""

        file.print(
            "    default:\n"
            + utf8_literal("#if 0 // deleted by ishikawa: tSysLogが未実装\n")
            + '        syslog(LOG_INFO, "unmarshaler task: ERROR: unknown func_id: %d", func_id_ );\n'
            "#endif /* 0 */\n"
            "        break;\n"
            "    };\n"
            f"{ppallocator_dealloc_str}\n"
            "    return;\n\n"
            "error_reset:\n"
            "#if 0\n"
            "    if( ercd_ != ERCD( E_RPC, E_RESET ) )\n"
            "        (void)cTDR_reset();\n"
            "#else\n"
            "    return ercd_;\n"
            "#endif\n"
            f"{ppallocator_dealloc_str}\n"
        )

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
                # Ruby 版は GenParamCopy を include していないので print_param が無い
                raise no_method("print_param", self)
            elif (
                (b_get is False and b_marshal is True)
                or (b_get is True and b_marshal is False)
            ) and dir_ in (Y.IN, Y.INOUT, Y.OUT, Y.SEND, Y.RECEIVE):
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
            # Ruby の bit_size は、IntType・FloatType 以外では nil
            bit_size: int | None = None
            if isinstance(type_, IntType):
                bit_size = type_.get_bit_size()
                if bit_size not in (-1, -11, -2, -3, -4, -5, 8, 16, 32, 64, 128):
                    raise RuntimeError(f"unknown bit_size '{bit_size}' for int type ")
            elif isinstance(type_, FloatType):
                bit_size = type_.get_bit_size()

            file.print("    " * nest)
            if b_get:
                file.print(
                    f"{to_s(name)} = *(({type_.get_type_str()} *)(&msg[{self._index}]));\n"
                )
            else:
                file.print(
                    f"*(({type_.get_type_str()} *)(&msg[{self._index}])) = {to_s(name)};\n"
                )
            if bit_size is None or bit_size not in (8, 16, 32, 64, 128):
                raise RuntimeError("HRP2 RPC supports only specified bit_size")
            self._index += bit_size // 8

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
        file.print(utf8_literal("/* アンマーシャラ関数のプロトタイプ宣言 */\n"))
        # signature に含まれる すべての関数について
        for f in signature.get_function_head_array():
            f_name = f.get_name()
            fid = signature.get_id_from_func_name(f_name)
            file.print(
                f"static ER  tTransparentUnmarshaler_{to_s(signature.get_name())}_{to_s(f_name)}"
                f"();\t/* func_id: {to_s(fid)} */\n"
            )
        file.print("\n")
        file.print("static uint8_t msg[256];\n")
        file.print("\n")

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """アンマーシャラセルタイプの場合、アンマーシャラ関数の生成。"""
        from tecsgen.core.cdl_types import ArrayType

        if sym(ct_name) != sym(self._unmarshaler_celltype_name):
            return

        signature = self._signature  # type: ignore[attr-defined]
        file.print(utf8_literal("\n/*** アンマーシャラ関数 ***/\n\n"))
        for f in signature.get_function_head_array():
            f_name = f.get_name()
            f_type = f.get_declarator().get_type()
            fid = signature.get_id_from_func_name(f_name)

            # 関数は返り値を持つか?
            b_void = bool(f_type.get_type().is_void())

            file.print(
                f"/*\n * name:    {to_s(f_name)}\n * func_id: {to_s(fid)} \n */\n"
            )
            file.print("static ER\n")
            file.print(
                f"tTransparentUnmarshaler_{to_s(signature.get_name())}_{to_s(f_name)}()\n"
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
                # oneway の場合、受け取るが捨てられる。それ以外も ishikawa の変更で "" にしている
                file.printf(
                    f"    %-12s {retval_ptr}retval_%s;\n",
                    f_type.get_type().get_type_str(),
                    f_type.get_type().get_type_str_post(),
                )

            # in 方向の入出力を入力
            file.print(utf8_literal("\n        /* 入力引数受取 */\n"))
            b_get = True  # unmarshal では get
            b_marshal = False
            self._index = 2
            self.print_params(
                param_list, file, 1, b_marshal, b_get, True, f.is_oneway()
            )
            self.print_params(
                param_list, file, 1, b_marshal, b_get, False, f.is_oneway()
            )

            # パケットの受信完了
            # mikan 本当は、対象関数を呼出す後に実施したい．呼出しパケットの使用終わりを宣言する目的として
            file.print(utf8_literal("        /* パケット終わりをチェック */\n"))

            # 対象関数を呼出す
            file.print(utf8_literal("    /* 対象関数の呼出し */\n"))
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

            # 戻り値、出力引数の受取コードの生成
            if not b_void and not f.is_oneway():
                file.print(
                    f"    if( (ercd_ = cMessageBuffer_send(&retval_, sizeof({f_type.get_type().get_type_str()})) != E_OK ) )\n"
                )
                file.print("        goto error_reset;\n")

            # oneway の場合出力、戻り値が無く、受取を待たない（非同期な呼出し）
            if not f.is_oneway():
                file.print(
                    utf8_literal("    /* 関数処理の終了を通知 */\n")
                    + "    if( ( ercd_ = cEventflag_set( 0x01 ) ) != E_OK ){\n"
                    "      goto error_reset;\n"
                    "    }\n"
                )
            file.print("    return E_OK;\nerror_reset:\n    return ercd_;\n}\n\n")
