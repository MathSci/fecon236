#  Python Module for import                           Date : 2018-05-10
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  holtwinters.py :: Holt-Winters time-series functions.

Holt-Winters is two-parameter linear growth exponential smoothing model.

TESTS for this module are carried out in tests/test_holtwinters.py
and the doctests there show numerical examples of how some of our
time-series algorithms are built.

OPTIMIZATION occur in a separate module to avoid clutter here.
To optimize Holt-Winters parameters alpha and beta,
conditional on a particular dataset, for forecasting purposes
(rather than smoothing), please see our module opt_holt.py

USAGE of the code for the Holt-Winters time-series model is illustrated
in the Jupyter notebook at https://git.io/gdpspx which is a rendering of
nb/fred-gdp-spx.ipynb in the fecon235 repository.

Note: rolling_* methods, including rolling_apply, only work on one-dimensional
array, thus we may work outside pandas in numpy, then bring back the results.
See pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html
and compare holt_winters_growth() vs. holt().


REFERENCES:

  - Spyros Makridakis, 1978, _FORECASTING_, pp. 64-66.
       H-W does extremely well against ARIMA models in competitions.
  - Rob Hyndman, 2008, _Forecasting with Exponential Smoothing_,
       discusses level, growth (linear), and seasonal variants.
  - Sarah Gelper, 2007, _Robust Forecasting with Exponential
       and Holt-Winters smoothing_, useful for parameter values.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-05-10  holtwinters.py, fecon236 fork. Pass flake8.
2016-12-20  yi_timeseries.py, fecon235 v5.18.0312, https://git.io/fecon235
2016-12-14  Fix initial guess of b[0] for holt_winters_growth(),
                especially critical when beta=0 e.g. in new ema().
'''

from __future__ import absolute_import, print_function

#  import matplotlib.pyplot as plt   # Unused as of 2018-05-10.
#  import pandas as pd               # Unused as of 2018-05-10.

import numpy as np
from . import yi_0sys as system
from .yi_1tools import todf


#  Holt-Winters DEFAULT parameters:
hw_alpha = 0.26      # Based on robust optimization in Gelper 2007,
hw_beta = 0.19       # for Gaussian, fat tail, and outlier data.


def holt_winters_growth(y, alpha=hw_alpha, beta=hw_beta):
    '''Helper for Holt-Winters growth (linear) model using numpy arrays.'''
    #  N.B. -  SEASONAL variant of Holt-Winters is omitted.
    N = y.size             # y should be a numpy array.
    #                        0 < alpha and beta < 1
    alphac = 1 - alpha     # Complements of alpha and beta
    betac = 1 - beta       # pre-computed before the loop.
    #   Create ndarrays filled with zeros to be updated
    #   as the y data comes in:
    l = np.zeros((N,))     # noqa \ Fill level array with zeros.
    l[0] = y[0]            # Initialize level.
    b = np.zeros((N,))     # Smoothed one-step growths.
    #  b[0] = y[1] - y[0]  # Propagates errors if beta=0; fixed 2016-12-14:
    b[0] = 0               # Algorithmically the correct guess if beta=0.
    for i in range(1, N):
        l[i] = (alpha * y[i]) + (alphac * (l[i-1] + b[i-1]))
        ldelta = l[i] - l[i-1]
        #      ^change in smoothed data = proxy for implicit growth.
        b[i] = (beta * ldelta) + (betac * b[i-1])
        #              ^not ydelta !!
    #       l, b are arrays.
    return [l, b]


def holt(data, alpha=hw_alpha, beta=hw_beta):
    '''Holt-Winters growth (linear) model outputs workout dataframe.'''
    #  holt is an EXPENSIVE function, so retain its output for later.
    holtdf = todf(data).dropna()
    #              'Y'    ^else:
    #     "ValueError: Length of values does not match length of index"
    y = holtdf.values      # Convert to array.
    l, b = holt_winters_growth(y, alpha, beta)
    holtdf['Level'] = l
    holtdf['Growth'] = b
    #    In effect, additional columns 'Level' and 'Growth'
    # for smoothed data and local slope,
    #    along side the original index and given data:
    return holtdf


def holtlevel(data, alpha=hw_alpha, beta=hw_beta):
    '''Just smoothed Level dataframe from Holt-Winters growth model.'''
    #  Useful to filter out seasonals, e.g. see X-11 method:
    #     http://www.sa-elearning.eu/basic-algorithm-x-11
    return todf(holt(data, alpha, beta)['Level'])


def holtgrow(data, alpha=hw_alpha, beta=hw_beta):
    '''Just the Growth dataframe from Holt-Winters growth model.'''
    #  In terms of units expressed in data.
    return todf(holt(data, alpha, beta)['Growth'])


def holtpc(data, yearly=256, alpha=hw_alpha, beta=hw_beta):
    '''Annualized percentage growth dataframe from H-W growth model.'''
    #  yearly is the multiplier to annualize Growth.
    #
    #       MOST VALUABLE H-W function              <= !!
    #       It contains the HISTORY of FORECASTED RATES!
    #
    holtdf = holt(data, alpha, beta)
    level = todf(holtdf['Level'])
    grow = todf(holtdf['Growth'])
    growan = todf(grow * yearly)
    return todf(100 * (growan / level))


def holtforecast(holtdf, h=12):
    '''Given a dataframe from holt, forecast ahead h periods.'''
    #  N.B. -  holt forecasts by multiplying latest growth
    #          by the number of periods ahead. Somewhat naive...
    #          notice that the growth is based on smoothed levels.
    last = holtdf[-1:]
    y, l, b = last.values.tolist()[0]
    #         df to array to list, but extract first element:-(
    forecasts = [y] + [l + (b*(i+1)) for i in range(h)]
    #            ^last actual point
    return todf(forecasts, 'Forecast')


def plotholt(holtdf, h=12):
    '''Given a dataframe from holt, plot forecasts h periods ahead.'''
    #  plotdf will not work since index there is assumed to be dates.
    holtforecast(holtdf, h).plot(title='Holt-Winters linear forecast')
    return


def ema(y, alpha=0.20):
    '''EXPONENTIAL MOVING AVERAGE using traditional weight arg.'''
    #  y could be a dataframe.
    #  ema is mathematically equivalent to holtlevel with beta=0,
    #  thus issue #5 can be easily resolved for all pandas versions.
    return holtlevel(y, alpha, beta=0)


if __name__ == "__main__":
    system.endmodule()


# ======================================================= ENDNOTES ============

#  #  Table 3-8 from Makridakis 1978:
#  makridakis_p65 = np.array([143, 152, 161, 139, 137, 174, 142, 141, 162,
#                            180, 164, 171, 206, 193, 207, 218, 229, 225, 204,
#                            227, 223, 242, 239, 266])
