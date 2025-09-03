# tests/plotting/test_errors_axes_io.py
import os
import pytest
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot, Scatter
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def test_set_xscale_invalid_raises():
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    with pytest.raises(ValueError, match="requested scale"):
        plot.set_xscale("test")


def test_set_yscale_invalid_raises():
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    with pytest.raises(ValueError, match="requested scale"):
        plot.set_yscale("test")


def test_save_figure_creates_directories(tmp_path):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    out = tmp_path / "nested" / "deep" / "figure.png"
    fig.save_figure(str(out))
    assert out.exists()


def test_close_figure_closes_handle():
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    num = fig.fig.number
    fig.close_figure()
    assert not plt.fignum_exists(num)


def test_sharex_sharey_hide_ticklabels():
    p1 = CreatePlot(plot_layers=[LinePlot([0, 1],[0, 1])])
    p2 = CreatePlot(plot_layers=[LinePlot([0, 1],[1, 2])])
    fig = CreateFigure(nrows=2, ncols=1, sharex=True, sharey=True)
    fig.plot_list = [p1, p2]
    fig.create_figure()
    ax0, ax1 = fig.fig.axes
    assert all(not t.get_visible() for t in ax0.get_xticklabels())  # hidden on top
    assert any(t.get_visible() for t in ax1.get_xticklabels())      # visible on bottom


def test_invalid_map_feature_raises(skip_if_no_cartopy):
    skip_if_no_cartopy()
    plot = CreatePlot()
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_map_features(["not_a_real_feature"])
    fig = CreateFigure()
    fig.plot_list = [plot]
    with pytest.raises(TypeError, match="is not a valid map feature"):
        fig.create_figure()
