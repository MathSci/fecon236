#  Python Module for import                           Date : 2018-11-10
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
r"""Gaussian mixture distribution for fecon236

- Refinement of geometric mean computations relies on Jean (1983)
  which derives an exact infinite series of higher moments, wherein
  the premature truncation in the classic paper Young (1969) is corrected.

Notes
-----

- Tests of this module at ``tests/test_gaussmix.py``
- For LATEST version, see https://git.io/fecon236


Structured Zero Mean GM(2)
--------------------------

Given data set {:math:`x`}, we can compute its variance and kurtosis.
Thus, :math:`\sigma` and :math:`\rm K` are observable.
Corollary 1.2 says that GM(2) parameters can indeed synthesize :math:`\rm K`,
but its messiness suggests that we impose further structure for clarity.
A sensible requirement is a strict ordering,
:math:`\sigma_1 < \sigma < \sigma_2`
in consideration of the weighted equation for :math:`\sigma^2`.
We can impose this ordering by constrained constants :math:`a` and :math:`b`.

PROPOSITION 2: Let :math:`\sigma_1 = a\sigma` and :math:`b\sigma = \sigma_2`
such that :math:`0<a<1<b`, then for zero-mean GM(2)
the following satisfies conditions for both kurtosis and variance:

.. math::

    \frac{\rm K - b^4}{a^4 - b^4} = \frac{1 - b^2}{a^2 - b^2}

This shows how constants :math:`a` and :math:`b` are jointly constrained
by the moments of the Gaussian mixture.

Our STRATEGY will be to choose :math:`b>1`, then use the kurtosis $\kappa$
to compute :math:`a`. Probability :math:`p` can then be computed using
Lemma 2.2, for which :math:`q=1-p` follows.
Since :math:`\sigma_1 = a\sigma` and :math:`b\sigma = \sigma_2`
the components of our zero-mean GM(2) are fully resolved,
given specific :math:`\sigma`.

From two observable statistics :math:`\sigma` and :math:`\kappa`,
we have deduced, not fitted, the parameters of a zero-mean GM(2).
An observable mean :math:`\mu` which is non-zero can be added to
our model to obtain a zero-skew GM(2).

References
----------

- Gaussian Mixture and Leptokurtotic Assets, 2017, Jupyter notebook,
  https://github.com/rsvp/fecon235/blob/master/nb/gauss-mix-kurtosis.ipynb
- William H. JEAN and Billy P. Helms, 1983, Geometric Mean Approximations,
  J. Financial and Quantitative Analysis, 18:3:287-293.
- William E. YOUNG and Robert H. Trent, 1969, Geometric Mean Approximations
  of Individual Security and Portfolio Performance,
  J. Financial and Quantitative Analysis, 4:2:179-199.

Change Log
----------

* 2018-11-10  Minor: raw string mode for intro, fix #6 flake8 W605 SyntaxError.
* 2018-07-08  Change from ``np.std`` to ``tool.std`` for population argument.
* 2018-07-04  On excessive kurtosis, change ``system.die`` to
  ``OverflowError``.
* 2018-06-03  Rename to ``gaussmix.py``, ``fecon236`` fork. Pass flake8, fix
  imports.
* 2017-06-29  ``ys_gauss_mix.py``, fecon235 v5.18.0312, https://git.io/fecon235
  Fallback clause for ``gemrate`` when log fails (2008Q4).
* 2017-05-21  Deprecate ``gm2_georet`` and ``georet_gm2`` due to math proof.
  For geometric mean computations, add ``gemreturn_Jean``, ``gemrate``, and for
  data: ``georat``.

"""

from __future__ import absolute_import, print_function, division

import sympy as sym    # Symbolic math package
import numpy as np
from fecon236 import tool
from fecon236.util import system


