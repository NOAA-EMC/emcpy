import numpy as np
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib import rcParams
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.stats import get_linear_regression

__all__ = ['CreatePlot', 'CreateMap']


class EMCPyPlots:

    def __init__(self, figsize):
        """
        EMCPyPlots Constructor.

        Args:
            figsize : (tuple) Figure dimension size
        """

        self.fig = plt.figure(figsize=figsize)

        return

    def add_title(self, label,
                  loc='center',
                  fontsize=12,
                  fontweight='normal',
                  color='k',
                  verticalalignment='baseline'):
        """
        Adds title to map axes.

        Args:
            label : (str) Text to use for title
            loc : (str; default='center') Location of title
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
            verticalalignment : (str; default='baseline') Vertical
                                alignment of text
        """

        self.ax.set_title(label, loc=loc, fontsize=fontsize,
                          fontweight=fontweight, color=color,
                          verticalalignment=verticalalignment)

    def add_xlabel(self, xlabel,
                   loc='center',
                   fontsize=12,
                   fontweight='normal',
                   color='k'):
        """
        Adds x label to map axes.

        Args:
            xlabel : (str) Text to use for x label
            loc : (str; default='center') Location of title
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
        """

        self.ax.set_xlabel(xlabel=xlabel, loc=loc, fontsize=fontsize,
                           fontweight=fontweight, color=color)

    def add_ylabel(self, ylabel,
                   loc='center',
                   fontsize=12,
                   fontweight='normal',
                   color='k'):
        """
        Adds y label to map axes.

        Args:
            ylabel : (str) Text to use for y label
            loc : (str; default='center') Location of title
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
        """

        self.ax.set_ylabel(ylabel=ylabel, loc=loc, fontsize=fontsize,
                           fontweight=fontweight, color=color)

    def add_colorbar(self, label=None, orientation='horizontal',
                     label_fontsize=12, extend='neither'):
        """
        Creates new axes and adds colorbar to figure.

        Args:
            label : (str; default=None) Colorbar label
            orientation  : (str; default='horizontal') colorbar orientation
            label_fontsize : (int; default=12) Colorbar label font size
            extend : (str; default='neither') Extends min/max side of colorbar
        """
        # 'cs' is saved as an attribute if colorbar is True in plotting
        # object. If 'cs' exists, it will create a colorbar for the data
        # saved to the variable. 'cs' can be overwritten if plotting
        # multiple layers and with colorbar set to True.

        from mpl_toolkits.axes_grid1.inset_locator import inset_axes

        if 'cs' in dir(self):
            if orientation == 'horizontal':
                axins = inset_axes(self.ax,
                                   width="95%",
                                   height="5%",
                                   loc='lower center',
                                   borderpad=-8)
            else:
                axins = inset_axes(self.ax,
                                   width="2.5%",
                                   height="95%",
                                   loc='right',
                                   borderpad=-4)

            cb = self.fig.colorbar(self.cs, extend=extend, cax=axins,
                                   orientation=orientation)
            cb.set_label(label, fontsize=label_fontsize)

        else:
            raise TypeError('Data object has colorbar set to False.' +
                            'Set obj.colorbar=True')

    def add_stats_dict(self, stats_dict={'Stats': 'None'}, xloc=0.5,
                       yloc=-0.1, fontsize=12):
        """
        Annotate statistics to the figure. For a given dictionary, stats_dict,
        each key and value will be annotated in order.

        Args:
            stats_dict : (dict; default={'Stats': 'None'}) dict of values
                         to be annotated
            xloc : (float; default=0.5) location of text on x-axis
            yloc : (float; default=-0.1) location of text on y-axis
            fontsize : (int; default=10) Annotated text font size
        """
        # loop through the dictionary and create the sting to annotate
        outstr = ''
        for key, value in stats_dict.items():
            outstr = outstr + f'    {key}: {value}'
        # annotate this just underneath the figure on the right side
        self.ax.annotate(outstr, xy=(xloc, yloc), xycoords='axes fraction',
                         fontsize=fontsize, horizontalalignment='center',
                         verticalalignment='top')

    def add_text(self, xloc, yloc, text, fontsize=12,
                 fontweight='normal', color='k', alpha=1.,
                 horizontalalignment='center'):
        """
        Add text to a figure.

        Args:
            xloc : (int/float) x location on axis
            yloc : (int/float) y location on axis
            text : (str) Text to plot on figure
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
            alpha : (float; default=1.) alpha of text
            horizontalalignment : (str; default='baseline') Vertical
                                alignment of text
        """
        self.ax.text(xloc, yloc, text, fontsize=fontsize,
                     fontweight=fontweight, color=color,
                     alpha=alpha, ha=horizontalalignment)

    def return_figure(self):
        """
        Returns the figure created.
        """

        return self.fig


