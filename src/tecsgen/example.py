"""tree-sitter 製 CDL パーサ・C ヘッダ用パーサの動作確認用スクリプト。"""

from tree_sitter import Parser

from tecsgen.syntax.languages import cdecl_language, cdl_language

SAMPLE_CDL = b"""
celltype tTask {
    entry sTask eTask;
};
"""

SAMPLE_C_HEADER = b"""
typedef int int_t;
struct point { int_t x; int_t y; };
"""


def main() -> None:
    print("=== CDL ===")
    print(Parser(cdl_language()).parse(SAMPLE_CDL).root_node)
    print("=== C header (import_C) ===")
    print(Parser(cdecl_language()).parse(SAMPLE_C_HEADER).root_node)
