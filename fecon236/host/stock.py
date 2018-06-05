#  Python Module for import                           Date : 2018-06-04
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  stock.py :: Access stock quotes for fecon236

Functions here are designed to access stock quotes FREELY.
Vendors of choice have been Yahoo Finance or Google Finance,
but given disruptions since late 2017, we consider alternates;
see https://github.com/rsvp/fecon235/issues/7 for details.

        Usage:  df = getstock('s4code', 7)
                #                       ^one week.
                #             ^begin with s4, then
                #              append stock SYMBOL in lower case.

 Dependencies:  pandas-datareader (for pandas>=0.17)

REFERENCES
- pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html
- pandas-datareader,
  https://pydata.github.io/pandas-datareader/stable/index.html
      ATTN: Package name is "pandas-datareader", but it is
         imported under the "pandas_datareader" module name.
- Wes McKinney, 2013, Python for Data Analysis.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-05-23  Rename to stock.py, fecon236 fork. Fix imports, pass flake8.
2017-02-06  yi_stocks.py, fecon235 v5.18.0312, https://git.io/fecon235
                pandas<=0.17 supported in fecon235.
'''

from __future__ import absolute_import, print_function, division

import datetime                # pddata dependency.
import pandas_datareader.data as pddata
from fecon236 import tool
from fecon236.util import system


#      __________ Favorite ABBREVIATIONS as variables:
s4spx = 's4spy'            # Largest S&P500 ETF.


def stock_decode(slang):
    '''Validate and translate slang string into vendor stock code.
       Our short slang must be in all lower case starting with s4,
       e.g. 's4spy' with SYMBOL in lower case.

       Using slang helps to avoid collision in our larger namespace.
    '''
    if slang.isupper() or slang[:2] != 's4':
        #  So if given argument is in all CAPS,
        #  or does not begin with 's4'
        raise ValueError('Stock slang argument is invalid.')
    else:
        try:
            symbol = slang[2:].upper()
        except Exception:
            raise ValueError('Stock slang argument is invalid.')
    return symbol


def stock_all(slang, maxi=3650):
    '''slang string retrieves ALL columns for single stock.

    The slang string consists of 's4' + symbol, all in lower case,
    e.g. 's4spy' for SPY.

    maxi is set to default of ten years past data.
    '''
    #       Typical:  start = datetime.datetime(2013, 1, 20)
    #       but we just want the most current window of data.
    now = datetime.datetime.now()
    end = now + datetime.timedelta(days=1)
    #           ^add just to be safe about timezones.
    start = end - datetime.timedelta(days=maxi)
    #             Date offsets are chronological days,
    #             NOT trading days.
    symbol = stock_decode(slang)
    #
    #        MAIN: use Yahoo Finance before Google Finance:
    try:
        df = pddata.DataReader(symbol, 'yahoo',  start, end)
        print(" ::  Retrieved from Yahoo Finance: " + symbol)
    except Exception:
        df = pddata.DataReader(symbol, 'google', start, end)
        print(" ::  Retrieved from Google Finance: " + symbol)
    return df


def stock_one(slang, maxi=3650, col='Close'):
    '''slang string retrieves SINGLE column for said stock.
        Available col include: Open, High, Low, Close, Volume
    '''
    df = stock_all(slang, maxi)
    #      return just a single column dataframe:
    return tool.todf(df[[col]])


def getstock(slang, maxi=3650):
    '''Retrieve stock data from Yahoo Finance or Google Finance.
    maxi is the number of chronological, not trading, days.
    We can SYNTHESIZE a s4 slang by use of string equivalent arg.
    '''
    if False:
        pass
    elif False:
        pass
    else:
        df = stock_one(slang, maxi, 'Close')
    #
    #         _Give default fecon235 names to column and index:
    df = tool.names(df)
    #         Finally NO NULLS, esp. for synthetics derived from
    #         overlapping indexes (note that readfile does
    #         fillna with pad beforehand):
    return df.dropna()


if __name__ == "__main__":
    system.endmodule()
