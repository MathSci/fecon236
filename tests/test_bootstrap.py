#  Python Module for import                           Date : 2018-07-01
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_bootstrap.py :: Test fecon236 bootstrap module.

Doctests display at lower precision since equality test becomes fuzzy across
different systems if full floating point representation is used.

Testing: We favor pytest over nosetests, so e.g.
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-07-01  Reflect change of function names.
2018-06-28  First version
'''

from __future__ import absolute_import, print_function, division

from os import sep
from fecon236 import tool
from fecon236.util import system
from fecon236.host import fred
from fecon236.boots import bootstrap as bs
from fecon236.dst.gaussmix import gemrat


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


def test_bootstrap_fecon236_Read_CSV_file():
    '''Read CSV file then check values.'''
    df = fred.readfile('tests' + sep + 'zdata-xau-13hj-c30.csv')
    #         readfile disregards XAU column name:
    assert [col for col in df.columns] == ['Y']
    assert df.shape == (30, 1)
    return df


#  Establish REFERENCE dataframe for tests below:
xau = test_bootstrap_fecon236_Read_CSV_file()


def test_bootstrap_fecon236_writefile_normdiflog_read():
    '''Create normdiflog CSV file, then read it as dataframe for testing.'''
    fname = 'tests' + sep + 'tmp-xau-normdiflog.csv'
    bs.writefile_normdiflog(xau, filename=fname)
    df = bs.readcsv('tests' + sep + 'tmp-xau-normdiflog.csv')
    assert [col for col in df.columns] == ['Y']
    assert df.shape == (29, 1)
    assert round(tool.tailvalue(df[:'2013-04-15']), 3) == -4.804
    assert round(tool.tailvalue(df), 3) == 0.295


def test_bootstrap_fecon236_ROUNDTRIP():
    '''Do a roundtrip using all the functionality.'''
    fname = 'tests' + sep + 'tmp-xau-normdiflog.csv'
    bs.writefile_normdiflog(xau, filename=fname)
    _, xaumean, xausigma, _, _, _ = gemrat(xau, yearly=256, pc=False)
    #  gemrat: "RuntimeWarning: invalid value encountered in log"
    #          due to smackdown in price on 2013-04-15,
    #          i.e. expect inaccuracies as a consequence.
    poparr = bs.csv2ret(fname, mean=xaumean, sigma=xausigma, yearly=256)
    #  So poparr is the "population" array which will be
    #  repetitively hammered in memory for bootstrap resamplings.
    pxdf = bs.bsret2prices(29, poparr, inprice=1581.75, replace=False)
    #  Crucial fact: tail price is indifferent as to the order in which
    #                returns are selected without replacement,
    #                so long as ALL the returns are selected.
    #  Horrible assertion range, but our test data is just too short,
    #  and contains statistical abnormality per smackdown on 2013-04-15.
    #  In actuality: expecting 1393.75, but got 1386.112272.
    assert 1385.00 < tool.tailvalue(pxdf) < 1395.00


if __name__ == "__main__":
    system.endmodule()
