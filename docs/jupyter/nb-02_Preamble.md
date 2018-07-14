## fecon236 :: PREAMBLE for Jupyter Notebooks

The fecon235 notebooks for financial economics rely on
Python source code, especially fecon236 at https://git.io/fecon236

For display settings and system details within the notebooks,
the template below is very useful, placed in an input cell.
We will refer to this template as the "**preamble**"
with date-based versioning written as *pNN.yy.mmdd*,
where NN is the major version number of fecon236.


```
CHANGE LOG
2018-07-14  Change pd import to fe.pd
2018-06-23  Include self-referential URL.
2018-05-14  First working version.
2018-04-21  Preliminary draft for fecon236.
```


### Current preamble

In the first cell, we generally only need to invoke this one-liner
explicitly: `import fecon236 as fe`

Then for the second cell:

```python
#  PREAMBLE-p10.18.0714 :: Settings, https://git.io/236pa
from __future__ import absolute_import, print_function, division
fe.system.specs()
%load_ext autoreload
%autoreload 2
#       Use 0 to disable autoreload when a module is modified.
#  NOTEBOOK DISPLAY OPTIONS...
fe.pd.set_option('display.notebook_repr_html', False)
#       Represent pandas DataFrames as text; not HTML representation.
from IPython.display import HTML  # Useful for snippets from web.
#  e.g. HTML('<iframe src=http://en.mobile.wikipedia.org/?useformat=mobile \
#            width=700 height=350></iframe>')
from IPython.display import Image
#  e.g. Image(filename='holt-winters-equations.png', embed=True)
#                  url= Also works instead of filename.
from IPython.display import YouTubeVideo
#  e.g. YouTubeVideo('1j_HxD4iLn8', start='43', width=600, height=400)
from IPython.core import page
get_ipython().set_hook('show_in_pager', page.as_hook(page.display_page), 0)
#  Or equivalently in config file: "InteractiveShell.display_page = True",
#  which will display results in secondary notebook pager frame in a cell.
%matplotlib inline
#  Generate PLOTS inside notebook, "inline" generates static png,
#  whereas "notebook" argument allows interactive zoom and resize.
```

---

Short URL, https://git.io/236pa | Last update : 2018-07-14
