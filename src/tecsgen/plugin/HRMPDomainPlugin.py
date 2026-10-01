"""HRMPDomainPlugin.rb の移植（内部仕様9章）。HRMP カーネル用ドメインプラグイン。

各メソッドの役割りは DomainPlugin.rb を参照のこと。
"""

from __future__ import annotations

from typing import Any, ClassVar

from tecsgen.context import dbg_print, get_context
from tecsgen.core.generator import Generator
from tecsgen.plugin.DomainPlugin import DomainPlugin
from tecsgen.plugin.HRMPPlugin import HRMPJoinManager
from tecsgen.plugin.lib.GenAttMod import GenAttMod, GenDefSvc
from tecsgen.ruby_compat import Y, sym, to_s


class HRMPDomainPlugin(HRMPJoinManager, GenAttMod, GenDefSvc, DomainPlugin):
    # ATT_MODを生成済みかどうか                   # 2017.8.27
    _generate_memory_module: ClassVar[dict[Any, Any]] = {}

    _include_extsvc_fncd: ClassVar[bool] = False  # 17.07.26 暫定

    # {entry_cell =>{domain_root=>count} }  Hash of inter domain join
    _inter_domain_join_set: ClassVar[dict[Any, Any]] = {}

    @classmethod
    def reset(cls) -> None:
        HRMPDomainPlugin._generate_memory_module = {}
        HRMPDomainPlugin._include_extsvc_fncd = False
        HRMPDomainPlugin._inter_domain_join_set = {}

    def __init__(self, region: Any, name: Any, option: Any) -> None:
        super().__init__(region, name, option)
        dbg_print(
            f"HRMPPlugin: initialize: region={to_s(region.get_name())}, domainName={to_s(name)}, option={to_s(option)}\n"
        )
        self._region = region
        self._name = name
        if option in ("kernel", "user", "OutOfDomain"):
            self._option = option
        else:
            self.cdl_error(
                "HRMPPlugin: '$1' is unacceptable domain kind, specify 'kernel', 'user' or 'OutOfDomain'",
                option,
            )
            self._option = "kernel"  # とりあえず kernel を設定しておく

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        dbg_print(
            f"MyDomainPlugin: joinable? from {to_s(current_region.get_name())} to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    def get_kind(self) -> Any:
        """ドメイン種別を返す（:kernel, :user, :OutOfDomain）。"""
        return sym(self._option)

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass

    def gen_factory(self, node_root: Any) -> None:
        """ATT_MODの生成。

        gen_factory実行時には，すべてのセルタイププラグインを生成済みのはずなので，
        カーネルAPIコードのメモリ保護を省略できる．
        """
        from tecsgen.core.generate import AppFile

        super().gen_factory(node_root)

        if not HRMPDomainPlugin._include_extsvc_fncd:
            file = AppFile.open(f"{get_context().gen}/tecsgen.cfg")
            file.print("/* HRMPPlugin 001 */\n")
            file.print('#include "extsvc_fncode.h"\n')  ## 2017.7.26
            file.close()
            HRMPDomainPlugin._include_extsvc_fncd = True

        if HRMPDomainPlugin._generate_memory_module.get(node_root) is None:
            HRMPDomainPlugin._generate_memory_module[node_root] = True

            # INCLUDE の生成
            self.gen_include()

            # ATT_MOD の生成
            self.gen_att_mod(node_root)

            # DEF_SVC の生成
            self.gen_def_svc(node_root)

    # ----- Inter Domain Join Set -----#
    @classmethod
    def add_inter_domain_join_set(cls, join: Any) -> None:
        rhs_cell = join.get_cell()
        dbg_print(
            f"--------- add_inter_domain:{to_s(join.get_owner().get_namespace_path())} => "
            f"{to_s(join.get_cell().get_namespace_path())}-----\n"
        )
        if HRMPDomainPlugin._inter_domain_join_set.get(rhs_cell) is None:
            HRMPDomainPlugin._inter_domain_join_set[rhs_cell] = []
        # 左辺のドメインルートを記録
        HRMPDomainPlugin._inter_domain_join_set[rhs_cell].append(join)

    @classmethod
    def get_inter_domain_join_set(cls, rhs_cell: Any) -> Any:
        if HRMPDomainPlugin._inter_domain_join_set.get(rhs_cell) is not None:
            # Array#uniq!（同一オブジェクトの重複を除く）
            uniq: list[Any] = []
            for j in HRMPDomainPlugin._inter_domain_join_set[rhs_cell]:
                if not any(j is u for u in uniq):
                    uniq.append(j)
            HRMPDomainPlugin._inter_domain_join_set[rhs_cell] = uniq
        else:
            HRMPDomainPlugin._inter_domain_join_set[rhs_cell] = []
        return HRMPDomainPlugin._inter_domain_join_set[rhs_cell]

    @classmethod
    def get_inter_domain_join_roots(cls, rhs_cell: Any) -> list[Any]:
        dbg_print(
            f"--------- get_inter_domain {to_s(rhs_cell.get_namespace_path())} -----\n"
        )
        domain_roots: list[Any] = []
        for join in cls.get_inter_domain_join_set(rhs_cell):
            dbg_print(
                f"--------- get_inter_domain:{to_s(join.get_owner().get_namespace_path())} => "
                f"{to_s(join.get_cell().get_namespace_path())}-----\n"
            )
            domain_roots.append(join.get_owner().get_region().get_domain_root())
        uniq: list[Any] = []
        for r in domain_roots:
            if not any(r is u for u in uniq):
                uniq.append(r)
        return uniq

    @classmethod
    def get_sac_str(cls, cell: Any) -> str:
        domain_roots = cls.get_inter_domain_join_roots(cell)
        delim = ""
        acv = ""
        cell_domain_root = cell.get_region().get_domain_root()
        dbg_print(
            f"get_sac_str: cell={to_s(cell.get_name())} domain_root={to_s(cell_domain_root.get_namespace_path())}\n"
        )
        for dr in domain_roots:
            dbg_print(f"   src_domain={to_s(dr.get_namespace_path())}\n")
        if cell_domain_root.get_domain_type().get_kind() != Y.OutOfDomain:
            domain_roots.append(
                cell.get_region().get_domain_root()
            )  # 結合先のドメインも含める
        b_info = False
        for dr in domain_roots:
            kind = dr.get_domain_type().get_kind()
            if kind == Y.kernel:
                acv += f"{delim}TACP_KERNEL"
                delim = "|"
            elif kind == Y.user:
                dbg_print(
                    f"cell={to_s(cell.get_name())} domain_kind={to_s(cell_domain_root.get_domain_type().get_kind())}\n"
                )
                dbg_print(
                    f"dr_src={to_s(dr.get_namespace_path())} dr_dst={to_s(cell_domain_root.get_namespace_path())}\n"
                )
                acv += f"{delim}TACP({to_s(dr.get_name())})"
                delim = "|"
                if cell_domain_root.get_domain_type().get_kind() == Y.user and to_s(
                    dr.get_namespace_path()
                ) != to_s(cell_domain_root.get_namespace_path()):
                    Generator.error(
                        "HRMP9999 '$1': kernel object joined from other user domain. "
                        "kernel object joined from multi-user-domain must be placed out of domain",
                        cell.get_name(),
                    )
            elif kind == Y.OutOfDomain:
                if cell_domain_root.get_domain_type().get_kind() == Y.OutOfDomain:
                    acv += f"{delim}TACP_SHARED"
                    delim = "|"
                else:
                    b_info = True
            else:
                raise RuntimeError("unkown domain kind")
        if acv == "":
            # 呼び先セルが無所属かつ、呼び元も無所属のみ、または結合無しの場合
            acv = "TACP_SHARED"
        sac_str = "{"
        delim = ""
        for acp in (
            Y.accessPattern1,
            Y.accessPattern2,
            Y.accessPattern3,
            Y.accessPattern4,
        ):
            init = to_s(cell.get_attr_initializer(acp))
            if init != "OMIT":
                sac_str += delim + init
            else:
                sac_str += delim + acv
                if b_info:
                    # この情報は、必要性がわからないため、とりあえず出すのはやめる
                    b_info = False  # 2度出ないようにする
            delim = ", "
        return sac_str + "}"
