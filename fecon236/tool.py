#  Python Module for import                           Date : 2018-11-29
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  tool.py :: Fundamental tools for data analysis.

REFERENCES:

- Data structures, http://pandas.pydata.org/pandas-docs/dev/dsintro.html

- pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html

Note that np.float() is just an alias to Python's float type,
which is only exposed for backwards compatibility with a very early
version of numpy that inappropriately exposed np.float64 as np.float,
causing problems upon: from numpy import *
   - np.float() is not a numpy scalar type like np.float64()
   - Plain float() is fine for our numerical work here.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-11-29  Add median(), mad(), and madmen() for robust rescaling.
2018-07-08  Modify kurtfun() with population argument.
2018-07-07  Add std() with population argument for ddof.
2018-05-11  Rename to tool.py, fix imports.
2018-05-09  tools.py, fecon236 fork. Pass flake8.
2017-06-20  yi_1tools.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
import pandas as pd
import statsmodels.formula.api as smf
from fecon236.util import system


def nona(df):
    '''Eliminate any row in a dataframe containing NA, NaN nulls.'''
    return df.dropna()
    #  When calculating among dataframes, sometimes null entries
    #  are produced where the indexes are overlapping.
    #  Such nulls may choke numerical routines.


def head(dfx, n=7):
    '''Quick look at the INITIAL data point(s).'''
    return dfx.head(n)


def tail(dfx, n=7):
    '''Quick look at the LATEST data point(s).'''
    return dfx.tail(n)


def tailvalue(df, pos=0, row=1):
    '''Seek (last) row of dataframe, then the element at position pos.'''
    #  For pos, the index is not considered.
    return df.tail(row).values.tolist()[0][pos]
    #      values to array to list within list, then the element.
    #  Note how the name of a column is not required.


def div(numerator, denominator, floor=False):
    '''Division via numpy for pandas, Python 2 and 3 compatibility.
        Returns a scalar if both inputs are scalar, ndarray otherwise.
        We shall AVOID the ambiguous python2-like: np.divide()
    >>> x = np.array([0, 1, 2, 3, 4])
    >>> div(x, 4, floor=False)
    array([0.  ,  0.25,  0.5 ,  0.75,  1.])
    >>> div(x, 4, floor=True)
    array([0, 0, 0, 0, 1])
    >>> div(2, 4, floor=True)
    0
    >>> div(2, 4)
    0.5
    >>> div(2, 0)  # Dividing by zero returns infinity, not error:
    inf
    '''
    if floor:
        #      Like python3 "//":
        return np.floor_divide(numerator, denominator)
    else:
        #      Like python3 "/":
        return np.true_divide(numerator, denominator)


def roundit(it, n=4, echo=True):
    '''Echo or return list from iterable where floats are rounded n places.'''
    lst = [round(x, n) if isinstance(x, float) else x for x in it]
    #                                           ^e.g. exempt int and strings.
    if echo:
        print(lst)
    else:
        return lst


def dif(dfx, freq=1):
    '''Lagged difference for pandas series.'''
    #  Thus freq=1 gives so-called "first difference."
    return dfx.diff(periods=freq)


def pcent(dfx, freq=1):
    '''PERCENTAGE CHANGE method for pandas.'''
    return dfx.pct_change(periods=freq) * 100


def retrace(minimum, maximum, percent=50):
    '''Compute retracement between minimum and maximum.
        Noteworthy Fibonacci retracements: 23.6%, 38.2%, 61.8%
        Set percent as negative for retracement down from maximum,
        whereas positive percent implies retrace up from the minimum.
    >>> retrace(10, 110, -20)
    90.0
    >>> retrace(10, 110, 20)
    30.0
    '''
    if isinstance(minimum, pd.DataFrame):
        system.die("DataFrame argument UNACCEPTABLE. Try retracedf()")
    span = maximum - minimum
    portion = span * (abs(percent)/100.0)
    if percent < 0:
        target = maximum - portion
    else:
        target = minimum + portion
    return target


def retracedf(dfx, percent=50):
    '''Compute retracement between minimum and maximum of dataframe.'''
    #  Set percent as negative for retracement down from maximum,
    #  whereas positive percent implies retrace up from the minimum.
    minimum = dfx.min().iloc[0]
    maximum = dfx.max().iloc[0]
    target = retrace(minimum, maximum, percent)
    return [target, percent, minimum, maximum]


