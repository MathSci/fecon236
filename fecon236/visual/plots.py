#  Python Module for import                           Date : 2018-06-08
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  plots.py :: Plot functions using matplotlib.

Functions to plot data look routine, but in actuality specifying
the details can be a huge hassle involving lots of trial and error.
To avoid repetitive boilerplate code, we use decorator saveImage.

A plot has default title STRING of 'tmp' which prevents saving the
image to disk. This is suitable for quick show on screen, and for
conserving disk space. Specifying a title NOT starting with 'tmp'
will produce a PNG image file. Moreover, it is possible to
suppress screen show by adding a leading blank space to the title.

REFERENCES:

- matplotlib, http://matplotlib.org/api/pyplot_api.html

- pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-08  Clarify plotn() usage.
2018-05-20  Use functools.wraps within saveImage decorator.
2018-05-17  Suppress show screen via leading space in title.
                Fix boxplot() by removing NaN from data.
2018-05-16  MAJOR refactoring using decorator saveImage().
2018-05-14  Transplant plot() but deprecate use of symbol code as argument.
2018-05-11  Fix imports.
2018-05-09  plots.py, fecon236 fork. Pass flake8.
2017-05-15  yi_plot.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

#  import matplotlib.cm as colormap   # Unused, but see comments.
import matplotlib.pyplot as plt
import pandas as pd
import scipy
from fecon236.util import system
from fecon236 import tool

from functools import wraps
#  functools.wraps is meta-decorator which revises attributes of the wrapper
#  to those of the underlying function. Useful for introspection and debugging,
#  adequate for "?" but not informative enough for "??" inquiry.
#  https://www.thecodeship.com/patterns/guide-to-python-function-decorators


dotsperinch = 140
# DPI resolution for plots. Modifiable by e.g. "fe.plots.dotsperinch = 200"


def saveImage(func):
    '''Decorator to save plot image to disk, option to suppress screen show.'''
    #  The underlying func MUST "return [title, fig]".
    #  Image saved to file ONLY if title string does NOT start with 'tmp'.
    #  Screen show can be suppressed by a leading blank space in title arg.
    @wraps(func)
    def saveimage(*args, **kwargs):
        '''Wrapper for the decorator saveImage.'''
        title, fig = func(*args, **kwargs)
        if not title.startswith(' '):
            plt.show()
        if not title.startswith('tmp'):
            title = title.replace(' ', '_')
            imgf = 'img' + '-' + func.__name__ + '-' + title + '.png'
            print(" ::  Stand-by, saving, " + str(dotsperinch)
                  + " DPI: " + imgf)
            fig.set_size_inches(11.5, 8.5)
            fig.savefig(imgf, dpi=dotsperinch)
            #  ^Will overwrite file with same name.
            plt.close()
        return
    return saveimage


@saveImage
def plotdf(dataframe, title='tmp'):
    '''Plot dataframe where its index are dates.'''
    dataframe = tool.todf(dataframe)
    #                ^todf must dropna(),
    #                 otherwise index of last point plotted may be wrong.
    #           Also helps if dataframe resulted from synthetic operations,
    #           or if a Series was incorrectly submitted as Dataframe.
    fig, ax = plt.subplots()
    ax.xaxis_date()
    #  ^interpret x-axis values as dates.
    plt.xticks(rotation='vertical')
    #       show x labels vertically.

    ax.plot(dataframe.index, dataframe, 'b-')
    #       ^x               ^y          blue line
    #                                    k is black.
    ax.set_title(title + ' / last ' + str(dataframe.index[-1]))
    #                                 ^timestamp of last data point
    plt.grid(True)
    return [title, fig]


#  saveImage decorator not needed here.
def plot(data, title='tmp', maxi=87654321):
    '''Wrapper around plotdf() which accepts DataFrame with date index.
       For list or numbered index, use plotn() instead.
       Backwards-compatible maxi is maximum number of most recent data.
    '''
    if isinstance(data, pd.DataFrame):
        plotdf(tool.tail(data, maxi), title)
    else:
        #  Wrapping of plotfred and plotqdl has been deprecated (fecon236),
        #  thus "data" argument can no longer be a fredcode or quandlcode.
        msg = "Symbol codes no longer supported by plot; get() a DataFrame."
        raise TypeError(msg)
    return


@saveImage
def plotn(data, title='tmp'):
    '''Plot list, array, Series, or DataFrame where the index is numbered.'''
    #  With todf: list, array, or Series will be converted to DataFrame.
    dataframe = tool.todf(data)
    #               ^todf must dropna(),
    #                otherwise index of last point plotted may be wrong.
    fig, ax = plt.subplots()
    #  ax.xaxis_date()
    #  #  ^interpret x-axis values as dates.
    plt.xticks(rotation='vertical')
    #       show x labels vertically.
    #
    ax.plot(dataframe.index, dataframe, 'b-')
    #       ^x               ^y          blue line
    #                                    k is black.
    ax.set_title(title + ' / last ' + str(dataframe.index[-1]))
    #                                 ^index on last data point
    plt.grid(True)
    return [title, fig]


