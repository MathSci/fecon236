#  Python Module for import                           Date : 2018-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  fedfunds.py :: Fed Funds rate module for fecon236

- For derivation of forefunds() which forecasts the Fed Funds rate,
    see https://git.io/fedfunds

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-17  Spin-off forefunds() from top.py.
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.tool import todf
from fecon236.host.hostess import get
from fecon236.tsa.holtwinters import ema


def forefunds(nearby='16m', distant='17m'):
    '''Forecast distant Fed Funds rate using Eurodollar futures.'''
    #  Derivation in fecon235/nb/qdl-libor-fed-funds.ipynb
    #  See https://git.io/fedfunds
    ffer = get('DFF')
    #      ^Retrieve Fed Funds effective rate, daily since 1954.
    ffer_ema = ema(ffer['1981':], 0.0645)
    #                    ^Eurodollar futures debut.
    #          ^Exponentially Weighted Moving Average, 30-period.
    libor_nearby = get('f4libor' + nearby)
    libor_distant = get('f4libor' + distant)
    libor_spread = todf(libor_nearby - libor_distant)
    #     spread in forward style quote since futures uses 100-rate.
    return todf(ffer_ema + libor_spread)


if __name__ == "__main__":
    system.endmodule()
