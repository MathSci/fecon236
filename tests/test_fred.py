#  Python Module for import                           Date : 2018-05-12
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_fred.py :: Test fecon236 fred module.

- Include test of index_delta_secs()
- Indirect test of resample_main() via rewritten functions:
    daily(), monthly(), and quarterly().

Testing: We favor pytest over nosetests, so e.g.
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-05-12  Specify directory of zdata.
2018-05-10  fecon236 fork. Pass flake8.
2016-11-06  fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from os import sep
from fecon236 import tool
from fecon236.util import system
from fecon236.host import fred
#
#  N.B. -  In this tests directory without __init__.py,
#          we use absolute import as if outside the fecon236 package,
#          not relative import.

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


def test_fred_fecon236_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('tests' + sep + 'zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [col for col in df.columns] == ['Y']
    assert df.shape == (30, 1)
    return df


xau = test_fred_fecon236_Read_CSV_file()
xau = tool.todf(xau, 'XAU')
#          todf used to rename column.


def test_fred_fecon236_check_xau_DataFrame():
    '''Check xau dataframe.'''
    assert [col for col in xau.columns] == ['XAU']
    assert tool.tailvalue(xau) == 1393.75


def test_fred_fecon236_check_xau_frequency():
    '''Check xau dataframe frequency.'''
    assert fred.index_delta_secs(xau) == 86400.0
    #      Expect min daily frequency in seconds.


def test_fred_fecon236_check_xau_resample_main():
    '''Check daily xau converted by monthly(), then daily().
       Demonstrates downsampling, then upsampling --
       thus validating fred.resample_main().
       Check dates produced from quarterly().
    >>> xaumon = fred.monthly(xau)
    >>> xaumon
                    XAU
    T                  
    2013-03-01  1598.25
    2013-04-01  1566.50
    >>> xaumondaily = fred.daily(xaumon)
    >>> xaumondaily = xaumondaily.round(2)  # for sys independence.
    >>> xaumondaily  # expect linear interpolation.
                    XAU
    T                  
    2013-03-01  1598.25
    2013-03-04  1596.74
    2013-03-05  1595.23
    2013-03-06  1593.71
    2013-03-07  1592.20
    2013-03-08  1590.69
    2013-03-11  1589.18
    2013-03-12  1587.67
    2013-03-13  1586.15
    2013-03-14  1584.64
    2013-03-15  1583.13
    2013-03-18  1581.62
    2013-03-19  1580.11
    2013-03-20  1578.60
    2013-03-21  1577.08
    2013-03-22  1575.57
    2013-03-25  1574.06
    2013-03-26  1572.55
    2013-03-27  1571.04
    2013-03-28  1569.52
    2013-03-29  1568.01
    2013-04-01  1566.50
    >>> xauq = fred.quarterly(xau)
    >>> xauq  # verify if dates are quarterly.
                    XAU
    T                  
    2013-01-01  1598.25
    2013-04-01  1566.50
    '''
    pass


if __name__ == "__main__":
    system.endmodule()
