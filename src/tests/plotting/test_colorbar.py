# tests/plotting/test_colorbar.py
import numpy as np
import pytest
from emcpy.plots.plots import GriddedPlot, Histogram
from emcpy.plots.create_plots import CreatePlot, CreateFigure


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


def test_single_cbar_only_on_last_subplot():
    left = CreatePlot(plot_layers=[Histogram(np.random.randn(1000))])
    left.add_colorbar(single_cbar=True, label="left")

    x = np.linspace(0, 1, 6)
    y = np.linspace(0, 1, 5)
    Z = np.add.outer(y, x)
    right = CreatePlot(plot_layers=[GriddedPlot(x, y, Z)])
    right.add_colorbar(single_cbar=True, label="right")

    fig = CreateFigure(nrows=1, ncols=2, figsize=(6, 3))
    fig.plot_list = [left, right]
    fig.create_figure()

    # 2 plot axes + 1 colorbar axes
    assert len(fig.fig.axes) == 3

def test_colorbar_ticks_integer_boundarynorm(tmp_path):
    import matplotlib.pyplot as plt
    import numpy as np
    from matplotlib.colors import BoundaryNorm

    fig, ax = plt.subplots()
    Z = np.arange(16).reshape(4, 4)
    boundaries = np.arange(0, 5)  # 0..4 → 4 bins of width 1
    m = ax.imshow(Z, norm=BoundaryNorm(boundaries, 256))

    cb = fig.colorbar(m, ax=ax, orientation="vertical")
    # call your helper directly if convenient, or rely on _plot_colorbar path
    # create_figure_instance._apply_integer_colorbar_ticks(cb)

    ticks = cb.get_ticks()
    labels = [t.get_text() for t in cb.ax.get_yticklabels()]
    assert np.allclose(ticks, [0.5, 1.5, 2.5, 3.5])
    assert labels == ["0", "1", "2", "3"]

