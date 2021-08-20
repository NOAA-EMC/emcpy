import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from emcpy.stats import get_linear_regression


__all__ = ['CreatePlot']


class CreatePlot:

    def __init__(self, figsize=(8, 6)):

        self.figsize = figsize

    def draw_data(self, plot_list):
        """
        Add data layer onto figure.

        Args:
            plot_list : (array-like) List of map plot objects from emcpy
        """

        plot_dict = {
            'scatter': self._scatter,
            'histogram': self._histogram,
            'line_plot': self._lineplot
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
        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111)

        # checks to see if density has been added as an attribute
        # to the plotting object and if it's True
        if 'density' in dir(plotobj) and plotobj.density:
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

        # checks to see if linear regression has been added as an attribute
        # to the plotting object and if it's True
        if 'linear_regression' in dir(plotobj) and plotobj.linear_regression:
            y_pred, r_sq, intercept, slope = get_linear_regression(plotobj.x,
                                                                   plotobj.y)
            label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
            self.ax.plot(plotobj.x, y_pred, color=plotobj.lr_color,
                         linewidth=plotobj.lr_linewidth, label=label)

    def _histogram(self, plotobj):
        """
        Uses Histogram object to plot on axis.
        """

        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111)

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

        self.fig = plt.figure(figsize=self.figsize)
        self.ax = self.fig.add_subplot(111)

        self.ax.plot(plotobj.x,
                     plotobj.y,
                     color=plotobj.color,
                     linestyle=plotobj.linestyle,
                     linewidth=plotobj.linewidth,
                     marker=plotobj.marker,
                     markersize=plotobj.markersize,
                     alpha=plotobj.alpha,
                     label=plotobj.label)

    def add_title(self, label,
                  loc='center',
                  fontsize=12,
                  fontweight='normal',
                  color='k',
                  va='baseline'):
        """
        Adds title to plot.

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
        Adds x label to plot.

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
        Adds y label to plot.

        Args:
            ylabel : (str) Text to use for y label
            loc : (str; default='center') Location of title
            fontsize : (int; default=12) Text font size
            fontweight : (str; default='normal') Text font weight
            color : (str; default='k') Text font color
        """

        self.ax.set_ylabel(ylabel=ylabel, loc=loc, fontsize=fontsize,
                           fontweight=fontweight, color=color)

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
            raise TypeError('Data being plotted has no color series ' +
                            'to plot. Make sure data requres a colorbar.')

    def return_figure(self):
        """
        Returns the figure created.
        """

        return self.fig
