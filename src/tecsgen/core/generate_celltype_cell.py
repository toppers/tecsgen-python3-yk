"""generate.rb の Celltype 再オープン部分のうち、セルのグルーコード（`<celltype>_tecsgen.c`）の生成
（`generate_cell_code`・`gen_cell_*`・`get_name_array`・`gen_cell_cb_init`）。"""

from __future__ import annotations

import re
from typing import Any

from tecsgen.context import dbg_print, get_context
from tecsgen.core.generate import AppFile, print_indent, print_note
from tecsgen.core.generator import _get_at
from tecsgen.ruby_compat import RubyRuntimeError, Y, rb_puts, sub_first, to_s, truthy


def _msg(key: str) -> str:
    from tecsgen.core.messages import TECSMsg

    return TECSMsg.get(key)


_CLOSE_BRACE_EOL = re.compile(r"\}$", re.MULTILINE)


def _fs_at(fs: dict[Any, Any], region: Any) -> Any:
    """Ruby の `fs[ region ]`（無ければ nil）。"""
    return fs.get(region)


class CelltypeGenerateCell:
    """セルのグルーコードの生成。"""

    def generate_cell_code(self: Any) -> None:
        """CELLTYPE_tecsgen.c を生成。"""
        ctx = get_context()
        gn = to_s(self._global_name)
        fs: dict[Any, Any] = {}
        f: Any = None
        roots2 = self.__dict__["_domain_class_roots2"]
        for r in roots2:
            nsp = (
                ""
                if r.is_root()
                else f"_{to_s(r.get_namespace_path().get_global_name())}"
            )
            dbg_print(
                f"celltype:{to_s(self._name)} nsp:{nsp} "
                f"class_root={to_s(r.get_class_root().get_namespace_path())} "
                f"domain_root={to_s(r.get_domain_root().get_namespace_path())}\n"
            )
            fs[r] = AppFile.open(f"{ctx.gen}/{gn}{nsp}_tecsgen.{ctx.c_suffix}")
            if r.is_link_root():
                f = fs[r]

        # in case that domain_roots does not include root region
        if f is None:
            keys = list(roots2)
            if len(keys) > 1:
                # if domain_roots.length >= 2 && no cell in root region
                # shared code are placed in root region
                gnr = keys[0].get_link_root().get_up_global_name()
                f = AppFile.open(f"{ctx.gen}/{gn}{gnr}_tecsgen.{ctx.c_suffix}")
            else:
                # shared code are placed in unique region
                f = _fs_at(fs, _get_at(keys, 0))

        # すべての _tecsgen.c に出力
        print_note(f)
        self.gen_cell_private_header(f)
        self.gen_cell_factory_header(f)
        self.gen_cell_ep_des_type(f)

        # すべての _tecsgen.c に出力
        for f2 in fs.values():
            if f is f2:
                continue
            print_note(f2)
            self.gen_cell_private_header(f2)
            self.gen_cell_factory_header(f2)
            self.gen_cell_ep_des_type(f2)

        # 一つの _tecsgen.c に出力
        self.gen_cell_skel_fun(f)
        self.gen_cell_fun_table(f)
        self.gen_cell_var_init(f)

        # セルごとに _tecsgen.c に出力
        self.gen_cell_ep_vdes(fs)
        self.gen_cell_ep_vdes_array(fs)
        self.gen_cell_cb_out_init(
            fs
        )  # INITIALIZE_CB で参照されるため ram_initializer=false でも消せない
        self.gen_cell_cb(fs)
        self.gen_cell_extern_mt(fs)
        self.gen_cell_ep_des(fs)

        # 一つの _tecsgen.c に出力
        self.gen_cell_cb_tab(f)
        if ctx.ram_initializer:
            self.gen_cell_cb_initialize_code(f)

        for f2 in fs.values():
            f2.close()
            if f is f2:
                f = None
        if f is not None:
            f.close()

    #####  celltype glue code

    def gen_cell_private_header(self: Any, f: Any) -> None:
        f.print(
            f'#include "{to_s(self._global_name)}_tecsgen.{get_context().h_suffix}"\n'
        )

    def gen_cell_factory_header(self: Any, f: Any) -> None:
        f.print(
            f'#include "{to_s(self._global_name)}_factory.{get_context().h_suffix}"\n\n'
        )

    def gen_cell_ep_des_type(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EDT_comment"), "#_EDT_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            if p.is_skelton_useless():  # 受け口最適化
                f.print(f"/* {pn} : omitted by entry port optimize */\n\n")
                continue

            f.print(f"/* {pn} */\n")
            f.print(f"struct tag_{gn}_{pn}_DES {{\n")
            f.print(
                f"    const struct tag_{to_s(p.get_signature().get_global_name())}_VMT *vmt;\n"
            )
            if self.has_CB() or self.has_INIB():
                f.print(f"    {to_s(self._name)}_IDX  idx;\n")
            else:
                # CB も INIB も存在しない (ので、idx として整数で初期化しておく)
                f.print("    int           idx;\n")
            if p.get_array_size() is not None:
                f.print("    int_t  subscript;\n")
            f.print("};\n\n")

    def gen_cell_skel_fun(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EPSF_comment"), "#_EPSF_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            if p.is_skelton_useless():  # 受け口最適化
                f.print(f"/* {pn} : omitted by entry port optimize */\n")
                continue

            f.print(f"/* {pn} */\n")

            for fun in p.get_signature().get_function_head_array():
                fn = to_s(fun.get_name())
                functype = fun.get_declarator().get_type()
                f.printf("%-14s", functype.get_type_str())

                f.print(f" {gn}_{pn}_{fn}_skel(")
                f.print(
                    f" const struct tag_{to_s(p.get_signature().get_global_name())}_VDES *epd"
                )
                delim = ","

                if truthy(functype.get_paramlist()):
                    items = functype.get_paramlist().get_items()
                else:
                    # ここで nil になるのは、引数なしの時に void がなかった場合
                    items = []
                for param in items:
                    f.print(f"{delim} ")
                    delim = ","
                    f.print(param.get_type().get_type_str())
                    f.print(" ")
                    f.print(param.get_name())
                    f.print(param.get_type().get_type_str_post())
                f.print(")\n")

                f.print("{\n")
                if not truthy(self._singleton) or p.get_array_size() is not None:
                    f.print(f"    struct tag_{gn}_{pn}_DES *lepd\n")
                    f.print(f"        = (struct tag_{gn}_{pn}_DES *)epd;\n")

                if (
                    functype.get_type_str() == "void"
                ):  # mikan "void" の typedef に未対応
                    f.print("    ")
                else:
                    f.print("    return ")

                f.print(f"{gn}_{pn}_{fn}(")
                if truthy(self._singleton):
                    delim = ""
                else:
                    f.print(" lepd->idx")
                    delim = ","

                if p.get_array_size() is not None:
                    f.print(f"{delim} lepd->subscript")
                    delim = ","

                for param in items:
                    f.print(f"{delim} ")
                    delim = ","
                    f.print(param.get_name())
                f.print(" );\n")

                f.print("}\n")
        if self._n_entry_port > 0:
            f.print("\n")

    def gen_cell_fun_table(self: Any, f: Any) -> None:
        gn = to_s(self._global_name)
        if self._n_entry_port > 0:
            f.printf(_msg("EPSFT_comment"), "#_EPSFT_#")

        for p in self._port:
            if p.get_port_type() != Y.ENTRY:
                continue
            if p.is_omit():
                continue
            pn = to_s(p.get_name())
            if p.is_VMT_useless():  # 受け口最適化
                f.print(f"/* {pn} : omitted by entry port optimize */\n")
                continue

            f.print(f"/* {pn} */\n")
            f.print(f"const struct tag_{to_s(p.get_signature().get_global_name())}_VMT")
            f.print(f" {gn}_{pn}_MT_ = {{\n")

            for fun in p.get_signature().get_function_head_array():
                f.print(f"    {gn}_{pn}_{to_s(fun.get_name())}_skel,\n")

            f.print("};\n")
        f.print("\n")

    def gen_cell_ep_vdes(self: Any, fs: dict[Any, Any]) -> None:
        from tecsgen.core.componentobj.port import Port

        gn = to_s(self._global_name)
        if self._n_cell_gen > 0:
            for f in fs.values():
                f.printf(_msg("CPEPD_comment"), "#_CPEPD_#")

        # このセルタイプのすべてのセルについて
        for c in self._ordered_cell_list:
            if not c.is_generate():  # 生成対象か？
                continue
            f = _fs_at(fs, c.get_domain_class_root())

            # 結合のリスト (NamedList)
            jl = c.get_join_list()

            # 全ての結合リストについて
            for j in jl.get_items():
                # 左辺の定義を得る
                definition = j.get_definition()

                # 呼び口ではない？　（属性）
                if type(definition) is not Port:
                    continue

                port = self.find(
                    j.get_name()
                )  # celltype の Port (こちらに最適化情報がある)
                if port.is_cell_unique():
                    continue
                if port.is_omit():
                    continue

                # 配列要素を得る（受け口配列でなければ nil が返る）
                am = j.get_array_member2()

                # 呼び口配列か?
                if truthy(am):
                    i = 0
                    while i < len(am):
                        j2 = am[i]
                        if truthy(j2):
                            if j2.get_rhs_cell().get_celltype() is self:
                                # 同じセルタイプへ結合している場合(VDES では type conflict になる)
                                p = j2.get_rhs_port()
                                des_type = (
                                    f"const struct tag_{gn}_{to_s(p.get_name())}_DES"
                                )
                            else:
                                des_type = f"struct tag_{to_s(definition.get_signature().get_global_name())}_VDES"

                            # 右辺は受け口配列か？
                            if truthy(j2.get_rhs_subscript()):
                                # 受け口の配列添数
                                subscript = j2.get_rhs_subscript()
                                f.printf(
                                    "extern %s %s%d;\n",
                                    des_type,
                                    f"{to_s(j2.get_port_global_name(i))}_des",
                                    subscript,
                                )
                            else:
                                f.printf(
                                    "extern %s %s;\n",
                                    des_type,
                                    f"{to_s(j2.get_port_global_name(i))}_des",
                                )
                        i += 1
                else:
                    dbg_print(
                        f"me={to_s(self._name)} callee={to_s(j.get_rhs_cell().get_celltype().get_name())} "
                        f"{to_s(j.get_cell().get_celltype().get_name())} \n"
                    )
                    if j.get_rhs_cell().get_celltype() is self:
                        # 同じセルタイプへ結合している場合(VDES では type conflict になる)
                        p = j.get_rhs_port()
                        des_type = f"const struct tag_{gn}_{to_s(p.get_name())}_DES"
                    else:
                        des_type = f"struct tag_{to_s(definition.get_signature().get_global_name())}_VDES"

                    if truthy(j.get_rhs_subscript()):
                        # 受け口配列
                        subscript = j.get_rhs_subscript()
                        f.printf(
                            "extern %s %s%d;\n",
                            des_type,
                            f"{to_s(j.get_port_global_name())}_des",
                            subscript,
                        )
                    else:
                        f.printf(
                            "extern %s %s;\n",
                            des_type,
                            f"{to_s(j.get_port_global_name())}_des",
                        )

            f.print("\n")

    def gen_cell_ep_vdes_array(self: Any, fs: dict[Any, Any]) -> None:
        ctx = get_context()
        if self._n_cell_gen > 0:
            for f in fs.values():  # mikan 呼び口配列が無い場合も出てしまう
                f.printf(_msg("CPA_comment"), "#_CPA_#")

        for c in self._ordered_cell_list:
            if not c.is_generate():
                continue
            f = _fs_at(fs, c.get_domain_class_root())

            jl = c.get_join_list()
            # ループを回す変数を jl から @port に変更（dynamic, optional）
            for port in self._port:
                if port.get_port_type() != Y.CALL:
                    continue
                dbg_print(
                    f"gen_cell_ep_vdes_array: {to_s(c.get_name())}.{to_s(port.get_name())}\n"
                )
                j = jl.get_item(port.get_name())

                if port.is_cell_unique():
                    continue
                if port.is_omit():
                    continue

                b_array = False
                am: Any = None
                if truthy(j):
                    am = j.get_array_member2()
                    if truthy(am):
                        b_array = True
                else:
                    if port.get_array_size() == "[]":
                        # this case is dynamic optional and nothing joined
                        continue
                    elif port.get_array_size() is not None:
                        b_array = True
                if not b_array:
                    continue

                # 左辺は配列
                const = (
                    "" if port.is_dynamic() and not ctx.ram_initializer else "const "
                )
                init = "_init_" if port.is_dynamic() and ctx.ram_initializer else ""

                if not port.is_skelton_useless():
                    f.printf(
                        f"struct %s * {const}%s_%s[] = {{\n",
                        f"tag_{to_s(port.get_signature().get_global_name())}_VDES",
                        to_s(c.get_global_name()),
                        to_s(port.get_name()) + init,
                    )
                else:
                    # スケルトン関数不要最適化の場合、この配列は参照されない
                    # mikan このケースがテストされていない
                    f.printf(
                        f"{const}%s_IDX  %s_%s[] = {{\n",
                        to_s(j.get_rhs_cell().get_celltype().get_global_name()),
                        to_s(c.get_global_name()),
                        to_s(j.get_name()),
                    )
                if port.get_array_size() == "[]":
                    length = len(am)
                else:
                    length = port.get_array_size()
                i = 0
                while i < length:
                    if am is None:
                        f.print("    0,\n")
                        i += 1
                        continue
                    j2 = am[i]
                    i += 1

                    if truthy(j2):
                        # 同一セルタイプの結合の場合、VDES 型へのキャストが必要
                        if j2.get_rhs_cell().get_celltype() is self:
                            definition = j2.get_definition()
                            des_type_cast = f"(struct tag_{to_s(definition.get_signature().get_global_name())}_VDES *)"
                        else:
                            des_type_cast = ""

                        if truthy(j2.get_rhs_subscript()):
                            # 右辺配列の場合(最適化はない)
                            subscript = j2.get_rhs_subscript()
                            f.printf(
                                "    %s%d,\n",
                                f"{des_type_cast}&{to_s(j2.get_port_global_name())}_des",
                                subscript,
                            )
                        else:
                            # 右辺非配列の場合 */
                            if not port.is_skelton_useless():
                                f.printf(
                                    "    %s,\n",
                                    f"{des_type_cast}&{to_s(j2.get_port_global_name())}_des",
                                )
                            else:
                                cell = j2.get_rhs_cell()
                                name_array = cell.get_celltype().get_name_array(cell)
                                f.printf(f"    {to_s(name_array[7])},\n")
                    else:
                        # optional で呼び口配列要素が初期化されていない
                        f.printf("    0,\n")
                f.print("};\n")
                # dynamic の呼び口配列
                if port.is_dynamic() and ctx.ram_initializer:
                    f.printf(
                        f"struct %s * %s_%s[ {to_s(length)} ];\n",
                        f"tag_{to_s(port.get_signature().get_global_name())}_VDES",
                        to_s(c.get_global_name()),
                        to_s(port.get_name()),
                    )

            f.print("\n")

    def gen_cell_cb_initialize_code(self: Any, f: Any) -> None:
        """CB を初期化するプログラムの生成。"""
        if not truthy(self.need_CB_initializer()):
            return
        gn = to_s(self._global_name)
        f.printf(_msg("CIC_comment"), "#_CIC_#")
        f.print(f"void\n{gn}_CB_initialize()\n{{\n")
        if truthy(self._singleton):
            f.print("    SET_CB_INIB_POINTER(i,p_cb)\n    INITIALIZE_CB()\n")
        else:
            f.print(
                f"""    {gn}_CB	*p_cb;
    int		i;
    FOREACH_CELL(i,p_cb)
        SET_CB_INIB_POINTER(i,p_cb)
        INITIALIZE_CB(p_cb)
    END_FOREACH_CELL
"""
            )
        f.print("}\n")

    def gen_cell_cb_out_init(self: Any, fs: dict[Any, Any]) -> None:
        """CB/INIB の外で初期化される変数の出力。"""
        from tecsgen.core.cdl_types import ArrayType, PtrType
        from tecsgen.core.expression import Expression
        from tecsgen.core.generator import Token

        ctx = get_context()
        # セルがなければ、出力しない
        if self._n_cell_gen == 0:
            return

        for f in fs.values():
            f.printf(_msg("AVAI_comment"), "#_AVAI_#")

        # attribute, var のポインタ型の参照する配列を生成
        for c in self._ordered_cell_list:
            if not c.is_generate():
                continue

            f = _fs_at(fs, c.get_domain_class_root())
            name_array = self.get_name_array(c)

            ct = c.get_celltype()
            jl = c.get_join_list()

            # attribute, var のポインタ変数が配列により初期化される場合の、配列を出力
            av_list = ct.get_attribute_list() + ct.get_var_list()
            for a in av_list:  # a: Decl
                j = jl.get_item(a.get_identifier())
                init = j.get_rhs() if truthy(j) else a.get_initializer()

                if a.is_type(PtrType) and (
                    (truthy(init) and type(init) is list) or init is None
                ):
                    ptr_type = a.get_type()
                    size = ptr_type.get_size()

                    if truthy(size):
                        # 式を評価する(attribute, var に含まれる変数を参照可能)
                        sz = size.eval_const(
                            c.get_join_list(), c.get_celltype().get_name_list()
                        )
                        # 式を生成しなおす (変数を含まない形にする)  不完全な形で Token を生成
                        size = Expression([Y.INTEGER_CONSTANT, Token(sz, None, 0, 0)])
                        array_type = ArrayType(size)
                        type_ = a.get_type().get_referto()
                        if not type_.is_const() and a.get_kind() == Y.ATTRIBUTE:
                            type_.set_qualifier(Y.CONST)
                        array_type.set_type(type_)
                        if a.get_kind() == Y.ATTRIBUTE:
                            f.print("const ")
                        referto = a.get_type().get_referto()
                        f.printf(
                            f"{to_s(referto.get_type_str())} {to_s(name_array[3])}_"
                            f"{to_s(a.get_identifier())}_INIT[%d]{to_s(referto.get_type_str_post())}",
                            sz,
                        )
                        # name_array[3]: cell_CB_INIT
                        if not (ctx.ram_initializer and a.get_kind() == Y.VAR):
                            # -R (ram initializer 使用) の場合 var は初期化コードを出力しない
                            if truthy(init):
                                s = " = " + to_s(
                                    self.gen_cell_cb_init(
                                        f,
                                        c,
                                        name_array,
                                        array_type,
                                        init,
                                        a.get_identifier(),
                                        1,
                                        True,
                                    )
                                )
                                s = sub_first(_CLOSE_BRACE_EOL, "};\n", s)
                            else:
                                s = ";\n"
                            f.print(s)
                        else:
                            f.print(";\n")

    def gen_cell_var_init(self: Any, f: Any) -> None:
        """var の初期値の ROM 部への出力。"""
        from tecsgen.core.cdl_types import ArrayType, PtrType, StructType
        from tecsgen.core.expression import Expression
        from tecsgen.ruby_compat import class_name

        gn = to_s(self._global_name)
        # var の{ }で囲まれた初期値指定があるか調べる
        n_init = 0
        for v in self._var:
            init = v.get_initializer()
            if truthy(init) and type(init) is list:
                n_init += 1

        if n_init > 0:
            f.printf(_msg("AVI_comment"), "#_AVI_#")
            for v in self._var:
                init = v.get_initializer()
                if not (truthy(init) and type(init) is list):
                    continue
                type_ = v.get_type()
                org_type = v.get_type().get_original_type()

                if isinstance(org_type, PtrType):
                    # PtrType は ArrayType にすり替える（初期化子の要素数だけとする（後は 0)）
                    t2 = ArrayType(Expression.create_integer_constant(len(init), None))
                    t2.set_type(type_.get_type())
                    type_ = t2
                    org_type = t2

                c = _get_at(
                    self._ordered_cell_list, 0
                )  # 仮の cell (実際には使われない)
                name_array = self.get_name_array(c)
                f.print(
                    f"const {to_s(type_.get_type_str())}\t{gn}_{to_s(v.get_name())}_VAR_INIT"
                    f"{to_s(type_.get_type_str_post())} = "
                )
                if isinstance(org_type, StructType):
                    # celltype の default の初期値あり
                    s = self.gen_cell_cb_init(
                        f, c, name_array, type_, init, v.get_identifier(), 1, True
                    )
                elif isinstance(org_type, (PtrType, ArrayType)):
                    s = "{ "
                    type_ = org_type.get_type()
                    # mikan ポインタではなく、配列型としないと、ポインタ変数の領域の分、損する
                    for i in init:
                        s += to_s(
                            self.gen_cell_cb_init(
                                f, c, name_array, type_, i, v.get_identifier(), 1, True
                            )
                        )
                        s += ", "
                    s += "}"
                else:
                    rb_puts(class_name(type(type_)))
                    raise RubyRuntimeError("Unknown Type")
                f.print(s)
                f.print(";\n")
            f.print("\n")

    def gen_cell_cb(self: Any, fs: dict[Any, Any]) -> None:
        ctx = get_context()
        gn = to_s(self._global_name)
        singleton = truthy(self._singleton)
        need_ptab = truthy(self._b_need_ptab)
        if self.has_INIB():
            if self._n_cell_gen > 0:
                for f in fs.values():
                    f.printf(_msg("INIB_comment"), "#_INIB_#")
            if singleton:
                for f in fs.values():
                    f.print(f"{gn}_INIB {gn}_SINGLE_CELL_INIB = \n")
                indent = 0
            elif not need_ptab:
                for f in fs.values():
                    f.print(f"{gn}_INIB {gn}_INIB_tab[] = {{\n")
                indent = 1
            else:
                indent = 0

            for c in self._ordered_cell_list:
                if not c.is_generate():
                    continue

                f = _fs_at(fs, c.get_domain_class_root())

                name_array = self.get_name_array(c)

                if not singleton:
                    print_indent(f, indent)
                    f.print(
                        f"/* cell: {to_s(name_array[2])}:  {to_s(name_array[1])} id={to_s(c.get_id())} */\n"
                    )

                print_indent(f, indent)
                if need_ptab:
                    f.print(f"const {gn}_INIB {to_s(name_array[5])} = ")
                f.print("{\n")

                self.gen_cell_cb_port(c, indent, f, name_array, Y.INIB)
                self.gen_cell_cb_attribute(c, indent, f, name_array, Y.INIB)

                if not singleton:
                    # 1 つの cell INIB の終わり
                    if need_ptab:
                        f.print("};\n\n")
                    else:
                        f.print("    },\n")
            if not need_ptab:
                for f in fs.values():
                    f.print("};\n\n")

        if self.has_CB():
            if self._n_cell_gen > 0:
                for f in fs.values():
                    f.printf(_msg("CB_comment"), "#_CB_#")

            # RAM initializer を使用しない、または ROM 化しない
            if ctx.ram_initializer is False or ctx.rom is False:
                if singleton:
                    for f in fs.values():
                        f.print(f"struct tag_{gn}_CB {gn}_SINGLE_CELL_CB = \n")
                    indent = 0
                elif not need_ptab:
                    for f in fs.values():
                        f.print(f"struct tag_{gn}_CB {gn}_CB_tab[] = {{\n")
                    indent = 1
                else:
                    indent = 0

                for c in self._ordered_cell_list:
                    if not c.is_generate():
                        continue

                    f = _fs_at(fs, c.get_domain_class_root())

                    name_array = self.get_name_array(c)

                    if not singleton:
                        print_indent(f, indent)
                        f.print(
                            f"/* cell: {to_s(name_array[2])}:  {to_s(name_array[1])} id={to_s(c.get_id())} */\n"
                        )

                    print_indent(f, indent)
                    if need_ptab:
                        f.print(f"{gn}_CB {to_s(name_array[2])} = ")
                    f.print("{\n")

                    if self.has_INIB():
                        print_indent(f, indent + 1)
                        f.printf("&%-39s /* _inib */\n", f"{to_s(name_array[5])},")

                    if ctx.rom is False:
                        self.gen_cell_cb_port(c, indent, f, name_array, Y.CB_ALL)
                    else:
                        self.gen_cell_cb_port(c, indent, f, name_array, Y.CB_DYNAMIC)

                    self.gen_cell_cb_attribute(c, indent, f, name_array, Y.CB)
                    self.gen_cell_cb_var(c, indent, f, name_array)

                    if not singleton:
                        # 1 つの cell CB の終わり
                        if need_ptab:
                            f.print("};\n\n")
                        else:
                            f.print("    },\n")
                if not need_ptab:
                    for f in fs.values():
                        f.print("};\n\n")
            else:
                if singleton:
                    for f in fs.values():
                        f.print(f"struct tag_{gn}_CB {gn}_SINGLE_CELL_CB;\n")
                elif need_ptab:
                    for c in self._ordered_cell_list:
                        if not c.is_generate():
                            continue
                        f = _fs_at(fs, c.get_domain_class_root())
                        name_array = self.get_name_array(c)
                        f.print(
                            f"/* cell: {to_s(name_array[2])}:  {to_s(name_array[1])} id={to_s(c.get_id())} */\n"
                        )
                        f.print(f"{gn}_CB {to_s(name_array[2])} = {{}};\n")
                else:
                    for f in fs.values():
                        f.print(
                            f"struct tag_{gn}_CB {gn}_CB_tab[{to_s(self._n_cell_gen)}];\n"
                        )

    def gen_cell_cb_tab(self: Any, f: Any) -> None:
        from tecsgen.core.componentobj.region import Region

        ctx = get_context()
        gn = to_s(self._global_name)
        indent = 0
        if truthy(self._b_need_ptab):
            if self.has_INIB() and (ctx.ram_initializer or not self.has_CB()):
                f.print("/* ID to INIB table #_INTAB_# */\n")
                for c in self._ordered_cell_list:
                    # 生成対象かつ、ルート以外か
                    if (
                        c.is_generate()
                        and c.get_domain_class_root() is not Region.get_root()
                    ):
                        name_array = self.get_name_array(c)
                        print_indent(f, indent + 1)
                        f.print(f"extern {gn}_INIB  {to_s(name_array[5])};\n")

                f.print(f"{gn}_INIB *const {gn}_INIB_ptab[] ={{\n")
                for c in self._ordered_cell_list:
                    if c.is_generate():  # 生成対象か？
                        name_array = self.get_name_array(c)
                        print_indent(f, indent + 1)
                        f.print(f"&{to_s(name_array[5])},\n")
                f.print("};\n")
            if self.has_CB():
                f.print("/* ID to CB table #_CBTAB_# */\n")
                for c in self._ordered_cell_list:
                    # 生成対象かつ、ルート以外か
                    if (
                        c.is_generate()
                        and c.get_domain_class_root() is not Region.get_root()
                    ):
                        name_array = self.get_name_array(c)
                        print_indent(f, indent + 1)
                        f.print(f"extern {gn}_CB  {to_s(name_array[2])};\n")

                f.print(f"{gn}_CB *const {gn}_CB_ptab[] ={{\n")
                for c in self._ordered_cell_list:
                    if c.is_generate():  # 生成対象か？
                        name_array = self.get_name_array(c)
                        print_indent(f, indent + 1)
                        f.print(f"&{to_s(name_array[2])},\n")
                f.print("};\n")

    def get_name_array(self: Any, cell: Any) -> list[Any]:
        """name_array を生成。

        name_array[0] = @name / [1] = cell.get_name / [2] = cell_CB_name / [3] = cell_CB_INIT
        [4] = cell_CB_proto / [5] = cell_INIB / [6] = cell_ID / [7] = cell_IDX / [8] = cell_CBP
        [9] = @global_name / [10] = cell.get_global_name / [11] = cell_INIB_proto
        """
        gn = to_s(self._global_name)
        if truthy(self._singleton):
            cell_CB_name = f"{gn}_SINGLE_CELL_CB"
            cell_CB_INIT = cell_CB_name
            cell_CB_proto = f"{gn}_SINGLE_CELL_CB"
            cell_INIB_name = f"{gn}_SINGLE_CELL_INIB"
            cell_INIB_proto = cell_INIB_name
            cell_ID: Any = 0
        else:
            if not truthy(self._b_need_ptab):
                index = cell.get_id() - cell.get_celltype().get_id_base()
                cell_CB_name = f"{gn}_CB_tab[{index}]"
                cell_CB_INIT = f"{gn}_{to_s(cell.get_name())}_CB"
                cell_CB_proto = f"{gn}_CB_tab[]"
                cell_INIB_name = f"{gn}_INIB_tab[{index}]"
                cell_INIB_proto = f"{gn}_INIB_tab[]"
            else:
                cgn = to_s(cell.get_global_name())
                cell_CB_name = f"{cgn}_CB"
                cell_CB_INIT = cell_CB_name
                cell_CB_proto = cell_CB_name
                cell_INIB_name = f"{cgn}_INIB"
                cell_INIB_proto = cell_INIB_name
            cell_ID = cell.get_id()

        if self.has_CB():
            cell_CBP = f"&{cell_CB_name}"
        elif self.has_INIB():
            cell_CBP = f"&{cell_INIB_name}"
        else:
            # CB も INIB もなければ 0 に置換 (警告が出ることがあったので "NULL" から変更)
            cell_CBP = f"(({gn}_IDX)0)"

        cell_IDX = cell_ID if truthy(self._idx_is_id_act) else cell_CBP

        return [
            self._name,  # celltype name
            cell.get_name(),  # cell name
            cell_CB_name,  # cell_CB_name
            cell_CB_INIT,  # cell_CB_INIT
            cell_CB_proto,  # CB name for prototype
            cell_INIB_name,  # cell INIB name
            cell_ID,  # cell ID
            cell_IDX,  # cell IDX
            cell_CBP,  # cell CBP
            self._global_name,  # celltype global name
            cell.get_global_name(),  # cell global name
            cell_INIB_proto,  # INIB name for prototype
        ]

    def gen_cell_cb_attribute(
        self: Any, cell: Any, indent: int, f: Any, name_array: list[Any], cb_inib: Any
    ) -> None:
        """attribute と size_is 指定された var (ポインタ)の初期化データを出力。

        ROM 化サポートの有無、および出力対象が CB か INIB かにより出力される内容が異なる。
        """
        ctx = get_context()
        ct = self
        jl = cell.get_join_list()

        if cb_inib == Y.INIB:
            if self._n_attribute_ro == 0 and self._n_var_size_is == 0:
                return
            print_indent(f, indent + 1)
            f.print("/* attribute(RO) */ \n")
        elif ctx.rom:  # && cb_inib == CB
            # CB で rw と var
            if self._n_attribute_rw == 0:
                return
            print_indent(f, indent + 1)
            f.print("/* attribute(RW) */ \n")
        else:  # cb_inib == CB && $rom == false
            # CB に全部
            if (
                self._n_attribute_rw == 0
                and self._n_attribute_ro == 0
                and self._n_var_size_is == 0
            ):
                return
            print_indent(f, indent + 1)
            f.print("/* attribute */ \n")

        for a in ct.get_attribute_list():  # a: Decl
            if a.is_omit():
                continue
            if cb_inib == Y.INIB and a.is_rw() is True:
                # $rom == true でしか、ここへ来ない
                continue
            elif cb_inib == Y.CB and ctx.rom and not a.is_rw():
                continue

            j = jl.get_item(a.get_identifier())
            if truthy(j):
                # cell の初期値指定あり
                self.gen_cell_cb_init(
                    f,
                    cell,
                    name_array,
                    a.get_type(),
                    j.get_rhs(),
                    a.get_identifier(),
                    indent + 1,
                )
            elif truthy(a.get_initializer()):
                # celltype の default の初期値あり
                self.gen_cell_cb_init(
                    f,
                    cell,
                    name_array,
                    a.get_type(),
                    a.get_initializer(),
                    a.get_identifier(),
                    indent + 1,
                )
            else:
                # 初期値未指定
                self.gen_cell_cb_init(
                    f,
                    cell,
                    name_array,
                    a.get_type(),
                    None,
                    a.get_identifier(),
                    indent + 1,
                )
        for v in self._var:
            if v.is_omit():
                continue
            if (
                v.get_size_is() is None
            ):  # size_is 指定がある場合 attribute の一部として出力
                continue

            if truthy(v.get_initializer()) and ctx.ram_initializer is False:
                self.gen_cell_cb_init(
                    f,
                    cell,
                    name_array,
                    v.get_type(),
                    v.get_initializer(),
                    v.get_identifier(),
                    indent + 1,
                )
            else:
                # 初期値未指定 または RAM initializer 使用
                self.gen_cell_cb_init(
                    f,
                    cell,
                    name_array,
                    v.get_type(),
                    None,
                    v.get_identifier(),
                    indent + 1,
                )

    def gen_cell_cb_var(
        self: Any, cell: Any, indent: int, f: Any, name_array: list[Any]
    ) -> None:
        """var の初期化データを出力。"""
        ctx = get_context()
        var = self.get_var_list()
        if self._n_var - self._n_var_size_is > 0:
            print_indent(f, indent + 1)
            f.print("/* var */ \n")
            for v in var:
                if v.is_omit():
                    continue
                if truthy(
                    v.get_size_is()
                ):  # size_is 指定がある場合 attribute の一部として出力
                    continue

                if truthy(v.get_initializer()) and ctx.ram_initializer is False:
                    self.gen_cell_cb_init(
                        f,
                        cell,
                        name_array,
                        v.get_type(),
                        v.get_initializer(),
                        v.get_identifier(),
                        indent + 1,
                    )
                else:
                    # 初期値未指定 または RAM initializer 使用
                    self.gen_cell_cb_init(
                        f,
                        cell,
                        name_array,
                        v.get_type(),
                        None,
                        v.get_identifier(),
                        indent + 1,
                    )

    def gen_cell_cb_port(
        self: Any,
        cell: Any,
        indent: int,
        f: Any,
        name_array: list[Any],
        inib_cb: Any = Y.INIB,
    ) -> None:
        """inib_cb::Symbol: :INIB, :CB_ALL, :CB_DYNAMIC"""
        self.gen_cell_cb_call_port(cell, indent, f, name_array, inib_cb)
        self.gen_cell_cb_entry_port(cell, indent, f, name_array)

    def gen_cell_cb_call_port(
        self: Any, cell: Any, indent: int, f: Any, name_array: list[Any], inib_cb: Any
    ) -> None:
        """呼び口の初期化コードの生成。"""
        ctx = get_context()
        jl = cell.get_join_list()

        port = self.get_port_list()
        dyn = self._n_call_port_dynamic - self._n_call_port_array_dynamic
        if (
            (
                inib_cb == Y.INIB
                and (
                    self._n_call_port
                    - self._n_call_port_omitted_in_CB
                    - (0 if ctx.ram_initializer else dyn)
                    > 0
                )
            )
            or (inib_cb == Y.CB_ALL and self._n_call_port > 0)
            or (inib_cb == Y.CB_DYNAMIC and dyn > 0)
        ):
            print_indent(f, indent + 1)
            f.print(f"/* call port ({to_s(inib_cb)}) #_CP_# */ \n")
            cgn = to_s(cell.get_global_name())
            for p in port:
                if p.get_port_type() != Y.CALL:
                    continue
                if p.is_omit():
                    continue
                if p.is_cell_unique():  # 最適化（単一セルで呼び口マクロに埋め込まれる）
                    continue
                has_array = p.get_array_size() is not None
                if (
                    inib_cb == Y.INIB
                    and p.is_dynamic()
                    and not has_array
                    and not ctx.ram_initializer
                ):
                    continue
                if inib_cb == Y.CB_DYNAMIC and (not p.is_dynamic() or has_array):
                    continue

                pn = to_s(p.get_name())
                j = jl.get_item(p.get_name())
                print_indent(f, indent + 1)

                if j is None:
                    dbg_print(
                        f"cell_cb_call_port: {pn} array size={to_s(p.get_array_size())}\n"
                    )
                    # optional 呼び口
                    if has_array:
                        if p.is_dynamic():
                            if inib_cb == Y.INIB:
                                if ctx.ram_initializer:
                                    f.printf(
                                        "%-40s /* #_CCP7_# _init_ */\n",
                                        f"{cgn}_{pn}_init_,",
                                    )
                                    print_indent(f, indent + 1)
                                f.printf("%-40s /* #_CCP7B_# */\n", f"{cgn}_{pn},")
                            elif ctx.rom is False:
                                f.printf("%-40s /* #_CCP8_# */\n", f"{cgn}_{pn},")
                        else:
                            f.printf("%-40s /* #_CCP9_# */\n", "0,")
                        if p.get_array_size() == "[]":
                            # 添数省略の呼び口配列
                            print_indent(f, indent + 1)
                            f.printf(
                                "%-40s /* %s #_CCP6_# */\n",
                                "0,",
                                f"length of {pn} (n_{pn})",
                            )
                    else:
                        f.printf("%-40s /* #_CCP5_# */\n", "0,")
                    continue

                am = j.get_array_member2()
                if truthy(am):
                    # 呼び口配列の場合
                    jn = to_s(j.get_name())
                    if (
                        inib_cb == Y.INIB
                        and p.is_dynamic()
                        and has_array
                        and ctx.ram_initializer
                    ):
                        f.printf("%-40s /* #_CCP3_# _init_ */\n", f"{cgn}_{jn}_init_,")
                        print_indent(f, indent + 1)
                    f.printf("%-40s /* #_CCP3B_# */\n", f"{cgn}_{jn},")
                    if p.get_array_size() == "[]":
                        # 添数省略の呼び口配列
                        print_indent(f, indent + 1)
                        f.printf(
                            "%-40s /* %s #_CCP4_# */\n",
                            f"{len(am)},",
                            f"length of {pn} (n_{pn})",
                        )
                else:
                    # 同一セルタイプの結合の場合、VDES 型へのキャストが必要
                    if j.get_rhs_cell().get_celltype() is self:
                        definition = j.get_definition()
                        des_type_cast = f"(struct tag_{to_s(definition.get_signature().get_global_name())}_VDES *)"
                    else:
                        des_type_cast = ""

                    init = "_init_" if p.is_dynamic() and inib_cb == Y.INIB else ""

                    if truthy(j.get_rhs_subscript()):
                        # 受け口配列の場合
                        subscript = j.get_rhs_subscript()
                        f.printf(
                            "%-40s /* %s #_CCP0_# */\n",
                            f"{des_type_cast}&{to_s(j.get_port_global_name())}_des{to_s(subscript)},",
                            pn + init,
                        )
                    else:
                        # 呼び口配列でも、受け口配列でもない
                        if not p.is_skelton_useless():
                            f.printf(
                                "%-40s /* %s #_CCP1_# */\n",
                                f"{des_type_cast}&{to_s(j.get_port_global_name())}_des,",
                                pn + init,
                            )
                        else:
                            # スケルトン不要最適化（CB (INIB) へのポインタを埋め込む）
                            c = j.get_rhs_cell()  # 呼び先セル
                            ct = c.get_celltype()  # 呼び先セルタイプ
                            na = ct.get_name_array(
                                c
                            )  # 呼び先セルタイプで name_array を得る
                            if ct.has_INIB() or ct.has_CB():
                                f.printf(
                                    "%-40s /* %s #_CCP2_# */\n", f"{to_s(na[7])},", pn
                                )
                            else:
                                # 呼び先は CB も INIB も持たない（NULL に初期化）
                                f.printf("%-40s /* %s #_CCP2B_# */\n", "0,", pn)

    def gen_cell_cb_entry_port(
        self: Any, cell: Any, indent: int, f: Any, name_array: list[Any]
    ) -> None:
        """受け口の初期化コードの生成。"""
        if self._n_entry_port != 0:
            print_indent(f, indent + 1)
            f.print("/* entry port #_EP_# */ \n")
            for p in self._port:
                # 受け口配列の個数は省略しない
                if p.get_port_type() == Y.ENTRY and p.get_array_size() == "[]":
                    print_indent(f, indent + 1)
                    f.printf(
                        "%-40s /*  #_EEP_# */\n",
                        f"{cell.get_entry_port_max_subscript(p) + 1},",
                    )

    def gen_cell_cb_init(
        self: Any,
        f: Any,
        cell: Any,
        name_array: list[Any],
        type_: Any,
        init: Any,
        identifier: Any,
        indent: int,
        f_get_str: bool = False,
    ) -> Any:
        """セルの attribute, var の初期値を出力。

        f_get_str:: true の場合、文字列を返す、false の場合、ファイル f に出力する．
        文字列を返すとき、末尾に ',' は含まれない．ファイルへ出力するとき、末尾に ',' が出力される．
        戻り値は Ruby のメソッドの最後の式の値に合わせる（構造体の C_EXP の場合など）。
        """
        from tecsgen.core.cdl_types import (
            ArrayType,
            BoolType,
            DefinedType,
            DescriptorType,
            EnumType,
            FloatType,
            IntType,
            PtrType,
            StructType,
        )
        from tecsgen.core.expression import C_EXP

        cell_CB_INIT = to_s(name_array[3])
        ident = to_s(identifier)

        while isinstance(type_, DefinedType):
            type_ = type_.get_type()

        def out(s: str) -> None:
            f.print("    " * indent)
            f.printf("%-40s /* %s */\n", s, identifier)

        if init is None:
            if isinstance(type_, BoolType):
                s = "false"  # formerly tecs_false
            elif isinstance(type_, IntType):
                s = "0"
            elif isinstance(type_, FloatType):
                s = "0.0"
            elif isinstance(type_, EnumType):
                s = "0"
            elif isinstance(type_, (ArrayType, StructType)):
                s = "{}"
            elif isinstance(type_, PtrType):
                s = f"{cell_CB_INIT}_{ident}_INIT" if truthy(type_.get_size()) else "0"
            elif isinstance(type_, DescriptorType):
                s = "{}"
            else:
                raise RubyRuntimeError("UnknownType")
            if f_get_str:
                return s
            out(s + ",")
            return None

        jl = cell.get_join_list()
        # このメソッドは Celltype のものである必要は無い（上に続くのでここに置く）
        # 初期値指定あり
        if isinstance(type_, (BoolType, IntType)):
            if type(init) is C_EXP:
                init_str = self.subst_name(init.get_c_exp_string(), name_array)
            else:
                init_str = init.eval_const2(jl, self._name_list)
            if f_get_str:
                return to_s(init_str)
            out(f"{to_s(init_str)},")
            return None
        elif isinstance(type_, (FloatType, EnumType)):
            # mikan C_EXP for FloatType, EnumType
            if f_get_str:
                return to_s(init.eval_const2(jl, self._name_list))
            out(f"{to_s(init.eval_const2(jl, self._name_list))},")
            return None
        elif isinstance(type_, ArrayType):
            if truthy(type_.get_subscript()):
                length = type_.get_subscript().eval_const(jl, self._name_list)
            else:
                length = len(init)

            at = type_.get_type()
            i = 0
            if f_get_str:
                s = "{ "
            else:
                f.print("    " * indent)
                f.print("{\n")

            for _ in range(length):
                if not truthy(_get_at(init, i)):  # mikan この処置は適切？
                    continue
                if f_get_str:
                    s += to_s(
                        self.gen_cell_cb_init(
                            f,
                            cell,
                            name_array,
                            at,
                            init[i],
                            f"{ident}[{i}]",
                            indent + 1,
                            f_get_str,
                        )
                    )
                    s += ", "
                else:
                    self.gen_cell_cb_init(
                        f,
                        cell,
                        name_array,
                        at,
                        init[i],
                        f"{ident}[{i}]",
                        indent + 1,
                        f_get_str,
                    )
                i += 1

            if f_get_str:
                s += "}"
                return s
            f.print("    " * indent)
            f.print("},\n")
            return None
        elif isinstance(type_, StructType):
            if type(init) is C_EXP:
                # Ruby 版は文字列を作るだけで出力しない（戻り値にはなる）
                return self.subst_name(init.get_c_exp_string(), name_array)
            i = 0
            decls = type_.get_members_decl().get_items()
            if f_get_str:
                s = "{ "
            else:
                f.print("    " * indent)
                f.print(f"{{                                        /* {ident} */\n")

            for d in decls:
                if not truthy(_get_at(init, i)):
                    continue
                if f_get_str:
                    s += to_s(
                        self.gen_cell_cb_init(
                            f,
                            cell,
                            name_array,
                            d.get_type(),
                            init[i],
                            d.get_identifier(),
                            indent + 1,
                            f_get_str,
                        )
                    )
                    s += ", "
                else:
                    self.gen_cell_cb_init(
                        f,
                        cell,
                        name_array,
                        d.get_type(),
                        init[i],
                        d.get_identifier(),
                        indent + 1,
                        f_get_str,
                    )
                i += 1
            if f_get_str:
                s += "}"
                return s
            f.print("    " * indent)
            f.print("},\n")
            return None
        elif isinstance(type_, PtrType):
            if type(init) is list:
                if f_get_str:
                    return f"{cell_CB_INIT}_{ident}_INIT"
                out(f"{cell_CB_INIT}_{ident}_INIT,")
                return None
            elif type(init) is C_EXP:
                init_str = self.subst_name(init.get_c_exp_string(), name_array)
                if f_get_str:
                    return to_s(init_str)
                out(f"{to_s(init_str)},")
                return None
            else:
                if f_get_str:
                    return to_s(init.eval_const2(jl, self._name_list))
                out(f"{to_s(init.eval_const2(jl, self._name_list))},")
                return None
        raise RubyRuntimeError("UnknownType")

    def get_cell_attr_var_init_str(
        self: Any, cell: Any, name_array: list[Any], attr_var_name: Any
    ) -> Any:
        from tecsgen.core.syntaxobj.decl import Decl
        from tecsgen.ruby_compat import class_name

        decl = self._name_list.get_item(attr_var_name)
        if not isinstance(decl, Decl):
            raise RubyRuntimeError(
                f"get_cell_attr_var_init_str: not Decl {to_s(attr_var_name)}. "
                f"{class_name(type(decl)) if decl is not None else 'NilClass'}"
            )
        j = cell.get_join_list().get_item(attr_var_name)
        init = j.get_rhs() if truthy(j) else decl.get_initializer()
        return self.gen_cell_cb_init(
            None, cell, name_array, decl.get_type(), init, attr_var_name, 0, True
        )

    def gen_cell_extern_mt(self: Any, fs: dict[Any, Any]) -> None:
        """関数テーブルの外部参照。"""
        gn = to_s(self._global_name)
        for r, f in fs.items():
            if not r.is_link_root():
                for p in self._port:
                    if p.is_omit():
                        continue
                    if p.get_port_type() == Y.ENTRY and not p.is_VMT_useless():
                        f.print(
                            f"extern const struct tag_{to_s(p.get_signature().get_global_name())}_VMT"
                        )
                        f.print(f" {gn}_{to_s(p.get_name())}_MT_;\n")

    def gen_cell_ep_des(self: Any, fs: dict[Any, Any]) -> None:
        """受け口ディスクリプタの定義を生成。"""
        gn = to_s(self._global_name)
        if self._n_cell_gen > 0:
            for f in fs.values():
                f.printf(_msg("EPD_comment"), "#_EPD_#")

        for c in self._ordered_cell_list:
            if not c.is_generate():
                continue

            f = _fs_at(fs, c.get_domain_class_root())

            ct = c.get_celltype()  # ct = self でも同じ
            name_array = self.get_name_array(c)
            cgn = to_s(c.get_global_name())

            for p in ct.get_port_list():
                if p.get_port_type() != Y.ENTRY:
                    continue
                if p.is_omit():
                    continue
                pn = to_s(p.get_name())
                if p.is_skelton_useless():  # 受け口最適化n ep_opt
                    f.print(f"/* {pn} : omitted by entry port optimize */\n")
                    continue

                length = p.get_array_size()
                if length == "[]":
                    length = c.get_entry_port_max_subscript(p) + 1

                if length is not None:
                    # 受け口配列の場合
                    i = 0
                    while i < length:
                        f.print(f"extern const struct tag_{gn}_{pn}_DES")
                        f.print(f" {cgn}_{pn}_des{i};\n")
                        f.print(f"const struct tag_{gn}_{pn}_DES")
                        f.print(f" {cgn}_{pn}_des{i} = {{\n")
                        if p.is_VMT_useless():
                            f.print("    0,\n")
                        else:
                            f.print(f"    &{gn}_{pn}_MT_,\n")
                        if truthy(self._idx_is_id_act):
                            f.print(f"    {to_s(c.get_id())},           /* ID */\n")
                        elif self.has_CB():
                            f.print(f"    {to_s(name_array[8])},      /* CB 1 */\n")
                        elif self.has_INIB():
                            f.print(f"    &{to_s(name_array[5])},      /* INIB 1 */\n")
                        else:
                            f.print("    0,\n")
                        f.print(f"    {i}\n")
                        f.print("};\n")
                        i += 1
                else:
                    f.print(f"extern const struct tag_{gn}_{pn}_DES")
                    f.print(f" {cgn}_{pn}_des;\n")
                    f.print(f"const struct tag_{gn}_{pn}_DES")
                    f.print(f" {cgn}_{pn}_des = {{\n")
                    if p.is_VMT_useless():
                        f.print("    0,\n")
                    else:
                        f.print(f"    &{gn}_{pn}_MT_,\n")
                    if truthy(self._idx_is_id_act):
                        f.print(f"    {to_s(c.get_id())},     /* ID */\n")
                    elif self.has_CB():
                        f.print(f"    {to_s(name_array[8])},      /* CB 3 */\n")
                    elif self.has_INIB():
                        f.print(f"    &{to_s(name_array[5])},      /* INIB 3 */\n")
                    else:
                        f.print("    0,\n")
                    f.print("};\n")
