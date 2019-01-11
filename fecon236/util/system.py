#  Python Module for import                           Date : 2019-01-11
#  vim: set fileencoding=utf-8 ff=unix tw=78 ai syn=python : per PEP 0263
'''
_______________|  system.py :: system and date functions including specs.

Code in this module should be compatible with both Python 2 and 3
until 2019-01-01, thereafter only python3.

For example, it is used in the preamble of fecon235 Jupyter notebooks.


REFERENCES:
- Compatible IDIOMS: http://python-future.org/compatible_idioms.html
                     Nice presentation.

- SIX module is exhaustive: https://pythonhosted.org/six/
        Single file source: https://bitbucket.org/gutworth/six


CHANGE LOG  For latest version, see https://git.io/fecon236
2019-01-11  Fix versionstr(): python3 dislikes import using exec().
2018-06-20  Update specs(), include version for statsmodels.
2018-05-15  Include version("fecon236") to specs.
2018-04-25  Ignore "raw_input" < python3 flake8.
2018-04-21  yi_0sys module from fecon235 renamed to system.
                Major flake8 fixes. Move notebook preamble to docs.
'''

# py2rm
from __future__ import absolute_import, print_function
#    __future__ for Python 2 and 3 compatibility; must be first in file.

import sys
import os
import time
from subprocess import check_output, CalledProcessError
#                      ^for Python 2.7 and 3+


minimumPython = (2, 7, 0)
#             ... else a warning is generated in specs().
minimumPandas = 18.0
#               ^after replacing the first dot, then float.


#             Open  /dev/null equivalent file for Unix and Windows:
dev_null = os.open(os.devnull, os.O_RDWR)
#                                 ^Cross-platform read and write.
#             os.devnull is just a string:  "/dev/null" or "nul"
#             thus redirecting to os.devnull is insufficient
#             and that alone will cause a fileno error.
#  We could later close it by: os.close(dev_null). Leave open.
#  See gitinfo() for example of usage.


def getpwd():
    '''Get present working directory (Linux command is pwd).
       Works cross-platform, giving absolute path.
    '''
    return os.getcwd()


def program():
    '''Get name of present script; works cross-platform.'''
    #  Note: __file__ can get only the name of this module.
    return os.path.basename(sys.argv[0])


def warn(message, stub="WARNING:", prefix=" !. "):
    '''Write warning solely to standard error.'''
    print(prefix, stub, program(), message, sep=' ', file=sys.stderr)


def die(message, errcode=1, prefix=" !! "):
    '''Gracefully KILL script, optionally specifying error code.'''
    stub = "FATAL " + str(errcode) + ":"
    warn(message, stub, prefix)
    sys.exit(errcode)
    #         ^interpretation is system dependent;
    #          generally non-zero is considered as some error.
    #  Note: "os._exit" exits without calling cleanup handlers,
    #  flushing stdio buffers, etc. Thus, it is not a standard way.


def date(hour=True, utc=True, localstr=' Local'):
    '''Get date, and optionally time, as ISO string representation.
       Boolean hour variable also gives minutes and seconds.
       Setting utc to False will give local time instead of UTC,
       then localstr can be used to indicate location.
    '''
    if hour:
        form = "%Y-%m-%d, %H:%M:%S"
    else:
        form = "%Y-%m-%d"
    if utc:
        form += ' UTC'
        tup = time.gmtime()
    else:
        form += localstr
        tup = time.localtime()
    return time.strftime(form, tup)


def timestamp():
    '''Timestamp per strict RFC-3339 standard where timezone Z:=UTC.'''
    form = "%Y-%m-%dT%H:%M:%SZ"
    tup = time.gmtime()
    return time.strftime(form, tup)


def pythontup():
    '''Represent invoked Python version as an integer 3-tuple.'''
    #  Using sys.version is overly verbose.
    #  Here we get something like (2, 7, 10) which can be compared.
    return sys.version_info[:3]


