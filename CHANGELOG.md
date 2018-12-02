## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*


### 2018-12-02  (tag: 10.8.0)

tool.py: Add median(), mad(), and madmen() for robust rescaling
using MAD, Median Absolute Deviation.

Add module rates/credit.py.
Derivation in fecon235 notebook, https://git.io/creditprof
Include rates/credit module in __init__.py,
specifically for Unified Credit Profile, creditprof(),
which produces robust MAD rescaling of credit spreads.


### 2018-07-31  (tag: 10.7.1)

Default switch from biased to unbiased estimator of standard deviation,
cf. population vs. sample statistics.
fecon236/tool.py: Add `std()` with population argument,
which can make a significant difference for small sample sizes.
Clarify use of ddof, delta degrees of freedom, and data format cases.
Modify `kurtfun()` in tool.py with population argument.
Thus in dst/gaussmix.py, switch from np.std() to tool.std()
where implicitly population=False by default.

prob/sim.py: Add norat2ret(), ret2prices(),
gmix2ret(), and gmix2prices(), then for display, gmixshow().
Generalizing the bootstrap module reveals two new
primitive functions which can be reused often.
Replace rates2prices() by zerat2prices() for clarity.
Rename simshow() to simushow() using replaced function.
Include the latest SPX constants as default arguments,
so that the numerical values can be sourced by the bootstrap module.

Total rewrite of boots/bootstrap.py:
generalization and clarification of logic flow.
The 2014 code was too SPX specific,
but this new version can be applied across all asset classes.
Add hybrid2ret() where hybrid means
synthesis of bootstrap method with Gaussian mixture.

boots/bootstrap.py: Add smallsample_gmr() to demo
geometric mean rates, and smallsample_loss() to demo
probability of loss.

Also for boots/bootstrap.py, let replace=True as default.
This aligns generally with theoretical bootstrap assumptions.
The opposite was useful during preliminary testing.
Add tests/test_bootstrap.py
where the roundtrip test illustrates overall usage.

We can deprecate `fecon235/nb/SIMU-mn0-sd1pc-d4spx_1957-2014.csv.gz`
but include recipe for creating similar pre-computed CSV files
in https://git.io/bootspx notebook.

dst/gaussmix.py: Modify error handling.
On excessive kurtosis, change `system.die` to OverflowError.
In such cases, retry with larger argument b.

Add docs/index.md for https://fecon236.readthedocs.io
thus markdown files in the `docs` directory should be rendered
automatically by Read the Docs webhooks on fecon236.

Re-establish `.github` directory and revise contents:

```
.old/235/.github/CODE_OF_CONDUCT.md -> .github/CODE_OF_CONDUCT.md
.old/235/.github/CONTRIBUTING.md -> .github/CONTRIBUTING.md
.old/235/.github/PULL_REQUEST_TEMPLATE.md -> .github/PULL_REQUEST_TEMPLATE.md
.old/235/.github/ISSUE_TEMPLATE.md -> .github/ISSUE_TEMPLATE.md
.github/ISSUE_TEMPLATE.md -> .github/ISSUE_TEMPLATE/custom.md
```


### 2018-06-24  (tag: 10.7.0)

**Bump minor to 7 to mark COMPLETION OF REFACTORING.**
See `fecon236/__init__.py` for tree "map" of package directory,
reproduced in README.md: `print(fe.map)`

Revise docs/READ/fe-00_Intro.md esp. on versioning and
use first half on first half of wiki Home.

Add docs/READ/fe-02_FAQ.md originally from
https://github.com/rsvp/fecon235/wiki a.k.a. Home
but revised to reflect new fecon236 changes.
Re-use this FAQ as second half of renewed Home.

Add docs/jupyter/nb-10_Security_trust.md for notebooks.
*Documentation now in sync between fecon235 and fecon236.*

```
.old/235/lib/ys_prtf_boltzmann.py -> fecon236/prtf/boltzmann.py
.old/235/tests/test_boltzmann.py -> tests/test_boltzmann.py
```

prtf/boltzmann.py: Fix circular dependency problem using
fecon235.fecon235 module, especially for covdiflog()
and groupgemrat().


### 2018-06-20  (tag: 10.6.7b70)

The objective of this micro-7 beta release was to
spin-off, integrate, and test the old *fecon235/fecon235.py*
top module as *fecon236/fecon236/top.py*.
Spin-off from top.py, which is now entirely clean and empty,
results in several new subdirectories and modules.

```
.old/235/fecon235.py -> fecon236/top.py
.old/235/tests/test_fecon235.py -> tests/test_group.py
```

- Add util/group.py for `group*()` functions
    - Move covdiflog() from util/group.py to math/matrix.py
- Add futures/cftc.py resulting from groupcotr()
- Function forecast() moved to holtwinters module
    - Include foreholt() and forecast() in test_holtwinters.py
