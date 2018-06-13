#  Python Module for import                           Date : 2018-06-13
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_learn.py :: Test fecon236 ml/learn.py module

Testing: We favor pytest over nosetests, so e.g. $ py.test --doctest-modules

REFERENCE
- pytest, https://pytest.org/latest/getting-started.html

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-13  Spin-off doctests from learn.py module.
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.ml.learn import (softmax, softmax_sort)  # noqa


def test_learn_fecon236_softmax():
    '''Softmax function without sort.
    >>> softmax([16, 8, 4, 0, -8, -16], temp=200, n=4)
    [0, 16, 0.2598, 200, [0.2598, 0.2001, 0.1757, 0.1542, 0.1188, 0.0915]]
    >>> softmax([16, 8, 4, 0, -8, -16], temp=50, n=4)
    [0, 16, 0.5733, 50, [0.5733, 0.2019, 0.1198, 0.0711, 0.0251, 0.0088]]
    >>> softmax([16, 8, 4, 0, -8, -16], temp=30, n=4)
    [0, 16, 0.7773, 30, [0.7773, 0.1365, 0.0572, 0.024, 0.0042, 0.0007]]
    >>> softmax([16, 8, 4, 0, -8, -16], temp=1, n=4)
    [0, 16, 1.0, 1, [1.0, 0.0, 0.0, 0.0, 0.0, 0.0]]
    >>> softmax([16, 8, 4, 0, -8, -16], temp=0, n=4)
    [0, 16, 0.9997, 0, [0.9997, 0.0003, 0.0, 0.0, 0.0, 0.0]]
    >>> softmax([16, 16], temp=200, n=4)
    [0, 16, 0.5, 200, [0.5, 0.5]]
    >>> softmax([16, 15, -8], temp=50, n=4)
    [0, 16, 0.5587, 50, [0.5587, 0.4395, 0.0018]]
    '''
    pass


def test_learn_fecon236_softmax_sort():
    '''Softmax function with sort.
    >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=False)
    [(0.5733, 5, 16.0), (0.2019, 4, 8.0), (0.1198, 3, 4.0), (0.0711, 2, 0.0)]
    >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=True)
    [(0.5934, 5, 16.0), (0.209, 4, 8.0), (0.124, 3, 4.0), (0.0736, 2, 0.0)]
    '''
    pass


if __name__ == "__main__":
    system.endmodule()
