# This work developed by NOAA/NWS/EMC under the Apache 2.0 license.
from __future__ import annotations
import numpy as np
from packaging.version import Version
import matplotlib

__all__ = [
    'Scatter', 'Histogram', 'Density', 'LinePlot',
    'VerticalLine', 'HorizontalLine', 'HorizontalSpan',
    'BarPlot', 'HorizontalBar', 'SkewT',
    'GriddedPlot', 'ContourPlot', 'FilledContourPlot',
    'BoxandWhiskerPlot', 'FillBetween', 'ErrorBar',
    'ViolinPlot', 'HexBin', 'Hist2D',
]


class Scatter:
    def __init__(self, x, y):
        """
        Scatter plot layer.
        Args:
            x: array-like
            y: array-like
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
        self.do_linear_regression = False
        # Optional style overrides for the regression line; kept empty by default.
        # The renderer will default to the scatter color if 'color' isn't provided.
        self.linear_regression = {}

    def add_linear_regression(self):
        """
        Include linear regression line info as attributes.
        """
        self.linear_regression = {
            'color': 'black',
            'linewidth': 1,
            'linestyle': '-'
        }

    def density_scatter(self):
        """
        Include density scatter plot info as attributes.
        """
        self.density = {
            'sort': True,
            'cmap': 'nipy_spectral_r',
            'colorbar': True,
            'bins': [100, 100],
            'interp': 'linear',
            'nsamples': True
        }


class Histogram:
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


class Density():
    def __init__(self, data):
        """
        Constructor for Density.
        Args:
            data : (array type)
        """

        super().__init__()
        self.plottype = 'density'

        self.data = data

        self.color = 'tab:blue'
        self.fill = False
        self.multiple = 'layer'
        self.common_norm = True
        self.common_grid = False
        self.cumulative = False
        self.bw_method = 'scott'
        self.bw_adjust = 1
        self.warn_singular = True
        self.log_scale = False
        self.levels = 10
        self.thresh = 0.05
        self.gridsize = 200
        self.cut = 3
        self.legend = False
        self.cbar = False
        self.cbar_ax = None
        self.cbar_kws = None
        self.label = f'n={np.count_nonzero(~np.isnan(data))}'
        self.alpha = None


class LinePlot:
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


class GriddedPlot:
    def __init__(self, x, y, z):
        """
        Constructor for GriddedPlot.
        Args:
            x : (array type)
            y : (array type)
            z : (array type)
        """
        super().__init__()
        self.plottype = 'gridded_plot'

        self.x = x
        self.y = y
        self.z = z

        self.cmap = 'viridis'
        self.norm = None
        self.vmin = None
        self.vmax = None
        self.edgecolors = None
        self.shading = 'auto'
        self.alpha = None
        self.colorbar = True


class ContourPlot:
    def __init__(self, x, y, z):
        """
        Constructor for ContourPlot.
        Args:
            x : (array type)
            y : (array type)
            z : (array type)
        """
        super().__init__()
        self.plottype = 'contour'

        self.x = x
        self.y = y
        self.z = z

        self.corner_mask = False
        self.colors = 'black'
        self.alpha = None
        self.cmap = None
        self.norm = None
        self.vmin = None
        self.vmax = None
        self.origin = None
        self.extent = None
        self.locator = None
        self.extend = None
        self.levels = None
        self.colorbar = False


class FilledContourPlot:
    def __init__(self, x, y, z):
        """
        Constructor for FilledContourPlot.
        Args:
            x : (array type)
            y : (array type)
            z : (array type)
        """
        super().__init__()
        self.plottype = 'contourf'

        self.x = x
        self.y = y
        self.z = z

        self.corner_mask = False
        self.colors = None
        self.alpha = None
        self.cmap = 'viridis'
        self.norm = None
        self.vmin = None
        self.vmax = None
        self.origin = None
        self.extent = None
        self.locator = None
        self.extend = None
        self.colorbar = True


class VerticalLine:
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


class HorizontalLine:
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


class HorizontalSpan:
    def __init__(self, ymin, ymax):
        """
        Constructor for HorizontalSpan
        Args:
            ymin : (int/float) lower y-coordinate of the span, in data units.
            ymax : (int/float) upper y-coordinate of the span, in data units.
        """
        super().__init__()
        self.plottype = 'horizontal_span'

        self.ymin = ymin
        self.ymax = ymax

        self.facecolor = 'lightgoldenrodyellow'
        self.edgecolor = None
        self.alpha = None


class BarPlot:
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


class HorizontalBar:
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


class SkewT:
    def __init__(self, x, y):
        """
        Constructor to create a Skew T plot.
        Args:
            x : (array type)
            y : (array type)
        """

        super().__init__()
        self.plottype = 'skewt'

        self.x = x
        self.y = y

        self.color = 'tab:blue'
        self.linestyle = '-'
        self.linewidth = 1.5
        self.marker = None
        self.markersize = None
        self.alpha = None
        self.label = None


class BoxandWhiskerPlot:
    def __init__(self, data):
        self.plottype = 'boxandwhisker'
        self.data = data

        # Matplotlib kwargs (modern defaults where applicable)
        self.notch = False
        self.sym = None
        self.orientation = 'vertical'   # modern, we’ll map to vert=True/False
        self.vert = None                # optional legacy explicit override
        self.whis = 1.5
        self.bootstrap = None
        self.usermedians = None
        self.conf_intervals = None
        self.positions = None
        self.widths = None
        self.patch_artist = False

        # 3.9+ prefers 'tick_labels'; we’ll down-convert to 'labels' on older MPL
        self.tick_labels = None

        self.manage_ticks = True
        self.autorange = False
        self.meanline = False
        self.zorder = None


class FillBetween:
    def __init__(self, x, y1, y2):
        """
        Area fill between y1 and y2 across x.

        Args:
            x  : array-like
            y1 : array-like
            y2 : array-like
        """
        super().__init__()
        self.plottype = 'fill_between'

        self.x = x
        self.y1 = y1
        self.y2 = y2

        self.where = None          # optional boolean mask
        self.color = 'tab:blue'
        self.alpha = None
        self.label = None
        self.linewidth = None
        self.linestyle = None
        self.step = None           # {'pre','post','mid'} or None
        self.zorder = None


class ErrorBar:
    def __init__(self, x, y):
        """
        Error bar layer.

        Args:
            x : array-like
            y : array-like
        """
        super().__init__()
        self.plottype = 'errorbar'

        self.x = x
        self.y = y

        # errors
        self.yerr = None           # float, array-like, or (lower, upper)
        self.xerr = None           # float, array-like, or (lower, upper)

        # style / markers
        self.fmt = 'o'
        self.color = 'darkgray'
        self.alpha = None
        self.markersize = 5
        self.ecolor = 'black'
        self.elinewidth = 1.0
        self.capthick = None
        self.capsize = 0.0
        self.barsabove = False
        self.zorder = None

        # label defaults to non-NaN x count (consistent with Scatter/Histogram)
        self.label = f'n={np.count_nonzero(~np.isnan(x))}'


class ViolinPlot:
    def __init__(self, data):
        """
        Violin plot layer for 1-D distributions.

        Args:
            data : sequence of 1-D array-like datasets
        """
        super().__init__()
        self.plottype = 'violin'

        self.data = data

        self.positions = None      # sequence of x positions
        self.widths = 0.8
        self.showmeans = False
        self.showmedians = True
        self.showextrema = True
        self.alpha = None
        self.zorder = None


class HexBin:
    def __init__(self, x, y, C=None):
        """
        Hexagonal binning layer.

        Args:
            x : array-like
            y : array-like
            C : optional array-like of values to reduce within bins
        """
        super().__init__()
        self.plottype = 'hexbin'

        self.x = x
        self.y = y
        self.C = C

        self.gridsize = 30                      # int or (nx, ny)
        self.reduce_C_function = None           # e.g., np.mean
        self.extent = None                      # (xmin, xmax, ymin, ymax)
        self.bins = None                        # None, 'log', or int
        self.mincnt = None
        self.linewidths = None
        self.cmap = 'viridis'
        self.norm = None                        # optional matplotlib Normalize
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.zorder = None
        self.label = None

        # colorbar controls
        self.colorbar = False
        self.colorbar_label = None
        self.colorbar_location = 'right'


class Hist2D:
    def __init__(self, x, y):
        """
        2D histogram layer.

        Args:
            x : array-like
            y : array-like
        """
        super().__init__()
        self.plottype = 'hist2d'

        self.x = x
        self.y = y

        self.bins = 30                            # int, (nx, ny), or (xbins, ybins)
        self.range = None                         # ((xmin, xmax), (ymin, ymax))
        self.density = False
        self.cmap = 'viridis'
        self.norm = None                          # optional matplotlib Normalize
        self.vmin = None
        self.vmax = None
        self.cmin = None
        self.cmax = None
        self.alpha = None
        self.zorder = None
        self.label = None

        # colorbar controls
        self.colorbar = True
        self.colorbar_label = None
        self.colorbar_location = 'right'
