#include <Python.h>
#include <numpy/arrayobject.h>

static PyObject * pydog_helper_getbuffer(PyObject* self, PyObject* args) {
    PyArrayObject *buf, *pixels;
    int width, height;

    if (!PyArg_ParseTuple(args, "OOii", &buf, &pixels, &width, &height))
        return Py_None;

    int x,y,greyscale;
    for(y=0;y<height;y++) {
        for(x=0;x<width;x++) {
            greyscale = ((pixels->data[y*width + x])/0x40)&0x3;
            buf->data[y/4 * width + x] |= ( greyscale << ((y % 4)<<1) );
        }
    }
    return Py_None;
}

static PyMethodDef module_methods[] = {
  {"getbuffer", pydog_helper_getbuffer, METH_VARARGS,
    "Fills a buffer with pixel values to upload to the display."},
  {NULL, NULL, 0, NULL},
};

static struct PyModuleDef cModPyDem =
{
    PyModuleDef_HEAD_INIT,
    "pydog_helper",
    "",
    -1,
    module_methods
};

PyMODINIT_FUNC PyInit_pydog_helper(void)
{
    return PyModule_Create(&cModPyDem);
}