"""Risk management tools for educational simulations."""

from finsimlab.risk.metrics import volatility
from finsimlab.risk.plots import plot_loss_distribution
from finsimlab.risk.returns import calculate_returns, losses_from_returns
from finsimlab.risk.var import conditional_value_at_risk, value_at_risk

__all__ = [
    "calculate_returns",
    "conditional_value_at_risk",
    "losses_from_returns",
    "plot_loss_distribution",
    "value_at_risk",
    "volatility",
]

