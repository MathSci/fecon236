#  Python Module for import                           Date : 2018-07-04
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  sim.py :: Simulation module for fecon236

- Essential probabilistic functions for simulations.
- Synthesis of prices from Gaussian mixture model GM(2), see gmix2prices().
- Visualize simulated price paths, see simushow() and gmixshow().
- Let N be an integer for sample size or length of a series.

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-07-04  Add gmix2ret() and SPX constants for default arguments.
                Add supplemental gmix2prices() and gmixshow().
2018-07-01  Add norat2ret() and ret2prices().
                Replace rates2prices by zerat2prices for clarity.
                Rename simshow() to simushow() and use new function.
2018-06-09  Add rates2prices() and summary simshow().
2018-06-08  Spin-off 2014 bootstrap material to boots/bootstrap.py.
2018-06-07  Rename to sim.py, fecon236 fork. Pass flake8, fix imports.
2017-06-29  yi_simulation.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from fecon236.util import system
from fecon236.tool import todf
from fecon236.dst.gaussmix import gm2gem
from fecon236.visual.plots import plotn


#  SPX stats from 1957-01-03 to 2018-06-29:
SPXmean = 0.065026     # Arithmetic vs. Geometric mean rate: 0.050103
SPXsigma = 0.154936    # volatility
SPXsigma1 = 0.060996   # gaussmix
SPXsigma2 = 0.542276   # gaussmix, its magnitude is not a typo.
SPXq = 0.0699          # probability of sigma2
SPXb = 3.5             # sigma2 = sigma * b
SPXN = 16042           # Number of returns
SPXinprice = 46.20     # initial price


def randou(upper=1.0):
    '''Single random float, not integer, from Uniform[0.0, upper).'''
    #  Closed lower bound of zero, and argument for open upper bound.
    #  To generate arrays, please use np.random.random().
    return np.random.uniform(low=0.0, high=upper, size=None)


def maybe(p=0.50):
    '''Uniformly random indicator function such that prob(I=1=True) = p.'''
    #  Nice to have for random "if" conditional branching.
    #  Fun note: Python's boolean True is actually mapped to int 1.
    if randou() <= p:
        return 1
    else:
        return 0


def randog(sigma=1.0):
    '''Single random float from Gaussian N(0.0, sigma^2).'''
    #  Argument sigma is the standard deviation, NOT the variance!
    #  For non-zero mean, just add it to randog later.
    #  To generate arrays, please use simug().
    return np.random.normal(loc=0.0, scale=sigma, size=None)


def simug(sigma=SPXsigma/16., N=256):
    '''Simulate array of shape (N,) from Gaussian Normal(0.0, sigma^2).
       Argument sigma is the standard deviation, NOT the variance!
       Note the use of raw sigma, which is not necessarily annualized.
    '''
    #  Default sigma is stylized per daily SPX data, see https://git.io/gmix
    ratarr = sigma * np.random.randn(N)
    #  For non-zero mean, simply add it later: mu + simug(sigma)
    return ratarr


def simug_mix(sigma1=SPXsigma1/16., sigma2=SPXsigma2/16., q=SPXq, N=256):
    '''Simulate array from zero-mean Gaussian mixture GM(2).
       Note the use of raw sigmas, which are not necessarily annualized.
    '''
    #  Default values are stylized per daily SPX data, see https://git.io/gmix
    #  Mathematical details in fecon235/nb/gauss-mix-kurtosis.ipynb
    #     Pre-populate an array of shape (N,) with the FIRST Gaussian,
    #     so that most work is done quickly and memory efficient...
    ratarr = simug(sigma1, N)
    #     ... except for some random replacements:
    for i in range(N):
        #                p = 1-q = probability drawing from FIRST Gaussian.
        #  So with probability q, replace an element of ratarr
        #  with a float from the SECOND Gaussian:
        if maybe(q):
            ratarr[i] = randog(sigma2)
    return ratarr


def norat2ret(normarr, mean, sigma, yearly=256):
    '''Reform array of N(0, 1) normalized RATES into array of RETURNS.
       Arguments mean and sigma should be in decimal form.
       Argument yearly expresses frequency to be obtained.
    '''
    meanly = mean / yearly   # e.g. 256 trading days in a year.
    sigmaly = sigma / (yearly ** 0.5)
    retarr = (1 + meanly) + (sigmaly * normarr)
    #  Thus e.g. an approximate 2% gain is converted to 1.02.
    #  Recall that log differences approximate percentage changes.
    return retarr


