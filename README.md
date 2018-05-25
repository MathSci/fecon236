## fecon236 :: Tools for financial economics

***Refactor straddling fecon235 source code (not notebooks) to Python 3.***

GitHub repository is at [fecon236], see [CHANGELOG] for revision history.
The protected **master** branch gets released via `pip`, see our [PyPI].
The **develop** branch is where pull requests are currently directed.

[![Gitter](https://badges.gitter.im/MathSci/fecon236.svg)](https://gitter.im/MathSci/fecon236?utm_source=badge&utm_medium=badge&utm_campaign=pr-badge&utm_content=badge) / master [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=master)](https://travis-ci.org/MathSci/fecon236) / develop [![Build Status](https://travis-ci.org/MathSci/fecon236.svg?branch=develop)](https://travis-ci.org/MathSci/fecon236)


### Currently at ALPHA development status

Home for our ***Jupyter notebooks*** shall remain at [fecon235]
due to their bulky size.
Migration to the python3 kernel should present no problems
since fecon235 is compatible with both python27 and python3.
For full details, see [235is9].
End users will be able to simply `import fecon236 as fe`
as a drop-in replacement.

Version 10 of fecon236 represents the refactoring of only the fecon235
source code (not the Jupyter notebooks).
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


---

Last update : 2018-05-25

[rsvp]: https://rsvp.github.com "Adriano, lead developer"
[MathSci]: https://github.com/MathSci "Mathematical Sciences Group"
[Gitter]: https://gitter.im/MathSci/fecon236 "MathSci at Gitter"
[235is9]: https://github.com/rsvp/fecon235/issues/9 "fecon235 issue 9"
[fecon235]: https://github.com/rsvp/fecon235 "fecon235 repository"
[fecon236]: https://github.com/MathSci/fecon236 "fecon236 repository"
[CHANGELOG]: https://git.io/236log "fecon236 Change Log"
[236is]: https://git.io/236is "fecon236 issues"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
[PyPI]: https://pypi.org/project/fecon236 "fecon236 at PyPI"

