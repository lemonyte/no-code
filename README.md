# No Code

> The best way to write code is to write [no code](https://github.com/kelseyhightower/nocode) at all.

Writing code that does nothing is great, but sometimes you still want your code to do *something*.
This package allows you to write nothing, and still have your code do something.

## Installation

> [!TIP]
> It is highly recommended to use a virtual environment for proper installation of the `no.pth` file.

```shell
python -m pip install no-code
```

[Python 3.10](https://www.python.org/downloads/) or a newer version is required.

## Usage

This package is intended to be used as a command-line tool.

> [!IMPORTANT]
> Make sure you are in an activated virtual environment. Using `uv run` tends to break this package.

To turn your code into no code:

```shell
$ cat some_code.py
print("Hello, world! 😁")

$ no_code some_code.py > no_code.py

$ cat no_code.py
# coding: no
​‌‌‌​​​​​‌‌‌​​‌​​‌‌​‌​​‌​‌‌​‌‌‌​​‌‌‌​‌​​​​‌​‌​​​​​‌​​​‌​​‌​​‌​​​​‌‌​​‌​‌​‌‌​‌‌​​​‌‌​‌‌​​​‌‌​‌‌‌‌​​‌​‌‌​​​​‌​​​​​​‌‌‌​‌‌‌​‌‌​‌‌‌‌​‌‌‌​​‌​​‌‌​‌‌​​​‌‌​​‌​​​​‌​​​​‌​​‌​​​​​‌‌‌‌​​​​‌​​‌‌‌‌‌‌​​‌‌​​​‌​​​​​​‌​​‌​​​‌​​​‌​‌​​‌​​​​‌​‌​

```

You can then run no code as usual:

```shell
$ python no_code.py
Hello, world! 😁

```

If, for some reason, you need to turn no code back into Python code:

```shell
$ yes_code no_code.py > some_code.py

$ cat some_code.py
print("Hello, world! 😁")

```

## Troubleshooting

If you get `SyntaxError: invalid syntax`, make sure the line `# coding: no` is present at the top of your script.

If you get `SyntaxError: encoding problem: no`, follow the steps below to make sure the `no` encoding is registered on startup:

1. Run `SITE_PACKAGES=$(python -c 'import sysconfig; print(sysconfig.get_path("purelib"))')` to get the path to the Python site-packages directory.
2. Run `echo "import no_code" > "$SITE_PACKAGES/no.pth"` to register the `no` encoding on startup.

> [!NOTE]
> If using PowerShell, use `$SITE_PACKAGES` instead of `SITE_PACKAGES` to assign the variable.

This issue is commonly encountered when installing `no-code` into the user site-packages.

## More details

Not satisfied with no code? The package also provides two functions to easily convert between something and nothing.

- `no_code.nothing()`: Transform something (a string or bytes-like object) into nothing.
- `no_code.something()`: Transform nothing into something (a string or bytes-like object).

The commands `no_code` and `yes_code` also accept input from `stdin` if no file is provided.

```shell
$ echo "print(bool(1))" | no_code | yes_code | python
True
```

## Credits

Inspired by [Kelsey Hightower](https://github.com/kelseyhightower/nocode), based on [INVISIBLE.js](https://aem1k.com/invisible/encoder/) by [Martin Kleppe](https://aem1k.com/).

## License

[MIT License](LICENSE.txt)
