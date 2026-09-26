"""tree-sitter 文法の拡張モジュールをビルドする。

プロジェクトの設定は pyproject.toml にある。ここでは C 拡張の定義だけを行う。
"""

import sys

from setuptools import Extension, setup

GRAMMARS = "src/tecsgen/syntax/grammars"


def grammar_extension(name: str) -> Extension:
    return Extension(
        name=f"tecsgen.syntax._{name}",
        sources=[f"src/tecsgen/syntax/_{name}.c", f"{GRAMMARS}/{name}/parser.c"],
        include_dirs=[f"{GRAMMARS}/{name}"],
        # MSVC は既定でソースを CP932 として読むため、UTF-8 を明示する
        extra_compile_args=["/utf-8"] if sys.platform == "win32" else ["-std=c11"],
    )


setup(ext_modules=[grammar_extension("cdl"), grammar_extension("tecs_cdecl")])
