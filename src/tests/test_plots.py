import numpy as np
from scipy.ndimage.filters import gaussian_filter
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot, VerticalLine, \
    Histogram, Density, Scatter, HorizontalLine, BarPlot, \
    GriddedPlot, ContourPlot, FilledContourPlot, HorizontalBar, \
    BoxandWhiskerPlot, HorizontalSpan, SkewT
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def test_line_plot():
    # create line plot

    x1, y1, x2, y2, x3, y3 = _getLineData()
    lp1 = LinePlot(x1, y1)
    lp1.label = 'line 1'

    lp2 = LinePlot(x2, y2)
    lp2.color = 'tab:green'
    lp2.label = 'line 2'

    lp3 = LinePlot(x3, y3)
    lp3.color = 'tab:red'
    lp3.label = 'line 3'

    plot1 = CreatePlot()
    plot1.plot_layers = [lp1, lp2, lp3]
    plot1.add_title('Test Line Plot')
    plot1.add_xlabel('X Axis Label')
    plot1.add_ylabel('Y Axis Label')
    plot1.add_legend(loc='upper right')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_line_plot.png')


# def test_line_plot_2_x_axes():
#     # create line plot with two sets of axes
#     # sharing a common y axis

#     x1, y1, x2, y2, x3, y3 = _getLineData()
#     lp1 = LinePlot(x1, y1)
#     lp1.label = 'line 1'

#     lp2 = LinePlot(x2, y2)
#     lp2.color = 'tab:green'
#     lp2.label = 'line 2'
#     lp2.use_shared_ay()

#     lp3 = LinePlot(x3, y3)
#     lp3.color = 'tab:red'
#     lp3.label = 'line 3'
#     lp3.use_shared_ay()

#     myplt = CreatePlot()
#     plt_list = [lp1, lp2, lp3]
#     myplt.draw_data(plt_list)

#     myplt.add_title(label='Test Line Plot, 2 X Axes ')
#     myplt.add_xlabel(xlabel='X Axis Label')
#     myplt.add_ylabel(ylabel='Y Axis Label')
#     myplt.add_xlabel(xlabel='Secondary X Axis Label', xaxis='secondary')

#     fig = myplt.return_figure()
#     fig.add_legend(plotobj=myplt, loc="upper right")
#     fig.savefig('test_line_plot_2_x_axes.png')


# def test_line_plot_2_y_axes():
#     # create line plot with two sets of axes
#     # sharing a common x axis

#     x1, y1, x2, y2, x3, y3 = _getLineData()

#     lp1 = LinePlot(x1, y1)
#     lp1.label = 'line 1'

#     lp2 = LinePlot(x2, y2)
#     lp2.color = 'tab:green'
#     lp2.label = 'line 2'
#     lp2.use_shared_ax()

#     lp3 = LinePlot(x3, y3)
#     lp3.color = 'tab:red'
#     lp3.label = 'line 3'

#     myplt = CreatePlot()
#     plt_list = [lp1, lp2, lp3]
#     myplt.draw_data(plt_list)

#     myplt.add_title(label='Test Line Plot, 2 Y Axes ')
#     myplt.add_xlabel(xlabel='X Axis Label')
#     myplt.add_ylabel(ylabel='Y Axis Label')
#     myplt.add_ylabel(ylabel='Secondary Y Axis Label', yaxis='secondary')

#     fig = myplt.return_figure()
#     fig.add_legend(plotobj=myplt, loc='upper right')
#     fig.savefig('test_line_plot_2_y_axes.png')


def test_line_plot_inverted_log_scale():
    # create a line plot with an inverted, log scale y axis

    x = [0, 401, 1039, 2774, 2408, 512]
    y = [0, 45, 225, 510, 1200, 1820]
    lp = LinePlot(x, y)
    plt_list = [lp]

    plot1 = CreatePlot()
    plot1.plot_layers = [lp]
    plot1.add_title(label='Test Line Plot, Inverted Log Scale')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.set_yscale('log')
    plot1.invert_yaxis()

    ylabels = [0, 50, 100, 500, 1000, 2000]
    plot1.set_yticklabels(labels=ylabels)

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_line_inverted_log_scale.png')


