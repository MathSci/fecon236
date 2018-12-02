#  Python Module for import                           Date : 2018-11-29
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  credit.py :: Credit risk module for fecon236

- For detailed derivation of Unified Credit Profile, creditprof(),
    see fecon235 notebook, https://git.io/creditprof

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-11-29  Add creditprof().
'''

from __future__ import absolute_import, print_function, division

from fecon236.util import system
from fecon236.tool import todf, madmen
from fecon236.host.hostess import get
from fecon236.host.fred import d4bond10, daily


def creditprof():
    '''Credit profile derived from mortgage and corporate credit spreads.'''
    #  Derivation in fecon235/nb/fred-credit-spreads.ipynb
    #  See https://git.io/creditprof
    #  First, note the oldest start date common among all series herein:
    start = '1991-08-30'
    #  ----- MORTGAGE CREDIT SPREAD
    #  Freddie Mac 15-Year Fixed Rate Mortgage v. Treasury 10-year bond.
    #  Freddie Mac series is updated weekly on Thursdays,
    #  so we apply daily interpolation to be
    #  frequency compatible with the other series in this function:
    fmac = daily(get('MORTGAGE15US'))
    #  Retrieve daily rates for 10-year Treasuries...
    ty = get(d4bond10)
    #  ... then compute the mortgage spread:
    mort = todf(fmac - ty)
    #  Profile the mortgage credit spread:
    mortmad = madmen(mort)
    #  ----- CORPORATE BOND SPREAD
    #  Examine daily BAA10Y spread between Moody's Seasoned Baa-rated
    #  Corporate Bonds and 10-year Treasury Constant Maturity:
    baa = get('BAA10Y')
    #  Profile the corporate credit spread:
    baamad = madmen(baa[start:])
    #  ----- UNIFIED PROFILE for generality,
    #  take the mean of all profiles:
    return todf((mortmad + baamad) / 2)


if __name__ == "__main__":
    system.endmodule()
