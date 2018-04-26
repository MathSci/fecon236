## CHANGE LOG 

*Each file in this project generally has a detailed change log contained 
within itself. This file simply gives a grand overview of such details 
and the annotations in the commits and tags.*


### 2018-04-25  (tag: 10.6.18b)

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

File movements:

- Rename: .old/235/.gitignore -> .gitignore
- Rename: .old/235/__init__.py -> fecon236/__init__.py
- Rename: .old/235/lib/__init__.py -> fecon236/util/__init__.py
- Rename: .old/235/lib/yi_0sys.py -> fecon236/util/system.py
- Rename: .old/235/tests/test_system.py -> tests/test_system.py

Establish rudimentary package structure:

- Add **setup.py**: OK using virtualenv and `pip install DIR`
- fecon236/__init__.py: Non-empty to call in favors
- Delete tests/__init__.py, explain in docs/fe-90-tests.md
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

[rsvp]: https://rsvp.github.com
[issue235]: https://github.com/rsvp/fecon235/issues/9
[fecon235]: https://github.com/rsvp/fecon235
[fecon236]: https://github.com/MathSci/fecon236
[MathSci]: https://github.com/MathSci

