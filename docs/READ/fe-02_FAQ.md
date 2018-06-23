## fecon236 docs :: FAQ, Frequently Asked Questions


### Q: How do fecon235 and fecon236 differ?

The tools for financial economics started out as IPython notebooks
at **fecon235** https://github.com/rsvp/fecon235 in 2014.
Four years later the source code derived from the patterns and idioms
used in rebranded Jupyter notebooks was refactored at **fecon236**
https://github.com/MathSci/fecon236 and integration tested under
both python27 and python3.

The two repositories are curated wrappers over the Python and Jupyter
ecosystems. The notebooks will be continue to be developed in the
fecon235 `nb` directory https://git.io/fecon235nb
serving as usage examples and templates for research, while
the source code behind the notebooks will be supported at fecon236.


### Q: How do I INSTALL and start using fecon235?

First: fork, clone, or download a copy of our [project][fecon235] from GitHub.

- Info on HOWTO fork: https://guides.github.com/activities/forking
- Info on HOWTO clone: https://help.github.com/articles/cloning-a-repository
- Get zip file without git: https://github.com/rsvp/fecon235/zipball/master

Second: our project has external package dependencies which can be
easily fulfilled by [Anaconda]. If you are new to the Python ecosystem,
we would highly recommend that free distribution which includes Jupyter,
IPython, numpy, pandas, matplotlib, etc.

Optional: to run *old* fecon235 code make sure your local fecon235
top directory is under the scope of your PYTHONPATH, a system variable.
PYTHONPATH is used by the Python interpreter to determine which
modules to load.

The most important fecon235 assets are the **notebooks** located in the
[nb directory][235nb] (which is explicitly *not* a package).
Please see the introductory notebook at https://git.io/fecon-intro
to get started.


### Q: How do I INSTALL and run fecon236?

Ideally, fork, clone, or download a copy of our [project][fecon236]
from GitHub. A fork will allow you to later make pull requests.
Community development of the code is an important aspect of the project.

- Note that fecon236 includes a setup.py file for manual installation.
- Extra fine details on [fecon236 installation][236inst]
- Get zip file without git: https://github.com/MathSci/fecon236/zipball/master

OK, but there is also the quick way: `pip install --pre fecon236`

The `--pre` flag will include the latest version which is stable enough
for the non-developer user.  Of course, it can be used in conjunction
with the `--upgrade` flag.
To remove the project completely: `pip uninstall fecon236`

As for satisfying external dependencies, we recommend the [Anaconda]
distribution which properly handles binaries (for computational speed,
e.g. MKL Math Kernel Library) for all operating systems,
and correctly performs dependency resolution (unlike PyPI).
Pro tip: get the conda-aware version of pip by `conda update pip`
before pip-installing fecon236.

If you insist on satisfying the dependencies manually,
we have provided information for a proven deterministic build
via [required.txt][236req]

One everything is installed, only one further command suffices:
`import fecon236 as fe`

We adopted absolute\_import throughout this project,
which is a feature compatible with python27,
also making fecon236 easy to incorporate into other projects.


### Q: Where is the documentation?

The most current user documentation can be found in the `docs` directory, 
however, the source code is thoroughly documented with useful comments.

The best way to learn about the user-friendly code is to pick a Jupyter
notebook on a topic which interests you, and then to work interactively with
it for analysis, see the [nb directory][235nb].


### Q: Are there online discussions? Help?

Chat with fellow users at Gitter: https://gitter.im/rsvp/fecon235
or with fellow developers at Gitter: https://gitter.im/MathSci/fecon236


### Q: How do I report a bug, or suggest enhancements?

Chat with us first, then also check the Issues section of repositories.


### Q: How do I retrieve economic off-beat FRED data series?

To access data from the U.S. Federal Reserve Bank, each economic time series
and its frequency has its own "fredcode" which is freely available at their
site [FRED].

```
    df = fe.get( fredcode )
    #            fredcode is entered as a string, or an
    #            assigned variable named d4*, m4*, q4*.
    #  E.g. the variable q4gdpusr contains the string 'GDPC1'
    #       which is U.S. real GDP in 2009 USD billions, SA quarterly.
    fe.plot(df)
    #       df is automatically in pandas DataFrame format.
```


### Q: How do I retrieve data from Quandl?

The same idea as FRED above. For example, d7xbtusd='BCHAIN/MKPRU' which
is for the Bitcoin price in USD (d7 indicates that the data is 7 days 
per week). The quandlcodes can be found at [Quandl], however,
use Google search with keyword "quandl" for better results.


### Q: How do I retrieve data series for equities?

We use a special string called "*stock slang*" in the format "s4symbol"
where symbol is spelled out in all lower-case.

For example, to retrieve SPY (the ETF for S&P500), use "s4spy"
and this line to get a pandas DataFrame: `df = fe.get("s4spy")`
 
Note: there has recently been upstream disruption in getting
equities data, please consult [235is7] for remedies.


### Q: Where is the package map for fecon236?

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

[![fecon236 logo](https://git.io/fecon236-px200.png)](https://github.com/MathSci/fecon236)

---

[BSD License and TOS][236li] / This page, last update : 2018-06-22

[rsvp]: https://rsvp.github.com "Adriano, lead developer"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[Gitter]: https://gitter.im/MathSci/fecon236 "MathSci at Gitter"
[235is7]: https://github.com/rsvp/fecon235/issues/7 "Disruption equities data"
[235is9]: https://github.com/rsvp/fecon235/issues/9 "Moving to Python 3"
[235nb]: https://git.io/fecon235nb "fecon235 nb directory"
[feconnb]: https://git.io/fecon-intro "fecon README notebook"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 repository"
[CHANGELOG]: https://git.io/236log "fecon236 Change Log"
[236docs]: https://github.com/MathSci/fecon236/tree/develop/docs "fecon236 Documentation"
[236li]: https://git.io/236li "fecon236 BSD License and TOS"
[236inst]: https://git.io/236inst "fecon236 installation"
[236req]: https://git.io/236req "fecon236 require.txt"
[236is]: https://git.io/236is "fecon236 issues"
[FRED]: https://fred.stlouisfed.org "Federal Reserve Economics Data"
[Quandl]: https://www.quandl.com "Quandl data"
[Anaconda]: https://www.anaconda.com/download "Anaconda Python distribution"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"
