"""region.rb の移植。リージョン（`Region`、Namespace の子クラス）。

root region は特殊で、root namespace と同じである。cell は region に属する。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print
from tecsgen.core.componentobj.namespace import Namespace
from tecsgen.ruby_compat import Y, dualmethod, rb_print, rb_puts, to_s, truthy


class Region(Namespace):
    """@name:: string
    @in_through_list:: [ [ plugin_name, plugin_arg ], ... ] : plungin_name = nil の時 in 禁止
    @out_through_list:: [ [ plugin_name, plugin_arg ], ... ] : plungin_name = nil の時 out 禁止
    @to_through_list:: [ [ dst_region, plugin_name, plugin_arg ], ... ]
    @from_through_list:: [ [ src_region, plugin_name, plugin_arg ], ... ]
    @cell_port_throug_plugin_list:: { "#{cell_name}.#{port_name}" => through_generated_list の要素 }
    @region_type::Symbol|Nil : :NODE, :LINKUNIT, :DOMAIN, :CLASS
    @region_type_param::Symbol|Nil : domain, class の名前. node, linkunit では nil
    @link_root:: Region / @node_root:: Region / @family_line:: [ @region_root, ...,@region_me ]
    @in_through_count / @out_through_count:: Integer
    @to_through_count / @from_through_count:: { :RegionName => Integer }
    @domain_type::DomainType / @domain_root::Region / @class_type::ClassType / @class_root::Region
    """

    _in_through_list: ClassVar[list[Any]] = []  # type: ignore[misc]
    _out_through_list: ClassVar[list[Any]] = []  # type: ignore[misc]
    _to_through_list: ClassVar[list[Any]] = []  # type: ignore[misc]
    _from_through_list: ClassVar[list[Any]] = []  # type: ignore[misc]
    _region_type: ClassVar[Any] = None  # type: ignore[misc]
    _region_type_param: ClassVar[Any] = None  # type: ignore[misc]
    _domain_name: ClassVar[Any] = None
    _domain_option: ClassVar[Any] = None  # Token が入る
    _class_name: ClassVar[Any] = None
    _class_option: ClassVar[Any] = None  # Token が入る

    _link_roots: ClassVar[list[Any]] = []
    _node_roots: ClassVar[list[Any]] = []

    _domain_type: Any
    _class_type: Any

    @classmethod
    def reset(cls) -> None:
        Region._in_through_list = []
        Region._out_through_list = []
        Region._to_through_list = []
        Region._from_through_list = []
        Region._region_type = None
        Region._region_type_param = None
        Region._domain_name = None
        Region._domain_option = None
        Region._class_name = None
        Region._class_option = None
        Region._link_roots = []
        Region._node_roots = []

    def __init__(self, name: Any) -> None:
        from tecsgen.core.componentobj.classtype import ClassType
        from tecsgen.core.componentobj.domaintype import DomainType
        from tecsgen.core.generator import Token
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        if not (type(name) is str and name == "::"):
            obj = Namespace.get_current().find(name)  # 1
        else:
            # root リージョン
            obj = None
            Region._region_type = Y.NODE

        # インスタンス変数（Ruby ではクラス変数と同名。Python ではクラス属性と区別できないので
        # インスタンスの __dict__ に入れる）
        self.__dict__["_in_through_list"] = Region._in_through_list
        self.__dict__["_out_through_list"] = Region._out_through_list
        self.__dict__["_to_through_list"] = Region._to_through_list
        self.__dict__["_from_through_list"] = Region._from_through_list
        self.__dict__["_region_type"] = Region._region_type
        self.__dict__["_region_type_param"] = Region._region_type_param

        Region._in_through_list = []
        Region._out_through_list = []
        Region._to_through_list = []
        Region._from_through_list = []
        Region._region_type = None
        Region._region_type_param = None

        self._in_through_count = -1
        self._out_through_count = -1
        self._to_through_count: dict[Any, Any] = {}
        self._from_through_count: dict[Any, Any] = {}

        super().__init__(name)
        self.set_region_roots()

        if truthy(Region._domain_name):
            dbg_print(
                f"Region={to_s(name)} domain_type={to_s(Region._domain_name)} "
                f"option={to_s(Region._domain_option)}\n"
            )
            domain_option = CDLString.remove_dquote(to_s(Region._domain_option))
            self._domain_type = DomainType(
                self, Region._domain_name, domain_option, self._node_root
            )
            Region._domain_name = None
            Region._domain_option = None
        else:
            self._domain_type = None

        if truthy(Region._class_name):
            dbg_print(
                f"Region={to_s(name)} class_type={to_s(Region._class_name)} "
                f"option={to_s(Region._class_option)}\n"
            )
            if isinstance(Region._class_option, Token):
                class_option = CDLString.remove_dquote(to_s(Region._class_option))
            else:
                class_option = Region._class_option  # :global
            self._class_type = ClassType(
                self, Region._class_name, class_option, self._node_root
            )
            Region._class_name = None
            Region._class_option = None
        else:
            self._class_type = None

        if truthy(obj):
            if type(obj) is Region:
                dbg_print(f"Region.new: re-appear {to_s(self._name)}\n")
                # 再出現時に specifier が指定されているか？
                if (
                    len(self._in_through_list) != 0
                    or len(self._out_through_list) != 0
                    or len(self._to_through_list) != 0
                    or len(self._from_through_list) != 0
                    or self._region_type is not None
                    or self._domain_type is not None
                    or self._class_type is not None
                ):
                    self.cdl_error(
                        "S1140 $1: region specifier must place at first appearence",
                        name,
                    )
                return
            # エラー用ダミー定義
            # 異なる同名のオブジェクトが定義済み
            self.cdl_error("S1141 $1 duplication, previous one : $2", name, type(obj))
        else:
            # 初出現
            dbg_print(f"Region.new: {to_s(self._name)}\n")
            self.set_region_family_line()

            if self._region_type == Y.NODE:
                dbg_print(f"new Node: {to_s(self._name)}\n")
                Region._node_roots.append(self)
            if self._region_type == Y.NODE or self._region_type == Y.LINKUNIT:
                dbg_print(f"new LinkRoot: {to_s(self._name)}\n")
                Region._link_roots.append(self)

        self._cell_port_throug_plugin_list: dict[Any, Any] = {}

    @dualmethod
    def end_of_parse(cls) -> None:
        Namespace.get_current().create_domain_plugin()
        Namespace.get_current().create_class_plugin()
        Namespace.get_current().end_of_parse()

    end_of_parse.instance(Namespace.end_of_parse)  # type: ignore[attr-defined]

    @classmethod
    def new_in_through(cls, plugin_name: Any = None, plugin_arg: Any = None) -> None:
        Region._in_through_list.append([plugin_name, plugin_arg])

    @classmethod
    def new_out_through(cls, plugin_name: Any = None, plugin_arg: Any = None) -> None:
        Region._out_through_list.append([plugin_name, plugin_arg])

    @classmethod
    def new_to_through(cls, dst_region: Any, plugin_name: Any, plugin_arg: Any) -> None:
        Region._to_through_list.append([dst_region, plugin_name, plugin_arg])

    @classmethod
    def new_from_through(
        cls, src_region: Any, plugin_name: Any, plugin_arg: Any
    ) -> None:
        Region._from_through_list.append([src_region, plugin_name, plugin_arg])

    @classmethod
    def set_type(cls, type_: Any, param: Any = None) -> None:
        from tecsgen.core.generator import Generator

        if truthy(Region._region_type):
            Generator.error(
                "S1178 $1 region type specifier duplicate, previous $2",
                type_,
                Region._region_type,
            )
        Region._region_type = type_
        Region._region_type_param = param

    @classmethod
    def set_domain(cls, name: Any, option: Any) -> None:
        from tecsgen.core.generator import Generator

        if truthy(Region._domain_name):
            Generator.error(
                "S9999 $1 domain specifier duplicate, previous $2",
                name,
                Region._domain_name,
            )
        elif truthy(Region._class_name):
            Generator.error(
                "S9999 $1 domain & class specifier are incompatible $2",
                name,
                Region._class_name,
            )
        Region._domain_name = name
        Region._domain_option = option

    @classmethod
    def set_class(cls, name: Any, option: Any) -> None:
        from tecsgen.core.generator import Generator

        if truthy(Region._class_name):
            Generator.error(
                "S9999 $1 class specifier duplicate, previous $2",
                name,
                Region._class_name,
            )
        elif truthy(Region._domain_name):
            Generator.error(
                "S9999 $1 class & domain specifier are incompatible $2",
                name,
                Region._domain_name,
            )
        Region._class_name = name
        Region._class_option = option

    @classmethod
    def get_root(cls) -> Any:
        """ルートリージョンを得る（ルートネームスペースと同じ）。"""
        return Namespace.get_root()

    def set_region_roots(self) -> None:
        dbg_print(f"Region#set_region_roots name={to_s(self._name)}\n")
        if self._region_type == Y.NODE:
            self._node_root = self
        else:
            self._node_root = self._owner.get_node_root()
        if self._region_type == Y.NODE or self._region_type == Y.LINKUNIT:
            self._link_root = self
        else:
            self._link_root = self._owner.get_link_root()

    def set_region_family_line(self) -> None:
        dbg_print(f"set_region_family_line: Region: {to_s(self._name)}  \n")
        # ---- Domain ----
        if (
            self._domain_type is not None
            or self._owner is None
            or self._region_type == Y.NODE
        ):
            self._domain_root = self
        else:
            self._domain_root = self._owner.get_domain_root()

        if truthy(self._domain_type):
            self._owner.set_domain_type(self._domain_type)

        # ---- Class ----
        if (
            self._class_type is not None
            or self._owner is None
            or self._region_type == Y.NODE
        ):
            self._class_root = self
        else:
            self._class_root = self._owner.get_class_root()

        if truthy(self._class_type):
            self._owner.set_class_type(self._class_type)

        # ---- Faily Line ----
        if truthy(self._owner):
            self._family_line = [*self._owner.get_family_line(), self]
        else:
            self._family_line = [self]  # root region

    def set_domain_type(self, domain_type: Any) -> None:
        """ドメインタイプが指定されたリージョンの親リージョンにドメインタイプを設定する。

        親リージョンは、既にドメインタイプが指定されていなければ、OutOfDomain とする。
        """
        from tecsgen.core.componentobj.domaintype import DomainType

        if self._region_type == Y.NODE:
            if truthy(self._domain_type):
                if self._domain_type.get_name() != domain_type.get_name():
                    self.cdl_error(
                        "S9999 '$1' node root cannot belong to both $2 and $3",
                        self._name,
                        self._domain_type.get_name(),
                        domain_type.get_name(),
                    )
            else:
                self._domain_type = DomainType(
                    self, domain_type.get_name(), "OutOfDomain", self._node_root
                )
                self._domain_type.create_domain_plugin()
        elif self._domain_type is None:
            self._owner.set_domain_type(domain_type)

    def set_class_type(self, class_type: Any) -> None:
        """クラスが指定されたリージョンの親リージョンにクラスを設定する（なければ OutOfClass）。"""
        from tecsgen.core.componentobj.classtype import ClassType

        if self._region_type == Y.NODE:
            if truthy(self._class_type):
                if self._class_type.get_name() != class_type.get_name():
                    self.cdl_error(
                        "S9999 '$1' node root cannot belong to both $2 and $3",
                        self._name,
                        self._class_type.get_name(),
                        class_type.get_name(),
                    )
            else:
                self._class_type = ClassType(
                    self, class_type.get_name(), Y.root, self._node_root
                )
                self._class_type.create_class_plugin()
        elif self._class_type is None:
            self._owner.set_class_type(class_type)

    @classmethod
    def get_node_roots(cls) -> list[Any]:
        return Region._node_roots

    @classmethod
    def get_link_roots(cls) -> list[Any]:
        return Region._link_roots

    def get_family_line(self) -> list[Any]:
        return self._family_line

    def get_in_through_list(self) -> list[Any]:
        return self._in_through_list

    def get_out_through_list(self) -> list[Any]:
        return self._out_through_list

    def get_to_through_list(self) -> list[Any]:
        return self._to_through_list

    def get_from_through_list(self) -> list[Any]:
        return self._from_through_list

    def get_node_root(self) -> Any:
        return self._node_root

    def get_link_root(self) -> Any:
        return self._link_root

    def get_domain_type(self) -> Any:
        """DomainType を返す（Region がドメインルートでない場合 nil）。"""
        return self._domain_type

    def get_domain_root(self) -> Any:
        """domain の根っことなる region を得る。"""
        return self._domain_root

    def get_class_type(self) -> Any:
        return self._class_type

    def get_class_root(self) -> Any:
        return self._class_root

    def get_path_string(self) -> str:
        pstring = ""
        delim = ""
        for p in self._family_line:
            pstring = f"{pstring}{delim}{to_s(p.get_name())}"
            delim = "."
        dbg_print(f"get_path_string: {pstring}\n")
        return pstring

    def get_region_type(self) -> Any:
        return self._region_type

    def next_in_through_count(self) -> int:
        self._in_through_count += 1
        return self._in_through_count

    def next_out_through_count(self) -> int:
        self._out_through_count += 1
        return self._out_through_count

    def next_to_through_count(self, symRegionName: Any) -> int:
        if self._to_through_count.get(symRegionName) is None:
            self._to_through_count[symRegionName] = 0
        else:
            self._to_through_count[symRegionName] += 1
        return self._to_through_count[symRegionName]

    def next_from_through_count(self, symRegionName: Any) -> int:
        if self._from_through_count.get(symRegionName) is None:
            self._from_through_count[symRegionName] = 0
        else:
            self._from_through_count[symRegionName] += 1
        return self._from_through_count[symRegionName]

    @classmethod
    def get_current(cls) -> Any:
        """構文解析中の region を得る（Namespace の上位をたどって Region を見つける）。"""
        region = Namespace.get_current()
        while True:
            if type(region) is Region:
                break
            region = region.get_owner()
        return region

    def add_cell_port_through_plugin(
        self, cell_name: Any, port_name: Any, subscript: Any, through_plugin_object: Any
    ) -> None:
        """through プラグインで、この region から cell_name.port_name へのプラグインオブジェクトを登録。"""
        if truthy(subscript):
            subscript = "[" + to_s(subscript) + "]"
        self._cell_port_throug_plugin_list[
            f"{to_s(cell_name)}.{to_s(port_name)}{to_s(subscript)}"
        ] = through_plugin_object

    def find_cell_port_through_plugin(
        self, cell_name: Any, port_name: Any, subscript: Any
    ) -> Any:
        if truthy(subscript):
            subscript = "[" + to_s(subscript) + "]"
        return self._cell_port_throug_plugin_list.get(
            f"{to_s(cell_name)}.{to_s(port_name)}{to_s(subscript)}"
        )

    def create_domain_plugin(self) -> None:
        if truthy(self._domain_type):
            self._domain_type.create_domain_plugin()

    def create_class_plugin(self) -> None:
        if truthy(self._class_type):
            self._class_type.create_class_plugin()

    def distance(self, to_region: Any) -> int | None:
        """to_region への距離（unreachable な場合 nil)。region#distance は require で用いられる。"""
        r1 = self  # 出発 region
        r2 = to_region  # 目的 region
        dist = 0

        if r1 is not r2:  # 同一 region なら呼出し可能
            f1 = r1.get_family_line()
            len1 = len(f1)
            f2 = r2.get_family_line()
            len2 = len(f2)

            # 不一致になるところ（兄弟）を探す
            i = 1  # i = 0 は :RootRegion なので必ず一致
            while i < len1 and i < len2:
                if f1[i] is not f2[i]:
                    break
                i += 1

            sibling_level = i  # 兄弟となるレベル、もしくはどちらか一方が終わったレベル

            # 呼び側について呼び元のレベルから兄弟レベルまで（out_through をチェックおよび挿入）
            i = len1 - 1
            while i >= sibling_level:
                dbg_print(f"going out from {to_s(f1[i].get_name())} level={i}\n")
                domain_type = f1[i].get_domain_type()
                class_type = f1[i].get_class_type()
                dbg_print(
                    f"distance: region={to_s(f1[i].get_name())} domain_type={to_s(domain_type)} "
                    f"class_type={to_s(class_type)}"
                )
                join_ok = False
                if truthy(domain_type):
                    if not domain_type.joinable(f1[i], f1[i - 1], Y.OUT_THROUGH):
                        return None
                    join_ok = True
                elif truthy(class_type):
                    if not class_type.joinable(f1[i], f1[i - 1], Y.OUT_THROUGH):
                        return None
                    join_ok = True
                if not join_ok and len(f1[i].get_out_through_list()) == 0:
                    return None
                i -= 1
                dist += 1

            # 兄弟レベルにおいて（to_through をチェックおよび挿入）
            a: Any = f1[sibling_level] if sibling_level < len1 else None
            b: Any = f2[sibling_level] if sibling_level < len2 else None
            if truthy(a) and truthy(b):
                dbg_print(f"going from {to_s(a.get_name())} to {to_s(b.get_name())}\n")
                domain_type = a.get_domain_type()
                class_type = a.get_class_type()
                join_ok = False
                if truthy(domain_type):
                    if not domain_type.joinable(f1[i], f1[i - 1], Y.TO_THROUGH):
                        return None
                    join_ok = True
                elif truthy(class_type):
                    if not class_type.joinable(f1[i], f1[i - 1], Y.TO_THROUGH):
                        return None
                    join_ok = True
                if not join_ok:
                    found = 0
                    for t in a.get_to_through_list():
                        if t[0][0] == b.get_name():  # region 名が一致するか ?
                            found = 1
                    for t in b.get_from_through_list():
                        if t[0][0] == a.get_name():  # region 名が一致するか ?
                            found = 1
                    if found == 0:
                        return None
                dist += 1

            # 受け側について兄弟レベルから受け側のレベルまで（in_through をチェックおよび挿入）
            i = sibling_level
            while i < len2:
                dbg_print(f"going in to {to_s(f2[i].get_name())} level={i}\n")
                domain_type = f2[i].get_domain_type()
                class_type = f2[i].get_class_type()
                join_ok = False
                if truthy(domain_type):
                    if not domain_type.joinable(f2[i - 1], f2[i], Y.IN_THROUGH):
                        return None
                    join_ok = True
                elif truthy(class_type):
                    if not class_type.joinable(f2[i - 1], f2[i], Y.IN_THROUGH):
                        return None
                    join_ok = True
                if not join_ok and len(f2[i].get_in_through_list()) == 0:
                    return None
                i += 1
                dist += 1

        dbg_print(
            f"dsitance={dist} from {to_s(r1.get_name())} to {to_s(r2.get_name())}\n"
        )
        return dist

    def is_sub_region_of(self, region: Any) -> bool:  # Ruby: is_sub_region_of?
        """self は、region の子リージョンか？"""
        while region is not self:
            if region.is_root():
                return True
            region = region.get_owner()
        return False

    def is_node_root(self) -> bool:  # Ruby: is_node_root?
        return any(r is self for r in Region._node_roots)

    def is_link_root(self) -> bool:  # Ruby: is_link_root?
        return any(r is self for r in Region._link_roots)

    def is_class_root(self) -> bool:
        return self._region_type == Y.NODE

    def is_domain_root(self) -> bool:
        return self._region_type == Y.NODE

    def show_tree(self, indent: int) -> None:
        super().show_tree(indent)
        rb_print("  " * (indent + 1))
        rb_puts(f"path: {self.get_path_string()}")
        rb_print("  " * (indent + 1))
        ns: Any = self.__dict__.get("_namespace")
        owner: Any = self._owner
        rb_puts(
            f"namespace: {to_s(ns.get_name()) if truthy(ns) else 'nil'}  "
            f"owner: {to_s(type(owner)) if owner is not None else 'NilClass'}."
            f"{to_s(owner.get_name()) if truthy(owner) else 'nil'}"
        )
        if truthy(self._domain_type):
            self._domain_type.show_tree(indent + 1)
        rb_print("  " * (indent + 1))
        rb_puts(
            f"domain_root={to_s(self._domain_root.get_name())} "
            f"class_root={to_s(self._class_root.get_name())}"
        )