def georet(dfx, yearly=256):
    '''Compute geometric mean return in a summary list.'''
    #  yearly refers to frequency, e.g. 256 for daily trading days,
    #                                    12 for monthly,
    #                                     4 for quarterly.
    # -alt  dflg = np.log(dfx)
    # -alt  dfpc = dflg.diff(periods=1)
    dfpc = dfx.pct_change(periods=1)
    #          ^instead of first difference of logged data,
    #           gives slightly higher arithmetic means.
    mean = dfpc.mean().values.tolist()[0] * yearly
    vari = dfpc.var().values.tolist()[0] * yearly
    #          ^summary statistics methods, see
    #           McKinney, p.139, Table 5-10.
    geor = mean - (0.5*vari)
    #      ^arithmetic mean return penalized by risk,
    #      optimal choice under log utility.
    lst = [geor, mean, vari ** 0.5]
    #                        ^^^^^^i.e. std sigma, or volatility.
    lst = [round(i*100, 2) for i in lst]
    #       ^[geor, mean, volatility] in readable % form.
    lst.append(yearly)
    lst.append(dfx.shape[0])
    lst.append(str(dfx.index[0]).replace(' 00:00:00', ''))
    lst.append(str(dfx.index[-1]).replace(' 00:00:00', ''))
    #   So lst: [geor, mean, volatility, yearly,
    #                   sample_size, start_date, end_date]
    return lst


def zeroprice(rate, duration=9, yearly=2, face=100):
    '''Compute price of zero-coupon bond given its duration.'''
    #  Assume rate is in percentage form, e.g. 2.5% (not 0.025).
    #         rate could be a dataframe column.
    #  2014-08-28  duration of 10-y Treasury is 9.1 approx.
    #  yearly refers to payouts per year, so 2 means semi-annual.
    periodrate = rate / float(yearly * 100)
    periods = duration * yearly
    return float(face) / ((1 + periodrate) ** periods)


def std(data, population=False):
    '''Compute standard deviation with delta degrees of freedom, ddof.
       Default population=False is compatible with pandas and MATLAB
       since both defaults to SAMPLE standard deviation
       (using so-called Bessel's correction of N-1).
    '''
    #  Ref: https://stackoverflow.com/questions/27600207
    #  ddof must be integer-valued (not boolean):
    if population:
        ddof = 0   # For POPULATION standard deviation: numpy default!
    else:
        ddof = 1   # For SAMPLE standard deviation: pandas default.
    if isinstance(data, pd.DataFrame):
        #  This case will include ALL columns in the DataFrame.
        #  Convert to numpy array, then use numpy std() function:
        return data.values.std(ddof=ddof)
        #  Cf. pandas awkward method: data.std().tolist()[0]
    else:
        #  This case assumes that data is a numpy array:
        return data.std(ddof=ddof)  # so expect a scalar output.


def normalize(dfy):
    '''Center around mean zero and standardize deviation.'''
    centered = dfy - dfy.mean().tolist()[0]
    return centered / float(dfy.std().tolist()[0])


def median(dfy, col=0):
    '''Compute the median (by default, of the first dataframe column).'''
    return dfy.median().tolist()[col]


def mad(dfy):
    '''Median Absolute Deviation is a robust measure of dispersion:
    MAD = 0.67449*sigma if distribution is Gaussian, i.e.
    3*MAD is about 2*sigma; however, MAD is resilient to outliers,
    thus very useful in non-Gaussian situations.
    See https://en.wikipedia.org/wiki/Median_absolute_deviation
    '''
    dev = dfy - median(dfy)  # Deviations from median.
    #  MAD is defined as the median (not the mean)
    #  of absolute deviations from the data's median:
    return median(abs(dev))


def madmen(dfy):
    '''Rescale data as unitless MAD multiples, after shifting median to zero.
    The main character in the "Mad Men" series pretending to be Donald Draper
    is akin to our data pretending to be Gaussian, which we robustly unmask.
    [Cf. alternative normalize() where large deviations are squared.]
    '''
    dev = dfy - median(dfy)  # Deviations from median.
    return dev / mad(dfy)


