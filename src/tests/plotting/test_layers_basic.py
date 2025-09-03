# tests/plotting/test_layers_basic.py
import numpy as np
import pytest
import matplotlib

from emcpy.plots.plots import (
    LinePlot, Histogram, Density, Scatter, BarPlot, HorizontalBar,
    GriddedPlot, ContourPlot, FilledContourPlot, BoxandWhiskerPlot,
    HorizontalSpan, SkewT,
)
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def _line_data():
    x1 = [0, 401, 1039, 2774, 2408]
    x2 = [500, 250, 710, 1515, 1212]
    x3 = [400, 150, 910, 1215, 850]
    y1 = [0, 2.5, 5, 7.5, 12.5]
    y2 = [1, 5, 6, 8, 10]
    y3 = [1, 4, 5.5, 9, 10.5]
    return x1, y1, x2, y2, x3, y3


def _hist_data():
    mu, sigma = 100, 15
    data1 = mu + sigma * np.random.randn(437)
    data2 = mu + sigma * np.random.randn(119)
    return data1, data2


def _scatter_data():
    rng = np.random.RandomState(0)
    x1 = rng.randn(100); y1 = rng.randn(100)
    rng = np.random.RandomState(1)
    x2 = rng.randn(30); y2 = rng.randn(30)
    return x1, y1, x2, y2


def _bar_data():
    x = ["a", "b", "c", "d", "e", "f"]
    heights = [5, 6, 15, 22, 24, 8]
    variance = [1, 2, 7, 4, 2, 3]
    x_pos = [i for i, _ in enumerate(x)]
    return x_pos, heights, variance


def _gridded_data():
    from scipy.ndimage import gaussian_filter
    x = np.linspace(0, 1, 51)
    y = np.linspace(0, 1, 51)
    r = np.random.RandomState(25)
    z = gaussian_filter(r.random_sample([50, 50]), sigma=5, mode="wrap")
    return x, y, z


def _contourf_data():
    x = np.linspace(-3, 15, 50).reshape(1, -1)
    y = np.linspace(-3, 15, 20).reshape(-1, 1)
    z = np.cos(x) * 2 - np.sin(y) * 2
    return x.flatten(), y.flatten(), z


def _skewt_data():
    from io import StringIO
    data_txt = '''
        978.0 345 7.8 0.8
        971.0 404 7.2 0.2
        946.7 610 5.2 -1.8
        944.0 634 5.0 -2.0
        925.0 798 3.4 -2.6
        911.8 914 2.4 -2.7
        906.0 966 2.0 -2.7
        877.9 1219 0.4 -3.2
        850.0 1478 -1.3 -3.7
        841.0 1563 -1.9 -3.8
        823.0 1736 1.4 -0.7
        813.6 1829 4.5 1.2
        809.0 1875 6.0 2.2
        798.0 1988 7.4 -0.6
        791.0 2061 7.6 -1.4
        783.9 2134 7.0 -1.7
        755.1 2438 4.8 -3.1
        727.3 2743 2.5 -4.4
        700.5 3048 0.2 -5.8
        700.0 3054 0.2 -5.8
        698.0 3077 0.0 -6.0
        687.0 3204 -0.1 -7.1
        648.9 3658 -3.2 -10.9
        631.0 3881 -4.7 -12.7
        600.7 4267 -6.4 -16.7
        592.0 4381 -6.9 -17.9
        577.6 4572 -8.1 -19.6
        555.3 4877 -10.0 -22.3
        536.0 5151 -11.7 -24.7
        533.8 5182 -11.9 -25.0
        500.0 5680 -15.9 -29.9
        472.3 6096 -19.7 -33.4
        453.0 6401 -22.4 -36.0
        400.0 7310 -30.7 -43.7
        399.7 7315 -30.8 -43.8
        387.0 7543 -33.1 -46.1
        382.7 7620 -33.8 -46.8
        342.0 8398 -40.5 -53.5
        320.4 8839 -43.7 -56.7
        318.0 8890 -44.1 -57.1
        310.0 9060 -44.7 -58.7
        306.1 9144 -43.9 -57.9
        305.0 9169 -43.7 -57.7
        300.0 9280 -43.5 -57.5
        292.0 9462 -43.7 -58.7
        276.0 9838 -47.1 -62.1
        264.0 10132 -47.5 -62.5
        251.0 10464 -49.7 -64.7
        250.0 10490 -49.7 -64.7
        247.0 10569 -48.7 -63.7
        244.0 10649 -48.9 -63.9
        243.3 10668 -48.9 -63.9
        220.0 11327 -50.3 -65.3
        212.0 11569 -50.5 -65.5
        210.0 11631 -49.7 -64.7
        200.0 11950 -49.9 -64.9
        194.0 12149 -49.9 -64.9
        183.0 12529 -51.3 -66.3
        164.0 13233 -55.3 -68.3
        152.0 13716 -56.5 -69.5
        150.0 13800 -57.1 -70.1
        136.0 14414 -60.5 -72.5
        132.0 14600 -60.1 -72.1
        131.4 14630 -60.2 -72.2
        128.0 14792 -60.9 -72.9
        125.0 14939 -60.1 -72.1
        119.0 15240 -62.2 -73.8
        112.0 15616 -64.9 -75.9
        108.0 15838 -64.1 -75.1
        107.8 15850 -64.1 -75.1
        105.0 16010 -64.7 -75.7
        103.0 16128 -62.9 -73.9
        100.0 16310 -62.5 -73.5
    '''
    import numpy as np
    from io import StringIO
    sound_data = StringIO(data_txt)
    p, h, T, Td = np.loadtxt(sound_data, unpack=True)
    return p, T, Td


