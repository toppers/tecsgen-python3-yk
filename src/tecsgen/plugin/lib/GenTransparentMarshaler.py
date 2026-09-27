"""GenTransparentMarshaler.rb の移植。`RPCPlugin` に mix-in される。

@task_priority:: int
@channelCelltype:: str
@channelCellName:: str
@PPAllocatorSize:: int | None

**P5 での既知の持ち越し**: このリポジトリの全155ケース中、RPCPlugin を使うケース（`rpc`・`class`・
`DataPumpHolder`）は、いずれも `generate(TransparentRPCSignaturePlugin, ...)` が参照する
`TransparentRPCSignaturePlugin` が存在しないため P2001 で失敗する（[[tecsgen内部仕様 - 09
プラグイン機構#9.7.1]] の既知の問題）。そのためこの移植では、実際に呼び出される
`initialize_transparent_marshaler` とプラグイン引数の解析までを移植し、その先でだけ呼ばれる
`gen_marshaler_celltype`・`gen_ep_func_body*`・`print_params`・`print_param_nc`・
`gen_preamble`・`gen_postamble` は `PluginNotPorted` を送出するに留める。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any, ClassVar

from tecsgen.core.plugin_module import PluginNotPorted
from tecsgen.ruby_compat import sym, to_s

# 型検査のときだけ Node の子として扱う（mixin から cdl_error を呼ぶため）
if TYPE_CHECKING:
    from tecsgen.core.syntaxobj.node import Node

    class _Base(Node):
        pass
else:
    _Base = object


class GenTransparentMarshaler(_Base):
    # プラグイン引数名と処理（サブクラスが複製して追加する。RPCPlugin.py 参照）
    RPC_PLUGIN_ARG_PROC: ClassVar[dict[str, Any]] = {}

    def set_taskPriority(self, rhs: Any) -> None:
        """プラグイン引数 taskPriority のチェック。"""
        self._task_priority = rhs

    def set_channelCelltype(self, rhs: Any) -> None:
        """プラグイン引数 channelCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._channel_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._channel_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: channeclCelltype '$1' not celltype or not found", rhs
            )

    def set_TDRCelltype(self, rhs: Any) -> None:
        """プラグイン引数 TDRCelltype のチェック。"""
        from tecsgen.core.componentobj.celltype import Celltype
        from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
        from tecsgen.core.componentobj.namespace import Namespace
        from tecsgen.core.componentobj.namespacepath import NamespacePath

        self._tdr_celltype = sym(rhs)
        nsp = NamespacePath.analyze(to_s(self._tdr_celltype))
        obj = Namespace.find(nsp)
        if not isinstance(obj, (Celltype, CompositeCelltype)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: TDRCelltype '$1' not celltype or not found", rhs
            )

    def set_channelCellName(self, rhs: Any) -> None:
        """プラグイン引数 channelCellName のチェック。"""
        import re

        self._channel_cell_name = rhs
        if not re.match(r"\A[a-zA-Z_]\w*", to_s(rhs)):
            self.cdl_error(  # type: ignore[attr-defined]
                "RPCPlugin: channeclCellName '$1' unsuitable for identifier", rhs
            )

    def set_PPAllocatorSize(self, rhs: Any) -> None:
        """プラグイン引数 PPAllocatorSize のチェック。"""
        self._pp_allocator_size = rhs

    def initialize_transparent_marshaler(self, cell_name: Any) -> None:
        """marshaler のセルタイプ名を設定する。"""
        from tecsgen.context import get_context

        # 他で初期化されてない場合に設定
        if getattr(self, "_task_priority", None) is None:
            self._task_priority = 8
        if getattr(self, "_channel_celltype", None) is None:
            self._channel_celltype = "tDataqueueOWChannel"
        if getattr(self, "_tdr_celltype", None) is None:
            self._tdr_celltype = "tTDR"
        if getattr(self, "_channel_cell_name", None) is None:
            self._channel_cell_name = f"{to_s(cell_name)}_Channel"
        if getattr(self, "_pp_allocator_size", None) is None:
            self._pp_allocator_size = None
        if getattr(self, "_b_datapumpholder", None) is None:
            self._b_datapumpholder = False

        marshaler_head_append = "DPH" if self._b_datapumpholder is True else ""
        self._marshaler_celltype_name = f"tMarshaler{marshaler_head_append}_{to_s(self._signature.get_global_name())}"
        self._unmarshaler_celltype_name = f"tUnmarshaler{marshaler_head_append}_{to_s(self._signature.get_global_name())}"
        self._marshaler_celltype_file_name = (
            f"{get_context().gen}/{self._marshaler_celltype_name}.cdl"
        )

        if self._signature.get_context() != "task":
            self.cdl_error(  # type: ignore[attr-defined]
                "RPC9999 context of signature ($1) must be 'task'. $2 is not compatible with RPCPlugin",
                self._signature.get_name(),
                self._signature.get_context(),
            )

    def gen_marshaler_celltype(self) -> None:
        """marshaler・unmarshaler のセルタイプを生成する（P5 未移植。9.7.1 によりどの既存ケースからも呼ばれない）。"""
        raise PluginNotPorted("GenTransparentMarshaler#gen_marshaler_celltype")

    def gen_ep_func_body(self, *args: Any, **kwargs: Any) -> None:
        """受け口関数の本体コードを生成する（P5 未移植。9.7.1 によりどの既存ケースからも呼ばれない）。"""
        raise PluginNotPorted("GenTransparentMarshaler#gen_ep_func_body")

    def print_params(self, *args: Any, **kwargs: Any) -> None:
        raise PluginNotPorted("GenTransparentMarshaler#print_params")

    def print_param_nc(self, *args: Any, **kwargs: Any) -> None:
        raise PluginNotPorted("GenTransparentMarshaler#print_param_nc")

    def gen_preamble(self, *args: Any, **kwargs: Any) -> None:
        raise PluginNotPorted("GenTransparentMarshaler#gen_preamble")

    def gen_postamble(self, *args: Any, **kwargs: Any) -> None:
        raise PluginNotPorted("GenTransparentMarshaler#gen_postamble")


GenTransparentMarshaler.RPC_PLUGIN_ARG_PROC = {
    "taskPriority": lambda obj, rhs: obj.set_taskPriority(rhs),
    "channelCelltype": lambda obj, rhs: obj.set_channelCelltype(rhs),
    "TDRCelltype": lambda obj, rhs: obj.set_TDRCelltype(rhs),
    "channelCell": lambda obj, rhs: obj.set_channelCellName(rhs),
    "PPAllocatorSize": lambda obj, rhs: obj.set_PPAllocatorSize(rhs),
}
