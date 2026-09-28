"""MrubyBridgeSignaturePluginModule.rb の移植。`MrubyBridgeSignaturePlugin` に mix-in される。

Ruby 版のモジュールのクラス変数（`@@celltypes` など）は、このモジュールを include したすべての
クラスで共有されるので、ここでも `MrubyBridgeSignaturePluginModule._xxx` として持つ。
"""

from __future__ import annotations

import re
from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.ruby_compat import RubyRuntimeError, sym, to_s, truthy

# 型検査のときだけ Plugin の子として扱う（mixin から cdl_error などを呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.plugin import Plugin

    class _Base(Plugin):
        pass
else:
    _Base = object


class MrubyBridgeSignaturePluginModule(_Base):
    # プラグイン引数名と処理（ファイル末尾で設定する）
    MRUBY_BRIDGE_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    _celltypes: ClassVar[
        dict[Any, list[Any]]
    ] = {}  # {celltype_name => [BridgePlugin のインスタンス]}
    _init_celltypes: ClassVar[dict[Any, bool]] = {}
    _struct_list: ClassVar[dict[Any, Any]] = {}  # {struct_name => StructType}
    _ptr_list: ClassVar[
        dict[Any, list[Any]]
    ] = {}  # {ptr_celltype_name => TYPE_MAP のエントリ}
    _VM_list: ClassVar[dict[Any, bool]] = {}
    _VM_celltypes: ClassVar[dict[Any, dict[Any, list[Any]]]] = {}
    _VM_struct_list: ClassVar[dict[Any, dict[Any, Any]]] = {}
    _VM_ptr_list: ClassVar[dict[Any, dict[Any, Any]]] = {}
    _b_post_coded: ClassVar[bool] = False

    #  type_str: [type_str, class, (Char/Bool/Int/Float), GET_SET]
    TYPE_MAP: ClassVar[dict[str, list[str]]] = {
        "char_t": ["char_t", "Char", "Char", "INT"],
        "uchar_t": ["uchar_t", "UChar", "Char", "INT"],
        "schar_t": ["schar_t", "SChar", "Char", "INT"],
        "bool_t": ["bool_t", "Bool", "Bool", "BOOL"],
        "int8_t": ["int8_t", "Int8", "Int", "INT"],
        "int16_t": ["int16_t", "Int16", "Int", "INT"],
        "int32_t": ["int32_t", "Int32", "Int", "INT"],
        "int64_t": ["int64_t", "Int64", "Int", "INT"],
        "uint8_t": ["uint8_t", "UInt8", "Int", "INT"],
        "uint16_t": ["uint16_t", "UInt16", "Int", "INT"],
        "uint32_t": ["uint32_t", "UInt32", "Int", "INT"],
        "uint64_t": ["uint64_t", "UInt64", "Int", "INT"],
        "int": ["int", "Int", "Int", "INT"],
        "char": ["char", "Char", "Char", "INT"],  # char は char_t として扱う
        "short": ["short", "Short", "Int", "INT"],
        "long": ["long", "Long", "Int", "INT"],
        "unsigned char": ["uchar_t", "UChar", "Char", "INT"],
        "unsigned int": ["unsigned int", "UInt", "Int", "INT"],
        "unsigned short": ["unsigned short", "UShort", "Int", "INT"],
        "unsigned long": ["unsigned long", "ULong", "Int", "INT"],
        "signed char": ["schar_t", "SChar", "Char", "INT"],
        "signed int": ["int", "Int", "Int", "INT"],
        "signed short": ["short", "Short", "Int", "INT"],
        "signed long": ["long", "Long", "Int", "INT"],
        "float32_t": ["float32_t", "Float32", "Float", "FLOAT"],
        "double64_t": ["double64_t", "Double64", "Float", "FLOAT"],
        "float": ["float", "Float32", "Float", "FLOAT"],
        "double": ["double", "Double64", "Float", "FLOAT"],
    }

    _signature: Any
    _b_ignoreUnsigned: bool
    _b_auto_exclude: bool
    _includes: list[Any]
    _excludes: list[Any]
    _celltype_name: Any

    @classmethod
    def reset_module(cls) -> None:
        """モジュールのクラス変数を初期化する（1プロセスで何度も実行するテスト用）。"""
        M = MrubyBridgeSignaturePluginModule
        M._celltypes = {}
        M._init_celltypes = {}
        M._struct_list = {}
        M._ptr_list = {}
        M._VM_list = {}
        M._VM_celltypes = {}
        M._VM_struct_list = {}
        M._VM_ptr_list = {}
        M._b_post_coded = False

    def gen_preamble_ptr(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        tment = MrubyBridgeSignaturePluginModule._ptr_list[ct_name]
        file.print(
            "\n"
            f"  GET_SET_{tment[3]}( {tment[1]}, {tment[0]} )\n"
            f"  POINTER_CLASS( {tment[1]}, {tment[0]} )\n"
        )

    def gen_preamble_struct(
        self, file: Any, b_singleton: bool, ct_name: Any, global_ct_name: Any
    ) -> None:
        from tecsgen.core.cdl_types import FloatType, IntType

        tag = to_s(ct_name)
        struct_type = MrubyBridgeSignaturePluginModule._struct_list[ct_name]
        file.print(f"  /* struct {tag} */\n  STRUCT_CLASS( {tag} )\n")
        for d in struct_type.get_members_decl().get_items():
            type_ = d.get_type().get_original_type()
            if isinstance(type_, IntType):  # CIntType も IntType の子
                bit_size = type_.get_bit_size()
                if bit_size in (-11, -1):
                    t_type, ttype = "Char", "char"
                elif bit_size == -2:
                    t_type, ttype = "Short", "short"
                elif bit_size == -3:
                    t_type, ttype = "Int", "int"
                elif bit_size == -4:
                    t_type, ttype = "Long", "long"
                elif bit_size == -5:
                    t_type, ttype = "IntPtr", "intptr"
                elif bit_size in (8, 16, 32, 64):
                    t_type, ttype = f"Int{bit_size}", f"int{bit_size}"
                else:
                    raise RubyRuntimeError(
                        "MrubyBridgeSignaturePlugin: MrubyBridgeSignaturePlugin: "
                        f"cannot handle bit_size {bit_size}"
                    )
                file.print(
                    f"MEMBER_GET_SET_INT( {tag}, {to_s(d.get_name())}, {t_type}, {ttype} )\n"
                )
            elif isinstance(type_, FloatType):
                file.print(f"MEMBER_GET_SET_FLOAT( {tag}, {to_s(d.get_name())} )\n")
            else:
                raise RubyRuntimeError(
                    "MrubyBridgeSignaturePlugin: MrubyBridgeSignaturePlugin: cannot handle type"
                )

    def gen_ep_func_body_ptr(
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
        params: Any,
    ) -> None:
        t = MrubyBridgeSignaturePluginModule._ptr_list[ct_name]
        type_ = t[1]
        file.print(
            "  struct RClass *a;                                /* MBP710 */\n"
            "\n"
            f'  a = mrb_define_class_under(mrb, TECS, "{type_}Pointer", mrb->object_class);\n'
            "  MRB_SET_INSTANCE_TT(a, MRB_TT_DATA);\n"
            "\n"
            f'  mrb_define_method(mrb, a, "initialize",      {type_}Pointer_initialize,   MRB_ARGS_REQ(1));\n'
            f'  mrb_define_method(mrb, a, "[]",              {type_}Pointer_aget,         MRB_ARGS_REQ(1));\n'
            f'  mrb_define_method(mrb, a, "value",           {type_}Pointer_get_val,      MRB_ARGS_NONE());\n'
            f'  mrb_define_method(mrb, a, "[]=",             {type_}Pointer_aset,         MRB_ARGS_REQ(2));\n'
            f'  mrb_define_method(mrb, a, "value=",          {type_}Pointer_set_val,      MRB_ARGS_REQ(1));\n'
            f'  mrb_define_method(mrb, a, "size",            {type_}Pointer_size,         MRB_ARGS_NONE());\n'
            f'  mrb_define_method(mrb, a, "length",          {type_}Pointer_size,         MRB_ARGS_NONE());\n'
        )
        if t[2] == "Char":
            file.print(
                '  mrb_define_method(mrb, a, "to_s",            CharPointer_to_s, MRB_ARGS_NONE());\n'
                '  mrb_define_method(mrb, a, "from_s",          CharPointer_from_s, MRB_ARGS_REQ(1));\n'
            )

    def gen_ep_func_body_struct(
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
        params: Any,
    ) -> None:
        tag = to_s(ct_name)
        struct_type = MrubyBridgeSignaturePluginModule._struct_list[ct_name]
        file.print(
            "    struct RClass *a;                                /* MBP720 */\n"
            "\n"
            f'    a = mrb_define_class_under(mrb, TECS, "Struct{tag}", mrb->object_class);\n'
            "    MRB_SET_INSTANCE_TT(a, MRB_TT_DATA);\n"
            "\n"
            f'    mrb_define_method(mrb, a, "initialize", Struct_{tag}_initialize, MRB_ARGS_NONE());\n'
        )
        for d in struct_type.get_members_decl().get_items():
            file.print(f"  STRUCT_INIT_MEMBER( {tag}, {to_s(d.get_name())} )\n")

    def ptrMrb2C(self, file: Any, type_: Any, param: Any) -> None:
        ttype = type_.get_type().get_original_type()
        # get_type_map_ent は MrubyBridgeSignaturePlugin 側（Ruby 版と同じ配置）
        tment: Any = self.get_type_map_ent(ttype)
        tstr = tment[1]
        if truthy(param.get_size()):
            sz_str = to_s(param.get_size())
        elif truthy(
            param.get_string()
        ):  # mikan size_is と string の同時指定 (二重ポインタ) はなし
            sz_str = to_s(param.get_string())
        else:
            sz_str = "1"
        # Ruby 版はここで unsigned 型のための cast_str を求めるが、使われていない

        from tecsgen.ruby_compat import Y

        modify = ""
        if param.get_direction() in (Y.OUT, Y.INOUT) and tstr in (
            "Char",
            "SChar",
            "UChar",
        ):
            modify = "Mod"
        nullable = "Nullable" if param.is_nullable() else ""
        file.print(
            f"\t{to_s(param.get_name())} = CheckAndGet{tstr}Pointer{modify}{nullable}"
            f"( mrb, mrb_{to_s(param.get_name())}, {sz_str} );\n"
        )

    def get_celltype_name(self) -> Any:
        return self._celltype_name

    def set_ignoreUnsigned(self, rhs: Any) -> None:
        """プラグイン引数 ignoreUnsigned。"""
        if rhs == "true" or rhs is None:
            self._b_ignoreUnsigned = True

    def set_include(self, rhs: Any) -> None:
        """プラグイン引数 include。"""
        for rhs_func in to_s(rhs).split(","):
            rhs_func = re.sub(r"\s", "", rhs_func)
            found = any(
                sym(rhs_func) == a.get_name()
                for a in self._signature.get_function_head_array()
            )
            if not found:
                self.cdl_error(
                    "MRB1009 include function '$1' not found in signagture '$2'",
                    rhs,
                    self._signature.get_name(),
                )
            else:
                self._includes.append(sym(rhs_func))

    def set_exclude(self, rhs: Any) -> None:
        """プラグイン引数 exclude。

        Ruby 版は `get_function_head` の結果を `false` と比べるが、見つからないときの戻り値は nil なので
        エラーにはならず、常に登録される（そのまま再現する）。
        """
        for rhs_func in to_s(rhs).split(","):
            rhs_func = re.sub(r"\s", "", rhs_func)
            self._excludes.append(sym(rhs_func))

    def set_auto_exclude(self, rhs: Any) -> None:
        """プラグイン引数 auto_exclude。"""
        if rhs == "false":
            self._b_auto_exclude = False
        elif rhs == "true":
            self._b_auto_exclude = True  # auto_exclude = true by default
        else:
            self.cdl_warning(
                "MRB9999 auto_exclude: unknown rhs value ignored. specify true or false"
            )


MrubyBridgeSignaturePluginModule.MRUBY_BRIDGE_PLUGIN_ARG_PROC = {
    "ignoreUnsigned": lambda obj, rhs: obj.set_ignoreUnsigned(rhs),
    "include": lambda obj, rhs: obj.set_include(rhs),
    "exclude": lambda obj, rhs: obj.set_exclude(rhs),
    "auto_exclude": lambda obj, rhs: obj.set_auto_exclude(rhs),
}
