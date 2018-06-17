#  Python Module for import                           Date : 2018-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  group.py :: Group utilities

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-17  Spin-off groupcotr() to futures.cftc module.
2018-06-16  Move covdiflog() to math.matrix module.
2018-06-14  Spin-off group stuff from top.py.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236 import tool
from fecon236.util import system
from fecon236.host import fred
from fecon236.host.hostess import get
from fecon236.dst.gaussmix import gemrat
from fecon236.tsa import holtwinters as hw


#  GROUPS:  specify our favorite series as a dictionary
#  where key is name, and corresponding value is its data code:

group4d = {'Zero10': fred.d4zero10, 'SPX': fred.d4spx, 'XAU': fred.d4xau,
           'EURUSD': fred.d4eurusd, 'USDJPY': fred.d4usdjpy}
#         For usage, see https://git.io/georet for details,
#         in particular, functions like group*() in this module.

world4d = {'America': 's4spy', 'Europe': 's4ezu',
           'Japan': 's4ewj',  'Emerging': 's4eem', 'Gold': 's4gld'}
#         For usage, see https://git.io/boltz1 and https://git.io/boltz2
#         for details, Exchange Traded Funds (ETF) of daily frequency
#         representing EQUITIES worldwide plus gold.


def groupget(ggdic=group4d, maxi=0):
    '''Retrieve and create group dataframe, given group dictionary.'''
    #  Since dictionaries are unordered, create SORTED list of keys:
    keys = [key for key in sorted(ggdic)]
    #  Download individual dataframes as values into a dictionary:
    dfdic = {key: get(ggdic[key], maxi) for key in keys}
    #           ^Illustrates dictionary comprehension.
    #  Paste together dataframes into one large sorted dataframe:
    groupdf = tool.paste([dfdic[key] for key in keys])
    #  Name the columns:
    groupdf.columns = keys
    return groupdf


def groupfun(fun, groupdf, *pargs, **kwargs):
    '''Use fun(ction) column-wise, then output new group dataframe.'''
    #  In mathematics, this is known as an "operator":
    #      a function which takes another function as argument.
    #  Examples of fun: pcent, normalize, etc. See grouppc() next.
    #  See groupget() to retrieve and create group dataframe.
    keys = list(groupdf.columns)
    #  Compute individual columns as dataframes in a list:
    out = [tool.todf(fun(tool.todf(groupdf[key]), *pargs, **kwargs))
           for key in keys]
    #   ^Python 2 and 3 compatible: apply() removed in Python 3.
    #  Paste together dataframes into one large dataframe:
    outdf = tool.paste(out)
    #  Name the columns:
    outdf.columns = keys
    return outdf


def grouppc(groupdf, freq=1):
    '''Create overlapping pcent dataframe, given a group dataframe.'''
    #  See groupget() to retrieve and create group dataframe.
    #  Very useful to visualize as boxplot, see fred-georeturns.ipynb
    return groupfun(tool.pcent, groupdf, freq)


def groupdiflog(groupdf, lags=1):
    '''Difference between lagged log(data) for columns in group dataframe.'''
    #  See groupget() to retrieve and create group dataframe.
    return groupfun(tool.diflog, groupdf, lags)


def groupgeoret(groupdf, yearly=256, order=True):
    '''Geometric mean returns, non-overlapping, for group dataframe.
       Argument "yearly" refers to annual frequency, e.g.
       256 for daily trading days, 12 for monthly, 4 for quarterly.
       ATTN: Use groupgemrat() instead for greater accuracy.
    '''
    keys = list(groupdf.columns)
    #  Use list comprehension to store lists from georet():
    geo = [tool.georet(tool.todf(groupdf[k]), yearly) + [k] for k in keys]
    #  where each georet list gets appended with an identifying key.
    if order:
        geo.sort(reverse=True)
        #  Group is ordered in-place with respect to decreasing georet.
    return geo


def groupgemrat(groupdf, yearly=256, order=False, n=2):
    '''Geometric mean rates, non-overlapping, for group dataframe.
       Argument "yearly" refers to annual frequency, e.g.
       256 for daily trading days, 12 for monthly, 4 for quarterly.
       Output is rounded to n-decimal places.
       Algorithm takes KURTOSIS into account for greater accuracy.
    '''
    keys = list(groupdf.columns)
    #  Use list comprehension to store lists from gemrat():
    gem = [tool.roundit(gemrat(tool.todf(groupdf[k]), yearly), n, echo=False)
           + [k] for k in keys]
    #      ^each gemrat list gets appended with an identifying key.
    if order:
        gem.sort(reverse=True)
        #  Group is ordered in-place with respect to decreasing gemrat.
    return gem


def groupholtf(groupdf, h=12, alpha=hw.hw_alpha, beta=hw.hw_beta):
    '''Holt-Winters forecasts h-periods ahead from group dataframe.'''
    forecasts = []
    keys = list(groupdf.columns)
    for k in keys:
        kdf = tool.todf(groupdf[k])
        holtdf = hw.holt(kdf, alpha, beta)
        forecastdf = hw.holtforecast(holtdf, h)
        forecasts.append(forecastdf)
    keysdf = tool.paste(forecasts)
    keysdf.columns = keys
    return keysdf


if __name__ == "__main__":
    system.endmodule()