def versionstr(module="IPython"):
    '''Represent version as a string, or None if not installed.'''
    #  Unfortunately must treat Python vs its modules differently...
    if module == "Python" or module == "python":
        ver = pythontup()
        return str(ver[0]) + '.' + str(ver[1]) + '.' + str(ver[2])
    else:
        try:
            #  2019-01-11 Fix: python3 dislikes import using exec().
            #  exec("import " + module)
            #  exec("vermod = " + module + ".__version__")
            mod = __import__(module)
            vermod = mod.__version__
            return vermod
        except Exception:
            return None


def versiontup(module="IPython"):
    '''Parse version string into some integer 3-tuple.'''
    s = versionstr(module)
    try:
        v = [int(k) for k in s.split('.')]
        return tuple(v)
    except Exception:
        #  e.g. if not installed or not convertible to integers...
        if s is None:
            return (0,  0,  0)
        else:
            return (-9, -9, -9)


def version(module="IPython"):
    '''Pretty print Python or module version info.'''
    print(" :: ", module, versionstr(module))


def utf(immigrant, xnl=True):
    '''Convert to utf-8, and possibly delete new line character.
       xnl means "delete new line"
    '''
    if xnl:
        #                Decodes to utf-8, plus deletes new line.
        return immigrant.decode('utf-8').strip('\n')
    else:
        #                Decode for compliance to utf-8:
        return immigrant.decode('utf-8')


def run(command, xnl=True, errf=None):
    '''RUN **quote and space insensitive** SYSTEM-LEVEL command.
       OTHERWISE: use check_output directly and list component
       parts of the command, e.g.
           check_output(["git", "describe", "--abbrev=0"])
       then generally use our utf() since check_output
       usually does not return utf-8, so be prepared to
       receive bytes and also new line.
    '''
    #  N.B. -  errf=None means the usual error transmittal.
    #          Cross-platform /dev/stdout is STDOUT
    #          Cross-platform /dev/null   is our dev_null above.
    #  https://docs.python.org/2/library/subprocess.html
    return utf(check_output(command.split(), stderr=errf), xnl)


def gitinfo():
    '''From git, get repo name, current branch and annotated tag.'''
    #  Suppressing error messages by os.devnull seems cross-platform,
    #  but it is just a string, so use our open file dev_null instead.
    try:
        repopath = run("git rev-parse --show-toplevel", errf=dev_null)
        #              ^returns the dir path plus working repo name.
        repo = os.path.basename(repopath)
        tag = run("git describe --abbrev=0", errf=dev_null)
        #                       ^no --tags because we want annotated tags.
        bra = run("git symbolic-ref --short HEAD", errf=dev_null)
        #         ^returns the current working branch name.
        return [repo, tag, bra]
    except CalledProcessError:
        #  Probably outside git boundaries...
        return ['git_repo_None', 'tag_None', 'branch_None']


def specs():
    '''Show ecosystem specifications, including execution timestamp.
       APIs are subject to change, so versions are critical for replication.
    '''
    if pythontup() < minimumPython:
        warn("This project requires a more recent Python version.")
    else:
        print(" !:  Code for this project straddles python27 and python3.")
    version("Python")
    version("IPython")
    version("jupyter_core")         # Common functionality of Jupyter projects.
    version("jupyter_client")       # Jupyter client libraries and protocol.
    version("notebook")             # Worked for Jupyter notebook 4.0.6
    version("matplotlib")
    version("numpy")
    version("scipy")
    version("statsmodels")
    version("sympy")
    version("pandas")               # pandas is the keystone for the rest.
    version("pandas_datareader")
    #       ^but package is "pandas-datareader" <=! GOTCHA
    version("fecon236")
    repo, tag, bra = gitinfo()
    print(" ::  Repository:", repo, tag, bra)
    print(" ::  Timestamp:", timestamp())


def endmodule():
    '''Procedure after __main__ conditional in modules.'''
    die("is a MODULE for import, not for direct execution.", 113)


# py2rm
'''ROSETTA STONE FUNCTIONS approximately bridging Python 2 and 3.
   e.g.    answer = get_input("Favorite animal? ")
           print(answer)
'''
if pythontup() < (3, 0, 0):
    get_input = raw_input   # noqa
else:
    #   But beware of untrustworthy arguments!
    get_input = input


if __name__ == "__main__":
    endmodule()
