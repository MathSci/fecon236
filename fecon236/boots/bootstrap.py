#  Python Module for import                           Date : 2018-06-28
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  bootstrap.py :: Bootstrap module for fecon236

- Design bootstrap to study alternate histories and small-sample statistics.
- Normalize, but include fat tails, in empirical distributions.
- Visualize sample price paths.

USAGE: Two methods to efficiently pre-compute asset returns:
    - writefile_normdiflog(): Create a CSV file of normalized rates of return.
    - Use CSV file in reshape_dst() to create "population" array of returns.
- Bootstrap (resample) from poparr to simulate price history by simu_prices().


The broad theoretical justification in using bootstrapping for asset prices
is that the best in-sample fit of an ARIMA model to log(price) is AR(1)
with unit root. Thus the stochastic process is memory-less. In addition,
studies of post-sample performances show it is extremely difficult to
surpass the current price as the forecast of prices over long horizons.


REFERENCES
Function np.random.choice() used in bootstrap():
http://docs.scipy.org/doc/numpy/reference/generated/numpy.random.choice.html

CHANGE LOG  For LATEST version, see https://git.io/fecon236
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
from fecon236.host.fred import readfile
from fecon236.visual.plots import plotn
from fecon236.dst.gaussmix import gemrat


#  SPX mean and volatility in DECIMAL form from 1957-01-03 to 2014-12-11.
SPXmean = 0.076306
SPXsigma = 0.155742
SPXn = 15116
SPXinprice = 46.20


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


def reshape_dst(datafile, mean=SPXmean, sigma=SPXsigma, yearly=256):
    '''Reshape empirical N(0, 1) rates distribution as returns array.'''
    df = readcsv(datafile)   # Get dataframe containing rates of return.
    meanly = mean / yearly   # e.g. 256 trading days in a year.
    sigmaly = sigma / (yearly ** 0.5)
    returns = tool.todf((1 + meanly) + (df * sigmaly))
    #  Thus e.g. an approximate 2% gain is converted to 1.02.
    #  Recall that log differences approximate percentage changes.
    #      Next, form an array to efficiently bootstrap later.
    #      The date index will no longer matter.
    #                    .values converts to numpy ARRAY form.
    poparr = returns['Y'].values
    #  TIP: For repetitive simulations, poparr should be PRE-COMPUTED.
    #     "POPULATION" array
    return poparr


def bootstrap(N, poparr, replace=False):
    '''Randomly pick out N items from poparr.
       Default argument, replace=False, means "WITHOUT replacement."
    '''
    bsarr = np.random.choice(poparr, size=N, replace=replace)
    #      BOOTSTRAPPED array
    return bsarr


def simu_prices(N, poparr, inprice=1.0, replace=False):
    '''Convert bootstrap returns into pandas DataFrame of prices.'''
    bsarr = bootstrap(N, poparr, replace=replace)
    #  For cumulative product of array elements,
    #  numpy's cumprod is very fast, and records the ongoing results.
    #  http://docs.scipy.org/doc/numpy/reference/generated/numpy.cumprod.html
    prices = np.cumprod(bsarr)  # prices will be a np.array
    #      Initial price implicitly starts at 1 where
    #      the history of prices is just the products of the returns.
    #      Initial price for SPX on 1957-01-02 was 46.20.
    if inprice == 1.0:
        return tool.todf(prices)
    else:
        return tool.todf(inprice * prices)


def simu_plots(N, poparr, charts=1, inprice=1.0, replace=False):
    '''Display simulated price charts of N periods.'''
    #  Also nice template for gathering SMALL-SAMPLE statistics...
    #  to be pursued elsewhere for different asset classes.
    for i in range(charts):
        px = simu_prices(N, poparr, inprice=inprice, replace=replace)
        plotn(px)
        print('     gemrat: ' + str(gemrat(px)))
        print('   ____________________________________')
        print('')
    return


if __name__ == "__main__":
    system.endmodule()
