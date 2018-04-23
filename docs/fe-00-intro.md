## Introduction to fecon series

### History

The **fecon** series of *computational tools for financial economics*
began around 2014 at U.C. Berkeley when Jupyter notebooks were known
as IPython notebooks (file extension `.ipynb` is an artifact of that era).
BIDS, Berkeley Institute for Data Science, was just getting established.
The joint seminars by the Economics Department and the Haas Business School,
run under the designation *235*, needed tools to replicate their findings
with publicly accessible data and code.

The Python scientific stack was complicated and the documentation
was murky, constantly in flux, at that time.
Also there was a transitional barrier between python2 and python3.
To address these needs, **fecon235** developed, starting with
datasets obtained through the U.S. Federal Reserve Bank.


### Critique of fecon235

Development occurred *bottom-up*. The open source repository at
http://git.io/fecon235 housed both the application code and
some illustrative notebooks designed to serve as HOWTO examples.
In retrospect, we see that: 

- Code and notebooks should have been separate `git` repositories.
- Code became increasingly unstructured ("spagetti").
- Repetitive patterns emerged in the code ("ravioli").


### Birth of fecon236

We address the critique by designing **fecon236** *top-down*
so that the structure of the code is refined.
It shall only contain *refactored* application code and its tests.

The rewriting opportunity also allows us:

- To conform to Python PEP8 lint guidelines.
- To eventually drop support for python2/3 "straddling" code.
- To make a definitive transition to python3 after 2019-01-01.
- To rebuild and minimize our Docker container based on Miniconda3.
- To have continuous integration tests.
- To be fully `pip` and `conda` compatible.
- To contribute to the PyPI and Anaconda distributions.

Please see https://git.io/fecon236 for more details.


### Versioning

**Application code** will be henceforth developed in **feconNNN** where NNN
is even-numbered. In fecon235, versions for the code were date-based
in the following format: vX.YY.MMDD --
whereas versions for fecon236 will have the traditional
MAJOR.MINOR format (starting with 10.00)
with occassional date as .YYMMDD appended (e.g. 10.05.180312).

The code versions correspond to git tags which annotated
and cryptograhically signed for security (verified by GitHub).

**Notebooks** shall continue to be developed in **feconNNN** where NNN
is odd-numbered. Their revision date is noted in the
"Change Log" section with specific code dependencies
revealed in the Preamble section.

The issue of trust for notebooks is discussed in our wiki:
[Security of Jupyter notebooks](https://github.com/rsvp/fecon235/wiki/Security:-trust).


### References

- [Moving to Python 3 > 2019-01-01](https://github.com/rsvp/fecon235/issues/9)
- [Major transitional annoyances](https://python3statement.org/practicalities)


- [BIDS, Berkeley Institute for Data Science](https://bids.berkeley.edu)
- [Mathematical Sciences Group](https://github.com/MathSci)


---

Last update : 2018-04-23
