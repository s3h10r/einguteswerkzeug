debug
=====

wdb
---

a comfortable & mighty but also easy to use 
debugger is [wdb](https://github.com/Kozea/wdb):

```console 
$ wdb.server &
$ firefox localhost:1984 

$ python -m wdb your_file.py
```

example:

```console
$ python -m wdb ./contactsheet ../input/ -o /tmp/out.jpg
```

pdb
---

an always available (but not very comfortable debugger) is pdb:

You can launch a Python program through pdb by using `pdb myscript.py` or `python -m pdb myscript.py`.
To set a ispecific breakpoint you can do:
```python
import pdb

""" ... your works fine code """

pdb.set_trace()

""" your buggy code... """
```

There are a few commands you can then issue, which are documented on the [pdb page](https://docs.python.org/3/library/pdb.html).

Some useful ones to remember are:

```
    b: set a breakpoint
    c: continue debugging until you hit a breakpoint
    s: step through the code
    n: to go to next line of code
    l: list source code for the current file (default: 11 lines including the line being executed)
    u: navigate up a stack frame
    d: navigate down a stack frame
    p: to print the value of an expression in the current context
```

literature
----------

* [how to step through python code to help debug issues](https://stackoverflow.com/questions/4929251/how-to-step-through-python-code-to-help-debug-issues)

