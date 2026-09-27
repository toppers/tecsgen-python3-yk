"""port.rb の移植。口を表すクラス（セルタイプの呼び口、受け口。`Port`）。"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.core.tecsinfo import PortTECSInfo
from tecsgen.ruby_compat import RubyRuntimeError, Y, rb_print, rb_puts, to_s, truthy


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


class Port(PortTECSInfo, BDNode):
    """@name::  str / @signature:: Signature / @port_type::  :CALL, :ENTRY
    @array_size:: nil: not array, "[]": sizeless, Integer: sized array
    @reverse_require_cell_path:: NamespacePath / @reverse_require_callport_name:: Symbol
    @allocator_port:: Port / @allocator_func_decl:: Decl / @allocator_param_decl:: ParamDecl
    @allocator_instance:: Hash / @allocator_instance_tmp:: Hash
    @b_require / @b_has_name / @b_inline / @b_omit / @b_optional / @b_ref_desc / @b_dynamic:: bool
    @celltype:: 属するセルタイプ
    最適化: @b_VMT_useless / @b_skelton_useless / @b_cell_unique:: bool
            @only_callee_port:: Port / @only_callee_cell:: Cell
    """

    def __init__(
        self,
        name: Any,
        sig_path: Any,
        port_type: Any,
        array_size: Any = None,
        reverse_require_cell_path: Any = None,
        reverse_require_entry_port_name: Any = None,
    ) -> None:
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.signature import Signature
        from tecsgen.core.expression import Expression

        super().__init__()
        self._name = name
        self._port_type = port_type

        if type(array_size) is str and array_size == "[]":
            self._array_size = array_size
        elif truthy(array_size):
            if isinstance(array_size, Expression):
                self._array_size = array_size.eval_const(None)
            else:
                self._array_size = array_size  # これはアロケータ呼び口の場合（元の呼び口で既に評価済み）
            if self._array_size is None:
                self.cdl_error("S1073 Not constant expression $1", to_s(array_size))

            if not _is_int(self._array_size):
                self.cdl_error("S1074 Not Integer $1", to_s(array_size))

        obj = Namespace.find(sig_path)  # 1
        if obj is None:
            # mikan signature の名前が不完全
            self.cdl_error("S1075 '$1' signature not found", sig_path)
        elif type(obj) is not Signature:
            self.cdl_error("S1076 '$1' not signature", sig_path)
        else:
            self._signature = obj

        # 逆require
        self._reverse_require_cell_path: Any = None
        self._reverse_require_entry_port_name: Any = None
        if truthy(reverse_require_cell_path):
            if port_type == Y.CALL:
                self.cdl_error("S1152 $1 call port cannot have fixed join", self._name)
            else:
                self._reverse_require_cell_path = reverse_require_cell_path
                self._reverse_require_entry_port_name = reverse_require_entry_port_name

                # 受け口配列か？
                if truthy(array_size):
                    self.cdl_error(
                        "S1153 $1: cannot be entry port array for fixed join port",
                        self._name,
                    )

                # 呼び口のセルタイプを探す
                ct_or_cell = Namespace.find(self._reverse_require_cell_path)  # 1
                if type(ct_or_cell) is Cell:
                    ct = ct_or_cell.get_celltype()
                elif type(ct_or_cell) is Celltype:
                    ct = ct_or_cell
                    if not ct.is_singleton():
                        self.cdl_error(
                            "S1154 $1: must be singleton celltype for fixed join",
                            to_s(self._reverse_require_cell_path),
                        )
                else:
                    ct = None
                    self.cdl_error(
                        "S1155 $1: not celltype or not found",
                        self._reverse_require_cell_path.get_path_str(),
                    )

                if ct is None:
                    return  # 既にエラー

                # 添え字なしの呼び口配列か？
                port = ct.find(self._reverse_require_entry_port_name)
                if port is None or port.get_port_type() != Y.CALL:
                    self.cdl_error(
                        "S1156 $1: not call port or not found",
                        self._reverse_require_entry_port_name,
                    )
                elif not (
                    type(port.get_array_size()) is str and port.get_array_size() == "[]"
                ):
                    self.cdl_error(
                        "S1157 $1: sized array or not array",
                        self._reverse_require_entry_port_name,
                    )

        self._b_require = False
        self._b_has_name = False
        self._b_inline = False
        self._b_optional = False
        self._b_omit = False
        self._b_ref_desc = False
        self._b_dynamic = False
        self.reset_optimize()

    def reset_optimize(self) -> None:
        """最適化に関する変数をリセットする（Region ごとに最適化のやりなおしをするため）。"""
        if self._port_type == Y.CALL:
            # call port optimize
            self._b_VMT_useless = (
                False  # VMT 不要 (true の時 VMT を介することなく呼出す)
            )
            self._b_skelton_useless = (
                False  # スケルトン関数不要   (true の時、受け口関数を呼出す)
            )
            self._b_cell_unique = False  # 唯一の呼び先セル
            self._only_callee_port: Any = None  # 唯一の呼び先ポート
            self._only_callee_cell: Any = None  # 唯一の呼び先セル
        else:
            # entry port optimize
            ctx = get_context()
            if ctx.unopt or ctx.unopt_entry:
                # 最適化なし
                self._b_VMT_useless = False
                self._b_skelton_useless = False
            else:
                # 最適化あり
                self._b_VMT_useless = True
                self._b_skelton_useless = True

    def set_celltype(self, celltype: Any) -> None:
        self._celltype = celltype

    def get_name(self) -> Any:
        return self._name

    def get_port_type(self) -> Any:
        return self._port_type

    def get_signature(self) -> Any:
        return self._signature

    def get_array_size(self) -> Any:
        return self._array_size

    def get_celltype(self) -> Any:
        return self._celltype

    def set_allocator_port(self, port: Any, fd: Any, par: Any) -> None:
        """アロケータポートの設定（この呼び口が生成されるもとになった呼び口または受け口の情報）。"""
        self._allocator_port = port
        self._allocator_func_decl = fd
        self._allocator_param_decl = par

    def is_allocator_port(self) -> bool:  # Ruby: is_allocator_port?
        return self._allocator_port is not None

    def get_allocator_port(self) -> Any:
        return self._allocator_port

    def get_allocator_func_decl(self) -> Any:
        return self._allocator_func_decl

    def get_allocator_param_decl(self) -> Any:
        return self._allocator_param_decl

    def set_require(self, b_has_name: Any) -> None:
        self._b_require = True
        self._b_has_name = b_has_name

    def is_require(self) -> Any:  # Ruby: is_require?
        return self._b_require

    def has_name(self) -> Any:  # Ruby: has_name?
        """require 呼び口が名前を持つ？（require 限定）"""
        return self._b_has_name

    def is_optional(self) -> Any:  # Ruby: is_optional?
        return self._b_optional

    def set_optional(self) -> None:
        self._b_optional = True

    def is_omit(self) -> Any:  # Ruby: is_omit?
        """omit 指定されている?"""
        if truthy(self._b_omit):
            return self._b_omit
        if not truthy(self._signature):
            return self._signature
        return self._signature.is_empty()

    def set_omit(self) -> None:
        self._b_omit = True

    def set_VMT_useless(self) -> None:
        self._b_VMT_useless = True

    def set_skelton_useless(self) -> None:  # スケルトン関数不要
        self._b_skelton_useless = True

    def set_cell_unique(self) -> None:  # 呼び先セルは一つだけ
        self._b_cell_unique = True

    def set_specifier(self, spec_list: list[Any]) -> None:
        """呼び口/受け口の指定子の設定（inline, allocator の指定）。"""
        for s in spec_list:
            s0 = s[0]
            if s0 == Y.INLINE:
                if self._port_type == Y.CALL:
                    self.cdl_error("S1077 inline: cannot be specified for call port")
                    continue
                self._b_inline = True
            elif s0 == Y.OMIT:
                if self._port_type == Y.ENTRY:
                    self.cdl_error("S9999 omit: cannot be specified for entry port")
                    continue
                self._b_omit = True
            elif s0 == Y.OPTIONAL:
                if self._port_type == Y.ENTRY:
                    self.cdl_error("S1078 optional: cannot be specified for entry port")
                    continue
                self._b_optional = True
            elif s0 == Y.REF_DESC:
                if self._port_type == Y.ENTRY:
                    self.cdl_error(
                        "S9999 ref_desc: cannnot be specified for entry port"
                    )
                    continue
                self._b_ref_desc = True
            elif s0 == Y.DYNAMIC:
                if self._port_type == Y.ENTRY:
                    self.cdl_error("S9999 dynamic: cannnot be specified for entry port")
                    continue
                self._b_dynamic = True
            elif s0 == Y.ALLOCATOR:
                if self._port_type == Y.CALL:
                    self.cdl_error("S1079 allocator: cannot be specified for call port")
                if truthy(self._allocator_instance_tmp):
                    self.cdl_error("S1080 duplicate allocator specifier")
                    continue
                self._allocator_instance_tmp = s[1]
            else:
                raise RubyRuntimeError(f"unknown specifier {to_s(s0)}")
        if self._b_dynamic or self._b_ref_desc:
            dyn_ref = "dynamic" if self._b_dynamic else "ref_desc"
            if self._b_omit:  # is_omit? は is_empty? も含んでいるので使えない
                self.cdl_error("S9999 omit cannot be specified with $1", dyn_ref)
            elif truthy(self._signature) and self._signature.is_empty():
                self.cdl_error(
                    "S9999 $1 cannot be specified for empty signature", dyn_ref
                )
            elif truthy(self._signature) and self._signature.has_descriptor():
                pass
        elif self._b_dynamic and self._b_ref_desc:
            self.cdl_error(
                "S9999 both dynamic & ref_desc cannot be specified simultaneously"
            )

    def set_allocator_instance(self) -> None:
        """リレーアロケータ、内部アロケータのインスタンスを設定する。

        呼び口の前方参照可能なように、セルタイプの解釈の最後で行う。
        """
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.generator import Token

        if self._allocator_instance_tmp is None:
            return

        self._allocator_instance: dict[Any, Any] = {}
        for ai in self._allocator_instance_tmp:
            direction = None
            alloc_type = ai[0]
            # ai = [ :INTERNAL_ALLOC|:RELAY_ALLOC, func_name, param_name, rhs ]
            if alloc_type == Y.INTERNAL_ALLOC:
                if (
                    type(self._owner) is not CompositeCelltype
                ):  # ミスを防ぐために composite でなければとした
                    self.cdl_error("S1081 self allocator not supported yet")
                    continue
            elif alloc_type == Y.RELAY_ALLOC:
                pass
            elif alloc_type == Y.NORMAL_ALLOC:
                # composite の受け口で右辺が "eEnt.func.param" 形式で指定されていた場合
                self.cdl_error(
                    "S1174 $1 not suitable for lhs, suitable lhs: 'func.param'",
                    f"{to_s(ai[1])}.{to_s(_at(ai, 3))}.{to_s(_at(ai, 4))}",
                )
                continue
            else:
                raise RubyRuntimeError(f"Unknown allocator type {to_s(ai[1])}")

            # '=' 左辺(func_name,param_name)は実在するか?
            if truthy(self._signature):  # signature = nil なら既にエラー
                fh = self._signature.get_function_head(ai[1])
                if fh is None:
                    self.cdl_error("S1082 function '$1' not found in signature", ai[1])
                    continue
                decl = fh.get_declarator()
                if not decl.is_function():
                    continue  # 既にエラー
                paramdecl = decl.get_type().get_paramlist().find(ai[2])
                if paramdecl is None:
                    self.cdl_error(
                        "S1083 '$1' not found in function '$2'", ai[2], ai[1]
                    )
                    continue
                if paramdecl.get_direction() in (Y.SEND, Y.RECEIVE):
                    direction = paramdecl.get_direction()
                else:
                    self.cdl_error(
                        "S1084 '$1' in function '$2' is not send or receive",
                        ai[2],
                        ai[1],
                    )
                    continue

            # 重複指定がないか?
            key = f"{to_s(self._name)}_{to_s(ai[1])}_{to_s(ai[2])}"
            if truthy(self._allocator_instance.get(key)):
                self.cdl_error(
                    "S1085 duplicate allocator specifier for '$1_$2'", ai[1], ai[2]
                )

            # 右辺のチェック
            ai2: Any = None
            if alloc_type == Y.INTERNAL_ALLOC:
                ele = ai[3].get_elements()
                if ele[0] != Y.IDENTIFIER:
                    self.cdl_error(
                        "S1086 $1: rhs not in 'allocator_entry_port' form", to_s(ai[3])
                    )
                    continue

                ep_name = ele[1]  # アロケータ受け口名
                ep = self._owner.find(ep_name.get_path()[0])  # mikan "a::b"
                if (
                    ep is None
                    or type(ep) is not Port
                    or ep.get_port_type() != Y.ENTRY
                    or not ep.get_signature().is_allocator()
                ):
                    self.cdl_error(
                        "S1175 $1 not found or not allocator entry port for $2",
                        ep_name,
                        ai[1],
                    )
                # ai2 = [ :INTERNAL_ALLOC, func_name, param_name, rhs_ep_name ]
                ai2 = [ai[0], ai[1], ai[2], ep_name]

            elif alloc_type == Y.RELAY_ALLOC:
                ele = ai[3].get_elements()
                if (
                    ele[0] != Y.OP_DOT
                    or ele[1][0] != Y.OP_DOT
                    or ele[1][1][0] != Y.IDENTIFIER
                    or not ele[1][1][1].is_name_only()
                    or type(ele[1][2]) is not Token
                    or type(ele[2]) is not Token
                ):  # 1
                    self.cdl_error(
                        "S1176 rhs not in 'call_port.func.param' form for for $1_$2",
                        ai[1],
                        ai[2],
                    )  # S1086
                    continue
                func_name = ele[1][2]
                cp_name = ele[1][1][1].get_name()
                param_name = ele[2].to_sym()
                cp = self._owner.find(cp_name)  # リレーする先の呼び口
                if truthy(cp):
                    sig = cp.get_signature()
                    if truthy(sig) and truthy(self._signature):
                        fh = self._signature.get_function_head(func_name)
                        if fh is None:
                            self.cdl_error(
                                "S1087 function '$1' not found in signature '$2'",
                                func_name,
                                sig.get_name(),
                            )
                            continue
                        decl = fh.get_declarator()
                        if not decl.is_function():
                            continue  # 既にエラー
                        paramdecl = decl.get_type().get_paramlist().find(param_name)
                        if paramdecl is None:
                            self.cdl_error(
                                "S1088 '$1' not found in function '$2'",
                                param_name,
                                func_name,
                            )
                            continue
                        if paramdecl.get_direction() in (Y.SEND, Y.RECEIVE):
                            if (
                                alloc_type == Y.RELAY_ALLOC
                                and direction != paramdecl.get_direction()
                            ):
                                self.cdl_error(
                                    "S1089 relay allocator send/receive mismatch between $1.$2 and $3_$4.$5",
                                    ai[1],
                                    ai[2],
                                    cp_name,
                                    func_name,
                                    param_name,
                                )
                        else:
                            self.cdl_error(
                                "S1090 '$1' in function '$2' is not send or receive",
                                param_name,
                                func_name,
                            )
                            continue
                else:
                    ct_name = (
                        self._celltype.get_name()
                        if truthy(self._celltype)
                        else "(None)"
                    )
                    self.cdl_error(
                        "S1091 call port '$1' not found in celltype $2",
                        cp_name,
                        ct_name,
                    )
                    continue
                # ai2 = [ :RELAY_ALLOC, func_name, param_name, rhs_cp_name, rhs_func_name, rhs_param_name ]
                ai2 = [ai[0], ai[1], ai[2], cp_name, func_name, param_name]

            self._allocator_instance[key] = ai2

    def is_inline(self) -> Any:  # Ruby: is_inline?
        return self._b_inline

    def is_VMT_useless(self) -> Any:
        if self._port_type == Y.ENTRY and get_context().unopt_entry is True:
            # プラグインから $unopt_entry を設定するケースのため
            return False
        return self._b_VMT_useless

    def is_skelton_useless(self) -> Any:  # Ruby: is_skelton_useless?
        if self._port_type == Y.ENTRY and get_context().unopt_entry is True:
            return False
        return self._b_skelton_useless

    def is_cell_unique(self) -> Any:  # Ruby: is_cell_unique?
        return self._b_cell_unique

    def set_entry_VMT_skelton_useless(
        self,
        b_VMT_useless: Any,
        b_skelton_useless: Any,
    ) -> None:
        """受け口最適化の設定。"""
        if not truthy(b_VMT_useless):
            self._b_VMT_useless = False
        if not truthy(b_skelton_useless):
            self._b_skelton_useless = False

    def set_only_callee(self, callee_port: Any, callee_cell: Any) -> None:
        """唯一の結合先を設定（最適化で使用）。"""
        self._only_callee_port = callee_port
        self._only_callee_cell = callee_cell

    def get_real_callee_port(self) -> Any:
        """唯一の結合先ポートを返す(compositeの場合実セル)。"""
        if truthy(self._only_callee_cell):
            return self._only_callee_cell.get_real_port(
                self._only_callee_port.get_name()
            )
        return None

    def get_real_callee_cell(self) -> Any:
        """唯一の結合先セルを返す(compositeの場合実セル)。"""
        if truthy(self._only_callee_cell):
            return self._only_callee_cell.get_real_cell(
                self._only_callee_port.get_name()
            )
        return None

    def get_allocator_instance(self) -> Any:
        return self._allocator_instance

    def get_allocator_instance_tmp(self) -> Any:
        return self._allocator_instance_tmp

    def create_reverse_require_join(self, cell: Any) -> None:
        """逆require の結合を生成する（STAGE: S）。"""
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression
        from tecsgen.core.generator import Token

        if self._reverse_require_cell_path is None:
            return

        # 呼び元セルを探す
        ct_or_cell = Namespace.find(
            self._reverse_require_cell_path
        )  # mikan namespace    #1
        if type(ct_or_cell) is Cell:
            cell2 = ct_or_cell
            ct = cell2.get_celltype()
            if ct is None:
                return  # 既にエラー
        elif type(ct_or_cell) is Celltype:
            cell2 = ct_or_cell.get_singleton_cell(cell.get_region())
            if cell2 is None:
                self.cdl_error(
                    "S1158 $1: singleton cell not found for fixed join",
                    ct_or_cell.get_name(),
                )
                return
            ct = ct_or_cell
        else:
            return  # 既にエラー：無視

        # 結合を生成する
        dbg_print(
            f"create_reverse_require_join {to_s(cell2.get_name())}."
            f"{to_s(self._reverse_require_entry_port_name)}[] = {to_s(cell.get_name())}.{to_s(self._name)}"
        )
        nsp = NamespacePath(cell.get_name(), False, cell.get_namespace())
        rhs = Expression(
            [Y.OP_DOT, [Y.IDENTIFIER, nsp], Token(self._name, None, None, None)],
            cell.get_locale(),
        )  # 1
        join = Join(self._reverse_require_entry_port_name, -1, rhs, cell.get_locale())
        cell2.new_join(join)
        join.set_definition(ct.find(join.get_name()))

    def each_param(self, pr: Any) -> None:
        """signature のすべての関数のすべてのパラメータをたどる。pr(port, func_decl, param_decl)"""
        if self._signature is None:  # signature 未定義（既にエラー）
            return
        fha = self._signature.get_function_head_array()
        if fha is None:  # nil なら文法エラーで有効値が設定されなかった
            return
        port = self
        for fh in fha:  # fh: FuncHead
            fd = fh.get_declarator()  # fd: Decl  (関数頭部からDeclarotorを得る)
            if fd.is_function():  # fd が関数でなければ、すでにエラー
                for par in fd.get_type().get_paramlist().get_items():
                    pr(port, fd, par)

    def is_reverse_required(self) -> bool:  # Ruby: is_reverse_required?
        return self._reverse_require_cell_path is not None

    def is_dynamic(self) -> Any:  # Ruby: is_dynamic?
        return self._b_dynamic

    def is_ref_desc(self) -> Any:  # Ruby: is_ref_desc?
        return self._b_ref_desc

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"Port: name:{to_s(self._name)} port_type:{to_s(self._port_type)} require:{to_s(self._b_require)} "
            f"inline:{to_s(self._b_inline)} omit:{to_s(self._b_omit)} optional:{to_s(self._b_optional)} "
            f"ref_desc:{to_s(self._b_ref_desc)} dynamic:{to_s(self._b_dynamic)}"
        )
        rb_print("  " * (indent + 1))
        if truthy(self._signature):
            rb_puts(f"signature: {to_s(self._signature.get_name())} #<Signature>")
        else:
            rb_puts("signature: NOT defined")
        if type(self._array_size) is str and self._array_size == "[]":
            rb_print("  " * (indent + 1))
            rb_puts("array_size: not specified")
        elif truthy(self._array_size):
            rb_print("  " * (indent + 1))
            rb_puts(f"array_size: {to_s(self._array_size)}")
        if truthy(self._allocator_instance):
            rb_print("  " * (indent + 1))
            rb_puts("allocator instance:")
            for b, a in self._allocator_instance.items():
                rb_print("  " * (indent + 2))
                rb_puts(f"{to_s(a[0])} {to_s(a[1])} {to_s(b)} ")
        rb_print("  " * (indent + 1))
        if self._port_type == Y.CALL:
            rb_puts(
                f"VMT_useless : {to_s(self._b_VMT_useless)}  skelton_useless : {to_s(self._b_skelton_useless)}  "
                f"cell_unique : {to_s(self._b_cell_unique)}"
            )
        else:
            rb_puts(
                f"VMT_useless : {to_s(self._b_VMT_useless)}  skelton_useless : {to_s(self._b_skelton_useless)}"
            )


def _at(lst: list[Any], i: int) -> Any:
    return lst[i] if i < len(lst) else None
