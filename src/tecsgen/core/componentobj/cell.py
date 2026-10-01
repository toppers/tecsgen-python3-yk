"""cell.rb の移植。セル（`Cell`）。

Cell クラスは、1) 普通のセル 2) composite セルタイプのセル 3) composite セルタイプの内側のセル
（@in_composite）を扱う。
"""

from __future__ import annotations

import copy
import re
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context, print_exception
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.plugin_module import PluginModule, PluginNotPorted
from tecsgen.core.syntaxobj.node import NSBDNode
from tecsgen.core.tecsinfo import CellTECSInfo
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    dualmethod,
    gsub,
    rb_integer,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


class Cell(CellTECSInfo, PluginModule, NSBDNode):  # < Nestable
    """@name:: Symbol / @global_name:: Symbol / @local_name:: str
    @celltype:: Celltype | CompositeCelltype / @join_list:: NamedList / @reverse_join_list:: NamedList
    @b_defined / @b_prototype / @b_duplicate / @b_checked:: bool
    @require_joined_list:: {cp_name=>true} / @f_ref:: refercenced from others
    @entry_array_max_subscript:: { @port=>Integer } / @plugin:: Plugin
    @referenced_port_list:: { Port => Integer } / @generate / @generate_list / @b_post_code_generated
    composite: @in_composite / @compositecelltypejoin_list / @f_cloned / @my_clone / @cell_list / @cell_list2
    region: @region / allocator: @alloc_list / ID: @id / @id_specified
    restrict: @restrict_list / @restrict_list2 / @b_restrict_referenced / 受け口 through: @ep_through_list
    """

    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []
    _current_object: ClassVar[Any] = None

    # インスタンス変数（Ruby では nil になり得るもの・型が動的に変わるもの）
    _join_list: Any
    _prev_locale: Any
    _compositecelltypejoin_list: Any
    _locale: Any

    # 定義されたすべてのセル（出現順. namespace に影響されない）
    _cell_list: ClassVar[list[Any]] = []  # type: ignore[misc]  composite の内部のセルを含まない
    _cell_list2: ClassVar[list[Any]] = []  # type: ignore[misc]  composite の内部のセルを含む

    @classmethod
    def reset(cls) -> None:
        Cell._nest_stack_index = -1
        Cell._nest_stack = []
        Cell._current_object = None
        Cell._cell_list = []
        Cell._cell_list2 = []

    @classmethod
    def push(cls) -> None:
        Cell._nest_stack_index += 1
        _set_at(Cell._nest_stack, Cell._nest_stack_index, Cell._current_object)
        Cell._current_object = None

    @classmethod
    def pop(cls) -> None:
        Cell._current_object = _get_at(Cell._nest_stack, Cell._nest_stack_index)
        Cell._nest_stack_index -= 1
        if Cell._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    def __init__(self, ct_path: Any, in_composite: bool = False) -> None:
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.generator import Generator
        from tecsgen.core.syntaxobj.namedlist import NamedList

        super().__init__()
        self._region = Region.get_current()

        # celltype のplugin/存在をチェック
        obj = Namespace.find(ct_path)  # 1
        if obj is None:
            # mikan celltype の名前が不完全 "::ct1ct2" になる
            self.cdl_error("S1027 '$1' celltype not found", ct_path.get_path_str())
        elif type(obj) is not Celltype and type(obj) is not CompositeCelltype:
            self.cdl_error("S1028 '$1' not celltype", ct_path.get_path_str())
        else:
            self._celltype = obj

        self._in_composite = in_composite
        if self._in_composite:
            self._compositecelltypejoin_list = NamedList(
                None, f"in cell '{to_s(self._name)}'"
            )
            self._plugin: Any = None
        else:
            self._compositecelltypejoin_list = None
            self._plugin = Generator.get_plugin()

        Cell._current_object = self
        self._b_defined = False
        self._b_prototype = False
        self._f_ref = False
        self._f_cloned = False
        self._alloc_list: list[Any] = []
        self._id = -1
        self._id_specified: Any = None
        self._b_duplicate = False
        self._b_checked = False
        self._require_joined_list: dict[Any, Any] = {}
        self._entry_array_max_subscript: dict[Any, Any] = {}
        self._referenced_port_list: dict[Any, Any] = {}
        self._restrict_list: dict[Any, Any] = {}
        self._restrict_list2: dict[Any, Any] = {}
        self._b_restrict_referenced = False
        self._b_post_code_generated = False
        self._ep_through_list: list[Any] = []

        # インスタンス変数（クラス変数 @@cell_list とは別物）
        self.__dict__["_cell_list"] = {}
        self.__dict__["_cell_list2"] = []

    @dualmethod
    def set_name(cls, name: Any) -> None:
        Cell._current_object.set_name(name)

    @set_name.instance
    def set_name(self, name: Any) -> None:
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression
        from tecsgen.core.generator import Token
        from tecsgen.core.syntaxobj.namedlist import NamedList

        self._name = name
        self._local_name = name
        if to_s(Namespace.get_global_name()) != "":
            self._global_name = sym(f"{to_s(Namespace.get_global_name())}_{to_s(name)}")
        else:
            self._global_name = name

        # この時点ではプロトタイプか、定義か分らないが、自己参照のために登録
        # set_f_def で再度登録しなおす。Celltype への登録は、end_of_parse で行う
        if self._in_composite:
            cell_prev = CompositeCelltype.find(name)
            if cell_prev is None:
                CompositeCelltype.new_cell_in_composite(self)
        else:
            cell_prev = Namespace.get_current().find(name)
            if cell_prev is None:
                Namespace.new_cell(self)
                self.set_namespace_path()  # @NamespacePath の設定

        if truthy(cell_prev):
            if type(cell_prev) is not Cell:
                self.cdl_error("S1029 $1 mismatch with previous one", name)
            elif self.get_celltype() is not cell_prev.get_celltype():
                self.cdl_error("S1030 $1: celltype mismatch with previous one", name)
            else:
                # region が一致しているか?
                if cell_prev.get_region() is not self.get_region():
                    self.cdl_error(
                        "S1031 $1 region '$2' mismatch  with previous one '$3'",
                        name,
                        self._region.get_name(),
                        cell_prev.get_region().get_name(),
                    )
                Cell._current_object = cell_prev
                # この時点では、まだプロトタイプ宣言か定義か分らない

        self._join_list = NamedList(None, f"in cell '{to_s(self._name)}'")
        self._reverse_join_list: Any = None

        dbg_print(
            f"Cell new_cell: {to_s(self._global_name)} {to_s(self._in_composite)} #<Cell>\n"
        )

        # 内部アロケータを @alloc_list に追加
        if type(self._celltype) is CompositeCelltype:
            for (
                _cell,
                _cp_internal_name,
                port_name,
                fd_name,
                par_name,
                ext_alloc_ent,
            ) in self._celltype.get_internal_allocator_list():
                nsp = NamespacePath(self._name, False)
                rhs = Expression(
                    [
                        Y.OP_DOT,
                        [Y.IDENTIFIER, nsp],
                        Token(sym(to_s(ext_alloc_ent)), None, None, None),
                    ]
                )  # 1 構文解析段階なので locale 不要
                self._alloc_list.append(
                    [Y.NORMAL_ALLOC, port_name, None, fd_name, par_name, rhs]
                )

    @dualmethod
    def new_def(cls) -> None:
        """cell の定義（本体(join)の定義の直前に呼び出される）。"""
        Cell._current_object.new_def()

    @new_def.instance
    def new_def(self) -> None:
        from tecsgen.core.generator import Generator
        from tecsgen.core.syntaxobj.namedlist import NamedList

        self.set_specifier_list(Generator.get_statement_specifier())

        # prototype 指定子ないか
        if not self._b_prototype:
            # 二重定義のチェック
            if self._b_defined is True:
                self.cdl_error("S1032 $1: duplicate cell", self._name)
                prev = self._prev_locale
                dbg_print(
                    f"previous: {to_s(prev[0])}: line {to_s(prev[1])} '{to_s(self._name)}' defined here\n"
                )
                # セルの重複定義エラーの処置  前の定義は捨てる
                self._join_list = NamedList(None, f"in cell '{to_s(self._name)}'")

            self._b_defined = True
            self._prev_locale = self._locale

    @dualmethod
    def new_join(cls, join: Any, b_regular: bool = False) -> None:
        Cell._current_object.new_join(join, b_regular)

    @new_join.instance
    def new_join(self, join: Any, b_regular: bool = False) -> None:
        """新しい結合をチェック（STAGE: P）。

        b_regular:: bool : 通常の場所 (bnf.y.rb)からならば true, それ以外(allocator, require) では false
        """
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.expression import Expression
        from tecsgen.core.syntaxobj.decl import Decl

        join.set_owner(self)

        # composite の新文法対応．
        # composite の中のセルで、attribute の定義である場合
        # cell 内の attr_ext = composite.attr; 構文を処理
        if self._in_composite:
            if truthy(self._celltype):
                if type(self._celltype.find(join.get_name())) is Decl:
                    rhs = join.get_rhs()
                    ident: Any = None
                    if type(rhs) is Expression:
                        ele = rhs.get_elements()
                        if (
                            ele[0] == Y.IDENTIFIER
                        ):  # attr = attr_ext （右辺単項）か？ #1
                            if CompositeCelltype.has_attribute(ele[1].get_name()):
                                ident = ele[1].get_name()  # 右辺は attribute．
                            else:
                                # 右辺は attribute にないのであれば、定数のはず
                                ident = None
                        elif (
                            join.get_rhs().eval_const2(None) is None
                        ):  # 定数式ではないか？
                            # 右辺が、単一のシンボルでない場合、現状は扱えない
                            self.cdl_error(
                                "S1033 rhs expression is not supported. Only attribute is permitted on current version."
                            )
                            return
                        else:
                            ident = None  # 定数は下へ渡す (cell の join にする)

                        if truthy(ident) and truthy(self._celltype.find(ident)):
                            # attr = attr; のような参照はエラー (a = composite.a とする必要がある)
                            self.cdl_error(
                                "S1034 $1 : cannot refer to $2's attribute here. Use 'composite.$3' to refer to composite celltype's",
                                ident,
                                self._celltype.get_name(),
                                ident,
                            )
                    elif type(rhs) is list:
                        if (
                            rhs and rhs[0] == Y.COMPOSITE
                        ):  # 右辺は composite.attr の形式
                            ident = rhs[1].to_sym()
                        else:
                            ident = None  # 右辺は { 10, -10 } の形式
                    else:
                        ident = None  # 右辺は C_EXP の形式

                    # ident が見つかった（右辺は単一の ident）
                    if truthy(ident):
                        # composite の旧文法の構文処理へ渡す．
                        decl = CompositeCelltype.new_join(
                            ident, self._name, join.get_name(), Y.ATTRIBUTE
                        )
                        if type(decl) is not Decl:
                            return
                        ini = decl.get_initializer()
                        if ini is None:
                            return
                        # attribute で指定された初期値を cell の属性として処理させる
                        join.change_rhs(ini)
            else:
                return  # celltype がない．すでにエラー
        elif type(join.get_rhs()) is list:
            rhs = join.get_rhs()
            if rhs and rhs[0] == Y.COMPOSITE:
                # composite の中でないのに attr = composite.attr が使われた
                self.cdl_error(
                    "S1035 composite : cannot specify out of composite celltype definition"
                )
                return

        # 既に左辺が同じ名前の初期化が存在するか？
        j = self._join_list.get_item(
            join.get_name()
        )  # mikan NamespacePath がパスを持っている
        if type(j) is Join:  # mikan ここでは j が Join or Nil 以外は、ないはず
            dbg_print(
                f"add_array_member: {to_s(self._name)} port: {to_s(j.get_port_name())} "
                f"rhs: {to_s(j.get_rhs())}, {to_s(join.get_port_name())} {to_s(join.get_rhs())}\n"
            )
            # 呼び口配列（であると仮定して）要素を追加
            j.add_array_member(join)
        else:
            dbg_print(
                f"new_join: cell={to_s(self._name)} add_item={to_s(join.get_name())}\n"
            )
            self._join_list.add_item(join)

        if not self._in_composite and truthy(join.get_cell()):
            dbg_print(
                f"new_join: {to_s(self._name)} {to_s(self._region.get_name())} => "
                f"{to_s(join.get_cell().get_name())} {join.get_cell().get_region().get_path_string()}\n"
            )

    @dualmethod
    def new_reverse_join(cls, reverse_join: Any) -> None:
        """新しい逆結合。"""
        Cell._current_object.new_reverse_join(reverse_join)

    @new_reverse_join.instance
    def new_reverse_join(self, reverse_join: Any) -> None:
        dbg_print(f"new_reverse_join name={to_s(reverse_join.get_name())}\n")
        b_cb = False
        if truthy(self._celltype):
            ep_name = reverse_join.get_name()
            port = self._celltype.find(ep_name)
            if (
                truthy(port)
                and truthy(port.get_signature())
                and port.get_signature().is_callback()
            ):
                b_cb = True
        if not self._b_prototype and not b_cb:
            self.cdl_error(
                "S9999 '$1': reverse join can be used in prototype cell, or with callback signature",
                self._name,
            )
        if self._reverse_join_list is None:
            self._reverse_join_list = [reverse_join]
        else:
            self._reverse_join_list.append(reverse_join)

    @dualmethod
    def create_reverse_join(cls) -> None:
        """reverse_join を生成する。"""
        for c in Cell._cell_list:
            ct = c.get_celltype()
            if truthy(ct):
                c.create_reverse_join()

    @create_reverse_join.instance
    def create_reverse_join(self) -> None:
        """逆結合から結合を生成（STAGE: S）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression

        if self._b_checked:
            return

        if truthy(self._reverse_join_list):
            for rj in self._reverse_join_list:
                # 逆結合の情報を得る
                ep_name = rj.get_name()
                ep_subscript, cp_cell_nsp, cp_name, cp_subscript = (
                    rj.get_rhs_cell_and_port()
                )

                # 呼び口側のセルと、そのセルタイプ
                if not self._in_composite:
                    cell = Namespace.find(cp_cell_nsp)
                else:
                    cell = CompositeCelltype.find(sym(to_s(cp_cell_nsp)))

                if type(cell) is not Cell:
                    self.cdl_error(
                        "S9999 '$1': not cell for reverse join",
                        cp_cell_nsp.get_path_str(),
                    )
                    continue
                ct = cell.get_celltype()
                if ct is None:
                    continue

                if not self._in_composite:
                    ep_cell_nsp = self.get_namespace_path()
                    ep_cell_nsp_str = ep_cell_nsp.get_path_str()
                else:
                    ep_cell_nsp = NamespacePath(self._name, False)
                    ep_cell_nsp_str = self._name
                ep_subscript_val = (
                    ep_subscript.eval_const(None) if truthy(ep_subscript) else None
                )
                rhs = Expression.create_cell_join_expression(
                    ep_cell_nsp, ep_subscript_val, ep_name, rj.get_locale()
                )
                join = Join(cp_name, cp_subscript, rhs, rj.get_locale())
                cell.new_join(join)
                ss_str = f"[{to_s(cp_subscript)}]" if truthy(cp_subscript) else ""
                dbg_print(
                    f"create_reverse_join: {to_s(cell.get_name())}.{to_s(cp_name)}{ss_str} => "
                    f"{to_s(ep_cell_nsp_str)}.{to_s(ep_name)}\n"
                )

    @dualmethod
    def external_join(
        cls, internal_cell_elem_name: Any, export_name: Any, b_composite: Any
    ) -> Any:
        return Cell._current_object.external_join(
            internal_cell_elem_name, export_name, b_composite
        )

    @external_join.instance
    def external_join(
        self, internal_cell_elem_name: Any, export_name: Any, b_composite: Any
    ) -> Any:
        """cell 内に記述する呼び口の外部結合（composite の中の cell でしか呼ばれない）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        # cCall => composite.cCall; ではないか？
        if b_composite is False and truthy(self._celltype.find(export_name)):
            # cCall => cCall; のような場合
            self.cdl_error(
                "S1036 $1 : cannot refer to $2's here. Use 'composite.$3' to refer to composite celltype's",
                export_name,
                self._celltype.get_name(),
                export_name,
            )
        # composite の旧文法における、cell 外の cCall = Cell.cCall; の構文処理に渡す
        return CompositeCelltype.new_join(
            export_name, self._name, internal_cell_elem_name, Y.CALL
        )

    @dualmethod
    def end_of_parse(cls, f_def: Any) -> Any:
        cell = Cell._current_object
        cell.end_of_parse(f_def)
        Cell._current_object = None
        return cell

    @end_of_parse.instance
    def end_of_parse(self, f_def: Any) -> None:
        from tecsgen.core.generator import Generator
        from tecsgen.core.tecsgen import TECSGEN

        if self._b_prototype:  # prototype 指定子あったか?
            f_def = False  # プロトタイプ宣言とする
            self._b_prototype = False
        if f_def is False:
            # cell tCelltype Cell; の形式の場合
            self.set_specifier_list(Generator.get_statement_specifier())
        if TECSGEN.is_post_coded():
            self._b_post_code_generated = True
        self.set_f_def(f_def)

        if truthy(self._generate):
            self.cell_plugin()

    def set_f_def(self, f_def: Any) -> None:
        """プロトタイプ宣言(false)か定義(true)かを設定（構文解釈の最後に呼出される）。"""
        if not truthy(f_def):
            return

        if not self._in_composite:
            if truthy(self._celltype):  # composite でも呼びだす, エラー時 nil
                self._celltype.new_cell(self)
            Cell._cell_list.append(self)

    def set_f_ref(self) -> None:
        dbg_print(f"set_f_ref: {to_s(self._global_name)}\n")
        self._f_ref = True

        # composite の内部セルを参照されたことにする
        if truthy(self._cell_list):
            for _cn, cell in _each_pair(self._cell_list):
                cell.set_f_ref()

    def set_specifier_list(self, spec_list: Any) -> None:
        """cell の指定子を設定（STAGE:  B）。

        spec_list:: [ :ALLOCATOR, [ [ :NORMAL_ALLOC, ep_name, subscript, func_name, param_name, expr ], ... ] ]
        """
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.expression import Expression
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        if spec_list is None:  # 空ならば何もしない
            return

        dbg_print(f"set_spec_list: {to_s(self._name)}\n")
        b_generate = False  # generate が指定された

        for s in spec_list:
            s0 = s[0]  # statement_specifier
            if s0 == Y.ALLOCATOR:  # [allocator(ePort.func.param=allocCell.eA,...)]
                for a in s[
                    1
                ]:  # alloc_list : allocator の内部の ',' で区切られた部分の配列
                    cp_name = sym(f"{to_s(a[1])}_{to_s(a[3])}_{to_s(a[4])}")
                    if truthy(a[2]):
                        subscript = a[2].eval_const(None)
                        a[2] = subscript
                    else:
                        subscript = None
                    # アロケータ呼び口の結合を生成
                    join = Join(
                        cp_name, subscript, a[5]
                    )  # 構文解析段階なので locale 不要
                    dbg_print(
                        f"new allocator join {to_s(cp_name)} {to_s(subscript)} {to_s(a[5])}\n"
                    )
                    Cell.new_join(join)
                    self._alloc_list.append(a)
            elif s0 == Y.ID:  # [id(0)]
                if type(s[1]) is not Expression:
                    self.cdl_error("S1160 $1 must be constant for id", to_s(s[1]))
                else:
                    cid = s[1].eval_const(None)
                    if cid is None or rb_integer(cid) != cid:
                        self.cdl_error("S1161 $1 must be constant for id", to_s(s[1]))
                    elif cid == 0:
                        self.cdl_error("S1162 $1: id cannot be 0", to_s(s[1]))
                    else:
                        self._id_specified = cid
            elif s0 == Y.GENERATE:  # [generate(CellPlugin,"option")]
                if truthy(self._generate):
                    self.cdl_error("S1163 generate specifier duplicate")
                self._generate = [s[1], s[2]]  # [ PluginName, "option" ]
                b_generate = True
            elif s0 == Y.PROTOTYPE:  # [prototype]
                self._b_prototype = True
            elif s0 == Y.RESTRICT:  # [restrict]
                for re_ in s[1]:
                    self.add_restrict(re_[0], re_[1], re_[2])
            elif s0 == Y.THROUGH:  # [through(ThroughPlugin,"option")]
                ep_name = s[1].to_sym()
                plugin_name = s[2]
                option = CDLString.remove_dquote(to_s(s[3]))
                dbg_print(
                    f"through: celltype={to_s(self._celltype.get_name())} ep_name={to_s(ep_name)}\n"
                )
                if self._celltype.find(ep_name) is None:
                    self.cdl_error("S9999 '$1' entry port not exist", ep_name)
                self._ep_through_list.append([ep_name, plugin_name, option])
            else:
                self.cdl_error("S1039 '$1': unknown specifier for cell", s0)
        if self._b_prototype:
            if b_generate:
                self.cdl_error(
                    "S9999 '$1': generate and prototype specified simultaneously",
                    self._name,
                )
            if self._b_defined:
                self.cdl_error(
                    "S9999 '$1': prototype specified after definition", self._name
                )

    def get_allocator_list(self) -> list[Any]:
        # 意味チェック(set_definition)されていない？
        # relay アロケータの場合、セルの意味チェックが行われていないと、@alloc_list が完成しない
        if self._b_checked is False:
            self.set_definition_join()
        return self._alloc_list

    def get_specified_id(self) -> Any:
        return self._id_specified

    def set_specified_id(self, cid: Any) -> None:
        """id 指定子の値を設定（プラグインで cell の生成順序を制御したい場合のために設けた）。"""
        if rb_integer(cid) != cid or cid <= 0:
            self.cdl_error(
                "S1164 '$1' set_specified_id: id not positive integer '$2'",
                self._name,
                cid,
            )
        elif truthy(self._id_specified):
            self.cdl_error("S1165 '$1' set_specified_id: id duplicate", self._name)
        else:
            self._id_specified = cid

    def cell_plugin(self) -> None:
        """セルプラグイン (generate 指定子)。"""
        plugin_name = self._generate[0]
        option = self._generate[1]
        result = self.apply_plugin(plugin_name, option)
        while len(self._generate) < 3:
            self._generate.append(None)
        self._generate[2] = result

    def apply_plugin(self, plugin_name: Any, option: Any) -> Any:
        if not self._b_defined:
            self.cdl_error(
                "S9999 plugin cannot apply to prototype cell '$1'", self._name
            )

        pl_class = self.load_plugin(plugin_name, "CellPlugin")
        if get_context().verbose:
            rb_print(
                f"new cell plugin: plugin_object = Class.new( "
                f"{to_s(self._name)}, {to_s(option)} )\n"
            )

        plugin_object = None
        try:
            plugin_object = pl_class(self, option)
            plugin_object.set_locale(self._locale)
            self.generate_and_parse(plugin_object)
        except PluginNotPorted:
            raise
        except Exception as evar:  # noqa: BLE001  Ruby の rescue Exception
            self.cdl_error("S1166 $1: fail to new", plugin_name)
            print_exception(evar)
        return plugin_object

    def add_compositecelltypejoin(self, join: Any) -> None:
        self._compositecelltypejoin_list.add_item(join)

    def get_compositecelltypejoin_by_cell_elem_name(self, cell_elem_name: Any) -> Any:
        for cj in self._compositecelltypejoin_list.get_items():
            if cj.get_cell_elem_name() == cell_elem_name:
                return cj
        return None

    def clone_for_composite(
        self,
        name: Any,
        global_name: Any,
        namespacePath: Any,
        join_array: list[Any],
        ct_name: Any,
        region: Any,
        plugin: Any,
        locale: Any,
    ) -> Cell:
        """cell を composite セルタイプのセル用に clone する（CompositeCelltype の expand から呼出される）。"""
        from tecsgen.core.componentobj.celltype import Celltype

        dbg_print(
            f"  CLONING Cell#clone_for_composite : cloning: {to_s(self._name)} {to_s(global_name)}  "
            f"b_defined={to_s(self._b_defined)} #<Cell>=>#<Cell> \n"
        )
        dbg_print(
            f"              my_name={to_s(self._name)} name={to_s(name)} owner class={to_s(type(self._owner))}\n"
        )

        self._my_clone = copy.copy(self)

        # clone したセルの内部に持つ名前情報を調整する
        self._my_clone.set_cloned(
            name,
            global_name,
            namespacePath,
            join_array,
            ct_name,
            region,
            plugin,
            locale,
        )

        # @celltype == nil は以前にセルタイプ未定義エラー
        if (
            self._b_defined is True
            and self._celltype is not None
            and type(self._celltype) is Celltype
        ):
            # celltype に登録（コード生成の対象となる）
            self._celltype.new_cell(self._my_clone)

        return self._my_clone

    def set_cloned(
        self,
        name: Any,
        global_name: Any,
        namespacePath: Any,
        join_array: list[Any],
        parent_ct_name: Any,
        region: Any,
        plugin: Any,
        locale: Any,
    ) -> None:
        """clone されたセルの内部に持つ名前情報を調整する。"""
        dbg_print(
            f"cell.set_cloned : global_name: {to_s(global_name)}  name: {to_s(name)}  @name: {to_s(self._name)}\n"
        )
        dbg_print(
            f"set_cloned:  entry_array_max_subscript.len={len(self._entry_array_max_subscript)}\n"
        )
        self._global_name = sym(f"{to_s(global_name)}_{to_s(self._name)}")
        self._name = sym(f"{to_s(name)}_{to_s(self._name)}")
        self._NamespacePath = namespacePath.change_name(self._name)
        self._region = region
        self._plugin = plugin
        self._locale = locale

        self._in_composite = False
        self._b_checked = False
        self._f_cloned = True

        region.new_cell(self)  # mikan  namespace に cell を置けないことを仮定

        # join_list : NamedList の clone を作る
        if truthy(self._celltype):
            dbg_print(
                f"set_cloned: celltype={to_s(self._celltype.get_name())} name={to_s(self._name)} "
                f"global_name={to_s(global_name)} region={to_s(region.get_name())}\n"
            )
        self._join_list = self._join_list.clone_for_composite(
            parent_ct_name, global_name, locale
        )
        self._referenced_port_list = {}

        self._alloc_list = []
        self._require_joined_list = {}
        self._entry_array_max_subscript = dict(self._entry_array_max_subscript)
        self.__dict__["_cell_list"] = {}
        self.__dict__["_cell_list2"] = []

        # このセルのグローバル名を与える（C_EXP の$id$ 置換はこのセルの名前になる）
        for j in join_array:
            self._join_list.change_item(j)

    def expand_inner(self) -> None:
        """clone されたセルが composite の場合、内部セルを展開する。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if not self._f_cloned:
            raise RubyRuntimeError("expnad_inner: not cloned cell")

        # clone しようとするセルが composit セルタイプ？
        if type(self._celltype) is CompositeCelltype:
            # composite cell を再帰的に展開
            cl, cl2 = self._celltype.expand(
                self._name,
                self._global_name,
                self._NamespacePath,
                self._join_list,
                self._region,
                self._plugin,
                self._locale,
            )
            self.__dict__["_cell_list"] = cl
            self.__dict__["_cell_list2"] = cl2

    def change_rhs_port(self, cloned_cell_list: Any) -> None:
        """clone された cell の join_list の右辺の変更（呼び口の右辺の cell を他の clone された cell に置換え）。"""
        dbg_print(f"=====   Cell#change_rhs_port: name={to_s(self._name)}   =====\n")
        for j in self._join_list.get_items():
            j.change_rhs_port(cloned_cell_list, self._celltype)

    def get_f_def(self) -> Any:
        return self._b_defined

    def get_f_ref(self) -> bool:
        return bool(truthy(self._f_ref))

    def get_name(self) -> Any:
        return self._name

    def get_local_name(self) -> Any:
        return self._local_name

    def get_global_name(self) -> Any:
        return self._global_name

    def get_region(self) -> Any:
        return self._region

    def get_domain_class_root(self) -> Any:
        dr = self._region.get_domain_root()
        cr = self._region.get_class_root()
        if dr.is_sub_region_of(cr):
            return dr
        return cr

    def get_ep_through_list(self) -> list[Any]:
        dbg_print(
            f"Cell#get_ep_through_list: name={to_s(self._name)} len={len(self._ep_through_list)}\n"
        )
        return self._ep_through_list

    @classmethod
    def get_current(cls) -> Any:
        return Cell._current_object

    def is_generate(self) -> bool:  # Ruby: is_generate?
        """最適化、コード生成中に、対象となる region に属する場合 true を返す。"""
        generating_region = get_context().generating_region
        if generating_region is None:
            # 構文解釈、意味解析段階で呼ばれると例外発生
            raise RubyRuntimeError("is_generate? called before optimizing")
        return generating_region is self._region.get_link_root()

    def is_cloned(self) -> Any:  # Ruby: is_cloned?
        """composite 内部の複製されたセルか？"""
        return self._f_cloned

    def is_in_composite(self) -> Any:  # Ruby: is_in_composite?
        return self._in_composite

    def is_of_composite(self) -> bool:  # Ruby: is_of_composite?
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        return isinstance(self._celltype, CompositeCelltype)

    def post_code_generated(self) -> Any:  # Ruby: post_code_generated?
        return self._b_post_code_generated

    def _inner_cell(self, cj: Any) -> Any:
        """@cell_list[ "#{cj.get_cell_name}" ]（String のキーで引く）。"""
        return self.__dict__["_cell_list"].get(to_s(cj.get_cell_name()))

    def get_real_global_name(self, port_name: Any) -> Any:
        """composite cell の port に対応する内部の cell の port の名前（リンク時に必要な名前）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port_name)
            return _call(
                self._inner_cell(cj), "get_real_global_name", cj.get_cell_elem_name()
            )
        dbg_print(f"  get_real_global_name: cell name: {to_s(self._global_name)}\n")
        return self._global_name

    def get_real_global_port_name(self, port_name: Any) -> Any:
        """セルの受け口 port_name に対する実際のセル名、受け口名を '_' で連結。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port_name)
            return _call(
                self._inner_cell(cj),
                "get_real_global_port_name",
                cj.get_cell_elem_name(),
            )
        dbg_print(f"get_real_global_port_name:  cell name: {to_s(self._global_name)}\n")
        return f"{to_s(self._global_name)}_{to_s(port_name)}"

    def get_real_port(self, port_name: Any) -> Any:
        """PORT (celltype の定義) を得る。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port_name)
            return _call(self._inner_cell(cj), "get_real_port", cj.get_cell_elem_name())
        return self._celltype.find(port_name)

    def get_real_cell(self, port_name: Any) -> Any:
        """cell を得る（composite でなければ自分自身を返す）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port_name)
            return _call(self._inner_cell(cj), "get_real_cell", cj.get_cell_elem_name())
        return self

    def get_real_celltype(self, port_name: Any) -> Any:
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            return self._celltype.get_real_celltype(port_name)
        return self._celltype

    def port_referenced(self, port: Any) -> None:
        """受け口のport の参照カウントをアップする。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if truthy(self._referenced_port_list.get(port)):
            self._referenced_port_list[port] += 1
        else:
            self._referenced_port_list[port] = 1

        # composite か？
        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port.get_name())
            dbg_print(
                f" port_referenced: {to_s(self._celltype.get_name())} {to_s(self._name)} "
                f"cj={to_s(cj.get_name()) if truthy(cj) else 'nil'}\n"
            )
            if truthy(cj):  # 既にエラー
                cell = self._inner_cell(cj)
                if truthy(cell) and truthy(cell.get_celltype()):
                    cell.port_referenced(
                        cell.get_celltype().find(cj.get_cell_elem_name())
                    )

    def get_internal_port_name(self, port_name: Any) -> Any:
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if type(self._celltype) is CompositeCelltype:
            cj = self._celltype.find_export(port_name)
            return cj.get_cell().get_internal_port_name(cj.get_cell_elem_name())
        dbg_print(
            f"  get_global_port_name: cell port: {to_s(self._global_name)}_{to_s(port_name)}\n"
        )
        return f"{to_s(self._global_name)}_{to_s(port_name)}"

    def get_attr_initializer(self, attr_name: Any) -> Any:
        """属性の初期値を得る（必ず初期化されていないと Ruby 例外となる）。"""
        val = self._join_list.get_item(attr_name)
        if val is None:
            return _call(self._celltype.find(attr_name), "get_initializer")
        return val.get_rhs()

    def get_celltype(self) -> Any:
        return self._celltype

    def get_join_list(self) -> Any:
        return self._join_list

    def set_id(self, cid: Any) -> None:
        self._id = cid

    def get_id(self) -> Any:
        return self._id

    def get_plugin(self) -> Any:
        return self._plugin

    @dualmethod
    def get_cell_list2(cls) -> list[Any]:
        """@@cell_list2 を得る（composite 内を含む。意味解析後に作成される）。"""
        return Cell._cell_list2

    @get_cell_list2.instance
    def get_cell_list2(self) -> list[Any]:
        lst: list[Any] = []
        for cell in self._cell_list2:
            lst.append(cell)
            lst = lst + cell.get_cell_list2()
        return lst

    def set_entry_port_max_subscript(self, port: Any, num: int) -> None:
        """受け口配列の添数の最大値を設定。"""
        dbg_print(
            f"set_entry_port_max_subscript: {to_s(self._name)}.{to_s(port.get_name())}: {num}\n"
        )
        subscript = self._entry_array_max_subscript.get(port)

        if subscript is None or num > subscript:
            self._entry_array_max_subscript[port] = num
            self.set_entry_inner_port_max_subscript(port, num)

    def set_entry_inner_port_max_subscript(self, port: Any, num: int) -> None:
        """composite の内側セルの受け口配列の添数の最大値を設定。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if self._cell_list is None:
            return  # プロトタイプ宣言しかされていなくて、内側セルが展開されていない　or composite 展開前

        # composite の内側のセルに伝播
        if type(self._celltype) is CompositeCelltype:
            dbg_print(
                f"set_entry_inner_port_max_subscript {to_s(self._name)} {to_s(self._port)} {num} "
                f"cell_list.len={len(self._cell_list)}\n"
            )
            cj = self._celltype.find_export(port.get_name())
            if truthy(cj) and truthy(self._inner_cell(cj)):
                inner_cell = self._inner_cell(cj)
                ct = inner_cell.get_celltype()
                if truthy(ct):
                    inner_port = ct.find(cj.get_cell_elem_name())
                    inner_cell.set_entry_port_max_subscript(inner_port, num)

    def get_entry_port_max_subscript(self, port: Any) -> int:
        """受け口配列の添数の最大値を返す（1つもない場合は -1）。"""
        subscript = self._entry_array_max_subscript.get(port)
        if subscript is None:
            subscript = -1
        return subscript

    def create_relay_allocator_join(self) -> None:
        """リレーアロケータの結合を生成（STAGE: S。呼び口側の結合を元に受け口側の結合を生成）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.join import Join

        # celltype がなければチェックしない（既にエラー）
        if self._celltype is None:
            return

        # relay allocator を生成
        for p in self._celltype.get_port_list():
            ail = p.get_allocator_instance()
            if not truthy(ail):
                continue
            dbg_print(
                f"create_relay_allocator_join: {to_s(self._name)}, {to_s(p.get_name())}\n"
            )
            if truthy(p.get_array_size()):
                # mikan relay allocator が array に対応できてもよいのでは？
                self.cdl_error("S1040 array not supported for relay allocator")
                continue
            for name, ai2 in list(ail.items()):
                # ai2 = [ :INTERNAL_ALLOC|:RELAY_ALLOC, func_name, param_name, rhs_cp_name, rhs_func_name, rhs_param_name ]
                if ai2[0] != Y.RELAY_ALLOC:
                    continue
                dbg_print(
                    f"create_relay_allocator_join: {to_s(self._name)}, {to_s(name)}\n"
                )
                relay_name = sym(f"{to_s(ai2[3])}_{to_s(ai2[4])}_{to_s(ai2[5])}")
                # 呼び口側の結合を取り出す
                ja = self._join_list.get_item(relay_name)
                if ja is None:
                    # 見つからない場合
                    found = False

                    # composite 内で外部に結合されているか
                    if self._in_composite:
                        for cj in self._compositecelltypejoin_list.get_items():
                            dbg_print("create relay_allocator in_composite\n")
                            dbg_print(
                                f"    {to_s(cj.get_cell_name())} {to_s(self._name)} "
                                f"{to_s(cj.get_cell_elem_name())} {to_s(relay_name)}\n"
                            )
                            if (
                                cj.get_cell_name() == self._name
                                and cj.get_cell_elem_name() == relay_name
                            ):
                                found = True
                                dbg_print(
                                    f"create_relay_allocator: found {to_s(cj.get_cell_elem_name())}\n"
                                )
                                break

                    if found is False:
                        self.cdl_error(
                            "S1041 '$1_$2_$3': not joined. cannot create internal join for relay allocator",
                            ai2[3],
                            ai2[4],
                            ai2[5],
                        )
                    continue  # 打ち切る

                b_export = False
                # composite 内のセルでエクスポートされているかチェック
                if truthy(self._compositecelltypejoin_list):
                    for cj in self._compositecelltypejoin_list.get_items():
                        # 属性名と composite の export する名前は一致するか
                        if p.get_name() == cj.get_cell_elem_name():
                            b_export = True  # 属性は export されているので、とりあえず未初期化とはしない
                            break

                # mikan 配列（Ruby 版は am = nil 固定なので、配列の分岐は通らない）
                if b_export is False:
                    # CompositeCelltype の場合、内側のセルで生成させる
                    join_name = sym(
                        f"{to_s(p.get_name())}_{to_s(ai2[1])}_{to_s(ai2[2])}"
                    )
                    join = Join(join_name, None, ja.get_rhs(), self._locale)
                    self.new_join(join)
                    join.set_definition(self._celltype.find(join.get_name()))
                    if type(self._celltype) is CompositeCelltype:
                        jr = self._join_list.get_item(relay_name)
                        if (
                            jr.get_rhs_cell2() is not join.get_rhs_cell2()
                            or jr.get_rhs_port2() != join.get_rhs_port2()
                        ):
                            self.cdl_error(
                                "S1167 '$1': relay mismatch '$2'",
                                f"{to_s(p.get_name())}_{to_s(ai2[1])}_{to_s(ai2[2])}",
                                f"{to_s(ai2[3])}_{to_s(ai2[4])}_{to_s(ai2[5])}",
                            )
                        else:
                            dbg_print(
                                f"relay success:  {to_s(p.get_name())}_{to_s(ai2[1])}_{to_s(ai2[2])}=>"
                                f"{to_s(relay_name)} {to_s(jr.get_rhs_cell2().get_name())}.{to_s(jr.get_rhs_port2())} \n"
                            )
                self._alloc_list.append(
                    [Y.NORMAL_ALLOC, p.get_name(), None, ai2[1], ai2[2], ja.get_rhs()]
                )
                dbg_print(
                    f"create_relay_allocator_join: {to_s(p.get_name())}_{to_s(ai2[1])}_{to_s(ai2[2])} "
                    f"{to_s(relay_name)}\n"
                )

    @classmethod
    def make_cell_list2(cls) -> None:
        """@@cell_list2 を作る（出現順に composite 内を含むセルのリスト）。"""
        for c in Cell._cell_list:
            Cell._cell_list2.append(c)
            Cell._cell_list2 = Cell._cell_list2 + c.get_cell_list2()

    @classmethod
    def get_cell_list(cls) -> list[Any]:
        """@@cell_list を得る（composite の中を含まない）。"""
        return Cell._cell_list

    @classmethod
    def create_reverse_require_join(cls) -> None:
        """reverse_require_join を生成する。"""
        for c in Cell._cell_list2:
            ct = c.get_celltype()
            if truthy(ct):
                # self への呼び口側の結合を生成
                ct.create_reverse_require_join(c)

    def set_port_reference_count(self) -> None:
        """受け口のport の参照カウントを設定する（self は呼び元のセル）。"""
        from tecsgen.core.componentobj.port import Port

        for j in self._join_list.get_items():
            if type(j.get_definition()) is not Port:
                continue
            am = j.get_array_member2()
            if truthy(am):  # 呼び口配列
                for j2 in am:
                    if j2 is None:  # optional で一部が欠落しているケース
                        continue
                    cell = j2.get_rhs_cell2()
                    if cell is None:  # 右辺が見つからなかった．既にエラー
                        continue
                    port = cell.get_celltype().find(j2.get_rhs_port2())
                    dbg_print(
                        f"set_port_reference_count: {to_s(self._name)}.{to_s(j2.get_name())} => "
                        f"{to_s(cell.get_name())}.{to_s(port.get_name())}\n"
                    )
                    cell.port_referenced(port)
            else:
                cell = j.get_rhs_cell2()
                if (
                    cell is None or cell.get_celltype() is None
                ):  # 右辺が見つからなかった
                    continue
                port = cell.get_celltype().find(j.get_rhs_port2())
                if port is None:
                    dbg_print(
                        f"set_port_ref: {to_s(self._name)}.{to_s(j.get_name())} = "
                        f"{to_s(cell.get_name())}.{to_s(j.get_rhs_port2())}\n"
                    )
                    # through プラグインで生成されたセルの受け口が見つからないケース (のハズ)
                    self.cdl_error(
                        "entry '$1' not found in '$2' refered from $3.$4",
                        j.get_rhs_port2(),
                        cell.get_name(),
                        self._name,
                        j.get_name(),
                    )
                    continue
                dbg_print(
                    f"set_port_reference_count: {to_s(self._name)}.{to_s(j.get_name())} => "
                    f"{to_s(cell.get_name())}.{to_s(port.get_name())}\n"
                )
                cell.port_referenced(port)

    def check_join(self) -> None:
        """結合(Join)のチェック（呼び口の結合または attribute の初期化）。"""
        from tecsgen.core.cdl_types import PtrType
        from tecsgen.core.componentobj.compositecelltypejoin import (
            CompositeCelltypeJoin,
        )
        from tecsgen.core.expression import Expression
        from tecsgen.core.syntaxobj.decl import Decl

        # celltype がなければチェックしない（既にエラー）
        if self._celltype is None:
            return
        if self._b_defined is False:
            return
        if (
            self._f_cloned is True
        ):  # 内部セルについては、composite の定義時にチェックされている
            return

        # 未結合の呼び口のチェック
        for p in self._celltype.get_port_list():
            # 呼び口でなければ、チェックしない
            if p.get_port_type() != Y.CALL:
                continue

            dbg_print(
                f"check_join: {to_s(self._name)} {to_s(self.get_celltype().get_name())} {to_s(p.get_name())}\n"
            )

            # 結合リストの中から呼び口名に一致するものを取りだす
            j = self._join_list.get_item(p.get_name())

            if j is None:
                # 未結合の呼び口
                found = False
                if self._in_composite:
                    # composite celltype の export するものすべてから探す
                    for cj in self._compositecelltypejoin_list.get_items():
                        if p.get_name() == cj.get_cell_elem_name():
                            found = True

                # 呼び口配列の場合 optional で全ての要素が初期化されない場合に、ここへ来る
                if not found and not p.is_require() and not p.is_optional():
                    if not p.is_allocator_port():
                        self.cdl_error(
                            "S1042 call port '$1' not initialized in cell '$2'",
                            p.get_name(),
                            self._name,
                        )
                    else:
                        self.cdl_error(
                            "S1043 call port '$1' not initialized in cell '$2'. this call port is created by tecsgen. check allocator specifier",
                            p.get_name(),
                            self._name,
                        )
            elif _is_int(p.get_array_size()):
                # 添数あり呼び口配列の場合、すべての添数要素が初期化されているかチェックする
                am = j.get_array_member2()
                if truthy(am):
                    # 呼び口配列定義での配列の大きさ
                    length = p.get_array_size()

                    # 配列の大きさが呼び口配列定義と結合定義で一致するか？
                    if len(am) != length:
                        if not p.is_optional() or len(am) >= length:
                            # optional の場合、要素数が少なすぎるのは OK
                            self.cdl_error(
                                "S1044 $1: array initializer too many or few, $2 for $3",
                                p.get_name(),
                                len(am),
                                length,
                            )
                        # am の要素に nil を追加しておく (#_CPA_# のコード生成時、この配列要素数分生成)
                        i = len(am)
                        while i < length:
                            am.append(None)
                            i += 1

                    i = 0
                    while i < length:
                        if _at(am, i) is None:
                            if not p.is_optional():
                                self.cdl_error(
                                    "S1045 $1[$2]: not initialized", p.get_name(), i
                                )
                        elif not self._in_composite:
                            # 生成されないリージョンへの結合かチェック
                            am[i].check_region2()
                        i += 1
            elif truthy(j.get_array_member()):
                # 添数なし呼び口配列の場合
                am = j.get_array_member2()
                length = len(am)
                i = 0
                while i < length:
                    if am[i] is None and not p.is_optional():
                        self.cdl_error("S1046 $1[$2]: not initialized", p.get_name(), i)
                    i += 1

                # 生成されないリージョンへの結合かチェック
                if not self._in_composite:
                    for join in am:
                        if truthy(join):
                            join.check_region2()
            elif not self._in_composite:
                # 呼び口［配列」でない場合  生成されないリージョンへの結合かチェック
                j.check_region2()

        # ポインタ型が配列で初期化される場合のチェック
        for a in self._celltype.get_attribute_list() + self._celltype.get_var_list():
            if truthy(a.get_size_is()):
                if type(a) is CompositeCelltypeJoin:
                    continue  # 既にエラーになっている

                if not isinstance(a.get_type(), PtrType):
                    self.cdl_error(
                        "S1048 $1: size_is specified for non-pointer type", a.get_name()
                    )
                else:
                    size = a.get_size_is().eval_const(
                        self._join_list, self._celltype.get_name_list()
                    )
                    a.get_type().set_scs(a.get_size_is(), None, None, None, False)
                    if not _is_int(size):  # C_EXP の可能性あり
                        self.cdl_error(
                            "S1049 $1: size_is arg not constant", a.get_name()
                        )
                    else:
                        j = self._join_list.get_item(a.get_identifier())
                        if truthy(j):
                            ini = j.get_rhs()
                            if truthy(ini):
                                if type(ini) is not list:
                                    self.cdl_error(
                                        "S1050 unsuitable initializer, need array initializer"
                                    )
                                elif size < len(ini):
                                    self.cdl_error(
                                        "S1051 too many initializer for array, $1 for $2",
                                        len(ini),
                                        size,
                                    )
                        else:
                            # size_is 引数がセルで指定されていて、初期化子がセルタイプで指定されているケースのチェック
                            ini = a.get_initializer()
                            if type(ini) is Expression:
                                ini = ini.eval_const(self._celltype.get_name_list())
                            if type(ini) is list and len(ini) > size:
                                self.cdl_error(
                                    "S1168 too many initializer for array, $1 for $2",
                                    len(ini),
                                    size,
                                )
            elif type(a) is not CompositeCelltypeJoin and isinstance(
                a.get_type(), PtrType
            ):
                # composite は size_is 指定できない
                j = self._join_list.get_item(a.get_identifier())
                if truthy(j) and type(j.get_rhs()) is list:
                    # size_is 指定されていないポインタが Array で初期化されていたら、エラーとする
                    self.cdl_error(
                        "S1169 $1: non-size_is pointer cannot be initialized with array initializer",
                        a.get_identifier(),
                    )

        # 未初期化の属性をチェック
        for a in self._celltype.get_attribute_list():
            b_init = False
            if truthy(a.get_initializer()) or truthy(
                self._join_list.get_item(a.get_name())
            ):  # セルタイプで初期化されている
                b_init = True
            elif self._in_composite and truthy(self._compositecelltypejoin_list):
                # 属性が export されているか調べる。export されていれば未初期化とはしない
                for cj in self._compositecelltypejoin_list.get_items():
                    if sym(a.get_name()) == sym(cj.get_cell_elem_name()):
                        b_init = True
                if b_init and truthy(a.get_size_is()):
                    self._check_exported_size_is(a, Decl)

            if b_init is False:
                self.cdl_error(
                    "S1052 attribute '$1' not initialized in cell '$2'",
                    a.get_name(),
                    self._name,
                )

    def _check_exported_size_is(self, a: Any, decl_cls: type) -> None:
        """内部セルの size_is をエクスポートする size_is とマッチするかチェックする。"""
        cj = self._compositecelltypejoin_list.get_item(sym(a.get_name()))
        if type(cj.get_port_decl()) is not decl_cls:
            return  # else cj は Port (既にエラー)
        # cj_size_is は、外部公開される attr の size_is
        cj_size_is = cj.get_port_decl().get_size_is()
        if cj_size_is is None:
            self.cdl_error(
                "S1170 '$1' has size_is but export attr '$2' doesn't have",
                a.get_name(),
                cj.get_name(),
            )
        exprs = to_s(a.get_size_is())
        remain: Any = exprs
        inner_to_export: dict[Any, Any] = {}
        # exprs に含まれる識別子を抜き出し、対応する export される名前を探す
        while remain != "" and remain is not None:
            m = re.search(r"([^\w]*)([_A-Za-z][\w\d]*)", remain, re.ASCII)
            if m is None:
                break
            arg_name = sym(m.group(2))
            remain = remain[m.end() :]
            # size_is に含まれる変数は、composite で export されているか
            cj2 = None
            for cj2t in self._compositecelltypejoin_list.get_items():
                if cj2t.get_cell_elem_name() == arg_name:
                    cj2 = cj2t
            if cj2 is None:
                self.cdl_error(
                    "S1171 '$1' size_is argument of '$2' not exported",
                    a.get_name(),
                    cj.get_name(),
                )
                continue
            if type(cj2.get_port_decl()) is decl_cls:
                decl2 = cj2.get_port_decl()
                # 内部の名前と外部の名前の対応関係を記憶
                inner_to_export[arg_name] = decl2.get_name()
        # 内部の名前を外部の名前で置換
        for arg_name, exp_name in inner_to_export.items():
            exprs = gsub(
                re.compile(f"{to_s(arg_name)}(\\W)"), to_s(exp_name) + "\\1", exprs
            )
            exprs = gsub(re.compile(f"{to_s(arg_name)}\\Z"), to_s(exp_name), exprs)
        if exprs != to_s(cj_size_is):
            self.cdl_error(
                "S1172 '$1' size_is argument mismatch with exporting one '$2'",
                a.get_name(),
                cj.get_name(),
            )

    def check_reverse_require(self) -> None:
        """逆 require をチェックする（逆 require 指定された受け口に複数の結合がないか）。"""
        if self._celltype is None:
            return
        if self._b_defined is False:
            return
        for port, count in self._referenced_port_list.items():
            if port.is_reverse_required() and count > 1:
                self.cdl_warning(
                    "W1009 $1: fixed join entry port has multi join", port.get_name()
                )

    def set_require_join(self, cp_name: Any, cell_or_ct: Any, port: Any) -> None:
        """require 呼び口の結合を行う（STAGE: S）。

        cp_name:: Symbol : 呼び口名 / cell_or_t:: Celltype|Cell / port:: Port
        """
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression
        from tecsgen.core.generator import Token

        dbg_print(
            f"set_require_join: {to_s(self._name)}.{to_s(cp_name)} = "
            f"{to_s(cell_or_ct.get_name())}.{to_s(port.get_name())}\n"
        )

        if type(cell_or_ct) is Celltype:
            cell = cell_or_ct.get_singleton_cell(self._region)
            if cell is None:
                self.cdl_error(
                    "S1025 not found reachable cell for require '$1' in celltype '$2'",
                    port.get_name(),
                    cell_or_ct.get_name(),
                )
                return
        else:
            # require: cell で指定
            cell = cell_or_ct
            if self._region.distance(cell.get_region()) is None:
                self.cdl_error(
                    "S1026 required cell '$1' not reachable", cell.get_name()
                )

        if truthy(self._join_list.get_item(cp_name)):
            self.cdl_warning(
                "W1003 $1 : require call port overridden in $2", cp_name, self._name
            )
        else:
            # require の join を生成(呼び口の結合)
            nsp = NamespacePath(cell.get_name(), False, cell.get_namespace())
            nsp.set_locale(self._locale)
            rhs = Expression(
                [
                    Y.OP_DOT,
                    [Y.IDENTIFIER, nsp],
                    Token(port.get_name(), None, None, None),
                ],
                self._locale,
            )  # 1
            join = Join(cp_name, None, rhs, self._locale)
            self.new_join(join)

            join.set_definition(self._celltype.find(join.get_name()))

    def set_definition_join(self) -> None:
        """Join の definition の設定とチェック（STAGE: S。結合の意味チェック）。"""
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype

        if self._celltype is None:  # 既にエラー：打ち切る
            return
        if self._b_defined is False:  # プロトタイプ宣言のみ
            return
        if self._b_checked is True:  # 既に設定（チェック）済み
            return

        dbg_print(f"set_definition_join in {to_s(self._name)}\n")

        # relay allocator をたどって再入しないよう、先頭で @b_checked を true にする
        self._b_checked = True

        if not self._f_cloned:
            self.check_restrict_list()

            # compoiste セルのクローンされたものは、set_definition 不要
            for join in self._join_list.get_items():
                dbg_print(
                    f" set_definition_join: checking {to_s(self._name)}.{to_s(join.get_name())}\n"
                )
                if truthy(join.get_array_member()):
                    port = self._celltype.find(join.get_name())
                    for am in join.get_array_member2():
                        if am is None:  # 未結合の場合、エラーチェックは check_join
                            continue
                        am.set_definition(port)
                else:
                    dbg_print(
                        f"set_definition_join: {to_s(self._name)}.{to_s(join.get_name())} "
                        f"celltype={to_s(self._celltype.get_name())}\n"
                    )
                    join.set_definition(self._celltype.find(join.get_name()))

        # リレー join は through プラグイン生成後にしかできない
        self.create_relay_allocator_join()

        # composite セルの展開
        if (
            not self._in_composite
            and not self._f_cloned
            and type(self._celltype) is CompositeCelltype
        ):
            # composite セルタイプ内の composite は展開しない
            self.expand()

    def expand(self) -> None:
        """composite セルの展開（このセルが composite セルタイプ）。"""
        dbg_print(f"=====    expanding   {to_s(self._name)}     =====\n")

        # composite celltype の cell を展開
        cl, cl2 = self._celltype.expand(
            self._name,
            self._global_name,
            self._NamespacePath,
            self._join_list,
            self._region,
            self._plugin,
            self._locale,
        )
        self.__dict__["_cell_list"] = cl
        self.__dict__["_cell_list2"] = cl2

        # プロトタイプが参照されている場合、子も参照されていることにする
        if self._f_ref:
            dbg_print("expand: set_f_ref\n")
            self.set_f_ref()

    def set_max_entry_port_inner_cell(self) -> None:
        """内部セルの受け口添数最大値を設定。"""
        if self._cell_list is None:
            return

        dbg_print(
            f"set_max_entry_port_inner_cell name={to_s(self._name)} "
            f"entry_array_max_subscript.len={len(self._entry_array_max_subscript)}\n"
        )

        # プロトタイプ宣言で設定されていたものを反映する
        for port, name in list(self._entry_array_max_subscript.items()):
            dbg_print(f"set_entry_inner_port_max_subscript( #<Port>, {to_s(name)} )\n")
            self.set_entry_inner_port_max_subscript(port, name)

    def add_restrict(
        self, entry_name: Any, func_name: Any, region_name_list: list[Any]
    ) -> None:
        """restrict を追加。"""
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.region import Region

        if self._restrict_list.get(entry_name) is None:
            self._restrict_list[entry_name] = {}
            self._restrict_list2[entry_name] = {}
        if self._restrict_list[entry_name].get(func_name) is None:
            self._restrict_list[entry_name][func_name] = []
            self._restrict_list2[entry_name][func_name] = []
        for rp in region_name_list:
            self._restrict_list[entry_name][func_name].append(rp)
            obj = Namespace.find(rp)
            if isinstance(obj, Region):
                self._restrict_list2[entry_name][func_name].append(
                    obj.get_domain_root()
                )
            else:
                self.cdl_error("S9999 $1 not found or not region", to_s(rp))

    def check_restrict_list(self) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.region import Region

        for func_hash in self._restrict_list.values():
            for region_list in func_hash.values():
                for rp in region_list:
                    obj = Namespace.find(rp)
                    if isinstance(obj, Region):
                        if obj.get_domain_root() is not self._region.get_domain_root():
                            pass
                        else:
                            self.cdl_info(
                                "I9999 $1: restrict calling domain to $2, which is same domain as the cell locates",
                                self._name,
                                to_s(rp),
                            )
                    else:
                        self.cdl_error("S9999 $1 not region", to_s(rp))

    def callable(
        self, callee_cell: Any, entry_name: Any, func_name: Any
    ) -> Any:  # Ruby: callable?
        res = callee_cell.callable_from(entry_name, func_name, self)
        dbg_print(
            f"callable? {to_s(callee_cell.get_namespace_path())}.{to_s(entry_name)}.{to_s(func_name)} "
            f"from {to_s(self._NamespacePath)} is {to_s(res)}\n"
        )
        return res

    def callable_from(
        self, entry_name: Any, func_name: Any, caller_cell: Any
    ) -> Any:  # Ruby: callable_from?
        """（private）Ruby 版は、許可リストに一致しなかったとき each の戻り値（配列）を返す。"""
        self._b_restrict_referenced = True
        if len(self._restrict_list) == 0:
            return True

        dr = caller_cell.get_region().get_domain_root()
        if truthy(self._restrict_list.get(entry_name)):
            if truthy(self._restrict_list[entry_name].get(func_name)):
                lst = self._restrict_list2[entry_name][func_name]
            elif truthy(self._restrict_list[entry_name].get(None)):
                lst = self._restrict_list2[entry_name][None]
            else:
                return False
            for region in lst:
                if dr is region:
                    return True
            return lst
        return False

    def get_restricted_regions(self, entry_name: Any, func_name: Any) -> Any:
        """func_name=nil の場合、entry_name の可否をチェックする（nil は制限されていないこと）。"""
        self._b_restrict_referenced = True
        if truthy(self._restrict_list.get(entry_name)):
            if truthy(self._restrict_list[entry_name].get(func_name)):
                return self._restrict_list2[entry_name][func_name]
            return self._restrict_list2[entry_name].get(None)
        return None

    def has_ineffective_restrict_specifier(self) -> bool:
        """restrict 指定子が指定されていて、参照されていない場合 true。"""
        return len(self._restrict_list) != 0 and self._b_restrict_referenced is False

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"Cell: name: {to_s(self._name)} in_composite: {to_s(self._in_composite)} "
            f"def: {to_s(self._b_defined)} ref: {to_s(self._f_ref)} cloned: {to_s(self._f_cloned)}"
        )
        rb_print("  " * (indent + 1))
        rb_puts(
            f"Cell locale: {to_s(self._name)}@{to_s(self._locale[0])}#{to_s(self._locale[1])}"
        )
        rb_print("  " * (indent + 1))
        plugin_class = "NilClass" if self._plugin is None else to_s(type(self._plugin))
        rb_puts(
            f"id: {to_s(self._id)}  global_name: {to_s(self._global_name)}  "
            f"region: {to_s(self._region.get_name())} plugin: {plugin_class} #<Cell>"
        )
        rb_print("  " * (indent + 1))
        rb_puts(f"namespace_path: {to_s(self._NamespacePath)}")

        if truthy(self._celltype):
            rb_print("  " * (indent + 1))
            rb_puts(f"celltype: {to_s(self._celltype.get_name())}")
        self._join_list.show_tree(indent + 1)
        for port, num in self._entry_array_max_subscript.items():
            rb_print("  " * (indent + 1))
            rb_puts(f"entry array {to_s(port.get_name())}: max subscript={to_s(num)}")
        if truthy(self._cell_list):
            rb_print("  " * (indent + 1))
            rb_puts("cloned cell list:")
            for n, c in _each_pair(self._cell_list):
                rb_print("  " * (indent + 2))
                rb_puts(f"inner cell : {to_s(n)} = {to_s(c.get_name())}")
        if truthy(self._compositecelltypejoin_list):
            for cj in self._compositecelltypejoin_list.get_items():
                cj.show_tree(indent + 1)
        if len(self._alloc_list) > 0:
            rb_print("  " * (indent + 1))
            rb_puts("allocator list: ")
            for a in self._alloc_list:
                cp_name = f"{to_s(a[1])}_{to_s(a[3])}_{to_s(a[4])}"
                subscript = f"[{to_s(a[2])}]" if truthy(a[2]) else ""
                rb_print("  " * (indent + 2))
                rb_puts(f"{cp_name}{subscript} = {to_s(a[5])}")
        for port, count in self._referenced_port_list.items():
            rb_print("  " * (indent + 1))
            rb_puts(f"{to_s(port.get_name())} : {to_s(count)} times referenced")


def _at(lst: list[Any], i: int) -> Any:
    return lst[i] if i < len(lst) else None


def _each_pair(h: Any) -> Any:
    """Hash#each { |k, v| }（配列のときは要素を [k, v] として展開する）。"""
    if isinstance(h, dict):
        return list(h.items())
    return [tuple(e) if isinstance(e, (list, tuple)) else (e, None) for e in h]


def _call(obj: Any, name: str, *args: Any) -> Any:
    if obj is None:
        from tecsgen.ruby_compat import no_method

        raise no_method(name, None)
    return getattr(obj, name)(*args)
