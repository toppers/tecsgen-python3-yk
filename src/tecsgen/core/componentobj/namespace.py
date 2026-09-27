"""namespace.rb の移植。名前空間（`Namespace`）。

root namespace だけ、Region クラスのインスタンスとして生成される（root region を兼ねる）。
@cell_list は Region の場合にのみ持つ (mikan @cell_list 関連は Region に移すべき)。

Ruby 版は同じ名前のクラスメソッドとインスタンスメソッドを多く持つ（`Namespace.find` と
`ns.find` など）。これらは `dualmethod` で表す。クラス変数は、子クラス（Region）からも
同じものを参照するので、必ず `Namespace._xxx` と書く（`cls._xxx` に代入すると子クラスに
別の属性ができてしまう）。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.core.generate import NamespaceGenerate
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.syntaxobj.node import NSBDNode
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    dualmethod,
    rb_print,
    rb_puts,
    to_s,
    truthy,
)


class Namespace(NamespaceGenerate, NSBDNode):
    """@name::  Symbol     # root の場合 "::" (String)
    @global_name:: str
    @name_list:: NamedList   Signature,Celltype,CompositeCelltype,Cell,Typedef,Namespace
    @struct_tag_list:: NamedList : StructType
    @namespace_list:: Namespace[] : Region は Namespace の子クラスであり、含まれる
    @signature_list:: Sginature[] / @celltype_list:: Celltype[]
    @compositecelltype_list:: CompositeCelltype[] / @cell_list:: Cell[]
    @typedef_list:: Typedef[]
    @decl_list:: ( Typedef | StructType | EnumType )[]   依存関係がある場合に備えて、順番どおりに配列に格納
    @const_decl_list:: Decl[]
    @cache_n_cells:: Integer :  get_n_cells の結果をキャッシュする
    @cache_generating_region:: Region :  get_n_cells の結果をキャッシュするしているリージョン
    @NamespacePath:: NamespacePath: NamespacePath クラスのオブジェクト
    """

    # namespace 階層用のスタック
    _namespace_stack: ClassVar[
        list[Any]
    ] = []  # @@namespace_stack[0] = "::" (generator.rb)
    _namespace_sp: ClassVar[int] = -1

    # Generator ネスト用のスタック (namespace 階層用のスタックを対比する)
    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []

    _root_namespace: ClassVar[Any] = None

    # generate.rb がクラス本体で定義するクラス変数
    _domain_gen_factory_list: ClassVar[dict[Any, Any]] = {}
    _class_gen_factory_list: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        Namespace._namespace_stack = []
        Namespace._namespace_sp = -1
        Namespace._nest_stack_index = -1
        Namespace._nest_stack = []
        Namespace._root_namespace = None
        Namespace._domain_gen_factory_list = {}
        Namespace._class_gen_factory_list = {}

    # Generator ネスト用スタックの push, pop (クラスメソッド)
    # namespace 階層用スタックの push, pop (インスタンスメソッド)
    @dualmethod
    def push(cls) -> None:
        dbg_print("push Namespace\n")
        Namespace._nest_stack_index += 1
        _set_at(
            Namespace._nest_stack,
            Namespace._nest_stack_index,
            [Namespace._namespace_stack, Namespace._namespace_sp],
        )
        if truthy(Namespace._root_namespace):
            Namespace._namespace_sp = 0
            _set_at(Namespace._namespace_stack, 0, Namespace._root_namespace)

    @push.instance
    def push(self, ns: Any) -> None:
        Namespace._namespace_sp += 1
        _set_at(Namespace._namespace_stack, Namespace._namespace_sp, self)
        dbg_print(f"Namespace.PUSH {Namespace._namespace_sp} {to_s(self._name)}\n")

    @dualmethod
    def pop(cls) -> None:
        dbg_print("pop Namespace\n")
        Namespace._namespace_stack, Namespace._namespace_sp = _get_at(
            Namespace._nest_stack, Namespace._nest_stack_index
        )
        Namespace._nest_stack_index -= 1
        if Namespace._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    @pop.instance
    def pop(self) -> None:
        dbg_print(f"Namespace.POP {Namespace._namespace_sp} {to_s(self._name)}\n")
        Namespace._namespace_sp -= 1
        if Namespace._namespace_sp < 0:
            raise RubyRuntimeError("StackUnderflow")

    def __init__(self, name: Any) -> None:
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.syntaxobj.namedlist import NamedList

        dbg_print(
            f"Namespace: initialize name={to_s(name)} sp={Namespace._namespace_sp} **\n"
        )
        super().__init__()
        self._name = name

        if type(name) is str and name == "::":
            if Namespace._root_namespace is not None:
                # root は一回のみ生成できる
                raise RubyRuntimeError("try to re-create root namespace")
            Namespace._root_namespace = self
            self._NamespacePath = NamespacePath(name, True)
        else:
            ns = Namespace._current_stack_top().find(name)
            if isinstance(ns, Namespace):
                dbg_print(f"namespace: re-appear {to_s(self._name)}\n")
                # 登録済み namespace の再登録
                self.set_owner(Namespace._current_stack_top())
                ns.push(ns)
                return
            elif truthy(ns):
                self.cdl_error("S1151 $1: not namespace", self._name)
                prev_locale = ns.get_locale()
                rb_puts(
                    f"previous: {to_s(prev_locale[0])}: line {to_s(prev_locale[1])} "
                    f"'{to_s(name)}' defined here"
                )
            dbg_print(f"namespace: 1st-appear {to_s(self._name)}\n")

        dbg_print(
            f"Namespace: initialize name={to_s(name)} sp={Namespace._namespace_sp}\n"
        )
        if Namespace._namespace_sp >= 0:  # root は除外
            dbg_print(
                f"Namespace: initialize2 name={to_s(name)} sp={Namespace._namespace_sp}\n"
            )
            Namespace._current_stack_top().new_namespace(self)
        self.push(self)

        self._global_name = Namespace.get_global_name()  # stack 登録後取る
        self._name_list = NamedList(None, f"symbol in namespace '{to_s(self._name)}'")
        self._struct_tag_list = NamedList(None, "struct tag")

        self._namespace_list: list[Any] = []
        self._signature_list: list[Any] = []
        self._celltype_list: list[Any] = []
        self._compositecelltype_list: list[Any] = []
        self._cell_list: list[Any] = []
        self._typedef_list: list[Any] = []
        self._decl_list: list[Any] = []
        self._const_decl_list: list[Any] = []
        self._cache_n_cells: Any = None
        self._cache_generating_region: Any = None
        if self._NamespacePath is None:
            # root namespace の場合は設定済 (親 namespace が見つからず例外になる)
            self.set_namespace_path()  # @NamespacePath の設定

    @staticmethod
    def _current_stack_top() -> Any:
        """@@namespace_stack[@@namespace_sp]（nil なら NoMethodError になる呼び出し元のため）。"""
        top = _get_at(Namespace._namespace_stack, Namespace._namespace_sp)
        if top is None:
            from tecsgen.ruby_compat import no_method

            raise no_method("find", None)
        return top

    def end_of_parse(self) -> None:
        self.pop()

    def get_name(self) -> Any:
        return self._name

    @dualmethod
    def get_global_name(cls) -> str:
        """global_name を得る（parse 中のみこのメソッドは使える。STAGE: P）。"""
        if Namespace._namespace_sp <= 0:
            return ""

        path = to_s(Namespace._namespace_stack[1].get_name())
        i = 2
        while i <= Namespace._namespace_sp:
            path = path + "_" + to_s(Namespace._namespace_stack[i].get_name())
            i += 1
        return path

    @get_global_name.instance
    def get_global_name(self) -> Any:
        return self._global_name

    def get_n_cells(self) -> int:
        """セルの個数を得る。

        子 region が linkunit, node 指定されていれば、含めない（別のリンク単位）。
        プロトタイプ宣言のもののみの個数を含めない。
        """
        from tecsgen.ruby_compat import Y

        generating_region = get_context().generating_region
        if self._cache_generating_region is generating_region:
            # このメソッドは繰り返し呼び出されるため、結果をキャッシュする
            return self._cache_n_cells

        count = 0
        for c in self._cell_list:
            # 定義かプロトタイプ宣言だけかは、new_cell の段階で判断できないため、カウントしなおす
            if c.get_f_def() is True:
                count += 1

        for ns in self._namespace_list:
            if type(ns) is Namespace:
                count += ns.get_n_cells()
            else:
                # ns は Region である
                rt = ns.get_region_type()
                if rt == Y.NODE or rt == Y.LINKUNIT:
                    pass  # 別の linkunit なので加算しない
                else:
                    count += ns.get_n_cells()

        self._cache_generating_region = generating_region
        self._cache_n_cells = count
        return count

    @dualmethod
    def find(cls, in_path: Any) -> Any:
        """in_path で示されるオブジェクトを探す。

        in_path:: NamespacePath
        in_path:: Array : 古い形式  [ "::", "ns1", "ns2" ] absolute / [ "ns1", "ns2" ] relative
        """
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        if type(in_path) is list:
            path = in_path
            length = len(path)
            if length == 1:
                return Namespace.find_one(path[0])

            name = path[0]
            if type(name) is str and name == "::":
                i = 1
                name = path[i]  # 構文的に必ず存在
                obj = Namespace._root_namespace.find(name)  # root
            else:
                # 相対パス
                i = 0
                obj = Namespace._current_stack_top().find_one(name)  # crrent
        elif type(in_path) is NamespacePath:
            path = in_path.get_path()
            length = len(path)

            if length == 0:
                if in_path.is_absolute():
                    return Namespace._root_namespace
                raise RubyRuntimeError("path length 0, not absolute")

            i = 0
            name = path[0]
            if in_path.is_absolute():
                obj = Namespace._root_namespace.find(name)  # root
            else:
                bns = in_path.get_base_namespace()
                obj = bns.find_one(name)  # crrent
        else:
            raise RubyRuntimeError("unexpected path")

        i += 1
        while i < length:
            if not isinstance(obj, Namespace):
                # このメソッドから nil が帰った場合 "not found" が出るので、ここでは出さない
                return None
            obj = obj.find(path[i])
            i += 1

        return obj

    @find.instance
    def find(self, name: Any) -> Any:
        return self._name_list.get_item(name)

    @dualmethod
    def find_one(cls, name: Any) -> Any:
        """namespace から探す。見つからなければ親 namespace から探す。"""
        return Namespace._current_stack_top().find_one(name)

    @find_one.instance
    def find_one(self, name: Any) -> Any:
        obj = self.find(name)
        if obj is not None:
            return obj
        if not (type(self._name) is str and self._name == "::"):
            return self._owner.find_one(name)
        return None

    @classmethod
    def get_current(cls) -> Any:
        return _get_at(Namespace._namespace_stack, Namespace._namespace_sp)

    @dualmethod
    def find_tag(cls, name: Any) -> Any:
        """カレント namespace から根に向かって探す（mikan tag : namespace の path に対応しない）。"""
        i = Namespace._namespace_sp
        while i >= 0:
            res = Namespace._namespace_stack[i].find_tag(name)
            if truthy(res):
                return res
            i -= 1
        return None

    @find_tag.instance
    def find_tag(self, name: Any) -> Any:
        return self._struct_tag_list.get_item(name)

    # --- namespace
    @dualmethod
    def new_namespace(cls, namespace: Any) -> None:
        Namespace._current_stack_top().new_namespace(namespace)

    @new_namespace.instance
    def new_namespace(self, namespace: Any) -> None:
        dbg_print(
            f"new_namespace: {to_s(self._name)}:{self!r} {to_s(namespace.get_name())}:{namespace!r} \n"
        )
        namespace.set_owner(self)  # Namespace (Namespace)
        self._name_list.add_item(namespace)
        self._namespace_list.append(namespace)

    # --- signature
    @dualmethod
    def new_signature(cls, signature: Any) -> None:
        Namespace._current_stack_top().new_signature(signature)

    @new_signature.instance
    def new_signature(self, signature: Any) -> None:
        signature.set_owner(self)  # Signature (Namespace)
        self._name_list.add_item(signature)
        self._signature_list.append(signature)

    # --- celltype
    @dualmethod
    def new_celltype(cls, celltype: Any) -> None:
        Namespace._current_stack_top().new_celltype(celltype)

    @new_celltype.instance
    def new_celltype(self, celltype: Any) -> None:
        celltype.set_owner(self)  # Celltype (Namespace)
        self._name_list.add_item(celltype)
        self._celltype_list.append(celltype)

    # --- compositecelltype
    @dualmethod
    def new_compositecelltype(cls, compositecelltype: Any) -> None:
        Namespace._current_stack_top().new_compositecelltype(compositecelltype)

    @new_compositecelltype.instance
    def new_compositecelltype(self, compositecelltype: Any) -> None:
        compositecelltype.set_owner(self)  # CompositeCelltype (Namespace)
        self._name_list.add_item(compositecelltype)
        self._compositecelltype_list.append(compositecelltype)

    # --- cell (Namespace)
    @dualmethod
    def new_cell(cls, cell: Any) -> None:
        Namespace._current_stack_top().new_cell(cell)

    @new_cell.instance
    def new_cell(self, cell: Any) -> None:
        from tecsgen.core.componentobj.region import Region

        dbg_print(
            f"Namespace.new_cell: {self._NamespacePath.get_path_str()}::{to_s(cell.get_name())}\n"
        )
        if not self.is_root() and type(self) is not Region:
            self.cdl_error(
                "S9999 '$1' cell cannot be placed under namespace", cell.get_name()
            )
        cell.set_owner(self)  # Cell (Namespace)
        self._name_list.add_item(cell)
        self._cell_list.append(cell)

    def check_ref_but_undef(self) -> None:
        """参照されているが、未定義のセルを探す。

        プロトタイプ宣言だけで定義されていないケースをエラーとする。受動の未結合セルについて警告する。
        """
        for c in self._cell_list:
            if not truthy(
                c.get_f_def()
            ):  # Namespace の @cell_list にはプロトタイプが含まれるケースあり
                if truthy(c.get_f_ref()):
                    c.cdl_error(
                        "S1093 $1 : undefined cell",
                        c.get_namespace_path().get_path_str(),
                    )
                elif get_context().verbose:
                    c.cdl_warning(
                        "W1006 $1 : only prototype, unused and undefined cell",
                        c.get_namespace_path().get_path_str(),
                    )
            else:
                dbg_print(f"check_ref_but_undef: {to_s(c.get_global_name())}\n")
                ct = c.get_celltype()
                if c.get_f_ref() is False and truthy(ct) and ct.is_inactive():
                    c.cdl_warning(
                        "W1007 $1 : non-active cell has no entry join and no factory",
                        c.get_namespace_path().get_path_str(),
                    )
                if truthy(c.has_ineffective_restrict_specifier()):
                    c.cdl_warning(
                        "W9999: $1 has ineffective restrict specifier",
                        c.get_namespace_path().get_path_str(),
                    )
        for n in self._namespace_list:
            n.check_ref_but_undef()

    def set_port_reference_count(self) -> None:
        """セルの受け口の参照カウントを設定する。"""
        for c in self._cell_list:
            c.set_port_reference_count()
        for n in self._namespace_list:
            n.set_port_reference_count()

    # --- struct
    @dualmethod
    def new_structtype(cls, struct: Any) -> None:
        Namespace._current_stack_top().new_structtype(struct)

    @new_structtype.instance
    def new_structtype(self, struct: Any) -> None:
        # StructType は BDNode ではない
        dup = self._struct_tag_list.get_item(struct.get_name())
        if dup is not None and struct.same(dup):
            # 同じものが typedef された
            return
        self._struct_tag_list.add_item(struct)
        self._decl_list.append(struct)

    # --- typedef
    @dualmethod
    def new_typedef(cls, typedef: Any) -> None:
        Namespace._current_stack_top().new_typedef(typedef)

    @new_typedef.instance
    def new_typedef(self, typedef: Any) -> None:
        typedef.set_owner(self)  # TypeDef (Namespace)
        dup = self._name_list.get_item(typedef.get_name())
        if dup is not None:
            typedef_type = typedef.get_declarator().get_type().get_original_type()
            dup_type = dup.get_declarator().get_type().get_original_type()
            if (
                typedef_type.get_type_str() == dup_type.get_type_str()
                and typedef_type.get_type_str_post() == dup_type.get_type_str_post()
            ):
                # 同じものが typedef された
                # ここへ来るのは C で関数ポインタを typedef しているケース
                return

        self._name_list.add_item(typedef)
        self._typedef_list.append(typedef)
        self._decl_list.append(typedef)

    @dualmethod
    def is_typename(cls, s: Any) -> bool:  # Ruby: is_typename?
        i = Namespace._namespace_sp
        while i >= 0:
            if Namespace._namespace_stack[i].is_typename(s):
                return True
            i -= 1
        return False

    @is_typename.instance
    def is_typename(self, s: Any) -> bool:
        from tecsgen.core.syntaxobj.typedef import Typedef

        return type(self._name_list.get_item(s)) is Typedef

    # --- const_decl
    @dualmethod
    def new_const_decl(cls, decl: Any) -> None:
        Namespace._current_stack_top().new_const_decl(decl)

    @new_const_decl.instance
    def new_const_decl(self, decl: Any) -> None:
        from tecsgen.core.cdl_types import BoolType, FloatType, IntType, PtrType
        from tecsgen.ruby_compat import Y

        decl.set_owner(self)  # Decl (Namespace:const)
        if not decl.is_const():  # const 修飾さていること
            if decl.is_type(PtrType):
                self.cdl_error(
                    "S1094 $1: pointer is not constant. check 'const'", decl.get_name()
                )
            else:
                self.cdl_error("S1095 $1: not constant", decl.get_name())
        elif (
            not decl.is_type(IntType)
            and not decl.is_type(FloatType)
            and not decl.is_type(BoolType)
            and not decl.is_type(PtrType)
        ):
            self.cdl_error(
                "S1096 $1: should be int, float, bool or pointer type", decl.get_name()
            )
        elif decl.get_initializer() is None:  # 初期値を持つこと
            self.cdl_error("S1097 $1: has no initializer", decl.get_name())
        else:
            decl.get_type().check_init(
                self._locale, decl.get_name(), decl.get_initializer(), Y.CONSTANT
            )
            self._name_list.add_item(decl)
            self._const_decl_list.append(decl)

    def set_require_join(self) -> None:
        """すべてのセルの require ポートを設定（STAGE: S）。"""
        for ct in self._celltype_list:
            ct.set_require_join()
        for ns in self._namespace_list:
            ns.set_require_join()

    def set_definition_join(self) -> None:
        """Join への definition の設定とチェック。"""
        for c in self._cell_list:
            dbg_print(f"set_definition_join {to_s(c.get_name())}\n")
            c.set_definition_join()
        for ns in self._namespace_list:
            ns.set_definition_join()

    def set_max_entry_port_inner_cell(self) -> None:
        for c in self._cell_list:
            c.set_max_entry_port_inner_cell()
        for ns in self._namespace_list:
            ns.set_max_entry_port_inner_cell()

    def check_join(self) -> None:
        """セルの結合をチェックする。"""
        for c in self._cell_list:
            dbg_print(f"check_join {to_s(c.get_name())}\n")
            c.check_join()
            c.check_reverse_require()
        for ns in self._namespace_list:
            ns.check_join()

    def is_root(self) -> bool:  # Ruby: is_root?
        """ルートか?（ルートネームスペース と ルートリージョンは同じ）"""
        return type(self._name) is str and self._name == "::"

    @classmethod
    def get_root(cls) -> Any:
        """ルートを得る（ルートリージョンとルートネームスペースは同じオブジェクト）。"""
        return Namespace._root_namespace

    def get_signature_list(self) -> list[Any]:
        return self._signature_list

    def get_namespace_list(self) -> list[Any]:
        return self._namespace_list

    def get_cell_list(self) -> list[Any]:
        return self._cell_list

    def get_region_list(self) -> list[Any]:
        """子リージョンのリスト（リージョンは Namespace クラスで namespace として記憶されている）。"""
        return self._namespace_list

    def get_NamespacePath(self) -> Any:
        return self._NamespacePath

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"{to_s(type(self))}: name: {to_s(self._name)} path: {self.get_namespace_path().get_path_str()}"
        )
        self._struct_tag_list.show_tree(indent + 1)
        self._name_list.show_tree(indent + 1)