class CreatePlot(EMCPyPlots):
    """
    Creates a figure to plot data as a scatter plot,
    histogram, or line plot.
    """

    def __init__(self, figsize=(8, 6)):
        """
        CreatePlot constructor.

        Args:
            figsize : (tuple; default=(8,6)) Figure dimension size
        """

        super().__init__(figsize)
        self.ax = self.fig.add_subplot(111)

    def draw_data(self, plot_list):
        """
        Add data layer onto figure.

        Args:
            plot_list : (array-like) List of map plot objects from emcpy
        """

        plot_dict = {
            'scatter': self._scatter,
            'histogram': self._histogram,
            'line_plot': self._lineplot,
            'vertical_line': self._verticalline,
            'horizontal_line': self._horizontalline
        }

        for obj in plot_list:
            try:
                plot_dict[obj.plottype](obj)
            except KeyError:
                raise TypeError(f'{obj} is not a valid plot type.' +
                                'Current plot types supported are:\n' +
                                f'{" | ".join(feature_dict.keys())}"')

    def _density_scatter(self, plotobj):
        """
        Uses Scatter Object to plot density scatter colored by
        2d histogram.
        """
        data, x_e, y_e = np.histogram2d(plotobj.x, plotobj.y,
                                        bins=plotobj.bins,
                                        density=True)
        z = interpn((0.5*(x_e[1:] + x_e[:-1]), 0.5*(y_e[1:]+y_e[:-1])),
                    data, np.vstack([plotobj.x, plotobj.y]).T,
                    method="splinef2d", bounds_error=False)
        # To be sure to plot all data
        z[np.where(np.isnan(z))] = 0.0
        # Sort the points by density, so that the densest
        # points are plotted last
        if plotobj.sort:
            idx = z.argsort()
            x, y, z = plotobj.x[idx], plotobj.y[idx], z[idx]
        cs = self.ax.scatter(x, y, c=z,
                             s=plotobj.markersize,
                             cmap=plotobj.cmap,
                             label=plotobj.label)
        norm = Normalize(vmin=np.min(z), vmax=np.max(z))

        if plotobj.colorbar:
            self.cs = cs

    def _scatter(self, plotobj):
        """
        Uses Scatter object to plot on axis.
        """

        # checks to see if density attribute is True
        if plotobj.density:
            self._density_scatter(plotobj)

        else:
            s = self.ax.scatter(plotobj.x, plotobj.y,
                                s=plotobj.markersize,
                                color=plotobj.color,
                                marker=plotobj.marker,
                                vmin=plotobj.vmin,
                                vmax=plotobj.vmax,
                                alpha=plotobj.alpha,
                                linewidths=plotobj.linewidths,
                                edgecolors=plotobj.edgecolors,
                                label=plotobj.label)

        # checks to see if linear regression attribute is True
        if plotobj.linear_regression:
            y_pred, r_sq, intercept, slope = get_linear_regression(plotobj.x,
                                                                   plotobj.y)
            label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
            self.ax.plot(plotobj.x, y_pred, color=plotobj.lr_color,
                         linewidth=plotobj.lr_linewidth, label=label)

    def _histogram(self, plotobj):
        """
        Uses Histogram object to plot on axis.
        """

        self.ax.hist(plotobj.data,
                     bins=plotobj.bins,
                     range=plotobj.range,
                     density=plotobj.density,
                     weights=plotobj.weights,
                     cumulative=plotobj.cumulative,
                     bottom=plotobj.bottom,
                     histtype=plotobj.histtype,
                     align=plotobj.align,
                     orientation=plotobj.orientation,
                     rwidth=plotobj.rwidth,
                     log=plotobj.log,
                     color=plotobj.color,
                     label=plotobj.label,
                     stacked=plotobj.stacked,
                     alpha=plotobj.alpha)

    def _lineplot(self, plotobj):
        """
        Uses LinePlot object to plot on axis.
        """

        self.ax.plot(plotobj.x,
                     plotobj.y,
                     color=plotobj.color,
                     linestyle=plotobj.linestyle,
                     linewidth=plotobj.linewidth,
                     marker=plotobj.marker,
                     markersize=plotobj.markersize,
                     alpha=plotobj.alpha,
                     label=plotobj.label)

    def _verticalline(self, plotobj):
        """
        Uses VerticalLine object to plot on axis.
        """

        self.ax.axvline(plotobj.x,
                        color=plotobj.color,
                        linestyle=plotobj.linestyle,
                        linewidth=plotobj.linewidth,
                        label=plotobj.label)

    def _horizontalline(self, plotobj):
        """
        Uses HorizontalLine object to plot on axis.
        """

        self.ax.axhline(plotobj.y,
                        color=plotobj.color,
                        linestyle=plotobj.linestyle,
                        linewidth=plotobj.linewidth,
                        label=plotobj.label)

    def add_legend(self, loc='upper left',
                   fontsize='medium'):
        """
        Adds legend to plot.
        """

        self.ax.legend(loc=loc, fontsize=fontsize)

    def add_grid(self,
                 linewidth=1,
                 color='gray',
                 alpha=None,
                 linestyle='-'):
        """
        Plots gridlines on plot.

        Args:
            linewidth : (int; default=1) Line thickness
            color : (str; default='gray') Line color
            alpha : (float; default=None) The alpha value,
                    between 0 (transparent) and 1 (opaque)
            linestyle : (str; default='-') Line style
        """
        self.ax.grid(linewidth=linewidth, color=color,
                     alpha=alpha, linestyle=linestyle)

    def set_xlim(self, left=None, right=None):
        """
        Sets x limits on plot.

        Args:
            left: (int, float) the left xlim in data coorinates
            right: (int, float) the right xlim in data coorinates
        """
        self.ax.set_xlim(left, right)

    def set_ylim(self, bottom=None, top=None):
        """
        Sets y limits on plot.

        Args:
            bottom: (int, float) the bottom ylim in data coorinates
            top: (int, float) the top ylim in data coorinates
        """
        self.ax.set_ylim(bottom, top)

    def set_xticks(self, ticks=list(), minor=False):
        """
        Sets x ticks on plot.
        """
        self.ax.set_xticks(ticks, minor=minor)

    def set_yticks(self, ticks=list(), minor=False):
        """
        Sets y ticks on plot.
        """
        self.ax.set_yticks(ticks, minor=minor)

    def set_xticklabels(self, labels=list(),
                        fontsize=12,
                        fontweight='normal',
                        color='k',
                        rotation=0):
        """
        Sets the xtick labels.

        Note, if len of labels does not equal the number of x ticks,
        a Value Error will be raised.

        Args:
            labels : (array like) list of str to use for x ticks
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
            rotation : (int) rotation of tick labels
        """

        if len(labels) == len(self.ax.get_xticks()):
            self.ax.set_xticklabels(labels=labels,
                                    fontsize=fontsize,
                                    fontweight=fontweight,
                                    color=color, rotation=rotation)

        else:
            raise ValueError('Len of xtick labels does not equal ' +
                             'len of xticks. Set xticks appropriately ' +
                             'or change labels to be len of xticks.')

    def set_yticklabels(self, labels=list(),
                        fontsize=12,
                        fontweight='normal',
                        color='k',
                        rotation=0):
        """
        Sets the ytick labels.

        Note, if len of labels does not equal the number of y ticks,
        a Value Error will be raised.

        Args:
            labels : (array like) list of str to use for y ticks
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
            rotation : (int) rotation of tick labels
        """

        if len(labels) == len(self.ax.get_yticks()):
            self.ax.set_yticklabels(labels=labels,
                                    fontsize=fontsize,
                                    fontweight=fontweight,
                                    color=color, rotation=rotation)

        else:
            raise ValueError('Len of ytick labels does not equal ' +
                             'len of yticks. Set yticks appropriately ' +
                             'or change labels to be len of yticks.')

    def invert_xaxis(self):
        """
        Invert the x axis
        """
        self.ax.invert_xaxis()

    def invert_yaxis(self):
        """
        Invert the y axis
        """
        self.ax.invert_yaxis()

    def set_yscale(self, scale):
        """
        Sets the y axis scale to 'log', 'linear', 'symlog', or 'logit'

        Args:
            scale : (str) scale type 'log', 'linear', 'symlog', or 'logit'
        """
        valid_scales = ['log', 'linear', 'symlog', 'logit']
        if scale not in valid_scales:
            raise ValueError(f'requested scale {scale} is invalid. Valid choices are: {" | ".join(valid_scales)}')

        self.ax.set_yscale(scale)


