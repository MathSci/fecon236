#  Python Module for import                           Date : 2017-06-17
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per Python PEP 0263 
''' 
_______________|  ys_prtf_markowitz.py : Markowitz portfolio

Convex optimization using cvxopt package.

REFERENCES
- Stephen Boyd and Lieven Vandenberghe, 2004, Convex Optimization, Cambridge
  U. Press. Book: http://www.stanford.edu/~boyd/cvxbook/bv_cvxbook.pdf
  Slides: http://www.stanford.edu/~boyd/cvxbook/bv_cvxslides.pdf

- John H. Cochrane, 2005, Asset Pricing, Princeton U. Press.

- William F. Sharpe, 1999, On Markowitz's critical line method, 
  https://web.stanford.edu/~wfsharpe/mia/opt/mia_opt3.htm

- Thomas Wiecki, 2015, The efficient frontier: Markowitz portfolio
  optimization in Python using cvxopt:
  https://www.quantopian.com/posts/the-efficient-frontier-markowitz-portfolio-optimization-in-python-using-cvxopt
  https://blog.quantopian.com/markowitz-portfolio-optimization-2/

- Sean J. Welleck, 2014, Portfolio Optimization with Python cvxopt,
  https://wellecks.wordpress.com/2014/03/23/portfolio-optimization-with-python
  https://github.com/wellecks/port_opt

CHANGE LOG  For latest version, see https://github.com/rsvp/fecon235
2017-06-17  First version.
'''

from __future__ import absolute_import, print_function, division
import numpy as np
from . import yi_0sys as system


def dummyfun():
    print("hi from dummyfun!")


if __name__ == "__main__":
     system.endmodule()
