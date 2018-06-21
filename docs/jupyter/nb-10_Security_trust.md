## Security of Jupyter notebooks

A notebook from a different core version, and especially a different user,
will be tagged as ***"Untrusted"*** due to security concerns.

The best reference here is:
http://jupyter-notebook.readthedocs.io/en/stable/security.html
which contains detailed explanations of:

- Tokens
- Shared security
- Authentication SQLite database: `nbsignatures.db`

When you have decided to **trust** a notebook the quickest way is via
the command: `jupyter trust /PATH/TO/notebook.ipynb`.
Also, within the Jupyter browser interface, one can perform
the same operation under the menu item called "File".

A fecon235 notebook obtained through its GitHub repository is secure.
Release tags are cryptographically signed, and can be verified
through a third-party such as GitHub. See https://git.io/fecon235


### Under the hood

@takluyver, a core developer, provides some interesting
[details](https://github.com/jupyter/help/issues/330#issuecomment-376835261):

> Notebooks can contain two kinds of code: **Code in code cells.** This you just
have to look at before you run it and decide if what it's doing looks
reasonable. It doesn't do anything until you explicitly run those cells, so
it's not a worry when loading the notebook.

> **Javascript code in the output.** This is invisible when you view the
notebook, but it can talk to the kernel and send it Python code (or whatever
language the kernel runs) to execute on your computer. This is what the trust
mechanism deals with.

> When you load an *untrusted* notebook, it won't display any output that can
contain Javascript (or CSS). This is meant to make it safe to open a notebook
to look at. If you run all the cells in a notebook, the output has all been
generated on your computer from code you can see, so the notebook becomes
trusted. If you're sure of where it comes from, you can also bypass this by
marking it trusted directly. A trusted notebook can display
HTML/Javascript/CSS when you open it, so it could immediately start running
code on your computer.

> Markdown cells are sanitised even for trusted notebooks, so they're safe.

> Trust is based on signing the notebook content. So if you've had an identical
notebook at some point which was trusted, another copy of the file will also
be trusted even if it's a fresh download.


### Reporting security bugs

First, see if there is a similar open issue at
https://github.com/jupyter/help/issues
then if necessary, create a new issue for a friendly response.

For extremely serious bugs, contact security@ipython.org

---

Latest revision at https://git.io/trustnb | This document date : 2018-06-21
