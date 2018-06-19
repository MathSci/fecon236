#  Python Module for import                           Date : 2018-06-19
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_hostess.py :: Test fecon236 host.hostess module

We favor pytest over nosetests, so e.g.

    $ py.test --doctest-modules [optional dir/file argument]

Mark very slow tests with "vSlow" suffix, so

    $ py.test -k 'not vSlow'  # Excludes such tests.

Mark tests requiring authentication with "oLocal" suffix
denoting Only Local testing, e.g. Quandl access.


REFERENCE:
pytest:  https://pytest.org/latest/getting-started.html
         or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-19  Spin-off from test_group.py.
'''

from __future__ import absolute_import, print_function, division

import pytest
from fecon236 import tool
from fecon236.util import system
from fecon236.host.hostess import get   # noqa
from fecon236.host import fred          # noqa
from fecon236.host import qdl           # noqa


def test_group_fecon236_GET_d4xau_from_FRED_vSlow():
    '''Test get() which uses getfred() in the fred module.
       Here we get London PM Gold quotes from the FRED database.
    >>> xau = get(fred.d4xau)
    >>> xau['2015-07-21':'2015-07-28']
                     Y
    T                 
    2015-07-21  1105.6
    2015-07-22  1088.6
    2015-07-23  1097.4
    2015-07-24  1080.8
    2015-07-27  1100.0
    2015-07-28  1096.2
    '''
    pass


def test_group_fecon236_GET_d7xbtusd_from_QUANDL_vSlow_oLocal():
    '''Test get() which uses getqdl() in qdl module.
       Here we get a Bitcoin price from Quandl.
    '''
    xbt = get(qdl.d7xbtusd)
    assert tool.tailvalue(xbt[:'2018-06-14']) == 6315.7


#  FAIL 2018-06-19. Quandl is operational, so the problem is w4cotr* series.
@pytest.mark.xfail
def test_group_fecon236_GET_w4cotr_metals_from_QUANDL_vSlow_oLocal():
    '''Test get() which uses getqdl() in qdl module.
       Here we get the CFTC Commitment of Traders Reports
       for gold and silver expressed as our position indicator.
    >>> print(qdl.w4cotr_metals)
    w4cotr_metals
    '''
    metals = get(qdl.w4cotr_metals)
    assert round(tool.tailvalue(metals[:'2015-07-28']), 3) == 0.461


if __name__ == "__main__":
    system.endmodule()
