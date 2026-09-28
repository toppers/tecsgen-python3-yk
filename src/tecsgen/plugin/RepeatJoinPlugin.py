"""RepeatJoinPlugin.rb の移植（内部仕様9章）。

呼び口配列の添数 0 の結合を、count 個までくり返した結合を追加するセルプラグイン。
右辺のセル名の末尾の数字・右辺の受け口配列の添数 0 もカウントアップする。
"""

from __future__ import annotations

import re
from typing import Any, ClassVar

from tecsgen.plugin.CellPlugin import CellPlugin
from tecsgen.ruby_compat import rb_print, sym, to_s, truthy


class RepeatJoinPlugin(CellPlugin):
    REPEAT_JOIN_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {
        "count": lambda obj, rhs: obj.set_count(rhs),
    }

    def __init__(self, cell: Any, option: Any) -> None:
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.expression import Expression

        super().__init__(cell, option)
        rb_print(f"RepeatJoinPlugin: {to_s(self._cell.get_name())}\n")
        self._plugin_arg_check_proc_tab = RepeatJoinPlugin.REPEAT_JOIN_PLUGIN_ARG_PROC
        self.parse_plugin_arg()

        for j in self._cell.get_join_list().get_items():
            # Join の右辺を解析
            ret = j.get_rhs().analyze_cell_join_expression()
            if ret is None:
                continue
            rhs_nsp = ret[0]
            rhs_subscript = ret[1]
            rhs_port_name = ret[2]

            # 呼び口配列で、添数が 0 の場合にのみカウントアップさせる
            if j.get_subscript() != 0:
                continue

            rhs_name = to_s(rhs_nsp.get_name())
            m = re.search(r"(.*[^0-9])([0-9]+)\Z", rhs_name)
            n_digits = 0
            if m:
                b_rhs_name_count = True
                rhs_name = m.group(1)
                n_digits = len(m.group(2))
                rhs_count_base = int(m.group(2))
            else:
                b_rhs_name_count = False
                rhs_count_base = 0

            b_rhs_subscript_count = truthy(rhs_subscript) and rhs_subscript == 0

            count = 1
            while count < self._count:
                count_str = str(count + rhs_count_base)

                if b_rhs_subscript_count:
                    rhs_subscript = count

                if b_rhs_name_count:
                    if n_digits - len(count_str) > 0:
                        leading_zero = "0" * (n_digits - len(count_str))
                    else:
                        leading_zero = ""
                    rhs_name_real = rhs_name + leading_zero + count_str
                else:
                    rhs_name_real = rhs_name
                rhs_nsp2 = rhs_nsp.change_name_clone(sym(rhs_name_real))

                rhs = Expression.create_cell_join_expression(
                    rhs_nsp2, rhs_subscript, rhs_port_name
                )
                j2 = Join(j.get_name(), count, rhs)
                cell.new_join(j2)

                count += 1

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
