"""Value at Risk and Conditional Value at Risk calculations."""

from __future__ import annotations

import numpy as np

from finsimlab.risk.metrics import _scalar_or_array
from finsimlab.risk.returns import _as_finite_array, _normalize_axis


def _require_confidence_level(confidence_level: float) -> float:
    result = float(confidence_level)
    if not np.isfinite(result):
        raise ValueError("confidence_level must be finite.")
    if result <= 0 or result >= 1:
        raise ValueError("confidence_level must be between 0 and 1.")
    return result


def value_at_risk(
    losses,
    *,
    confidence_level: float = 0.95,
    axis: int | None = None,
) -> np.ndarray | float:
    """Calculate VaR from a loss distribution.

    FinSimLab treats losses as positive values. The returned VaR is therefore a
    positive loss amount at the requested confidence level.
    """
    values = _as_finite_array("losses", losses)
    confidence_level = _require_confidence_level(confidence_level)
    if axis is not None:
        axis = _normalize_axis(axis, values.ndim)

    result = np.quantile(values, confidence_level, axis=axis)
    return _scalar_or_array(result)


def _cvar_1d(values: np.ndarray, confidence_level: float) -> float:
    var_value = float(np.quantile(values, confidence_level))
    tail = values[values >= var_value]
    return float(np.mean(tail))


def conditional_value_at_risk(
    losses,
    *,
    confidence_level: float = 0.95,
    axis: int | None = None,
) -> np.ndarray | float:
    """Calculate CVaR as the average tail loss at or above VaR.

    FinSimLab fixes the tail rule as ``losses >= VaR``. This makes the result
    easy to explain for small educational examples and avoids an empty tail
    when the quantile equals the maximum observed loss.
    """
    values = _as_finite_array("losses", losses)
    confidence_level = _require_confidence_level(confidence_level)

    if axis is None:
        return _cvar_1d(values.ravel(), confidence_level)

    axis = _normalize_axis(axis, values.ndim)
    result = np.apply_along_axis(_cvar_1d, axis, values, confidence_level)
    return _scalar_or_array(result)

