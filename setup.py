#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Name: pwsearch PyPI setup file
Creator: K4YT3X
Date Created: June 14, 2021
Last Modified: June 14, 2021

pip3 install --user -U setuptools wheel twine
python3 setup.py sdist bdist_wheel
python3 -m twine upload --repository pypi dist/*
"""

import setuptools

with open("README.md", "r") as fh:
    LONG_DESCRIPTION = fh.read()

setuptools.setup(
    name="pwsearch",
    version="1.0.0",
    author="K4YT3X",
    author_email="k4yt3x@k4yt3x.com",
    description="PwnWiki 命令行搜索工具",
    long_description=LONG_DESCRIPTION,
    long_description_content_type="text/markdown",
    url="https://github.com/k4yt3x/pwsearch",
    packages=setuptools.find_packages(),
    license="GNU General Public License v3.0",
    install_requires=["pymediawiki", "rich"],
    classifiers=[
        "Topic :: Security",
        "Environment :: Console",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Operating System :: OS Independent",
    ],
    python_requires=">=3.6",
    entry_points={"console_scripts": ["pwsearch = pwsearch:main"]},
)