def correlate(dfy, dfx, type='pearson'):
    '''CORRELATION FUNCTION between series using pandas method.'''
    #  N.B. -  must specify column(s) within dataframe(s) !
    #              Types of correlations:
    #  'pearson'   Standard correlation coefficient
    #  'kendall' 	Kendall Tau correlation coefficient
    #  'spearman' 	Spearman rank correlation coefficient
    return dfy.corr(dfx, method=type)


def cormatrix(dataframe, type='pearson'):
    '''PAIRWISE CORRELATIONS within a dataframe using pandas method.'''
    #              Types of correlations:
    #  'pearson'   Standard correlation coefficient
    #  'kendall' 	Kendall Tau correlation coefficient
    #  'spearman' 	Spearman rank correlation coefficient
    return dataframe.corr(method=type)


def regressformula(df, formula):
    '''Helper function for statsmodel linear regression using formula.'''
    #
    #  FORMULA is a string like "Y ~ 0 + X + Z"
    #          where column names of the df dataframe are used.
    #          Omit the 0 if you want an intercept fitted.
    #
    #  USAGE given that: result = regressformula(...)
    #        - print(result.summary())
    #        - result.params
    #        - coeff = result.params.tolist()
    #        - result.rsquared is also available.
    #        - result.aic is Akaike Information Criterion AIC.
    #
    return smf.ols(formula=formula, data=df).fit()


def regressTIME(dfy, col='Y'):
    '''Regression on time since that index cannot be independent variable.'''
    #  Assuming time series is evenly-spaced...
    df = dfy.dropna()
    #        ^insures proper alignment with timer:
    timer = [-i for i in range(df.count())]
    timer.reverse()
    #    ^thus current point is 0, timer future is 1, 2, 3, etc.
    #  Start creating two new columns, Timer and Fitted, to df:
    df['Timer'] = timer
    formula = col + " ~ Timer"
    result = regressformula(df, formula)
    coeff = result.params.tolist()
    fitted = [coeff[0] + (coeff[1] * i) for i in timer]
    df['Fitted'] = fitted
    #  Now we can return the fitted dataframe with original time index:
    dffit = todf(df['Fitted'])
    #             ^type Series
    return [dffit, coeff]


def regresstime(dfy, col='Y'):
    '''Regression on time since that index cannot be independent variable.'''
    #  Return just the fitted dataframe with original time intact.
    results = regressTIME(dfy, col)
    c, slope = results[1]
    print(" ::  regresstime slope = " + str(slope))
    return results[0]


def regresstimeforecast(dfy, h=24, col='Y'):
    '''Forecast h-periods ahead based on linear regression on time.'''
    c, slope = regressTIME(dfy, col)[1]
    forecast = [c + (slope * i) for i in range(h+1)]
    #  h=0 corresponds to the latest fitted point by design,
    #      so h=1 corresponds one-period ahead forecast.
    print(" ::  regresstime slope = " + str(slope))
    return todf(forecast, 'Forecast')


#  ALIASES for regression on TIME functions:
trend = regresstime
trendforecast = regresstimeforecast
foretrend = regresstimeforecast


def detrend(dfy, col='Y'):
    '''Detread using linear regression on time.'''
    trend = regresstime(dfy, col)
    return dfy - trend


def detrendpc(dfy, col='Y'):
    '''Detread using linear regression on time; percent deviation.'''
    trend = regresstime(dfy, col)
    #  return ((dfy - trend) * 100.00) / trend  #-X 2015-12-28
    return div((dfy - trend)*100, trend)


def detrendnorm(dfy, col='Y'):
    '''Detread using linear regression on time, then normalize.'''
    trend = regresstime(dfy, col)
    return normalize(dfy - trend)