- Add rates/fedfunds.py especially for forefunds()
- Add econ/infl.py especially for foreinfl()
- Add host/hostess.py especially for get()

Fix #3: Circular dependencies resolved within host/hostess.py.
The Python circular dependency hack is detailed in the Endnotes:
put imports inside get() and avoid "from" import syntax.
Test get() via FRED and Quandl in test_hostess.py.

Decorate w4cotr_metals with pytest.mark.xfail, to be investigated.

**setup.py: Change development status from alpha to STABLE.**
***The essential core spin-off from fecon235 to fecon236
is now complete and passes flake8, unit and integration tests:***
Travis build 70, https://travis-ci.org/MathSci/fecon236/builds/394678277


### 2018-06-13  (tag: 10.6.6a58)

The `__version__` variable in `fecon236/__init__.py` will be updated
by `./bin/up-pypi` before each release upload to PyPI.

Add new directories: `parse`, `math`, and `ml` such that

```
.old/235/lib/yi_secform.py -> fecon236/parse/sec.py
.old/235/lib/yi_matrix.py -> fecon236/math/matrix.py
.old/235/tests/test_matrix.py -> tests/test_matrix.py
.old/235/lib/ys_mlearn.py -> fecon236/ml/learn.py
```

Add `tests/test_learn.py` by spin-off of doctests from ml/learn.py.


### 2018-06-09  (tag: 10.6.5a50)

The objective of this micro-5 alpha release was to
update, integrate, and test the *gaussmix* module.
The sympy module for symbolic mathematics is a prerequisite
so we have included notebook documentation.
The analytical results are verified through numerical simulation,
hence we also use our *sim* module.

Add fecon236/dst directory for Distributions (Statistical, not software).
We extensively develop the Gaussian mixture distribution.
In .travis.yml: conda install sympy --
symbolic math package needed for gaussmix module.
Notebook demo of symbolic math package: `docs/READ/fe-54_Symbolic_sympy.ipynb`.

```
.old/235/lib/ys_gauss_mix.py -> fecon236/dst/gaussmix.py
.old/235/tests/test_gauss_mix.py -> tests/test_gaussmix.py
.old/235/docs/fecon235-08-sympy.ipynb -> docs/READ/fe-54_Symbolic_sympy.ipynb
.old/235/lib/yi_simulation.py -> fecon236/prob/sim.py
.old/235/lib/yi_stocks.py -> fecon236/host/stock.py
```

Add fecon236/boots directory for Bootstrap and small-sample studies.
Spin-off 2014 material from prob/sim.py to boots/bootstrap.py.
This will need polish and generalization, useful for a notebook later.

prob/sim.py: Add rates2prices() and simshow().
The latter provides a statistical and optional visual summary
of the simulation module.

In .travis.yml: conda install pandas-datareader --
not pandas_datareader, GOTCHA, which is the module name.
The package name is pandas-datareader, which is prerequisite for
`fecon236/host/stock.py` to retrieve data from Yahoo and Google Finance.


### 2018-06-01  (tag: 10.6.4a43)

The objective of this micro-4 alpha release was to
update, integrate, and test the *optimize* module.
That enabled the absorption of the *opt_holt* module
into the *holtwinters* module.

Add `oc` "Optimal Control" directory for general optimization methods.

```
.old/235/lib/ys_optimize.py -> fecon236/oc/optimize.py
.old/235/tests/test_optimize.py -> tests/test_optimize.py
.old/235/lib/ys_opt_holt.py -> fecon236/tsa/opt_holt.py -> rm
```

tsa/holtwinters.py: Absorb tsa/opt_holt.py
and delete tsa/opt_holt.py.

test_holtwinters.py: Include test of `optimize_holt()`
concluding absorption of opt_holt module, which produces
robust optimal estimation of alpha and beta,
into the holtwinters module.

README.md: Edit sections, include issues URL,
add "what for" section and logo image.
Provisional link to docs.


### 2018-05-24  (tag: 10.6.3a35)

The objective of this micro-3 alpha release was to
update, integrate, and test the *qdl* module
and its dependencies into the project.

```
.old/235/lib/yi_quandl.py -> fecon236/host/qdl.py
.old/235/lib/yi_quandl_api.py -> fecon236/host/_ex_Quandl.py
.old/235/tests/test_timeseries.py -> tests/test_holtwinters.py
```

Add tests/test_qdl.py: Pass xbt price test.

The `_ex_Quandl` module is still operational,
despite Quandl's deprecation of its Quandl.py version 2.8.9.
We fork the single module and will maintain it
as straddling python2/3 code.

host/qdl.py: Deprecate plotqdl() and holtqdl().
Rename quandl() as `_qget()` for future clarity.
Explain the mechanics of API key and token file "authtoken.p".