@saveImage
def boxplot(data, title='tmp', labels=[]):
    '''Make boxplot from data which could be a dataframe.'''
    #  - Use list of strings for labels,
    #       since we presume data has no column names,
    #       unless data is a dataframe.
    #
    #  - Directly entering a dataframe as data will fail,
    #       but dataframe.values will work, so:
    lastidx = 'NA'
    #         ^for part of the plot's title...
    #  If data is a dataframe, extract some info
    #    before conversion to values:
    if isinstance(data, pd.DataFrame):
        data = data.dropna()
        #          ^NaN interferes with "percentile interpolation"
        lastidx = str(data.index[-1])
        colnames = list(data.columns)
        labels = colnames
        data = data.values
    fig, ax = plt.subplots()
    ax.boxplot(data)
    ax.set_xticklabels(labels)
    #  HACK to show points of last row as a red dot:
    ax.plot([list(data[-1])[0]] + list(data[-1]), 'or')
    #        ^need a dummy first point in the neighborhood
    #         for autoscale to work properly.
    ax.set_title(title + ' / last ' + lastidx)
    plt.grid(True)
    return [title, fig]

    #  #  Test data for boxplot:
    #  import numpy as np
    #
    #  np.random.seed(10)
    #
    #  data = np.random.randn(30, 4)
    #  labels = ['A', 'B', 'C', 'D']


@saveImage
def scatter(dataframe, title='tmp', col=[0, 1]):
    '''Scatter plot for dataframe by zero-based column positions.'''
    #  First in col is x-axis, second is y-axis.
    #  Index itself is excluded from position numbering.
    dataframe = dataframe.dropna()
    #           ^esp. if it resulted from synthetic operations,
    #                 else timestamp of last point plotted may be wrong.
    count = len(dataframe)
    countf = float(count)
    colorseq = [i / countf for i in range(count)]
    #  Default colorseq uses rainbow, same as MATLAB.
    #  So sequentially: blue, green, yellow, red.
    #  We could change colormap by cmap below.
    fig, ax = plt.subplots()
    plt.xticks(rotation='vertical')
    #       Show x labels vertically.
    ax.scatter(dataframe.iloc[:, col[0]], dataframe.iloc[:, col[1]],
               c=colorseq)
    #         First arg for x-axis, second for y-axis, then
    #         c is for color sequence. For another type of
    #         sequential color shading, we could append argument:
    #             cmap=colormap.coolwarm
    #             cmap=colormap.Spectral
    #             cmap=colormap.viridis  [perceptual uniform]
    #         but we leave cmap arg out since viridis will be the
    #         default soon: http://matplotlib.org/users/colormaps.html
    colstr = '_' + str(col[0]) + '-' + str(col[1])
    title = title + colstr
    ax.set_title(title + colstr + ' / last ' + str(dataframe.index[-1]))
    #                                          ^index on last data point
    plt.grid(True)
    return [title, fig]


#  saveImage decorator not needed here.
def scats(dataframe, title='tmp'):
    '''All pair-wise scatter plots for dataframe.'''
    #  Renaming title will result in file output.
    ncol = dataframe.shape[1]
    #                ^number of columns
    pairs = [[i, j] for i in range(ncol) for j in range(ncol) if i < j]
    npairs = (ncol**2 - ncol) / 2
    #  e.g. ncol==5  implies npairs==10
    #       ncol==10 implies npairs==45
    #       ncol==20 implies npairs==190
    print(" ::  Number of pair-wise plots: " + str(npairs))
    for pair in pairs:
        print(" ::  Show column pair: " + str(pair))
        scatter(dataframe, title, pair)
        print("----------------------")
    return


#  saveImage decorator not needed here.
def scat(dfx, dfy, title='tmp', col=[0, 1]):
    '''Scatter plot between two pasted dataframes.'''
    #  Renaming title will result in file output.
    scatter(tool.paste([dfx, dfy]), title, col)
    return


#  Note: Leptokurtosis ("fat tails") is much more distinctive in the
#  Q-Q plots than P-P plots. Bi-modality and skewness are more distinctive
#  in P-P plots (discriminating in regions of high probability density)
#  than Q-Q plots (better for regions of low probability density).
#     See https://en.wikipedia.org/wiki/P–P_plot
#     and http://v8doc.sas.com/sashtml/qc/chap8/sect9.htm


@saveImage
def plotqq(data, title='tmp', dist='norm', fitLS=True):
    '''Display/save quantile-quantile Q-Q probability plot.
    Q–Q plot here is used to compare data to a theoretical distribution.
    Ref: https://en.wikipedia.org/wiki/Q–Q_plot
    '''
    #     Assume "data" to be np.ndarray or single-column DataFrame.
    #  Theoretical quantiles on horizontal x-axis estimated by Filliben method.
    #  Green line depicits theoretical distribution; fitLS computes R^2:
    #      The axes are purposely transformed in order to make the specified
    #      distribution "dist" appear as a linear green line.
    #                   'norm' is a Gaussian distribution.
    #  The "data" plotted along the vertical y-axis.
    fig, ax = plt.subplots()
    arr = tool.toar(data)
    #     ^Roundabout way guarantees a pure array needed for MAIN probplot:
    _ = scipy.stats.probplot(arr, dist=dist, fit=fitLS, plot=plt)  # noqa
    #   Ignore numerical output, just give plot object to matplotlib.
    #  https://docs.scipy.org/doc/scipy/reference/generated/scipy.stats.probplot.html
    #  Prefer scipy version over statsmodels.graphics.gofplots.qqplot()
    ax.get_lines()[0].set_marker('.')
    ax.get_lines()[0].set_markersize(7.0)
    ax.get_lines()[0].set_markerfacecolor('r')
    #             [0] strangely refers to data points, set to red.
    ax.get_lines()[1].set_color('g')
    #             [1] refers to the straight theoretic line, set to green.
    #         But points in common should be blue, rather than brown.
    plt.title(title + " / plotqq " + dist + ", count=" + str(len(arr)))
    plt.grid(True)
    return [title, fig]


if __name__ == "__main__":
    system.endmodule()
