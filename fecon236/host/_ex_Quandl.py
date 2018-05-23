#  Python Module for import                           Date : 2018-05-23
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  _ex_Quandl.py :: fecon236 fork of Quandl API 2.8.9.

Currently supports getting and searching datasets.

On 2016-04-22 Quandl released version 3 of their API which was a "drop-in"
replacement of version 2, but a very complex *package* which has not seen
any substantive improvement since that date -- see
https://github.com/quandl/quandl-python/blob/master/2_SERIES_UPGRADE.md

Their version 2.8.9, however, had the virtue of being just a *single* module,
and has been battle-tested in fecon235 notebooks since 2015-08-03.
That module has been forked at fecon236 and renamed _ex_Quandl.py.
The fecon236 qdl module is a wrapper around _ex_Quandl.py.


REFERENCES:

- Using Quandl's Python module: https://www.quandl.com/tools/python
                   GitHub repo: https://github.com/quandl/quandl-python

- Source code for Quandl.py version 2.8.9:
  https://github.com/quandl/quandl-python/blob/v2.8.9/Quandl/Quandl.py

- Complete Quandl API documentation: https://www.quandl.com/docs/api
  including error codes.

- RESTful interface introduction:  https://www.quandl.com/help/api
  Not needed here, but it's available for their API version 3.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-05-23  _ex_Quandl.py, fecon236 fork of Quandl.py version 2.8.9.
                Fix over 80 flake8 violations. Pass test_qdl.py.
2016-04-22  [Ignore newly introduced complex Quandl package version 3.]
2016-02-23  [Quandl.py API version 2.8.9 removes push() to upload data.]
2015-08-03  Quandl.py API version 2.8.7 adopted as yi_quandl_api.py
                in fecon235, unchanged and operative through
                2018-03-12, v5.18.0312, https://git.io/fecon235
