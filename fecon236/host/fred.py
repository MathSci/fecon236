#  Python Module for import                           Date : 2018-12-10
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  fred.py :: FRED database into pandas.

Functions access data from the Federal Reserve Bank, St. Louis.
Each economic time series and its frequency has its own "fredcode"
which is freely available from https://fred.stlouisfed.org

        Usage:  df = getfred(fredcode)

Favorite fredcodes are variables named d4*, m4*, q4*
which indicate their frequency: daily, monthly, or quarterly.

Principal functions: getfred(), daily(), monthly(), quarterly().

Some series are synthetically created using raw data from FRED.
Also we may extend their past history, but your working directory
must contain our supplemental CSV files.

REFERENCES:

- pandas, http://pandas.pydata.org/pandas-docs/stable/computation.html

- Wes McKinney, 2013, Python for Data Analysis.

- Mico Loretan, Federal Reserve Bulletin, Winter 2005,
       "Indexes of the Foreign Exchange Value of the Dollar",
       http://www.federalreserve.gov/pubs/bulletin/2005/winter05_index.pdf


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-12-10  Include more fredcodes for Treasury bonds.
2018-05-14  Gracefully deprecate plotfred().
2018-05-13  Eliminate lazy abbreviations, clarify comments.
2018-05-12  Given new division, eliminate float(integer).
2018-05-11  Fix imports. Deprecate plotfred().
2018-05-09  fred.py, fecon236 fork. Pass flake8.
2018-03-11  yi_fred.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

try:
    from urllib.request import urlopen
    #    ^for python3
except ImportError:
    from urllib2 import urlopen
    #    ^for python2   # py2rm

import numpy as np
import pandas as pd
from fecon236 import tool as tool
from fecon236.util import system as system
from fecon236.tsa import holtwinters as hw


zero10dur = 8.962           # duration of 10-y Treasury bond
#  2014-08-29 = 8.962 for 10-y due 8/15/24 c2.375 at 100.36 YTM 2.334%


#      __________ DAILY fredcode:

d4defl = 'd4defl'            # synthetic deflator dataframe, see deflator()

d4libjpy = 'JPY3MTD156N'     # 3-m LIBOR JPY, daily
d4libeur = 'EUR3MTD156N'     # 3-m LIBOR EUR, daily
d4libusd = 'USD3MTD156N'     # 3-m LIBOR USD, daily
d4ff = 'DFF'                 # Fed Funds, daily since 1954
d4ff30 = 'd4ff30'            # Fed Funds synthetic, "30-day" exp.mov.avg.
d4bills = 'DTB3'             # Treasury bills, daily, 1954 (not DGS3MO, 1982)

d4bond1 = 'DGS1'             # Treasury  1-y constant maturity, daily, 1962
d4bond2 = 'DGS2'             # Treasury  2-y constant maturity, daily, 1976
d4bond3 = 'DGS3'             # Treasury  3-y constant maturity, daily, 1962
d4bond5 = 'DGS5'             # Treasury  5-y constant maturity, daily, 1962
d4bond7 = 'DGS7'             # Treasury  7-y constant maturity, daily, 1969
d4bond10 = 'DGS10'           # Treasury 10-y constant maturity, daily, 1962
d4bond20 = 'DGS20'           # Treasury 20-y constant maturity, daily, 1993*
d4bond30 = 'DGS30'           # Treasury 30-y constant maturity, daily, 1977

d4zero10 = 'd4zero10'        # Zero-coupon price of Treasury 10-y, daily
d4tips10 = 'DFII10'          # TIPS 10-y constant, daily
d4curve = 'd4curve'          # Treasury 10_y-bills, getfred synthetic
d4bei = 'd4bei'              # 10_y Break-even inflation, getfred synthetic

d4usdjpy = 'DEXJPUS'         # USDJPY, daily
d4eurusd = 'DEXUSEU'         # EURUSD, daily
d4eurjpy = 'd4eurjpy'        # EURJPY, daily, getfred synthetic
d4usdcny = 'DEXCHUS'         # USDCNY, daily since 1981, not offshore USDCNH

