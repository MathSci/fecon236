## fecon236 :: PREAMBLE for Jupyter Notebooks

The notebooks for financial economics are based on
Python source code, e.g. fecon236 at https://git.io/fecon236

To offer additional services, specifically for notebooks,
and especially for display settings and system details,
we shall rely on a template to be placed in an input cell.

Such a template will be called the "*preamble*"
with date-based versions indicated by pNN.yy.mmdd,
where NN will correspond to major number
of the source code itself.


```
CHANGE LOG
2018-04-21  Preliminary draft for fecon236.
```


### Current preamble

```python
#  PREAMBLE-p10.18.0421a :: Settings and system details
from __future__ import absolute_import, print_function
system.specs()
%load_ext autoreload
%autoreload 2
#       Use 0 to disable autoreload when a module is modified.
#  NOTEBOOK DISPLAY OPTIONS...
import pandas as pd
pd.set_option('display.notebook_repr_html', False)
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

Last update : 2018-04-21