def test_histogram_plot():
    # create histogram plot

    data1, data2 = _getHistData()
    hst1 = Histogram(data1)

    plot1 = CreatePlot()
    plot1.plot_layers = [hst1]
    plot1.add_title(label='Test Histogram Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_histogram_plot.png')


# def test_histogram_plot_2_x_axes():
#     # create histogram plot on two pair of axes with
#     # a shared y axis

#     data1, data2 = _getHistData()
#     hst1 = Histogram(data1)
#     hst2 = Histogram(data2)

#     hst2.color = 'tab:red'
#     hst2.use_shared_ay()

#     myplt = CreatePlot()
#     plt_list = [hst1, hst2]
#     myplt.draw_data(plt_list)

#     myplt.add_title(label='Test Histogram Plot, 2 X Axes')
#     myplt.add_xlabel(xlabel='X Axis Label')
#     myplt.add_ylabel(ylabel='Y Axis Label')
#     myplt.add_xlabel(xlabel='Secondary X Axis Label', xaxis='secondary')

#     fig = myplt.return_figure()
#     fig.savefig('test_histogram_plot_2_x_axes.png')


def test_density_plot():
    # Test density plot

    data1, data2 = _getHistData()
    den1 = Density(data1)

    plot1 = CreatePlot()
    plot1.plot_layers = [den1]
    plot1.add_title(label='Test Density Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_density_plot.png')


def test_scatter_plot():
    # create scatter plot

    x1, y1, x2, y2 = _getScatterData()
    sctr1 = Scatter(x1, y1)

    plot1 = CreatePlot()
    plot1.plot_layers = [sctr1]
    plot1.add_title(label='Test Scatter Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_scatter_plot.png')


# def test_scatter_plot_2_y_axes():
#     # create scatter plot using two sets of axes
#     # with a shared x axis

#     x1, y1, x2, y2 = _getScatterData()
#     sctr1 = Scatter(x1, y1)

#     sctr2 = Scatter(x2, y2)
#     sctr2.color = 'tab:blue'
#     sctr2.use_shared_ax()

#     myplt = CreatePlot()
#     plt_list = [sctr1, sctr2]
#     myplt.draw_data(plt_list)

#     myplt.add_title(label='Test Scatter Plot, 2 Y Axes')
#     myplt.add_xlabel(xlabel='X Axis Label')
#     myplt.add_ylabel(ylabel='Y Axis Label')
#     myplt.add_ylabel(ylabel='Secondary Y Axis Label', yaxis='secondary')

#     fig = myplt.return_figure()
#     fig.savefig('test_scatter_plot_2_y_axes.png')


def test_bar_plot():
    # Create bar plot with error bars

    x_pos, heights, variance = _getBarData()

    bar = BarPlot(x_pos, heights)
    bar.color = 'tab:red'
    bar.yerr = variance
    bar.capsize = 5.

    plot1 = CreatePlot()
    plot1.plot_layers = [bar]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title("Test Bar Plot")

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_bar_plot.png')


def test_gridded_plot():
    # Create gridded plot

    x, y, z = _getGriddedData()

    gp = GriddedPlot(x, y, z)
    gp.cmap = 'plasma'

    plot1 = CreatePlot()
    plot1.plot_layers = [gp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Test Gridded Plot')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_gridded_plot.png')


