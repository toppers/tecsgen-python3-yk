"""node.rb の移植。全モデルクラスの基底 `Node`・`BDNode`・`NSBDNode`（内部仕様4章）。

Node の直接の子クラス: C_EXP, Type, BaseVal, BDNode（ほとんどのものは BDNode の子クラス）。
Node に（BDNode にも）入らないもの: Token, Import, Import_C, Generate。

エラーは cdl_error を通じて報告する（意味解析が構文解析後に行われる場合でも、
生成時に記憶した位置で行番号を出力できる）。
"""

from __future__ import annotations

from typing import TYPE_CHECKING, Any

from tecsgen.context import dbg_print
from tecsgen.core.generator import Generator, Locale
from tecsgen.core.tecs_lang import Console
from tecsgen.ruby_compat import to_s, truthy

if TYPE_CHECKING:
    from tecsgen.core.componentobj.namespace import Namespace


class Node:
    _locale: Locale | None

    def __init__(self) -> None:
        self._locale = Generator.current_locale()

    def __getattr__(self, name: str) -> Any:
        """代入されていないインスタンス変数（`_x`）は、Ruby と同じく nil として読める。

        通常の属性の探索で見つからなかったときだけ呼ばれる。インスタンス変数の既定値を
        クラス属性で与えると、クラス変数の比較に混ざってしまうので、こうしている。
        """
        if name.startswith("_") and not name.startswith("__"):
            return None
        raise AttributeError(
            f"{type(self).__name__!r} object has no attribute {name!r}"
        )

    def cdl_error(self, message: str, *args: Any) -> None:
        """エラーを出力する。"""
        Generator.error2(self._locale, message, *args)

    def cdl_error2(self, locale: Locale | None, message: str, *args: Any) -> None:
        """エラーを出力する。locale は構文解析中は無視される。"""
        Generator.error2(locale, message, *args)

    def cdl_error3(self, locale: Any, message: str, *args: Any) -> None:
        """エラーを出力する。構文解析中でも locale を別の行に出力する。"""
        Generator.error(message, *args)
        Console.puts(
            f"check: {to_s(locale[0])}: line {to_s(locale[1])} for above error"
        )

    def cdl_warning(self, message: str, *args: Any) -> None:
        Generator.warning2(self._locale, message, *args)

    def cdl_warning2(self, locale: Locale | None, message: str, *args: Any) -> None:
        Generator.warning2(locale, message, *args)

    def cdl_info(self, message: str, *args: Any) -> None:
        Generator.info2(self._locale, message, *args)

    def cdl_info2(self, locale: Locale | None, message: str, *args: Any) -> None:
        Generator.info2(locale, message, *args)

    def get_locale(self) -> Locale | None:
        return self._locale

    def set_locale(self, locale: Locale | None) -> None:
        self._locale = locale

    def locale_str(self) -> str:
        if self._locale is not None:
            return f"locale=({to_s(self._locale[0])}, {to_s(self._locale[1])})"
        return "locale=(?)"


def _current_import() -> Any:
    """Import.get_current（componentobj/import.rb、P2 で移植）。"""
    from tecsgen.core.componentobj.import_cdl import Import

    return Import.get_current()


class BDNode(Node):
    """双方向 Node（Bi Direction Node）。owner Node から参照され、owner へのリンクも持つ。

    get_owner で得られるもの（Ruby 版 node.rb のコメントを参照）:
      FuncHead => Signature, Decl => Namespace/Typedef/Celltype/..., Cell => Region/CompositeCelltype,
      Port => Celltype/Composite, Join => Cell, Namespace => Namespace（root の場合 Generator）など
    """

    _owner: Any
    _NamespacePath: Any
    _import: Any

    def __init__(self) -> None:
        super().__init__()
        self._owner = None
        self._NamespacePath = None
        self._import = _current_import()

    def set_owner(self, owner: Any) -> None:
        dbg_print(f"set_owner: {type(owner).__name__}\n")
        self._owner = owner

    def get_owner(self) -> Any:
        if self._owner is None:
            # get_name は子クラスが定義する（BDNode 自身は持たない）
            name = getattr(self, "get_name")()  # noqa: B009
            raise RuntimeError(f"Node have no owner {type(self).__name__} {to_s(name)}")
        return self._owner


class NSBDNode(BDNode):
    """Namespace 名を持つ BDNode。Namespace(Region), Signature, Celltype, CompositeCelltype, Cell。"""

    _name: Any

    def get_namespace(self) -> Namespace | None:
        """属する namespace を得る。owner を namespace にたどり着くまで上にたどる。"""
        from tecsgen.core.componentobj.namespace import Namespace

        if isinstance(self._owner, Namespace):
            return self._owner
        if self._owner is not None:
            return self._owner.get_namespace()
        # owner が無いなら "::"
        if self._name != "::":
            raise RuntimeError(
                f"non-root namespace has no owner {type(self).__name__}#{to_s(self._name)} {self!r}"
            )
        return None

    def set_namespace_path(self) -> None:
        ns = self.get_namespace()
        if ns is None:
            raise RuntimeError("get_namespace_path: no namespace found")
        name = getattr(self, "get_name")()  # noqa: B009  get_name は子クラスが定義する
        self._NamespacePath = ns.get_namespace_path().append(name)

    def get_namespace_path(self) -> Any:
        return self._NamespacePath

    def is_imported(self) -> bool:  # Ruby: is_imported?
        if truthy(self._import):
            return self._import.is_imported()
        return False  # mikan: 仮 @import が nil になるケースが追求できていない
