"""HRP2TaskPlugin.rb の移植（内部仕様9章）。HRP2 のタスク（CRE_TSK/DEF_TEX/SAC_TSK）と ATT_MOD を生成する。"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin
from tecsgen.ruby_compat import Y, inspect, rb_puts, sym, to_s, truthy


class HRP2TaskPlugin(HRP2KernelObjectPlugin):
    # ATT_MODを生成済みかどうか
    _generate_memory_module: ClassVar[bool] = False

    @classmethod
    def reset(cls) -> None:
        HRP2TaskPlugin._generate_memory_module = False

    def print_cfg_cre(self, file: Any, cell: Any, val: Any, tab: Any) -> None:
        # $cbp$の代わり
        index = cell.get_id() - self._celltype.get_id_base()
        cell_cb_name = f"{index}"
        # CRE_XXX/DEF_XXXの生成
        dbg_print("assign task plugin\n")
        domain_option = (
            cell.get_region().get_domain_root().get_domain_type().get_option()
        )
        v = {
            n: val.get(sym(n))
            for n in (
                "id",
                "taskAttribute",
                "priority",
                "systemStackSize",
                "userStackSize",
                "exceptionAttribute",
            )
        }
        if domain_option != "OutOfDomain":
            # 保護ドメインに属する場合
            if domain_option == "trusted":
                # カーネルドメイン
                if v["userStackSize"] != "OMIT":
                    raise RuntimeError("system task cannot have user stack.")
                rb_puts(
                    inspect(
                        f"CRE_TSK 0 user={to_s(v['userStackSize'])} system={to_s(v['systemStackSize'])}"
                    )
                )
                file.print(
                    f"{tab}CRE_TSK({v['id']}, {{ {v['taskAttribute']}, {cell_cb_name}, tTask_start_task, {v['priority']}, {v['systemStackSize']}, NULL }});\n"
                )
            else:
                # ユーザドメイン
                if v["userStackSize"] == "OMIT":
                    raise RuntimeError("user task must have user stack.")
                rb_puts(inspect("CRE_TSK 1"))
                if v["systemStackSize"] == "OMIT":
                    file.print(
                        f"{tab}CRE_TSK({v['id']}, {{ {v['taskAttribute']}, {cell_cb_name}, tTask_start_task, {v['priority']}, {v['userStackSize']}, NULL }});\n"
                    )
                else:
                    rb_puts(inspect("CRE_TSK 2"))
                    file.print(
                        f"{tab}CRE_TSK({v['id']}, {{ {v['taskAttribute']}, {cell_cb_name}, tTask_start_task, {v['priority']}, {v['userStackSize']}, NULL, {v['systemStackSize']}, NULL }});\n"
                    )
        else:
            # 無所属の場合
            raise RuntimeError(f"task {v['id']} must belong to a domain.")

        # 例外用のを生成
        file.print(
            f"{tab}DEF_TEX({v['id']}, {{ {v['exceptionAttribute']}, tTask_start_exception }});\n"
        )

    def print_cfg_sac(self, file: Any, val: Any, acv: Any) -> None:
        file.puts(
            f"SAC_TSK({val.get(sym('id'))}, {{ {acv[0]}, {acv[1]}, {acv[2]}, {acv[3]} }});"
        )

    def gen_factory(self, file: Any) -> None:
        """ATT_MODの生成。

        gen_factory実行時には，すべてのセルタイププラグインを生成済みのはずなので，
        カーネルAPIコードのメモリ保護を省略できる．
        """
        from tecsgen.core.componentobj.cell import Cell
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.region import Region
        from tecsgen.core.generate import AppFile

        super().gen_factory(file)
        if HRP2TaskPlugin._generate_memory_module:
            return  # 何もしない
        gen = get_context().gen
        check_celltype_list: list[Any] = []

        for cell in Cell.get_cell_list2():
            # すべてのセルを走査してセルタイプをチェック
            ct = cell.get_celltype()
            if type(ct) is not Celltype or any(ct is c for c in check_celltype_list):
                continue  # 何もしない
            # チェック済みセルタイプに登録
            check_celltype_list.append(ct)

            # 未チェックのセルタイプだった場合
            rb_puts(f"check for ATT_MOD : {to_s(ct.get_global_name())}")

            # カーネルAPIのコード，データはメモリ保護しない
            if HRP2KernelObjectPlugin.include_celltype(ct):
                continue

            # 必要のないセルタイプのコード，データはメモリ保護しない
            if not ct.need_generate():
                continue

            # HRP2のドメインリージョンを取得
            regions_hrp2 = ct.get_domain_roots()[Y.HRP2]
            dbg_print(f"HRP2 domain in {to_s(ct.get_name())}: ")
            for reg in regions_hrp2:
                dbg_print(to_s(reg.get_name()))
            rb_puts("")

            has_root = any(r is Region.get_root() for r in regions_hrp2)

            # セル管理ブロックとスケルトンのメモリ保護
            # gen_celltype_names_domain 相当の処理
            if not has_root and len(regions_hrp2) > 1:
                # ドメインが複数で，OutOfDomainにセルが存在しないセルタイプの場合
                # 共有のセル管理ブロックとスケルトンコードを登録する
                f = AppFile.open(f"{gen}/tecsgen.cfg")
                f.print(f'ATT_MOD("{to_s(ct.get_global_name())}_tecsgen.o");\n')
                f.close()

            for reg in regions_hrp2:
                if reg.is_root():
                    nsp = ""
                else:
                    nsp = f"_{to_s(reg.get_namespace_path().get_global_name())}"
                f = AppFile.open(f"{gen}/tecsgen{nsp}.cfg")
                f.print(f'ATT_MOD("{to_s(ct.get_global_name())}{nsp}_tecsgen.o");\n')
                f.close()

            # セルタイプコードがない場合はスキップ
            if ct.is_all_entry_inline() and not truthy(ct.is_active()):
                continue

            # セルタイプコードのメモリ保護
            # gen_celltype_names_domain2 相当の処理
            if has_root or len(regions_hrp2) > 1:
                # OutOfDomainにセルが存在するセルタイプの場合
                # または，複数のドメインにセルが存在するセルタイプの場合
                # セルタイプコードを共有するように登録する
                f = AppFile.open(f"{gen}/tecsgen.cfg")
            else:
                # OutOfDomainでない単一のドメインにセルが存在するセルタイプの場合
                # セルタイプコードを専有するように登録する
                f = AppFile.open(
                    f"{gen}/tecsgen_{to_s(regions_hrp2[0].get_namespace_path().get_global_name())}.cfg"
                )

            f.print(f'ATT_MOD("{to_s(ct.get_global_name())}.o");\n')
            f.close()

        HRP2TaskPlugin._generate_memory_module = True
