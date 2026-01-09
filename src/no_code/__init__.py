"""
The best way to write code is to write no code at all.

## Usage

This package is intended to be used as a command-line tool.

To turn your code into no code:

```
$ no_code some_code.py > no_code.py
```

If, for some reason, you need to turn no code back into Python code:

```
$ yes_code no_code.py > some_code.py
```

See the [README](https://github.com/lemonyte/no-code) for more information.
"""

from importlib.metadata import version

from no_code.no import no_code, nothing, something

__version__ = version("no-code")
__all__ = ("no_code", "nothing", "something")