def gm2_strategy(kurtosis, b=2):
    """Use sympy to solve for "a" in Proposition 2 numerically."""
    #  sym.init_printing(use_unicode=True)
    #  #        ^required if symbolic output is desired.
    a = sym.symbols('a')
    K = kurtosis / 3.0
    #  Use equation from Prop. 2
    LHS = (K - (b**4)) / ((a**4) - (b**4))
    RHS = (1 - (b**2)) / ((a**2) - (b**2))
    a_solved = sym.solveset(sym.Eq(LHS, RHS), a, domain=sym.S.Reals)
    #  ... expect negative and positve real solutions
    #      provided in sympy's FiniteSet format.
    if a_solved == sym.S.EmptySet:
        #               ^when no feasible solution was found in domain.
        #                Do not accept imaginary solutions.
        raise OverflowError("Extreme kurtosis: Retry using larger b.")
        #     ^dies when kurtosis > 12 and b=2, for example.
        #           SPX returns since 1957 have kurtosis around 31.6
        #           which is very high, requiring b>3.4 for feasiblity.
    else:
        #  But a>0 by construction, so extract the positive real number:
        a_positive = max(list(a_solved))
    return a_positive


def gm2_main(kurtosis, sigma, b=2):
    """Compute specs for GM(2) given observable statistics and b."""
    a = gm2_strategy(kurtosis, b)
    #  Probability p as given in Lemma 2.2:
    p = float((1 - (b**2)) / ((a**2) - (b**2)))
    #   The returned parameters can then be used in simulations,
    #   e.g. simug_mix() in lib/yi_simulation.py module,
    #   or for synthetic assets in risk management.
    q = 1-p
    sigma1 = float(a*sigma)
    sigma2 = float(b*sigma)
    #    Use float above to convert from np.float64, for roundit().
    return [[a, b], [p, sigma1], [q, sigma2]]


def gm2_print(kurtosis, sigma, b=2):
    """Print specs for GM(2) given observable statistics and b."""
    specs = gm2_main(kurtosis, sigma, b)
    print("Constants a, b:", specs[0])
    print("GM(2), p: ", specs[1][0])
    print("GM(2), sigma1:", specs[1][1])
    print("GM(2), q: ", specs[2][0])
    print("GM(2), sigma2:", specs[2][1])


# ======================================================= APPLICATIONS ========


def gm2_vols_fit(data, b=2.5):
    """Estimate GM(2) VOLATILITY parameters including mu, given b.

    Notes
    -----

    * Our data is presumed to be prices of some financial asset.

    """
    rat = tool.diflog(data, lags=1)
    #          ^First difference of log(data).
    arr = tool.df2a(rat)
    #
    #  Routine stat calculations on our array:
    N = len(arr)
    mu = np.mean(arr)
    sigma = tool.std(arr)
    k_Pearson = (sum((arr - mu)**4)/N) / sigma**4
    #  For kurtosis details, see our kurtfun().
    #
    specs = gm2_main(k_Pearson, sigma, b)
    #       [[a, b], [p, a*sigma], [1-p, b*sigma]]
    sigma1 = specs[1][1]
    sigma2 = specs[2][1]
    q = specs[2][0]
    return [mu, sigma1, sigma2, q, k_Pearson, sigma, b, N]


