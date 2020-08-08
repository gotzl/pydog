from setuptools import setup, Extension
import numpy

setup(
    name='pydog',
    py_modules=[
        'pydog',
        ],
    ext_modules=[Extension(
        'pydog_helper', 
        include_dirs = [numpy.get_include()],
        sources = ['pydog_helper.c'])],
    version=0.1,
    description='EA DOG LCD display interface',
)