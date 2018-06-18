#  Python Module for import                           Date : 2018-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  top.py :: Top priority fecon236 experiments

- TODO: Works in progress to be moved into a subdirectory upon maturity.

USAGE
- More explicit syntax recommended: "import fecon236 as fe"
  (Former usage in notebooks was casual: "from fecon235.fecon235 import *").

REFERENCE
- Bloomberg Open Symbology which assigns a global ID for obscure financial
  instruments is now accessible via OpenFIGI, https://www.openfigi.com/search

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-17  Spin-off forefunds() to rates/fedfunds.py.
                Spin-off foreinfl() to econ/infl.py.
2018-06-16  Spin-off Holt-Winters section to tsa/holtwinters.py.
2018-06-14  Spin-off group stuff to util/group.py.
                Spin-off get() to host/hostess.py.
2018-06-13  Rename to top.py, fecon236 fork. Lint bugs:
                too many undefined names (module specs) and bare excepts.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system


#  INTENTIONALLY EMPTY... 2018-06-17 All cleared!


if __name__ == "__main__":
    system.endmodule()
