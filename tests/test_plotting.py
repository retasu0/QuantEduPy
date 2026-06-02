import matplotlib

matplotlib.use("Agg")

import matplotlib.pyplot as plt
import numpy as np
import pytest

import finsimlab as fsl


def test_plot_paths_returns_axes():
    paths = np.array(
        [
            [100.0, 100.0],
            [101.0, 99.0],
            [102.0, 98.0],
        ]
    )

    ax = fsl.plot_paths(paths, title="Test")

    assert ax.get_title() == "Test"
    assert ax.get_xlabel() == "Step"
    assert ax.get_ylabel() == "Value"
    plt.close(ax.figure)


def test_plot_paths_rejects_empty_path():
    with pytest.raises(ValueError, match="at least two time steps"):
        fsl.plot_paths(np.array([100.0]))

