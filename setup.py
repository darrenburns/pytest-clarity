#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import codecs
from setuptools import setup


def read(fname):
    file_path = os.path.join(os.path.dirname(__file__), fname)
    return codecs.open(file_path, encoding="utf-8").read()


setup(
    name="pytest-clarity",
    version="0.1.0a1",
    author="Darren Burns",
    author_email="darrenb900@gmail.com",
    maintainer="Darren Burns",
    maintainer_email="darrenb900@gmail.com",
    license="MIT",
    url="https://github.com/darrenburns/pytest-clarity",
    description="A plugin providing an alternative, colourful diff output for failing assertions.",
    long_description=read("README.rst"),
    packages=["pytest_clarity"],
    python_requires=">=2.7, !=3.0.*, !=3.1.*, !=3.2.*, !=3.3.*",
    install_requires=["pytest>=3.5.0", "termcolor==1.1.0"],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Framework :: Pytest",
        "Intended Audience :: Developers",
        "Topic :: Software Development :: Testing",
        "Programming Language :: Python",
        "Programming Language :: Python :: 2",
        "Programming Language :: Python :: 2.7",
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.4",
        "Programming Language :: Python :: 3.5",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: Implementation :: CPython",
        "Operating System :: OS Independent",
        "License :: OSI Approved :: MIT License",
    ],
    entry_points={"pytest11": ["clarity = pytest_clarity.plugin"]},
)
