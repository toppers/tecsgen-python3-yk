"""generate.rb の Celltype 再オープン部分（コード生成）の入口。

大きいので、生成物ごとに3つの mixin に分けた。

- `generate_celltype_ph`: セルタイプヘッダ・factory ヘッダ
- `generate_celltype_cell`: セルのグルーコード（`_tecsgen.c`）
- `generate_celltype_templ`: テンプレートコード・factory・Makefile 類
"""

from __future__ import annotations

from typing import Any

from tecsgen.context import get_context
from tecsgen.core.generate_celltype_cell import CelltypeGenerateCell
from tecsgen.core.generate_celltype_ph import CelltypeGeneratePH
from tecsgen.core.generate_celltype_templ import CelltypeGenerateTempl


class CelltypeGenerate(CelltypeGeneratePH, CelltypeGenerateCell, CelltypeGenerateTempl):
    def generate(self: Any) -> None:
        if self.need_generate():  # セルのないセルタイプは生成しない
            self.generate_private_header()
            self.generate_factory_header()
            self.generate_cell_code()
            self.generate_template_code()
            self.generate_inline_template_code()
            self.generate_celltype_factory_code()
            self.generate_cell_factory_code()
            self.generate_makefile()
        elif get_context().generate_all_template:  # テンプレートコード生成オプション
            self.generate_template_code()
            self.generate_inline_template_code()
            # generate_makefile_template は Makefile に追記するものだから、呼び出さない

    def generate_post(self: Any) -> None:
        if not self.need_generate():  # セルのないセルタイプは生成しない
            return
        self.generate_private_header_post()
        self.generate_factory_header_post()
