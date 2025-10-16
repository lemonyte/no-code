from codecs import CodecInfo, register
from encodings import utf_8
from pathlib import Path
from typing import TYPE_CHECKING, overload

if TYPE_CHECKING:
    from _typeshed import ReadableBuffer


__all__ = ("no_code", "nothing", "something")
BYTE_SIZE = 8
ZERO_WIDTH_SPACE = chr(0x200B)
ZERO_WIDTH_NON_JOINER = chr(0x200C)


def no_code(src: str, /) -> str:
    """Turn your code into no code."""
    return f"# coding: no\n{nothing(src)}\n"


@overload
def nothing(data: str, /) -> str: ...
@overload
def nothing(data: "ReadableBuffer", /, *, errors: str = "strict") -> bytes: ...
def nothing(data: "str | ReadableBuffer", /, *, errors: str = "strict") -> str | bytes:
    """Transform a string or bytes-like object into nothing."""
    as_string = isinstance(data, str)
    data_bytes = data.encode("utf-8", errors) if as_string else bytes(data)
    transformed = "".join(format(byte, "08b") for byte in data_bytes).translate({48: 0x200B, 49: 0x200C})
    return transformed if as_string else transformed.encode("utf-8", errors)


@overload
def something(data: str, /) -> str: ...
@overload
def something(data: "ReadableBuffer", /, *, errors: str = "strict") -> bytes: ...
def something(data: "str | ReadableBuffer", /, *, errors: str = "strict") -> str | bytes:
    """Transform nothing into a string or bytes-like object."""
    as_string = isinstance(data, str)
    data_str = data if as_string else bytes(data).decode("utf-8", errors)
    chars = bytearray()
    bits = []
    for char in data_str:
        if char == ZERO_WIDTH_SPACE:
            bits.append("0")
        elif char == ZERO_WIDTH_NON_JOINER:
            bits.append("1")
        else:
            chars.extend(char.encode("utf-8", errors))
        if len(bits) == BYTE_SIZE:
            chars.append(int("".join(bits), base=2))
            bits.clear()
    return chars.decode("utf-8", errors) if as_string else bytes(chars)


def encode(input: str, errors: str | None = None, /) -> tuple[bytes, int]:
    return utf_8.encode(nothing(input), errors)


def decode(input: "ReadableBuffer", errors: str | None = "strict") -> tuple[str, int]:
    return utf_8.decode(something(input), errors)


class IncrementalDecoder(utf_8.IncrementalDecoder):
    def decode(self, input: "ReadableBuffer", final: bool = False) -> str:  # noqa: FBT001 FBT002
        self.buffer += input
        if final:
            decoded, _ = decode(self.buffer)
            self.buffer = b""
            return decoded
        return ""


@register
def search_function(encoding_name: str) -> CodecInfo | None:
    if encoding_name in ("no", "no_code", "invisible"):
        return CodecInfo(
            name="no",
            encode=encode,
            decode=decode,
            incrementaldecoder=IncrementalDecoder,
        )
    return None


if __name__ == "__main__":
    print(no_code(Path(__file__).read_text(encoding="utf-8")))
