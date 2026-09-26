/* tree-sitter の C ヘッダ用文法（grammars/tecs_cdecl/parser.c）を Python へ公開する拡張モジュール。
 * import_C で C ヘッダから型宣言を取り出すために使う。
 * tree-sitter 公式の Python バインディング（bindings/python）と同じ形。 */
#include <Python.h>

typedef struct TSLanguage TSLanguage;

const TSLanguage *tree_sitter_tecs_cdecl(void);

static PyObject *language(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    return PyCapsule_New((void *)tree_sitter_tecs_cdecl(), "tree_sitter.Language", NULL);
}

static PyMethodDef methods[] = {
    {"language", language, METH_NOARGS, "Get the tree-sitter language for import_C headers."},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_tecs_cdecl",
    .m_doc = "tree-sitter language for the import_C header type extractor",
    .m_size = -1,
    .m_methods = methods,
};

PyMODINIT_FUNC PyInit__tecs_cdecl(void) {
    return PyModule_Create(&module);
}
