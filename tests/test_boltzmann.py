#  Python Module for import                           Date : 2018-06-21
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_boltzmann :: Test fecon236 prtf.boltzmann module

Doctests display at lower precision since equality test becomes fuzzy across
different systems if full floating point representation is used.

We favor pytest over nosetests, so e.g. $ py.test --doctest-modules

REFERENCE
   pytest:  https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-21  fecon236 fork. Fix imports. Change doctests to assert form.
2017-07-09  fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import pytest
import numpy as np
from fecon236.util import system
from fecon236.util import group
from fecon236.prtf import boltzmann as boltz


#  Sample covariance matrix (but we will not use np matrix class) via:
#      >>> prices = group.groupget(group.world4d, maxi=5650)
#       ::  Retrieved from Google Finance: SPY
#       ::  Retrieved from Google Finance: EEM
#       ::  Retrieved from Google Finance: EZU
#       ::  Retrieved from Google Finance: GLD
#       ::  Retrieved from Google Finance: EWJ
#      >>> V = matrix.covdiflog(prices['2011-01-01':'2017-06-26'], lags=1)
V = np.array([[8.48312099e-05,   1.02917158e-04,   1.13943470e-04,
               -2.79505009e-06,   7.46173310e-05],
              [1.02917158e-04,   1.87393335e-04,   1.63235156e-04,
               1.80039246e-05,   1.06210719e-04],
              [1.13943470e-04,   1.63235156e-04,   2.26817214e-04,
               8.18776853e-06,   1.15561266e-04],
              [-2.79505009e-06,   1.80039246e-05,   8.18776853e-06,
               1.13760941e-04,  -2.73835320e-08],
              [7.46173310e-05,   1.06210719e-04,   1.15561266e-04,
               -2.73835320e-08,   1.34652717e-04]])


#  Correlation matrix derived by cov2cor(V), but tested elsewhere:
corr = np.array([[1., 0.82, 0.82, -0.03, 0.7],
                 [0.82, 1., 0.79,  0.12, 0.67],
                 [0.82, 0.79, 1.,  0.05, 0.66],
                 [-0.03, 0.12, 0.05,  1.,  0.],
                 [0.7,  0.67, 0.66,  0.,  1.]])


#  Sample weights from a Global Minimum Variance Portfolio:
globalw = np.array([[0.87034542],
                    [-0.2267291],
                    [-0.19612603],
                    [0.40540278],
                    [0.14710693]])


def test_boltzmann_fecon236_weighcov():
    '''Check whether weighcov() function produces global weights.'''
    assert np.allclose(boltz.weighcov(V), globalw)


def test_boltzmann_fecon236_weighcov_LESSON():
    '''Check weighcov() function using related, but wrong, input.
       Only for testing purposes, we input the correlation matrix instead
       of the covariance matrix V which officially should be the argument.
       LESSON: weighcov(corr) != weighcov(V)
            i.e. global weights CANNOT be computed from correlation,
            we need the messy numbers from the covariance matrix.
            (Compare globalw above with globalw_corr here.)
    '''
    globalw_corr = boltz.weighcov(corr)
    gotx = np.round(globalw_corr, 2)
    wantx = np.array([[0.26], [-0.06], [0.1], [0.46], [0.24]])
    assert np.allclose(gotx, wantx)


def test_boltzmann_fecon236_trimit():
    '''Check trimit() function.'''
    weights = boltz.trimit(globalw, floor=0.01, level=0)
    gotx = np.round(weights, 4)
    wantx = np.array([[0.8703], [0.], [0.], [0.4054], [0.1471]])
    assert np.allclose(gotx, wantx)


def test_boltzmann_fecon236_rentrim():
    '''Check rentrim() function, but also renormalize() indirectly.'''
    weights = boltz.rentrim(globalw, floor=0.01, level=0)
    gotx = np.round(weights, 4)
    wantx = np.array([[0.6117], [0.], [0.], [0.2849], [0.1034]])
    assert np.allclose(gotx, wantx)


#  #  This is fragile due to disruption of equities data,
#  #  and replication of :: messages, which could be from Yahoo or Google.
#  @pytest.mark.xfail
#  def test_boltzmann_fecon236_boltzportfolio_DOCTEST_vSlow():
#      '''Check weighcov() indirectly through boltzportfolio() function.
#         ___ATTN___ Very Slow test due to data download, and
#         could fail years later due to data vendor; esp. check maxi and dates.
#      >>> prices = group.groupget(group.world4d, maxi=5650)
#       ::  Retrieved from Google Finance: SPY
#       ::  Retrieved from Google Finance: EEM
#       ::  Retrieved from Google Finance: EZU
#       ::  Retrieved from Google Finance: GLD
#       ::  Retrieved from Google Finance: EWJ
#      >>> prtf = boltz.boltzportfolio(prices['2011-01-01':'2017-06-26'], yearly=256, temp=55, floor=0.01, level=0, n=2)
#      >>> prtf
#      [8.59, [[0.95, 9.16, 'America'], [0.0, -4.96, 'Emerging'], [0.0, -1.41, 'Europe'], [0.03, -4.09, 'Gold'], [0.02, 1.33, 'Japan']]]
#      '''
#      pass


#  This is fragile due to disruption of equities data...
#  same as previously successful test, except use assert instead of doctest.
@pytest.mark.xfail
def test_boltzmann_fecon236_boltzportfolio_PYTEST_vSlow():
    '''Check weighcov() indirectly through boltzportfolio() function.
       ___ATTN___ Very Slow test due to data download, and
       could fail years later due to data vendor; esp. check maxi and dates.
    '''
    prices = group.groupget(group.world4d, maxi=5650)
    gotx = boltz.boltzportfolio(prices['2011-01-01':'2017-06-26'],
                                yearly=256, temp=55, floor=0.01, level=0, n=2)
    wantx = [8.59, [[0.95, 9.16, 'America'], [0.0, -4.96, 'Emerging'],
             [0.0, -1.41, 'Europe'], [0.03, -4.09, 'Gold'],
             [0.02, 1.33, 'Japan']]]
    #  We can use == to assert for lists, so no need for np.allclose() here:
    assert gotx == wantx


if __name__ == "__main__":
    system.endmodule()
