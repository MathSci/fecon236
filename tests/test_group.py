#  Python Module for import                           Date : 2018-06-19
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_group.py :: Test fecon236 util.group module

- This module originally tested the varied fecon235.py top module, so some
    tests are due for a spin-off to other modules.

We also favor pytest over nosetests, so e.g.

    $ py.test --doctest-modules [optional dir/file argument]

Mark very slow tests with "vSlow" suffix, so

    $ py.test -k 'not vSlow'  # Excludes such tests.

REFERENCE:
pytest:  https://pytest.org/latest/getting-started.html
         or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-18  test_group.py, fecon236 fork. Pass flake8.
                Tests due for a spin-off are commented out.
2018-03-10  test_fecon235.py, v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.util import group
from fecon236.host import fred


def test_group_fecon236_groupget_groupgeoret_vSlow():
    '''Test groupget(), followed by groupgeoret() which depends on georet().'''
    fxdic = {'EURUSD': fred.d4eurusd, 'USDJPY': fred.d4usdjpy}
    fxdf = group.groupget(fxdic)
    y, z = group.groupgeoret(fxdf['2010':'2015'], 256)
    assert y == [4.19, 4.63, 9.3, 256, 1565,
                 '2010-01-01', '2015-12-31', 'USDJPY']
    assert z == [-4.54, -4.08, 9.64, 256, 1565,
                 '2010-01-01', '2015-12-31', 'EURUSD']


if __name__ == "__main__":
    system.endmodule()
