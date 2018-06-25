# CONTRIBUTING: Notes on forks and pull requests

We are thrilled that you would like to collaborate on 
this project. Your help is essential.

- Code revisions: please kindly follow [Github flow]
  with respect to the `develop` branch.

- Running tests: details are in the `tests` directory. 
  Python tests are designed run under py.test with 
  with the `--doctest-modules` flag.

- For integration testing, we run [Travis].


## Submitting a pull request

0. [Fork][fork] and clone the repository.
0. Create a new branch: `git checkout -b my-branch-name`
0. Make your change, add tests, and make sure the tests still pass.
0. Tests are strict on PEP8, so please use `flake8` as your lint program.
0. Be sure to ***pull origin/develop and rebase*** before the next step.
0. Push to your fork and [submit a pull request][pr]
0. Kindly wait for your pull request to be reviewed.
0. Stay in touch with fellow developers at [Gitter].


## Tips regarding pull requests

- Refine and add tests whenever possible.

- Update documentation as necessary.  

- Keep your change focused. If there are multiple changes that are not
  dependent upon each other, please submit them as separate pull requests.

- Write a [good commit message](http://tbaggery.com/2008/04/19/a-note-about-git-commit-messages.html).


**Thank you very much for your consideration. 
Your contributing work is very appreciated.**


## Resources

- [Contributing to Open Source on GitHub](https://guides.github.com/activities/contributing-to-open-source/)
- [Using Pull Requests](https://help.github.com/articles/using-pull-requests/)

---

Revision date : 2018-06-25

[fork]:         https://github.com/MathSci/fecon236/fork "Fork fecon236"
[Github flow]:  http://scottchacon.com/2011/08/31/github-flow.html "Github Flow"
[Gitter]:       https://gitter.im/MathSci/fecon236 "Gitter fecon236"
[pr]:           https://github.com/MathSci/fecon236/compare "Pull request"
[Travis]: https://travis-ci.org/MathSci/fecon236 "fecon236 at Travis CI"
