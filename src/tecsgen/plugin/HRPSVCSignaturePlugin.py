"""HRPSVCSignaturePlugin.rb の移植（内部仕様9章）。拡張サービスコールを用いたドメイン間通信のシグニチャプラグイン。

HRP ドメインプラグインによって挿入されるセルの、セルタイプを生成する。前提条件: 呼出し先が
カーネルオブジェクトかどうかの判定は HRP ドメインプラグインで実施されるため、ここでは判定しない。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.cdl_types import (
    ArrayType,
    BoolType,
    DefinedType,
    FloatType,
    IntType,
    PtrType,
    StructType,
    VoidType,
)
from tecsgen.plugin.SignaturePlugin import SignaturePlugin
from tecsgen.ruby_compat import Y, sym, to_s, truthy

# HRP3 の拡張サービスコールで扱うことのできる引数の最大個数
NUM_SVC_ARG_MAX = 5


class HRPSVCSignaturePlugin(SignaturePlugin):
    NUM_SVC_ARG_MAX = NUM_SVC_ARG_MAX

    _generated_celltype: ClassVar[dict[Any, list[Any]]] = {}  # セルタイプの重複排除用
    _signature_checked: ClassVar[dict[Any, bool]] = {}  # check_signature 済を記憶する

    @classmethod
    def reset(cls) -> None:
        HRPSVCSignaturePlugin._generated_celltype = {}
        HRPSVCSignaturePlugin._signature_checked = {}

    def __init__(self, signature: Any, option: Any) -> None:
        """signature:: Signature  シグニチャ（インスタンス）"""
        super().__init__(signature, option)

        self._signature = signature
        sig_name = to_s(signature.get_global_name())
        self._ct_name_body = sym(f"tHRPSVCBody_{sig_name}")
        self._ct_name = sym(f"tHRPSVCCaller_{sig_name}")
        self._call_port_name = sym("cCall")
        self._entry_port_name = sym("eEntry")
        self._b_printed_include_stdint = False
        self.check_signature(signature)

    def get_cell_namespace_path(self) -> Any:
        """生成するセルの namespace path を生成する。"""
        nsp = self._start_region.get_namespace_path()
        return nsp.append(self._cell_name)

    def gen_cdl_file(self, file: Any) -> None:
        cls = HRPSVCSignaturePlugin
        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if cls._generated_celltype.get(self._ct_name_body) is None:
            cls._generated_celltype[self._ct_name_body] = [self]
            file.print(
                'import_C( "t_stdlib.h" );\n'
                "\n"
                "/* HRPSVC0001 : callee side celltype */\n"
                "[active]\n"
                f"celltype {to_s(self._ct_name_body)} {{\n"
                f"    call {to_s(self._signature.get_name())} {to_s(self._call_port_name)};\n"
                "    attr {\n"
            )
            for func_head in self._signature.get_function_head_array():
                file.print(
                    f"      ACPTN   restrict_acptn_{to_s(func_head.get_name())};\n"
                )
            file.print(
                "      };\n"
                "    FACTORY {\n"
                '    write("$ct$_tecsgen.h", "#include \\"kernel_cfg.h\\"");\n'
                "    };\n"
                "};\n"
            )
        else:
            cls._generated_celltype[self._ct_name_body].append(self)

        # このセルタイプ（同じシグニチャ）は既に生成されているか？
        if cls._generated_celltype.get(self._ct_name) is None:
            cls._generated_celltype[self._ct_name] = [self]
            file.print(
                "/* HRPSVC0002 : caller side celltype */\n"
                f"celltype {to_s(self._ct_name)} {{\n"
                "    attr {\n"
                "      FN  tfn_base;    //  TFN base number\n"
                "    };\n"
                f"    entry {to_s(self._signature.get_name())} {to_s(self._entry_port_name)};\n"
                "    FACTORY {\n"
                f'      write("$ct$_factory.h", "#include \\"{to_s(self._ct_name)}_id.h\\"");\n'
                "    };\n"
                "};\n"
            )
        else:
            cls._generated_celltype[self._ct_name].append(self)

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
        """受け口関数の本体(C言語)を生成する（拡張サービスコール呼出し側の関数生成）。"""
        file.print("  CELLCB *p_cellcb = GET_CELLCB(idx);\n")
        b_void = isinstance(func_type.get_type(), VoidType)
        if not b_void:
            file.print(f"  {func_type.get_type_str()}  retval;\n")

        if not b_void:
            file.print(f"  retval = ({func_type.get_type_str()})")
        else:
            file.print("  ")

        file.print(
            f"cal_svc( ATTR_tfn_base + FUNCID_{to_s(self._signature.get_global_name()).upper()}_{to_s(func_name).upper()} - 1"
        )

        delim = ","
        i = 0
        for param in params:
            file.print(f"{delim} (intptr_t){to_s(param.get_name())}")
            i += 1

        while i < NUM_SVC_ARG_MAX:
            file.print(f"{delim} 0")
            i += 1

        file.print(" );\n\n")

        if not b_void:
            file.print("  return retval;\n")

    def gen_postamble(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        """受け口関数の postamble (C言語)を生成する（拡張サービスコール本体側の関数生成）。"""
        # Callee (Body) 側のみ生成. Caller 側は生成しない
        if ct_name != self._ct_name_body:
            return

        file2 = file
        if not self._b_printed_include_stdint:
            file2.print(
                "  #ifndef SIZE_MAX\n  #define  SIZE_MAX   (~0UL)\n  #endif\n\n"
            )
            self._b_printed_include_stdint = True

        for func_head in self._signature.get_function_head_array():
            func_type = func_head.get_type()
            func_name = func_head.get_name()
            if isinstance(func_type.get_type(), VoidType):
                retval_assign = ""
            else:
                retval_assign = "retval = (ER_UINT)"

            params = func_head.get_paramlist().get_items()
            i = 0
            passed_param: dict[int, str] = {}
            for param in params:
                passed_param[i] = to_s(param.get_name())
                i += 1

            while i < NUM_SVC_ARG_MAX:
                passed_param[i] = f"par{i + 1}"
                i += 1

            file2.print(
                "  /* HRPSVC0006 */\n"
                "  ER_UINT\n"
                f"  {to_s(self._ct_name_body)}_{to_s(func_name)}(CELLCB *p_cellcb, intptr_t {passed_param[0]}, intptr_t {passed_param[1]}, intptr_t {passed_param[2]}, intptr_t {passed_param[3]}, intptr_t {passed_param[4]}, ID cdmid)\n"
                "  {\n"
                "    ER_UINT retval = E_OK;\n"
                "\n"
            )

            # エラーチェック処理の生成
            # 呼出し元ドメインのチェックは行わない（Ruby 版も gen_caller_check_code を呼ばない）
            check_code = ""
            user_cannot_callable = False

            # パラメータにポインタが存在する場合，呼出し元タスクに対するアクセス権のチェック処理を出力する
            # ※ cdmidがカーネルドメイン(拡張サービスコール呼出し中のユーザドメインを含む)であれば
            #   prb_memの処理をスキップし，初段の拡張サービスコールのみprb_memを呼出し元タスクに発行する
            for num, param in enumerate(params):
                if param.get_declarator().get_ptr_level() > 0:
                    referto = param.get_type().get_referto()
                    align_check_str = f"!ALIGN_TYPE({passed_param[num]}, {referto.get_type_str()}) || "

                    if isinstance(referto, IntType) and referto.get_bit_size() in (
                        -11,
                        -1,
                        8,
                    ):
                        # char, char_t, int8_t (無符号含む)
                        # charデータの場合，ALIGN_TYPEは必ずTRUEとなるので，エラーチェックを省略
                        align_check_str = ""
                    direction = param.get_direction()
                    if direction == Y.IN:
                        # 入力([in])のポインタパラメータは，呼出し元タスクに
                        # TPM_READ(読出し可能)のアクセス権が必要
                        # 二重ポインタが不可のため、size_is と string が同時に設定されることはない
                        prb_func = "prb_mem"
                        if truthy(param.get_size()):
                            size_str = to_s(param.get_size())
                        elif param.get_string() == -1:
                            size_str = "SIZE_MAX"
                            prb_func = "prb_str"
                        elif truthy(param.get_string()):
                            size_str = to_s(param.get_string())
                            prb_func = "prb_str"
                        else:
                            size_str = "1"
                        check_code += (
                            "      /* HRPSVC0007 */\n"
                            f"      if ({align_check_str}{prb_func}((void *){passed_param[num]}, sizeof({referto.get_type_str()}) * ({size_str}), TSK_SELF, TPM_READ) != E_OK) {{\n"
                            "        return E_MACV;\n"
                            "      }\n"
                        )
                    elif direction in (Y.OUT, Y.INOUT):
                        # 出力([out])のポインタパラメータは，呼出し元タスクに
                        # TPM_WRITE(書込み可能)のアクセス権が必要
                        prb_func = "prb_mem"
                        if truthy(param.get_size()):
                            size_str = to_s(param.get_size())
                        elif truthy(param.get_string()):  # 引数なしの string はない
                            size_str = to_s(param.get_string())
                            # out, inout の場合、必ず領域を確保する. prb_mem を用いる
                        else:
                            size_str = "1"
                        check_code += (
                            "      /* HRPSVC0008 */\n"
                            f"      if ({align_check_str}{prb_func}((void *){passed_param[num]}, sizeof({referto.get_type_str()}) * ({size_str}), TSK_SELF, TPM_WRITE) != E_OK) {{\n"
                            "        return E_MACV;\n"
                            "      }\n"
                        )

            # 呼出し元がカーネルドメインのみ許可されている場合，
            # すべてのユーザドメインからの呼出しに対し，E_OACVを返す
            if user_cannot_callable:
                check_code = "    return E_OACV;"

            # 呼出し元がカーネルドメインの場合，アクセス権のチェック処理をスキップさせる
            file2.print(
                "    if (cdmid != TDOM_KERNEL) {\n"
                f"{check_code}\n"
                "      /* HRPSVC0009 */\n"
                f"      if( (TACP(cdmid) & ATTR_restrict_acptn_{to_s(func_name)}) == 0 ){{\n"
                "        return E_OACV;\n"
                "      }\n"
                "    }\n"
            )

            # 拡張サービスコール本体(本来の受け口関数)を呼び出す
            file2.print(
                f"    {retval_assign}{to_s(self._call_port_name)}_{to_s(func_name)}("
            )

            delim = ""
            for num, param in enumerate(params):
                file2.print(delim)
                delim = ", "
                file2.print(f"({param.get_type().get_type_str()})")
                file2.print(passed_param[num])
                file2.print(param.get_type().get_type_str_post())

            file2.print(");\n")

            file2.print("\n    return retval;\n")
            file2.print("  }\n\n")

    # ---------------------------------------------------------#
    def check_signature(self, signature: Any) -> None:
        """シグニチャのチェック。"""
        cls = HRPSVCSignaturePlugin
        if cls._signature_checked.get(signature):
            return
        cls._signature_checked[signature] = True
        for fh in signature.get_function_head_array():
            type_ = fh.get_return_type()
            self.check_return_type(signature, fh, type_)
            if len(fh.get_paramlist().get_items()) > NUM_SVC_ARG_MAX:
                self.cdl_error(
                    f"HSV0005 $1.$2: # of parameter more than {NUM_SVC_ARG_MAX}",
                    signature.get_name(),
                    fh.get_name(),
                )
            for param in fh.get_paramlist().get_items():
                self.check_param(signature, fh, param)

    def check_return_type(self, signature: Any, fh: Any, type_: Any) -> None:
        """戻り値の型のチェック。ER, ER_UINT は推奨される型。整数、ブール、void は可能、他は不可。"""
        ot = type_.get_original_type()
        if type_.get_type_str() in ("ER", "ER_UINT"):
            pass  # OK!
        elif isinstance(ot, (IntType, VoidType, BoolType)):
            self.cdl_warning(
                "HSW0001 $1.$2: $3 return type cannot get access violation error",
                signature.get_name(),
                fh.get_name(),
                type_.get_type_str().lower(),
            )
            self.check_intptr(
                f"{to_s(signature.get_name())}.{to_s(fh.get_name())} return type",
                type_,
            )
        else:
            self.cdl_error(
                "HSV0001 $1.$2 return type $3 cannot be used",
                signature.get_name(),
                fh.get_name(),
                to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
            )

    def check_param(self, signature: Any, fh: Any, param: Any) -> None:
        """引数の型のチェック。"""
        type_ = param.get_type()
        ot = type_.get_original_type()
        direction = param.get_direction()
        if direction == Y.IN:
            if isinstance(ot, (IntType, BoolType)):
                # OK!
                self.check_intptr(
                    f"{to_s(signature.get_name())}.{to_s(fh.get_name())}.{to_s(param.get_name())}",
                    type_,
                )
            elif isinstance(ot, PtrType):
                self.check_ptr(signature, fh, param, direction)
            else:
                self.cdl_error(
                    "HSV0002 $1.$2.$3 $4 param type cannot be used",
                    signature.get_name(),
                    fh.get_name(),
                    param.get_name(),
                    to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
                )
        elif direction in (Y.OUT, Y.INOUT):
            if isinstance(ot, PtrType):
                self.check_ptr(signature, fh, param, direction)
        elif direction in (Y.SEND, Y.RECEIVE):
            self.cdl_error(
                "HSV0008 $1.$2.$3 param direction '$4' cannot be used",
                signature.get_name(),
                fh.get_name(),
                param.get_name(),
                to_s(param.get_direction()).lower(),
            )

    def check_ptr(self, signature: Any, fh: Any, param: Any, direction: Any) -> None:
        type_ = param.get_type().get_referto()
        ot = type_.get_original_type()
        if isinstance(ot, (IntType, BoolType, FloatType)):
            # OK!
            self.check_intptr(
                f"{to_s(signature.get_name())}.{to_s(fh.get_name())}.{to_s(param.get_name())}",
                type_,
            )
        elif isinstance(ot, PtrType):
            self.cdl_error(
                "HSV0003 $1.$2.$3 multi-pointer type cannot be used",
                signature.get_name(),
                fh.get_name(),
                param.get_name(),
                to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
            )
        elif isinstance(ot, StructType):
            self.check_struct(signature, fh, param)
        else:
            self.cdl_error(
                "HSV0004 $1.$2.$3 $4 type cannot be used",
                signature.get_name(),
                fh.get_name(),
                param.get_name(),
                to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
            )
        if direction in (Y.OUT, Y.INOUT) and param.get_string() == -1:
            self.cdl_error(
                "HSV0009 $1.$2.$3 string argment is necessary for out/inout parameter",
                signature.get_name(),
                fh.get_name(),
                param.get_name(),
            )

    def check_struct(self, signature: Any, fh: Any, param: Any) -> None:
        type_ = param.get_type().get_referto()
        ot = type_.get_original_type()
        for decl in ot.get_members_decl().get_items():
            type_ = decl.get_type()
            ot = type_.get_original_type()
            if isinstance(ot, (IntType, BoolType, FloatType)):
                # OK!
                self.check_intptr(
                    f"{to_s(signature.get_name())}.{to_s(fh.get_name())}.{to_s(param.get_name())}.{to_s(decl.get_name())} member",
                    type_,
                )
            else:
                dbg_print(
                    f"struct member {to_s(decl.get_name())} {to_s(type_)} {to_s(decl.get_type())} {to_s(decl.get_type().get_original_type())}\n"
                )
                if isinstance(decl.get_type().get_original_type(), ArrayType):
                    self.check_struct_member_array(signature, fh, param, decl)
                else:
                    self.cdl_error(
                        "HSV0006 $1.$2.$3 $4 type cannot be used as struct member",
                        signature.get_name(),
                        fh.get_name(),
                        param.get_name(),
                        to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
                    )

    def check_struct_member_array(
        self, signature: Any, fh: Any, param: Any, member_decl: Any
    ) -> None:
        type_ = member_decl.get_type().get_type()
        ot = type_.get_original_type()
        if isinstance(ot, (IntType, BoolType, FloatType)):
            # OK!
            self.check_intptr(
                f"{to_s(signature.get_name())}.{to_s(fh.get_name())}.{to_s(param.get_name())}.{to_s(member_decl.get_name())} member",
                type_,
            )
        else:
            self.cdl_error(
                "HSV0007 $1.$2.$3 $4 type cannot be used as struct member",
                signature.get_name(),
                fh.get_name(),
                param.get_name(),
                to_s(type_.get_type_str()) + to_s(type_.get_type_str_post()),
            )

    def check_intptr(self, msg: str, type_: Any) -> None:
        dbg_print("check_intptr IN\n")
        t = type_
        while isinstance(t, DefinedType):
            dbg_print(
                f"check_intptr {msg} {t.get_type_str()} {t.get_original_type().get_type_str()}\n"
            )
            tstr = to_s(t.get_type_str())
            tstr = tstr.replace("const ", "", 1)
            tstr = tstr.replace("volatile ", "", 1)
            if tstr in ("intptr_t", "uintptr_t"):
                self.cdl_info(
                    "HSI0001 $1 type '$2' not checked by plugin",
                    msg,
                    type_.get_type_str(),
                )
            t = t.get_type()