d4xau = 'GOLDPMGBD228NLBM'   # London PM Gold fix, daily
d4xauusd = d4xau             # synonym

d4vix = 'VIXCLS'             # CBOE volatility on S&P options, daily
d4spx = 'SP500'              # S&P 500 index a.k.a. SPX, daily
#       ^only last ten years by April 2014 licensing,
#        however, we have it archived since 1957:
#            ~/ok/biz/inv/eq/data/FRED-SP500_1957-2014-ARC.csv.gz
#        See getspx below which will read a local copy.
#
#  [_] - method expires 2024, then use to_csv method to renew archive.


d4brent = 'DCOILBRENTEU'     # Oil Brent, DoE NSA daily
d4wti = 'DCOILWTICO'         # Oil WTI,   DoE NSA daily
d4oil = 'd4oil'              # Oil av. Brent and WTI, synthetic daily
d4gas = 'd4gas'              # Reg. gasoline $/gal. w/ tax, synthetic daily

dl_forex = [d4xau, d4eurusd, d4usdjpy]
dl_short = [d4bills, d4libusd, d4libeur, d4libjpy]
dl_long = [d4bond10, d4tips10, d4spx]
dlist = dl_forex + dl_short + dl_long


#      __________ MONTHLY fredcode:

m4gdpus = 'm4gdpus'    # U.S. GDP in billions, SA monthly synthetic
m4gdpusr = 'm4gdpusr'  # U.S. real GDP, current billions, SA monthly synthetic
m4housing = 'HOUST'    # U.S. Housing Starts, SA monthly
m4homepx = 'm4homepx'  # Home price Case-Shiller 20-city, SA monthly synthetic

m4wage = 'AHETPI'      # Hourly earnings, all private nonfarm, SA monthly
#                            production/nonsupervisory since 1964.
#  m4wage = 'CES0500000003'  # Hourly earnings, all private nonfarm, SA monthly
#           ^but only starts from 2006 -- shallow data.
#            Larger than AHETPI by $24.45/$20.61 = 1.1863 as of July 2014.
m4unemp = 'UNRATE'    # Unemployment rate, SA monthly
m4emppop = 'EMRATIO'  # Civilian employment/population, percent SA monthly
m4pop = 'POP'         # Total US population in thousands, NSA monthly
m4workers = 'm4workers'  # Total US workers in thousands, NSA monthly
m4nfp = 'PAYEMS'         # US Nonfarm Payroll workers in thousands, SA monthly
m4debt = 'm4debt'        # U.S. Federal debt in millions, NSA monthly synthetic

m4defl = 'm4defl'        # synthetic deflator, see getdeflator().
m4cpi = 'CPIAUCSL'       # Consumer Price Index, SA monthly since 1947
m4cpicore = 'CPILFESL'   # CPI core, SA monthly since 1957
#    core excludes food and energy.
m4pce = 'PCEPI'          # Personal Consumption Expenditure, SA monthly
m4pcecore = 'PCEPILFE'   # PCE core, SA monthly
m4infl = 'm4infl'        # synthetic inflation, see getinflations().
m4inflbei = 'm4inflbei'  # synthetic inflation averaged with BEI, see getfred.

m4bills = 'TB3MS'      # Treasury bills, monthly
m4zero10 = 'm4zero10'  # Zero-coupon price of Treasury 10-y, monthly
m4bond10 = 'GS10'      # Treasury 10-y constant, monthly
m4tips10 = 'FII10'     # TIPS 10-y constant, monthly
m4bei = 'm4bei'        # 10_y Break-even inflation, getfred synthetic

m4usdrtb = 'TWEXBPA'   # Real trade-weighted USD index: Broad, monthly
m4xau = 'm4xau'        # London Gold PM fix, synthetic monthly for getfred
m4xauusd = m4xau       # synonym
m4xaueur = 'm4xaueur'  # Gold euro-denominated, synthetic monthly
m4xaujpy = 'm4xaujpy'  # Gold  yen-denominated,           monthly
m4xaurtb = 'm4xaurtb'  # Real trade-weighted Gold index, synthetic monthly

