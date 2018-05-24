#  Python Module for import                           Date : 2018-05-22
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_qdl.py :: Test fecon236 qdl module for Quandl.

- Implicit test of _ex_Quandl.py imported by qdl module.
- Test online data retrieval of Bitcoin prices.

Testing: We favor pytest over nosetests, so e.g.
    $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-05-23  Mark download test function with "oLocal".
2018-05-22  First version.
'''

from __future__ import absolute_import, print_function, division

from fecon236 import tool
from fecon236.util import system
from fecon236.host import qdl
#
#  In this tests directory without __init__.py, we use absolute import,
#  as if outside the fecon236 package, not relative import.


def test_qdl_fecon236_Check_variable_assignment():
    '''Check on variable assignment.'''
    #  Trivial test just for non-local testing.
    assert qdl.d7xbtusd == 'BCHAIN/MKPRU'
    return


def test_qdl_fecon236_Check_xbt_prices_vSlow_oLocal():
    '''Check on xbt prices on various dates, only Local.'''
    #  Download Bitcoin prices from Quandl:
    xbt = qdl.getqdl(qdl.d7xbtusd)
    xbt = tool.todf(xbt, 'XBT')
    #          todf used to rename column.
    assert abs(tool.tailvalue(xbt[:'2014-02-01']) - 815.99) < 0.1
    assert abs(tool.tailvalue(xbt[:'2015-02-01']) - 220.72) < 0.1
    assert abs(tool.tailvalue(xbt[:'2016-02-01']) - 376.86) < 0.1
    #
    #  Q: Why only Local, i.e. oLocal?
    #
    #  Without revealing one's private authtoken.p,
    #  all Travis CI machines sharing an IP address
    #  will be considered one anonymous user, thus
    #  the limited calls to Quandl will be jointly exceeded,
    #  resulting in "HTTP Error 429: Too Many Requests".
    #  And the Travis job will fail for Quandl's server policy
    #  reasons, not the validity of the code.
    return


if __name__ == "__main__":
    system.endmodule()
