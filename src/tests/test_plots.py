import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot, VerticalLine,\
    Histogram, Scatter, HorizontalLine, BarPlot, \
    HorizontalBar
from emcpy.plots.create_plots import CreatePlot


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

# def test_add_logo():
#     # Test adding logos
#     x1, y1, x2, y2, x3, y3 = _getLineData()
#     lp1 = LinePlot(x1, y1)
#     lp1.label = 'line 1'

#     lp2 = LinePlot(x2, y2)
#     lp2.color = 'tab:green'
#     lp2.label = 'line 2'

#     lp3 = LinePlot(x3, y3)
#     lp3.color = 'tab:red'
#     lp3.label = 'line 3'

#     plt_list = [lp1, lp2, lp3]
#     myplt = CreatePlot()
#     myplt.draw_data(plt_list)

#     myplt.add_title(label='Test Line Plot')
#     myplt.add_xlabel(xlabel='X Axis Label')
#     myplt.add_ylabel(ylabel='Y Axis Label')
#     myplt.add_logo(400, 50, which='noaa')

#     fig = myplt.return_figure()
#     fig.savefig('test_add_logo.png')


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
    fig.save_figure('test_multi_subplot.png')


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


def main():

    test_line_plot()
    test_histogram_plot()
    test_scatter_plot()
    test_bar_plot()
    test_horizontal_bar_plot()
    test_multi_subplot()


if __name__ == "__main__":

    main()
