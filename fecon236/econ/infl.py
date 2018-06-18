#  Python Module for import                           Date : 2018-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  infl.py :: Inflation module for fecon236

- "Unified" inflation is a sythesis of CPI, CPIc, PCE, PCEc.

- For derivation of foreinfl() see fecon235/nb/fred-inflation.ipynb,
    which is rendered as https://git.io/infl

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-17  Spin-off foreinfl() from top.py.
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.tool import todf, tail, tailvalue
from fecon236.host.fred import m4infl, m4bond10, m4tips10
from fecon236.host.hostess import get
from fecon236.tsa.holtwinters import foreholt
from fecon236.dst.gaussmix import gemrat


def foreinfl(n=120, alpha=1.0, beta=0.3673):
    '''Forecast Unified Inflation 1-year ahead per https://git.io/infl
       which a rendering of fecon235/nb/fred-inflation.ipynb.
       SUMMARY output: [Average, "infl-date", GMR, HW, BEI]
       e.g.  [2.2528, '2018-01-01', 1.5793, 3.0791, 2.1000]
       where Average is the mean of three orthogonal methods:
       GMR for geometric mean rate, HW for Holt-Winters time-series,
       and BEI for Break-even Inflation from the Treasury bond market.
       Default n denotes 120-month history, i.e. last 10 years.
    '''
    #  Holt-Winters parameters alpha and beta are optimized
    #  from the 1960-2018 dataset, consisting of 697 monthly points.
    #  Each "way" is an orthogonal method, to be averaged into way[0].
    way = [-9, -9, -9, -9, -9]  # dummy placeholders.
    inflall = get(m4infl)       # synthetic Unified Inflation, monthly.
    infl = tail(inflall, n)
    way[1] = str(infl.index[-1]).replace(" 00:00:00", "")
    #                ^Most recent month for CPI, CPIc, PCE, PCEc data.
    gm = gemrat(infl, yearly=12)
    way[2] = gm[0]   # Geometric Mean Rate over n months.
    hw = foreholt(infl, 12, alpha, beta)  # Holt-Winters model.
    way[3] = (tailvalue(hw) - 1) * 100    # Convert forecasted level to rate.
    bond10 = get(m4bond10)
    tips10 = get(m4tips10)
    bei = todf(bond10 - tips10)           # 10-year BEI Break-even Inflation.
    #         ^Treasury bond market data will be much more recent than m4infl.
    way[4] = tailvalue(bei)
    #  Final forecast is the AVERAGE of three orthogonal methods:
    way[0] = sum(way[2:]) / len(way[2:])
    return way


if __name__ == "__main__":
    system.endmodule()
