## fecon236 :: Tools for financial economics

***Refactor straddling fecon235 source code (not notebooks) to Python 3.***

GitHub repository is at [fecon236], see [CHANGELOG] for revision history.
The protected **master** branch gets released via `pip`, see our [PyPI].
The **develop** branch is where pull requests are currently directed.

[![Gitter](https://badges.gitter.im/MathSci/fecon236.svg)](https://gitter.im/MathSci/fecon236?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) / master [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=master)](https://travis-ci.org/MathSci/fecon236) / develop [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=develop)](https://travis-ci.org/MathSci/fecon236)


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

***The best way to see the convenience of [fecon236] in action is to
run the notebooks in the `nb` directory at [fecon235].***

Documentation is currently being served from [236docs].


### Currently at ALPHA development status

Home for our ***Jupyter notebooks*** shall remain at [fecon235]
due to their bulky size.
Migration to the python3 kernel should present no problems
since fecon235 is compatible with both python27 and python3.
For full details, see [235is9].
End users will be able to simply `import fecon236 as fe`
as a drop-in replacement.

Version 10 of fecon236 represents the refactoring of only the fecon235
v5.18.0312 library code (not the Jupyter notebooks).
It shall maintain compatibility with both python27 and python34.
 
After 2019-01-01, our official support for python27 will discontinue
(like numpy and pandas), however, straddling code may still
continue to work.
 
Version 11 will signal when our [Travis] builds under python27 fail,
and at that point we expect to require at least Python 3.6.


### Contact 

Please kindly open issues at [236is].

To discuss, or to help out with development and documentation...
please ping @rsvp at [Gitter] or see [rsvp] at the [MathSci] Group.

[![fecon236 logo](https://git.io/fecon236-px200.png)](https://github.com/MathSci/fecon236)

---

[BSD License and TOS][236li] / This page, last update : 2018-05-29

[rsvp]: https://rsvp.github.com "Adriano, lead developer"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[Gitter]: https://gitter.im/MathSci/fecon236 "MathSci at Gitter"
[235is9]: https://github.com/rsvp/fecon235/issues/9 "fecon235 issue 9"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 repository"
[CHANGELOG]: https://git.io/236log "fecon236 Change Log"
[236docs]: https://github.com/MathSci/fecon236/tree/develop/docs "fecon236 Documentation"
[236li]: https://git.io/236li "fecon236 BSD License and TOS"
[236is]: https://git.io/236is "fecon236 issues"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"
