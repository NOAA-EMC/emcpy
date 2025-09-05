# src/tests/plotting/test_mappables_colorbar.py
import numpy as np
from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.contour import ContourSet

from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.plots import Scatter, GriddedPlot, ContourPlot, FilledContourPlot, LinePlot, BarPlot


def test_scatter_with_color_returns_mappable_and_colorbar(single_axes):
    x = np.linspace(0, 1, 20)
    y = np.linspace(0, 1, 20)
    s = Scatter(x, y)
    s.c = np.linspace(0, 1, len(x))  # emulate "c=" kw; Scatter stores as attribute → forwarded
    s.cmap = "viridis"
    s.markersize = 25

    plot = CreatePlot(plot_layers=[s])
    plot.add_colorbar(label="scatter cb")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, PathCollection)
    # one plot axes + one colorbar axes
    assert len(fig.fig.axes) == 2


def test_scatter_plain_points_no_colorbar(single_axes):
    s = Scatter([0, 1, 2], [1, 2, 3])
    s.color = "tab:red"  # no scalar-mapped 'c='
    plot = CreatePlot(plot_layers=[s])
    plot.add_colorbar(label="ignored")
    fig, ax = single_axes(plot)

    # No scalar mappable => no colorbar axes added.
    assert len(fig.fig.axes) == 1


def test_gridded_returns_quadmesh_and_colorbar(single_axes):
    x = np.linspace(0, 1, 51)  # edges
    y = np.linspace(0, 1, 51)  # edges
    z = np.random.RandomState(0).rand(50, 50)  # centers
    gp = GriddedPlot(x, y, z)
    gp.cmap = "plasma"

    plot = CreatePlot(plot_layers=[gp])
    plot.add_colorbar(label="gridded cb")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, QuadMesh)
    assert len(fig.fig.axes) == 2


def test_contour_and_contourf_last_mappable_wins(single_axes):
    # Make a simple field
    x = np.linspace(-3, 3, 40)
    y = np.linspace(-3, 3, 30)
    X, Y = np.meshgrid(x, y)
    Z = np.cos(X) * np.sin(Y)

    cf = FilledContourPlot(x, y, Z)
    cf.cmap = "viridis"
    c = ContourPlot(x, y, Z)
    c.colors = "k"
    c.levels = np.linspace(-1, 1, 11)

    # Order matters: add contourf then contour → last mappable should be the contour set
    plot = CreatePlot(plot_layers=[cf, c])
    plot.add_colorbar(label="combo cb")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, ContourSet)
    assert len(fig.fig.axes) == 2


def test_single_cbar_on_last_subplot_only():
    plots = []
    for seed in (0, 1, 2, 3):
        rng = np.random.RandomState(seed)
        x = np.linspace(0, 1, 40)
        y = np.linspace(0, 1, 30)
        X, Y = np.meshgrid(x, y)
        Z = rng.rand(*Y.shape)

        cf = FilledContourPlot(x, y, Z)
        cf.cmap = "viridis"
        p = CreatePlot(plot_layers=[cf])
        p.add_colorbar(orientation="horizontal", single_cbar=True, label="CF")
        plots.append(p)

    fig = CreateFigure(nrows=2, ncols=2, figsize=(8, 6))
    fig.plot_list = plots
    fig.create_figure()

    # 4 plot axes + 1 colorbar axes
    assert len(fig.fig.axes) == 5


def test_lineplot_produces_no_mappable(single_axes):
    lp = LinePlot([0, 1, 2], [0, 1, 4])
    plot = CreatePlot(plot_layers=[lp])
    fig, ax = single_axes(plot)
    assert fig._last_mappable_for_ax(ax) is None


def test_colorbar_picks_last_valid_mappable_and_ignores_bar(single_axes):
    # Non-mappable first
    bar = BarPlot(x=[0, 1, 2], height=[1, 2, 3])
    # Mappable second (scatter with 'c' set)
    sc = Scatter([0, 1, 2], [0.0, 1.0, 0.5])
    sc.c = np.array([10, 20, 30])

    plot = CreatePlot(plot_layers=[bar, sc])
    plot.add_colorbar(label="units", fontsize=10)

    fig, ax = single_axes(plot)

    # One extra axes (the colorbar)
    assert len(fig.fig.axes) == 2

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, PathCollection)
    arr = m.get_array()
    assert arr is not None and arr.size == 3
