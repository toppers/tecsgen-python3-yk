"""tree-sitter 製 CDL パーサの動作確認用スクリプト。

DLL の場所は環境変数 TECSGEN_CDL_DLL で上書きできる。
"""

import ctypes
import os
import types

from tree_sitter import Language, Parser

DEFAULT_CDL_DLL = (
    r"E:\Crepo\toppers-tecs-svn\toppers\tecsgen\branches\ykominami_r3033"
    r"\tools-ts\tree-sitter-cdl\tree_sitter_cdl.dll"
)

SAMPLE_CDL = b"""
celltype tTask {
    entry sTask eTask;
};
"""


def load_cdl_language(dll_path: str | None = None) -> Language:
    """CDL パーサの DLL を読み込み、tree-sitter の Language を返す。"""
    path = dll_path or os.environ.get("TECSGEN_CDL_DLL", DEFAULT_CDL_DLL)
    lib = ctypes.CDLL(path)
    func = lib.tree_sitter_cdl
    func.restype = ctypes.c_void_p
    # py-tree-sitter は "tree_sitter.Language" という名前の PyCapsule を受け取る。
    # 整数ポインタを直接渡す方式は非推奨で、Windows では桁あふれする。
    capsule_new = ctypes.pythonapi.PyCapsule_New
    capsule_new.restype = ctypes.py_object
    capsule_new.argtypes = [ctypes.c_void_p, ctypes.c_char_p, ctypes.c_void_p]
    capsule: types.CapsuleType = capsule_new(func(), b"tree_sitter.Language", None)
    return Language(capsule)


def main() -> None:
    parser = Parser(load_cdl_language())
    tree = parser.parse(SAMPLE_CDL)
    print("=== Root S-Expression ===")
    print(tree.root_node)
