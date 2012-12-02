#! /usr/bin/env python

# System imports
from distutils.core import *

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory. This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# pyQP extension module
_pyQP = Extension("pyQP/_pyQP",
                   ["pyQP/QuadProg++.cpp","pyQP/Array.cpp","pyQP/pyQP.i"],
                   include_dirs = ['pyQP', numpy_include],
                   swig_opts = ["-c++"],
                   )

# py setup
setup(  name        = "pyQP",
        description = "Swig of QuadProg++, quadratic solver using an active-set dual method.",
        author      = "Joseph Salini",
        url         = 'https://github.com/salini/pyQP',
        version     = "0.1",
        ext_modules = [_pyQP],
        py_modules  = ["pyQP/pyQP", "pyQP/__init__"],
        )