m4usdjpy = 'm4usdjpy'  # USDJPY monthly, getfred synthetic
m4eurusd = 'm4eurusd'  # EURUSD, DEM FRF synthetic 1971-2002, getfred monthly
m4eurjpy = 'm4eurjpy'  # EURJPY monthly, getfred synthetic back to 1971

m4baseus = 'AMBSL'     # U.S. Adjusted Monetary Base in billions, SA monthly

m4spx = 'm4spx'        # S&P 500 index aka SPX, synthetic monthly for getfred
m4spxrtb = 'm4spxrtb'  # Real trade-weighted SPX index, synthetic monthly

m4oil = 'm4oil'        # Oil av. Brent and WTI, synthetic monthly

ml_econ = [m4gdpusr, m4wage, m4unemp]
ml_infl = [m4cpi, m4cpicore, m4pce, m4pcecore]
ml_short = [m4bills]
ml_long = [m4bond10, m4tips10, m4spx]
mlist = ml_econ + ml_infl + ml_long


#      __________ QUARTERLY fredcode:

q4gdpus = 'GDP'       # U.S. GDP in billions, SA quarterly
q4gdpusr = 'GDPC1'    # U.S. real GDP in 2009 billions, SA quarterly
q4debt = 'GFDEBTN'    # U.S. Federal debt in millions, NSA quarterly

q4spx = 'q4spx'       # S&P 500 index, synthetic quarterly for getfred

ql_econ = [q4gdpusr]
ql_long = [q4spx]
qlist = ql_econ + ql_long


#      __________ EUROZONE fredcode:
q4gdpeu = 'EUNGDP'     # EU GDP in million euros, Eurostat SA quarterly
m4gdpeur = 'm4gdpeur'  # EU GDP in real billions, synthetic SA monthly
m4infleu = 'm4infleu'  # EU Consumer Prices, synthetic Eurostat monthly
m4defleu = 'm4defleu'  # EU deflator, synthetic monthly

m4unempeu = 'LRHUTTTTEZM156S'  # EU Unemployment rate, OECD SA monthly
m4unempfr = 'LRHUTTTTFRM156S'  # FR Unemployment rate, OECD SA monthly
#      France data is updated frequently, whereas for EU there is a severe lag.


#  ======================================== End of fredcode ===============


#  GOTCHA: pd.read_csv assumes str in what's read, thus
#          make conversions for numerical work later.

def readfile(filename, separator=',', compress=None):
    '''Read file (CSV default) as pandas dataframe.'''
    #  If separator is space, use '\s+' since regex will work.
    #  compress will take 'gzip' or 'bzip' as value.
    #
    dataframe = pd.read_csv(filename, sep=separator,
                            compression=compress,
                            index_col=0, parse_dates=True,
                            header=0, names=['T', 'Y'])
    #                       Header on FRED's first line was: DATE, VALUE
    #
    #  Numeric conversion is critical for math ops between dataframes!
    #        (Not necessary for plotting, seemingly auto-converted?)
    #  dtype is crucial, yet numeric conversion can be fragile
    #        when data is missing or mistyped, e.g.
    #             dataframe['Y'] = dataframe['Y'].astype(float)
    #        will fail if the data is not in perfect condition.
    try:
        dataframe['Y'] = pd.to_numeric(dataframe['Y'], errors='coerce')
        #  'coerce' gives NaN if particular parsing is invalid.
    except Exception:
        #  convert_objects deprecated, but courtesy for pd < 0.17:
        dataframe['Y'] = dataframe['Y'].convert_objects(convert_numeric=True)
        #                              ^non-convertibles become NaN
    #  FRED uses "." to indicate missing value.
    dataframe['Y'] = dataframe['Y'].fillna(method='pad')
    #                              ^NaN replaced by fill forward,
    #                               common practice in time series analysis.
    return dataframe
    #      ^has NO NULL VALUES because of pad above,
    #       thus .dropna() is unnecessary.


