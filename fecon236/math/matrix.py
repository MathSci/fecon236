#  Python Module for import                           Date : 2018-06-16
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
"""Linear algebra

Usage
-----
To easily invert a matrix, use ``invert`` which includes testing
for ill-conditioned matrix and fallback to computing the Moore-Penrose
pseudo-inverse.

Notes
-----
For LATEST version, see https://git.io/fecon236

For numpy work, we want to DISCOURAGE the use of ``np.matrix``,
which is a subclass of ``np.ndarray``, since their
interoperations may produce unexpected results.

- The ``np.matrix`` subclass is confined to 2-D matrices.
- Sticking with array constructs:
  Operator ``*`` means element-wise multiplication.
  For MATRIX MULTIPLICATION, using ``.dot`` is BEST,
  since operator ``@`` originates from Python 3.5.
- For our arguments, ``mat`` is mathematically a matrix,
  but not necessarily designed for subclass ``np.matrix``.
- We explicitly AVOID ``np.matrix.I`` to calculate inverse.
- We will ASSUME matrices are of TYPE ``np.ndarray``.

Tests
-----
See ``tests/test_matrix.py``, esp. for output examples.

References
----------

- numpy, https://docs.scipy.org/doc/numpy-dev/user/quickstart.html
- Gilbert Strang, 1980, Linear Algebra and Its Applications, 2nd ed.
- Gene H. Golub, 1989, Matrix Computations, 2nd. ed.

Change Log
----------

* 2018-06-16  Bring ``covdiflog`` from ``util.group`` module.
* 2018-06-13  Appropriate error message for ``invert_caution``.
* 2018-06-12  ``matrix.py``, ``fecon236`` fork. Fix imports, pass flake8.
* 2017-06-19  ``yi_matrix.py``, fecon235 v5.18.0312, https://git.io/fecon235

"""

from __future__ import absolute_import, print_function, division

import numpy as np
from fecon236.util import system
from fecon236.util.group import groupdiflog


RCOND = 1e-15
#       Cutoff for small singular values.


def is_singular(mat):
    """Just test whether matrix is singular (thus not invertible).

    Mathematically, ``if det(mat)==0:`` NOT recommended numerically.
    If the condition number is very large, then the matrix is said to
    be "ill-conditioned." Practically such a matrix is almost singular,
    and the computation of its inverse, or solution of a linear system
    of equations is prone to large numerical errors.
    A matrix that is not invertible has condition number equal to
    infinity mathematically, but here for numerical purposes,
    "ill-conditioned" shall mean condition number exceeds 1/epsilon.

    Notes
    -----

    Ref: https://en.wikipedia.org/wiki/Condition_number

    We shall use epsilon for np.float64 data type
    since Python’s floating-point numbers are usually 64-bit.

    .. code-block:: python

        np.finfo(np.float32).eps
        # 1.1920929e-07
        sys.float_info.epsilon
        # 2.220446049250313e-16
        np.finfo(np.float64).eps
        # 2.2204460492503131e-16
        1/np.finfo(np.float64).eps
        # 4503599627370496.0

    """
    if np.linalg.cond(mat) < 1 / np.finfo(np.float64).eps:
        #       ^2-norm, computed directly using the SVD.
        return False
    else:
        #  Intentionally, no error handling here.
        return True


def invert_caution(mat):
    """Compute the multiplicative inverse of a matrix.

    Numerically ``np.linalg.inv`` is generally NOT suitable,
    especially if the matrix is ill-conditioned,
    but it executes faster than ``invert_pseudo``:
    ``np.linalg.inv`` calls ``numpy.linalg.solve(mat, I)``
    where ``I`` is identity and uses LAPACK LU FACTORIZATION.
    """
    #  Curiously np.linalg.inv() does not test this beforehand:
    if is_singular(mat):
        raise ValueError("SINGULAR matrix here is fatal. Try invert().")
    else:
        #         LinAlgError if mat is not square.
        return np.linalg.inv(mat)


def invert_pseudo(mat, rcond=RCOND):
    """Compute the pseudo-inverse of a matrix.

    If a matrix is invertible, its pseudo-inverse will be its inverse.
    Moore-Penrose algorithm here uses SINGULAR-VALUE DECOMPOSITION (SVD).

    Notes
    -----
    Mathematically, pseudo-inverse (a.k.a. generalized inverse) is defined
    and unique for all matrices whose entries are real or complex numbers.
    LinAlgError if SVD computation does not converge.

    References
    ----------

    * https://en.wikipedia.org/wiki/Moore–Penrose_pseudoinverse

    """
    return np.linalg.pinv(mat, rcond)


def invert(mat, rcond=RCOND):
    """Compute the inverse, or pseudo-inverse as fallback, of a matrix."""
    try:
        #  Faster version first, with is_singular() test...
        return invert_caution(mat)
    except Exception:
        #           ... so mat is probably singular:
        system.warn("ILL-CONDITION: invert() may output pseudo-nonsense.")
        #  How did we get here? The problem is most likely collinearity.
        return invert_pseudo(mat, rcond)


def covdiflog(groupdf, lags=1):
    """Covariance array for differenced log(column) from group dataframe.

    For correlation array, feed output here to ``cov2cor``.
    """
    #  See util.group.groupget() to retrieve and create group dataframe.
    rates = groupdiflog(groupdf, lags)
    V = rates.cov()
    #        ^Type of V is still pandas DataFrame, so convert to array.
    #  AVOID the np.matrix subclass; stick with np.ndarrays instead:
    return V.values


def cov2cor(cov, n=6):
    """Covariance array to correlation array, n-decimal places.

    Returns
    -------
    Pearson product-moment CORRELATION COEFFICIENTS.

    References
    ----------

    * https://en.wikipedia.org/wiki/Covariance_matrix

    """
    darr = np.diagonal(cov)
    #        ^get diagonal elements of cov into a pure array.
    #         Numpy docs says darr is not writeable, OK.
    D = np.diag(1.0/np.sqrt(darr))
    #     ^creates diagonal square "matrix" but not of subclass np.matrix.
    cor = D.dot(cov).dot(D)
    return np.round(cor, n)


if __name__ == "__main__":
    system.endmodule()
