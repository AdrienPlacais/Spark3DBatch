"""Provide helper functions."""

from typing import Literal

from numpy.typing import NDArray

COLORS = Literal["red", "blue", "green", "magenta", "cyan", "normal"]


def printc(*args: str, color: COLORS = "cyan"):
    """Print colored messages."""
    dict_c = {
        "red": "\x1b[31m",
        "blue": "\x1b[34m",
        "green": "\x1b[32m",
        "magenta": "\x1b[35m",
        "cyan": "\x1b[36m",
        "normal": "\x1b[0m",
    }
    print(dict_c[color] + args[0] + dict_c["normal"], end=" ")
    for arg in args[1:]:
        print(arg, end=" ")
    print("")


def fmt_array(p_s: NDArray) -> str:
    """Convert numpy array to a string that SPARK3D can understand.

    Parameters
    ----------
    p_s :
        Array of powers.

    Returns
    -------
    str
        List of floats as understood by SPARK3D.

    """
    return ";".join(f"{x:.12g}" for x in p_s)
