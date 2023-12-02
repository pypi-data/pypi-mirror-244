from . import _lib  # type: ignore


def sum_as_string(a: int, b: int) -> str:
    """return the sum as a string"""
    return _lib.sum_as_string(a, b)  # pylint: disable=no-member
