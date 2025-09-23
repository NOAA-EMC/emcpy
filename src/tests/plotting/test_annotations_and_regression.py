# tests/plotting/test_annotations_and_regression.py
import numpy as np

from emcpy.plots.plots import Scatter, LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def test_stats_annotation_text_present():
    x = [0, 1, 2]
    y = [2, 3, 5]
    plot = CreatePlot(plot_layers=[LinePlot(x, y)])
    stats = {"nobs": 3, "vmin": 2, "vmax": 5}
    plot.add_stats_dict(stats_dict=stats, yloc=-0.2)
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert any("nobs:" in t.get_text() for t in ax.texts)


def test_add_text_axcoords_adds_artist():
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    plot.add_text(0.5, 0.5, "Hello", transform="axcoords", fontsize=8)
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert any(t.get_text() == "Hello" for t in ax.texts)


def test_scatter_linear_regression_adds_line_and_label():
    rng = np.random.RandomState(42)
    x = np.linspace(0, 10, 50)
    y = 2.0 * x + 1.0 + rng.normal(scale=0.5, size=x.size)
    s = Scatter(x, y)
    s.do_linear_regression = True
    # Optional style overrides are supported; leave default color so line shows
    plot = CreatePlot(plot_layers=[s])
    plot.add_legend()
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    # one regression line should have been added
    assert len(ax.lines) >= 1
    # legend should include the regression label (starts with 'y = ...')
    leg = ax.get_legend()
    labels = [t.get_text() for t in leg.get_texts()]
    assert any(label.startswith("y = ") for label in labels)


def test_scatter_legend_handles_have_fixed_size():
    s = Scatter([0, 1, 2], [1, 2, 3])
    s.label = "points"
    plot = CreatePlot(plot_layers=[s])
    plot.add_legend()
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    leg = ax.get_legend()

    handles = getattr(leg, "legend_handles", None) or getattr(leg, "legendHandles", [])
    sizes = []
    for h in handles:
        if hasattr(h, "get_sizes"):
            sizes.extend(h.get_sizes())
        elif hasattr(h, "_sizes"):
            sizes.extend(h._sizes)

    assert sizes and all(abs(sz - 20) < 1e-6 for sz in sizes)
