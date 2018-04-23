## fecon236 :: tests documentation

We will follow the best practices for `pytest`
as described in greater detail at
https://docs.pytest.org/en/latest/goodpractices.html


### Tests will be outside the application code

Thus `__init__.py` shall be *excluded* from the `tests` directory
because we want our tests to run easily against an installed version,
not the local repository code.

One consequence is *giving up subdirectories* under `tests`
and accepting *only unique test filenames*, for example,
`test_module.py` or `integrated_test.py`.


### Development testing

The `pytest` recommendation is "to use virtualenv environments and pip
for installing your application and any dependencies [which] ensures
isolation from the system Python installation."

You can then install the package in "editable" mode: `pip install -e DIR`
which lets you change your source code (both application and tests)
and rerun tests at will.
This is similar to running `python setup.py develop` or `conda develop`
in that the package is installed using a symlink to the development code.


### Continuous integration

To make sure that our actual package passes all tests,
we will use Travis CI and its pytest support.
Travis helps to setup environments with pre-defined dependencies
where a pre-configured test command is executed.
It will run tests against the *installed* package and
not against the source code checkout, helping to detect packaging glitches.


---

Last update : 2018-04-23
