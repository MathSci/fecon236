#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
#  Python package installation                        Date : 2018-11-29
'''
_______________|  fecon236/__init__.py :: Project import architecture

- Clarify the essential namespace for this project.
- Simplify the import of modules, possibly with shorter names.
- Highlight useful functions within long modules.
- Provide an annotated tree map of the project package.

Q:  What are these "# noqa" comments about?
A:  When something is IMPORTED BUT UNUSED, flake8 lint alerts as F401.
        That comment says, "Don't worry, that thing is intentional."

References:  https://github.com/kennethreitz/samplemod
             https://github.com/kennethreitz/setup.py

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-11-29  Add creditprof() in new rates/credit module.
2018-06-22  Annotated TREE "map" for package directory.
2018-06-21  Include boltzmann module as boltz.
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

from fecon236.boots import bootstrap as bs                               # noqa
from fecon236.prob import sim                                            # noqa
from fecon236.math import matrix as mat                                  # noqa
from fecon236.ml import learn                                            # noqa
from fecon236.prtf import boltzmann as boltz                             # noqa

from fecon236.futures.cftc import groupcotr                              # noqa
from fecon236.econ.infl import foreinfl                                  # noqa
from fecon236.rates.fedfunds import forefunds                            # noqa
from fecon236.rates.credit import creditprof                             # noqa


map = '''Annotated tree map of package directory [with module aliases]
    fecon236
    ├── __init__.py   (Router, sole non-empty __init__.py file herein)
    ├── tool.py       (Tools, low-level essentials)
    ├── top.py        (Top priority, experimental)
    ├── boots   (Bootstrap)
    │   └── bootstrap.py   [bs]
    ├── dst   (Distributions)
    │   └── gaussmix.py   [gmix]
    ├── econ
    │   └── infl.py
    ├── futures
    │   └── cftc.py
    ├── host
    │   ├── fred.py
    │   ├── hostess.py
    │   ├── qdl.py
    │   ├── _ex_Quandl.py
    │   └── stock.py
    ├── math
    │   └── matrix.py   [mat]
    ├── ml   (Machine Learning)
    │   └── learn.py
    ├── oc   (Optimization Control)
    │   └── optimize.py   [op]
    ├── parse
    │   └── sec.py
    ├── prob   (Probability)
    │   └── sim.py   (Simulation)
    ├── prtf   (Porfolio theory)
    │   └── boltzmann.py   [boltz]
    ├── rates  (Fixed Income)
    │   ├── credit.py
    │   └── fedfunds.py
    ├── tsa    (Time Series Analysis)
    │   └── holtwinters.py   [hw]
    ├── util   (Utilities)
    │   ├── group.py
    │   └── system.py
    └── visual
        └── plots.py
'''


__version__ = '10.8.0'
#             ^MAJOR.MINOR.MICRO release (updated by ./bin/up-pypi).
#              The alpha "a" or beta "b" tag is based on Travis build number.
#              Release candidates will be denoted by "c" (not rc).
#              Any .post handle is date-based.
#  For public versioning from PyPI viewpoint, use: "pip show fecon236"
