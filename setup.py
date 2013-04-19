#!/usr/bin/env python
# This file is part of py-endicia.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from setuptools import setup, find_packages

version = {}
with open('endicia/version.py') as f:
    exec(f.read(), version)


setup(
    name='endicia',
    version=version['__version__'],
    description='endicia API for Python',
    author='Open Labs Business Solutions',
    maintainer="Open Labs Business Solutions",
    maintainer_email="info@openlabs.co.in",
    author_email='info@openlabs.co.in',
    url='http://www.openlabs.co.in/',
    packages=find_packages(),
    classifiers=[
        'Development Status :: 4 - Beta',
        'Environment :: Plugins',
        'Intended Audience :: Developers',
        'Intended Audience :: Financial and Insurance Industry',
        'Intended Audience :: Legal Industry',
        'License :: OSI Approved :: GNU General Public License (GPL)',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Topic :: Office/Business',
    ],
    license='GPL-3',
    install_requires=['lxml'],
    test_suite='endicia.tests',
)
