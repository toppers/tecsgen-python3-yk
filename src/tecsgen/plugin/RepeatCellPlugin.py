"""RepeatCellPlugin.rb の移植（内部仕様9章）。

セルを count 個までくり返し生成するセルプラグイン。セル名の末尾の数字と、結合の右辺の
セル名の末尾の数字をカウントアップする。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import class_name, rb_print, sym, to_s, truthy


class RepeatCellPlugin(CellPlugin):
    _plugin_list: ClassVar[list[Any]] = []  # @@plugin_list

    REPEAT_CELL_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {
        "count": lambda obj, rhs: obj.set_count(rhs),
    }

    @classmethod
    def reset(cls) -> None:
        """`@@plugin_list` を初期化する（1プロセスで何度も実行するテスト用）。"""
        RepeatCellPlugin._plugin_list = []

    def __init__(self, cell: Any, option: Any) -> None:
        super().__init__(cell, option)
        RepeatCellPlugin._plugin_list.append(self)
        rb_print(f"RepeatCellPlugin: {to_s(self._cell.get_name())}\n")
        self._count: Any = 0
        self._plugin_arg_check_proc_tab = RepeatCellPlugin.REPEAT_CELL_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

    def gen_cdl_file(self, file: Any) -> None:
        from tecsgen.context import get_context

        if get_context().verbose:
            # Ruby 版の "#(num}" は式展開ではないので、そのまま出る
            rb_print(
                f"{class_name(type(self))}: repeat {to_s(self._cell.get_name())} #(num}} times\n"
            )

        nest = self._cell.get_region().gen_region_str_pre(file)
        indent_str = "  " * nest
        cell_name = to_s(self._cell.get_name())
        m = re.search(r".*[^0-9]([0-9]+)\Z", cell_name)
        if m:
            tail_zero = m.group(1)
            bname = re.sub(r"[0-9]+\Z", "", cell_name)
        else:
            self.cdl_error(
                f"{class_name(type(self))}: {cell_name}'s name ends without '0-9'"
            )
            return
        base_count = int(tail_zero)

        count = 1
        num = self._count
        file.print(f"/*  {to_s(num)} times repeat of '{cell_name}' */\n")
        while count < num:
            # セル名のカウント
            count_str = str(count + base_count)
            if len(tail_zero) > len(count_str):
                leading_zero = "0" * (len(tail_zero) - len(count_str))
            else:
                leading_zero = ""
            cname = bname + leading_zero + count_str

            #   "cell tCelltype Cell {"
            file.print(
                f"{indent_str}cell {to_s(self._cell.get_celltype().get_name())} {cname}{{\n"
            )

            # Join の CDL 文字列生成
            for j in self._cell.get_join_list().get_items():
                # Join の右辺の解析
                res = j.get_rhs().analyze_cell_join_expression()
                if res is not None:
                    nsp, subscript, port_name = res[0], res[1], res[2]
                else:
                    nsp = j.get_rhs().analyze_single_identifier()
                    if nsp is not None:
                        subscript: Any = None
                        port_name: Any = None
                    else:
                        file.print(
                            f"{indent_str}  {to_s(j.get_name())} = {to_s(j.get_rhs())};\n"
                        )
                        continue

                # 右辺のセル名 (末尾の数字をカウントアップ)
                m2 = re.search(r"(.*[^0-9])([0-9]+)\Z", to_s(nsp.get_name()))
                if m2:
                    rhs_tail_num = m2.group(2)
                    rhs_name_count = count + int(rhs_tail_num)
                    if len(rhs_tail_num) > len(str(rhs_name_count)):
                        leading_zero = "0" * (
                            len(rhs_tail_num) - len(str(rhs_name_count))
                        )
                    else:
                        leading_zero = ""
                    rhs_cname = m2.group(1) + leading_zero + str(rhs_name_count)
                    nsp = nsp.change_name_clone(rhs_cname)

                # Join 文字列の出力
                if truthy(port_name):
                    # 右辺は セルの結合
                    if truthy(subscript):
                        file.print(
                            f"{indent_str}  {to_s(j.get_name())} = {nsp.get_path_str()}."
                            f"{to_s(port_name)}[{count + subscript}];\n"
                        )
                    else:
                        file.print(
                            f"{indent_str}  {to_s(j.get_name())} = {nsp.get_path_str()}."
                            f"{to_s(port_name)};\n"
                        )
                else:
                    # 右辺は単一の識別子
                    file.print(
                        f"{indent_str}  {to_s(j.get_name())} = {nsp.get_path_str()};\n"
                    )

            file.print(f"{indent_str}}};\n\n")
            count += 1

        self._cell.get_region().gen_region_str_post(file)

    def set_count(self, rhs: Any) -> None:
        """count オプションの解析。"""
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression

        if re.search(r"\A\d+\Z", to_s(rhs)):
            self._count = int(to_s(rhs))
        else:
            nsp = NamespacePath(sym(rhs), True)
            expr = Expression.create_single_identifier(nsp, None)
            res = expr.eval_const(None)
            if res is None:
                self.cdl_error(
                    "count value ($1): not single identifier or integer number",
                    to_s(rhs),
                )
                self._count = 0
            else:
                self._count = res