test_qdl.py: Mark download function with "oLocal",
else Quandl raises: "HTTP Error 429: Too Many Requests"
when testing without authtoken.p through external Travis.

setup.py: Support markdown, correct PyPI rendering
by appending "content_type" incantation.
PyPI rendering also corrected by excluding "license" as text.

Add `docs/READ/fe-97-upkeep.md`
for maintenance of the code infrastructure and distribution.


### 2018-05-18  (tag: 10.6.2a29)

The objective of this micro-2 alpha release was to
update, integrate, and test the *plots* module
and its dependencies into the project.

`host/fred.py`: Graceful deprecate plotfred()
since system.die() does not provide traceback.

`visual/plots.py`: Transplant plot() from `.old/235`
and deprecate use of symbol code as argument.
Wrapping of plotfred and plotqdl within `plot()`
has been deprecated in fecon236, thus the "data"
argument can no longer be a fredcode or quandlcode.

MAJOR decorator refactoring of `visual/plots.py`
using ***decorator*** `saveImage()`.
This greatly reduced repetitive boilerplate code,
and introduced centralized logic, for example, the
option to suppress screen show via leading blank space in title.

Fix `boxplot()` by removing NaN from data.
Hopefully this fixes the "percentile interpolation" bug
which can be traced back to use of `np.compress()`.

`require.txt`: Mirror conda installs in .travis.yml where
minimum versions were obtained through Travis' raw log.
Adopt lockfile "==" syntax to obtain a known deterministic build,
actually used in testing. The shown combination of versions
is *de facto* dependency resolved.

`fecon236/__init__.py`: Include principal modules,
i.e. tool, fred, plots, holtwinters.

`docs/nb-02-preamble.md`: Update Preamble-p10.18.0514
for use in Jupyter notebooks.

Renamed and fully tested:

```
.old/235/tests/test_1tools.py -> tests/test_tool.py
```


### 2018-05-12  (tag: 10.6.1a24)

The objective of this micro-1 alpha release was to
update, integrate, and test the *fred* module
and its dependencies into the project.

We shall use absolute, not relative, import statements
for both `tests` and package modules.
Import division from `__future__`.

Add bin/up-pypi for uploading to PyPI.
Create and upload dist wheel to PyPI.org with option to bump VERSION.
Since our code is still straddling between python27
and python34, we must pay attention to the difference
between Universal versus Pure wheels.
Delete prior wheels in `dist`, else PyPI will consider
duplicate submissions as error.

Add require.txt as placeholder for requirements.txt
where explanation is given in `docs/fe-10-install.md`.

```
.old/235/lib/yi_fred.py -> fecon236/host/fred.py
.old/235/lib/yi_plot.py -> fecon236/visual/plots.py
.old/235/lib/yi_1tools.py -> fecon236/tools.py -> fecon236/tool.py
.old/235/lib/yi_timeseries.py -> fecon236/tsa/holtwinters.py
.old/235/tests/test_fred.py -> tests/test_fred.py
.old/235/tests/zdata-xau-13hj-c30.csv -> tests/zdata-xau-13hj-c30.csv
```

Add fecon236/tsa, directory for *time-series analysis*.
Holt-Winters is only one major method.
We plan to also include Kalman filters.

After each module was renamed, we made lint changes
to comply with flake8. Then the import statements were
modified from relative to proper absolute form.

In `host/fred.py` we eliminate float(integer).
Deprecate plotfred() in favor of using get() and plot().

Add `docs/fe-80-db-store.md` to show how we can persist
a DataFrame using the pandas pickle feature.

Our integration testing via `.travis.yml` begins to
conda install some scientific packages.
Successfully passed Travis build 24.


### 2018-05-01  (tag: 10.6a19)

MathSci joins new PyPI site https://pypi.org/user/MathSci and
establishes the **pip release of the master branch of fecon236**
via https://pypi.org/project/fecon236 (to be done manually by the
maintainers from the git repository using `twine`).

Current alpha version passed Travis build 19 with python27 and python34 env.
Version 10 will support straddling code.
Version 11, expected before 2019-01-01, will drop python27 support
(like upstream numpy and pandas).

The module `fecon236/__init__.py` will contain the hand-coded
string variable `__version__` which approximates the
VERSION file read in by setup.py.

Add docs/fe-10-install.md to help the fecon236 user optimally
install the project.


### 2018-04-25

Add .old/235 which is fecon235 v5.18.0312 --
so bump fecon236 VERSION to 10.05.180312 to signal transition.

Explicitly EXCLUDED are the NOTEBOOKS in the fecon235 `nb`
directory, and also its `.git` directory.
Essential focus is the source code.
Thus we have 10 directories, 49 files as shown in this tree:

