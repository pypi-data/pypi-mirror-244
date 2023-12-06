#!/usr/bin/env python
from setuptools import setup

# See setup.cfg for configuration.
setup(
    package_data={
        'dinkit': ['libdinkit.dylib', 'libdinkit.so', 'dinkit.dll', 'dinkit.py'],
    }
)