def regress(dfy, dfx, intercept=True):
    '''Perform LINEAR REGRESSION, a.k.a. Ordinary Least Squares.'''
    #  2016-04-28  DEPRECATED ols from pandas.stats.api as of pandas 0.18,
    #                 so use regressformula() instead.
    #                 Add intercept option as boolean.    <= New feature!
    tmpdf = paste([todf(dfy), todf(dfx)])
    #  Need paste to properly align their index.
    tmpdf.columns = ['Y', 'X']
    if intercept:
        result = regressformula(tmpdf, 'Y ~ X')
        #   Implicitly, formula includes constant intercept term...
    else:
        result = regressformula(tmpdf, 'Y ~ 0 + X')
        #         ... whereas 0 excludes constant intercept term.
    #  Formerly pandas ols returned printable result summary,  <= Gotcha
    #  but now that is achieved by: print(result.summary())
    #  Returning pure result gives us the flexibility to access
    #  list of coefficients later as: result.params.tolist()
    return result


def kurtfun(data, raw=False, population=False):
    '''Compute kurtosis of an array or a single column DataFrame.
       Default uses PEARSON fourth central moment, where kurtosis is 3
       if data is Gaussian. Fischer "excess kurtosis":= k_Pearson-3.
    '''
    arr = toar(data)
    mu = np.mean(arr)
    sigma = std(arr, population=population)
    k_raw = (sum((arr - mu)**4)/len(arr))
    #     ^is sometimes called the "ABSOLUTE fourth central moment"
    #      which the Pearson version will then rescale.
    if raw:
        return k_raw
    else:
        k_Pearson = k_raw / sigma**4
        #  Equivalent to: scipy.stats.kurtosis(arr, fisher=False, bias=False)
        #                 when population=False, i.e. unbiased estimator,
        #  and preferred by Wolfram: http://mathworld.wolfram.com/Kurtosis.html
        #  which includes good references on estimation.
        #  For normality test, see scipy.stats.kurtosistest()
        return k_Pearson


def stat2(dfy, dfx, intercept=True):
    '''Quick STATISTICAL SUMMARY and regression on two variables'''
    print(" ::  FIRST variable:")
    now = dfy.describe()
    print(now)
    print()
    print(" ::  SECOND variable:")
    now = dfx.describe()
    print(now)
    print()
    print(" ::  CORRELATION")
    now = correlate(dfy, dfx)
    print(now)
    now = regress(dfy, dfx, intercept)
    print(now.summary())
    return


def stat(data, pctiles=[0.25, 0.50, 0.75]):
    '''QUICK summary statistics on given dataframe.'''
    dataframe = todf(data)
    print(dataframe.describe(percentiles=pctiles))
    #  excludes NaN values. Percentiles can be customized,
    #  but 50% (median) cannot be suppressed even with [] as arg.
    #  Also handles object dtypes like strings, see
    #  http://pandas.pydata.org/pandas-docs/version/0.17.0/generated/pandas.DataFrame.describe.html
    print("kurtosis ", round(kurtfun(data), 6))
    return


def stats(dataframe, n=3):
    '''VERBOSE statistics on dataframe; CORRELATIONS without regression.'''
    print(dataframe.describe())
    print()
    print(" ::  Index on min:")
    print(dataframe.idxmin())
    print()
    print(" ::  Index on max:")
    print(dataframe.idxmax())
    print()
    print(" ::  Head:")
    print(head(dataframe, n))
    print(" ::  Tail:")
    print(tail(dataframe, n))
    print()
    print(" ::  Correlation matrix:")
    print(cormatrix(dataframe))
    return


def df2a(dataframe):
    '''Convert single column dataframe to pure np.ndarray type.'''
    #     After numpy operations, avoids getting single-value array,
    #     rather than the single-value itself which one would be expecting.
    #  Suppose len(dataframe) is m, then after dropna(),
    #  data_n_1 of type np.ndarrary will have shape (n,1)
    #  but that can be annoying, so data_n will have pure shape (n,) instead.
    data_n_1 = dataframe.dropna().values
    data_n = data_n_1.reshape((len(data_n_1),))
    return data_n


#  TIP:  After operating between dataframes, USE todf FOR CLARITY:

def todf(data, col='Y'):
    '''CONVERT (list, Series, or DataFrame) TO DataFrame, NAMING single column.
           Also from np.ndarray of shapes (N,) or (N,1).
    '''
    #
    #  Operating among dataframes often produces a SERIES.
    #  We need CONVERSION for possible "paste" later,
    #     without the hassle of type() testing beforehand.
    #
    if isinstance(data, pd.DataFrame):
        #  Oooops, easy to mistaken a dataframe for a series.
        #  Move on, and just name that single column:
        target = data
        target.columns = [col]
    else:
        #  Do the conversion as intended:
        #  target = pd.DataFrame(data, columns=[col])
        #                               ^fails if col pre-exists in data.
        target = pd.DataFrame(data)
        target.columns = [col]
    #             ________ Explicitly drop NA values. Very helpful routinely!
    return target.dropna()


