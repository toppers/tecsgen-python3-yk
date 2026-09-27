"""TECSInfoCompoPlugin.rb の移植。`CompositePlugin` for tTECSInfo（composite セルタイプ側）。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.plugin.CompositePlugin import CompositePlugin


class TECSInfoCompoPlugin(CompositePlugin):
    _cell_list: ClassVar[list[Any]] = []

    @classmethod
    def reset(cls) -> None:
        """`@@cell_list` 相当のクラス変数を初期化する（Ruby 版はプロセスごとに1回だけ実行するので
        この処理は無い。この移植のテストは1プロセスで何度も実行するため必要）。"""
        TECSInfoCompoPlugin._cell_list = []

    def __init__(self, celltype: Any, option: Any) -> None:
        """celltype:: CompositeCelltype   セルタイプ（インスタンス）"""
        super().__init__(celltype, option)
        from tecsgen.context import get_context

        ctx = get_context()
        if ctx.unopt_entry is False:
            self.cdl_info(
                "TIF0001 forcely set --unoptimize-entry by TECSInfoPlugin (by importing TECSInfo.cdl)"
            )
            ctx.unopt_entry = True

    def new_cell(self, cell: Any) -> None:
        """celltype プラグインを指定されたセルタイプのセルが生成された（セルタイププラグインに対する新しいセルの報告）。"""
        from tecsgen.core.componentobj.import_cdl import Import
        from tecsgen.core.componentobj.join import Join
        from tecsgen.core.componentobj.namespacepath import NamespacePath
        from tecsgen.core.expression import Expression
        from tecsgen.core.plugin import CFile
        from tecsgen.ruby_compat import sym, to_s

        type(self)._cell_list.append(cell)

        # TECSInfoSub セルのプロトタイプ宣言
        from tecsgen.context import get_context

        fn = f"{get_context().gen}/tmp_{to_s(cell.get_region().get_global_name())}_TECSInfoSub.cdl"
        f = CFile.open(fn, "w")
        f.print("/* prototype declaration of TECSInfoSub */\n")
        nest = cell.get_region().gen_region_str_pre(f)
        indent = "    " * nest
        f.print(
            f"{indent}[in_through()]\n"
            f"{indent}region rTECSInfo {{\n"
            f"{indent}    cell nTECSInfo::tTECSInfoSub TECSInfoSub;\n"
            f"{indent}}}; /* rTECSInfo}} */\n"
        )
        cell.get_region().gen_region_str_post(f)
        f.close()
        Import(fn)

        # セルに cTECSInfo の結合があるか？
        if cell.get_join_list().get_item(sym("cTECSInfo")) is None:
            # cTECSInfo = rTECSInfo::TECSInfosub.eTECSInfo; の追加
            nsp = NamespacePath(sym("rTECSInfo"), False)
            nsp.append_bang(sym("TECSInfoSub"))
            rhs = Expression.create_cell_join_expression(nsp, None, sym("eTECSInfo"))
            join = Join(sym("cTECSInfo"), None, rhs)
            cell.new_join(join)
