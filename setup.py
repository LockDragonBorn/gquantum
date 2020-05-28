#!/usr/bin/env python
#-*- coding:utf-8 -*-

#############################################
# File Name: setup.py
# Author: mage
# Mail: mage@woodcol.com
# Created Time:  2018-1-23 19:17:34
#############################################


from setuptools import setup, find_packages

setup(
    name="gquantum",
    version="0.1.0",
    keywords=("quantum computer simulator", "quantum computing", "quantum information", "grace quantum"),
    description="Grace quantum computer simulator",
    long_description="Grace quantum computer simulator",
    license="MIT Licence",

    url="https://github.com/YangzheLiu/gquantum",
    author="Yangzhe Liu",
    author_email="liuyangzhe@163.com",

    packages=find_packages(),
    include_package_data=True,
    platforms="any",
    install_requires=['numpy']
)
