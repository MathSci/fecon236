#  Python Module for import                           Date : 2018-07-08
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_tool.py :: Test fecon236 tool module.

Using an offline CSV file, we construct and test two dataframes:
xau and foo, then paste(), and test lagdf().

We use pytest, so for example,
    $ py.test --doctest-modules

Re pytest:  https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-07-08  Add test for std().
2018-05-18  fecon236 fork. Pass flake8.
2016-04-18  fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
import pandas as pd
from os import sep
from fecon236 import tool
from fecon236.util import system
from fecon236.host import fred
#
#  In the tests directory without __init__.py,
#  use absolute import, as if outside the fecon236 package,
#  not relative import.


#  #  Show the CSV file zdata-xau-13hj-c30.csv:
#  #                    ^created in Linux environment...
#
#       T,XAU
#       2013-03-08,1581.75
#       2013-03-11,1579.0
#       2013-03-12,1594.0
#       2013-03-13,1589.25
#       2013-03-14,1586.0
#       2013-03-15,1595.5
#       2013-03-18,1603.75
#       2013-03-19,1610.75
#       2013-03-20,1607.5
#       2013-03-21,1613.75
#       2013-03-22,1607.75
#       2013-03-25,1599.25
#       2013-03-26,1598.0
#       2013-03-27,1603.0
#       2013-03-28,1598.25
#       2013-03-29,1598.25
#       2013-04-01,1598.25
#       2013-04-02,1583.5
#       2013-04-03,1574.75
#       2013-04-04,1546.5
#       2013-04-05,1568.0
#       2013-04-08,1575.0
#       2013-04-09,1577.25
#       2013-04-10,1575.0
#       2013-04-11,1565.0
#       2013-04-12,1535.5
#       2013-04-15,1395.0
#       2013-04-16,1380.0
#       2013-04-17,1392.0
#       2013-04-18,1393.75


def test_tool_fecon236_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('tests' + sep + 'zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [col for col in df.columns] == ['Y']
    assert df.shape == (30, 1)
    return df


xau = test_tool_fecon236_Read_CSV_file()
xau = tool.todf(xau, 'XAU')
#          todf used to rename column.


def test_tool_fecon236_check_xau_DataFrame():
    '''Check xau dataframe.'''
    assert [col for col in xau.columns] == ['XAU']
    assert tool.tailvalue(xau) == 1393.75


foo = tool.todf(xau + 5000.00, 'FOO')


def test_tool_fecon236_check_foo_DataFrame():
    '''Check foo dataframe which is just xau + 5000.00 increase.'''
    assert [col for col in foo.columns] == ['FOO']
    assert tool.tailvalue(foo) == 6393.75


xaufoo = tool.paste([xau, foo])


def test_tool_fecon236_paste_function():
    '''Test xau and foo pasted together as xaufoo dataframe.'''
    assert [col for col in xaufoo.columns] == ['XAU', 'FOO']
    assert xaufoo.shape == (30, 2)
    assert tool.tailvalue(xaufoo, pos=0) == 1393.75
    assert tool.tailvalue(xaufoo, pos=1) == 6393.75
    assert xaufoo.index[0] == pd.Timestamp('2013-03-08 00:00:00')
    assert xaufoo.index[-1] == pd.Timestamp('2013-04-18 00:00:00')
    #                             Timestamp is yet another pandas type.
    #                             Default time is midnight.


xaufoolag = tool.lagdf(xaufoo, lags=3)


def test_tool_fecon236_lagdf_function():
    '''Test xaufoolag dataframe created by lagdf on xaufoo with lags=3.'''
    assert [col for col in xaufoolag.columns] == ['XAU_0', 'FOO_0',
            'XAU_1', 'FOO_1', 'XAU_2', 'FOO_2', 'XAU_3', 'FOO_3']  # noqa
    #  Number after underscore indicates lag.
    assert xaufoolag.shape == (27, 8)
    #                lags will introduce NaN, which are then dropped,
    #                so rows are reduced from 30 to 27.
    #
    #  Making sure LAGGED VALUES are correctly placed...
    assert tool.tailvalue(xaufoolag, pos=0, row=1) == 1393.75
    assert tool.tailvalue(xaufoolag, pos=1, row=1) == 6393.75
    assert tool.tailvalue(xaufoolag, pos=2, row=1) == 1392.0
    assert tool.tailvalue(xaufoolag, pos=3, row=1) == 6392.0
    assert tool.tailvalue(xaufoolag, pos=4, row=1) == 1380.0
    assert tool.tailvalue(xaufoolag, pos=5, row=1) == 6380.0
    assert tool.tailvalue(xaufoolag, pos=6, row=1) == 1395.0
    assert tool.tailvalue(xaufoolag, pos=7, row=1) == 6395.0

    assert tool.tailvalue(xaufoolag, pos=0, row=2) == 1392.0
    assert tool.tailvalue(xaufoolag, pos=1, row=2) == 6392.0
    assert tool.tailvalue(xaufoolag, pos=2, row=2) == 1380.0
    assert tool.tailvalue(xaufoolag, pos=3, row=2) == 6380.0
    assert tool.tailvalue(xaufoolag, pos=4, row=2) == 1395.0
    assert tool.tailvalue(xaufoolag, pos=5, row=2) == 6395.0

    assert tool.tailvalue(xaufoolag, pos=0, row=3) == 1380.0
    assert tool.tailvalue(xaufoolag, pos=1, row=3) == 6380.0
    assert tool.tailvalue(xaufoolag, pos=2, row=3) == 1395.0
    assert tool.tailvalue(xaufoolag, pos=3, row=3) == 6395.0

    assert tool.tailvalue(xaufoolag, pos=0, row=4) == 1395.0
    assert tool.tailvalue(xaufoolag, pos=1, row=4) == 6395.0

    assert xaufoolag.index[0] == pd.Timestamp('2013-03-13 00:00:00')
    assert xaufoolag.index[-1] == pd.Timestamp('2013-04-18 00:00:00')
    #                                Timestamp is yet another pandas type.
    #                                Default time is midnight.


def test_tool_fecon236_std():
    '''Test standard deviation on population arg and data formats.'''
    #  tool.std() should work for both numpy array and pandas DataFrame.
    darr = np.array([0, 1])
    data = tool.todf(darr)
    assert round(tool.std(darr, population=True), 3) == 0.500
    assert round(tool.std(data, population=True), 3) == 0.500
    #  When sample size is small, the difference is huge!
    assert round(tool.std(darr, population=False), 3) == 0.707
    assert round(tool.std(data, population=False), 3) == 0.707


if __name__ == "__main__":
    system.endmodule()
