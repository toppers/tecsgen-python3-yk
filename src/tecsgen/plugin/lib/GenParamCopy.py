"""GenParamCopy.rb の移植。

パラメータをコピーするマーシャラ／アンマーシャラコードを生成するメソッド `print_param` を提供する。
`RPCPlugin`・`OpaqueRPCPlugin` に mix-in される。RPCPlugin（トランスペアレント）では、oneway 関数で
in のポインタ引数の場合に限って `print_param` が用いられる。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tecsgen.core.cdl_types import (
    ArrayType,
    BoolType,
    DefinedType,
    EnumType,
    FloatType,
    FuncType,
    IntType,
    PtrType,
    StructType,
    VoidType,
)
from tecsgen.ruby_compat import Y, to_s, truthy

# 型検査のときだけ Node の子として扱う（mixin から cdl_error を呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.syntaxobj.node import Node

    class _Base(Node):
        pass
else:
    _Base = object


class GenParamCopy(_Base):
    def print_param(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        dir_: Any,
        outer: str | None,
        outer2: str | None,
        b_marshal: bool,
        b_get: bool,
        alloc_cp: Any = None,
        alloc_cp_extra: Any = None,
        name_list: Any = None,
    ) -> None:
        """引数の転送コードを生成する。"""
        o = outer or ""
        o2 = outer2 or ""
        if isinstance(type_.get_original_type(), ArrayType) and b_get and dir_ != Y.OUT:
            indent = "\t" * nest
            subsc = type_.get_subscript()
            if subsc is None:
                raise RuntimeError("Unsubscripted Array Not Supported")
            size_str = subsc.to_str(name_list, outer, outer2)
            elem_type = type_.get_type()
            file.print(
                "/* (GenParamCopy0001) */\n"
                f"{indent}if((ercd_={to_s(alloc_cp)}(sizeof({elem_type.get_type_str()}"
                f"{elem_type.get_type_str_post()})*({size_str}),(void **)&{o}{to_s(name)}{o2}"
                f"{to_s(alloc_cp_extra)}))!=E_OK)\t/* GenParamCopy 1 */\n"
                f"{indent}\tgoto error_reset;\n"
            )
            if dir_ in (Y.SEND, Y.RECEIVE) and elem_type.has_pointer():
                # send, receive の場合は、エラーリセットに備え NULL にする
                file.print(
                    f"{indent}memset( (void *){o}{to_s(name)}{o2}{to_s(alloc_cp_extra)}, 0, "
                    f"sizeof({elem_type.get_type_str()}{elem_type.get_type_str_post()})*"
                    f"({size_str});   /* GenParamCopy Alloc1 */\n"
                )
        self.print_param0(
            name,
            type_,
            file,
            nest,
            dir_,
            outer,
            outer2,
            b_marshal,
            b_get,
            alloc_cp,
            alloc_cp_extra,
            name_list,
        )

    def print_param0(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        dir_: Any,
        outer: str | None,
        outer2: str | None,
        b_marshal: bool,
        b_get: bool,
        alloc_cp: Any = None,
        alloc_cp_extra: Any = None,
        name_list: Any = None,
    ) -> None:
        indent = "\t" * nest
        o = outer or ""
        o2 = outer2 or ""

        if isinstance(type_, DefinedType):
            self.print_param0(
                name,
                type_.get_type(),
                file,
                nest,
                dir_,
                outer,
                outer2,
                b_marshal,
                b_get,
                alloc_cp,
                alloc_cp_extra,
            )
        elif isinstance(type_, (BoolType, IntType, FloatType)):
            if isinstance(type_, BoolType):
                type_str = "Bool"
            elif isinstance(type_, IntType):
                bit_size = type_.get_bit_size()
                sign_kind = type_.get_sign()
                if sign_kind == Y.UNSIGNED:
                    sign = "U"
                elif sign_kind == Y.SIGNED:
                    sign = "S" if bit_size in (-1, -11) else ""
                else:
                    sign = ""

                if bit_size in (-1, -11):  # -1: char_t, -11: char
                    type_str = f"{sign}Char"
                elif bit_size == -2:
                    type_str = f"{sign}Short"
                elif bit_size == -3:
                    type_str = f"{sign}Int"
                elif bit_size == -4:
                    type_str = f"{sign}Long"
                elif bit_size == -5:
                    type_str = "Intptr"
                elif bit_size in (8, 16, 32, 64, 128):
                    type_str = f"{sign}Int{bit_size}"
                else:
                    raise RuntimeError(f"unknown bit_size '{bit_size}' for int type ")
            else:  # FloatType
                bit_size = type_.get_bit_size()
                type_str = "Float32" if bit_size == 32 else "Double64"

            if b_get:
                file.print(
                    f"{indent}/* (GenParamCopy0101) */\n"
                    f"{indent}if( ( ercd_ = cTDR_get{type_str}( &({o}{to_s(name)}{o2}) ) ) "
                    "!= E_OK )\t/* GenParamCopy 2 */\n"
                    f"{indent}\tgoto error_reset;\n"
                )
            else:
                file.print(
                    f"{indent}/* (GenParamCopy0102) */\n"
                    f"{indent}if( ( ercd_ = cTDR_put{type_str}( {o}{to_s(name)}{o2} ) ) "
                    "!= E_OK )\t/* GenParamCopy 3 */\n"
                    f"{indent}\tgoto error_reset;\n"
                )
        elif isinstance(type_, PtrType):
            self._print_param0_ptr(
                name,
                type_,
                file,
                nest,
                dir_,
                outer,
                outer2,
                b_marshal,
                b_get,
                alloc_cp,
                alloc_cp_extra,
                name_list,
            )
        elif isinstance(type_, StructType):
            members_decl = type_.get_members_decl()
            for m in members_decl.get_items():
                if m.is_referenced():
                    self.print_param0(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest,
                        dir_,
                        f"{o}{to_s(name)}{o2}.",
                        None,
                        b_marshal,
                        b_get,
                        alloc_cp,
                        alloc_cp_extra,
                        members_decl,
                    )
            for m in members_decl.get_items():
                if not m.is_referenced():
                    self.print_param0(
                        m.get_name(),
                        m.get_type(),
                        file,
                        nest,
                        dir_,
                        f"{o}{to_s(name)}{o2}.",
                        None,
                        b_marshal,
                        b_get,
                        alloc_cp,
                        alloc_cp_extra,
                        members_decl,
                    )
        elif isinstance(type_, (VoidType, EnumType, FuncType)):
            pass  # mikan EnumType / FuncType
        elif isinstance(type_, ArrayType):
            subsc = type_.get_subscript()
            if subsc is None:
                raise RuntimeError("Unsubscripted Array Not Supported")
            size_str = subsc.to_str(name_list, outer, outer2)

            loop_counter_type = IntType(
                32
            )  # mikan 型を size_is, count_is の引数の型とする
            file.print(
                f"{indent}{{  /* (GenParamCopy0112) */\n"
                f"{indent}\t{loop_counter_type.get_type_str()}  i__{nest}, "
                f"length__{nest} = {size_str};\n"
                f"{indent}\tfor( i__{nest} = 0; i__{nest} < length__{nest}; i__{nest}++ ){{\n"
            )
            self.print_param0(
                name,
                type_.get_type(),
                file,
                nest + 2,
                dir_,
                outer,
                f"{o2}[i__{nest}]",
                b_marshal,
                b_get,
                alloc_cp,
                alloc_cp_extra,
            )
            file.print(f"{indent}\t}}\n{indent}}}\n")

    def _print_param0_ptr(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        dir_: Any,
        outer: str | None,
        outer2: str | None,
        b_marshal: bool,
        b_get: bool,
        alloc_cp: Any,
        alloc_cp_extra: Any,
        name_list: Any,
    ) -> None:
        o = outer or ""
        o2 = outer2 or ""
        count = type_.get_count()
        size = type_.get_size()
        string = type_.get_string()

        if truthy(count) or truthy(size) or truthy(string):
            nest = self.print_nullable_pre(
                name, type_, file, nest, dir_, outer, outer2, b_marshal, b_get
            )
            indent = "\t" * nest
            loop_counter_type = IntType(
                32
            )  # mikan 型を size_is, count_is の引数の型とする
            file.print(f"{indent}{{\t/* GenParamCopy0103 */\n")
            file.print(
                f"{indent}\t{loop_counter_type.get_type_str()}  i__{nest}, length__{nest};\n"
            )

            size_str = None
            count_str = None
            if truthy(size) or truthy(count):
                if truthy(size):
                    size_str = size.to_str(name_list, outer, outer2)
                count_str = (
                    count.to_str(name_list, outer, outer2)
                    if truthy(count)
                    else size_str
                )
                file.print(
                    f"{indent}\tlength__{nest} = {count_str};\t/* GenParamCopy0104 */\n"
                )

                # size_is に max 指定がある場合、length が max を超えているかチェックするコードを生成
                # alloc_cp == nil のとき dir は INOUT, OUT のはず (条件が冗長)
                if (
                    b_get
                    and truthy(type_.get_max())
                    and not ((dir_ in (Y.INOUT, Y.OUT)) and alloc_cp is None)
                ):
                    file.print(
                        f"{indent}\tif( length__{nest} > {to_s(type_.get_max())} ){{"
                        "\t/* GenParamCopy0105 max check 1 */\n"
                        f"{indent}\t\tercd_ = E_PAR;\n"
                        f"{indent}\t\tgoto error_reset;\n"
                        f"{indent}\t}}\n"
                    )
            else:  # string
                elem_bit_size = type_.get_type().get_bit_size()
                if elem_bit_size == -1:  # char_t
                    b_size = 8
                elif elem_bit_size in (8, 16, 32, 64):  # intN_t, uintN_t
                    b_size = elem_bit_size
                else:
                    self.cdl_error(
                        "R9999 $1: string specifier cannot be specified to '$2' in current implementation",
                        name,
                        type_.get_type().get_type_str()
                        + type_.get_type().get_type_str_post(),
                    )
                    b_size = None
                if not b_get:
                    from tecsgen.core.expression import Expression

                    if isinstance(string, Expression):
                        length = string.to_str(name_list, outer, outer2)
                        file.print(
                            f"{indent}\tlength__{nest} = STRNLEN{b_size}({o}{to_s(name)}{o2},"
                            f"({length}-1))+1;\t/* GenParamCopy0106 */\n"
                            f"{indent}\tif( length__{nest} < {length})\tlength__{nest} += 1;\n"
                        )
                    else:
                        file.print(
                            f"{indent}\tlength__{nest} = STRLEN{b_size}({o}{to_s(name)}{o2})+1;"
                            "\t/* GenParamCopy0107 */\n"
                        )
                    size_str = f"length__{nest}"  # string の場合、strnlen 以上の領域を確保しない
                else:
                    from tecsgen.core.expression import Expression

                    if dir_ == Y.INOUT:
                        if isinstance(string, Expression):
                            length = string.to_str(name_list, outer, outer2)
                            size_str = f"{length}"  # string(len) の場合 len を確保する
                        else:
                            raise RuntimeError(
                                f"unsuscripted string used for inout parameter {to_s(name)}"
                            )
                    else:
                        size_str = f"length__{nest}"  # string の場合、strnlen 以上の領域を確保しない
                self.print_param0(
                    f"length__{nest}",
                    loop_counter_type,
                    file,
                    nest + 1,
                    dir_,
                    None,
                    None,
                    b_marshal,
                    b_get,
                )

            if (
                b_get
                and dir_ in (Y.IN, Y.INOUT, Y.SEND, Y.RECEIVE)
                and truthy(alloc_cp)
            ):
                elem_type = type_.get_type()
                file.print(
                    f"{indent} /* (GenParamCopy0108) */\n"
                    f"{indent}\tif((ercd_={to_s(alloc_cp)}(sizeof({elem_type.get_type_str()}"
                    f"{elem_type.get_type_str_post()})*({size_str}),(void **)&{o}{to_s(name)}{o2}"
                    f"{to_s(alloc_cp_extra)}))!=E_OK)\t/* GenParamCopy 8 */\n"
                    f"{indent}\t\tgoto error_reset;\n"
                )
                if dir_ in (Y.SEND, Y.RECEIVE) and elem_type.has_pointer():
                    # send, receive の場合は、エラーリセットに備え NULL にする
                    file.print(
                        f"{indent} /* (GenParamCopy0109) */\n"
                        f"{indent}\tmemset( (void *){o}{to_s(name)}{o2}{to_s(alloc_cp_extra)}, 0, "
                        f"sizeof({elem_type.get_type_str()}{elem_type.get_type_str_post()})*"
                        f"({size_str}) );   /* GenParamCopy Alloc2 */\n"
                    )
            file.print(
                f"{indent}\tfor( i__{nest} = 0; i__{nest} < length__{nest}; i__{nest}++ ){{"
                "\t/* GenParamCopy 9 */\n"
            )
            self.print_param0(
                name,
                type_.get_type(),
                file,
                nest + 2,
                dir_,
                outer,
                f"{o2}[i__{nest}]",
                b_marshal,
                b_get,
                alloc_cp,
                alloc_cp_extra,
            )
            file.print(f"{indent}\t}}\n{indent}}}\n")

            nest = self.print_nullable_post(
                name, type_, file, nest, dir_, outer, outer2, b_marshal, b_get
            )
        else:
            # nullable (pre)
            nest = self.print_nullable_pre(
                name, type_, file, nest, dir_, outer, outer2, b_marshal, b_get
            )
            indent = "\t" * nest

            # allocate memory for getting value
            if (
                b_get
                and dir_ in (Y.IN, Y.INOUT, Y.SEND, Y.RECEIVE)
                and truthy(alloc_cp)
            ):
                elem_type = type_.get_type()
                file.print(
                    f"{indent} /* (GenParamCopy0110) */\n"
                    f"{indent}if((ercd_={to_s(alloc_cp)}(sizeof({elem_type.get_type_str()}"
                    f"{elem_type.get_type_str_post()}),(void **)&{o}{to_s(name)}{o2}"
                    f"{to_s(alloc_cp_extra)}))!=E_OK)\t/* GenParamCopy 10 */\n"
                    f"{indent}\t goto error_reset;\n"
                )
                if dir_ in (Y.SEND, Y.RECEIVE) and elem_type.has_pointer():
                    # send, receive の場合は、エラーリセットに備え NULL にする
                    file.print(
                        f"{indent} /* (GenParamCopy0111) */\n"
                        f"{indent}memset( (void *){o}{to_s(name)}{o2}{to_s(alloc_cp_extra)}, 0, "
                        f"sizeof({elem_type.get_type_str()}{elem_type.get_type_str_post()}) );"
                        "   /* GenParamCopy Alloc3 */\n"
                    )

            self.print_param0(
                name,
                type_.get_type(),
                file,
                nest,
                dir_,
                f"(*{o}",
                f"{o2})",
                b_marshal,
                b_get,
                alloc_cp,
                alloc_cp_extra,
            )
            # nullable (post)
            nest = self.print_nullable_post(
                name, type_, file, nest, dir_, outer, outer2, b_marshal, b_get
            )

    def print_nullable_pre(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        dir_: Any,
        outer: str | None,
        outer2: str | None,
        b_marshal: bool,
        b_get: bool,
    ) -> int:
        """nullable (pre)。"""
        o = outer or ""
        o2 = outer2 or ""
        if type_.is_nullable():
            indent = "\t" * nest
            if dir_ == Y.OUT:
                # 'null or not' is sent in the function 'print_out_nullable'
                if b_get:
                    file.print(
                        f"{indent}if( {o}{to_s(name)}{o2} ){{\t/* (GenParamCopy0201) Null */\n"
                    )
                else:
                    file.print(
                        f"{indent}if( ! b_{to_s(name)}_null_ ){{\t/* (GenParamCopy0202) Null */\n"
                    )
                nest += 1
            else:  # dir = :IN, :INOUT, :SEND, :RECEIVE
                if b_get:
                    file.print(f"{indent}{{\n")
                    if not (dir_ == Y.INOUT and b_marshal is True):
                        file.print(
                            f"{indent} /* (GenParamCopy0203) */\n"
                            f"{indent}\tint8_t  b_null_;\n"
                            f"{indent}\tif((ercd_=cTDR_getInt8( &b_null_ )) != E_OK )"
                            "\t/* GenParamCopy Null 20 */\n"
                            f"{indent}\t\t goto error_reset;\n"
                            f"{indent}\tif( ! b_null_ ){{\n"
                        )
                    else:  # dir = :INOUT, b_marshal = true, b_get = true の場合、NULL かどうかの情報を渡さない
                        file.print(
                            f"{indent} /* (GenParamCopy0204) */\n"
                            f"{indent}\tint8_t  b_null_ = ({o}{to_s(name)}{o2} == NULL);"
                            "\t/* GenParamCopy Null 21 */\n"
                            f"{indent}\tif( ! b_null_ ){{\n"
                        )
                else:
                    file.print(
                        f"{indent}{{\n"
                        f"{indent}\tint8_t  b_null_ = (int8_t)({o}{to_s(name)}{o2} == NULL);"
                        "\t/* GenParamCopy Null 31 */\n"
                    )
                    if not (dir_ == Y.INOUT and b_marshal is False):
                        # dir = :INOUT, b_marshal = false, b_get = false の場合
                        file.print(
                            f"{indent} /* (GenParamCopy0205) */\n"
                            f"{indent}\tif((ercd_=cTDR_putInt8( b_null_ )) != E_OK )"
                            "\t/* GenParamCopy Null 32 */\n"
                            f"{indent}\t\t goto error_reset;\n"
                        )
                    file.print(
                        f"{indent}\tif( ! b_null_ ){{\t/* GenParamCopy Null 33 */\n"
                    )
                nest += 2
        return nest

    def print_nullable_post(
        self,
        name: Any,
        type_: Any,
        file: Any,
        nest: int,
        dir_: Any,
        outer: str | None,
        outer2: str | None,
        b_marshal: bool,
        b_get: bool,
    ) -> int:
        """nullable (post)。"""
        o = outer or ""
        o2 = outer2 or ""
        if type_.is_nullable():
            if dir_ == Y.OUT:
                nest -= 1
                indent = "\t" * nest
                file.print(
                    f"{indent}}}  /* ! b_{to_s(name)}_null_   (GenParamCopy0301) Null */\n"
                )
            else:  # ( dir == :IN || dir == :INOUT || dir == :SEND || dir == :RECEIVE )
                nest -= 2
                indent = "\t" * nest
                if b_get:
                    if not (dir_ == Y.INOUT and b_marshal is True):
                        file.print(
                            f"\n{indent}\t}} else {{ /* null  (GenParamCopy0302) Null */\n"
                            f"{indent}\t\t{o}{to_s(name)}{o2} = NULL;\n"
                            f"{indent}\t}}  /* ! b_null_ */\n"
                        )
                    else:  # dir = :INOUT, b_marshal = true   # inout の out 方向
                        file.print(
                            f"{indent}\t}}  /* ! b_null_  (GenParamCopy0303) Null */\n"
                        )
                else:
                    file.print(f"{indent}\t}}\t/* (GenParamCopy0304) Null */\n")
                file.print(f"{indent}}}\t/* (GenParamCopy0305) Null */\n")
        return nest