def ret2prices(retarr, inprice=1.0):
    '''Transform array of returns into DataFrame of prices.'''
    #  For cumulative product of array elements,
    #  numpy's cumprod is very fast, and records the ongoing results.
    #  http://docs.scipy.org/doc/numpy/reference/generated/numpy.cumprod.html
    prices = np.cumprod(retarr)  # prices here is in np.array form.
    #      Initial price implicitly starts at 1 where
    #      the history of prices is just the products of the returns.
    if inprice == 1.0:
        return todf(prices)
    else:
        return todf(inprice * prices)


def zerat2prices(ratarr, mean=0, yearly=256, inprice=1.0):
    '''Transform array of mean-0 rates into DataFrame of prices with mean.'''
    #  Default inprice means initial price implicitly starts at 1.
    meanly = mean / yearly   # e.g. 256 trading days in a year.
    retarr = (1 + meanly) + ratarr
    return ret2prices(retarr, inprice)


def simushow(N=256, mean=0, yearly=256, repeat=1, func=simug_mix, visual=True,
             b=SPXb, inprice=100):
    '''Statistical and optional visual SUMMARY: repeat simulations of func.
       Function func shall use all its default arguments, except for N.
    '''
    for i in range(repeat):
        istr = str(i)
        ratarr = func(N=N)
        prices = zerat2prices(ratarr, mean, yearly, inprice)
        if visual:
            plotn(prices, title='tmp-'+func.__name__+'-'+istr)
        try:
            gm2gem(prices, yearly=yearly, b=b)
        except OverflowError:
            system.warn("Excessive kurtosis: Skipping gm2gem() print.")
        print('---------------------------------------' + istr)
    return


def gmix2ret(N=256, mean=SPXmean, sigma=SPXsigma, yearly=256):
    '''Simulate array of GM(2) returns given arithmetic mean and plain sigma.
       GAUSSIAN MIXTURE is synthesized through primitive sim functions.
       Default values are stylized per daily SPX data, see https://git.io/gmix
    '''
    sigmaly = SPXsigma / (yearly ** 0.5)
    sigmaly1 = SPXsigma1 / (yearly ** 0.5)
    sigmaly2 = SPXsigma2 / (yearly ** 0.5)
    gmarr = simug_mix(sigmaly1, sigmaly2, q=SPXq, N=N)
    normarr = gmarr * (1. / sigmaly)  # Stylized array of normalized rates.
    #  normarr, though normalized, still retains leptokurtotic features.
    #  Plain volatility is used to RESCALE variations using fitted GM(2).
    retarr = norat2ret(normarr, mean, sigma, yearly)
    #  TIP: concatenate this array with corresponding array from bootstrap
    #       to create HYBRID synthetic/empirical returns.
    #       See fecon236.boots.bootstrap.hybrid2ret()
    return retarr


def gmix2prices(N=256, mean=SPXmean, sigma=SPXsigma, yearly=256, inprice=1.0):
    '''Simulate N prices from GM(2) given arithmetic mean and plain sigma.
       GAUSSIAN MIXTURE is synthesized through primitive sim functions.
    '''
    retarr = gmix2ret(N, mean, sigma, yearly)
    return ret2prices(retarr, inprice)


def gmixshow(N=256, mean=SPXmean, sigma=SPXsigma, yearly=256, repeat=1,
             visual=True, inprice=100, b=SPXb):
    '''Statistical and optional visual SUMMARY: repeat simulations of GM(2).'''
    for i in range(repeat):
        istr = str(i)
        prices = gmix2prices(N, mean, sigma, yearly, inprice)
        if visual:
            plotn(prices, title='tmp-gmixshow-'+istr)
        try:
            gm2gem(prices, yearly=yearly, b=b)
        except OverflowError:
            system.warn("Excessive kurtosis: Skipping gm2gem() print.")
        print('---------------------------------------' + istr)
    return


if __name__ == "__main__":
    system.endmodule()
