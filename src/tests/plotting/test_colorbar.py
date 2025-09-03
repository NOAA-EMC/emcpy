# tests/plotting/test_colorbar.py
import numpy as np
from emcpy.plots.plots import GriddedPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


_NEED_FIX = not (hasattr(Axes, "is_last_row") and hasattr(Axes, "is_last_col"))


@pytest.mark.xfail(
    _NEED_FIX,
    reason="Waiting for GridSpec-based last-row/col helpers in CreateFigure (next PR).",
    strict=False  # don't break CI if it unexpectedly passes
)
def test_per_axes_colorbar_adds_axes_and_label():
    x = np.linspace(0, 1, 30)
    y = np.linspace(0, 1, 20)
    z = np.outer(np.sin(np.pi*x), np.cos(np.pi*y)).T
    gp = GriddedPlot(x, y, z)

    plot = CreatePlot(plot_layers=[gp])
    plot.add_colorbar(orientation="vertical", label="colorbar label", fontsize=12)

    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()

    # 1 plot axes + 1 colorbar axes
    assert len(fig.fig.axes) == 2
    cbar_ax = fig.fig.axes[-1]
    # Vertical colorbar label should be y-label
    assert cbar_ax.get_ylabel() == "colorbar label"


def test_single_colorbar_on_last_subplot_only():
    plots = []
    for seed in (0, 1, 2, 3):
        rng = np.random.RandomState(seed)
        x = np.linspace(0, 1, 20)
        y = np.linspace(0, 1, 20)
        z = rng.rand(20, 20)
        gp = GriddedPlot(x, y, z)
        p = CreatePlot(plot_layers=[gp])
        p.add_colorbar(orientation="horizontal", single_cbar=True)
        plots.append(p)

    fig = CreateFigure(nrows=2, ncols=2, figsize=(8, 6))
    fig.plot_list = plots
    fig.create_figure()

    # 4 plot axes + 1 colorbar axes
    assert len(fig.fig.axes) == 5
