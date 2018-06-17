#  Python Module for import                           Date : 2018-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  cftc.py :: For futures markets under CFTC

- CFTC:= Commodity Futures Trading Commission, a US government agency
- COTR:= Commitment of Traders Report

REFERENCE
- "Market position indicators using CFTC COTR", https://git.io/cotr
    A fecon235 Jupyter notebook illustrating derivation and usage.


CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-17  First version: groupcotr() spin-off from util.group module.
'''

from __future__ import absolute_import, print_function, division

from fecon236 import tool
from fecon236.util import system
from fecon236.util.group import groupget, groupfun
from fecon236.host import qdl
from fecon236.tsa import holtwinters as hw


#  GROUPS:  specify our favorite series as a dictionary
#  where key is name, and corresponding value is its data code:

cotr4w = {'Bonds': qdl.w4cotr_bonds, 'Equities': qdl.w4cotr_equities,
          'Metals': qdl.w4cotr_metals, 'USD': qdl.w4cotr_usd}


def groupcotr(group=cotr4w, alpha=0):
    '''Compute latest normalized CFTC COTR position indicators.
       COTR is the Commitment of Traders Report from US gov agency.
       Optionally specify alpha for Exponential Moving Average
       which is a smoothing parameter: 0 < alpha < 1 (try 0.26).
    '''
    #  For detailed derivation, see https://git.io/cotr
    positions = groupget(group)
    norpositions = groupfun(tool.normalize, positions)
    #  Default alpha argument will skip SMOOTHING operation...
    #  in any case, this function returns a pandas DataFrame:
    if alpha:
        return groupfun(hw.ema, norpositions, alpha)
    else:
        return norpositions


if __name__ == "__main__":
    system.endmodule()