def makeURL(fredcode):
    '''Create http address to access FRED's CSV files.'''
    #         Validated July 2014.
    return 'http://research.stlouisfed.org/fred2/series/' \
        + fredcode + '/downloaddata/' + fredcode + '.csv'


#  N.B. -  getdata_fred is a vital helper for MORE GENERAL getfred BELOW.
#          It's the best primitive to get raw FRED data.

def getdata_fred(fredcode):
    '''Download CSV file from FRED and read it as pandas DATAFRAME.'''
    #  2014-08-11 former name "getdataframe".
    #  2015-12-05 fredcsv = urllib2.urlopen(makeURL(fredcode))
    #                Change import style for python3 compatibility.
    fredcsv = urlopen(makeURL(fredcode))
    return readfile(fredcsv)


def index_delta_secs(dataframe):
    '''Find minimum in seconds between index values.'''
    nanosecs_timedelta64 = np.diff(dataframe.index.values).min()
    #  Picked min() over median() to conserve memory;      ^^^^^!
    #  also avoids missing values issue,
    #  e.g. weekend or holidays gaps for daily data.
    secs_timedelta64 = tool.div(nanosecs_timedelta64, 1e9)
    #  To avoid numerical error, we divide before converting type:
    secs = secs_timedelta64.astype(np.float32)
    if secs == 0.0:
        system.warn('Index contains duplicate, min delta was 0.')
        return secs
    else:
        return secs

    #  There are OTHER METHODS to get the FREQUENCY of a dataframe:
    #       e.g.  df.index.freq  OR  df.index.freqstr ,
    #  however, these work only if the frequency was attributed:
    #       e.g.  '1 Hour'       OR  'H'  respectively.
    #  The fecon235 derived dataframes will usually return None.
    #
    #  Two timedelta64 units, 'Y' years and 'M' months, are
    #  specially treated because the time they represent depends upon
    #  their context. While a timedelta64 day unit is equivalent to
    #  24 hours, there is difficulty converting a month unit into days
    #  because months have varying number of days.
    #       Other numpy timedelta64 units can be found here:
    #  http://docs.scipy.org/doc/numpy/reference/arrays.datetime.html
    #
    #  For pandas we could do:  pd.infer_freq(df.index)
    #  which, for example, might output 'B' for business daily series.
    #
    #  But the STRING representation of index frequency is IMPRACTICAL
    #  since we may want to compare two unevenly timed indexes.
    #  That comparison is BEST DONE NUMERICALLY in some common unit
    #  (we use seconds since that is the Unix epoch convention).
    #
    #  Such comparison will be crucial for the machine
    #  to chose whether downsampling or upsampling is appropriate.
    #  The casual user should not be expected to know the functions
    #  within index_delta_secs() to smoothly work with a notebook.


#  For details on frequency conversion, see McKinney 2013,
#       Chp. 10 RESAMPLING, esp. Table 10-5 on downsampling.
#       pandas defaults are:  how='mean', closed='right', label='right'
#
#  2014-08-10  closed and label to the 'left' conform to FRED practices.
#              how='median' since it is more robust than 'mean'.
#  2014-08-14  If upsampling, interpolate() does linear evenly,
#              disregarding uneven time intervals.
#  2016-11-06  McKinney 2013 on resampling is outdated as of pandas 0.18


