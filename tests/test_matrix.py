#  Python Module for import                           Date : 2018-06-12
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_matrix.py :: Test fecon236 matrix module

Doctests display at lower precision since equality test becomes fuzzy across
different systems if full floating point representation is used.

Testing: We favor pytest over nosetests, so e.g. $ py.test --doctest-modules

REFERENCE
- pytest, https://pytest.org/latest/getting-started.html


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-12  fecon236 fork. Fix imports, pass flake8.
2017-06-19  fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from fecon236.util import system
from fecon236.math import matrix

#   A is non-singular, hence invertible:
A = np.array([[7, 2, 1],
              [0, 3, -1],
              [-3, 4, -2]])

#   First column of Abad is thrice the second column.
Abad = np.array([[6, 2, 1],
                 [9, 3, -1],
                 [12, 4, -2]])

#   Aiv is, in fact, A inverted.
Aiv = np.array([[-2, 8, -5],
                [3, -11, 7],
                [9, -34, 21]])

#  V is a covariance array:
V = np.array([[1875.3209,  429.8712,  462.4775],
              [429.8712,  1306.9817, -262.8231],
              [462.4775,  -262.8231,  755.5193]])


def test_matrix_fecon236_is_singular():
    '''Check if matrix is singular.'''
    assert matrix.is_singular(A) is False
    assert matrix.is_singular(Abad) is True


def test_matrix_fecon236_check_example_matrics():
    '''Multiply A by Aiv should return the identity matrix.
    >>> A.dot(Aiv)
    array([[1, 0, 0],
           [0, 1, 0],
           [0, 0, 1]])
    '''
    assert np.allclose(A.dot(Aiv), np.identity(3))


def test_matrix_fecon236_invert_caution():
    '''Compute inverse using numpy inv() should return float of Aiv.
    >>> matrix.invert_caution(A)
    array([[ -2.,   8.,  -5.],
           [  3., -11.,   7.],
           [  9., -34.,  21.]])
    '''
    assert np.allclose(matrix.invert_caution(A), Aiv)


def test_matrix_fecon236_invert_pseudo():
    '''Compute inverse using numpy pinv() should return float of Aiv.
    >>> matrix.invert_pseudo(A)
    array([[ -2.,   8.,  -5.],
           [  3., -11.,   7.],
           [  9., -34.,  21.]])
    '''
    assert np.allclose(matrix.invert_pseudo(A), Aiv)


def test_matrix_fecon236_Abad_invert():
    '''Compute inverse using invert() with singular Abad.
       Pseudo-inverse will handle ILL-CONDITION with NONSENSE.
    >>> np.round(matrix.invert(Abad), 5)
    array([[ 0.06774,  0.02903,  0.01935],
           [ 0.02258,  0.00968,  0.00645],
           [ 0.50538, -0.02151, -0.23656]])
    '''
    pass


def test_matrix_fecon236_cov2cor():
    '''Compute correlation array given covariance array.
    >>> matrix.cov2cor(V, n=6)
    array([[ 1.      ,  0.274578,  0.388535],
           [ 0.274578,  1.      , -0.264488],
           [ 0.388535, -0.264488,  1.      ]])
    '''
    #  R test: http://rfunction.com/archives/851
    pass


if __name__ == "__main__":
    system.endmodule()
