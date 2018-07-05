#  Python Module for import                           Date : 2018-07-04
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


DEPENDENCIES
fecon236.prob.sim module

REFERENCES
Function np.random.choice() used in bootstrap():
http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-07-04  Add hybrid2ret() for synthesis with Gaussian mixture.
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


#  (For version on 2018-07-01, SPX stats from 1957-01-03 to 2018-06-29.)
#  Changes in specific numerical values are made in fecon236.prob.sim module:
SPXmean = sim.SPXmean        # Arithmetic (not Geometric mean rate)
SPXsigma = sim.SPXsigma      # volatility
SPXsigma1 = sim.SPXsigma1    # gaussmix
SPXsigma2 = sim.SPXsigma2    # gaussmix, its magnitude is not a typo.
SPXb = sim.SPXb              # sigma2 = sigma * b
SPXq = sim.SPXq              # probability of sigma2
SPXN = sim.SPXN              # Number of returns
SPXinprice = sim.SPXinprice  # initial price


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


def hybrid2ret(poparr, mean=SPXmean, sigma=SPXsigma, yearly=256):
    '''Concatenate synthetic GM(2) returns for DataFrame of hybrid prices.
       This is a SYNTHESIS between empirical and Gaussian mixture methods.
       Array poparr is assumed to be constructed from same mean and sigma.
       This function is OPTIONAL, strictly outside proper bootstrapping.
    '''
    poplen = poparr.shape[0]
    gmarr = sim.gmix2ret(poplen, mean, sigma, yearly)
    #  gmarr has same length as poparr to maximize the uncertainty
    #  in distinguishing between population sample and GM(2) origins.
    poparr2 = np.concatenate([poparr, gmarr])
    #  We have DOUBLED the population size.
    #      poparr2 can be used WHEREVER poparr is accepted.  <=!
    #      poparr2 is intended to be PRE-COMPUTED for further processing.
    return poparr2


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


def bootshow(N, poparr, yearly=256, repeat=1, visual=True, b=SPXb,
             inprice=100, replace=False):
    '''Statistical and optional visual SUMMARY: repeat bsret2prices().'''
    #  Also nice template for gathering SMALL-SAMPLE statistics...
    #  to be pursued elsewhere for different asset classes.
    for i in range(repeat):
        istr = str(i)
        prices = bsret2prices(N, poparr, inprice=inprice, replace=replace)
        if visual:
            plotn(prices, title='tmp-bootshow-'+istr)
        try:
            gm2gem(prices, yearly=yearly, b=b)
        except OverflowError:
            system.warn("Excessive kurtosis: Skipping gm2gem() print.")
        print('---------------------------------------' + istr)
    return


if __name__ == "__main__":
    system.endmodule()
