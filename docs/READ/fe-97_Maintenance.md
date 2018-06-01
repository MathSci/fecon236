## fecon236 docs :: Upkeep

*Here we delineate the details behind the ***maintenance***
of the infrastructure for the fecon236 code base and
its external distribution.*


### Imports

Use absolute, rather than relative, import styles.
`fecon236/__init__.py` shall be the only *non-empty* `__init__.py` file.

- Update `fecon236/__init__.py` for abbreviated access to modules.


### Commits

Merge commits disabled at GitHub (prefer fast-forward rebase).

- `__version__` should be manually edited in `fecon236/__init__.py`
- `__version__` is not necessarily synced with VERSION.


### Dependencies

- Update install instructions for `tests` by editing `.travis.yml`
- Update `require.txt` especially when ecosystem changes substantially.
- Rule: let the user take care of installing specific dependencies.


### setup.py

- Verify minimum Python version.
- Revise old classifiers.


### PyPI.org

This is the site from which the world will `pip install fecon236`
so great care must be taken here.

- For ./bin/up-pypi, verify whether wheel is Universal (2/3) or Pure (3).
- Bump VERSION.
- Upload project to PyPI *only* from the *master* branch.
- Execute ./bin/up-pypi without version argument.


### References

- [Mathematical Sciences Group](https://github.com/MathSci)


---

Last update : 2018-05-19
