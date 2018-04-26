#  Python Module for import                           Date : 2018-04-25
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  test_system.py :: Test fecon236 system module.

We favor pytest with doctest, so

    $ py.test --doctest-modules

REFERENCE:  py.test   https://pytest.org/latest/getting-started.html
            or PDF at http://pytest.org/latest/pytest.pdf

CHANGE LOG  For latest version, see https://git.io/fecon236
2018-04-25  Fix Travis 16.1 fail.
                Use "oLocal" to mean Only Local testing.
2018-04-22  Refactor from fecon235.
'''

# py2rm
from __future__ import absolute_import, print_function

from fecon236.util import system


def test_minimumPython_system_fecon236():
    '''Test minimum Python version for fecon236.'''
    #  We will support Python 2.7 until 2019-01-01, since
    #  numpy, pandas, and Jupyter views it as "legacy" thereafter.
    assert system.pythontup() >= system.minimumPython


def test_minimumPandas_system_fecon236_vSlow():
    '''Test minimum Pandas version for fecon236.'''
    s = system.versionstr("pandas")
    if s is not None:
        s = s.replace('.', '', 1)
        #     ^only one replace: e.g. 0.17.1 -> 017.1
        assert float(s) >= system.minimumPandas


def test_gitinfo_system_fecon236_oLocal():
    '''Test gitinfo() which obtains repo info by running git.'''
    repo, tag, bra = system.gitinfo()
    #  Only repo has a response known here in advance:
    assert repo == 'fecon236'


if __name__ == "__main__":
    system.endmodule()
