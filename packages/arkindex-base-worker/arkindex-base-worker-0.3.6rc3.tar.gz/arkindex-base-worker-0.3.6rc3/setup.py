#!/usr/bin/env python
from pathlib import Path

from setuptools import find_packages, setup

setup(
    version=Path("VERSION").read_text().strip(),
    packages=find_packages(),
)