def resample_main(dataframe, rule, secs):
    '''Generalized resample routine for downsampling or upsampling.'''
    #  rule is the offset string or object representing target conversion,
    #       e.g. 'B', 'MS', or 'QS-OCT' to be compatible with FRED.
    #  secs should be the maximum seconds expected for rule frequency.
    if index_delta_secs(dataframe) < secs:
        df = dataframe.resample(rule, closed='left', label='left').median()
        #    how='median' for DOWNSAMPLING deprecated as of pandas 0.18
        return df
    else:
        df = dataframe.resample(rule, closed='left', label='left').fillna(None)
        #    fill_method=None for UPSAMPLING deprecated as of pandas 0.18
        #    note that None almost acts like np.nan which fails as argument.
        #    interpolate() applies to those filled nulls when upsampling:
        #    'linear' ignores index values treating it as equally spaced.
        return df.interpolate(method='linear')


def daily(dataframe):
    '''Resample data to daily using only business days.'''
    #                         'D' is used calendar daily
    #                         'B' for business daily
    secs1day2hours = 93600.0
    return resample_main(dataframe, 'B', secs1day2hours)


def monthly(dataframe):
    '''Resample data to FRED's month start frequency.'''
    #  FRED uses the start of the month to index its monthly data.
    #                         'M'  is used for end of month.
    #                         'MS' for start of month.
    secs31days = 2678400.0
    return resample_main(dataframe, 'MS', secs31days)


def quarterly(dataframe):
    '''Resample data to FRED's quarterly start frequency.'''
    #  FRED uses the start of the month to index its monthly data.
    #  Then for quarterly data: 1-01, 4-01, 7-01, 10-01.
    #                            Q1    Q2    Q3     Q4
    #  ________ Start at first of months,
    #  ________ for year ending in indicated month.
    #  'QS-OCT'
    secs93days = 8035200.0
    return resample_main(dataframe, 'QS-OCT', secs93days)


def getm4eurusd(fredcode=d4eurusd):
    '''Make monthly EURUSD, and try to prepend 1971-2002 archive.'''
    #  Synthetic euro is the average between
    #                 DEM fixed at 1.95583 and
    #                 FRF fixed at 6.55957.
    eurnow = monthly(getdata_fred(fredcode))
    try:
        eurold = readfile('FRED-EURUSD_1971-2002-ARC.csv.gz', compress='gzip')
        eurall = eurold.combine_first(eurnow)
        #               ^appends dataframe
        print(' ::  EURUSD synthetically goes back monthly to 1971.')
    except Exception:
        eurall = eurnow
        print(' ::  EURUSD monthly without synthetic 1971-2002 archive.')
    return eurall


def getspx(fredcode=d4spx):
    '''Make daily S&P 500 series, and try to prepend 1957-archive.'''
    #  Fred is currently licensed for only 10 years worth,
    #  however, we have a local copy of 1957-2014 daily data.
    spnow = getdata_fred(fredcode)
    try:
        spold = readfile('FRED-SP500_1957-2014-ARC.csv.gz', compress='gzip')
        spall = spold.combine_first(spnow)
        #             ^appends dataframe
        print(' ::  S&P 500 prepend successfully goes back to 1957.')
    except Exception:
        spall = spnow
        print(' ::  S&P 500 for last 10 years (1957-archive not found).')
    return spall


def gethomepx(fredcode=m4homepx):
    '''Make Case-Shiller 20-city, and try to prepend 1987-2000 10-city.'''
    #  Fred's licensing may change since source is S&P,
    #  however, we have a local copy of 1987-2013 monthly SA data.
    hpnow = getdata_fred('SPCS20RSA')
    #                          20-city home price index back to 2000-01-01.
    try:
        hpold = readfile('FRED-home-Case-Shiller_1987-2013.csv.gz',
                         compress='gzip')
        #                ^includes 10-city index from 1987-2000.
        #                 Current correlation with 20-city: 0.998
        #                 Thus the mashup is justified.
        hpall = hpold.combine_first(hpnow)
        #             ^appends dataframe
        print(' ::  Case-Shiller prepend successfully goes back to 1987.')
    except Exception:
        hpall = hpnow
        print(' ::  Case-Shiller since 2000 (1987-archive not found).')
    #  Case-Shiller is not dollar based, so we use:
    #  Median Sales Price of Existing Homes
    #  from the National Association of Realtors, fredcode: HOSMEDUSM052N
    dollarindex = 183700.57 / 153.843
    #     means:  ^Realtor$   ^C-S 20-city from 2000-01-01 to 2014-06-01.
    return hpall * dollarindex


