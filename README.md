## fecon236 :: Tools for financial economics

[![Gitter](https://badges.gitter.im/MathSci/fecon236.svg)](https://gitter.im/MathSci/fecon236?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) / master [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=master)](https://travis-ci.org/MathSci/fecon236) / develop [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=develop)](https://travis-ci.org/MathSci/fecon236)
Repository is at [fecon236], see [CHANGELOG] for revision history.


### Currently at ALPHA development status

***Refactor straddling fecon235 source code (not notebooks) to Python 3.***
For full details, see [235is9].

Home for our ***Jupyter notebooks*** shall remain at [fecon235]
due to their bulky size.
Migration to the python3 kernel should have no problems
since fecon235 is compatible with both python27 and python3.
End users will be able to simply `import fecon236 as fe`
as a drop-in replacement.

The fecon236 **develop** branch is where pull requests are currently directed.
The **master** branch is protected and gets released via `pip`, see our [PyPI].

Version 10 of fecon236 represents the refactoring of only the fecon235
source code (not the Jupyter notebooks).
It will maintain compatibility with both python27 and python34.
 
After 2019-01-01, our official support for python27 will discontinue
(like numpy and pandas), however, straddling code may still
continue to work.
 
Version 11 will signal when our [Travis] builds under python27 fail,
and at that point we expect to require at least Python 3.6.


### Contact 

To discuss, or to help out with development and documentation...
please ping @rsvp at [Gitter] or see [rsvp] at the [MathSci] Group.


---

Last update : 2018-05-24

[rsvp]: https://rsvp.github.com "Adriano, lead developer"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[Gitter]: https://gitter.im/MathSci/fecon236 "MathSci at Gitter"
[235is9]: https://github.com/rsvp/fecon235/issues/9 "fecon235 issue 9"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 repository"
[CHANGELOG]: https://github.com/MathSci/fecon236/blob/master/CHANGELOG.md "fecon236 Change Log"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"

