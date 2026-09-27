"""cdlinitializer.rb の移植。CDL の初期化子を扱うためのクラス（初期化子そのものではない）。"""

from __future__ import annotations

from typing import Any

from tecsgen.ruby_compat import RubyRuntimeError, Y


class CDLInitializer:
    @staticmethod
    def clone_for_composite(rhs: Any, ct_name: Any, cell_name: Any, locale: Any) -> Any:
        """初期化子のクローン。初期化子は Expression, C_EXP, Array のいずれか。"""
        from tecsgen.core.expression import C_EXP, Expression

        if type(rhs) is C_EXP:
            # C_EXP の clone を作るとともに置換
            rhs = rhs.clone_for_composite(ct_name, cell_name, locale)
        elif type(rhs) is Expression:
            rhs = rhs.clone_for_composite()
        elif type(rhs) is list:
            rhs = CDLInitializer.clone_for_compoiste_array(
                rhs, ct_name, cell_name, locale
            )
        else:
            raise RubyRuntimeError("unknown rhs for join")
        return rhs

    @staticmethod
    def clone_for_compoiste_array(
        array: list[Any], ct_name: Any, cell_name: Any, locale: Any
    ) -> list[Any]:
        """初期化子（配列）のクローン。要素は clone_for_composite を持つものだけ。"""
        # "compoiste.identifier" の場合 (CDL としては誤り)
        if array and array[0] == Y.COMPOSITE:
            return list(array)
        return [
            CDLInitializer.clone_for_composite(m, ct_name, cell_name, locale)
            for m in array
        ]