class CreateMap(EMCPyPlots):
    """
    Creates a map axes on a figure to plot data.
    """

    def __init__(self, figsize=(12, 8),
                 domain=Domain('global'),
                 proj_obj=MapProjection('plcarr')):
        """
        CreateMap constructor

        Args:
            figsize : (tuple; default=(12,8)) Figure dimension size
            domain : (object) domain from emcpy.plots.map_tools.Domain()
            projection : (object) projection from emcpy
                         emcpy.plots.map_tools.MapProjection()
        """

        super().__init__(figsize)

        self.domain = domain
        self.proj_obj = proj_obj
        ax = self.fig.add_subplot(1, 1, 1, projection=proj_obj.projection)

        if str(proj_obj) not in ['npstere', 'spstere']:
            ax.set_extent(domain.extent)
            ax.set_xticks(domain.xticks, crs=ccrs.PlateCarree())
            ax.set_yticks(domain.yticks, crs=ccrs.PlateCarree())
            lon_formatter = LongitudeFormatter(zero_direction_label=False)
            lat_formatter = LatitudeFormatter()
            ax.xaxis.set_major_formatter(lon_formatter)
            ax.yaxis.set_major_formatter(lat_formatter)

        self.ax = ax

    def add_features(self, feature_list=['coastlines']):
        """
        Add features onto map.

        Args:
            feature_list : (array-like, default=['coastlines']) List of cartopy
                           cfeatures that can be found here:
                           https://scitools.org.uk/cartopy/docs/v0.14/matplotlib
                           /feature_interface.html


        ***Need to get shapefiles/figure out how to get cfeatures from Cartopy
        """

        feature_dict = {
            'coastlines': self._add_coastlines,
            'borders': self._add_borders,
            'states': self._add_states,
            'lakes': self._add_lakes,
            'rivers': self._add_rivers
        }

        for feat in feature_list:
            try:
                feature_dict[feat]()
            except KeyError:
                raise TypeError(f'{feat} is not a valid map feature.' +
                                'Current map features supported are:\n' +
                                f'{" | ".join(feature_dict.keys())}"')

    def draw_data(self, plot_list=list()):
        """
        Add data layer onto map.

        Args:
            plot_list : (array-like) List of map plot objects from emcpy
        """

        plot_dict = {
            'map_scatter': self._scatter,
            'map_gridded': self._gridded,
            'map_contour': self._contour
        }

        for plotobj in plot_list:
            try:
                plot_dict[plotobj.plottype](plotobj)
            except KeyError:
                raise TypeError(f'{plotobj} is not a valid plot type.' +
                                'Current plot types supported are:\n' +
                                f'{" | ".join(feature_dict.keys())}"')

    def _scatter(self, plot):
        """
        Plots MapScatter object on map axes.
        """

        cs = self.ax.scatter(plot.longitude,
                             plot.latitude,
                             c=plot.data,
                             s=plot.markersize,
                             cmap=plot.cmap,
                             marker=plot.marker,
                             vmin=plot.vmin,
                             vmax=plot.vmax,
                             transform=self.proj_obj.projection)
        if plot.colorbar:
            self.cs = cs

    def _gridded(self, plot):
        """
        Plots MapGridded object on map axes.
        """

        cs = self.ax.pcolormesh(plot.longitude,
                                plot.latitude,
                                plot.data,
                                cmap=plot.cmap,
                                vmin=plot.vmin,
                                vmax=plot.vmax,
                                alpha=plot.alpha,
                                transform=self.proj_obj.projection)

        if plot.colorbar:
            self.cs = cs

    def _contour(self, plot):
        """
        Plots MapContour object on map axes.
        """

        cs = self.ax.contour(plot.longitude,
                             plot.latitude,
                             plot.data,
                             levels=plot.levels,
                             colors=plot.colors,
                             linewidth=plot.linewidths,
                             linestyle=plot.linestyles,
                             cmap=plot.cmap,
                             vmin=plot.vmin,
                             vmax=plot.vmax,
                             alpha=plot.alpha,
                             transform=self.proj_obj.projection)

        if plot.clabel:
            plt.clabel(cs, levels=plot.levels, use_clabeltext=True)

        if plot.colorbar:
            self.cs = cs

    def add_grid(self,
                 linewidth=1,
                 color='gray',
                 alpha=None,
                 linestyle='-'):
        """
        Adds gridlines on map axes.

        Args:
            linewidth : (int; default=1) Line thickness
            color : (str; default='gray') Line color
            alpha : (float; default=None) The alpha value,
                    between 0 (transparent) and 1 (opaque)
            linestyle : (str; default='-') Line style
        """
        self.ax.gridlines(crs=ccrs.PlateCarree(), linewidth=linewidth,
                          color=color, alpha=alpha, linestyle=linestyle)

    def _add_coastlines(self):
        """
        Add coastline to map axes. (Only feature that currently works)
        """
        self.ax.add_feature(cfeature.GSHHSFeature(scale='auto'))

        # Will uncomment when we can get cfeatures to work
        # self.ax.add_feature(cfeature.COASTLINE)

    def _add_borders(self):
        """
        Add country borders to map axes.
        """
        self.ax.add_feature(cfeature.BORDERS)

    def _add_states(self):
        """
        Add state borders to map axes.
        """
        self.ax.add_feature(cfeature.STATES)

    def _add_lakes(self):
        """
        Add lakes to map axes.
        """
        self.ax.add_feature(cfeature.LAKES)

    def _add_rivers(self):
        """
        Add rivers to map axes.
        """
        self.ax.add_feature(sfeature.RIVERS)
