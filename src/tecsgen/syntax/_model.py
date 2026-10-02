"""文法アクションが使うモデルのクラスと関数をまとめて読み込む（循環 import を避けるため）。

cdl_actions・cdecl_actions は、パーサ（cdl_parser）がモデルより先に読み込まれるので、
モデルのモジュールをアクションの実行時に読み込む。
"""

from __future__ import annotations

from tecsgen.core.c_types import (
    CArrayType,
    CBoolType,
    CDefinedType,
    CEnumType,
    CFloatType,
    CFuncType,
    CIntType,
    CPtrType,
    CStructType,
    CType,
    CVoidType,
)
from tecsgen.core.cdl_types import (
    ArrayType,
    BoolType,
    DefinedType,
    DescriptorType,
    EnumType,
    FloatType,
    FuncType,
    IntType,
    PtrType,
    StructType,
    VoidType,
)
from tecsgen.core.componentobj.cell import Cell
from tecsgen.core.componentobj.celltype import Celltype
from tecsgen.core.componentobj.compositecelltype import CompositeCelltype
from tecsgen.core.componentobj.factory import Factory
from tecsgen.core.componentobj.generate import Generate
from tecsgen.core.componentobj.import_c import Import_C
from tecsgen.core.componentobj.import_cdl import Import
from tecsgen.core.componentobj.join import Join
from tecsgen.core.componentobj.namespace import Namespace
from tecsgen.core.componentobj.namespacepath import NamespacePath
from tecsgen.core.componentobj.port import Port
from tecsgen.core.componentobj.region import Region
from tecsgen.core.componentobj.reversejoin import ReverseJoin
from tecsgen.core.componentobj.signature import Signature
from tecsgen.core.expression import C_EXP, Expression
from tecsgen.core.generator import Generator, Token
from tecsgen.core.syntaxobj.decl import Decl
from tecsgen.core.syntaxobj.funchead import FuncHead
from tecsgen.core.syntaxobj.namedlist import NamedList
from tecsgen.core.syntaxobj.paramdecl import ParamDecl
from tecsgen.core.syntaxobj.paramlist import ParamList
from tecsgen.core.syntaxobj.typedef import Typedef
from tecsgen.core.tool_info import TOOL_INFO
from tecsgen.ruby_compat import Y, gsub, rb_to_f, rb_to_i, sym, truthy


__all__ = [
    "ArrayType",
    "BoolType",
    "CArrayType",
    "CBoolType",
    "CDefinedType",
    "CEnumType",
    "CFloatType",
    "CFuncType",
    "CIntType",
    "CPtrType",
    "CStructType",
    "CType",
    "CVoidType",
    "C_EXP",
    "Cell",
    "Celltype",
    "CompositeCelltype",
    "Decl",
    "DefinedType",
    "DescriptorType",
    "EnumType",
    "Expression",
    "Factory",
    "FloatType",
    "FuncHead",
    "FuncType",
    "Generate",
    "Generator",
    "Import",
    "Import_C",
    "IntType",
    "Join",
    "NamedList",
    "Namespace",
    "NamespacePath",
    "ParamDecl",
    "ParamList",
    "Port",
    "PtrType",
    "Region",
    "ReverseJoin",
    "Signature",
    "StructType",
    "TOOL_INFO",
    "Token",
    "Typedef",
    "VoidType",
    "Y",
    "gsub",
    "rb_to_f",
    "rb_to_i",
    "sym",
    "truthy",
]
