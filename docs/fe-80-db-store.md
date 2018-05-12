## fecon236 documentation :: Database and storage


### Pickle: save and load DataFrame

The easiest way to save a DataFrame on disk is to pickle it:

```
    df.to_pickle(FILENAME)  # where FILENAME usually ends with .pkl
```

This is a pandas feature. Then one can later load df:

```
    df2 = pd.read_pickle(FILENAME)
```

However, the pickle format may be subject to change as pandas develops.

Expect the file size to be about 4x relative to a gzip compressed file.


---

Last update : 2018-05-11
