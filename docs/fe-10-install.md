## fecon236 docs :: Installation

### Background information

Here an excellent overall TUTORIAL for Python installation in general:
https://packaging.python.org/tutorials/installing-packages
especially regarding **pip**.

- Do not invoke setup.py directly.
- Please use setuptools>=24.3
- Please use pip>=9.0
- For regular installs, use `pip install ...`
- For developer installs, use `pip install -e ...`
- See further [Python 3 practicalities](https://python3statement.org/practicalities)

An **egg** is a Built Distribution format which is being *replaced* by
**wheel**.


### How are the versions named?

[Semantic Versioning](https://packaging.python.org/tutorials/distributing-packages/#choosing-a-versioning-scheme)
and more formally in [PEP440](https://www.python.org/dev/peps/pep-0440)

Within a numeric release (1.0, 2.7.3), the following suffixes
are permitted and MUST be ordered as shown:
`.devN, aN, bN, rcN, <None>, .postN`.
Note that c is considered to be semantically equivalent to
rc (release candidate) and must be sorted as if it were rc. 
Letters: "a" denotes alpha, "b" beta, whereas
None signifies a *Major.Minor* release from the master branch.
The ".post" suffix is used when code itself
unaffected, for example, corrected typos in documentation.


#### fecon236 version specifics

In general, the version at PyPI (and thus the pip installed versions)
will lag that of the "develop" branch at GitHub.

Version 10 denotes our effort to port and refactor only the source code
from fecon235 (excluding the Jupyter notebooks).
It will maintain compatibility with both python27 and python34 series.

After 2019-01-01, our support for python27 will discontinue
(like numpy and pandas), however, straddling code may still work.

Version 11 is expected to require at least Python 3.6.


### References

- [fecon236 at GitHub](https://github.com/MathSci/fecon236)
- [fecon236 at PyPI](https://pypi.org/project/fecon236)
- [BIDS, Berkeley Institute for Data Science](https://bids.berkeley.edu)
- [Mathematical Sciences Group](https://github.com/MathSci)


---

Last update : 2018-05-01
