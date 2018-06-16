#  Python Module for import                           Date : 2018-06-14
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  top.py :: Unity among fecon236 modules

- Frequently used idioms can be generalized with shorter names.

USAGE
- More explicit syntax recommended: "import fecon236 as fe"
  (Former usage in notebooks was casual: "from fecon235.fecon235 import *").

REFERENCE
- Bloomberg Open Symbology which assigns a global ID for obscure financial
  instruments is now accessible via OpenFIGI, https://www.openfigi.com/search

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-14  Spin-off group stuff to util/group.py.
                Spin-off get() to host/hostess.py.
2018-06-13  Rename to top.py, fecon236 fork. Lint bugs:
                too many undefined names (module specs) and bare excepts.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import pandas as pd
from fecon236.util import system


def get(code, maxi=0):
    '''Unifies getfred, getqdl, and getstock for data retrieval.
    code is fredcode, quandlcode, futures slang, or stock slang.
    maxi should be an integer to set maximum number of data points,
         where 0 implies the default value.

    get() will accept the vendor code directly as string, e.g.
    from FRED and Quandl, or use one of our abbreviated variables
    documented in the appropriate module listed above.
    The notebooks provide good code examples in action.

    Futures slang is of the form 'f4spotyym' where
                  spot is the spot symbol in lower case,
                  yy   is the last two digits of the year
                  m    is the delivery month code,
            so for December 2015 COMEX Gold: 'f4xau15z'

    Stock slang can be also used for ETFs and mutual funds.
    The general form is 's4symbol' where the symbol must be in
    lower case, so for SPY, use 's4spy' as an argument.
    '''
    try:
        df = getfred(code)
    except:
        try:
            if maxi:
                df = getqdl(code, maxi)
            else:
                df = getqdl(code)
        except:
            try:
                if maxi:
                    df = getstock(code, maxi)
                else:
                    df = getstock(code)
            except:
                raise ValueError('INVALID string or code for fecon get()')
    return df


def forecast(data, h=12, grids=0, maxi=0):
    '''Make h period ahead forecasts using holt* or optimize_holtforecast,
       where "data" may be a DataFrame, fredcode, quandlcode, or stock slang.
       (Supercedes: "Unifies holtfred and holtqdl for quick forecasting.")
    '''
    #  Generalization of 2016-12-29 preserves and expands former interface.
    if not isinstance(data, pd.DataFrame):
        try:
            data = get(data, maxi)
            #           ^expecting fredcode, quandlcode, or stock slang
            #      to be retrieved as DataFrame.
        except:
            raise ValueError("fecon235.forecast(): INVALID data argument.")
    if grids > 0:
        #  Recommend grids=50 for reasonable results,
        #  but TIME-CONSUMING for search grids > 49
        #  to FIND OPTIMAL alpha and beta by minBrute():
        opt = optimize_holtforecast(data, h, grids=grids)
        #  See optimize_holtforecast() in module ys_opt_holt for details.
        system.warn(str(opt[1]), stub="OPTIMAL alpha, beta, losspc, loss:")
        return opt[0]
    else:
        #  QUICK forecasts when grids=0 ...
        #  by using FIXED defaults: alpha=ts.hw_alpha and beta=ts.hw_beta:
        holtdf = holt(data)
        system.warn("Holt-Winters parameters have NOT been optimized.")
        return holtforecast(holtdf, h)


def foreholt(data, h=12, alpha=hw_alpha, beta=hw_beta, maxi=0):
    '''Holt-Winters forecast h-periods ahead (data slang aware).'''
    #  "data" can be a fredcode, quandlcode, stock slang,
    #         OR a DataFrame which will be detected:
    if not isinstance(data, pd.DataFrame):
        try:
            data = get(data, maxi)
        except:
            raise ValueError("fecon235.forehalt(): INVALID data argument.")
    #  To find optimal parameter values for alpha and beta beforehand,
    #  use optimize_holtforecast() in module ys_opt_holt.
    holtdf = holt(data, alpha, beta)
    #   Interim results will not be retained.
    return holtforecast(holtdf, h)


def holtfred(data, h=24, alpha=hw_alpha, beta=hw_beta):
    '''Holt-Winters forecast h-periods ahead (fredcode aware).'''
    #  Retained for backward compatibility, esp. pre-2016 notebooks.
    return foreholt(data, h, alpha, beta)


def forefunds(nearby='16m', distant='17m'):
    '''Forecast distant Fed Funds rate using Eurodollar futures.'''
    #  Long derivation is given in qdl-libor-fed-funds.ipynb
    ffer = getfred('DFF')
    #      ^Retrieve Fed Funds effective rate, daily since 1954.
    ffer_ema = ema(ffer['1981':], 0.0645)
    #                    ^Eurodollar futures debut.
    #          ^Exponentially Weighted Moving Average, 30-period.
    libor_nearby = get('f4libor' + nearby)
    libor_distant = get('f4libor' + distant)
    libor_spread = todf(libor_nearby - libor_distant)
    #     spread in forward style quote since futures uses 100-rate.
    return todf(ffer_ema + libor_spread)


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
