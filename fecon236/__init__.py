#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
#  Python package installation                        Date : 2018-06-20
'''
_______________|  fecon236/__init__.py :: Top installation goods

- Clarify the essential namespace for this project.
- Simplify the import of modules, possibly with shorter names.
- Highlight useful functions within long modules.

Q:  What are these "# noqa" comments about?
A:  When something is IMPORTED BUT UNUSED, flake8 lint alerts as F401.
        That comment says, "Don't worry, that thing is intentional."

References:  https://github.com/kennethreitz/samplemod
             https://github.com/kennethreitz/setup.py

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-20  Arrange star imports.
2018-06-18  Include top, fedfunds, group, cftc, infl modules.
2018-06-15  Include get() from host/hostess.py.
2018-06-13  Include matrix and learn modules, but not sec.
2018-06-10  Include plotn(). __version__ updates by ./bin/up-pypi
2018-06-07  Include stock, gaussmix, and sim modules.
2018-05-30  Include optimize module. Delete core module.
2018-05-22  Include qdl module.
2018-05-15  Include plot() as principal.
2018-05-13  Include principal modules.
2018-05-01  Clarify use of hand-coded __version__.
2018-04-25  Hand-code __version__. First pass tests: Travis build 18.
2018-04-23  First version.
'''

from __future__ import absolute_import, print_function, division

import numpy as np                                                       # noqa
import pandas as pd                                                      # noqa
from fecon236.util import system                                         # noqa
from fecon236.util import group                                          # noqa
from fecon236 import top                                                 # noqa
from fecon236.tool import *                                              # noqa
from fecon236.host.fred import *                                         # noqa
from fecon236.host.qdl import *                                          # noqa
from fecon236.host.stock import *                                        # noqa
from fecon236.host.hostess import get                                    # noqa
from fecon236.visual import plots                                        # noqa
from fecon236.visual.plots import plot, plotn, boxplot                   # noqa
from fecon236.tsa import holtwinters as hw                               # noqa
from fecon236.oc import optimize as op                                   # noqa
from fecon236.dst import gaussmix as gmix                                # noqa
from fecon236.dst.gaussmix import gemrat, gm2gem                         # noqa
from fecon236.prob import sim                                            # noqa
from fecon236.math import matrix as mat                                  # noqa
from fecon236.ml import learn                                            # noqa
from fecon236.econ.infl import foreinfl                                  # noqa
from fecon236.rates.fedfunds import forefunds                            # noqa
from fecon236.futures.cftc import groupcotr                              # noqa


__version__ = '10.6.7b70'
#             ^MAJOR.MINOR.MICRO release (updated by ./bin/up-pypi).
#              The alpha "a" or beta "b" tag is based on Travis build number.
#              Release candidates will be denoted by "c" (not rc).
#              Any .post handle is date-based.
#  For public versioning from PyPI viewpoint, use: "pip show fecon236"
