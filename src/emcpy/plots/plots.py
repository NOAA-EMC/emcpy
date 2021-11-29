import numpy as np


__all__ = ['Scatter', 'Histogram', 'LinePlot' 'VerticalLine',
           'HorizontalLine', 'BarPlot' 'HorizontalBar']


class BasePlot:
    def __init__(self):
        """
        BasePlot Constructor.
        """
        self.plot_ax = 'ax'
        return

    def use_shared_ax(self):
        """
        Set object to plot on shared ax axis
        """
        self.plot_ax = 'shared_ax'

    def use_shared_ay(self):
        """
        Set object to plot on shared ay axis
        """
        self.plot_ax = 'shared_ay'


class Scatter(BasePlot):

    def __init__(self, x, y):
        """
        Constructor for Scatter.

        Args:
            x : (array type)
            y : (array type)
        """

        super().__init__()
        self.plottype = 'scatter'

        self.x = x
        self.y = y

        self.markersize = 5
        self.color = 'darkgray'
        self.marker = 'o'
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.linewidths = 1.5
        self.edgecolors = None
        self.label = f'n={np.count_nonzero(~np.isnan(x))}'
        self.linear_regression = False
        self.density = False

    def add_linear_regression(self):
        """
        Include linear regression line info as attributes.
        """
        self.linear_regression = True
        self.lr_color = 'black'
        self.lr_linewidth = 1

    def density_scatter(self):
        """
        Include density scatter plot info as attributes.
        """
        self.density = True
        self.sort = True
        self.cmap = 'nipy_spectral_r'
        self.colorbar = True
        self.bins = [100, 100]
        self.interp = 'linear'
        self.nsamples = True


class Histogram(BasePlot):

    def __init__(self, data):
        """
        Constructor for Histogram.

        Args:
            data : (array type)
        """

        super().__init__()
        self.plottype = 'histogram'

        self.data = data

        self.bins = 10
        self.range = None
        self.density = False
        self.weights = None
        self.cumulative = False
        self.bottom = None
        self.histtype = 'bar'
        self.align = 'mid'
        self.orientation = 'vertical'
        self.rwidth = None
        self.log = False
        self.color = 'tab:blue'
        self.label = f'n={np.count_nonzero(~np.isnan(data))}'
        self.stacked = False
        self.alpha = None


class LinePlot(BasePlot):

    def __init__(self, x, y):
        """
        Constructor for LinePlot.

        Args:
            x : (array type)
            y : (array type)
        """
        super().__init__()
        self.plottype = 'line_plot'

        self.x = x
        self.y = y

        self.color = 'tab:blue'
        self.linestyle = '-'
        self.linewidth = 1.5
        self.marker = None
        self.markersize = None
        self.alpha = None
        self.label = None


class VerticalLine(BasePlot):

    def __init__(self, x):
        """
        Constructor for VerticalLine

        Args:
            x : (int/float) x-value where vertical line
                is to be plotted
        """

        super().__init__()
        self.plottype = 'vertical_line'

        self.x = x

        self.color = 'black'
        self.linestyle = '-'
        self.linewidth = 1.5
        self.label = None


class HorizontalLine(BasePlot):

    def __init__(self, y):
        """
        Constructor for HorizontalLine

        Args:
            y : (int/float) y-value where horizontal
                line is to be plotted
        """

        super().__init__()
        self.plottype = 'horizontal_line'

        self.y = y

        self.color = 'black'
        self.linestyle = '-'
        self.linewidth = 1.5
        self.label = None


class BarPlot(BasePlot):

    def __init__(self, x, height):
        """
        Constructor for BarPlot.

        Args:
            x : (array type) x coordinate of bars
            height : (array type) the height(s) of the bars
        """

        super().__init__()
        self.plottype = 'bar_plot'

        self.x = x
        self.height = height

        self.width = 0.8
        self.bottom = 0
        self.align = 'center'
        self.color = 'tab:blue'
        self.edgecolor = None
        self.linewidth = 0
        self.tick_label = None
        self.xerr = None
        self.yerr = None
        self.ecolor = 'black'
        self.capsize = 0
        self.error_kw = {}
        self.log = False


class HorizontalBar(BasePlot):

    def __init__(self, y, width):
        """
        Constructor to create a horizontal bar plot.

        Args:
            y : (array type) y coordinate of bars
            width : (array type) the width(s) of the bars
        """

        super().__init__()
        self.plottype = 'horizontal_bar'

        self.y = y
        self.width = width

        self.height = 0.8
        self.left = 0
        self.align = 'center'
        self.color = 'tab:blue'
        self.edgecolor = None
        self.linewidth = 0
        self.tick_label = None
        self.xerr = None
        self.yerr = None
        self.ecolor = 'black'
        self.capsize = 0
        self.error_kw = {}
        self.log = False
