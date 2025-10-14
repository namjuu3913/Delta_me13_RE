from setuptools import setup
from pybind11.setup_helpers import Pybind11Extension

# Read the contents of your README file
with open("README.md", "r", encoding="utf-8") as fh:
    long_description = fh.read()

# Define the C++ extension module
ext_module = Pybind11Extension(
    "config_dy_module",      # The name of the module you will import in Python
    ["src/config_dy.cpp"],   # List of C++ source files
    # Tell the compiler where to find external headers
    include_dirs=["ExternalResorces"],
    language="c++",
)

# Main setup configuration
setup(
    name="delta-me13-config-dy", # The package name on PyPI (must be unique)
    version="0.1.0",
    author="namjuu3913",
    author_email="",
    description="A Python module for dynamic configuration only for my project, written in C++.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/namjuu3913/Delta_me13_RE", # Optional: Project URL
    ext_modules=[ext_module],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    python_requires='>=3.11',
    zip_safe=False,
)