#!/usr/bin/env python
# This file is part of py-endicia.  The COPYRIGHT file at the top level of
# this repository contains the full copyright notices and license terms.
from setuptools import setup, find_packages, Command

class XMLTests(Command):
    """Runs the tests and save the result to an XML file

    Running this requires unittest-xml-reporting which can
    be installed using::

        pip install unittest-xml-reporting

    """
    description = "Run test with coverage"

    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import coverage
        import xmlrunner
        cov = coverage.coverage(source=["endicia"])
        cov.start()
        from tests import suite
        xmlrunner.XMLTestRunner(output="xml-test-results").run(suite())
        cov.stop()
        cov.save()
        cov.xml_report(outfile="coverage.xml")

class Audit(Command):
    """Audits source code using PyFlakes for following issues:
        - Names which are used but not defined or used before they are defined.
        - Names which are redefined without having been used.
    """
    description = "Audit source code with PyFlakes"
    user_options = []

    def initialize_options(self):
        pass

    def finalize_options(self):
        pass

    def run(self):
        import os, sys
        try:
            import pyflakes.scripts.pyflakes as flakes
        except ImportError:
            print "Audit requires PyFlakes installed in your system."
            sys.exit(-1)

        warns = 0
        # Define top-level directories
        dirs = ('.')
        for dir in dirs:
            for root, _, files in os.walk(dir):
                if root.startswith(('./build', './doc')):
                    continue
                for file in files:
                    if not file.endswith(('__init__.py', 'upload.py')) \
                            and file.endswith('.py'):
                        warns += flakes.checkPath(os.path.join(root, file))
        if warns > 0:
            print "Audit finished with total %d warnings." % warns
            sys.exit(-1)
        else:
            print "No problems found in sourcecode."
            sys.exit(0)


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
    test_suite='tests.suite',
    cmdclass={
        'xmltests': XMLTests,
        'audit': Audit,
    },
)
