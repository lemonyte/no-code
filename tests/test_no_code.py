from __future__ import annotations

import shutil
import subprocess
import sys
import sysconfig
from pathlib import Path
from typing import TYPE_CHECKING, NamedTuple

import pytest

from no_code import no_code, nothing, something

if TYPE_CHECKING:
    from collections.abc import Generator


class CodePair(NamedTuple):
    decoded: str
    encoded: str


class FilePair(NamedTuple):
    decoded: Path
    encoded: Path


ROOT_DIR = Path(__file__).parent.parent
SRC_DIR = ROOT_DIR / "src"
TEST_CODE_DIR = Path(__file__).parent / "code"
TEST_FILES = (
    FilePair(
        decoded=TEST_CODE_DIR / "decoded.py",
        encoded=TEST_CODE_DIR / "encoded.py",
    ),
    FilePair(
        decoded=TEST_CODE_DIR / "embedded_d.py",
        encoded=TEST_CODE_DIR / "embedded_e.py",
    ),
)
TEST_CODE = tuple(CodePair(*(file.read_text(encoding="utf-8") for file in file_pair)) for file_pair in TEST_FILES)
DECODED_TEST_STRING = "Hello, world! 😁"
ENCODED_TEST_STRING = "​‌​​‌​​​​‌‌​​‌​‌​‌‌​‌‌​​​‌‌​‌‌​​​‌‌​‌‌‌‌​​‌​‌‌​​​​‌​​​​​​‌‌‌​‌‌‌​‌‌​‌‌‌‌​‌‌‌​​‌​​‌‌​‌‌​​​‌‌​​‌​​​​‌​​​​‌​​‌​​​​​‌‌‌‌​​​​‌​​‌‌‌‌‌‌​​‌‌​​​‌​​​​​​‌"  # noqa: PLE2515


@pytest.fixture
def install_pth_file() -> Generator[None, None, None]:
    """Install the `no.pth` file in the site-packages directory to make the execute tests work."""
    pth_file = ROOT_DIR / "purelib" / "no.pth"
    site_packages = sysconfig.get_path("purelib")
    shutil.copy(pth_file, Path(sys.prefix) / site_packages)
    installed_pth_file = Path(sys.prefix) / site_packages / "no.pth"
    assert installed_pth_file.exists()
    yield
    installed_pth_file.unlink()


@pytest.mark.usefixtures("install_pth_file")
@pytest.mark.parametrize(("file_pair"), TEST_FILES)
def test_execute(file_pair: FilePair) -> None:
    args = (sys.executable, "-X", "utf8")
    decoded_process = subprocess.run(
        (*args, file_pair.decoded),
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    encoded_process = subprocess.run(
        (*args, file_pair.encoded),
        check=False,
        capture_output=True,
        encoding="utf-8",
    )
    assert decoded_process.stdout == encoded_process.stdout, f"{decoded_process.stderr}\n\n{encoded_process.stderr}"


def test_encode_str() -> None:
    assert nothing(DECODED_TEST_STRING) == ENCODED_TEST_STRING


def test_decode_str() -> None:
    assert something(ENCODED_TEST_STRING) == DECODED_TEST_STRING


def test_encode_bytes() -> None:
    assert nothing(DECODED_TEST_STRING.encode("utf-8")) == ENCODED_TEST_STRING.encode("utf-8")


def test_decode_bytes() -> None:
    assert something(ENCODED_TEST_STRING.encode("utf-8")) == DECODED_TEST_STRING.encode("utf-8")


def test_no_code() -> None:
    code_pair = TEST_CODE[0]
    assert no_code(code_pair.decoded) == code_pair.encoded


def test_registered_encoding() -> None:
    assert "test".encode("no").decode("no") == "test"
