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
2018-06-16  Spin-off Holt-Winters section to tsa/holtwinters.py.
2018-06-14  Spin-off group stuff to util/group.py.
                Spin-off get() to host/hostess.py.
2018-06-13  Rename to top.py, fecon236 fork. Lint bugs:
                too many undefined names (module specs) and bare excepts.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system


def foreinfl(n=120, alpha=1.0, beta=0.3673):
    '''Forecast Unified Inflation 1-year ahead per fred-inflation.ipynb.'''
    #  Holt-Winters parameters alpha and beta are optimized
    #  from the 1960-2018 dataset, consisting of 697 monthly points.
    #  Each "way" is an orthogonal method, to be averaged as way[0].
    way = [-9, -9, -9, -9, -9]
    inflall = get(m4infl)  # synthetic Unified Inflation, monthly.
    infl = tail(inflall, n)
    #                    ^Default n=120 months, i.e. last 10 years.
    way[1] = str(infl.index[-1]).replace(" 00:00:00", "")
    #                ^Most recent month for CPI, CPIc, PCE, PCEc data.
    gm = gemrat(infl, yearly=12)
    way[2] = gm[0]  # Geometric Mean Rate over n months.
    hw = foreholt(infl, 12, alpha, beta)  # Holt-Winters model.
    way[3] = (tailvalue(hw) - 1) * 100   # Convert forecasted level to rate.
    bond10 = get(m4bond10)
    tips10 = get(m4tips10)
    bei = todf(bond10 - tips10)   # 10-year BEI Break-even Inflation.
    #         ^Bond market data will be more recent than m4infl.
    way[4] = tailvalue(bei)
    #        Final forecast is the AVERAGE of orthogonal ways:
    way[0] = sum(way[2:]) / len(way[2:])
    #     "way" in SUMMARY is thus: [Average, "infl-date", GMR, HW, BEI]
    #                e.g. [2.2528, '2018-01-01', 1.5793, 3.0791, 2.1000]
    return way


if __name__ == "__main__":
    system.endmodule()
