#  Python Module for import                           Date : 2018-06-16
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  holtwinters.py :: Holt-Winters time-series functions.

Holt-Winters is two-parameter linear growth exponential smoothing model.
It has many uses, for example, stabilizing a time-series.
For forecasting, the results are distilled in the forecast() function
which features robust parameter optimization in the background.

TESTS for this module are carried out in tests/test_holtwinters.py
and the doctests there show numerical examples of how some of our
time-series algorithms are built.

To optimally ESTIMATE Holt-Winters parameters alpha and beta,
conditional on a particular dataset, for forecasting purposes
(rather than smoothing), opt_holt.py was absorbed here on 2018-05-31.

USAGE of the code for the Holt-Winters time-series model is illustrated
in the Jupyter notebook at https://git.io/gdpspx which is a rendering of
nb/fred-gdp-spx.ipynb in the fecon235 repository.

Note: rolling_* methods, including rolling_apply, only work on one-dimensional
array, thus we may work outside pandas in numpy, then bring back the results.
See pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html
and compare holt_winters_growth() vs. holt().

Details in comments: 2*sigma can be approximated by 3*(median_absolute_error).


REFERENCES:

  - Spyros Makridakis, 1978, _FORECASTING_, pp. 64-66.
       H-W does extremely well against ARIMA models in competitions.
  - Rob Hyndman, 2008, _Forecasting with Exponential Smoothing_,
       discusses level, growth (linear), and seasonal variants.
  - Sarah Gelper, 2007, _Robust Forecasting with Exponential
       and Holt-Winters smoothing_, useful for parameter values.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-16  Absort Holt-Winters functions from top.py, esp. forecast().
2018-05-31  ABSORB opt_holt module to estimate optimal alpha and beta.
2018-05-11  Fix imports.
2018-05-10  holtwinters.py, fecon236 fork. Pass flake8.
2016-12-20  yi_timeseries.py, fecon235 v5.18.0312, https://git.io/fecon235
2016-12-14  Fix initial guess of b[0] for holt_winters_growth(),
                especially critical when beta=0 e.g. in new ema().
'''

from __future__ import absolute_import, print_function, division

import numpy as np
import pandas as pd
from fecon236.util import system
from fecon236.tool import todf, tailvalue
from fecon236.host.hostess import get

#  To estimate optimal alpha and beta, see === section:
from fecon236.oc import optimize as op
#  Assuming that DISPLAY=0 at optimize module.

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


def foreholt(data, h=12, alpha=hw_alpha, beta=hw_beta, maxi=0):
    '''Data slang aware Holt-Winters holtforecast(), h-periods ahead.
       Thus "data" can be a fredcode, quandlcode, stock slang,
       OR a DataFrame should be detected.
    '''
    if not isinstance(data, pd.DataFrame):
        try:
            data = get(data, maxi)
        except Exception:
            raise ValueError("INVALID data argument.")
    holtdf = holt(data, alpha, beta)
    return holtforecast(holtdf, h)


def holtfred(data, h=24, alpha=hw_alpha, beta=hw_beta):
    '''Holt-Winters forecast h-periods ahead (fredcode aware).'''
    #  Retained for backward compatibility, esp. pre-2016 notebooks.
    return foreholt(data, h, alpha, beta)


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


# ============================= ROBUST OPTIMAL ESTIMATION of alpha and beta ===
'''
We shall rely on optimize.minBrute() to find optimal alpha and beta:

- minBrute() from optimize module: non-convex problem: GLOBAL optimizers:
    If your problem does NOT admit a unique local minimum (which can be hard
    to test unless the function is convex), and you do not have prior
    information to initialize the optimization close to the solution: Brute
    force uses a grid search: scipy.optimize.brute() evaluates the function on
    a given grid of parameters and returns the parameters corresponding to the
    minimum value.

    See oc/optimize.py for implementation details and references.
    Also tests/test_optimize.py is intended as a TUTORIAL for USAGE.

- GOAL: given some data and a MODEL, we want to MINIMIZE the LOSS FUNCTION
    over possible values of the model's PARAMETERS.
    Parameters which satisfy that goal are called BEST estimates
    for the specified functional form.

    Loss function should DISTINGUISH between parameters to be optimized,
    and other supplemental arguments. The latter is introduced
    via a tuple called funarg, frequently used to inject data.

- We forego using RMSE (root mean squared errors) in favor of a more
    ROBUST loss function since the squaring magnifies large errors.

STATISTICAL NOTE: if L is the median absolute error, then by definition,
                  prob(-L <= error <= L) = 0.5
    If we assume the errors are Gaussian centered around zero,
    then L = 0.675*sigma (by table look-up), thus sigma = 1.48*L.

    RULE of thumb: Two sigma confidence can be approximated by 3*L.