def toar(data):
    '''General converter to pure np.ndarray type.'''
    #  Examples of data input types: list, Series, or single-column DataFrame,
    #           but also np.ndarray of shapes (N,) or (N,1).
    #  Why? Because some numerical packages ONLY work with arrays,
    #       i.e. pandas types are not recognized.
    #  The following will assuredly have pure shape of (N,):
    return df2a(todf(data))


#  Data from different sources need standardized NAMES
#  to interoperate, esp. the time index which we call 'T'.
#  We imposed this convention when importing FRED data, and
#  thus for compatibility we shall use names()
#  as part of getqdl() and getstocks().

def names(data, col='Y', idx='T'):
    '''Give names to single column of a dataframe and its index.'''
    #  pandas has a confusing history of using .reindex and .rename
    #  but this works as of v5 (expect changes later from upstream):
    if isinstance(data, pd.DataFrame):
        #  data.columns.names is wrong for FRED, Quandl, and stocks.
        data.columns = [col]
        data.index.names = [idx]
    else:
        raise TypeError(' !!  names() requires DataFrame; use todf.')
    return data


def paste(df_list):
    '''Merge dataframes (not Series) across their common index values.'''
    #  N.B. -  paste for pandas < 0.14 will fail
    #          if column names are not unique
    #          (newer pandas append _x to non-unique names).
    for i in df_list:
        if not isinstance(i, pd.DataFrame):
            raise TypeError(' !!  paste requires DataFrame args; use todf.')
            #  paste will choke on a Series type, so use todf beforehand.
    combo = df_list[0]
    for df in df_list[1:]:
        temp = combo.merge(df, left_index=True,
                           right_index=True, how='inner')
        #  'inner' takes intersection of index values,
        #  whereas 'outer' takes their union.
        combo = temp.dropna()
        #            ^so row values will be comparable.
    return combo


def pastear(array_list):
    '''Merge arrays as columns (like paste for dataframes).'''
    #  N.B. -  To concatenate arrays horizontally, use np.hstack().
    #          To merge arrays as rows, use np.vstack().
    arr_tup = tuple(array_list)
    return np.column_stack(arr_tup)


def lagdf(df, lags=1):
    '''Create dataframe with lagged columns (labeled with underscore_lag).'''
    #  Argument df may have single or mutiple column(s).
    #  Argument lags can be any positive integer.
    #  N.B. -  useful data structure for vector autoregression of AR(lags).
    if not isinstance(df, pd.DataFrame):
        raise TypeError(' !!  lagdf requires DataFrame arg; use todf.')
    lagged = paste([df.shift(i) for i in range(lags+1)])
    #            Due to shift(0), original df is included in lagged.
    #  But shift() does NOT rename columns to indicate lag,
    #  which can be confusing for multiple lags, so we fix that next:
    lagged.columns = [i + '_' + str(j) for j in range(lags+1)
                      for i in df.columns]
    #      ^Thus: original column names + underscore_lag notation.
    return lagged


def diflog(data, lags=1):
    '''Difference between lagged log(data).'''
    #  If data is a DataFrame, it must be given as SINGLE-COLUMN.
    logged = np.log(todf(data))
    lagged = lagdf(logged, lags)
    #        ^!!=> produces columns like Y_0, Y_1, Y_2, etc.
    #              So large lags will hog memory, but cf. pcent().
    #  Even if data is an array, output will always be a DataFrame:
    return todf(lagged['Y_0'] - lagged['Y_'+str(lags)])


def writefile(dataframe, filename='tmp-fe-tool.csv', separator=','):
    '''Write dataframe to disk file using UTF-8 encoding.'''
    #  For tab delimited, use '\t' as separator.
    dataframe.to_csv(filename, sep=separator, encoding='utf-8')
    print(' ::  Dataframe written to file: ' + filename)
    return


if __name__ == "__main__":
    system.endmodule()
