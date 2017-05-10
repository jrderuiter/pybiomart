#!/usr/bin/env python

# -*- coding: utf-8 -*-

# pylint: disable=invalid-name

import setuptools

REQUIREMENTS = ['future', 'pandas', 'requests', 'requests_cache']

EXTRAS_REQUIRE = {
    'dev': [
        'sphinx', 'sphinx-autobuild', 'sphinx-rtd-theme', 'bumpversion',
        'pytest>=2.7', 'pytest-mock', 'pytest-helpers-namespace', 'pytest-cov',
        'python-coveralls'
    ]
}

setuptools.setup(
    name='pybiomart',
    version='0.2.0',
    url='https://github.com/jrderuiter/pybiomart',
    author='Julian de Ruiter',
    author_email='julianderuiter@gmail.com',
    description='A simple pythonic interface to biomart.',
    license='MIT',
    packages=setuptools.find_packages('src'),
    package_dir={'': 'src'},
    zip_safe=True,
    classifiers=[
        'Intended Audience :: Developers',
        'Intended Audience :: Science/Research',
        'License :: OSI Approved :: MIT License',
        'Operating System :: OS Independent',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5'
    ],
    install_requires=REQUIREMENTS,
    extras_require=EXTRAS_REQUIRE)
