"""join.rb の移植。結合（`Join`。セルの呼び口の結合、または属性の初期化）。"""

from __future__ import annotations

import copy
from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context, print_exception
from tecsgen.core.generator import _get_at, _set_at
from tecsgen.core.plugin_module import PluginModule, PluginNotPorted, is_plugin_kind
from tecsgen.core.syntaxobj.node import BDNode
from tecsgen.ruby_compat import (
    RubyRuntimeError,
    Y,
    class_name,
    rb_print,
    rb_puts,
    sym,
    to_s,
    truthy,
)


def _is_int(x: Any) -> bool:
    return isinstance(x, int) and not isinstance(x, bool)


class Join(PluginModule, BDNode):
    """結合の左辺 @name:: string / @subscript:: nil: not array, -1: subscript not specified, >=0
    @definition:: Port, Decl(attribute or var)
    結合の右辺 @rhs:: Expression | initializer / @cell_name / @cell / @celltype / @port_name / @port
    @array_member:: rhs array / @array_member2:: Join array / @rhs_subscript:: nil or >=0
    @through_list:: @cp_through_list + @region_through_list + @ep_through_list
    @through_generated_list / @region_through_generated_list:: [Plugin_class object, ...]
    """

    _through_count: ClassVar[dict[Any, Any]] = {}
    # プラグインへの引数で渡さないものを、一時的に記憶しておく
    _plugin_creating_join: ClassVar[Any] = None
    _start_region: ClassVar[Any] = None
    _end_region: ClassVar[Any] = None
    _through_type: ClassVar[Any] = None
    _region_count: ClassVar[Any] = None

    @classmethod
    def reset(cls) -> None:
        Join._through_count = {}
        Join._plugin_creating_join = None
        Join._start_region = None
        Join._end_region = None
        Join._through_type = None
        Join._region_count = None

    def __init__(self, name: Any, subscript: Any, rhs: Any, locale: Any = None) -> None:
        """name:: 名前（属性名、呼び口名） / subscript:: Nil=非配列, -1="[]", N="[N]" / rhs:: 右辺の式"""
        from tecsgen.core.expression import Expression

        dbg_print(f"Join#new: {to_s(name)}, {to_s(subscript)}\n")

        super().__init__()
        if truthy(locale):
            self._locale = locale

        self._name = name
        if type(subscript) is Expression:
            # mikan 配列添数が整数であることを未チェック
            self._subscript = subscript.eval_const(None)
            if self._subscript is None:
                self.cdl_error("S1099 array subscript not constant")
        else:
            self._subscript = subscript

        self._rhs = rhs
        self._definition: Any = None

        # 配列要素を設定
        if _is_int(self._subscript) and self._subscript == -1:
            self._array_member: Any = [self]
            self._array_member2: Any = [self]
        elif self._subscript is not None:
            self._array_member = []
            self._array_member2 = []
            _set_at(self._array_member, self._subscript, self)
            _set_at(self._array_member2, self._subscript, self)

        self._through_list: list[Any] = []
        self._cp_through_list: list[Any] = []
        self._ep_through_list: list[Any] = []
        self._region_through_list: list[Any] = []
        self._through_generated_list: list[Any] = []
        self._region_through_generated_list: list[Any] = []

    def set_definition(self, definition: Any) -> None:
        """左辺に対応する celltype の定義を設定するとともにチェックする（STAGE: S）。

        definition:: Decl (attribute,varの時) または Port (callの時) または nil
        """
        from tecsgen.core.componentobj.port import Port
        from tecsgen.core.syntaxobj.decl import Decl

        dbg_print(
            f"set_definition: {to_s(self._owner.get_name())}.{to_s(self._name)} = "
            f"{'NilClass' if definition is None else class_name(type(definition))}\n"
        )

        # 二重チェックの防止
        if truthy(self._definition):
            return

        self._definition = definition

        # mikan 左辺値、右辺値の型チェックなど
        if type(self._definition) is Decl:
            self.check_var_init()
        elif type(self._definition) is Port:
            self.check_call_port_init()
            if (
                self._definition.get_port_type() == Y.CALL
            ):  # :ENTRY ならエラー。無視しない
                self.check_and_gen_through()
                self.create_allocator_join()
        elif self._definition is None:
            self.cdl_error("S1117 '$1' not in celltype", self._name)
        else:
            raise RubyRuntimeError("UnknownToken")

    def check_var_init(self) -> None:
        """変数の初期化チェック。"""
        if self._definition.get_kind() == Y.ATTRIBUTE:
            # 右辺で初期化可能かチェック
            self._definition.get_type().check_init(
                self._locale, self._definition.get_identifier(), self._rhs, Y.ATTRIBUTE
            )
        elif self._definition.get_kind() == Y.VAR:
            # var は初期化できない
            self.cdl_error("S1100 $1: cannot initialize var", self._name)
        else:
            raise RubyRuntimeError("UnknownDeclKind")

    def check_call_port_init(self) -> None:
        """呼び口の初期化チェック。"""
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.port import Port
        from tecsgen.core.expression import Expression

        dbg_print(
            f"Join#check_call_port_init:cell.call={to_s(self._owner.get_name())}.{to_s(self._name)}\n"
        )

        # 左辺は受け口か（受け口を初期化しようとしている）？
        if self._definition.get_port_type() == Y.ENTRY:
            self.cdl_error("S1101 '$1' cannot initialize entry port", self._name)
            return

        # 配列添数の整合性チェック
        as_ = self._definition.get_array_size()
        if self._subscript is None and as_ is not None:
            self.cdl_error("S1102 $1: must specify array subscript here", self._name)
        elif self._subscript is not None and as_ is None:
            self.cdl_error("S1103 $1: cannot specify array subscript here", self._name)

        # 右辺がない（以前の段階でエラー）
        if not truthy(self._rhs):
            return

        # cCall = composite.cCall; のチェック．この形式は属性用
        if type(self._rhs) is list and self._rhs and self._rhs[0] == Y.COMPOSITE:
            self.cdl_error(
                "S1107 to export port '$1', use 'cCall => composite.cCall'", self._name
            )
            return
        elif type(self._rhs) is not Expression:
            raise RubyRuntimeError("Unknown bug. specify -t to find problem in source")

        # 右辺の Expression の要素を取り出す
        ret = self._rhs.analyze_cell_join_expression()
        if ret is None:  # 1
            self.cdl_error("S1108 $1: rhs not 'Cell.ePort' form", self._name)
            return

        nsp, self._rhs_subscript, self._port_name = ret[0], ret[1], ret[2]
        self._cell_name = nsp.get_name()  # mikan ns::cellname の形式の考慮

        # composite の定義の中なら object は結合先 cell か、見つからなければ nil が返る
        # composite の定義外なら false が返る
        obj = CompositeCelltype.find(self._cell_name)
        if obj is False:
            obj = Namespace.find(nsp)  # 1
        elif len(nsp.get_path()) != 1:
            self.cdl_error("$1 cannot have path", nsp.get_path_str())

        if obj is None:  # (2)
            self.cdl_error("S1109 '$1' not found", to_s(nsp))
        elif type(obj) is not Cell:  # (3)
            self.cdl_error("S1110 '$1' not cell", to_s(nsp))
        else:
            dbg_print(
                f"set_definition: set_f_ref {to_s(self._owner.get_name())}.{to_s(self._name)} => {to_s(obj.get_name())}\n"
            )
            obj.set_f_ref()

            # 右辺のセルのセルタイプ
            celltype = obj.get_celltype()

            if truthy(celltype):  # (4)
                object2 = celltype.find(self._port_name)
                if object2 is None:  # (5)
                    self.cdl_error("S1111 '$1' not found", self._port_name)
                # Ruby 版は `! object2.instance_of? Port || object2.get_port_type != :ENTRY` と
                # 括弧なしで書いているので `!object2.instance_of?(Port || ...)` と解釈され、
                # 受け口かどうかの判定は行われない（そのまま再現する）
                elif type(object2) is not Port:  # (6)
                    self.cdl_error("S1112 '$1' not entry port", self._port_name)
                elif (
                    self._definition.get_signature() is not object2.get_signature()
                ):  # (7)
                    self.cdl_error("S1113 '$1' signature mismatch", self._port_name)
                elif truthy(object2.get_array_size()):  # (8)
                    # 受け口配列
                    if not truthy(self._rhs_subscript):
                        # 右辺に添数指定がなかった
                        self.cdl_error("S1114 '$1' should be array", self._port_name)
                    else:
                        as_ = object2.get_array_size()
                        if _is_int(as_) and as_ <= self._rhs_subscript:
                            # 受け口配列の大きさに対し、右辺の添数が同じか大きい
                            self.cdl_error(
                                "S1115 $1[$2]: subscript out of range (< $3)",
                                self._port_name,
                                self._rhs_subscript,
                                as_,
                            )
                        else:
                            dbg_print(
                                f"Join OK {to_s(self._owner.get_name())}.{to_s(self._name)}[{to_s(self._rhs_subscript)}] = "
                                f"{to_s(obj.get_name())}.{to_s(self._port_name)} #<Join>\n"
                            )
                            self._cell = obj
                            self._celltype = celltype
                            self._port = object2
                            # 右辺のセルの受け口 object2 を参照済みにする
                            self._cell.set_entry_port_max_subscript(
                                self._port, self._rhs_subscript
                            )

                        dbg_print(
                            f"Join set_definition: rhs: #<Cell>  "
                            f"{to_s(self._cell.get_name()) if truthy(self._cell) else ''}\n"
                        )
                elif truthy(self._rhs_subscript):
                    # 受け口配列でないのに右辺で添数指定されている
                    self.cdl_error(
                        "S1116 '$1' entry port is not array", self._port_name
                    )
                else:
                    dbg_print(
                        f"Join OK {to_s(self._owner.get_name())}.{to_s(self._name)} = "
                        f"{to_s(obj.get_name())}.{to_s(self._port_name)} #<Join>\n"
                    )
                    self._cell = obj
                    self._port = object2
                    self._celltype = celltype

            if not is_plugin_kind(self._owner.get_plugin(), "ThroughPlugin"):
                # 受け口の through を設定
                dbg_print(
                    f"ep_through_list: cell={to_s(obj.get_name())} len={len(obj.get_ep_through_list())}\n"
                )
                for ent in obj.get_ep_through_list():
                    dbg_print(
                        f"Join name={to_s(self._name)} port_name={to_s(_call(self._port, 'get_name'))} "
                        f"ep_through={to_s(ent[0])}\n"
                    )
                    if ent[0] == _call(self._port, "get_name"):
                        plugin_name = to_s(ent[1])
                        cell_name = sym(f"{to_s(ent[1])}_")
                        plugin_arg = ent[2]
                        rb_print(f"ep_through: plugin_name={plugin_name}\n")
                        self._ep_through_list.append(
                            [plugin_name, cell_name, plugin_arg]
                        )
            self.check_region(obj)

    def create_allocator_join(self) -> None:
        """アロケータの結合を生成（STAGE: S。呼び口側に生成されるアロケータ呼び口の結合を生成）。"""
        cell = self.get_rhs_cell2()  # 右辺のセルを得る
        port = self.get_rhs_port2()

        if truthy(cell) and truthy(
            cell.get_allocator_list()
        ):  # cell == nil なら既にエラー
            dbg_print(
                f"create_allocator_join: {to_s(self._owner.get_name())}.{to_s(self._name)}=>"
                f"{to_s(cell.get_name()) if truthy(cell) else 'nil'}\n"
            )
            for a in cell.get_allocator_list():
                if a[1] == port and _eq(a[2], self._rhs_subscript):
                    # 名前の一致するものの結合を生成する
                    cp_name = sym(f"{to_s(self._name)}_{to_s(a[3])}_{to_s(a[4])}")
                    join = Join(cp_name, self._subscript, a[5], self._locale)
                    dbg_print(
                        f"create_allocator_join: {to_s(self._owner.get_name())}.{to_s(cp_name)} "
                        f"[{to_s(self._subscript)}] {to_s(self._name)}\n"
                    )
                    self._owner.new_join(join)
                else:
                    dbg_print(
                        f"create_allocator_join:3 not {to_s(self._owner.get_name())}.{to_s(a[1])} {to_s(self._name)}\n"
                    )

    def check_region(self, obj: Any) -> None:
        """リージョン間の結合をチェック（リージョン間の through による @region_through_list の作成）。"""
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        dbg_print(
            f"check_region {to_s(self._owner.get_name())}.{to_s(self._name)} => {to_s(obj.get_name())}\n"
        )

        # プラグインで生成されたなかでは生成しない
        if is_plugin_kind(self._owner.get_plugin(), "ThroughPlugin"):
            return  # プラグイン生成されたセルの場合、結合チェックのみ

        # region のチェック
        r1 = self._owner.get_region()  # 呼び口セルの region
        r2 = obj.get_region()  # 受け口セルの region

        if r1 is r2:  # 同一 region なら呼出し可能
            return

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

        dbg_print(f"sibling_level: {i}\n")
        if truthy(_at(f1, i)):
            dbg_print(f"from: {to_s(f1[i].get_name())}\n")
        if truthy(_at(f2, i)):
            dbg_print(f"to: {to_s(f2[i].get_name())}\n")

        b_to_through = truthy(_at(f1, sibling_level)) and truthy(_at(f2, sibling_level))

        # 呼び側について呼び元のレベルから兄弟レベルまで（out_through をチェックおよび挿入）
        i = len1 - 1
        end_level = sibling_level if b_to_through else sibling_level - 1
        domain_through: Any = None
        class_through: Any = None
        while i > end_level:
            dbg_print(f"going out from {to_s(f1[i].get_name())} level={i}\n")
            region_count = f1[i].next_out_through_count()
            out_through_list = f1[
                i
            ].get_out_through_list()  # [ plugin_name, plugin_arg ]
            domain_type = f1[i].get_domain_type()
            class_type = f1[i].get_class_type()
            if truthy(domain_type):
                domain_through = domain_type.add_through_plugin(
                    self, f1[i], f1[i - 1], Y.OUT_THROUGH
                )
                if domain_through is None:
                    self.cdl_error(
                        "S9999 $1: going out from regin '$2' not permitted by domain '$3'",
                        self._name,
                        f1[i].get_name(),
                        domain_type.get_name(),
                    )
            elif truthy(class_type):
                class_through = class_type.add_through_plugin(
                    self, f1[i], f1[i - 1], Y.OUT_THROUGH
                )
                if class_through is None:
                    self.cdl_error(
                        "S9999 $1: going out from regin '$2' not permitted by class '$3'",
                        self._name,
                        f1[i].get_name(),
                        class_type.get_name(),
                    )
            elif len(out_through_list) == 0:
                self.cdl_error(
                    "S1118 $1: going out from region '$2' not permitted",
                    self._name,
                    f1[i].get_name(),
                )

            for ol in out_through_list:
                if truthy(ol[0]):  # plugin_name が指定されていなければ登録しない
                    plugin_arg = CDLString.remove_dquote(ol[1])
                    through = [
                        ol[0],
                        Y.Join_out_through_,
                        plugin_arg,
                        f1[i],
                        f1[i - 1],
                        Y.OUT_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
            if truthy(domain_through) and len(domain_through) > 0:
                through = [
                    domain_through[0],
                    Y.Join_domain_out_through_,
                    domain_through[1],
                    f1[i],
                    f1[i - 1],
                    Y.OUT_THROUGH,
                    region_count,
                ]
                self._region_through_list.append(through)
            if truthy(class_through) and len(class_through) > 0:
                through = [
                    class_through[0],
                    Y.Join_class_out_through_,
                    class_through[1],
                    f1[i],
                    f1[i - 1],
                    Y.OUT_THROUGH,
                    region_count,
                ]
                self._region_through_list.append(through)
            i -= 1

        # 兄弟レベルにおいて（to_through をチェックおよび挿入）
        a = _at(f1, sibling_level)
        b = _at(f2, sibling_level)
        if truthy(a) and truthy(b):
            dbg_print(f"going from {to_s(a.get_name())} to {to_s(b.get_name())}\n")
            found = 0
            region_count = f1[i].next_to_through_count(
                b.get_name()
            )  # to_through の region カウント
            for t in a.get_to_through_list():
                if t[0][0] == b.get_name():  # region 名が一致するか ?
                    if truthy(t[1]):  # plugin_name が指定されていなければ登録しない
                        plugin_arg = CDLString.remove_dquote(t[2])
                        through = [
                            t[1],
                            Y.Join_to_through__,
                            plugin_arg,
                            a,
                            b,
                            Y.TO_THROUGH,
                            region_count,
                        ]
                        self._region_through_list.append(through)
                    found = 1
            domain_type = a.get_domain_type()
            class_type = a.get_class_type()
            if truthy(domain_type):
                domain_through = domain_type.add_through_plugin(
                    self, a, b, Y.TO_THROUGH
                )
                if domain_through is None:
                    self.cdl_error(
                        "S9999 $1: going from regin '$2' not permitted by domain'$3'",
                        self._name,
                        a.get_name(),
                        b.get_domain_type().get_name(),
                    )
                if truthy(domain_through) and len(domain_through) > 0:
                    through = [
                        domain_through[0],
                        Y.Join_domain_to_through_,
                        domain_through[1],
                        a,
                        b,
                        Y.TO_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
                found = 1  # ２重エラー抑制のため、いずれにせよ found とする
            elif truthy(class_type):
                class_through = class_type.add_through_plugin(self, a, b, Y.TO_THROUGH)
                if class_through is None:
                    self.cdl_error(
                        "S9999 $1: going from regin '$2' not permitted by class'$3'",
                        self._name,
                        a.get_name(),
                        b.get_class_type().get_name(),
                    )
                if truthy(class_through) and len(class_through) > 0:
                    through = [
                        class_through[0],
                        Y.Join_class_to_through_,
                        class_through[1],
                        a,
                        b,
                        Y.TO_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
                found = 1
            region_count = f2[i].next_from_through_count(
                a.get_name()
            )  # form_through の region カウント
            for t in b.get_from_through_list():
                if t[0][0] == a.get_name():  # region 名が一致するか ?
                    if truthy(t[1]):
                        plugin_arg = CDLString.remove_dquote(t[2])
                        through = [
                            t[1],
                            Y.Join_from_through__,
                            plugin_arg,
                            a,
                            b,
                            Y.FROM_THROUGH,
                            region_count,
                        ]
                        self._region_through_list.append(through)
                    found = 1

            if found == 0:
                self.cdl_error(
                    "S1119 $1: going from region '$2' to '$3' not permitted",
                    self._name,
                    a.get_name(),
                    b.get_name(),
                )

        # 受け側について兄弟レベルから受け側のレベルまで（in_through をチェックおよび挿入）
        i = sibling_level + 1 if b_to_through else sibling_level
        while i < len2:
            dbg_print(f"going in to {to_s(f2[i].get_name())} level={i}\n")
            region_count = f2[i].next_in_through_count()
            in_through_list = f2[i].get_in_through_list()  # [ plugin_name, plugin_arg ]
            domain_type = f2[i].get_domain_type()
            class_type = f2[i].get_class_type()
            if truthy(domain_type):
                domain_through = domain_type.add_through_plugin(
                    self, f2[i - 1], f2[i], Y.IN_THROUGH
                )
                if domain_through is None:
                    self.cdl_error(
                        "S9999 $1: going in from regin '$2' to '$3' not permitted by domain '$4'",
                        self._name,
                        f2[i - 1].get_name(),
                        f2[i].get_name(),
                        domain_type.get_name(),
                    )
                if truthy(domain_through) and len(domain_through) > 0:
                    through = [
                        domain_through[0],
                        Y.Join_domain_in_through_,
                        domain_through[1],
                        f2[i - 1],
                        f2[i],
                        Y.IN_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
            elif truthy(class_type):
                class_through = class_type.add_through_plugin(
                    self, f2[i - 1], f2[i], Y.IN_THROUGH
                )
                if class_through is None:
                    self.cdl_error(
                        "S9999 $1: going in from regin '$2' to '$3' not permitted by class '$4'",
                        self._name,
                        f2[i - 1].get_name(),
                        f2[i].get_name(),
                        class_type.get_name(),
                    )
                if truthy(class_through) and len(class_through) > 0:
                    through = [
                        class_through[0],
                        Y.Join_class_in_through_,
                        class_through[1],
                        f2[i - 1],
                        f2[i],
                        Y.IN_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
            elif len(in_through_list) == 0:
                self.cdl_error(
                    "S1120 $1: going in to region '$2' not permitted",
                    self._name,
                    f2[i].get_name(),
                )
            for il in in_through_list:
                if truthy(il[0]):  # plugin_name が指定されていなければ登録しない
                    plugin_arg = CDLString.remove_dquote(il[1])
                    through = [
                        il[0],
                        Y.Join_in_through_,
                        plugin_arg,
                        f2[i - 1],
                        f2[i],
                        Y.IN_THROUGH,
                        region_count,
                    ]
                    self._region_through_list.append(through)
            i += 1

    def check_region2(self) -> None:
        """生成しないリージョンへの結合かチェック（右辺のセルが、生成されないリージョンにあればエラー）。"""
        lhs_cell = self._owner

        rhs_region = self.get_rhs_region()
        if truthy(rhs_region):
            dbg_print(
                f"check_region2 {to_s(lhs_cell.get_name())} => {rhs_region.get_path_string()}{to_s(self._rhs)}\n"
            )
            if (
                self._owner.get_region().get_link_root()
                is not self.get_rhs_region().get_link_root()
            ):
                self.cdl_error(
                    "S1121 '$1' in region '$2' cannot be directly joined $3 in  $4",
                    lhs_cell.get_name(),
                    lhs_cell.get_region().get_namespace_path().get_path_str(),
                    to_s(self._rhs),
                    self.get_rhs_region().get_namespace_path().get_path_str(),
                )

    def get_definition(self) -> Any:
        return self._definition

    def set_specifier_list(self, specifier_list: list[Any]) -> None:
        """specifier を設定（STAGE: B。through 指定子を設定）。"""
        from tecsgen.core.syntaxobj.cdlstring import CDLString

        for s in specifier_list:
            if s[0] == Y.THROUGH:
                # set plugin_name（先頭文字を大文字に : ruby のクラス名の制約）
                plugin_name = to_s(s[1])
                if plugin_name:
                    plugin_name = plugin_name[0].upper() + plugin_name[1:]
                # set cell_name
                cell_name = sym(f"{to_s(s[1])}_")
                # set plugin_arg
                plugin_arg = CDLString.remove_dquote(to_s(s[2]))
                self._cp_through_list.append([plugin_name, cell_name, plugin_arg])

    def check_and_gen_through(self) -> None:
        """through のチェックと生成。"""
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.port import Port

        dbg_print(
            f"check_and_gen_through {to_s(self._owner.get_name())}.{to_s(self._name)}\n"
        )

        if type(self._definition) is not Port:
            self.cdl_error(
                "S1123 $1 : not port: 'through' can be specified only for port",
                self._name,
            )
            return
        if len(self._cp_through_list) > 0:
            # is_empty? must check before is_omit?
            sig = self._definition.get_signature()
            if truthy(sig) and sig.is_empty():
                self.cdl_warning(
                    "W9999 'through' is specified for empty signature, ignored"
                )
                return
            if truthy(self._definition.is_omit()):
                self.cdl_warning(
                    "W9999 'through' is specified for omitted port, ignored"
                )
                return

        self._through_list = (
            self._cp_through_list + self._region_through_list + self._ep_through_list
        )

        length = len(self._through_list)  # through が連接している数
        cp_len = len(self._cp_through_list)
        rgn_len = len(self._region_through_list)

        if self._owner.is_in_composite() and length > 0:
            self.cdl_error(
                "S1177 cannot specify 'through' in composite in current version"
            )
            return

        # 連続した through について、受け口側から順にセルを生成し解釈する
        i = length - 1
        while i >= 0:
            through = self._through_list[i]
            plugin_name = through[0]

            if i != length - 1:
                try:
                    gen = _get_at(self._through_generated_list, i + 1)
                    next_cell_nsp = gen.get_cell_namespace_path()
                    next_port_name = gen.get_through_entry_port_name()
                    next_port_subscript = gen.get_through_entry_port_subscript()
                except PluginNotPorted:
                    raise
                except Exception as evar:  # noqa: BLE001  Ruby の rescue Exception
                    self.cdl_error(
                        "S1124 $1: plugin function failed: 'get_through_entry_port_name'",
                        plugin_name,
                    )
                    print_exception(evar)
                    i -= 1
                    continue

                next_cell = Namespace.find(next_cell_nsp)  # 1
                if next_cell is None:
                    self.cdl_error(
                        "S1125 $1: not generated cell '$2'",
                        type(_get_at(self._through_generated_list, i + 1)),
                        next_cell_nsp.get_path_str(),
                    )
                    return
            else:
                # 最後のセルの場合、次のセルの名前、ポート名
                next_cell = self._cell
                next_port_name = self._port_name
                next_port_subscript = self._rhs_subscript
                if next_cell is None:
                    return  # 結合先がない

            if i < cp_len:
                prev_region = self._owner.get_region()  # 呼び元セルのリージョン
            elif i < (cp_len + rgn_len):
                prev_region = self._through_list[i][3]  # region 間プラグイン
            elif rgn_len > 0:
                prev_region = self._through_list[cp_len + rgn_len - 1][3]
            else:
                prev_region = self._owner.get_region()

            if cp_len <= i < (cp_len + rgn_len):
                # region から @cell_name.@port_name への through がないか探す
                rp = self._through_list[i][3].find_cell_port_through_plugin(
                    self._cell.get_global_name(), self._port_name, self._rhs_subscript
                )
            else:
                rp = None

            if rp is None:
                pl_class = self.load_plugin(plugin_name, "ThroughPlugin")
                if truthy(pl_class):
                    self.gen_through_cell_code_and_parse(
                        plugin_name,
                        i,
                        prev_region,
                        next_cell,
                        next_port_name,
                        next_port_subscript,
                        pl_class,
                    )
            else:
                _set_at(self._through_generated_list, i, rp)  # 見つかったものを共用する

            if cp_len <= i < (cp_len + rgn_len):
                _set_at(
                    self._region_through_generated_list,
                    i - cp_len,
                    _get_at(self._through_generated_list, i),
                )
                if rp is None:
                    self._through_list[i][3].add_cell_port_through_plugin(
                        self._cell.get_global_name(),
                        self._port_name,
                        self._rhs_subscript,
                        _get_at(self._through_generated_list, i),
                    )

            if i == 0:
                # 最も呼び口側のセルは、CDL 上の結合がないため、参照されたことにならない
                if _get_at(self._through_generated_list, 0) is None:
                    return  # plugin_object の生成に失敗している
                cell = Namespace.find(
                    self._through_generated_list[0].get_cell_namespace_path()
                )  # 1
                if type(cell) is Cell:
                    cell.set_f_ref()

            i -= 1

    def get_through_count(self, name: Any) -> int:
        s = sym(name)
        if truthy(Join._through_count.get(s)):
            Join._through_count[s] += 1
        else:
            Join._through_count[s] = 0
        return Join._through_count[s]

    def gen_through_cell_code_and_parse(
        self,
        plugin_name: Any,
        i: int,
        prev_region: Any,
        next_cell: Any,
        next_port_name: Any,
        next_port_subscript: Any,
        pl_class: Any,
    ) -> None:
        """through プラグインを呼び出して CDL 生成させるとともに、import する（P5 で使う）。"""
        through = self._through_list[i]
        plugin_name = through[0]
        generating_cell_name = sym(
            f"{to_s(through[1])}_{self.get_through_count(through[1])}"
        )
        plugin_arg = through[2]
        Join._start_region = prev_region
        if truthy(_at(through, 3)):
            # region 間の through の場合
            if next_cell.get_region() is Join._start_region:
                Join._end_region = Join._start_region
            else:
                Join._end_region = through[4]
            Join._through_type = through[5]
            Join._region_count = through[6]
        else:
            # 呼び口の through の場合
            Join._end_region = next_cell.get_region()  # 次のセルの region
            Join._through_type = Y.THROUGH  # 呼び口の through 指定
            Join._region_count = 0
        Join._plugin_creating_join = self
        caller_cell = self._owner

        try:
            plugin_object = pl_class(
                sym(generating_cell_name),
                to_s(plugin_arg),
                next_cell,
                sym(next_port_name),
                next_port_subscript,
                self._definition.get_signature(),
                self._celltype,
                caller_cell,
            )
            plugin_object.set_locale(self._locale)
        except PluginNotPorted:
            raise
        except Exception as evar:  # noqa: BLE001
            self.cdl_error("S1126 $1: fail to new", plugin_name)
            if (
                truthy(self._celltype)
                and truthy(self._definition.get_signature())
                and truthy(caller_cell)
                and truthy(next_cell)
            ):
                rb_print(
                    f"signature: {to_s(self._definition.get_signature().get_name())} from: "
                    f"{to_s(caller_cell.get_name())} to: {to_s(next_cell.get_name())} of celltype: "
                    f"{to_s(self._celltype.get_name())}\n"
                )
            print_exception(evar)
            return

        _set_at(self._through_generated_list, i, plugin_object)
        self.generate_and_parse(plugin_object)

    @classmethod
    def set_through_info(cls, plugin_object: Any) -> None:
        """ThroughPlugin の追加情報を設定する（ThroughPlugin#initialize から呼び出される）。"""
        plugin_object.set_through_info(
            Join._start_region,
            Join._end_region,
            Join._through_type,
            Join._plugin_creating_join,
            Join._plugin_creating_join.get_cell(),
            Join._region_count,
        )

    def get_name(self) -> Any:
        return self._name

    def get_subscript(self) -> Any:
        """配列添数を得る（@subscript の説明を参照のこと）。"""
        return self._subscript

    def get_cell_name(self) -> Any:  # 受け口セル名
        return self._cell_name

    def get_celltype(self) -> Any:
        return self._celltype

    def get_cell(self) -> Any:
        return self._cell

    def get_rhs_cell(self) -> Any:
        """右辺の実セルを得る（through で挿入されたもの、composite の内部など実際に結合される先）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if truthy(_at(self._through_list, 0)):
            gen = _at(self._through_generated_list, 0)
            if truthy(gen):
                cell = Namespace.find(gen.get_cell_namespace_path())  # 1
                return _call(cell, "get_real_cell", gen.get_through_entry_port_name())
            return None  # generate に失敗している
        if truthy(self._cell):
            return self._cell.get_real_cell(self._port_name)
        return None

    def get_rhs_cell2(self) -> Any:
        """右辺のセルを得る（composite 展開されていない）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if truthy(_at(self._through_list, 0)):
            gen = _at(self._through_generated_list, 0)
            if truthy(gen):
                return Namespace.find(gen.get_cell_namespace_path())  # 1
            return self._cell  # generate に失敗している
        return self._cell

    def get_rhs_cell3(self) -> Any:
        """右辺のセルを得る（through は適用しないが、composite は展開した後のセル）。"""
        if truthy(self._cell):
            return self._cell.get_real_cell(self._port_name)
        return None

    def get_rhs_region(self) -> Any:
        """右辺のセルのリージョンを得る（右辺が未定義の場合、nil を返す）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if truthy(_at(self._through_list, 0)):
            gen = _at(self._through_generated_list, 0)
            if truthy(gen):
                cell = Namespace.find(gen.get_cell_namespace_path())  # 1
                if truthy(cell):
                    return cell.get_region()
            else:
                return None  # generate に失敗している
        elif truthy(self._cell):
            return self._cell.get_region()
        return None

    def get_cell_global_name(self) -> Any:
        """受け口セル名（コンポジットなら展開した内側のセル）。"""
        dbg_print(f"cell get_cell_global_name:  {to_s(self._cell_name)}\n")
        if truthy(self._cell):
            return self._cell.get_real_global_name(self._port_name)
        return "NonDefinedCell?"

    def get_port_global_name(self, subscript: Any = None) -> Any:
        """結合の右辺の受け口の名前（コンポジットなら展開した内側のセル）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        dbg_print(f"Cell get_port_global_name:  {to_s(self._cell_name)}\n")
        if truthy(_at(self._through_list, 0)):
            gen = self._through_generated_list[0]
            cell = Namespace.find(gen.get_cell_namespace_path())  # 1
            return cell.get_real_global_port_name(gen.get_through_entry_port_name())
        if truthy(self._cell):
            return self._cell.get_real_global_port_name(self._port_name)
        return "UndefinedCellsPort?"

    def get_port_name(self) -> Any:
        return self._port_name

    def get_rhs(self) -> Any:
        return self._rhs

    def get_rhs_cell1(self) -> Any:  # get_cell と同じ
        return self._cell

    def get_rhs_port1(self) -> Any:  # get_port_name 同じ
        return self._port_name

    def get_rhs_subscript1(self) -> Any:
        return self._rhs_subscript

    def get_rhs_port(self) -> Any:
        """右辺のポートを得る（composite は内部の繋がるセルのポート, through は挿入されたセルのポート）。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if truthy(_at(self._through_list, 0)):
            gen = self._through_generated_list[0]
            cell = Namespace.find(gen.get_cell_namespace_path())  # 1
            return cell.get_real_port(gen.get_through_entry_port_name())
        return self._cell.get_real_port(self._port_name)

    def get_rhs_subscript(self) -> Any:
        """右辺の配列添数を得る（through の場合は挿入されたセルの添数）。"""
        if truthy(_at(self._through_list, 0)):
            return self._through_generated_list[0].get_through_entry_port_subscript()
        return self._rhs_subscript

    def get_rhs_port2(self) -> Any:
        """右辺のポートを得る（プロトタイプ宣言しかされていない場合には、こちらしか使えない）。"""
        if truthy(_at(self._through_list, 0)):
            gen = _at(self._through_generated_list, 0)
            if truthy(gen):
                return sym(gen.get_through_entry_port_name())
            return self._port_name  # generate に失敗している
        return self._port_name

    def get_rhs_port3(self) -> Any:
        """右辺のポートを得る（through は適用しないが、composite は展開した後のセルの対応するポート）。"""
        if truthy(self._cell):
            return self._cell.get_real_port(self._port_name)
        return None

    def add_array_member(self, join2: Any) -> None:
        """呼び口配列の2番目以降の要素を追加する（非配列の場合も呼出される：join 重複エラー）。"""
        subscript2 = join2.get_subscript()  # join2 の左辺添数

        if self._subscript is None:  # not array : initialize duplicate
            self.cdl_error("S1127 '$1' duplicate", self._name)
        elif self._subscript >= 0:
            # 添数指定ありの場合
            if subscript2 is None or subscript2 < 0:
                # join2 左辺は非配列または添数なし
                self.cdl_error("S1128 '$1' inconsistent array definition", self._name)
            elif _get_at(self._array_member, subscript2) is not None:
                # 同じ添数が既に定義済み
                self.cdl_error(
                    "S1129 '$1' redefinition of subscript $2", self._name, subscript2
                )
            else:
                # 添数の位置に要素を追加
                _set_at(self._array_member, subscript2, join2.get_rhs())
                _set_at(self._array_member2, subscript2, join2)
        else:
            # 添数指定なしの場合
            if subscript2 is None or subscript2 >= 0:
                self.cdl_error("S1130 'R1' inconsistent array definition", self._name)
            # 添数なし配列の場合、配列要素を追加
            self._array_member.append(join2.get_rhs())
            self._array_member2.append(join2)

    def get_array_member(self) -> Any:
        return self._array_member

    def get_array_member2(self) -> Any:
        return self._array_member2

    def change_name(self, name: Any) -> None:
        dbg_print(f"change_name: {to_s(self._name)} to {to_s(name)}\n")
        self._name = name
        if truthy(self._array_member2):
            i = 0
            while i < len(self._array_member2):
                if (
                    self._array_member2[i] is not self
                    and _get_at(self._array_member, i) is not None
                ):
                    self._array_member2[i].change_name(name)
                i += 1

    def change_rhs_port(self, clone_cell_list: Any, celltype: Any) -> None:
        """composite cell を展開したセルの結合を clone したセルの名前に変更。"""
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        dbg_print(f"change_rhs_port: name={to_s(self._name)}\n")

        if get_context().debug:
            rb_print("============\n")
            rb_print(
                f"CHANGE_RHS change_rhs name: {to_s(self._owner.get_name())}.{to_s(self._name)}  "
                f"rhs cell_name: {to_s(self._cell_name)} #<Cell> #<Join>\n"
            )
            for cell, ce in clone_cell_list.items():
                rb_print(
                    f"   CHANGE_RHS  change_rhs:  {to_s(cell.get_name())}=#<Cell> : {to_s(ce.get_name())}\n"
                )
            rb_print("============\n")

        c = clone_cell_list.get(self._cell) if self._cell is not None else None
        if c is None:
            return

        dbg_print(
            f"  REWRITE cell_name:  {to_s(self._owner.get_name())}   {to_s(self._cell_name)} => "
            f"{to_s(c.get_global_name())}, {to_s(c.get_name())}\n"
        )

        # @rhs の内容を調整しておく（この内容は、subscript を除いて、後から使われていない）
        elements = self._rhs.get_elements()
        if elements[0] == Y.OP_SUBSC:  # 右辺：受け口配列？
            elements = elements[1]

        # 右辺が　cell.ePort の形式でない
        if elements[0] != Y.OP_DOT or elements[1][0] != Y.IDENTIFIER:  # 1
            return
        # セル名を composite 内部の名前から、外部の名前に入れ替える
        elements[1][1] = NamespacePath(c.get_name(), False, c.get_namespace())

        self._cell_name = c.get_name()
        self._cell = c

        if truthy(self._array_member2):
            dbg_print(f"array_member2.len : {len(self._array_member)}\n")
            i = 0
            while i < len(self._array_member2):
                if (
                    self._array_member2[i] is not self
                    and _get_at(self._array_member, i) is not None
                ):
                    dbg_print(
                        f"change_rhs array_member {i}: {to_s(self._name)}  {to_s(self._cell_name)}\n"
                    )
                    self._array_member2[i].change_rhs_port(clone_cell_list, celltype)
                i += 1

    def clone_for_composite(
        self, ct_name: Any, cell_name: Any, locale: Any, b_need_recursive: bool = True
    ) -> Join:
        """composite セル用にクローン（右辺の C_EXP に含まれる $id$, $cell$, $ct$ を置換）。"""
        from tecsgen.core.syntaxobj.cdlinitializer import CDLInitializer

        dbg_print(
            f"=====  clone_for_composite: {to_s(self._name)} {to_s(self._cell_name)} #<Join>   =====\n"
        )
        cl = copy.copy(self)

        if truthy(self._array_member2) and b_need_recursive:
            cl.clone_array_member(ct_name, cell_name, self, locale)

        rhs = CDLInitializer.clone_for_composite(self._rhs, ct_name, cell_name, locale)
        cl.change_rhs(rhs)

        dbg_print("join cloned : #<Join>\n")
        return cl

    def clone_array_member(
        self, ct_name: Any, cell_name: Any, prev: Any, locale: Any
    ) -> None:
        # 配列のコピーを作る
        am = list(self._array_member)
        am2 = list(self._array_member2)

        # 配列要素のコピーを作る
        i = 0
        while i < len(am2):
            if self._array_member2[i] is prev:
                # 自分自身である（ので、呼出すと無限再帰呼出しとなる）
                am2[i] = self
                _set_at(am, i, am2[i].get_rhs())
            elif truthy(self._array_member2[i]):
                am2[i] = self._array_member2[i].clone_for_composite(
                    ct_name, cell_name, locale, True
                )
                _set_at(am, i, am2[i].get_rhs())
            dbg_print(
                f"clone_array_member: {to_s(self._name)} subsript={i} #<Join> #<Join>\n"
            )
            i += 1

        self._array_member = am
        self._array_member2 = am2

    def change_rhs(self, rhs: Any) -> None:
        """rhs を入れ換える（composite で cell の属性の初期値を attribute の値で置き換える）。"""
        self._rhs = rhs

    def set_cloned(self, owner: Any) -> None:
        """clone された join の owner を変更。"""
        dbg_print(
            f"Join#set_cloned: {to_s(self._name)}  prev owner: {to_s(self._owner.get_name())} "
            f"new owner: {to_s(owner.get_name())}\n"
        )
        self._owner = owner
        if truthy(self._array_member2):
            for join in self._array_member2:
                dbg_print(
                    f"Joinarray#set_cloned: {to_s(self._name)}  prev owner: {to_s(join.get_owner().get_name())} "
                    f"new owner: {to_s(owner.get_name())}\n"
                )
                join.set_owner(owner)

    def show_tree(self, indent: int) -> None:
        from tecsgen.core.componentobj.port import Port
        from tecsgen.ruby_compat import Symbol

        rb_print("  " * indent)
        rb_puts(
            f"Join: name: {to_s(self._name)} owner: {to_s(self._owner.get_name())} id: #<Join>"
        )
        if self._subscript is None:
            pass
        elif self._subscript >= 0:
            rb_print("  " * (indent + 1))
            rb_puts(f"subscript: {to_s(self._subscript)}")
        else:
            rb_print("  " * (indent + 1))
            rb_puts("subscript: not specified")
        rb_print("  " * (indent + 1))
        rb_puts("rhs: ")
        if type(self._rhs) is list:
            for i in self._rhs:
                if type(i) is list:
                    for j in i:
                        j.show_tree(indent + 3)
                elif type(i) is Symbol:
                    rb_print("  " * (indent + 2))
                    rb_print(to_s(i))
                    rb_print("\n")
                else:
                    i.show_tree(indent + 2)
        else:
            self._rhs.show_tree(indent + 2)
            rb_print("  " * (indent + 1))
            if truthy(self._definition):
                rb_puts("definition:")
                self._definition.show_tree(indent + 2)
            else:
                rb_puts("definition: not found")
        if type(self._definition) is Port:
            rb_print("  " * (indent + 2))
            if truthy(self._cell):
                rb_puts(
                    f"cell: {to_s(self._cell_name)} #<Cell>  port: {to_s(self._port_name)}  "
                    f"cell_global_name: {to_s(self._cell.get_global_name())}"
                )
            else:
                rb_puts(
                    f"cell: {to_s(self._cell_name)} port: {to_s(self._port_name)}  (cell not found)"
                )
        if truthy(self._through_list):
            for i, t in enumerate(self._through_list):
                rb_print("  " * (indent + 2))
                rb_puts(f"through: plugin name :  '{to_s(t[0])}' arg : '{to_s(t[2])}'")
                gen = _at(self._through_generated_list, i)
                if truthy(gen):
                    gen.show_tree(indent + 3)
        if truthy(self._array_member2):
            rb_print("  " * (indent + 1))
            rb_puts("array member:")
            for i, j in enumerate(self._array_member2):
                if truthy(j):
                    rb_print("  " * (indent + 2))
                    rb_puts(
                        f"[{i}]: {to_s(j.get_name())}  id: #<Join> owner={to_s(j.get_owner().get_name())}"
                    )
                    j.get_rhs().show_tree(indent + 3)
                else:
                    rb_print("  " * (indent + 2))
                    rb_puts(f"[{i}]: [optional]  id: ")


def _at(lst: Any, i: int) -> Any:
    return lst[i] if lst is not None and 0 <= i < len(lst) else None


def _eq(a: Any, b: Any) -> bool:
    """Ruby の a == b（nil どうしは等しい）。"""
    if a is None or b is None:
        return a is b
    return a == b


def _call(obj: Any, name: str, *args: Any) -> Any:
    if obj is None:
        from tecsgen.ruby_compat import no_method

        raise no_method(name, None)
    return getattr(obj, name)(*args)
