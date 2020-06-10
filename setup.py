#!/usr/bin/env python
#-*- coding:utf-8 -*-

from setuptools import setup, find_packages

with open("README.md", "r") as fh:
    long_description = fh.read()

setup(
    name="gquantum",
    version="0.2.0",
    keywords=("quantum computer simulator", "quantum computing", "quantum information", "grace quantum"),
    description="Light-weighted quantum computing tool supports 31 qubits.",
    long_description=long_description,
    license="MIT Licence",

    url="https://github.com/YangzheLiu/gquantum",
    author="Yangzhe Liu",
    author_email="liuyangzhe@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['numpy']
)
