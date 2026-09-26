"""tree-sitter の文法（CDL と import_C 用の C ヘッダ）を読み込む。

文法の C ソースは grammars/ に同梱し、拡張モジュール _cdl・_tecs_cdecl として
ビルドしている（取り込み元は grammars/README.md）。
"""

from functools import cache

from tree_sitter import Language

from tecsgen.syntax import _cdl, _tecs_cdecl


@cache
def cdl_language() -> Language:
    """CDL の文法を返す。"""
    return Language(_cdl.language())


@cache
def cdecl_language() -> Language:
    """import_C で C ヘッダから型宣言を取り出すための文法を返す。"""
    return Language(_tecs_cdecl.language())
