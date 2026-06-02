"""Shared validation helpers for simulation modules."""

from __future__ import annotations

from numbers import Real

import numpy as np


def make_rng(seed: int | None) -> np.random.Generator:
    """Create a NumPy random generator from an optional seed."""
    return np.random.default_rng(seed)


def require_real(name: str, value: Real) -> float:
    """Return a finite float or raise a beginner-friendly error."""
    if not isinstance(value, Real):
        raise TypeError(f"{name} must be a real number.")

    result = float(value)
    if not np.isfinite(result):
        raise ValueError(f"{name} must be finite.")

    return result


def require_positive(name: str, value: Real) -> float:
    """Return a positive finite float."""
    result = require_real(name, value)
    if result <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return result


def require_non_negative(name: str, value: Real) -> float:
    """Return a non-negative finite float."""
    result = require_real(name, value)
    if result < 0:
        raise ValueError(f"{name} must be greater than or equal to 0.")
    return result


def require_positive_int(name: str, value: int) -> int:
    """Return a positive integer."""
    if not isinstance(value, int):
        raise TypeError(f"{name} must be an integer.")
    if value <= 0:
        raise ValueError(f"{name} must be greater than 0.")
    return value