def test_contours_plot():
    # Create contourf plot

    x, y, z = _getContourfData()

    cfp = FilledContourPlot(x, y, z)
    cfp.cmap = 'Greens'

    cp = ContourPlot(x, y, z)
    cp.linestyles = '--'

    plot1 = CreatePlot()
    plot1.plot_layers = [cfp, cp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Test Contour and Contourf Plot')
    plot1.add_colorbar(orientation='vertical')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_contour_and_contourf_plot.png')


def test_box_and_whisker_plot():
    # Create box and whisker plot

    data = _getBoxPlotData()

    bwp = BoxandWhiskerPlot(data)

    plot1 = CreatePlot()
    plot1.plot_layers = [bwp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Test Box and Whisker Plot')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_box_and_whisker_plot.png')


def test_horizontal_bar_plot():
    # Create horizontal bar plot

    y_pos, widths, variance = _getBarData()

    bar = HorizontalBar(y_pos, widths)
    bar.color = 'tab:green'
    bar.xerr = variance
    bar.capsize = 5

    plot1 = CreatePlot()
    plot1.plot_layers = [bar]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title("Test Horizontal Bar Plot")

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_horizontal_bar_plot.png')


def test_add_logo():
    # Test adding logos
    x1, y1, x2, y2, x3, y3 = _getLineData()
    lp1 = LinePlot(x1, y1)
    lp1.label = 'line 1'

    plot1 = CreatePlot()
    plot1.plot_layers = [lp1]
    plot1.add_title('Test Line Plot')
    plot1.add_xlabel('X Axis Label')
    plot1.add_ylabel('Y Axis Label')
    plot1.add_legend(loc='upper right')

    fig = CreateFigure()
    fig.plot_list = [plot1, plot1, plot1, plot1]
    fig.nrows = 2
    fig.ncols = 2
    fig.figsize = (12, 8)
    fig.create_figure()
    fig.tight_layout()
    fig.plot_logo(loc='lower right', zoom=0.9, alpha=0.2)
    fig.save_figure('test_add_logo.png')


def test_multi_subplot():
    # Create a figure with four different subplots

    # Line plot
    x1, y1, x2, y2, x3, y3 = _getLineData()
    lp1 = LinePlot(x1, y1)
    lp1.label = 'line 1'

    lp2 = LinePlot(x2, y2)
    lp2.color = 'tab:green'
    lp2.label = 'line 2'

    lp3 = LinePlot(x3, y3)
    lp3.color = 'tab:red'
    lp3.label = 'line 3'

    plot1 = CreatePlot()
    plot1.plot_layers = [lp1, lp2, lp3]
    plot1.add_title('Test Line Plot')
    plot1.add_xlabel('X Axis Label')
    plot1.add_ylabel('Y Axis Label')
    plot1.add_legend(loc='upper right')

    # Histogram plot
    data1, data2 = _getHistData()
    hst1 = Histogram(data1)

    plot2 = CreatePlot()
    plot2.plot_layers = [hst1]
    plot2.add_title(label='Test Histogram Plot')
    plot2.add_xlabel(xlabel='X Axis Label')
    plot2.add_ylabel(ylabel='Y Axis Label')

    # Bar plot
    x_pos, heights, variance = _getBarData()

    bar = BarPlot(x_pos, heights)
    bar.color = 'tab:red'
    bar.yerr = variance
    bar.capsize = 5.

    plot3 = CreatePlot()
    plot3.plot_layers = [bar]
    plot3.add_xlabel(xlabel='X Axis Label')
    plot3.add_ylabel(ylabel='Y Axis Label')
    plot3.add_title("Test Bar Plot")

    # Horizontal bar plot
    y_pos, widths, variance = _getBarData()

    bar = HorizontalBar(y_pos, widths)
    bar.color = 'tab:green'
    bar.xerr = variance
    bar.capsize = 5

    plot4 = CreatePlot()
    plot4.plot_layers = [bar]
    plot4.add_xlabel(xlabel='X Axis Label')
    plot4.add_ylabel(ylabel='Y Axis Label')
    plot4.add_title("Test Horizontal Bar Plot")

    fig = CreateFigure()
    fig.plot_list = [plot1, plot2, plot3, plot4]
    fig.figsize = (14, 10)
    fig.ncols = 2
    fig.nrows = 2
    fig.create_figure()
    fig.tight_layout()
    fig.save_figure('test_multi_subplot.png')


def test_HorizontalSpan():
    # Create a figure that looks like a vertical profile of
    # RMS, then demo HorizontalSpan by marking areas of
    # statistical significance.

    levbot = 925
    levtop = 125
    deltap = 50.0
    pbot = 975
    n_levs = 23
    levs = np.zeros(n_levs, float)
    levs1 = np.zeros(n_levs, float)
    levs2 = np.zeros(n_levs, float)
    levs[0:18] = pbot - deltap * np.arange(18)
    levs1[0:18] = levs[0:18] + 0.5 * deltap
    levs2[0:18] = levs[0:18] - 0.5 * deltap
    levs1[18] = levs2[17]
    levs2[18] = 70.0
    levs1[19] = 70.0
    levs2[19] = 50.0
    levs1[20] = 50.0
    levs2[20] = 30.0
    levs1[21] = 30.0
    levs2[21] = 10.0
    levs1[22] = 10.0
    levs2[22] = 0.0
    levs1[0] = 1200.0
    pbins = np.zeros(n_levs + 1, float)
    pbins[0:n_levs] = levs1
    pbins[n_levs] = levs2[-1]
    for nlev in range(18, n_levs):
        levs[nlev] = 0.5 * (levs1[nlev] + levs2[nlev])

    levels = levs
    levels_up = levs2
    levels_down = levs1

    rms = [1.80, 2.02, 2.36, 2.10, 2.21,
           2.17, 2.08, 2.14, 2.14, 2.19,
           2.43, 2.38, 2.60, 2.66, 2.63,
           2.72, 2.88, 3.99, np.nan, np.nan, np.nan, np.nan, np.nan]

    plt_list = []
    y = levels
    x = rms
    lp = LinePlot(x, y)
    lp.color = "red"
    lp.linestyle = '-'
    lp.linewidth = 1.5
    lp.marker = "o"
    lp.markersize = 4
    lp.label = "rms of F-O"
    plt_list.append(lp)

    # Make up which levels show significance to demo HorizontalSpan
    sig = [False for i in range(len(rms))]
    sig[5] = True
    sig[6] = True
    sig[8] = True
    sig[12] = True

    # Mark areas of statistical significance
    for n in range(len(levels)):
        if sig[n]:
            lp = HorizontalSpan(levels_up[n], levels_down[n])
            plt_list.append(lp)

    # Create the plot
    plot = CreatePlot()
    plot.plot_layers = plt_list
    plot.set_ylim(levbot, levtop)
    plot.add_xlabel(xlabel='X Axis Label')
    plot.add_ylabel(ylabel='Y Axis Label')
    plot.add_title("Test Horizontal Span")
    plot.add_grid()

    fig = CreateFigure(nrows=1, ncols=1, figsize=(5, 8))
    fig.plot_list = [plot]
    fig.create_figure()
    fig.tight_layout()
    fig.save_figure("./test_HorizontalSpan.png")


def test_SkewT():
    # Create skew-T log-p plot
    p, T, Td = _getSkewTData()

    tplot = SkewT(T, p)
    tplot.color = 'tab:red'

    tdplot = SkewT(Td, p)
    tdplot.color = 'tab:green'

    plot1 = CreatePlot()
    plot1.plot_layers = [tplot, tdplot]
    plot1.add_grid()
    plot1.add_xlabel('Temperature (C)')
    plot1.add_ylabel('Pressure (hPa)')
    plot1.add_title('Example Skew-T')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.tight_layout()
    fig.save_figure("./test_SkewT.png")


def _getLineData():
    # generate test data for line plots

    x1 = [0, 401, 1039, 2774, 2408]
    x2 = [500, 250, 710, 1515, 1212]
    x3 = [400, 150, 910, 1215, 850]
    y1 = [0, 2.5, 5, 7.5, 12.5]
    y2 = [1, 5, 6, 8, 10]
    y3 = [1, 4, 5.5, 9, 10.5]

    return x1, y1, x2, y2, x3, y3


def _getHistData():
    # generate test data for histogram plots

    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    data1 = mu + sigma * np.random.randn(437)
    data2 = mu + sigma * np.random.randn(119)

    return data1, data2


def _getScatterData():
    # generate test data for scatter plots

    rng = np.random.RandomState(0)
    x1 = rng.randn(100)
    y1 = rng.randn(100)

    rng = np.random.RandomState(0)
    x2 = rng.randn(30)
    y2 = rng.randn(30)

    return x1, y1, x2, y2


def _getBarData():
    # generate test data for bar graphs

    x = ['a', 'b', 'c', 'd', 'e', 'f']
    heights = [5, 6, 15, 22, 24, 8]
    variance = [1, 2, 7, 4, 2, 3]

    x_pos = [i for i, _ in enumerate(x)]

    return x_pos, heights, variance


def _getGriddedData():
    # generate test data for gridded data

    x = np.linspace(0, 1, 51)
    y = np.linspace(0, 1, 51)
    r = np.random.RandomState(25)
    z = gaussian_filter(r.random_sample([50, 50]), sigma=5, mode='wrap')

    return x, y, z


def _getContourfData():
    # generate test data for contourf plots

    x = np.linspace(-3, 15, 50).reshape(1, -1)
    y = np.linspace(-3, 15, 20).reshape(-1, 1)
    z = np.cos(x)*2 - np.sin(y)*2

    x, y = x.flatten(), y.flatten()

    return x, y, z


def _getBoxPlotData():
    # generate test data for box and whisker plot

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    data = [np.random.normal(0, std, 100) for std in range(6, 10)]

    return data


def _getSkewTData():
    # use data for skew-t log-p plot
    from io import StringIO

    # Some example data.
    data_txt = '''
        978.0    345    7.8    0.8
        971.0    404    7.2    0.2
        946.7    610    5.2   -1.8
        944.0    634    5.0   -2.0
        925.0    798    3.4   -2.6
        911.8    914    2.4   -2.7
        906.0    966    2.0   -2.7
        877.9   1219    0.4   -3.2
        850.0   1478   -1.3   -3.7
        841.0   1563   -1.9   -3.8
        823.0   1736    1.4   -0.7
        813.6   1829    4.5    1.2
        809.0   1875    6.0    2.2
        798.0   1988    7.4   -0.6
        791.0   2061    7.6   -1.4
        783.9   2134    7.0   -1.7
        755.1   2438    4.8   -3.1
        727.3   2743    2.5   -4.4
        700.5   3048    0.2   -5.8
        700.0   3054    0.2   -5.8
        698.0   3077    0.0   -6.0
        687.0   3204   -0.1   -7.1
        648.9   3658   -3.2  -10.9
        631.0   3881   -4.7  -12.7
        600.7   4267   -6.4  -16.7
        592.0   4381   -6.9  -17.9
        577.6   4572   -8.1  -19.6
        555.3   4877  -10.0  -22.3
        536.0   5151  -11.7  -24.7
        533.8   5182  -11.9  -25.0
        500.0   5680  -15.9  -29.9
        472.3   6096  -19.7  -33.4
        453.0   6401  -22.4  -36.0
        400.0   7310  -30.7  -43.7
        399.7   7315  -30.8  -43.8
        387.0   7543  -33.1  -46.1
        382.7   7620  -33.8  -46.8
        342.0   8398  -40.5  -53.5
        320.4   8839  -43.7  -56.7
        318.0   8890  -44.1  -57.1
        310.0   9060  -44.7  -58.7
        306.1   9144  -43.9  -57.9
        305.0   9169  -43.7  -57.7
        300.0   9280  -43.5  -57.5
        292.0   9462  -43.7  -58.7
        276.0   9838  -47.1  -62.1
        264.0  10132  -47.5  -62.5
        251.0  10464  -49.7  -64.7
        250.0  10490  -49.7  -64.7
        247.0  10569  -48.7  -63.7
        244.0  10649  -48.9  -63.9
        243.3  10668  -48.9  -63.9
        220.0  11327  -50.3  -65.3
        212.0  11569  -50.5  -65.5
        210.0  11631  -49.7  -64.7
        200.0  11950  -49.9  -64.9
        194.0  12149  -49.9  -64.9
        183.0  12529  -51.3  -66.3
        164.0  13233  -55.3  -68.3
        152.0  13716  -56.5  -69.5
        150.0  13800  -57.1  -70.1
        136.0  14414  -60.5  -72.5
        132.0  14600  -60.1  -72.1
        131.4  14630  -60.2  -72.2
        128.0  14792  -60.9  -72.9
        125.0  14939  -60.1  -72.1
        119.0  15240  -62.2  -73.8
        112.0  15616  -64.9  -75.9
        108.0  15838  -64.1  -75.1
        107.8  15850  -64.1  -75.1
        105.0  16010  -64.7  -75.7
        103.0  16128  -62.9  -73.9
        100.0  16310  -62.5  -73.5
    '''

    # Parse the data
    sound_data = StringIO(data_txt)
    p, h, T, Td = np.loadtxt(sound_data, unpack=True)

    return p, T, Td


def main():

    test_line_plot()
    test_histogram_plot()
    test_scatter_plot()
    test_bar_plot()
    test_gridded_plot()
    test_contours_plot()
    test_box_and_whisker_plot()
    test_horizontal_bar_plot()
    test_multi_subplot()
    test_HorizontalSpan()
    test_SkewT()


if __name__ == "__main__":

    main()
