"""HRP2Plugin.rb の移植（内部仕様9章）。HRP2 カーネル用ドメインプラグイン。

各メソッドの役割りは DomainPlugin.rb を参照のこと。Ruby 版は進行状況を `puts`／`print` で標準出力へ書く。
"""

from __future__ import annotations

from typing import Any

from tecsgen.plugin.DomainPlugin import DomainPlugin
from tecsgen.ruby_compat import Y, rb_print, rb_puts, sym, to_s


class HRP2Plugin(DomainPlugin):
    def __init__(self, region: Any, name: Any, option: Any) -> None:
        super().__init__(region, name, option)
        rb_print(
            f"HRP2Plugin: initialize: region={to_s(region.get_name())}, domainName={to_s(name)}, option={to_s(option)}\n"
        )
        self._region = region
        self._name = name

        if option in ("trusted", "nontrusted", "OutOfDomain"):
            self._option = option
        else:
            self.cdl_error(
                "HRPPlugin: '$1' is unacceptable domain kind, specify 'trusted' or 'nontrusted'",
                option,
            )
            self._option = "trusted"  # とりあえず trusted を設定しておく

    def add_through_plugin(
        self, join: Any, current_region: Any, next_region: Any, through_type: Any
    ) -> Any:
        from tecsgen.plugin.HRP2KernelObjectPlugin import HRP2KernelObjectPlugin

        rb_print(
            f"HRP2Plugin: add_through_plugin: {to_s(current_region.get_name())}=>{to_s(next_region.get_name())}, "
            f"{to_s(join.get_owner().get_name())}.{to_s(join.get_definition().get_name())}=>"
            f"{to_s(join.get_cell().get_name())}.{to_s(join.get_port_name())}, {to_s(through_type)}\n"
        )

        rb_puts("=====Join Check Start=====")
        rb_puts(
            f"caller: {to_s(join.get_owner().get_name())}, callee: {to_s(join.get_cell().get_name())}"
        )
        rb_puts("=====Join Check param=====")
        current_domain = current_region.get_domain_root().get_domain_type()
        next_domain = next_region.get_domain_root().get_domain_type()
        rb_puts(to_s(current_domain.get_option()))
        if next_domain is not None:
            rb_puts(to_s(next_domain.get_option()))
        else:
            rb_puts("next domain is nil!")

        if HRP2KernelObjectPlugin.include_celltype(join.get_cell().get_celltype()):
            # 結合先がカーネルオブジェクトセル: 何もしないthrough
            rb_puts(
                f"***** {to_s(join.get_cell().get_celltype().get_name())} is kernel object"
            )
            return []
        elif to_s(next_domain.get_option()) == "OutOfDomain":
            # 結合先が無所属
            rb_puts("***** nil")
            return []
        elif (
            to_s(current_domain.get_option()) != "trusted"
            and to_s(next_domain.get_option()) == "trusted"
        ):
            # ユーザドメインからカーネルドメインへの結合
            rb_puts("***** svc")
            return [sym("HRP2SVCPlugin"), ""]
        elif current_domain is not next_domain:
            # ユーザドメインから別のユーザドメインへの結合
            rb_puts("***** rpc")
            return [
                sym("HRP2RPCPlugin"),
                "channelCelltype=tMessagebufferChannel,noClientSemaphore=true",
            ]
        else:
            # その他: 何もしないthrough
            rb_print("warning: at HRP2 Join Check")
            return None

    def get_kind(self) -> Any:
        """ドメイン種別を返す（:kernel, :user, :OutOfDomain）。"""
        if self._option == "trusted":
            return Y.kernel
        elif self._option == "nontrusted":
            return Y.user
        elif self._option == "OutOfDomain":
            return Y.OutOfDomain
        return None

    def joinable(
        self, current_region: Any, next_region: Any, through_type: Any
    ) -> bool:  # Ruby: joinable?
        rb_print(
            f"HRP2Plugin: joinable? from {to_s(current_region.get_name())} to {to_s(next_region.get_name())} ({to_s(through_type)})\n"
        )
        return True

    @classmethod
    def gen_post_code(cls, file: Any) -> None:
        pass
