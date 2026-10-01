"""HRMPPlugin.rb の移植（内部仕様9章）。

`HRMPPlugin` は MultiPlugin で、付与位置（domain / class）に応じて `HRMPDomainPlugin`・
`HRMPClassPlugin` へ振り分ける。`HRMPJoinManager` は、両者が include する結合ごとの through
プラグインの選択（`add_through_plugin`）をまとめたモジュール。
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import dbg_print
from tecsgen.plugin.HRPKernelObjectManager import HRPKernelObjectManager
from tecsgen.plugin.MultiPlugin import MultiPlugin
from tecsgen.ruby_compat import sym, to_s


class HRMPPlugin(MultiPlugin):
    @classmethod
    def get_plugin(cls, super_class: Any) -> Any:
        from tecsgen.core.plugin_module import _import_plugin_class

        if super_class is _import_plugin_class("DomainPlugin"):
            dbg_print("HRMPPlugin: DomainPlugin")
            return _import_plugin_class("HRMPDomainPlugin")
        elif super_class is _import_plugin_class("ClassPlugin"):
            dbg_print("HRMPPlugin: ClassPlugin")
            return _import_plugin_class("HRMPClassPlugin")
        else:
            dbg_print("HRMPPlugin: unsupported")
            return None


class HRMPJoinManager:
    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        dbg_print(
            f"MyDomainPlugin: add_through_plugin: {to_s(current_region.get_name())}=>{to_s(next_region.get_name())}, "
            f"{to_s(join.get_owner().get_name())}.{to_s(join.get_definition().get_name())}=>"
            f"{to_s(join.get_cell().get_name())}.{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )

        current_domain = current_region.get_domain_root().get_domain_type()
        next_domain = next_region.get_domain_root().get_domain_type()

        if current_domain is not next_domain:
            from tecsgen.plugin.HRMPDomainPlugin import HRMPDomainPlugin

            HRMPDomainPlugin.add_inter_domain_join_set(join)
            if HRPKernelObjectManager.include_celltype(
                join.get_cell()
                .get_real_celltype(join.get_rhs_port1())
                .get_global_name()
            ):
                # 結合先がカーネルオブジェクトセル
                return self.add_through_plugin_class(
                    join, current_region, next_region, through_type
                )
            elif to_s(next_domain.get_option()) == "OutOfDomain":
                # 結合先が無所属
                return self.add_through_plugin_class(
                    join, current_region, next_region, through_type
                )
            elif (
                to_s(current_domain.get_option()) != "kernel"
                and to_s(next_domain.get_option()) == "kernel"
            ):
                # ユーザドメインからカーネルドメインへの結合
                return [sym("HRPSVCThroughPlugin"), ""] + list(
                    self.add_through_plugin_class(
                        join, current_region, next_region, through_type
                    )
                )
            else:
                # 別のユーザドメインへの結合
                return [
                    sym("HRPRPCPlugin"),
                    "noClientSemaphore=false,PPAllocatorSize=256",
                ]
        else:
            return self.add_through_plugin_class(
                join, current_region, next_region, through_type
            )

    def add_through_plugin_class(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        dbg_print(
            f"HRMPJoinManger: add_through_plugin_class: {to_s(current_region.get_name())}=>{to_s(next_region.get_name())}, "
            f"{to_s(join.get_owner().get_name())}.{to_s(join.get_definition().get_name())}=>"
            f"{to_s(join.get_cell().get_name())}.{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )

        # PU: Processing Unit, NPU: Non-Processing Unit
        # NPU の locality だけ見れば十分である
        # PU の情報は使用する必要がない
        # NPU が only なら PU は必ず only
        current_class_attr = (
            current_region.get_class_root().get_class_type().get_plugin().get_NPU_attr()
        )
        next_class_attr = (
            next_region.get_class_root().get_class_type().get_plugin().get_NPU_attr()
        )

        rhs_global_name = (
            join.get_cell().get_real_celltype(join.get_rhs_port1()).get_global_name()
        )
        dbg_print(
            "HRMPPlugin: Join: "
            + to_s(rhs_global_name)
            + " current:"
            + to_s(current_class_attr[sym("class_name")])
            + " next:"
            + to_s(next_class_attr[sym("class_name")])
            + "\n"
        )

        if HRPKernelObjectManager.include_celltype(rhs_global_name):
            # 呼び先がカーネルオブジェクトセル: 何もしないthrough
            dbg_print(
                f"***** {to_s(join.get_cell().get_celltype().get_name())} is kernel object\n"
            )
            return []
        else:
            dbg_print("HRMPPlugin: **** Direct Call\n")
            return []
