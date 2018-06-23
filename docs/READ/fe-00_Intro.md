## fecon236 docs :: Introduction

### History

The **fecon** series of *computational tools for financial economics*
began around 2014 at U.C. Berkeley when Jupyter notebooks were known
as IPython notebooks (file extension `.ipynb` is an artifact of that era).
BIDS, Berkeley Institute for Data Science, was just getting established.
The joint seminars by the Economics Department and the Haas School of Business,
run under the designation *235*, needed tools to replicate their findings
with publicly accessible data and code.

The Python scientific ecosystem was complicated and the documentation
was murky, constantly in flux, at that time.
Also there was a transitional barrier between python2 and python3.
To address these needs, **fecon235** developed, starting with
datasets obtained through the U.S. Federal Reserve Bank.


### Critique of fecon235 source code

Development occurred *bottom-up* through experiments replicable
in notebooks. The open source repository at http://git.io/fecon235
housed illustrative notebooks, designed to serve as HOWTO examples,
and the application code was abstracted from such experimentation.
In retrospect, we see that: 

- Code and notebooks should have been separate git repositories.
- Code became increasingly unstructured ("spagetti").
- Repetitive patterns emerged in the code ("ravioli").
- Low-level idioms should be accessible throughout the project.
- Notebooks became surrogate documentation.


### Birth of fecon236

In 2018 we address the critique by designing **fecon236**
*top-down* so that the structure of the code is refined,
providing a solid foundation for future development.
It shall consist only of *refactored* application code
and its tests, excluding the notebooks.

The new architecture allows us:

- To enable continuous integration testing (Travis).
- To eventually drop support for python2/3 "straddling" code.
- To make a definitive transition to python3 after 2019-01-01.
- To rebuild and minimize our Docker container based on Miniconda3.
- To be fully `pip` and `conda` compatible.
- To contribute via the PyPI and Anaconda distribution channels.
- To run code cross-platform: in scripts, IDE, virtual machines, etc.

Please see https://git.io/fecon236 for more details.


### Versioning differences

**Application code** will be henceforth developed in **feconNNN**
projects where NNN is even-numbered.
**Notebooks** shall continue to be developed in **feconNNN**
projects where NNN is odd-numbered.

In fecon235, versioning is date-based: vX.YY.MMDD

Versioning for fecon236, however, will use the traditional
MAJOR.MINOR.MICRO format conforming to PyPI standards.
The alpha "a" or beta "b" tag may be accompanied by a Travis build number.
Release candidates will be denoted by "c" (not rc).
We may occasionally use .post handles which are date-based,
for example: 10.6.7b70.postYYMMDD


### Security

The versions will correspond to git tags which annotated
and cryptograhically *signed* for security (verified by GitHub).
The issue of **trust** for notebooks is discussed in our docs:
https://git.io/trustnb


### References

- [Moving to Python 3 > 2019-01-01](https://github.com/rsvp/fecon235/issues/9)
- [Major transitional annoyances](https://python3statement.org/practicalities)


- [BIDS, Berkeley Institute for Data Science](https://bids.berkeley.edu)
- [Mathematical Sciences Group](https://github.com/MathSci)


---

Last update : 2018-06-22
