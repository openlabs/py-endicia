#!/usr/bin/env python
#This file is part of py-endicia.  The COPYRIGHT file at the top level of
#this repository contains the full copyright notices and license terms.
from setuptools import setup, find_packages
import endicia

major_version, minor_version, _ = endicia.__version__.split('.', 2)
major_version = int(major_version)
minor_version = int(minor_version)

setup(
    name='endicia',
    version=endicia.__version__,
    description='endicia API for Python',
    author='Open Labs Business Solutions',
    maintainer="Open Labs Business Solutions",
    maintainer_email="info@openlabs.co.in",
    author_email='info@openlabs.co.in',
    url='http://www.openlabs.co.in/',
    download_url="http://downloads.openlabs.co.in/" + \
            endicia.__version__.rsplit('.', 1)[0] + '/',
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
    install_requires=[],
    test_suite='endicia.tests',
)
