import cartopy.crs as ccrs
import cartopy.feature as cfeature
import matplotlib.pyplot as plt
from matplotlib import rcParams
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from emcpy.plots.map_tools import Domain, MapProjection


__all__ = ['CreateMap']


class CreateMap:
    """
    Creates a map axes on a figure to plot data.
    """

    def __init__(self, fig=plt.figure(figsize=(12, 8)),
                 domain=Domain('global'),
                 projection=MapProjection('plcarr')):
        """
        CreateMap constructor

        Args:
            fig : (matplotlib.figure) Figure object to plot on
            domain : (object) domain from emcpy.plots.map_tools.Domain()
            projection : (object) projection from emcpy
                         emcpy.plots.map_tools.MapProjection()
        """

        self.fig = fig
        self.domain = domain
        self.projection = projection

        if projection.__str__() not in ['npstere', 'spstere']:
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
                             transform=self.projection.projection)
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
                                transform=self.projection.projection)

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
                             transform=self.projection.projection)

        if plot.clabel:
            plt.clabel(cs, levels=plot.levels, use_clabeltext=True)

        if plot.colorbar:
            self.cs = cs

    def add_title(self, label,
                  loc='center',
                  fontsize=12,
                  fontweight='normal',
                  color='k',
                  va='baseline'):
        """
        Adds title to map axes.

        Args:
            label : (str) Text to use for title
            loc : (str; default='center') Location of title
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
            va : (str; default='baseline') Vertical alignment of text
        """

        self.ax.set_title(label, loc=loc, fontsize=fontsize,
                          fontweight=fontweight, color=color,
                          verticalalignment=va)

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

    def add_colorbar(self, label=None, label_fontsize=12, extend='neither'):
        """
        Creates new axes and adds colorbar to figure.

        Args:
            label : (str; default=None) Colorbar label
            label_fontsize : (int; default=12) Colorbar label font size
            extend : (str; default='neither') Extends min/max side of colorbar
        """
        # 'cs' is saved as an attribute if colorbar is True in plotting
        # object. If 'cs' exists, it will create a colorbar for the data
        # saved to the variable. 'cs' can be overwritten if plotting
        # multiple layers and with colorbar set to True.
        if 'cs' in dir(self):
            cax = self.fig.add_axes([self.ax.get_position().x1 + 0.02,
                                     self.ax.get_position().y0, 0.025,
                                     self.ax.get_position().height])

            cb = plt.colorbar(self.cs, extend=extend, cax=cax)
            cb.set_label(label, fontsize=label_fontsize)

        else:
            raise TypeError('Data object has colorbar set to False.' +
                            'Set obj.colorbar=True')

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
        self.ax.gridlines(crs=self.projection.projection, linewidth=linewidth,
                          color=color, alpha=alpha, linestyle=linestyle)

    def return_figure(self):
        """
        Returns the figure created.
        """

        return self.fig

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
