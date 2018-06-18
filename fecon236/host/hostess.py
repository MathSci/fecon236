#  Python Module for import                           Date : 2018-06-18
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  hostess.py :: Brings together fecon236 host modules

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-18  Circular dependency HACK [Endnotes]: put imports inside get()
                and avoid "from" import syntax there. Fix #3
2018-06-15  Faster get() by exploiting startswith('s4'). Pass flake8.
                Raised error messaging improved for getstock().
2018-06-14  Spin-off get() from top.py.
2018-03-12  fecon235.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system


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
    #  Just to avoid long names...
    #  and a verbose way of avoiding "from" import syntax:
    import fecon236.host.fred
    getfred = fecon236.host.fred.getfred
    import fecon236.host.qdl
    getqdl = fecon236.host.qdl.getqdl
    import fecon236.host.stock
    getstock = fecon236.host.stock.getstock
    #
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


# ======================================================== ENDNOTES ===========
'''
_______________ On CIRCULAR DEPENDENCIES

By putting imports within a function we used a technique called
"DEFERRED IMPORTING." This does not violate Python syntax, as the
official documentation states:

    "It is customary but not required to place all import statements
    at the beginning of a module (or script, for that matter)."
    https://docs.python.org/2/tutorial/modules.html

The downside to deferred imports generally is readability: one
cannot look at the very top of a module and see all its dependencies.

The official documentation also says that it is advisable to use
"import X.Y", instead of other statements such as
"from X import Y", or in the worst case: "from X.Y import *".

As for circular imports, the candidate solutions are explained at
https://stackoverflow.com/a/37126790 by brendan-abel
which can be BEST summarized as: use absolute (not relative) imports,
and definitely AVOID the "from" import style.

The downside to absolute import style is that the names can
get super long. But one can create aliases using "=" with Python objects,
especially functions, at the cost of readability. Generally this solution
across the tops of many modules becomes very tiresome to implement.

"Deferred importing" can speed up startup time, so it is not bad practice,
but some claim that it is a sign of bad design. The notion that circular
dependencies are somehow an indication of poor design seems to be more a
reflection on Python as a language ("glaring bug in the import machinery")
rather than a legitimate design point.

See also: http://stackabuse.com/python-circular-imports by Scott Robinson.


     __________ Example of fecon236 circular dependency

In the fred module, holtwinters.ema() is called to smooth data.
In the holtwinters module, hostess.get() is called to retrieve data.
But the hostess module relies on fred.getfred() in the fred module.

Our deferred import hack in this module, allows us to freely use the
"from" syntax everywhere else: e.g. "from fecon236.host.hostess import get"
at the top of modules without ImportError or AttributeError in both
python27 and python3.
'''
