"""ATK1EventPlugin.rb の移植。TOPPERS/ATK1（OSEK）のイベント定義（`EVENT_tecsgen.oil`）を生成する。

Ruby 版は mask のビット位置の割り当て中に `p` で標準出力へ書く（AUTO のときだけ）ので、同じ内容を書く。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.CelltypePlugin import CelltypePlugin
from tecsgen.ruby_compat import inspect, rb_puts, sym, to_s


def _to_i(s: str) -> int:
    """Ruby の `String#to_i`（先頭の整数部分だけを読む。読めなければ 0）。"""
    import re

    m = re.match(r"\s*[+-]?\d+", s)
    return int(m.group(0)) if m else 0


class ATK1EventPlugin(CelltypePlugin):
    # セル実体群。全てのセルの実体を意味解析後に参照する必要があるために、
    # 初期化時に singleton の instancies に格納する
    _instancies: ClassVar[list[Any]] = []

    @classmethod
    def reset(cls) -> None:
        ATK1EventPlugin._instancies = []

    def __init__(self, celltype: Any, option: Any) -> None:
        super().__init__(celltype, option)
        ATK1EventPlugin._instancies.append(self)

    def new_cell(self, cell: Any) -> None:
        pass

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        """意味解析実行後のコード生成。"""
        for inst in ATK1EventPlugin._instancies:
            inst.gen_oil_code(file)

    def gen_oil_code(self, file: Any) -> None:
        """OILファイル出力。"""
        from tecsgen.context import get_context
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.expression import Expression
        from tecsgen.core.plugin import CFile

        file2 = CFile.open(f"{get_context().gen}/EVENT_tecsgen.oil", "w")

        whole_mask = 0

        # EVENT
        for cell in self._celltype.get_cell_list():
            join = cell.get_join_list().get_item(sym("mask"))

            # AUTO type search and change to zero
            if join is not None:
                mask_bit = _to_i(to_s(join.get_rhs()))
                mask_str = to_s(join.get_rhs())
                if mask_str == "AUTO":
                    new_rhs = Expression.create_integer_constant(32, self._locale)
                    join.change_rhs(new_rhs)
                else:
                    mask_pattern = 1 << mask_bit
                    whole_mask |= mask_pattern
            else:
                new_rhs = Expression.create_integer_constant(32, self._locale)
                join = Join(sym("mask"), None, new_rhs)
                cell.new_join(join)

        mask_count = 0
        mask_place = 0

        for cell in self._celltype.get_cell_list():
            # bit place to mask pattern
            file2.print(f"\tEVENT {to_s(cell.get_name())} {{\n")
            join = cell.get_join_list().get_item(sym("mask"))
            if join is not None:
                mask_bit = _to_i(to_s(join.get_rhs()))
                if mask_bit == 32:
                    while True:
                        rb_puts(inspect("mask_count, current_mask"))
                        rb_puts(inspect(mask_count))
                        current_mask = 1 << mask_count
                        rb_puts(inspect(current_mask))
                        if whole_mask & current_mask == 0:
                            new_rhs = Expression.create_integer_constant(
                                current_mask, self._locale
                            )
                            join.change_rhs(new_rhs)
                            whole_mask = whole_mask | current_mask
                            mask_place = mask_count
                            break
                        if current_mask >= 0x8000:
                            mask_place = 0
                            break
                        mask_count = mask_count + 1
                else:
                    mask_place = _to_i(to_s(join.get_rhs()))
                    current_mask = 1 << mask_place
                    new_rhs = Expression.create_integer_constant(
                        current_mask, self._locale
                    )
                    join.change_rhs(new_rhs)
                file2.print(f"\t\tMASK = {mask_place};\n")

            file2.print("\t};\n")
            file2.print("\n")

        file2.close()
