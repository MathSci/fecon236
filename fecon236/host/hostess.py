#  Python Module for import                           Date : 2018-06-15
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  hostess.py :: Brings together fecon236 host modules

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-15  Faster get() by exploiting startswith('s4'). Pass flake8.
                Raised error messaging improved for getstock().
2018-06-14  Spin-off get() from top.py.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.host.fred import getfred
from fecon236.host.qdl import getqdl
from fecon236.host.stock import getstock


def get(code, maxi=0):
    '''Unifies getfred, getqdl, and getstock for data retrieval.
    code is fredcode, quandlcode, futures slang, or stock slang.
    maxi should be an integer to set maximum number of data points,
         where 0 implies the default value.

    get() will accept the vendor code directly as string, e.g.
    from FRED and Quandl, or use one of our abbreviated variables
    documented in the appropriate module listed in the import section.
    The notebooks provide good code examples in action.

    Futures slang is of the form 'f4spotyym' where
                  spot is the spot symbol in lower case,
                  yy   is the last two digits of the year
                  m    is the delivery month code,
            so for December 2015 COMEX Gold: 'f4xau15z'

    Stock slang can be also used for ETFs and mutual funds.
    The general form is 's4symbol' where the symbol must be in
    lower case, so for SPY, use 's4spy' as an argument.
    '''
    if code.startswith('s4'):
        #  Let failure report its real cause, e.g. RemoteDataError,
        #  when disruption of equities data occurs;
        #  see https://github.com/rsvp/fecon235/issues/7
        if maxi:
            df = getstock(code, maxi)
        else:
            df = getstock(code)
    else:
        try:
            df = getfred(code)
        except Exception:
            try:
                if maxi:
                    df = getqdl(code, maxi)
                else:
                    df = getqdl(code)
            except Exception:
                raise ValueError('INVALID symbol string or code variable.')
    return df


if __name__ == "__main__":
    system.endmodule()
