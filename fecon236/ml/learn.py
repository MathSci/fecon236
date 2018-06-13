#  Python Module for import                           Date : 2018-06-13
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  learn.py :: Fundamentals from Machine Learning

- softmax() for cross-entropy, MLE, neural networks, Boltzmann portfolio.
- softmax_sort() for ordering and filtering info on the probabilities.

USAGE: tests/test_learn.py contains numerical examples.

REFERENCES
- David J.C. MacKay (2008), Information theory, Inference, and Learning
    Algorithms, 7th printing from Cambridge U. Press.
- Softmax, https://compute.quora.com/What-is-softmax?share=1

CHANGE LOG  For LATEST version, see https://git.io/fecon236
2018-06-13  Spin-off doctests to tests/test_learn.py.
2018-06-12  learn.py, fecon236 fork. Fix imports, pass flake8, pass doctest.
2017-06-09  ys_mlearn.py, fecon235 v5.18.0312, https://git.io/fecon235
'''

from __future__ import absolute_import, print_function, division

import numpy as np
from operator import itemgetter
from fecon236 import tool
from fecon236.util import system


def softmax(it, temp=55, n=4):
    '''Softmax probabilities for iterable where temp sets temperature tau.
       Temperature tau is set as a temp percent of ensemble mean so that
       the scaling of tau works well across many different scenarios.
       Experiment with temp around 40 to 70; higher temp (100+)
       will make it-scores more equi-probable, whereas probabilities
       can be sharpened by decreasing temp towards 1.
       Setting temp to 0 results in generic softmax without temperature.
       Results are rounded to n decimal places.
    '''
    #  Convert iterable to numpy array, then find index of its maximum value:
    arr = tool.toar(it)
    idmax = np.argmax(arr)
    hardmax = arr[idmax]
    #  Without loss of generality for mathematically defined softmax,
    #  subtracting an arbitrary constant from each it-element
    #  always helps NUMERICAL STABILITY, so let it be hardmax:
    arrstable = arr - hardmax
    #      Important to note arrstable will consist of maximum(s) represented
    #      by zero, and all other values will be necessarily negative.
    if temp > 0:
        avg = np.mean(arrstable)
        if avg:
            tau = abs(avg * (temp/100.0))
            #  Let temperature be POSITIVE and temp percent of ensemble mean.
        else:
            #  Edge case: avg will be zero if it-scores are all equal,
            #  which implies they are equi-probable, so any tau should do,
            #  but tau must be NON-ZERO to avoid division error next.
            tau = 1.0
    else:
        #  Whenever temp is set to 0, False, or None => GENERIC softmax.
        #  Also negative temp will be treated as generic softmax.
        temp = 0   # Prefer the numerical eqivalent for return below.
        tau = 1.0
    #  MATHEMATICALLY, (Boltzmann) softmax is defined as follows:
    expit = np.exp(arrstable / tau)
    sum_expit = np.sum(expit)
    softmax_exact = expit / sum_expit
    #                      roundit will output a list, not an array:
    softmax_approx = tool.roundit(softmax_exact, n, echo=False)
    hardprob = softmax_approx[idmax]
    return [idmax, hardmax, hardprob, temp, softmax_approx]

    #      __________ SOFTMAX USAGE NOTES
    #      softmax_sort() is obviously slower to compute than softmax().
    #      They serve different purposes, for example,
    #      softmax()[-1][i] can track a particular i-th class of it, whereas
    #      softmax_sort()[:3] will give information on the top 3 classes.
    #
    #      The TEMPERATURE is a proxy for the degree of uncertainty
    #      in the relative estimation of it-scores, but can also serve
    #      to diffuse errors, i.e. a diversification technique with
    #      mathematical reasoning rooted in statistical mechanics,
    #      information theory, and maximum likelihood statistics.
    #      To test temperature variations, softmax() will be much faster.

#  >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=False)
#  [(0.5733, 5, 16.0), (0.2019, 4, 8.0), (0.1198, 3, 4.0), (0.0711, 2, 0.0)]
#
#  >>> softmax_sort([-16, -8, 0, 4, 8, 16], temp=50, drop=0.05, renorm=True)
#  [(0.5934, 5, 16.0), (0.209, 4, 8.0), (0.124, 3, 4.0), (0.0736, 2, 0.0)]


def softmax_sort(it, temp=55, n=4, drop=0.00, renorm=False):
    '''Softmax results sorted, include index; option to drop and renormalize.
       Probabilities less than drop are ignored.
       Setting renorm=True will make probabilities sum to 1.
    '''
    arr = tool.toar(it)
    softmax_approx = softmax(arr, temp, n)[-1]
    #  Tuples are formatted as (probability, index, it-value)
    tups = [(p, i, float(arr[i]))
            for i, p in enumerate(softmax_approx) if p >= drop]
    if renorm:
        subtotal = sum([p for p, i, v in tups])
        tups = [(round(p/subtotal, n), i, v) for p, i, v in tups]
    #  Want softmax_sort()[0] to yield the maximum candidate:
    return sorted(tups, key=itemgetter(2), reverse=True)


if __name__ == "__main__":
    system.endmodule()