```
.old
└── 235
    ├── bin
    │   ├── docker
    │   │   └── rsvp_fecon235
    │   │       └── Dockerfile
    │   ├── ipnbrun
    │   └── update-yi_quandl_api
    ├── CHANGELOG.md
    ├── docs
    │   ├── fecon235-00-README.ipynb
    │   ├── fecon235-08-sympy.ipynb
    │   └── wiki
    │       ├── fecon235-00-wiki.md
    │       ├── make-wiki-mirror.sh
    │       └── mirror
    │           └── Home.md
    ├── fecon235.py
    ├── .github
    │   ├── CODE_OF_CONDUCT.md
    │   ├── CONTRIBUTING.md
    │   ├── ISSUE_TEMPLATE.md
    │   └── PULL_REQUEST_TEMPLATE.md
    ├── .gitignore
    ├── __init__.py
    ├── lib
    │   ├── __init__.py
    │   ├── yi_0sys.py
    │   ├── yi_1tools.py
    │   ├── yi_fred.py
    │   ├── yi_matrix.py
    │   ├── yi_plot.py
    │   ├── yi_quandl_api.py
    │   ├── yi_quandl.py
    │   ├── yi_secform.py
    │   ├── yi_simulation.py
    │   ├── yi_stocks.py
    │   ├── yi_timeseries.py
    │   ├── ys_gauss_mix.py
    │   ├── ys_mlearn.py
    │   ├── ys_opt_holt.py
    │   ├── ys_optimize.py
    │   ├── ys_prtf_boltzmann.py
    │   └── ys_prtf_markowitz.py
    ├── README.md
    ├── tests
    │   ├── 01-run-notebooks.sh
    │   ├── 10-check-modules.sh
    │   ├── smell
    │   ├── test_1tools.py
    │   ├── test_boltzmann.py
    │   ├── test_fecon235.py
    │   ├── test_fred.py
    │   ├── test_gauss_mix.py
    │   ├── test_matrix.py
    │   ├── test_optimize.py
    │   ├── test_system.py
    │   ├── test_timeseries.py
    │   └── zdata-xau-13hj-c30.csv
    └── VERSION
```

File renames:

```
.old/235/.gitignore -> .gitignore
.old/235/__init__.py -> fecon236/__init__.py
.old/235/lib/__init__.py -> fecon236/util/__init__.py
.old/235/lib/yi_0sys.py -> fecon236/util/system.py
.old/235/tests/test_system.py -> tests/test_system.py
```

Establish rudimentary package structure:

- Add **setup.py**: OK using virtualenv and `pip install DIR`
- `fecon236/__init__.py`: Non-empty to call in favors
- Delete `tests/__init__.py`, explain in docs/fe-90-tests.md
- Add fecon236/core.py, a dummy for now
- New package directory created: fecon236/util
- Add docs/fe-00-intro.md, first introductory draft
- util/system.py: Move notebook preamble to docs/nb-02-preamble.md
- Add docs/fe-90-tests.md to explain testing
- Add .travis.yml for Travis CI (uses requirements.txt)
- .travis.yml: Exclude "oLocal" tests by pytest

*Continuous integration testing enabled on virtual machines.
First pass on build 18 at Travis CI,
which included pytest and flake8 tests*,
see https://travis-ci.org/MathSci/fecon236


### 2018-04-10  (tag: 10.00)

2018-04-09 Add README.md.

2018-04-09 LICENSE.md: BSD-3, plus further terms and conditions.

2018-04-10 Add Gitter badge for our chat room.

2018-04-10 Add VERSION, start at 10.00.

Our source code will originate from fecon235 v5.18.0312
which is date-based, so circa 2018-03-12.
The history of that repository goes back to the year 2014:
see https://github.com/rsvp/fecon235 for complete details.

The source code repo should be separate from bulky size
of Jupyter notebooks, thus they are expected to
remain in the fecon235 repository and be developed further there.


### 2018-04-05  (Initial commit)

Note the change in repository OWNERSHIP from
INDIVIDUAL [rsvp] to ORGANIZATION [MathSci]
as [fecon235] migrates to [fecon236].

The rationale for fecon236 is given in:
"Moving to Python 3 > 2020-01-01"
https://github.com/rsvp/fecon235/issues/9


---

[rsvp]: https://rsvp.github.com "Adriano rsvp.github.com"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[Gitter]: https://gitter.im/MathSci/fecon236 "MathSci at Gitter"
[235is9]: https://git.io/235is9 "fecon235 issue 9"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 Repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 Repository"
[CHANGELOG]: https://git.io/236log "fecon236 Change Log"
[236docs]: https://github.com/MathSci/fecon236/tree/develop/docs "fecon236 Documentation"
[236li]: https://git.io/236li "fecon236 BSD License and TOS"
[236is]: https://git.io/236is "fecon236 Issues"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"
