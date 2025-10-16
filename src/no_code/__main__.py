import sys
from pathlib import Path

from no_code.no import no_code, something


def no_code_cmd() -> None:
    code = Path(sys.argv[1]).read_text(encoding="utf-8") if len(sys.argv) > 1 else sys.stdin.read()
    print(no_code(code))


def yes_code_cmd() -> None:
    code = Path(sys.argv[1]).read_text(encoding="no-code") if len(sys.argv) > 1 else something(sys.stdin.read())
    print(code.removeprefix("# coding: no\n"))


if __name__ == "__main__":
    no_code_cmd()
