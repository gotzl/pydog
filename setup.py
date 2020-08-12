from setuptools import setup, Extension

setup(
    name='pydog',
    py_modules=[
        'pydog',
        ],
    ext_modules=[Extension(
        'pydog_helper', 
        sources = ['pydog_helper.c'])],
    version=0.1,
    description='EA DOG LCD display interface',
)
