from __future__ import annotations

import os
import shutil
from collections.abc import Iterator
from pathlib import Path

import pytest

from tecsgen.context import TecsgenContext, reset_context
from tecsgen.core.generate import AppFile
from tecsgen.core.generator import Generator
from tecsgen.core.tecs_lang import TECS_LANG
from tecsgen.core.tecsgen import TECSGEN
from tecsgen.host import set_host
from tecsgen.syntax.cdecl_parser import CdeclParser

# 移植元 Ruby 版 tecsgen（差分テストのオラクルに使う）。無ければ差分テストを飛ばす
RUBY_SRC = Path(
    os.environ.get(
        "TECSGEN_RUBY_SRC",
        "E:/Crepo/toppers-tecs-svn/toppers/tecsgen/branches/ykominami_r3033/tecsgen",
    )
)
GOLDEN = Path(__file__).parent / "golden" / "cases"


def ruby_available() -> bool:
    return shutil.which("ruby") is not None and (RUBY_SRC / "tecslib").is_dir()


@pytest.fixture(autouse=True)
def fresh_state() -> Iterator[TecsgenContext]:
    """テストごとに、Ruby のグローバル変数・クラス変数に当たる状態を初期化する。

    正解データの採取条件（LANG=C）に合わせて言語を設定する。
    """
    ctx = reset_context()
    Generator.reset()
    CdeclParser.reset()
    AppFile.reset()
    TECSGEN.reset()
    set_host(None)
    TECS_LANG.setup(ctx, {"LANG": "C"})
    yield ctx
    set_host(None)
