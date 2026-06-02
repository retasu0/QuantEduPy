"""Small helpers for long-only portfolio rebalancing examples."""

from __future__ import annotations

import numpy as np

from finsimlab.portfolio.metrics import _as_vector, _validate_weights


def rebalance_portfolio(values, target_weights) -> np.ndarray:
    """Return target asset values after rebalancing to ``target_weights``.

    ``values`` are current asset values. The total portfolio value is preserved
    and allocated according to the target long-only weights.
    """
    current_values = _as_vector("values", values)
    if np.any(current_values < 0):
        raise ValueError("values must be greater than or equal to 0.")
    total_value = float(np.sum(current_values))
    if total_value <= 0:
        raise ValueError("values must contain a positive total value.")

    target_weights = _validate_weights(
        target_weights,
        n_assets=current_values.shape[0],
    )
    return total_value * target_weights
