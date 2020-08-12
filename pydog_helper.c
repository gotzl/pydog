#include <Python.h>

static PyObject * pydog_helper_getbuffer(PyObject* self, PyObject* args) {
    Py_buffer buf, pixels;
    int width, height;
    uint8_t *buf_ptr, *pixels_ptr;

    if (!PyArg_ParseTuple(args, "y*y*ii", &buf, &pixels, &width, &height))
        return Py_None;

    buf_ptr = (uint8_t*) buf.buf;
    pixels_ptr = (uint8_t*) pixels.buf;

    int x,y,greyscale;
    for(y=0;y<height;y++) {
        for(x=0;x<width;x++) {
            greyscale = ((pixels_ptr[y*width + x])/0x40)&0x3;
            buf_ptr[y/4 * width + x] |= ( greyscale << ((y % 4)<<1) );
        }
    }
    PyBuffer_Release(&buf);
    PyBuffer_Release(&pixels);
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