## fecon236 :: Tools for financial economics :: Documentation

***Curated wrapper over Python ecosystem.
Source code for fecon235 Jupyter notebooks.***

GitHub repository is at [fecon236].
Documentation is currently in flux, see [issue 4][236is4].

- The `docs` directory is being served from [236docs].
    - Markdown files there are nicely rendered at [https://fecon236.readthedocs.io][rtd]
    - Jupyter notebooks, however, are not rendered by *Read the Docs*.
- Documentation of the modules and functions is available at [pydoc.io]
  but we prefer working directly with the source code at [fecon236].
- Please start your orientation with this [README notebook][readnb]
  which shows how most of this project is self-documenting.
- ***The best way to see [fecon236] in action is to
  run the notebooks in the fecon235 `nb` [directory][235nb].***
- For installation details and FAQ, please visit [https://git.io/econ][wiki]


[![fecon236 logo](https://git.io/fecon236-px200.png)](https://github.com/MathSci/fecon236)

### What is this repository for?

**fecon236** provides an interface for ***financial economics*** to the Python
ecosystem, especially packages for mathematics, statistics, science,
engineering, and data analysis.
Complex packages such as *numpy, pandas, statsmodels, scipy, and matplotlib*
are seamlessly integrated at a high-level with APIs of various data hosts for:

- Essential commands which correctly handle annoying low-level pitfalls.

- Retrieval of economic and financial data, both historical and the most current. 

- Data munging, for example, resampling and alignment of time-series data
  from hosts using mutually incompatible formats.

- Analysis using techniques from econometrics, time-series analysis,
  and statistical machine learning.

- Abstraction and software optimization of mathematical operators,
  for example, linear algebra used in portfolio analysis.

- Visualization of data using graphical packages. 

- *Reproducible research which is collaborative and openly accessible
  at zero cost.*

To practically test theoretical ideas interactively,
[fecon236] can employed with any Python IDE interactive development
environment, IPython console, or with a Jupyter notebook.
The code has been tested against both python27 and python3 since 2014,
and works across major platforms: Linux, Mac, and Windows.


### Questions?

Join the chat at [Gitter][236gtt] and consider becoming a member of the
[Mathematical Sciences Group][MathSci].

[![MathSci logo](https://git.io/MathSci-px200.png)](https://github.com/MathSci)



### Appendix 1: fecon236 package map

```
>>> print(fe.map)
Annotated tree map of package directory [with module aliases]
    fecon236
    ├── __init__.py   (Router, sole non-empty __init__.py file herein)
    ├── tool.py       (Tools, low-level essentials)
    ├── top.py        (Top priority, experimental)
    ├── boots   (Bootstrap)
    │   └── bootstrap.py   [bs]
    ├── dst   (Distributions)
    │   └── gaussmix.py   [gmix]
    ├── econ
    │   └── infl.py
    ├── futures
    │   └── cftc.py
    ├── host
    │   ├── fred.py
    │   ├── hostess.py
    │   ├── qdl.py
    │   ├── _ex_Quandl.py
    │   └── stock.py
    ├── math
    │   └── matrix.py   [mat]
    ├── ml   (Machine Learning)
    │   └── learn.py
    ├── oc   (Optimization Control)
    │   └── optimize.py   [op]
    ├── parse
    │   └── sec.py
    ├── prob   (Probability)
    │   └── sim.py   (Simulation)
    ├── prtf   (Porfolio theory)
    │   └── boltzmann.py   [boltz]
    ├── rates  (Fixed Income)
    │   └── fedfunds.py
    ├── tsa    (Time Series Analysis)
    │   └── holtwinters.py   [hw]
    ├── util   (Utilities)
    │   ├── group.py
    │   └── system.py
    └── visual
        └── plots.py
```

---

[BSD License and TOS][236li] / This page, last update : 2018-07-25


[pydoc.io]: https://www.pydoc.io/pypi/fecon236-10.7.0 "fecon236 pydoc VERSION <="
[rtd]: https://fecon236.readthedocs.io "fecon236 Read the Docs"
[wiki]: https://git.io/econ "fecon235 wiki Home"
[readnb]: https://git.io/fecon-intro "fecon235 README notebook"
[235gtt]: https://gitter.im/rsvp/fecon235 "@rsvp at Gitter"
[rsvp]: https://rsvp.github.com "Adriano, lead developer"
[236gtt]: https://gitter.im/MathSci/fecon236 "@MathSci at Gitter"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[BIDS]: https://bids.berkeley.edu "Berkeley Institute for Data Science"
[235is7]: https://github.com/rsvp/fecon235/issues/7 "Disruption equities data"
[235is9]: https://github.com/rsvp/fecon235/issues/9 "Moving to Python 3"
[235nb]: https://git.io/fecon235nb "fecon235 nb directory"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 repository"
[236log]: https://git.io/236log "fecon236 CHANGELOG"
[236docs]: https://github.com/MathSci/fecon236/tree/develop/docs "fecon236 Documentation"
[236li]: https://git.io/236li "fecon236 BSD License and TOS"
[236inst]: https://git.io/236inst "fecon236 docs Installation"
[236req]: https://git.io/236req "fecon236 require.txt"
[236is]: https://git.io/236is "fecon236 Issues"
[236is4]: https://github.com/MathSci/fecon236/issues/4 "Documentation needed"
[FRED]: https://fred.stlouisfed.org "Federal Reserve Economics Data"
[Quandl]: https://www.quandl.com "Quandl data"
[Anaconda]: https://www.anaconda.com/download "Anaconda Python distribution"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"