def test_line_plot_basic(single_axes):
    x1, y1, x2, y2, x3, y3 = _line_data()
    lp1, lp2, lp3 = LinePlot(x1, y1), LinePlot(x2, y2), LinePlot(x3, y3)
    lp2.color, lp3.color = "tab:green", "tab:red"
    lp1.label = lp2.label = lp3.label = "line"
    plot = CreatePlot(plot_layers=[lp1, lp2, lp3])
    plot.add_legend(loc="upper right")
    fig, ax = single_axes(plot)
    assert len(ax.lines) == 3
    assert ax.get_legend() is not None


def test_line_plot_inverted_log_scale(single_axes):
    x = [1, 401, 1039, 2774, 2408, 512]  # avoid 0 for log
    y = [1, 45, 225, 510, 1200, 1820]
    plot = CreatePlot(plot_layers=[LinePlot(x, y)])
    plot.set_yscale("log"); plot.invert_yaxis()
    _, ax = single_axes(plot)
    assert ax.yaxis.get_scale() == "log"
    assert ax.yaxis_inverted()


def test_histogram_plot(single_axes):
    data1, _ = _hist_data()
    plot = CreatePlot(plot_layers=[Histogram(data1)])
    _, ax = single_axes(plot)
    assert len(ax.patches) > 0


def test_density_plot(single_axes):
    pytest.importorskip("seaborn")
    data1, _ = _hist_data()
    plot = CreatePlot(plot_layers=[Density(data1)])
    _, ax = single_axes(plot)
    assert len(ax.lines) + len(ax.collections) > 0


def test_scatter_plot(single_axes):
    x1, y1, *_ = _scatter_data()
    plot = CreatePlot(plot_layers=[Scatter(x1, y1)])
    _, ax = single_axes(plot)
    assert len(ax.collections) >= 1  # PathCollection


def test_bar_plot(single_axes):
    x_pos, heights, variance = _bar_data()
    bar = BarPlot(x_pos, heights); bar.yerr = variance
    plot = CreatePlot(plot_layers=[bar])
    _, ax = single_axes(plot)
    assert len(ax.patches) == len(x_pos)


def test_horizontal_bar_plot(single_axes):
    y_pos, widths, variance = _bar_data()
    bar = HorizontalBar(y_pos, widths); bar.xerr = variance
    plot = CreatePlot(plot_layers=[bar])
    _, ax = single_axes(plot)
    assert len(ax.patches) == len(y_pos)


def test_gridded_plot(single_axes):
    x, y, z = _gridded_data()
    plot = CreatePlot(plot_layers=[GriddedPlot(x, y, z)])
    _, ax = single_axes(plot)
    assert len(ax.collections) >= 1  # QuadMesh


def test_contour_and_contourf_with_colorbar():
    x, y, z = _contourf_data()
    cfp = FilledContourPlot(x, y, z); cfp.cmap = "Greens"
    cp = ContourPlot(x, y, z); cp.linestyles = "--"
    plot = CreatePlot(plot_layers=[cfp, cp]); plot.add_colorbar(orientation="vertical")
    fig = CreateFigure(); fig.plot_list = [plot]; fig.create_figure()
    assert len(fig.fig.axes) >= 2  # colorbar added


def test_box_and_whisker_plot(single_axes):
    np.random.seed(19680801)
    data = [np.random.normal(0, std, 100) for std in range(6, 10)]
    plot = CreatePlot(plot_layers=[BoxandWhiskerPlot(data)])
    _, ax = single_axes(plot)
    assert len(ax.artists) + len(ax.lines) > 0


def test_horizontal_span(single_axes):
    levs = np.linspace(975, 125, 23)
    rms = [1.8, 2.02, 2.36, 2.10, 2.21, 2.17, 2.08, 2.14, 2.14, 2.19,
           2.43, 2.38, 2.60, 2.66, 2.63, 2.72, 2.88, 3.99] + [np.nan]*5
    lp = LinePlot(rms[:len(levs)], levs)
    spans = [HorizontalSpan(levs[n]+5, levs[n]-5) for n in (5, 6, 8, 12)]
    plot = CreatePlot(plot_layers=[lp] + spans)
    _, ax = single_axes(plot)
    assert len(ax.patches) >= len(spans)


def test_skewt_projection(single_axes):
    p, T, Td = _skewt_data()
    tplot = SkewT(T, p); tdplot = SkewT(Td, p)
    plot = CreatePlot(plot_layers=[tplot, tdplot])
    _, ax = single_axes(plot)
    assert "SkewXAxes" in ax.__class__.__name__
