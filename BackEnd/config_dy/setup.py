from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

ext_module = Pybind11Extension(
    "config_module",
    
    ["config_dy.cpp"],
    
    include_dirs=["../Lib_cpp/ExternalResorces"],
    
    language="c++",
)

setup(
    name="config_dy", 
    version="0.0.1",
    ext_modules=[ext_module],
    zip_safe=False,
)