'''


def loss_holt(params, *args):
    '''Loss function for holt() using np.median of absolute errors.
       This is much more robust than using np.sum or np.mean
       (and perhaps better than editing "outliers" out of data).
       The error array will consist of 1-step ahead prediction errors.
    '''
    alpha, beta = params  # Must specify arguments.
    data = args[0]        # Primary data assumed to be single column.
    #
    #  Information from the Holt-Winters filter is distilled
    #  to the holt() multi-column workout dataframe;
    #  see tests/test_optimize.py for numerical examples.
    holtdf = holt(data, alpha, beta)
    #  Henceforth use numpy arrays, rather than dataframes:
    y = holtdf['Y'].values       # Actual data, without index
    l = holtdf['Level'].values   # noqa
    b = holtdf['Growth'].values
    #
    error = y[1:] - (l[:-1] + b[:-1])
    #  #  Equivalent, but more expensive, version of previous line...
    #  #  Compute error array, taking one lag into account:
    #  N = y.size
    #  error = np.zeros((N-1,))   #  Fill level array with zeros.
    #  for i in range(N-1):
    #     error[i] = y[i+1] - (l[i] + b[i])
    #     #          ^Actual  ^Prediction MODEL
    #
    #  Ignore the first ten errors due to initialization warm-up:
    return np.median(np.absolute(error[10:]))


#  NOTICE: TUPLE "funarg" is used to specify arguments to function "fun"
#          which are NOT the parameters to be optimized (e.g. data).
#          Gotcha: Remember a single-element tuple must include
#          that mandatory comma: (alone,)


def optimize_holt(dataframe, grids=50, alphas=(0.0, 1.0), betas=(0.0, 1.0)):
    '''Optimize Holt-Winters parameters alpha and beta for given data.
       The alphas and betas are boundaries of respective explored regions.
       Function interpolates "grids" from its low bound to its high bound,
       inclusive. Final output: [alpha, beta, losspc, median absolute loss]
       TIP: narrow down alphas and betas using optimize_holt iteratively.
    '''
    if grids > 49:
        system.warn("Optimizing Holt-Winters alphabetaloss may take TIME!")
        #  Exploring loss at all the grids is COMPUTATIONALLY INTENSE
        #  due to holt(), especially if the primary data is very large.
        #  Tip: truncate dataframe to recent data.
    result = op.minBrute(fun=loss_holt, funarg=(dataframe,),
                         boundpairs=[alphas, betas], grids=grids)
    #  result is a numpy array, so convert to list:
    alpha, beta = list(result)
    #  Compute loss, given optimal parameters:
    loss = loss_holt((alpha, beta), dataframe)
    #  Compute percentage loss relative to absolute tailvalue:
    losspc = (float(loss) / abs(tailvalue(dataframe))) * 100
    #  Since np.round and np.around print ugly, use Python round() to
    #  display alpha and beta. Also include losspc and median absolute loss:
    return [round(alpha, 4), round(beta, 4), round(losspc, 4), loss]


def optimize_holtforecast(dataframe, h=12, grids=50):
    '''Forecast ahead h periods using optimized Holt-Winters parameters.'''
    #  Note: default hw_alpha and hw_beta from yi_timeseries module
    #        are NOT necessarily optimal given specific data.
    alphabetaloss = optimize_holt(dataframe, grids=grids)
    #  alphabetaloss will be a list: [alpha, beta, losspc, loss]
    #     computed from default boundpairs: alphas=(0.0, 1.0), betas=(0.0, 1.0)
    holtdf = holt(dataframe, alpha=alphabetaloss[0], beta=alphabetaloss[1])
    #  holdf is our Holt-Winters "workout" dataframe.
    forecasts_df = holtforecast(holtdf, h)
    #  forecasts_df is a dataframe containing h period forecasts.
    #
    #  Unlike holtforecast(), here we append alphabetaloss to the output
    #     so that the model parameters and median absolute loss are available.
    #     Forecasts alone can be obtained directly by func(...)[0]
    return [forecasts_df, alphabetaloss]


def forecast(data, h=12, grids=0, maxi=0):
    '''h-period ahead forecasts by holtforecast or optimize_holtforecast,
       where "data" may be fredcode, quandlcode, stock slang, or DataFrame.
       Given default grids argument, forecast is very QUICK since we use
       FIXED parameters implicitly: alpha=hw_alpha and beta=hw_beta.
       Recommend grids=50 for reasonable results, but it is TIME-CONSUMING
       for search grids > 49 to find OPTIMAL alpha and beta.
    '''
    if not isinstance(data, pd.DataFrame):
        try:
            data = get(data, maxi)
            #          ^Expecting fredcode, quandlcode, or stock slang.
        except Exception:
            raise ValueError("INVALID data argument.")
    if grids > 0:
        opt = optimize_holtforecast(data, h, grids=grids)
        system.warn(str(opt[1]), stub="OPTIMAL alpha, beta, losspc, loss:")
        return opt[0]
    else:
        holtdf = holt(data)
        system.warn("Holt-Winters parameters have NOT been optimized.")
        return holtforecast(holtdf, h)


if __name__ == "__main__":
    system.endmodule()


# ======================================================= ENDNOTES ============

#  #  Table 3-8 from Makridakis 1978:
#  makridakis_p65 = np.array([143, 152, 161, 139, 137, 174, 142, 141, 162,
#                            180, 164, 171, 206, 193, 207, 218, 229, 225, 204,
#                            227, 223, 242, 239, 266])
