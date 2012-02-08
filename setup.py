#!/usr/bin/env python

from setuptools import setup, find_packages

tests_require = [
    'nose ==1.1.2',
]

install_requires = [
    'pyparsing==1.5.6',
]

setup(
    name='pabl',
    version='0.0.1',
    author='PoundPay',
    author_email='dev@poundpay.com',
    url='http://github.com/poundpay/pabl',
    description='Python API Building Language',
    long_description=__doc__,
    packages=find_packages(exclude=("tests",)),
    zip_safe=False,
    install_requires=install_requires,
    tests_require=tests_require,
    extras_require={'test': tests_require},
    include_package_data=True,
    entry_points={},
)
