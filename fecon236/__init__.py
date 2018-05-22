#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
#  Python package installation                        Date : 2018-05-22
'''
_______________|  fecon236/__init__.py :: Top installation goods.

- Clarify the essential namespace for this project.
- Simplify the import of modules, possibly with shorter names.

Q:  What are these "# noqa" comments about?
A:  When something is IMPORTED BUT UNUSED, flake8 lint alerts as F401.
        That comment says, "Don't worry, that thing is intentional."

References:  https://github.com/kennethreitz/samplemod
             https://github.com/kennethreitz/setup.py

CHANGE LOG  For latest version, see https://git.io/fecon236
2018-05-22  Include qdl module.
2018-05-15  Include plot() as principal.
2018-05-13  Include principal modules.
2018-05-01  Clarify use of hand-coded __version__.
2018-04-25  Hand-code __version__. First pass tests: Travis build 18.
2018-04-23  First version.
'''

# py2rm
from __future__ import absolute_import, print_function, division

import numpy as np                                        # noqa
import pandas as pd                                       # noqa
from fecon236.core import hellocore                       # noqa
from fecon236.tool import *                               # noqa
from fecon236.util import system                          # noqa
from fecon236.host import fred                            # noqa
from fecon236.host import qdl                             # noqa
from fecon236.visual import plots                         # noqa
from fecon236.visual.plots import plot                    # noqa
from fecon236.tsa import holtwinters as hw                # noqa


__version__ = '10.6.2a29.post180522'
#             ^HAND-CODE this string on MAJOR.MINOR releases.
#              The alpha tag is based on Travis build number.
#              The .post handle here is date-based.
#  For current installed VERSION, use: "pip show fecon236"
