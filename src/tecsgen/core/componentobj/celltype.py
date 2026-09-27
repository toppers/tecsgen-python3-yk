"""celltype.rb の移植。セルタイプ（`Celltype`）。"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.core.componentobj.celltype_module import CelltypePluginModule
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.plugin_module import PluginModule
from tecsgen.core.syntaxobj.node import NSBDNode
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    dualmethod,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


class Celltype(CelltypePluginModule, PluginModule, NSBDNode):  # < Nestable
    """@name:: Symbol / @global_name:: Symbol / @name_list:: NamedList item: Decl (attribute, var), Port
    @port:: Port[] / @attribute:: Decl[] / @var:: Decl[] / @require:: [[cp_name,Celltype|Cell,Port],...]
    @factory_list:: Factory[] / @ct_factory_list:: Factory[] : celltype factory
    @cell_list:: Cell[] : 定義のみ (V1.0.0.2 以降)
    @ordered_cell_list:: Cell[] : ID 順に順序付けされたセルリスト、最適化以降有効
    @b_reuse:: bool :  reuse 指定されて import された(template 不要)
    @singleton / @idx_is_id / @idx_is_id_act / @b_need_ptab / @active / @pseudo_active:: bool
    @generate:: [ Symbol, String, Plugin ] / @generate_list:: [ [ Symbol, String, Plugin ], ... ]
    @n_*:: int >= 0（各種の個数）/ @id_base:: Integer / @b_cp_optimized:: bool
    @plugin:: PluginObject / @included_header:: Hash / @domain_roots::Hash
    @domain_class_roots::Hash / @domain_class_roots2::Hash
    @@domain_class_roots::Hash { sub_region => [ celltype ] }
    """

    _nest_stack_index: ClassVar[int] = -1
    _nest_stack: ClassVar[list[Any]] = []
    _current_object: ClassVar[Any] = None
    _celltype_list: ClassVar[list[Any]] = []  # type: ignore[misc]
    _dynamic_join_checked_list: ClassVar[dict[Any, Any]] = {}
    # optimize.rb がクラス本体で定義するクラス変数（インスタンス変数 @domain_class_roots とは別）
    ID_BASE = 1  # reset_optimize でリセットする
    _ID_BASE: ClassVar[int] = ID_BASE
    _domain_class_roots: ClassVar[Any] = {}  # type: ignore[misc]  { region => celltype }

    @classmethod
    def reset(cls) -> None:
        Celltype._nest_stack_index = -1
        Celltype._nest_stack = []
        Celltype._current_object = None
        Celltype._celltype_list = []
        Celltype._dynamic_join_checked_list = {}
        Celltype._ID_BASE = Celltype.ID_BASE
        Celltype._domain_class_roots = {}

    @classmethod
    def push(cls) -> None:
        Celltype._nest_stack_index += 1
        _set_at(
            Celltype._nest_stack, Celltype._nest_stack_index, Celltype._current_object
        )
        Celltype._current_object = None

    @classmethod
    def pop(cls) -> None:
        Celltype._current_object = _get_at(
            Celltype._nest_stack, Celltype._nest_stack_index
        )
        Celltype._nest_stack_index -= 1
        if Celltype._nest_stack_index < -1:
            raise RubyRuntimeError("TooManyRestore")

    def __init__(self, name: Any) -> None:
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.generator import Generator
        from tecsgen.core.syntaxobj.namedlist import NamedList

        super().__init__()
        Celltype._current_object = self
        self._name = name
        if to_s(Namespace.get_global_name()) != "":
            self._global_name = sym(
                f"{to_s(Namespace.get_global_name())}_{to_s(self._name)}"
            )
        else:
            self._global_name = name

        self._name_list = NamedList(None, f"symbol in celltype {to_s(name)}")
        self._port: list[Any] = []
        self._attribute: list[Any] = []
        self._var: list[Any] = []
        self._require: list[Any] = []
        self._factory_list: list[Any] = []
        self._ct_factory_list: list[Any] = []
        self.__dict__["_cell_list"] = []
        self._singleton = False
        self._active = False
        self._pseudo_active = False
        self._generate: Any = None
        self._generate_list: list[Any] = []

        self._n_attribute_ro = 0
        self._n_attribute_rw = 0
        self._n_attribute_omit = 0
        self._n_var = 0
        self._n_var_omit = 0
        self._n_var_size_is = 0
        self._n_var_init = 0
        self._n_call_port = 0
        self._n_call_port_array = 0
        self._n_call_port_omitted_in_CB = 0
        self._n_call_port_dynamic = 0
        self._n_call_port_array_dynamic = 0
        self._n_call_port_ref_desc = 0
        self._n_call_port_array_ref_desc = 0
        self._n_entry_port = 0
        self._n_entry_port_array = 0
        self._n_entry_port_array_ns = 0
        self._n_entry_port_inline = 0
        self._n_cell_gen = 0

        self._b_cp_optimized = False

        self._plugin = Generator.get_plugin()
        # plugin の場合 PluginObject が返される
        self._b_reuse = Generator.is_reuse()

        if get_context().idx_is_id:
            self._idx_is_id = True
            self._idx_is_id_act = True
            self._b_need_ptab = True
        else:
            self._idx_is_id = False
            self._idx_is_id_act = False
            self._b_need_ptab = False

        Namespace.new_celltype(self)
        self.set_namespace_path()  # @NamespacePath の設定
        self.set_specifier_list(Generator.get_statement_specifier())

        self._included_header: dict[Any, Any] = {}
        self._domain_roots: dict[Any, Any] = {}
        Celltype._celltype_list.append(self)

    def get_name(self) -> Any:
        return self._name

    def get_domain_roots(self) -> Any:
        """ドメインルートを返す（オプティマイズで設定される。コード生成以降有効）。"""
        return self._domain_roots

    def get_domain_class_roots(self) -> Any:
        return self.__dict__.get("_domain_class_roots")

    def get_domain_class_roots2(self) -> Any:
        return self.__dict__.get("_domain_class_roots2")

    @classmethod
    def get_domain_class_roots_total(cls) -> Any:
        return Celltype._domain_class_roots

    def end_of_parse(self) -> None:
        # 属性・変数のチェック
        self.check_attribute()

        # アロケータ呼び口を内部生成
        self.generate_allocator_port()

        # リレーアロケータ、内部アロケータの設定
        for p in self._port:
            p.set_allocator_instance()

        if (
            self._n_entry_port == 0
            and self._active is False
            and len(self._factory_list) == 0
            and (
                (self._singleton and len(self._ct_factory_list) == 0)
                or not self._singleton
            )
        ):
            self.cdl_warning(
                "W1002 $1: non-active celltype has no entry port & factory", self._name
            )

        if truthy(self._generate):
            self.celltype_plugin()

        Celltype._current_object = None

    @dualmethod
    def new_port(cls, port: Any) -> None:
        Celltype._current_object.new_port(port)

    @new_port.instance
    def new_port(self, port: Any) -> None:
        port.set_owner(self)
        self._port.append(port)
        self._name_list.add_item(port)
        if port.get_port_type() == Y.CALL:
            self._n_call_port += 1
            if port.get_array_size() is not None:
                self._n_call_port_array += 1
            if port.is_dynamic():
                self._n_call_port_dynamic += 1
                if port.get_array_size() is not None:
                    self._n_call_port_array_dynamic += 1
            if port.is_ref_desc():
                self._n_call_port_ref_desc += 1
                if port.get_array_size() is not None:
                    self._n_call_port_array_ref_desc += 1
        else:
            self._n_entry_port += 1
            if port.get_array_size() is not None:
                self._n_entry_port_array += 1
            if port.get_array_size() == "[]":
                self._n_entry_port_array_ns += 1
            if port.is_inline():
                self._n_entry_port_inline += 1
        port.set_celltype(self)

    def get_port_list(self) -> list[Any]:
        return self._port

    @dualmethod
    def new_attribute(cls, attribute: Any) -> None:
        Celltype._current_object.new_attribute(attribute)

    @new_attribute.instance
    def new_attribute(self, attribute: list[Any]) -> None:
        """new_attribute for Celltype。attribute:: [Decl]"""
        self._attribute = self._attribute + attribute
        for a in attribute:
            a.set_owner(self)
            self._name_list.add_item(a)
            if a.is_omit():
                self._n_attribute_omit += 1
            elif a.is_rw():
                self._n_attribute_rw += 1
            else:
                self._n_attribute_ro += 1
            if truthy(a.get_initializer()):
                # 登録後にチェックしても問題ない（attr を参照できないので、自己参照しない）
                a.get_type().check_init(
                    self._locale, a.get_identifier(), a.get_initializer(), Y.ATTRIBUTE
                )

    def check_attribute(self) -> None:
        """celltype の attribute/var のチェック（STAGE:  S）。celltype のパースが完了した時点で呼出される。"""
        from tecsgen.core.cdl_types import PtrType
        from tecsgen.core.expression import Expression

        for a in self._attribute + self._var:
            if truthy(a.get_size_is()):
                if not isinstance(a.get_type(), PtrType):
                    # size_is がポインタ型以外に指定された
                    self.cdl_error(
                        "S1011 $1: size_is specified for non-pointer type",
                        a.get_identifier(),
                    )
                else:
                    # 参照する変数が存在し、計算可能な型かチェックする
                    size = a.get_size_is().eval_const(
                        self._name_list
                    )  # C_EXP の可能性あり
                    init = a.get_initializer()
                    if truthy(init):
                        if type(init) is not list:
                            # 初期化子が配列ではない
                            self.cdl_error(
                                "S1012 $1: unsuitable initializer, need array initializer",
                                a.get_identifier(),
                            )
                        elif (
                            isinstance(size, int)
                            and not isinstance(size, bool)
                            and size < len(init)
                        ):
                            # size_is 指定された個数よりも初期化子の配列要素が多い
                            self.cdl_error(
                                "S1013 $1: too many initializer, $2 for $3",
                                a.get_identifier(),
                                len(init),
                                size,
                            )
            elif isinstance(a.get_type(), PtrType):
                ini = a.get_initializer()
                if type(ini) is list or (
                    type(ini) is Expression
                    and type(ini.eval_const2(self._name_list)) is list
                ):
                    # size_is 指定されていないポインタが Array で初期化されていたら、エラー
                    self.cdl_error(
                        "S1159 $1: non-size_is pointer cannot be initialized with array initializer",
                        a.get_identifier(),
                    )

    def get_attribute_list(self) -> list[Any]:
        """属性 (attr) のリストを得る。"""
        return self._attribute

    def generate_allocator_port(self) -> None:
        """アロケータ呼び口を生成（send, receive 引数のアロケータを呼出すための呼び口）。"""
        from tecsgen.core.componentobj.port import Port

        for port in list(self._port):

            def visit(port: Any, fd: Any, par: Any) -> None:
                if par.get_direction() in (Y.SEND, Y.RECEIVE) and truthy(
                    par.get_allocator()
                ):
                    cp_name = sym(
                        f"{to_s(port.get_name())}_{to_s(fd.get_name())}_{to_s(par.get_name())}"
                    )  # アロケータ呼び口の名前
                    alloc_sig_path = par.get_allocator().get_namespace_path()
                    array_size = port.get_array_size()  # 呼び口または受け口配列のサイズ
                    created_port = Port(cp_name, alloc_sig_path, Y.CALL, array_size)
                    created_port.set_allocator_port(port, fd, par)
                    if port.is_optional():
                        created_port.set_optional()
                    if port.is_omit():
                        created_port.set_omit()
                    self.new_port(created_port)  # セルタイプに新しい呼び口を追加

            port.each_param(visit)

    def get_name_list(self) -> Any:
        return self._name_list

    @dualmethod
    def new_var(cls, var: Any) -> None:
        Celltype._current_object.new_var(var)

    @new_var.instance
    def new_var(self, var: list[Any]) -> None:
        """新しい内部変数。var:: [Decl]"""
        self._var = self._var + var
        for i in var:  # i: Decl
            i.set_owner(self)
            if i.is_omit():
                self._n_var_omit += 1
            else:
                self._n_var += 1
            self._name_list.add_item(i)

            # size_is 指定された配列? mikan  count_is
            if truthy(i.get_size_is()):
                self._n_var_size_is += 1

            if truthy(i.get_initializer()):
                i.get_type().check_init(
                    self._locale,
                    i.get_identifier(),
                    i.get_initializer(),
                    Y.VAR,
                    self._name_list,
                )
                self._n_var_init += 1

    def get_var_list(self) -> list[Any]:
        """変数 (var) のリストを得る。"""
        return self._var

    def set_specifier_list(self, spec_list: Any) -> None:
        """celltype の指定子を設定する。"""
        if spec_list is None:
            return

        for s in spec_list:
            s0 = s[0]
            if s0 == Y.SINGLETON:
                self._singleton = True
            elif s0 == Y.IDX_IS_ID:
                self._idx_is_id = True
                self._idx_is_id_act = True
                self._b_need_ptab = True
            elif s0 == Y.ACTIVE:
                self._active = True
            elif s0 == Y.PSEUDO_ACTIVE:
                self._active = True
                self._pseudo_active = True
            elif s0 == Y.GENERATE:
                if truthy(self._generate):
                    self.cdl_error("S1014 generate specifier duplicate")
                self._generate = [s[1], s[2]]  # [ PluginName, "option" ]
            else:
                self.cdl_error("S1015 $1 cannot be specified for composite", s0)
        if self._singleton:
            self._idx_is_id_act = False
            self._b_need_ptab = False

    @dualmethod
    def new_require(
        cls, ct_or_cell_nsp: Any, ep_name: Any, cp_name: Any = None
    ) -> None:
        Celltype._current_object.new_require(ct_or_cell_nsp, sym(ep_name), cp_name)

    @new_require.instance
    def new_require(self, ct_or_cell_nsp: Any, ep_name: Any, cp_name: Any) -> None:
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.port import Port

        # Require: set_owner するものがない
        obj = Namespace.find(ct_or_cell_nsp)  # 1
        if type(obj) is Celltype:
            ct = obj  # Celltype 名で指定
        elif type(obj) is Cell:
            ct = obj.get_celltype()  # Cell 名で指定
        elif obj is None:
            self.cdl_error("S1016 $1 not found", ct_or_cell_nsp.get_path_str())
            return
        else:
            self.cdl_error(
                "S1017 $1 : neither celltype nor cell", ct_or_cell_nsp.get_path_str()
            )
            return

        if not ct.is_singleton():
            # シングルトンではない
            self.cdl_error("S1018 $1 : not singleton cell", obj.get_name())

        # 受け口を探す
        obj2 = ct.find(ep_name)
        if type(obj2) is not Port or obj2.get_port_type() != Y.ENTRY:
            self.cdl_error("S1019 '$1' : not entry port", ep_name)
            return
        elif obj2.get_array_size() is not None:
            self.cdl_error("S1020 '$1' : required port cannot be array", ep_name)
            return

        if obj2.get_signature() is None:
            # signature が未定義：既にエラー
            return

        require_call_port_prefix = Y._require_call_port
        if cp_name is None:
            # 関数名重複チェック
            for req in self._require:
                if not re.search("^" + to_s(require_call_port_prefix), to_s(req[0])):
                    continue  # 名前ありの require は関数名重複チェックしない
                port = req[2]
                if port.get_signature() is obj2.get_signature():
                    # 同じ signature （すべて同じ関数名を持つ）個別に出すのではなく、まとめてエラーとする
                    self.cdl_error(
                        "S1021 $1 : require cannot have same signature with '$2'",
                        obj2.get_name(),
                        port.get_name(),
                    )
                    continue
                for f in port.get_signature().get_function_head_array():
                    # mikan ここは、namedList からの検索にならないの？（効率が悪い）
                    for f2 in obj2.get_signature().get_function_head_array():
                        if f.get_name() == f2.get_name():
                            self.cdl_error(
                                "S1022 $1.$2 : '$3' conflict function name in $4.$5",
                                obj.get_name(),
                                obj2.get_name(),
                                f.get_name(),
                                req[1].get_name(),
                                req[2].get_name(),
                            )

        if cp_name is None:
            b_has_name = False
            cp_name = sym(
                f"{to_s(require_call_port_prefix)}_{to_s(ct.get_name())}_{to_s(obj2.get_name())}"
            )
        else:
            b_has_name = True
        # require を追加
        self._require.append(
            [cp_name, obj, obj2]
        )  # [ lhs:cp_name, rhs:Celltype, rhs:Port ]

        # require port を追加 (呼び口として追加する。ただし require をセットしておく)
        port = Port(cp_name, obj2.get_signature().get_namespace_path(), Y.CALL)
        port.set_require(b_has_name)
        self.new_port(port)

    @dualmethod
    def new_factory(cls, factory: Any) -> None:
        Celltype._current_object.new_factory(factory)

    @new_factory.instance
    def new_factory(self, factory: Any) -> None:
        factory.set_owner(self)
        if truthy(factory.get_f_celltype()):
            self._ct_factory_list.append(factory)
        else:
            self._factory_list.append(factory)
        factory.check_arg(self)

    @dualmethod
    def check_dynamic_join(cls) -> None:
        from tecsgen.core.componentobj.namespace import Namespace

        def visit(ct: Any) -> None:
            if Celltype._dynamic_join_checked_list.get(ct) is None:
                Celltype._dynamic_join_checked_list[ct] = True
                ct.check_dynamic_join()

        Namespace.get_root().travers_all_celltype(visit)

    @check_dynamic_join.instance
    def check_dynamic_join(self) -> None:
        """dynamic の適合性チェック。"""
        if not get_context().verbose:
            return
        for port in self._port:
            signature = port.get_signature()
            if signature is None:  # すでにエラー
                continue
            if port.is_dynamic():
                dbg_print(
                    f"[DYNAMIC] checking dynamic port: {to_s(self._global_name)}.{to_s(port.get_name())}\n"
                )
                if truthy(self.find_ref_desc_port(signature)):
                    continue
                if truthy(self.find_descriptor_param(signature, Y.DYNAMIC)):
                    continue
                self.cdl_warning(
                    "W9999 $1 cannot get information for dynamic port $2",
                    self._name,
                    port.get_name(),
                )
            elif port.is_ref_desc():
                dbg_print(
                    f"[DYNAMIC] checking ref_desc port: {to_s(self._global_name)}.{to_s(port.get_name())}\n"
                )
                if truthy(self.find_dynamic_port(signature)):
                    continue
                if truthy(self.find_descriptor_param(signature, Y.REF_DESC)):
                    continue
                self.cdl_warning(
                    "W9999 $1 cannot put information from ref_desc port $2",
                    self._name,
                    port.get_name(),
                )
            elif truthy(port.get_signature()) and port.get_signature().has_descriptor():
                for sig, param in port.get_signature().get_descriptor_list().items():
                    dbg_print(
                        f"[DYNAMIC] checking Descriptor parameter: {to_s(self._global_name)}."
                        f"{to_s(port.get_name())} ... {to_s(param.get_name())}\n"
                    )
                    if port.get_port_type() == Y.CALL:
                        if param.get_direction() == Y.IN:
                            if truthy(self.find_ref_desc_port(sig)):
                                continue
                            if truthy(self.find_descriptor_param(sig, Y.DYNAMIC)):
                                continue
                        elif param.get_direction() == Y.OUT:
                            if truthy(self.find_dynamic_port(sig)):
                                continue
                            if truthy(self.find_descriptor_param(sig, Y.REF_DESC)):
                                continue
                    elif param.get_direction() == Y.IN:  # :ENTRY
                        if truthy(self.find_dynamic_port(sig)):
                            continue
                        if truthy(self.find_descriptor_param(sig, Y.REF_DESC)):
                            continue
                    elif param.get_direction() == Y.OUT:
                        if truthy(self.find_ref_desc_port(sig)):
                            continue
                        if truthy(self.find_descriptor_param(sig, Y.DYNAMIC)):
                            continue
                    self.cdl_warning(
                        'W9999 "$1" cannot handle Descriptor "$2" information for port "$3"',
                        self._name,
                        param.get_name(),
                        port.get_name(),
                    )

    def find_dynamic_port(self, signature: Any) -> Any:
        dbg_print(f"[DYNAMIC] find_dynamic_port signature={to_s(signature.get_name())}")
        for port in self._port:
            dbg_print(
                f"[DYNAMIC] port={to_s(port.get_name())} signature={to_s(port.get_signature().get_name())} "
                f"dynamic={to_s(port.is_dynamic())}"
            )
            if port.is_dynamic() and port.get_signature() is signature:
                return port
        return None

    def find_ref_desc_port(self, signature: Any) -> Any:
        if signature is None:  # すでにエラー
            return None
        dbg_print(
            f"[DYNAMIC] find_ref_desc_port signature={to_s(signature.get_name())}"
        )
        for port in self._port:
            dbg_print(
                f"[DYNAMIC] port={to_s(port.get_name())} signature={to_s(port.get_signature().get_name())} "
                f"ref_desc={to_s(port.is_ref_desc())}"
            )
            if port.is_ref_desc() and port.get_signature() is signature:
                return port
        return None

    def find_descriptor_param(self, signature: Any, dyn_ref: Any) -> Any:
        """ディスクリプタ型でシグニチャが一致し dyn_ref に対応づく引数を探す。

        dyn_ref::Symbol: :DYNAMIC=ディスクリプタを得る手段となる引数を探す．:REF_DESC=渡す手段となる引数を探す
        """
        from tecsgen.core.cdl_types import DescriptorType, PtrType

        found: list[Any] = []

        for port in self._port:

            def visit(port: Any, func: Any, param: Any) -> None:
                if found:
                    return
                t = param.get_type()
                while isinstance(t, PtrType):
                    t = t.get_type()
                dbg_print(
                    f"[DYNAMIC] dyn_ref={to_s(dyn_ref)} port_type={to_s(port.get_port_type())} "
                    f"dir={to_s(param.get_direction())} paramName={to_s(param.get_name())} "
                    f"paramType={to_s(type(t))}\n"
                )
                if isinstance(t, DescriptorType) and t.get_signature() is signature:
                    d = param.get_direction()
                    if d == Y.INOUT:
                        found.append(param)
                    elif dyn_ref == Y.DYNAMIC:
                        if (d == Y.IN and port.get_port_type() == Y.ENTRY) or (
                            d == Y.OUT and port.get_port_type() == Y.CALL
                        ):
                            found.append(param)
                    elif dyn_ref == Y.REF_DESC:
                        if (d == Y.IN and port.get_port_type() == Y.CALL) or (
                            d == Y.OUT and port.get_port_type() == Y.ENTRY
                        ):
                            found.append(param)
                    else:
                        raise RubyRuntimeError("unknown ref_desc")

            port.each_param(visit)
            if found:
                return found[0]
        return None

    def new_cell(self, cell: Any) -> None:
        """celltype に新しい cell を追加（セルの構文解釈の最後でこのメソドを呼出される）。"""
        dbg_print(f"Celltype#new_cell( {to_s(cell.get_name())} )\n")
        # Celltype では Cell の set_owner しない
        if self._singleton:
            for c in self._cell_list:
                if c.get_region().get_link_root() is cell.get_region().get_link_root():
                    self.cdl_error(
                        "S1024 $1: multiple cell for singleton celltype", self._name
                    )
        self._cell_list.append(cell)

        # プラグインにより生成されたセルタイプか ?
        if truthy(self._plugin):
            self._plugin.new_cell(cell)

        # セルタイププラグインの適用
        self.celltype_plugin_new_cell(cell)

    def has_INIB(self) -> bool:
        """セルタイプは INIB を持つか？"""
        ctx = get_context()
        return bool(
            ctx.rom
            and (
                self._n_attribute_ro > 0
                or self._n_var_size_is > 0
                or (
                    self._n_call_port
                    - self._n_call_port_omitted_in_CB
                    - (self._n_call_port_dynamic - self._n_call_port_array_dynamic)
                )
                > 0
                or (ctx.ram_initializer and self._n_call_port_dynamic > 0)
                or self._n_entry_port_array_ns > 0
            )
        )

    def has_CB(self) -> bool:
        """セルタイプは CB を持つか？"""
        if get_context().rom:
            return (
                self._n_attribute_rw > 0
                or (self._n_var - self._n_var_size_is) > 0
                or (self._n_call_port_dynamic - self._n_call_port_array_dynamic) > 0
            )
        return (
            self._n_attribute_rw > 0
            or self._n_attribute_ro > 0
            or self._n_var > 0
            or (self._n_call_port - self._n_call_port_omitted_in_CB) > 0
            or self._n_entry_port_array_ns > 0
        )

    def need_CB_initializer(self) -> Any:
        """SET_CB_INIB_POINTER, INITIALIZE_CB が必要か。"""
        return (
            self._n_var_init > 0
            or self.has_CB()
            or (truthy(self._n_call_port_dynamic) and get_context().ram_initializer)
        )

    def create_reverse_require_join(self, cell: Any) -> None:
        """逆require の結合を生成する。"""
        for p in self._port:
            p.create_reverse_require_join(cell)

    def get_singleton_cell(self, region: Any) -> Any:
        """singleton セルを得る（距離が最も近いものを返す）。"""
        cell: Any = None
        dist = 999999999  # mikan 制限値
        for c in self._cell_list:
            # 到達可能で最も近いセルを探す（複数の singleton があるかもしれない）
            d = region.distance(c.get_region())
            dbg_print(
                f"distance {to_s(d)} from {to_s(region.get_name())} to {to_s(c.get_name())} "
                f"in {to_s(c.get_region().get_name())}\n"
            )
            if d is not None and d < dist:
                cell = c
                dist = d
        if truthy(cell):
            dbg_print(
                f"distance found:{to_s(cell.get_name())} in {to_s(cell.get_region().get_name())}\n"
            )
        else:
            dbg_print("distance not found\n")
        return cell

    def find(self, name: Any) -> Any:
        return self._name_list.get_item(name)

    def get_global_name(self) -> Any:
        return self._global_name

    def is_singleton(self) -> Any:  # Ruby: is_singleton?
        return self._singleton

    def is_active(self) -> Any:  # Ruby: is_active?
        return self._active

    def idx_is_id_act(self) -> Any:  # Ruby: idx_is_id_act?
        return self._idx_is_id_act

    def multi_domain(self) -> Any:  # Ruby: multi_domain?
        return self._b_need_ptab

    def is_inactive(self) -> bool:  # Ruby: is_inactive?
        """active の他に factory (singleton においては FACTORYを含む)がなければ inactive とする。"""
        return bool(
            self._active is False
            and len(self._factory_list) == 0
            and (
                (self._singleton and len(self._ct_factory_list) == 0)
                or not self._singleton
            )
        )

    def get_id_base(self) -> Any:
        return self._id_base

    def get_plugin(self) -> Any:
        return self._plugin

    def get_require(self) -> list[Any]:
        return self._require

    def need_generate(self) -> bool:  # Ruby: need_generate?
        """コード生成する必要があるか判定（セルの個数が 0 ならセルタイプコードは生成不要）。"""
        return self._n_cell_gen > 0

    def set_require_join(self) -> None:
        """require 呼び口の結合を行う（STAGE: S）。"""
        for req in self._require:
            cp_name = req[0]
            cell_or_ct = req[1]
            port = req[2]
            for c in self._cell_list:
                c.set_require_join(cp_name, cell_or_ct, port)

    def get_cell_list(self) -> list[Any]:
        return self._cell_list

    def is_all_entry_inline(self) -> bool:  # Ruby: is_all_entry_inline?
        """inline 受け口しかないか？（受け口が無い場合、すべての受け口が inline とはしない）"""
        return (
            self._n_entry_port == self._n_entry_port_inline and self._n_entry_port > 0
        )

    def has_celltype_code(self) -> bool:  # Ruby: has_celltype_code?
        """セルタイプコード (celltype.c) を持つか（false の場合、celltype_inline.h しか持たない）。"""
        return not (self.is_all_entry_inline() and not self.is_active())

    @classmethod
    def get_celltype_list(cls) -> list[Any]:
        return Celltype._celltype_list

    def show_tree(self, indent: int) -> None:
        rb_print("  " * indent)
        rb_puts(
            f"Celltype: name={to_s(self._name)} global_name={to_s(self._global_name)}"
        )
        rb_print("  " * (indent + 1))
        plugin_class = "NilClass" if self._plugin is None else to_s(type(self._plugin))
        rb_puts(
            f"active={to_s(self._active)}, singleton={to_s(self._singleton)}, "
            f"idx_is_id={to_s(self._idx_is_id)} plugin={plugin_class} reuse={to_s(self._b_reuse)}"
        )
        rb_print("  " * (indent + 1))
        rb_puts(f"namespace_path: {to_s(self._NamespacePath)}")
        rb_print("  " * (indent + 1))
        rb_puts("port:")
        for i in self._port:
            i.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts("attribute:")
        for i in self._attribute:
            i.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts("var:")
        for i in self._var:
            i.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts("factory:")
        for i in self._factory_list:
            i.show_tree(indent + 2)
        rb_print("  " * (indent + 1))
        rb_puts(f"@n_attribute_ro {self._n_attribute_ro}")
        rb_print("  " * (indent + 1))
        rb_puts(f"@n_attribute_rw {self._n_attribute_rw}")
        rb_print("  " * (indent + 1))
        rb_puts(f"@n_entry_port_inline {self._n_entry_port_inline}")
