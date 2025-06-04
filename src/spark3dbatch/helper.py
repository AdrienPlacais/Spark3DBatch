"""Provide helper functions."""

import math
from typing import Literal

from numpy.typing import NDArray

COLORS = Literal["red", "blue", "green", "magenta", "cyan", "normal"]


def e_acc_to_power(
    e_acc: NDArray, freq: float, r_q: float, l_acc: float
) -> NDArray:
    r"""Convert array of accelerating fields to RMS powers.

    .. important::
       SPARK3D uses peak power, but their definition is non-conventional.
       With single carriers, it corresponds to the classic RMS power, or half
       the classic peak power.

    Parameters
    ----------
    e_acc :
        Array of accelerating fields in :unit:`V/m`.
    freq :
        Frequency in :unit:`Hz`.
    r_q :
        Shunt impedance over quality factor ratio in :unit:`\\Omega`.
    l_acc :
        Accelerating length in :unit:`m`.

    Returns
    -------
        Array of powers in :unit:`W`.

    """
    omega_0 = 2.0 * math.pi * freq
    peak_power = (l_acc * e_acc) ** 2 / (omega_0 * r_q)
    return 0.5 * peak_power


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
