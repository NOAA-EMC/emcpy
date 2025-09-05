# tests/plotting/test_ticks.py
import pytest
import numpy as np
from datetime import datetime, timedelta
import matplotlib.dates as mdates
from matplotlib.ticker import NullLocator

from emcpy.plots.plots import LinePlot
from emcpy.plots.map_plots import MapScatter
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def test_datetime_xticks_replace_autos(single_axes):
    lp = LinePlot([0, 1, 2, 3, 4, 5], [1, 1, 2, 3, 5, 8])
    start = datetime(2025, 9, 2, 0, 0)
    ticks = [start + timedelta(hours=h) for h in range(6)]
    plot = CreatePlot(plot_layers=[lp])
    plot.set_xticks(ticks=ticks, date_format="%H:%M")
    _, ax = single_axes(plot)
    assert len(ax.get_xticks()) == len(ticks)
    assert isinstance(ax.xaxis.get_major_formatter(), mdates.DateFormatter)


def test_xticklabels_length_validation():
    lp = LinePlot([0, 1, 2, 3, 4], [1, 2, 3, 4, 5])
    plot = CreatePlot(plot_layers=[lp])
    plot.set_xticks(ticks=[0, 1, 2, 3, 4])
    plot.set_xticklabels(labels=["a", "b", "c"])  # wrong count
    fig = CreateFigure()
    fig.plot_list = [plot]
    with pytest.raises(ValueError, match="Len of xtick labels"):
        fig.create_figure()


def test_minor_labels_forbidden():
    lp = LinePlot([0, 1, 2], [0, 1, 2])
    plot = CreatePlot(plot_layers=[lp])
    plot.set_xticks(ticks=[0, 1, 2])
    plot.set_xticklabels(labels=["x", "y", "z"], minor=True)
    fig = CreateFigure()
    fig.plot_list = [plot]
    with pytest.raises(ValueError, match="MINOR tick labels"):
        fig.create_figure()


def test_yaxis_date_format_is_supported(single_axes):
    lp = LinePlot([0, 1, 2, 3], [0, 1, 2, 3])
    start = datetime(2025, 9, 2, 0, 0)
    yticks = [start + timedelta(hours=h) for h in range(4)]
    plot = CreatePlot(plot_layers=[lp])
    plot.set_yticks(ticks=yticks, date_format="%H:%M")
    _, ax = single_axes(plot)
    assert len(ax.get_yticks()) == len(yticks)
    assert isinstance(ax.yaxis.get_major_formatter(), mdates.DateFormatter)


def test_setting_major_ticks_clears_minor_locator_by_default(single_axes):
    lp = LinePlot([0, 1, 2], [0, 1, 2])
    plot = CreatePlot(plot_layers=[lp])
    plot.set_xticks(ticks=[0.5, 1.5], minor=True)
    plot.set_xticks(ticks=[0, 1, 2])  # should clear minor
    _, ax = single_axes(plot)
    assert isinstance(ax.xaxis.get_minor_locator(), NullLocator)


@pytest.mark.skipif(pytest.importorskip("cartopy", reason="Cartopy required") is None, reason="Cartopy missing")
def test_geoaxes_ticks_use_cartopy_formatters(single_axes):
    layer = MapScatter(latitude=np.array([0.0]), longitude=np.array([0.0]))
    plot = CreatePlot(plot_layers=[layer], projection="plcarr", domain="global")
    plot.set_xticks(ticks=[-180, -90, 0, 90, 180])
    plot.set_yticks(ticks=[-90, -45, 0, 45, 90])

    fig, ax = single_axes(plot)

    from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
    assert isinstance(ax.xaxis.get_major_formatter(), LongitudeFormatter)
    assert isinstance(ax.yaxis.get_major_formatter(), LatitudeFormatter)
