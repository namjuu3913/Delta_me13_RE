from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension, build_ext

ext_modules = [
    Pybind11Extension(
        "config_dy",
        ["config_dy.cpp"],
    ),
]

setup(
    name="pybind11-example",
    version="0.0.1",
    author="Your Name",
    author_email="your@email.com",
    description="A test project using pybind11",
    ext_modules=ext_modules,
    cmdclass={"build_ext": build_ext},
    zip_safe=False,
)