def getinflations(inflations=ml_infl):
    '''Normalize and average all inflation measures.'''
    #  We will take the average of indexes after their
    #  current value is set to 1 for equal weighting.
    inflsum = getdata_fred(inflations[0])
    inflsum = inflsum / float(tool.tailvalue(inflsum))
    for i in inflations[1:]:
        infl = getdata_fred(i)
        infl = infl / float(tool.tailvalue(infl))
        inflsum += infl
    return inflsum / len(inflations)


def getdeflator(inflation=m4infl):
    '''Construct a de-inflation dataframe suitable as multiplier.'''
    #  Usually we encounter numbers which have been deflated to dollars
    #  of some arbitrary year (where the value is probably 100).
    #  Here we set the present to 1, while past values have increasing
    #     multiplicative "returns" which will yield current dollars.
    infl = getfred(inflation)
    lastin = tool.tailvalue(infl)
    return float(lastin) / infl
    #           Think inverted inflation:-)


def getm4infleu():
    '''Normalize and average Eurozone Consumer Prices.'''
    #  FRED carries only NSA data from Eurostat,
    #  so we shall use Holt-Winters levels.
    cpiall = getdata_fred('CP0000EZ17M086NEST')
    #                        ^for 17 countries.
    holtall = hw.holtlevel(cpiall)
    normall = holtall / float(tool.tailvalue(holtall))
    return normall
    #  #   SUSPENDED since last is 2013-12-01.
    #  cpicore = getdata_fred('CPHPLA01EZM661N')
    #  holtcore = hw.holtlevel(cpicore)
    #  normcore = holtcore / float(tool.tailvalue(holtcore))
    #  #  We will take the average of indexes after their
    #  #  current value is set to 1 for equal weighting.
    #  return (normall + normcore) / 2.0


