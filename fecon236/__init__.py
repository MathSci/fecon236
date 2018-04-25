#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
#  Python package installation                        Date : 2018-04-23
'''
_______________|  fecon236/__init__.py :: Top installation goods.

- Derive __version__ as string.
- Clarify the essential namespace for this project.
- Import essential modules, possibly with shorter names.

Q:  What are these "# noqa" comments about?
A:  When something is IMPORTED BUT UNUSED, flake8 lint alerts as F401.
        That comment says, "Don't worry, that thing is intentional."

References:  https://github.com/kennethreitz/samplemod
             https://github.com/kennethreitz/setup.py

CHANGE LOG  For latest version, see https://git.io/fecon236
2018-04-23  First version.
'''

# py2rm
from __future__ import absolute_import, print_function

from .util import system                # noqa
from .core import hellocore             # noqa