'''

from __future__ import (print_function, division, absolute_import,
                        unicode_literals)
import pickle
import datetime
import json
import pandas as pd
import re
from dateutil import parser

try:
    from urllib.error import HTTPError  # Python 3
    from urllib.parse import urlencode
    from urllib.request import Request, urlopen
    strings = str
except ImportError:
    from urllib import urlencode  # Python 2
    from urllib2 import HTTPError, Request, urlopen
    strings = unicode


# Base API call URL
QUANDL_API_URL = 'https://www.quandl.com/api/v1/'
VERSION = '2.8.7'
#         ^2.8.9 removed push(), but failed to update VERSION variable.


def get(dataset, **kwargs):
    """Return dataframe of requested dataset from Quandl.

    :param dataset: str or list, depending on single or multiset dataset usage
            Dataset codes are available on the Quandl website
    :param str authtoken: Downloads are limited to 10 unless token is specified
    :param str trim_start, trim_end: Optional datefilers, otherwise entire
           dataset is returned
    :param str collapse: Options are daily, weekly, monthly, quarterly, annual
    :param str transformation: options are diff, rdiff, cumul, and normalize
    :param int rows: Number of rows which will be returned
    :param str sort_order: options are asc, desc. Default: `asc`
    :param str returns: specify what format you wish your dataset returned as,
        either `numpy` for a numpy ndarray or `pandas`. Default: `pandas`
    :param bool verbose: print output text to stdout? Default is False.
    :param str text: Deprecated. Use `verbose` instead.
    :returns: :class:`pandas.DataFrame` or :class:`numpy.ndarray`

    Note that Pandas expects timeseries data to be sorted ascending for most
    timeseries functionality to work.

    Any other `kwargs` passed to `get` are sent as field/value params to Quandl
    with no interference.

    """
    # Check whether dataset is given as a string (for a single dataset)
    # or an array (for a multiset call)

    # Unicode String
    if type(dataset) == strings or type(dataset) == str:

        if '.' in dataset:
            dataset_temp = dataset.split('.')
            dataset = dataset_temp[0]
            dataset_columns = dataset_temp[1]
            kwargs.update({'column': dataset_columns})

        url = QUANDL_API_URL + 'datasets/{}.csv?'.format(dataset)

    # Array
    elif type(dataset) == list:
        multiple_dataset_dataframe = pd.DataFrame()
        for i in dataset:
            try:
                d = get(i, **kwargs)
            except DatasetNotFound:
                d = pd.DataFrame({'NOT FOUND': []})

            # format dataset name for column name
            specific_column_name = i.split('.')[0].replace('/', '.')
            d.rename(columns=lambda x: specific_column_name + ' - ' + x,
                     inplace=True)
            multiple_dataset_dataframe = pd.merge(multiple_dataset_dataframe,
                                                  d, right_index=True,
                                                  left_index=True,
                                                  how='outer')
        return multiple_dataset_dataframe

    # If wrong format
    else:
        error = "Dataset must be specified as a string of Quandl code(s)."
        raise WrongFormat(error)
    # parse parameters
    kwargs.setdefault('sort_order', 'asc')
    verbose = kwargs.get('verbose', False)
    if 'text' in kwargs:
        print('Deprecated: "text", use "verbose" instead.')
        if isinstance(kwargs['text'], (strings, str)):
            if kwargs['text'].lower() in ['yes', 'y', 't', 'true', 'on']:
                verbose = True
        else:
            verbose = bool(kwargs['text'])
    auth_token = _getauthtoken(kwargs.pop('authtoken', ''), verbose)
    trim_start = _parse_dates(kwargs.pop('trim_start', None))
    trim_end = _parse_dates(kwargs.pop('trim_end', None))
    returns = kwargs.get('returns', 'pandas')
    # Append all parameters to API call
    url = _append_query_fields(url,
                               auth_token=auth_token,
                               trim_start=trim_start,
                               trim_end=trim_end,
                               **kwargs)
    if returns == 'url':
        return url      # for test purpose
    try:
        urldata = _download(url)
        if verbose and verbose != 'no':
            print("Returning Dataframe for ", dataset)

    # Error catching
    except HTTPError as e:
        # API limit reached
        if str(e) == 'HTTP Error 403: Forbidden':
            error = 'API daily call limit exceeded.'
            raise CallLimitExceeded(error)

        # Dataset not found
        elif str(e) == 'HTTP Error 404: Not Found':
            error = "Dataset not found. Check {} for errors".format(dataset)
            raise DatasetNotFound(error)

        # Catch all
        else:
            if verbose and verbose != 'no':
                print("url:", url)
            error = "Error Downloading! {}".format(e)
            raise ErrorDownloading(error)

    if returns == 'numpy':
        return urldata.to_records()

    return urldata


def search(query, source=None, page=1, authtoken=None,
           verbose=True, prints=None):
    """Return array of dictionaries of search results.
    :param str query: (required), query to search with
    :param str source: (optional), source to search
    :param +'ve int: (optional), page number of search
    :param str authotoken: (optional) Quandl auth token for extended API access
    :returns: :array: search results
    """
    if prints is not None:
        print('Deprecated: "prints", use "verbose" instead.')
        verbose = prints
    token = _getauthtoken(authtoken, verbose)
    search_url = QUANDL_API_URL
    search_url += '/datasets.json?request_source=python&request_version='
    search_url += VERSION + '&query='
    # parse query for proper API submission
    parsedquery = re.sub(" ", "+", query)
    parsedquery = re.sub("&", "+", parsedquery)
    url = search_url + parsedquery
    # Use authtoken if present
    if token:
        url += '&auth_token=' + token
    # Add search source if given
    if source:
        url += '&source_code=' + source
    # Page to be searched
    url += '&page=' + str(page)
    text = urlopen(url).read().decode("utf-8")
    data = json.loads(text)
    try:
        datasets = data['docs']
    except TypeError:
        raise TypeError("There are no matches for this search")
    datalist = []
    for i in range(len(datasets)):
        temp_dict = {}
        temp_dict['name'] = datasets[i]['name']
        temp_dict['code'] = datasets[i]['source_code'] + '/' + datasets[i]['code']  # noqa
        temp_dict['desc'] = datasets[i]['description']
        temp_dict['freq'] = datasets[i]['frequency']
        temp_dict['colname'] = datasets[i]['column_names']
        datalist.append(temp_dict)
        if verbose and i < 4:
            print('{0:20}       :        {1:50}'.format('Name', temp_dict['name']))  # noqa
            print('{0:20}       :        {1:50}'.format('Quandl Code', temp_dict['code']))  # noqa
            print('{0:20}       :        {1:50}'.format('Description', temp_dict['desc']))  # noqa
            print('{0:20}       :        {1:50}'.format('Frequency', temp_dict['freq']))  # noqa
            print('{0:20}       :        {1:50}'.format('Column Names', str(temp_dict['colname'])))  # noqa
            print('\n\n')
    return datalist


# format date, if None returns None
def _parse_dates(date):
    if date is None:
        return date
    if isinstance(date, datetime.datetime):
        return date.date().isoformat()
    if isinstance(date, datetime.date):
        return date.isoformat()
    try:
        date = parser.parse(date)
    except ValueError:
        raise ValueError("{} is not recognised a date.".format(date))
    return date.date().isoformat()


# Download data into pandas dataframe
def _download(url):
    dframe = pd.read_csv(url, index_col=0, parse_dates=True)
    return dframe


# Push data to Quandl. Returns json of HTTP push.
def _htmlpush(url, raw_params):
    page = url
    params = urlencode(raw_params)
    request = Request(page, params)
    page = urlopen(request)
    return json.loads(page.read())


# Test if code is capitalized alphanumeric
def _pushcodetest(code):
    regex = re.compile('[^0-9A-Z_]')
    if regex.search(code):
        error = ("Your Quandl Code for uploaded data must consist of only "
                 "capital letters, underscores and numbers.")
        raise CodeFormatError(error)
    return code


def _getauthtoken(token, text):
    """Return and save API token to a pickle file for reuse."""
    try:
        savedtoken = pickle.load(open('authtoken.p', 'rb'))
    except IOError:
        savedtoken = False
    if token:
        try:
            pickle.dump(token, open('authtoken.p', 'wb'))
            if text == "no" or text is False:
                pass
            else:
                print("Token {} activated and saved for later.".format(token))
        except Exception as e:
            print("Error writing token to cache: {}".format(str(e)))

    elif not savedtoken and not token:
            if text == "no" or text is False:
                pass
            else:
                print("No authentication tokens found: usage will be limited.")
                print("See www.quandl.com/api for more information.")
    elif savedtoken and not token:
        token = savedtoken
        if text == "no" or text is False:
            pass
        else:
            print("Using cached token {} for authentication.".format(token))
    return token


# In lieu of urllib's urlencode, as this handles None values by ignoring them.
def _append_query_fields(url, **kwargs):
    field_values = ['{0}={1}'.format(key, val)
                    for key, val in kwargs.items() if val]
    surl = url + 'request_source=python&request_version='
    return surl + VERSION + '&' + '&'.join(field_values)


# Setup custom Exceptions


class WrongFormat(Exception):
    """Exception for dataset formatting errors"""
    pass


class MultisetLimit(Exception):
    """Exception for calls exceeding the multiset limit"""
    pass


class ParsingError(Exception):
    """Exception for I/O parsing errors"""
    pass


class CallLimitExceeded(Exception):
    """Exception for daily call limit being exceeded"""
    pass


class DatasetNotFound(Exception):
    """Exception for the dataset not being found"""
    pass


class ErrorDownloading(Exception):
    """Catch all exception for download errors"""
    pass


class MissingToken(Exception):
    """Exception when API token needed but missing"""
    pass


class DateNotRecognized(Exception):
    """Exception when a date is not recognized as such"""
    pass


class CodeFormatError(Exception):
    """Exception when a Quandl code is not formatted properly"""
    pass