def getfred(fredcode):
    '''Retrieve from FRED in dataframe format, INCL. SPECIAL CASES.'''
    #    We can SYNTHESIZE a FREDCODE by use of string equivalent arg:
    if fredcode == m4gdpus:
        df = monthly(getdata_fred(q4gdpus))
    elif fredcode == m4gdpusr:
        df = getfred(m4defl) * getfred(m4gdpus)
    elif fredcode == m4debt:
        df = monthly(getdata_fred(q4debt))
    elif fredcode == m4workers:
        workfrac = getdata_fred(m4emppop) / 100.
        pop = getdata_fred(m4pop)
        df = workfrac * pop
    elif fredcode == m4homepx:
        df = gethomepx()

    elif fredcode == d4defl:
        df = daily(getdeflator())
    elif fredcode == m4defl:
        df = getdeflator()
    elif fredcode == m4infl:
        df = getinflations()

    elif fredcode == m4gdpeur:
        mgdpeu = monthly(getdata_fred(q4gdpeu)) / 1000.
        df = getfred(m4defleu) * mgdpeu
    elif fredcode == m4infleu:
        df = getm4infleu()
    elif fredcode == m4defleu:
        df = getdeflator(m4infleu)

    elif fredcode == d4eurjpy:
        eurusd = getdata_fred(d4eurusd)
        usdjpy = getdata_fred(d4usdjpy)
        df = eurusd * usdjpy
    elif fredcode == m4usdjpy:
        df = monthly(getdata_fred(d4usdjpy))
    elif fredcode == m4eurusd:
        df = getm4eurusd()
    elif fredcode == m4eurjpy:
        eurusd = getfred(m4eurusd)
        usdjpy = getfred(m4usdjpy)
        df = eurusd * usdjpy
    elif fredcode == m4xau:
        df = monthly(getdata_fred(d4xau))
    elif fredcode == m4xaueur:
        xauusd = getfred(m4xau)
        eurusd = getfred(m4eurusd)
        df = xauusd / eurusd
    elif fredcode == m4xaujpy:
        xauusd = getfred(m4xau)
        usdjpy = getfred(m4usdjpy)
        df = xauusd * usdjpy
    elif fredcode == m4xaurtb:
        usdrtb = getdata_fred(m4usdrtb)
        xauusd = getfred(m4xau) / 1000.
        df = usdrtb * xauusd

    elif fredcode == d4ff30:
        df = hw.ema(getdata_fred(d4ff), 0.0645)
        #       exponential moving avg.   ^"30-day"
    elif fredcode == d4zero10:
        bond10 = getdata_fred(d4bond10)
        df = tool.zeroprice(bond10, zero10dur)
    elif fredcode == m4zero10:
        df = monthly(getfred(d4zero10))
    elif fredcode == d4curve:
        bond10 = getdata_fred(d4bond10)
        bills = getdata_fred(d4bills)
        df = bond10 - bills
    elif fredcode == d4bei:
        bond10 = getdata_fred(d4bond10)
        tips10 = getdata_fred(d4tips10)
        df = bond10 - tips10
    elif fredcode == m4bei:
        bond10 = getdata_fred(m4bond10)
        tips10 = getdata_fred(m4tips10)
        df = bond10 - tips10
    elif fredcode == m4inflbei:
        inflpc = tool.pcent(getfred(m4infl), 12)  # YoY% form
        df = (inflpc + getfred(m4bei)) / 2.
        #  ^average of backward and forward looking inflation!

    elif fredcode == d4spx:
        df = getspx()
    elif fredcode == m4spx:
        df = monthly(getspx())
    elif fredcode == m4spxrtb:
        usdrtb = getdata_fred(m4usdrtb)
        spxusd = getfred(m4spx) / 1000.
        df = usdrtb * spxusd
    elif fredcode == q4spx:
        df = quarterly(getspx())

    elif fredcode == d4oil:
        brent = getdata_fred(d4brent)
        wti = getdata_fred(d4wti)
        df = (brent + wti) / 2.
    elif fredcode == m4oil:
        df = monthly(getfred(d4oil))
    elif fredcode == d4gas:
        df = daily(getdata_fred('GASREGW'))
        #           ^weekly DoE survey, USD/gallon + tax, NSA

    else:
        df = getdata_fred(fredcode)
    return df.dropna()
    #        ^NO NULLS finally, esp. for synthetics derived from
    #         overlapping indexes, noting that in general:
    #         readfile does fillna with pad beforehand.


def plotfred(data, title='tmp', maxi=87654321):
    '''DEPRECATED: Plot data should be given as dataframe or fredcode.'''
    #  ^2018-05-11. Removal OK after 2020-01-01.
    msg = "plotfred() DEPRECATED. Instead use get() and plot()."
    raise DeprecationWarning(msg)


if __name__ == "__main__":
    system.endmodule()


# ========================================================= ENDNOTES ==========


# - *"Two different price indexes are popular for measuring inflation: the
# consumer price index (CPI) from the Bureau of Labor Statistics and the
# personal consumption expenditures price index (PCE) from the Bureau of
# Economic Analysis. [A]n accurate measure of inflation is important for both
# the U.S. federal government and the Federal Reserve's Federal Open Market
# Committee (FOMC), but they focus on different measures. For example, the
# federal government uses the CPI to make inflation adjustments to certain
# kinds of benefits, such as Social Security. In contrast, the FOMC focuses on
# PCE inflation in its quarterly economic projections and also states its
# longer-run inflation goal in terms of headline PCE. The FOMC focused on CPI
# inflation prior to 2000 but, after extensive analysis, changed to PCE
# inflation for three main reasons: The expenditure weights in the PCE can
# change as people substitute away from some goods and services toward others,
# the PCE includes more comprehensive coverage of goods and services, and
# historical PCE data can be revised (more than for seasonal factors only)."*
# --James Bullard, president of the Federal Reserve Bank of St. Louis.
