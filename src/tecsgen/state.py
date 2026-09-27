"""Ruby のクラス変数に当たる状態をまとめて初期化する（1プロセスで何度も実行するテスト用）。

Ruby 版はプロセスごとに1回だけ実行するので、この処理は無い。
"""

from __future__ import annotations


def reset_model_state() -> None:
    from tecsgen.core.cdl_types import DescriptorType, StructType, Type
    from tecsgen.core.componentobj.cell import Cell
    from tecsgen.core.componentobj.celltype import Celltype
    from tecsgen.core.componentobj.classtype import ClassType
    from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
    from tecsgen.core.componentobj.domaintype import DomainType
    from tecsgen.core.componentobj.factory import Factory
    from tecsgen.core.componentobj.import_c import Import_C
    from tecsgen.core.componentobj.import_cdl import Import
    from tecsgen.core.componentobj.join import Join
    from tecsgen.core.componentobj.namespace import Namespace
    from tecsgen.core.componentobj.region import Region
    from tecsgen.core.componentobj.signature import Signature
    from tecsgen.core.generate import AppFile
    from tecsgen.core.generator import Generator
    from tecsgen.core.plugin_module import PluginModule
    from tecsgen.core.tecsgen import TECSGEN
    from tecsgen.syntax.cdecl_parser import CdeclParser

    for cls in (
        Generator,
        CdeclParser,
        AppFile,
        TECSGEN,
        Namespace,
        Region,
        Signature,
        Celltype,
        Cell,
        CompositeCelltype,
        Join,
        Factory,
        Import,
        Import_C,
        Type,
        StructType,
        DescriptorType,
        DomainType,
        ClassType,
        PluginModule,
    ):
        cls.reset()
