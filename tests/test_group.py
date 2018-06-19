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


#  def test_group_fecon236_FORECAST_m4xau_from_FRED_vSlow():
#      '''Test forecast() in fecon which uses Holt-Winters method.
#         Values for alpha and beta are somewhat optimized by moderate grids:
#             alpha, beta, losspc, loss: [0.9167, 0.125, 2.486, 28.45]
#         We use monthly gold data, and type forecast as integers
#         to avoid doctest with floats (almost equal problem).
#      >>> xau = get(m4xau)
#      >>> xaufc = forecast(xau['2005-07-28':'2015-07-28'], h=6, grids=25)
#      >>> xaufc.astype('int')
#         Forecast
#      0      1144
#      1      1135
#      2      1123
#      3      1112
#      4      1100
#      5      1089
#      6      1078
#      '''
#      pass


#  def test_group_fecon236_foreholt_m4xau_from_FRED_vSlow():
#      '''Test foreholt() in fecon236 which uses Holt-Winters method.
#         Default values for alpha and beta are assumed.
#         We use monthly gold data, and type forecast as integers
#         to avoid doctest with floats (almost equal problem).
#      >>> xau = get(m4xau)
#      >>> xaufh = foreholt(xau['2005-07-28':'2015-07-28'], h=6)
#      >>> xaufh.astype('int')
#         Forecast
#      0      1144
#      1      1161
#      2      1154
#      3      1146
#      4      1138
#      5      1130
#      6      1122
#      '''
#      pass


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
