#!/usr/bin/env python3
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
#  Python package installation                        Date : 2018-04-23
'''
_______________|  fecon236/setup.py :: Installation via setuptools.

                  Essential install config file, esp. for pip.

           Rant:  pip does NOT properly resolve dependencies.
                  Setting up installation is frustrating in the
                  Python ecosystem with complex and magical incantations.

      Templates:  https://github.com/kennethreitz/samplemod
                  https://github.com/kennethreitz/setup.py

     References:  Donald Stufft, 2013, "setup.py vs requirements.txt"
                  https://caremad.io/posts/2013/07/setup-vs-requirement
     https://packaging.python.org/guides/single-sourcing-package-version

     CLASSIFERS:  https://pypi.python.org/pypi?%3Aaction=list_classifiers

CHANGE LOG  For latest version, see https://git.io/fecon236
2018-04-23  First version.
'''

import os
from setuptools import setup, find_packages


PROJECT = 'fecon236'

#  What packages are required? For example:
#  'requests', 'maya', 'records',
#  ___ATTN___ But does this list start their installations??
#             How is this connected to requirements.txt??
#             What if prequisites are already furnished by Anaconda?
REQUIRED = []


with open('README.md') as f:
    readme = f.read()

with open('LICENSE.md') as f:
    licensed = f.read()

with open('VERSION') as f:
    #  Read top-level file as pure string, deleting line return:
    versioned = f.read().strip().replace(os.linesep, '')

__version__ = versioned


setup(
    name=PROJECT,
    version=__version__,
    description='Computational tools for financial economics',
    long_description=readme,
    author='Mathematical Science Group',
    author_email='MathSci-github@googlegroups.com',
    python_requires='>=2.7.0',
    url='https://github.com/MathSci/'+PROJECT,
    install_requires=REQUIRED,
    include_package_data=True,
    packages=find_packages(exclude=('.old', 'docs', 'tests')),
    license=licensed,
    classifiers=[
        'Development Status :: 3 - Alpha',
        'License :: OSI Approved :: BSD License',
        'Topic :: Scientific/Engineering',
        'Topic :: Office/Business :: Financial :: Investment',
        'Intended Audience :: Science/Research',
        'Intended Audience :: Financial and Insurance Industry',
        'Natural Language :: English',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: Implementation :: CPython'
    ],
)


# ======================================================== Endnotes ===========


#       __________ Donald STUFFT's template included:
#      dependency_links = [
#          "http://packages.example.com/snapshots/",
#          "http://example2.com/p/bar-1.0.tar.gz",
#      ],


#       __________ STATUS Classifiers
#          'Development Status :: 1 - Planning',
#          'Development Status :: 2 - Pre-Alpha',
#          'Development Status :: 3 - Alpha',
#          'Development Status :: 4 - Beta',
#          'Development Status :: 5 - Production/Stable',
#          'Development Status :: 6 - Mature',
#          'Development Status :: 7 - Inactive',