def gm2_vols(data, b=2.5, yearly=256):
    """Compute GM(2) ANNUALIZED VOLATILITY in percentage form, given b.


    2017-05-16  Outputs given SPX, informally minimizing b until fatal:

    .. code-block:: python

        gm2_vols(spx['1957':], b=3.4)
        # [6.4231, 4.878, 52.8776, 0.07866443, 31.5634,
           15.5522, 3.4, 256, 15748]

        gm2_vols(spx['1997':], b=2.0)
        # [5.6690, 5.8802435, 38.5585, 0.232142, 11.1628,
           19.2793, 2.0, 256, 5313]

        gm2_vols(spx['2007':], b=2.2)
        # [4.9873, 5.1699, 44.8882, 0.195946, 13.7804, 20.4037,
           2.2, 256, 2705]

    So one might suppose a typical set of outputs would look like:

    .. csv-table:: Outputs

        Annualized mean return,  5.69%
        Annualized sigma1,  5.30938
        Annualized sigma2, 45.44142
        Probability sigma2,  0.1689
        kurtosis, 18.8355
        Annualized sigma, 18.411734

    where b around 2.533 might work, but not always.

    Our sigma2 guess is interesting since "double or nothing"
    is just 2.2 standard deviations away. The probability of
    drawing from the second Gaussian with the higher volatility
    of 45% is about 0.17. The compensation for such risks taken
    is the annual mean return of 5.7%, plus dividends collected.


    Notes
    -----

    * Our data is presumed to be prices of some financial asset.
    * Argument yearly expresses frequency of data, default is business daily.

    """
    mu, sigma1, sigma2, q, k_Pearson, sigma, b, N = gm2_vols_fit(data, b)
    #  ANNUALIZE appropriately in "percentage" form...
    yc = 100 * yearly
    ysr = 100 * np.sqrt(yearly)
    #  ... the mean return mu is still arithmetic, not geometric:
    return [mu*yc, sigma1*ysr, sigma2*ysr, q,
            k_Pearson, sigma*ysr, b, yearly, N]


#  #  DEPRECATED 2017-05-21: If geometric mean approximation is only a
#  #             function of mu and sigma, then the probabilistic
#  #             GM(2) decomposition into sigma1 and sigma2
#  #             does not mathematically refine the approximation!
#
#  def gm2_georet(mu, sigma1, sigma2, q=0.10, yearly=1):
#      """Define GEOMETRIC mean return for GM(2) Gaussian mixture model."""
#      #  Argument q is the probability of the second Gaussian.
#      #  Argument yearly is a scale parameter to express frequency of data.
#      #   Default yearly=1 produces a plain unscaled geometric mean return.
#      var1 = sigma1 * sigma1 * yearly
#      var2 = sigma2 * sigma2 * yearly
#      geor1 = (mu*yearly) - (var1 / 2.0)
#      geor2 = (mu*yearly) - (var2 / 2.0)
#      #       Note that geor2 can be negative if var2 is large.
#      geor = ((1-q)*geor1) + (q*geor2)
#      #     ^TODO: [/] - prove this equality for geometric mean return.
#      return geor


def gemreturn_Jean(mu_return, sigma, k_Pearson=3):
    """Approximation for geometric mean RETURN via Jean (1983) infinite series.

    Notes
    -----
    Important definition: "financial return":= 1 + "rate" where rate is
    expressed in decimal form.
    """
    #  Jean (1983) derived the exact infinite series for geometric mean return
    #  around a reference point (the arithmetic mean return worked out best).
    #  Here we code an approximation by the first five terms of that series:
    terms = [np.log(mu_return), 0, 0, 0, 0]
    #  By stipulation, we shall ignore the odd moments...
    #  terms[1] = 0   # Zero by symmetry: absolute first  central moment.
    #  terms[3] = 0   # Zero by symmetry: absolute third  central moment.
    variance = sigma**2                 # absolute second central moment.
    k_raw = k_Pearson * (sigma**4)      # absolute fourth central moment.
    #       kurtosis details in kurtfun().
    terms[2] = -(variance / (2.0 * (mu_return**2)))
    terms[4] = -(k_raw / (4.0 * (mu_return**4)))
    #          ^increasing sigma and kurtosis will lower gemreturn <=!
    log_greturn = sum(terms)
    return np.exp(log_greturn)


def gemrate(mu_rate, sigma, kurtosis=3, yearly=1):
    """Approximation for annualized geometric mean RATE by preferred method.

    Notes
    -----
    Important definition: "financial return":= 1 + "rate" where rate is
    expressed in decimal form.
    """
    mu_return = 1 + mu_rate
    k_Pearson = kurtosis
    #           ^MUST be expressed as Pearson kurtosis here, see kurtfun().
    greturn = gemreturn_Jean(mu_return, sigma, k_Pearson)
    greturn_annual = greturn**yearly
    grat = greturn_annual - 1
    if np.isnan(grat):
        #   nan will occur when expected losses exceed 100% -- log error!!
        #   Such estimates actually occurred during 2008Q4 -- Great Recession.
        grat = (mu_rate - ((sigma*sigma)/2.0)) * yearly
        #      ^Second-order approximation used in georet.
    return grat


