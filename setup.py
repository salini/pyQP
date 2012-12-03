#! /usr/bin/env python

# System imports
from distutils.core import setup, Extension
from distutils.command.build_py import build_py

# Third-party modules - we depend on numpy for everything
import numpy

# Obtain the numpy include directory. This logic works across numpy versions.
try:
    numpy_include = numpy.get_include()
except AttributeError:
    numpy_include = numpy.get_numpy_include()

# pyQP extension module
_pyQP = Extension("pyQP._pyQP",
                   ["pyQP/QuadProg++.cpp","pyQP/Array.cpp","pyQP/pyQP.i"],
                   include_dirs = ['pyQP', numpy_include],
                   swig_opts = ["-c++"],
                   )

# py setup
dist = setup(  name        = "pyQP",
        description = "Swig of QuadProg++, quadratic solver using an active-set dual method.",
        author      = "Joseph Salini",
        url         = 'https://github.com/salini/pyQP',
        version     = "0.1",
        ext_modules = [_pyQP],
        packages    = ["pyQP"],
        )

# Rerun the build_py to ensure that swig generated py files are also copied
build_py = build_py(dist)
build_py.ensure_finalized()
build_py.run()
