#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Wed Mar  1 11:29:06 2023

@author: A. Plaçais
fork from Julien Hillairet JH218595
"""
import numpy as np


def printc(*args, color='cyan'):
    """Print colored messages."""
    dict_c = {
        'red': '\x1B[31m',
        'blue': '\x1b[34m',
        'green': '\x1b[32m',
        'magenta': '\x1b[35m',
        'cyan': '\x1b[36m',
        'normal': '\x1b[0m',
    }
    print(dict_c[color] + args[0] + dict_c['normal'], end=' ')
    for arg in args[1:]:
        print(arg, end=' ')
    print('')


def fmt_array(p_s: np.ndarray) -> str:
    """
    Helper to give Spark3D a list of powers with the proper format.

    Parameters
    ----------
    p_s : np.ndarray
        Array of powers.

    Returns
    -------
    str
        List of floats as understood by SPARK3D.

    """
    s_p_s = str(tuple(p_s))
    return s_p_s.replace(', ', ';')
