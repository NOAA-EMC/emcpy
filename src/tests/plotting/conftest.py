# ---------------------------------------------------------------------------
# Plotting test helpers (pytest auto-loaded for tests/plotting/)
#
# What this file does (no imports needed in tests):
# 1) Forces a headless Matplotlib backend (Agg) so tests run in CI/servers.
# 2) Makes plots deterministic by setting a separate MPL config/cache dir,
#    pinning a few rcParams (DPI/font size), and seeding NumPy RNG.
# 3) Closes all figures after each test to avoid leaks/flaky failures.
# 4) Provides small helpers:
#    - single_axes(plot): render a single CreatePlot and return (fig, ax)
#    - skip_if_no_cartopy: skip map tests if Cartopy isn't installed
#
# Usage examples in tests:
#   def test_something_with_ticks(single_axes):
#       plot = CreatePlot([...])
#       fig, ax = single_axes(plot)
#       assert len(ax.get_xticks()) == 6
#
#   def test_map_feature(skip_if_no_cartopy, single_axes):
#       skip_if_no_cartopy()
#       ...
# ---------------------------------------------------------------------------


import os
import pytest
import numpy as np
import matplotlib

# Force a headless backend for all plotting tests in this subtree
matplotlib.use("Agg", force=True)

import matplotlib.pyplot as plt
from emcpy.plots.create_plots import CreatePlot, CreateFigure


@pytest.fixture(scope="session", autouse=True)
def _stable_mpl_env(tmp_path_factory):
    """
    Make Matplotlib deterministic in CI:
    - Separate config/cache directory
    - Stable default DPI/font size (optional)
    """
    cfgdir = tmp_path_factory.mktemp("mplcfg")
    os.environ.setdefault("MPLCONFIGDIR", str(cfgdir))
    # Optionally pin some rcParams for reproducibility:
    import matplotlib as mpl
    old = mpl.rcParams.copy()
    mpl.rcParams.update({
        "figure.dpi": 100,
        "savefig.dpi": 100,
        "font.size": 10,
    })
    yield
    mpl.rcParams.update(old)


@pytest.fixture(autouse=True)
def _close_figures_after_each_test():
    """Ensure no figure leaks between tests."""
    yield
    plt.close("all")


@pytest.fixture(autouse=True)
def _seed_rng():
    """Deterministic random data for plotting tests."""
    np.random.seed(19680801)


@pytest.fixture
def single_axes():
    """
    Render a single CreatePlot to a figure and return (fig, ax).
    Usage:
        fig, ax = single_axes(plot)
    """
    def _run(plot: CreatePlot, **fig_kwargs):
        fig = CreateFigure(nrows=1, ncols=1, **fig_kwargs)
        fig.plot_list = [plot]
        fig.create_figure()
        ax = fig.fig.axes[0]
        return fig, ax
    return _run


@pytest.fixture
def skip_if_no_cartopy():
    """Return a callable that skips the test if Cartopy is unavailable."""
    def _skip():
        try:
            import cartopy  # noqa: F401
        except Exception:
            pytest.skip("Cartopy not installed/available for this environment.")
    return _skip
