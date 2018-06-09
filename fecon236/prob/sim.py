#  Python Module for import                           Date : 2018-06-09
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  sim.py :: Simulation module for fecon236

- Essential probabilistic functions for simulations.
- Handles Gaussian mixture model GM(2).
- Visualize simulated price paths, see simshow().
- Let N be an integer for sample size or length of a series.

CHANGE LOG  For LATEST version, see https://git.io/fecon236
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


def simug(sigma=0.13/16., N=256):
    '''Simulate array of shape (N,) from Gaussian Normal(0.0, sigma^2).'''
    #  Argument sigma is the standard deviation, NOT the variance!
    #  Default sigma is stylized per daily SPX data, see https://git.io/gmix
    ratarr = sigma * np.random.randn(N)
    #  For non-zero mean, simply add it later: mu + simug(sigma)
    return ratarr


def simug_mix(sigma1=0.0969/16., sigma2=0.26/16., q=0.129, N=256):
    '''Simulate array from zero-mean Gaussian mixture GM(2).'''
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


def rates2prices(ratarr, mean=0/256., initialpx=0):
    '''Convert array containing rates of return to DataFrame of prices.'''
    #  Initial price, initialpx, if not set, implicitly starts at 1.
    #  REMEMBER to adjust annualized mean to match data frequency.
    ret = (1 + mean) + ratarr
    #  Price history is just the products of the returns ret.
    #      Cumulative product, cumprod(), of array elements is very fast.
    #  http://docs.scipy.org/doc/numpy/reference/generated/numpy.cumprod.html
    productret = np.cumprod(ret)
    if initialpx:
        prices = initialpx * productret
    else:
        prices = productret
    return todf(prices)


def simshow(repeat=3, mean=0/256., N=256, func=simug_mix, visual=True):
    '''Statistical and optional visual SUMMARY: repeat simulations of func.'''
    #  Function func should rely on all its default args, except for N.
    for i in range(repeat):
        istr = str(i)
        ratarr = func(N=N)
        prices = rates2prices(ratarr, mean, initialpx=100)
        if visual:
            plotn(prices, title='tmp-'+istr)
        gm2gem(prices, b=2)
        print('---------------------------------------' + istr)
    return


if __name__ == "__main__":
    system.endmodule()