#  N.B. -  The gem* functions are related to the GM(2) model in so far
#          as kurtosis is involved. The probabilistic decomposition of sigma
#          into sigma1 and sigma2 does NOT affect geometric mean computations.


def gemrat(data, yearly=256, pc=True):
    """Compute annualized geometric mean rate for given data.

    Notes
    -----
    Output will be more accurate than the method implicit in georet() since the
    kurtosis of differenced log data matters. Argument pc will present
    appropriate output in percentage form.
    """
    rat = tool.diflog(data, lags=1)
    #          ^First difference of log(data).
    arr = tool.df2a(rat)
    #
    #  Routine stat calculations on our array:
    N = len(arr)
    mu = np.mean(arr)
    sigma = tool.std(arr)
    k_Pearson = (sum((arr - mu)**4)/N) / sigma**4
    #  For kurtosis details, see our kurtfun().
    #
    #     Annualize...
    muy = mu * yearly
    sigmay = sigma * np.sqrt(yearly)
    grate = gemrate(muy, sigmay, k_Pearson, yearly=1)
    #  Using gemrate(muy, sigmay, k_Pearson, yearly=256) instead could
    #  result in: geometric mean > arithmetic mean, which is a contradiction.
    if pc:
        return [grate*100, muy*100, sigmay*100, k_Pearson, yearly, N]
    else:
        return [grate, muy, sigmay, k_Pearson, yearly, N]


#       __________ UNIFY GM(2) and GEOMETRIC MEAN RATE
#       with only one pass through data: gm2gemrat() and gm2gem().
#
#       If only geometric mean rate matters, use gemrat()[0] instead
#       since there is no dependency on b which introduces fragility
#       due to symbolic computation exercised in gm2_main().


def gm2gemrat(data, yearly=256, b=2.5, pc=True):
    """Compute annualized geometric mean rate and GM(2) parameters.

    Notes
    -----
    Argument pc will present appropriate output in percentage form.
    """
    #                 k is Pearson kurtosis.
    grate, mu, sigma, k, yearly, N = gemrat(data, yearly, False)
    b = 2 if b <= 1.0 else b
    #   ^sensible correction for violating mathematical assumption.
    try:
        gm2out = gm2_main(k, sigma, b)
    except Exception:
        try:
            b += 0.5
            system.warn("INCREASED b by 0.5 -- attempting resurrection ...")
            gm2out = gm2_main(k, sigma, b)
        except Exception:
            b += 0.5
            system.warn("INCREASED b by 0.5 AGAIN -- final attempt ...")
            gm2out = gm2_main(k, sigma, b)
    [a, b], [p, sigma1], [q, sigma2] = gm2out
    if pc:
        return [grate*100, mu*100, sigma*100, k, sigma1*100, sigma2*100,
                q, b, yearly, N]
    else:
        return [grate, mu, sigma, k, sigma1, sigma2, q, b, yearly, N]


def gm2gem(data, yearly=256, b=2.5, pc=True, n=4):
    """Print annualized specs from gm2gemrat() with n decimal places."""
    specs = tool.roundit(gm2gemrat(data, yearly, b, pc), n, echo=False)
    print("Geometric  mean rate:", specs[0])
    print("Arithmetic mean rate:", specs[1])
    print("sigma:", specs[2])
    print("kurtosis (Pearson):", specs[3])
    print("GM(2), sigma1:", specs[4])
    print("GM(2), sigma2:", specs[5])
    print("GM(2), q: ", specs[6])
    print("GM(2), b: ", specs[7])
    print("yearly:", specs[8])
    print("N:", specs[9])


if __name__ == "__main__":
    system.endmodule()
