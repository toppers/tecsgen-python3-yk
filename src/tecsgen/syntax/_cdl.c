/* tree-sitter の CDL 文法（grammars/cdl/parser.c）を Python へ公開する拡張モジュール。
 * tree-sitter 公式の Python バインディング（bindings/python）と同じ形。 */
#include <Python.h>

typedef struct TSLanguage TSLanguage;

const TSLanguage *tree_sitter_cdl(void);

static PyObject *language(PyObject *Py_UNUSED(self), PyObject *Py_UNUSED(args)) {
    return PyCapsule_New((void *)tree_sitter_cdl(), "tree_sitter.Language", NULL);
}

static PyMethodDef methods[] = {
    {"language", language, METH_NOARGS, "Get the tree-sitter language for CDL."},
    {NULL, NULL, 0, NULL},
};

static struct PyModuleDef module = {
    .m_base = PyModuleDef_HEAD_INIT,
    .m_name = "_cdl",
    .m_doc = "tree-sitter language for TECS CDL",
    .m_size = -1,
    .m_methods = methods,
};

PyMODINIT_FUNC PyInit__cdl(void) {
    return PyModule_Create(&module);
}
