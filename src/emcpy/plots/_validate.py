# src/emcpy/plots/_validate.py
from __future__ import annotations
import numpy as np

__all__ = ["require_1d", "require_2d", "require_same_length", "require_same_shape2d"]


def require_1d(name, a):
    arr = np.asarray(a)
    if arr.ndim != 1:
        raise ValueError(f"{name} must be 1D; got shape {arr.shape}.")
    return arr


def require_2d(name, a):
    arr = np.asarray(a)
    if arr.ndim != 2:
        raise ValueError(f"{name} must be 2D; got shape {arr.shape}.")
    return arr


def require_same_length(a_name, a, b_name, b):
    if np.asarray(a).shape[0] != np.asarray(b).shape[0]:
        raise ValueError(f"{a_name} and {b_name} must have same length; "
                         f"got {len(a)} vs {len(b)}.")


def require_same_shape2d(A_name, A, B_name, B):
    if np.asarray(A).shape != np.asarray(B).shape:
        raise ValueError(f"{A_name} and {B_name} must have the same shape; "
                         f"got {np.asarray(A).shape} vs {np.asarray(B).shape}.")
