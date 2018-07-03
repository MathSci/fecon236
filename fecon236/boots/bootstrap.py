#  Python Module for import                           Date : 2018-07-01
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  bootstrap.py :: Bootstrap module for fecon236

- Design bootstrap to study alternate histories and small-sample statistics.
- Normalize, but include fat tails, in empirical distributions.
- Visualize sample price paths.

USAGE: Two methods to efficiently pre-compute asset returns:
    - writefile_normdiflog(): Create a CSV file of normalized rates of return.
    - Use CSV file in csv2ret() to create "population" array of returns.
- Bootstrap (resample) from poparr to simulate price history by bsret2prices().


The broad theoretical justification in using bootstrapping for asset prices
is that the best in-sample fit of an ARIMA model to log(price) is AR(1)
with unit root. Thus the stochastic process is memory-less. In addition,
studies of post-sample performances show it is extremely difficult to
surpass the current price as the forecast of prices over long horizons.


REFERENCES
Function np.random.choice() used in bootstrap():
http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-07-01  Apply the functions extracted to sim module.
2018-06-28  TOTAL REWRITE: generalization and clarification of logic flow.
                Deprecate fecon235/nb/SIMU-mn0-sd1pc-d4spx_1957-2014.csv.gz
                Include recipe for creating similar CSV files.
2018-06-08  Spin-off 2014 material from sim.py, but needs generalization.
                Let N generally be the count:= sample size.
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from fecon236 import tool
from fecon236.util import system
from fecon236.prob import sim
from fecon236.host.fred import readfile
from fecon236.visual.plots import plotn
from fecon236.dst.gaussmix import gm2gem


#  SPX stats from 1957-01-03 to 2018-06-29:
SPXmean = 0.065026     # Arithmetic vs. Geometric mean rate: 0.050103
SPXsigma = 0.154936    # volatility
SPXsigma1 = 0.060996   # gaussmix
SPXsigma2 = 0.542276   # gaussmix, its magnitude is not a typo.
SPXq = 0.0699          # probability of sigma2
SPXN = 16042           # Number of returns
SPXinprice = 46.20     # initial price


def writefile_normdiflog(df, filename='tmp-fe-normdiflog.csv', lags=1):
    '''Dataframe variations into CSV file: logrithmic differences as N(0,1).
       PRE-COMPUTING increases speed and eliminates network download time.
       Recommend gz compression of the produced CSV file.
    '''
    dfndl = tool.normalize(tool.diflog(df, lags=lags))
    tool.writefile(dfndl, filename)
    return


def readcsv(datafile='tmp-fe-normdiflog.csv'):
    '''Read CSV file.'''
    try:
        if datafile.endswith('.gz'):
            df = readfile(datafile, compress='gzip')
        else:
            df = readfile(datafile)
        return df
    except Exception:
        raise ValueError("Improper or non-existent datafile specified.")


def csv2ret(datafile, mean=SPXmean, sigma=SPXsigma, yearly=256):
    '''Reform empirical N(0, 1) rates distribution as returns array.'''
    df = readcsv(datafile)    # Dataframe of normalized RATES of return.
    normarr = df['Y'].values  # That dataframe expressed as array.
    #                .values converts to numpy ARRAY form.
    #      The pandas index will no longer matter.
    #      Next, form an array to efficiently bootstrap later.
    poparr = sim.norat2ret(normarr, mean, sigma, yearly)
    #  TIP: For repetitive simulations, poparr should be PRE-COMPUTED.
    #     "POPULATION" array in RETURNS form (no longer rates):
    return poparr


def bootstrap(N, poparr, replace=False):
    '''Randomly pick out N items from poparr.
       Default argument, replace=False, means "WITHOUT replacement."
    '''
    bsarr = np.random.choice(poparr, size=N, replace=replace)
    #      BOOTSTRAPPED array
    return bsarr


def bsret2prices(N, poparr, inprice=1.0, replace=False):
    '''Transform array of bootstrap returns into DataFrame of prices.'''
    bsarr = bootstrap(N, poparr, replace=replace)
    bsprices = sim.ret2prices(bsarr, inprice=inprice)
    return bsprices


def bootshow(N, poparr, yearly=256, repeat=1, visual=True, b=3.5,
             inprice=100, replace=False):
    '''Statistical and optional visual SUMMARY: repeat bsret2prices().'''
    #  Also nice template for gathering SMALL-SAMPLE statistics...
    #  to be pursued elsewhere for different asset classes.
    for i in range(repeat):
        istr = str(i)
        prices = bsret2prices(N, poparr, inprice=inprice, replace=replace)
        if visual:
            plotn(prices, title='tmp-bootshow-'+istr)
        gm2gem(prices, yearly=yearly, b=b)
        print('---------------------------------------' + istr)
    return


if __name__ == "__main__":
    system.endmodule()
