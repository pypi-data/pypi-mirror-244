#include <Python.h>

static PyObject * meth_bgra(PyObject * self, PyObject * arg) {
    Py_buffer view;
    if (PyObject_GetBuffer(arg, &view, PyBUF_C_CONTIGUOUS | PyBUF_WRITABLE)) {
        return NULL;
    }

    int count = (int)view.len / 4;
    unsigned * const ptr = (unsigned *)view.buf;
    unsigned x, y;

    while (count--) {
        x = y = ptr[count];
        x &= 0xff00ff00ul;
        y &= 0x00ff00fful;
        y = y >> 16 | y << 16;
        ptr[count] = x | y;
    }

    PyBuffer_Release(&view);
    Py_RETURN_NONE;
}

static PyMethodDef module_methods[] = {
    {"bgra", (PyCFunction)meth_bgra, METH_O},
    {0},
};

static PyModuleDef module_def = {PyModuleDef_HEAD_INIT, "bgra", NULL, -1, module_methods};

extern PyObject * PyInit_bgra() {
    PyObject * module = PyModule_Create(&module_def);
    return module;
}
