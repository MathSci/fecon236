#  Python Module for import                           Date : 2018-06-20
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  boltzmann.py :: Boltzmann portfolio for fecon236

Alternative to Markowitz portfolio. Usage demonstrated in notebook, see
fecon235/nb/prtf-boltzmann-1.ipynb for explicit details and derivation,
or Part 1: https://git.io/boltz1 and Part 2: https://git.io/boltz2

    The softmax() function is in fecon236/ml/learn.py since it applies
    more widely in machine learning.

One virtually has no control over how the assets perform and interact. Only
the portfolio allocation over time is in our decision set. Let's recast the
underlying assets as agents which supposedly will help increase our wealth.
Our task will be to select the expert(s) among the agents and to allocate
portions of our current wealth.

To discriminate among the agents we need their performance metrics. Since our
objective is to maximize future wealth, the optimal metric is the geometric
mean rate of each agent. From our research we know how to include risks,
including leptokurtotic events ("fat tails"), into that single metric.

There is evidence that the performance of some agents are inter-correlated.
Therefore, rather than select a single expert, we choose to diversify our bets
among a few agents, and call that our "portfolio." To maximize the geometric
mean rate of the portfolio, the second order condition is to minimize its
variance. That problem is easily solved by borrowing the weights of what is
known as the "Markowitz global minimum variance portfolio."

Those weights depend on the covariance structure of the agents' performance
which is unfortunately not stable over time. There may be some information
which can be exploited to tilt our bets favorably.


    prices ---> cov ---> globalw
      |                    |
      |                  trimit  <-- floor
      |                  renormalize
      |                    |
      v                    v
      |                    |
    gemrat              weights
      |                    |
      |________scores______|
                 |
                 |                   Boltzmann
      temp --> softmax --> probs --> pweights


The Markowitz weights may suggest that we bet against the consistently poor
performance of some agents. We shall generally regard the weights as
advisory, taking what suits us and renormalizing.

To summarize the information set so far, we cast the agents in a game, each
with some score. When the game consists of multiple rounds, we can use tools
from reinforcement learning to help us make the best sequential decisions.

The softmax function is fed the scores to compute the probability of a
particular agent being the expert. This function takes temperature as a
diffusion parameter, that is, an optimal way to diversify our bets across
possible experts. The theory here is due to Ludwig Boltzmann and his work
on statistical mechanics and entropy. But the temperature setting can also be
seen as a Bayesian way to express the overall uncertainty involved with
estimating the various measures.

Finally, those probabilities are combined with our renormalized weights to
arrive at "pweights," our portfolio weights.


REFERENCES

- John H. Cochrane, 2005, Asset Pricing, Princeton U. Press.

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-20  boltzmann.py, fecon236 fork. Fix imports, pass flake8.
2017-07-08  ys_prtf_boltzmann.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from fecon236 import tool
from fecon236.util import system
from fecon236.util import group
from fecon236.math import matrix
#               ^avoiding the np matrix type, stick with arrays!
from fecon236.ml import learn


def weighcov(cov):
    '''WEIGHT array (N,1) for Global Min Var Portfolio, given cov.'''
    #  Derived in Cochrane (2005), chp. 5, p.83.
    Viv = matrix.invert_pseudo(cov)
    #                  ^in case covariance matrix is ill-conditioned.
    one = np.ones((cov.shape[0], 1))
    top = Viv.dot(one)
    bot = one.T.dot(Viv).dot(one)
    return top / bot


def weighcovdata(dataframe):
    '''WEIGHT array (N,1) for Global Min Var Portfolio, given data.'''
    V = matrix.covdiflog(dataframe)
    return weighcov(V)


def trimit(it, floor, level):
    '''For an iterable, accept values > floor, else set to level.'''
    try:
        #  ... in case "it" array elements are integers,
        #  else we cannot assign floats later when enumerating:
        it = it.astype(np.float64)
    except Exception:
        pass
    cpit = it[:]
    for i, x in enumerate(it):
        cpit[i] = x if x > floor else level
    #      Output should be of same type as it:
    return cpit


def renormalize(it):
    '''Let elements of an iterable proportionally abs(sum) to 1.
       Renormalization of portfolio weights is treated differently
       than probabilities which cannot be negative.
    '''
    #  Remember that a list is an iterable, too.
    arr = np.array([float(x) for x in it])
    sumit = float(np.sum(arr))
    try:
        #  ... in case "it" array elements are integers,
        #  else we cannot assign floats later when enumerating:
        it = it.astype(np.float64)
    except Exception:
        pass
    cpit = it[:]
    for i, x in enumerate(it):
        cpit[i] = x / abs(sumit)
        #             ^preserves signs within it.
    #      Output should be of same type as it:
    return cpit


def rentrim(weights, floor, level):
    '''Accept weight > floor, else set to level, then renormalize.'''
    trimmed = trimit(weights, floor, level)
    return renormalize(trimmed)


def gemratarr(dataframe, yearly=256):
    '''Extract geometric mean rate of each column into an array.'''
    gems = group.groupgemrat(dataframe, yearly, order=False, n=8)
    return np.array([item[0] for item in gems]).reshape(len(gems), 1)


def weighsoft(weights, rates, temp, floor, level):
    '''Given weights, compute pweights as array by softmax transform.'''
    scores = weights * rates
    problist = learn.softmax(scores, temp)[-1]
    probs = np.array(problist).reshape(len(problist), 1)
    #  Revise weights based on softmax probabilities:
    pweights = probs * weights
    #  Then appropriately adjust:
    return rentrim(renormalize(pweights), floor, level)


def boltzweigh(dataframe, yearly=256, temp=55, floor=0.01, level=0):
    '''Given data, compute pweights as array by softmax transform.'''
    rates = gemratarr(dataframe, yearly)
    globalw = weighcovdata(dataframe)
    weights = rentrim(globalw, floor, level)
    pweights = weighsoft(weights, rates, temp, floor, level)
    return pweights


def boltzportfolio(dataframe, yearly=256, temp=55, floor=0.01, level=0, n=4):
    '''MAIN: SUMMARY of Boltzmann portfolio, rounded to n-decimal places.
       Return list where values are Python floats, not array type, e.g.
           [2.7833,
            [[0.6423, 2.05, 'America'],
             [0.0, -11.17, 'Emerging'],
             [0.0, -10.47, 'Europe'],
             [0.3577, 4.1, 'Gold'],
             [0.0, -4.99, 'Japan']]]
       The portfolio's geometric mean rate is included first.
       Each sub-sublist will consist of weight, rate, and key.
       The order of keys from the dataframe is preserved.
    '''
    rates = gemratarr(dataframe, yearly)
    globalw = weighcovdata(dataframe)
    weights = rentrim(globalw, floor, level)
    pweights = weighsoft(weights, rates, temp, floor, level)
    #      ---- so far should be the same as boltzweigh()
    scores = pweights * rates
    grat = round(float(np.sum(scores)), n)
    keys = list(dataframe.columns)
    #  wrk, i.e. "weight, rate, key", is a list of lists:
    wrk = [tool.roundit([float(w), float(rates[i]), keys[i]], n, echo=False)
           for i, w in enumerate(pweights)]
    return [grat, wrk]


if __name__ == "__main__":
    system.endmodule()
