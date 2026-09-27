"""compositecelltype.rb の移植。複合セルタイプ（`CompositeCelltype`）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.componentobj.celltype_module import CelltypePluginModule
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.plugin_module import PluginModule
from tecsgen.core.syntaxobj.node import NSBDNode
from tecsgen.ruby_compat import (
    RubyArgumentError,
    RubyRuntimeError,
    Y,
    dualmethod,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


class CompositeCelltype(CelltypePluginModule, PluginModule, NSBDNode):  # < Nestable
    """@name:: str / @global_name:: str / @cell_list_in_composite:: NamedList   Cell
    @cell_list::Array :: [ Cell ] / @export_name_list:: NamedList : CompositeCelltypeJoin
    @port_list / @attr_list:: CompositeCelltypeJoin[] / @b_singleton / @b_active:: bool
    @real_singleton / @real_active:: Cell / @name_list:: NamedList item: Decl (attribute), Port
    @internal_allocator_list:: [ [cell, internal_cp_name, port_name, func_name, param_name, ext_alloc_ent], ... ]
    @generate / @generate_list
    """

    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []
    _current_object: ClassVar[Any] = None

    @classmethod
    def reset(cls) -> None:
        CompositeCelltype._nest_stack_index = -1
        CompositeCelltype._nest_stack = []
        CompositeCelltype._current_object = None

    @classmethod
    def push(cls) -> None:
        CompositeCelltype._nest_stack_index += 1
        _set_at(
            CompositeCelltype._nest_stack,
            CompositeCelltype._nest_stack_index,
            CompositeCelltype._current_object,
        )
        CompositeCelltype._current_object = None

    @classmethod
    def pop(cls) -> None:
        CompositeCelltype._current_object = _get_at(
            CompositeCelltype._nest_stack, CompositeCelltype._nest_stack_index
        )
        CompositeCelltype._nest_stack_index -= 1
        if CompositeCelltype._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    def __init__(self, name: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.generator import Generator
        from tecsgen.core.syntaxobj.namedlist import NamedList

        super().__init__()
        self._name = name
        self._cell_list_in_composite = NamedList(
            None, f"in composite celltype {to_s(name)}"
        )
        self.__dict__["_cell_list"] = []
        self._export_name_list = NamedList(
            None, f"export in composite celltype {to_s(name)}"
        )
        self._name_list = NamedList(None, f"in composite celltype {to_s(name)}")
        CompositeCelltype._current_object = self

        self._b_singleton = False
        self._real_singleton: Any = None
        self._b_active = False
        self._real_active: Any = None
        if to_s(Namespace.get_global_name()) == "":
            self._global_name = self._name
        else:
            self._global_name = sym(
                f"{to_s(Namespace.get_global_name())}_{to_s(self._name)}"
            )

        Namespace.new_compositecelltype(self)
        self.set_namespace_path()  # @NamespacePath の設定

        self._port_list: list[Any] = []
        self._attr_list: list[Any] = []
        self._internal_allocator_list: list[Any] = []
        self._generate_list: list[Any] = []
        self.set_specifier_list(Generator.get_statement_specifier())

    @dualmethod
    def end_of_parse(cls) -> None:
        CompositeCelltype._current_object.end_of_parse()
        CompositeCelltype._current_object = None

    @end_of_parse.instance
    def end_of_parse(self) -> None:
        from tecsgen.core.componentobj.port import Port

        # singleton に関するチェック
        if self._b_singleton and self._real_singleton is None:
            self.cdl_warning(
                "W1004 $1 : specified singleton but has no singleton in this celltype",
                self._name,
            )
        elif not self._b_singleton and self._real_singleton is not None:
            self.cdl_error(
                "S1053 $1 must be singleton. inner cell '$2' is singleton",
                self._name,
                self._real_singleton.get_name(),
            )

        # active に関するチェック
        if self._b_active and self._real_active is None:
            self.cdl_error(
                "S1054 $1 : specified active but has no active in this celltype",
                self._name,
            )
        elif not self._b_active and self._real_active is not None:
            self.cdl_error(
                "S1055 $1 must be active. inner cell '$2' is active",
                self._name,
                self._real_active.get_name(),
            )

        # @allocator_instance を設定する
        for n in self._name_list.get_items():
            if type(n) is Port:
                n.set_allocator_instance()

        # リレーアロケータの entry 側
        for p in self._port_list:
            if p.get_port_type() == Y.ENTRY:
                if p.get_allocator_instance() is None:
                    continue
                for _name, ai in list(p.get_allocator_instance().items()):
                    if ai[0] == Y.RELAY_ALLOC:
                        self.new_join(
                            sym(f"{to_s(p.get_name())}_{to_s(ai[4])}_{to_s(ai[5])}"),
                            p.get_cell_name(),
                            sym(
                                f"{to_s(p.get_cell_elem_name())}_{to_s(ai[4])}_{to_s(ai[5])}"
                            ),
                            Y.CALL,
                        )

        # callback 結合
        for c in self._cell_list_in_composite.get_items():
            ct = c.get_celltype()
            if truthy(ct):
                c.create_reverse_join()

        # 意味解析
        for c in self._cell_list_in_composite.get_items():
            c.set_definition_join()

        # cell の未結合の呼び口がないかチェック
        for c in self._cell_list_in_composite.get_items():
            c.check_join()
            c.check_reverse_require()

        # 呼び口の結合について、export と内部結合の両方がないかチェック
        for p in self._port_list:
            p.check_dup_init()

        # すべてのエクスポート定義に対応した呼び口、受け口、属性が存在するかチェック
        for n in self._name_list.get_items():
            if self._export_name_list.get_item(n.get_name()) is None:
                self.cdl_error(
                    "S1056 $1 : cannot export, nothing designated", n.get_name()
                )

        # 内部アロケータを設定する
        for (
            cell,
            cp_internal_name,
            port_name,
            fd_name,
            par_name,
            ext_alloc_ent,
        ) in self._internal_allocator_list:
            res = ext_alloc_ent.get_allocator_rhs_elements(Y.INTERNAL_ALLOC)
            ep_name = res[0]
            cj = self._export_name_list.get_item(ep_name)
            internal_alloc_name_from_port_def = cj.get_cell_name()
            internal_alloc_ep_name_from_port_def = cj.get_cell_elem_name()

            for a in cell.get_allocator_list():
                if cp_internal_name == sym(f"{to_s(a[1])}_{to_s(a[3])}_{to_s(a[4])}"):
                    dbg_print(
                        f"internal_allocator {{cp_internal_name}} {to_s(a[1])}_{to_s(a[3])}_{to_s(a[4])}\n"
                    )
                    dbg_print(
                        f"internal_allocator: {to_s(a[5])}, {to_s(internal_alloc_name_from_port_def)}."
                        f"{to_s(internal_alloc_ep_name_from_port_def)}\n"
                    )
                    if to_s(a[5]) != (
                        f"{to_s(internal_alloc_name_from_port_def)}.{to_s(internal_alloc_ep_name_from_port_def)}"
                    ):
                        self.cdl_error(
                            "S1173 $1: allocator mismatch from $2's allocator",
                            f"{to_s(port_name)}.{to_s(fd_name)}.{to_s(par_name)}",
                            cell.get_name(),
                        )

        # composite プラグイン
        if truthy(self._generate):
            self.celltype_plugin()

    @dualmethod
    def new_cell_in_composite(cls, cell: Any) -> None:
        CompositeCelltype._current_object.new_cell_in_composite(cell)

    @new_cell_in_composite.instance
    def new_cell_in_composite(self, cell: Any) -> None:
        cell.set_owner(self)  # Cell (in_omposite)
        self._cell_list_in_composite.add_item(cell)
        if truthy(cell.get_celltype()):  # nil ならば、すでにセルタイプなしエラー
            if cell.get_celltype().is_singleton():
                self._real_singleton = cell
            if cell.get_celltype().is_active():
                self._real_active = cell

    def new_cell(self, cell: Any) -> None:
        self._cell_list.append(cell)
        # セルタイププラグインの適用
        self.celltype_plugin_new_cell(cell)

    @dualmethod
    def new_join(
        cls,
        export_name: Any,
        internal_cell_name: Any,
        internal_cell_elem_name: Any,
        type_: Any,
    ) -> Any:
        return CompositeCelltype._current_object.new_join(
            export_name, internal_cell_name, internal_cell_elem_name, type_
        )

    @new_join.instance
    def new_join(
        self,
        export_name: Any,
        internal_cell_name: Any,
        internal_cell_elem_name: Any,
        type_: Any,
    ) -> Any:
        """CompositeCelltypeJoin を作成（STAGE: B）。

        export_name:: Symbol : 外部に公開する名前 / internal_cell_name:: Symbol : 内部セル名
        internal_cell_elem_name:: Symbol : 内部セルの要素名 / type:: :CALL, :ENTRY, :ATTRIBUTE
        RETURN:: Decl | Port : エクスポート定義
        """
        from tecsgen.core.componentobj.compositecelltypejoin import (
            CompositeCelltypeJoin,
        )
        from tecsgen.core.componentobj.port import Port
        from tecsgen.core.syntaxobj.decl import Decl

        dbg_print(
            f"new_join: {to_s(export_name)} {to_s(internal_cell_name)} {to_s(internal_cell_elem_name)}\n"
        )

        cell = self._cell_list_in_composite.get_item(internal_cell_name)
        if cell is None:
            self.cdl_error("S1057 $1 not found in $2", internal_cell_name, self._name)
            return None

        celltype = cell.get_celltype()
        if celltype is None:  # celltype == nil ならすでにエラー
            return None

        # 内部セルのセルタイプから対応要素を探す
        obj = celltype.find(internal_cell_elem_name)
        if type(obj) is Decl:
            if obj.get_kind() == Y.VAR:
                self.cdl_error(
                    "S1058 '$1' : cannot export var", internal_cell_elem_name
                )
                return None
            elif type_ != Y.ATTRIBUTE:
                self.cdl_error(
                    "S1059 '$1' : exporting attribute. write in cell or use '=' to export attribute",
                    export_name,
                )
        elif type(obj) is Port:
            if obj.get_port_type() != type_:
                self.cdl_error(
                    "S1060 '$1' : port type mismatch. $2 type is allowed here.",
                    export_name,
                    type_,
                )
        else:
            self.cdl_error("S1061 '$1' : not defined", internal_cell_elem_name)
            dbg_print(
                f"S1061 CompositeCelltypeJoin#new_join: {to_s(export_name)} => "
                f"{to_s(internal_cell_name)}.{to_s(internal_cell_elem_name)} {to_s(type_)}\n"
            )
            return None

        # エクスポート定義と一致するかどうかチェック
        obj2 = self._name_list.get_item(export_name)
        if obj2 is None:
            self.cdl_error("S1062 $1 has no export definition", export_name)
        elif type(obj2) is Decl:
            if type(obj) is not Decl:
                self.cdl_error(
                    "S1063 $1 is port but previously defined as an attribute",
                    export_name,
                )
            elif not obj.get_type().equal(obj2.get_type()):
                self.cdl_error(
                    "S1064 $1 : type '$2$3' mismatch with pprevious definition'$4$5'",
                    export_name,
                    obj.get_type().get_type_str(),
                    obj.get_type().get_type_str_post(),
                    obj2.get_type().get_type_str(),
                    obj2.get_type().get_type_str_post(),
                )
        elif type(obj2) is Port:
            if type(obj) is Port:
                if obj.get_port_type() != obj2.get_port_type():
                    self.cdl_error(
                        "S1065 $1 : port type $2 mismatch with previous definition $3",
                        export_name,
                        obj.get_port_type(),
                        obj2.get_port_type(),
                    )
                elif obj.get_signature() is not obj2.get_signature():
                    if (
                        obj.get_signature() is not None
                        and obj2.get_signature() is not None
                    ):
                        self.cdl_error(
                            "S1066 $1 : signature '$2' mismatch with previous definition '$3'",
                            export_name,
                            obj.get_signature().get_name(),
                            obj2.get_signature().get_name(),
                        )
                elif obj.get_array_size() != obj2.get_array_size():
                    self.cdl_error(
                        "S1067 $1 : array size mismatch with previous definition",
                        export_name,
                    )
                elif obj.is_optional() != obj2.is_optional():
                    self.cdl_error(
                        "S1068 $1 : optional specifier mismatch with previous definition",
                        export_name,
                    )
                elif obj.is_omit() != obj2.is_omit():
                    self.cdl_error(
                        "S9999 $1 : omit specifier mismatch with previous definition",
                        export_name,
                    )
                elif obj.is_dynamic() != obj2.is_dynamic():
                    self.cdl_error(
                        "S9999 $1 : dynamic specifier mismatch with previous definition",
                        export_name,
                    )
                elif obj.is_ref_desc() != obj2.is_ref_desc():
                    self.cdl_error(
                        "S9999 $1 : ref_desc specifier mismatch with previous definition",
                        export_name,
                    )
            else:
                self.cdl_error(
                    "S1069 $1 is an attribute but previously defined as a port",
                    export_name,
                )

        join = CompositeCelltypeJoin(
            export_name, internal_cell_name, internal_cell_elem_name, cell, obj2
        )
        join.set_owner(self)  # CompositeCelltypeJoin
        cell.add_compositecelltypejoin(join)

        dbg_print(
            f"compositecelltype join: add {to_s(cell.get_name())} {to_s(export_name)} = "
            f"{to_s(internal_cell_name)}.{to_s(internal_cell_elem_name)}\n"
        )

        if type(obj) is Decl:
            self._attr_list.append(join)  # attribute
        else:
            self._port_list.append(join)  # call/entry port

        # join を @export_name_list に登録
        if (
            type(obj) is Decl and truthy(self._export_name_list.get_item(export_name))
        ) or (
            type(obj) is Port
            and obj.get_port_type() == Y.CALL
            and truthy(self._export_name_list.get_item(export_name))
        ):
            pass  # 既に存在する。追加しない。
        else:
            self._export_name_list.add_item(join)

        # export するポートに含まれる send/receive パラメータのアロケータ(allocator)呼び口をセルと結合
        if type(obj2) is Port:

            def visit(port: Any, fd: Any, par: Any) -> None:
                if par.get_direction() not in (Y.SEND, Y.RECEIVE):
                    return
                cp_name = sym(
                    f"{to_s(port.get_name())}_{to_s(fd.get_name())}_{to_s(par.get_name())}"
                )
                cp_internal_name = sym(
                    f"{to_s(internal_cell_elem_name)}_{to_s(fd.get_name())}_{to_s(par.get_name())}"
                )

                # リレーアロケータ or 内部アロケータ指定がなされている場合、アロケータ呼び口を追加しない
                if truthy(port.get_allocator_instance_tmp()):
                    found = False
                    for s in port.get_allocator_instance_tmp():
                        if s[1] == fd.get_name() and s[2] == par.get_name():
                            found = True
                            if s[0] == Y.INTERNAL_ALLOC:
                                # 内部アロケータの場合
                                self._internal_allocator_list.append(
                                    [
                                        cell,
                                        cp_internal_name,
                                        port.get_name(),
                                        fd.get_name(),
                                        par.get_name(),
                                        s[3],
                                    ]
                                )
                    if found is True:
                        return

                # 外部アロケータの場合
                self.new_join(cp_name, internal_cell_name, cp_internal_name, Y.CALL)

            obj2.each_param(visit)

        # エクスポート定義を返す
        return obj2

    @dualmethod
    def has_attribute(cls, attr: Any) -> bool:  # Ruby: has_attribute?
        return CompositeCelltype._current_object.has_attribute(attr)

    @has_attribute.instance
    def has_attribute(self, attr: Any) -> bool:
        return self._name_list.get_item(attr) is not None

    @dualmethod
    def new_port(cls, port: Any) -> None:
        CompositeCelltype._current_object.new_port(port)

    @new_port.instance
    def new_port(self, port: Any) -> None:
        from tecsgen.core.componentobj.port import Port

        port.set_owner(self)  # Port (CompositeCelltype)
        dbg_print(f"new_port: {to_s(self._owner.get_name())}.{to_s(port.get_name())}\n")
        self._name_list.add_item(port)

        # export するポートに含まれる send/receive パラメータのアロケータ呼び口の export を生成してポートに追加
        def visit(port: Any, fd: Any, par: Any) -> None:
            if par.get_direction() not in (Y.SEND, Y.RECEIVE):
                return
            # 内部アロケータ指定がなされている場合、アロケータ呼び口を追加しない
            if truthy(port.get_allocator_instance_tmp()):
                for s in port.get_allocator_instance_tmp():
                    if (
                        s[0] == Y.INTERNAL_ALLOC
                        and s[1] == fd.get_name()
                        and s[2] == par.get_name()
                    ):
                        return

            if truthy(par.get_allocator()):
                cp_name = sym(
                    f"{to_s(port.get_name())}_{to_s(fd.get_name())}_{to_s(par.get_name())}"
                )
                alloc_sig_path = [par.get_allocator().get_name()]  # mikan Namespace
                array_size = port.get_array_size()  # 呼び口または受け口配列のサイズ
                created_port = Port(
                    cp_name, alloc_sig_path, Y.CALL, array_size
                )  # 呼び口を生成
                created_port.set_allocator_port(port, fd, par)
                if port.is_omit():
                    created_port.set_omit()
                self.new_port(created_port)  # セルタイプに新しい呼び口を追加

        port.each_param(visit)

    @dualmethod
    def new_attribute(cls, attr: Any) -> None:
        CompositeCelltype._current_object.new_attribute(attr)

    @new_attribute.instance
    def new_attribute(self, attribute: list[Any]) -> None:
        """new_attribute for CompositeCelltype。attribute:: [Decl]"""
        for a in attribute:
            a.set_owner(self)  # Decl (CompositeCelltype)
            self._name_list.add_item(a)
            if truthy(a.get_initializer()):
                a.get_type().check_init(
                    self._locale, a.get_identifier(), a.get_initializer(), Y.ATTRIBUTE
                )

    def create_reverse_require_join(self, cell: Any) -> None:
        """逆require の結合を生成する。"""
        from tecsgen.core.componentobj.port import Port

        for n in self._name_list.get_items():
            if type(n) is Port:
                n.create_reverse_require_join(cell)

    @dualmethod
    def find(cls, name: Any) -> Any:
        """false : if not in celltype definition, nil : if not found in celltype"""
        if CompositeCelltype._current_object is None:
            return False
        return CompositeCelltype._current_object.find(name)

    @find.instance
    def find(self, name: Any) -> Any:
        dbg_print(f"CompositeCelltype: find in composite: {to_s(name)}\n")
        cell = self._cell_list_in_composite.get_item(name)
        if truthy(cell):
            return cell
        found = self._name_list.get_item(name)
        dbg_print(
            f"CompositeCelltype: {to_s(name)}, {'' if found is None else '#<obj>'}\n"
        )
        return self._name_list.get_item(name)

    def find_export(self, name: Any) -> Any:
        """export する CompositeCelltypeJoin を得る。"""
        return self._export_name_list.get_item(name)

    def expand(
        self,
        name: Any,
        global_name: Any,
        namespacePath: Any,
        join_list: Any,
        region: Any,
        plugin: Any,
        locale: Any,
    ) -> list[Any]:
        """composite celltype の cell を展開する。

        RETURN: [ { name => cell }, [ cell, ... ] ]（前は名前⇒cloneされた内部セル、後ろは composite の出現順のリスト）
        """
        dbg_print(
            f"expand composite: {to_s(self._name)} name: {to_s(name)}  global_name: {to_s(global_name)}\njoin_list:\n"
        )
        for j in join_list.get_items():
            dbg_print(f"   {to_s(j.get_name())} #<Join>\n")

        # 展開で clone されたセルのリスト、右辺は Cell (composite の場合 composite な cell の clone)
        clone_cell_list: dict[Any, Any] = {}
        clone_cell_list2: list[Any] = []
        clone_cell_list3: dict[Any, Any] = {}

        #  composite 内部のすべての cell について
        for c in self._cell_list_in_composite.get_items():
            dbg_print(f"expand : cell {to_s(c.get_name())}\n")

            # Join の配列
            ja = []

            # CompositeCelltype が export する呼び口、受け口、属性のリストについて
            for cj in self._port_list + self._attr_list:  # cj: CompositeCelltypeJoin
                dbg_print(f"        cj : {to_s(cj.get_name())}\n")

                # CompositeCelltypeJoin (export) の対象セルか？
                if cj.match(c):
                    # 対象セル内の CompositeCelltype の export する Join (attribute または call port)
                    j = join_list.get_item(cj.get_name())

                    if truthy(j):
                        dbg_print(
                            f"  REWRITE_EX parent cell: {to_s(name)} child cell: {to_s(c.get_name())}:  "
                            f"parent's export port: {to_s(cj.get_name())}  join: {to_s(j.get_name())}=>{to_s(j.get_rhs())}\n"
                        )
                    else:
                        dbg_print(
                            f"expand : parent cell: {to_s(name)} child cell: {to_s(c.get_name())}:  "
                            f"parent's export port: {to_s(cj.get_name())}  join: nil\n"
                        )

                    if truthy(j):
                        # ComositeCell 用のもの(j) を対象セル用に clone (@through_list もコピーされる)
                        jc = j.clone_for_composite(self._name, name, locale)
                        # 対象セルの呼び口または属性の名前に変更
                        jc.change_name(cj.get_cell_elem_name())
                        ja.append(jc)

                    dbg_print("\n")

            dbg_print(f"expand : clone {to_s(name)}_{to_s(c.get_name())}\n")

            # セルの clone を生成
            c2 = c.clone_for_composite(
                name, global_name, namespacePath, ja, self._name, region, plugin, locale
            )
            clone_cell_list[to_s(c.get_local_name())] = c2
            clone_cell_list2.append(c2)
            clone_cell_list3[c] = c2

        for nm, c in list(clone_cell_list.items()):
            dbg_print(f"  cloned: {to_s(nm)} = {to_s(c.get_global_name())}\n")
            # join の owner を clone されたセルに変更する V1.1.0.25
            for j in c.get_join_list().get_items():
                j.set_cloned(clone_cell_list.get(to_s(c.get_local_name())))
            dbg_print(f"change_rhs_port: inner cell {to_s(c.get_name())}\n")
            c.change_rhs_port(clone_cell_list3)
        for c in clone_cell_list2:
            c.expand_inner()
        return [clone_cell_list, clone_cell_list2]

    def set_specifier_list(self, spec_list: Any) -> None:
        """CompositeCelltype 指定子リストの設定。"""
        if spec_list is None:
            return
        for s in spec_list:
            s0 = s[0]
            if s0 == Y.SINGLETON:
                self._b_singleton = True
            elif s0 == Y.IDX_IS_ID:
                self.cdl_warning(
                    "W1005 $1 : idx_is_id is ineffective for composite celltype",
                    self._name,
                )
            elif s0 == Y.ACTIVE:
                self._b_active = True
            elif s0 == Y.GENERATE:
                if truthy(self._generate):
                    self.cdl_error("S9999 generate specifier duplicate")
                self._generate = [s[1], s[2]]  # [ PluginName, "option" ]
            else:
                self.cdl_error("S1071 $1 cannot be specified for composite", s0)

    def get_name(self) -> Any:
        return self._name

    def get_global_name(self) -> Any:
        return self._global_name

    def get_port_list(self) -> list[Any]:
        return self._port_list

    def get_attribute_list(self) -> list[Any]:
        return self._attr_list

    def get_var_list(self) -> list[Any]:
        return []  # 空の配列を返す

    def get_internal_allocator_list(self) -> list[Any]:
        return self._internal_allocator_list

    def get_real_celltype(self, port_name: Any) -> Any:
        """port_name に接続されている内部のセルタイプを得る。"""
        cj = self.find_export(port_name)
        inner_celltype = cj.get_cell().get_celltype()
        if type(inner_celltype) is CompositeCelltype:
            # Ruby 版は引数なしで呼んでいて ArgumentError になる
            raise RubyArgumentError("wrong number of arguments (given 0, expected 1)")
        return inner_celltype

    def is_singleton(self) -> Any:  # Ruby: is_singleton?
        return self._b_singleton

    def is_active(self) -> Any:  # Ruby: is_active?
        return self._b_active

    def is_inactive(self) -> bool:  # Ruby: is_inactive?
        """active ではないに加え、全ての内部セルのセルタイプが inactive の場合に inactive。"""
        if self._b_active is False:
            for c in self._cell_list_in_composite.get_items():
                if truthy(c.get_celltype()) and c.get_celltype().is_inactive() is False:
                    return False
            return True
        return False

    def get_id_base(self) -> Any:
        raise RubyRuntimeError("get_id_base")

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(f"CompositeCelltype: name: {to_s(self._name)}")
        rb_print("  " * (indent + 1))
        rb_puts(f"active: {to_s(self._b_active)}, singleton: {to_s(self._b_singleton)}")
        self._cell_list_in_composite.show_tree(indent + 1)
        rb_print("  " * (indent + 1))
        rb_puts("name_list")
        self._name_list.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts("export_name_list")
        self._export_name_list.show_tree(indent + 2)
        if len(self._internal_allocator_list) > 0:
            rb_print("  " * (indent + 1))
            rb_puts("internal_allocator_list:")
            for a in self._internal_allocator_list:
                rb_print("  " * (indent + 1))
                rb_puts(
                    f"  {to_s(a[0].get_name())} {to_s(a[1])} {to_s(a[2])} {to_s(a[3])} {to_s(a[4])}"
                )
