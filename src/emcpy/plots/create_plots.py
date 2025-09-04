# This work developed by NOAA/NWS/EMC under the Apache 2.0 license.
import os
import emcpy
import numpy as np
import pandas as pd
from pandas import Timestamp
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
import matplotlib.dates as mdates
import cartopy.crs as ccrs
import cartopy.feature as cfeature
import datetime as datetime
from dataclasses import dataclass, field
from typing import Any, List, Optional
from PIL import Image
from scipy.interpolate import interpn
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
from matplotlib.cm import ScalarMappable
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
from matplotlib.ticker import MultipleLocator, FixedLocator, NullLocator
from matplotlib.ticker import NullFormatter, ScalarFormatter
from matplotlib.projections import register_projection
from emcpy.plots.adapters import get_adapter, AxState
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.skewt_projection import SkewXAxes
from emcpy.stats.stats import get_linear_regression

__all__ = ['CreateFigure', 'CreatePlot']

# Register SkewXAxes projection exactly once
try:
    register_projection(SkewXAxes)
except ValueError:
    pass


class CreatePlot:
    """
    Creates a figure to plot data as a scatter plot,
    histogram, density or line plot.
    """
    def __init__(self, plot_layers=[], projection=None,
                 domain=None):

        self.plot_layers = plot_layers

        ###############################################
        # Need a better way of doing this
        if projection is not None and domain is not None:
            self.projection = projection
            self.domain = domain
        ###############################################

    def add_title(self, label, loc='center',
                  pad=None, **kwargs):

        self.title = {
            'label': label,
            'loc': loc,
            'pad': pad,
            **kwargs
        }

    def add_xlabel(self, xlabel, labelpad=None,
                   loc='center', **kwargs):

        self.xlabel = {
            'xlabel': xlabel,
            'labelpad': labelpad,
            'loc': loc,
            **kwargs
        }

    def add_ylabel(self, ylabel, labelpad=None,
                   loc='center', **kwargs):

        self.ylabel = {
            'ylabel': ylabel,
            'labelpad': labelpad,
            'loc': loc,
            **kwargs
        }

    def add_colorbar(self, label=None, fontsize=12, single_cbar=False,
                     cbar_location=None, **kwargs):

        kwargs.setdefault('orientation', 'horizontal')

        pad = 0.15 if kwargs['orientation'] == 'horizontal' else 0.1
        fraction = 0.065 if kwargs['orientation'] == 'horizontal' else 0.085

        kwargs.setdefault('pad', pad)
        kwargs.setdefault('fraction', fraction)

        if not cbar_location:
            h_loc = [0.14, -0.1, 0.8, 0.04]
            v_loc = [1.02, 0.12, 0.04, 0.8]
            cbar_location = h_loc if kwargs['orientation'] == 'horizontal' else v_loc

        self.colorbar = {
            'label': label,
            'fontsize': fontsize,
            'single_cbar': single_cbar,
            'cbar_loc': cbar_location,
            'kwargs': kwargs
        }

    def add_stats_dict(self, stats_dict={}, xloc=0.5,
                       yloc=-0.1, ha='center', **kwargs):

        self.stats = {
            'stats': stats_dict,
            'xloc': xloc,
            'yloc': yloc,
            'ha': ha,
            'kwargs': kwargs
        }

    def add_legend(self, **kwargs):

        self.legend = {
            **kwargs
        }

    def add_text(self, xloc, yloc, text, transform='datacoords',
                 **kwargs):

        if not hasattr(self, 'text'):
            self.text = []

        self.text.append({
            'xloc': xloc,
            'yloc': yloc,
            'text': text,
            'transform': transform,
            'kwargs': kwargs
        })

    def add_grid(self, **kwargs):

        self.grid = {
            **kwargs
        }

    def add_map_features(self, feature_list=['coastline']):

        self.map_features = feature_list

    def set_xlim(self, left=None, right=None):

        self.xlim = {
            'left': left,
            'right': right
        }

    def set_ylim(self, bottom=None, top=None):

        self.ylim = {
            'bottom': bottom,
            'top': top
        }

    def set_xticks(self, ticks=list(), minor=False, formatter=None, date_format=None, clear_minor=True):

        self.xticks = {
            "ticks": ticks,
            "minor": minor,
            "formatter": formatter,
            "date_format": date_format,
            "clear_minor": clear_minor,
        }

    def set_yticks(self, ticks=list(), minor=False, formatter=None, date_format=None, clear_minor=True):

        self.yticks = {
            "ticks": ticks,
            "minor": minor,
            "formatter": formatter,
            "date_format": date_format,
            "clear_minor": clear_minor,
        }

    def set_xticklabels(self, labels=list(), minor=False, date_format=None, **kwargs):

        self.xticklabels = {
            "labels": labels,
            "minor": minor,
            "date_format": date_format,
            "kwargs": kwargs,
        }

    def set_yticklabels(self, labels=list(), minor=False, date_format=None, **kwargs):

        self.yticklabels = {
            "labels": labels,
            "minor": minor,
            "date_format": date_format,
            "kwargs": kwargs,
        }

    def invert_xaxis(self):

        self.invert_xaxis = True

    def invert_yaxis(self):

        self.invert_yaxis = True

    def set_xscale(self, scale):

        valid_scales = ['log', 'linear', 'symlog', 'logit']
        if scale not in valid_scales:
            raise ValueError(f'requested scale {scale} is invalid. Valid '
                             f'choices are: {" | ".join(valid_scales)}')
        self.xscale = scale

    def set_yscale(self, scale):

        valid_scales = ['log', 'linear', 'symlog', 'logit']
        if scale not in valid_scales:
            raise ValueError(f'requested scale {scale} is invalid. Valid '
                             f'choices are: {" | ".join(valid_scales)}')

        self.yscale = scale


class CreateFigure:

    def __init__(self, nrows=1, ncols=1, figsize=(8, 6),
                 sharex=False, sharey=False):

        self.nrows = nrows
        self.ncols = ncols
        self.figsize = figsize
        self.sharex = sharex
        self.sharey = sharey
        self.plot_list = []

    def save_figure(self, pathfile, **kwargs):
        """
        Method to save figure to file
        """
        # Create directory if needed
        path, file = os.path.split(pathfile)
        if path != '':
            os.makedirs(path, exist_ok=True)

        # Remove deprecated options from dictionary
        if 'output name' in kwargs:
            del kwargs['output name']

        if 'tight_layout' in kwargs:
            del kwargs['tight_layout']

        # Save figure
        self.fig.savefig(pathfile, **kwargs)

    def tight_layout(self, **kwargs):
        """
        Set figure to tight layout.
        """
        self.fig.tight_layout(**kwargs)

    def close_figure(self):
        """
        Method to close figure
        """
        # Close figure
        plt.close()

    def create_figure(self):
        """
        Driver method to create figure and subplots.
        """
        # Validate grid shape vs. plot_list
        if len(self.plot_list) != self.nrows * self.ncols:
            raise ValueError(
                'Number of plots does not match the number inputted rows'
                'and columns.'
            )

        gs = gridspec.GridSpec(self.nrows, self.ncols)
        self.fig = plt.figure(figsize=self.figsize)

        # Track the last colorbar-capable artist per axes
        # (read by _last_mappable_for_ax in _plot_colorbar)
        self._ax_last_mappable = {}  # {Axes: mappable}

        for i, plot_obj in enumerate(self.plot_list):
            # --- Axes creation (map vs. normal) ---
            if hasattr(plot_obj, 'projection'):
                # Map: build domain/projection and a GeoAxes
                if isinstance(plot_obj.domain, (tuple, list)):
                    self.domain = Domain(domain=plot_obj.domain[0], dd=plot_obj.domain[1])
                else:
                    self.domain = Domain(plot_obj.domain)

                self.projection = MapProjection(plot_obj.projection)
                ax = self.fig.add_subplot(gs[i], projection=self.projection.projection)

                if str(self.projection) not in ['npstere', 'spstere']:
                    ax.set_extent(self.domain.extent)
                    if str(self.projection) not in ['lamconf']:
                        ax.set_xticks(self.domain.xticks, crs=ccrs.PlateCarree())
                        ax.set_yticks(self.domain.yticks, crs=ccrs.PlateCarree())
                        lon_formatter = LongitudeFormatter(zero_direction_label=False)
                        lat_formatter = LatitudeFormatter()
                        ax.xaxis.set_major_formatter(lon_formatter)
                        ax.yaxis.set_major_formatter(lat_formatter)
                else:
                    ax.set_extent(self.domain.extent, ccrs.PlateCarree())

            else:
                # Regular Axes (SkewT gets its projection)
                plot_types = [x.plottype for x in plot_obj.plot_layers]
                if 'skewt' in plot_types:
                    ax = self.fig.add_subplot(gs[i], projection='skewx')
                else:
                    ax = self.fig.add_subplot(gs[i])

            # --- Per-axes rendering state ---
            st = AxState(ax=ax)  # adapters append any mappables they create

            # --- Render each layer via the adapter registry ---
            for layer in plot_obj.plot_layers:
                adapter = get_adapter(layer.plottype)  # raises KeyError if unknown
                mappable = adapter.render(self, st, layer)
                if mappable is not None:
                    st.mappables.append(mappable)
                    self._ax_last_mappable[ax] = mappable  # used by _plot_colorbar

            # --- Plot figure/axes features (title, labels, ticks, colorbar, etc.) ---
            for feat in vars(plot_obj).keys():
                self._plot_features(plot_obj, feat, ax)

            # --- Shared axes label hiding ---
            if self.sharex:
                self._sharex(ax)
            if self.sharey:
                self._sharey(ax)

    def add_suptitle(self, text, **kwargs):
        """
        Add super title to figure. Useful for subplots.
        """
        if hasattr(self, 'fig'):
            self.fig.suptitle(text, **kwargs)

    def plot_logo(self, loc, which='noaa/nws',
                  subplot_orientation='last', zoom=1, alpha=0.5):
        """
        Add branding logo on all axes.
        """
        image_dict = {
            'noaa': 'noaa_logo_75x75.png',
            'nws': 'nws_logo_75x75.png',
            'noaa/nws': 'noaa_nws_logo_150x75.png'
        }

        image_path = os.path.join(emcpy.emcpy_directory, 'logos', image_dict[which])
        im = Image.open(image_path)

        if subplot_orientation.lower() not in ['first', 'last', 'all']:
            raise TypeError(f"{subplot_orientation} is not a valid input. " +
                            "Valid inputs include 'first', 'last', or 'all'")

        ax_list = self.fig.axes

        if subplot_orientation.lower() == 'first':
            ax = ax_list[0]
            self._display_logo(ax, im, loc, zoom, alpha)

        elif subplot_orientation.lower() == 'last':
            ax = ax_list[-1]
            self._display_logo(ax, im, loc, zoom, alpha)

        else:
            for ax in ax_list:
                self._display_logo(ax, im, loc, zoom, alpha)

    def _display_logo(self, ax, im, loc, zoom, alpha):

        loc_dict = {
            'upper right': 1,
            'upper left': 2,
            'lower left': 3,
            'lower right': 4,
            'center left': 6,
            'center right': 7,
            'lower center': 8,
            'upper center': 9,
            'center': 10
        }

        width, height = ax.figure.get_size_inches()*self.fig.dpi
        wm_width = int(width/4)  # make the watermark 1/4 of the figure size
        scaling = (wm_width / float(im.size[0]))
        wm_height = int(float(im.size[1])*float(scaling))

        imagebox = OffsetImage(im, zoom=zoom, alpha=alpha)
        imagebox.image.axes = ax

        ao = AnchoredOffsetbox(loc_dict[loc], pad=0.1, borderpad=0.1, child=imagebox)
        ao.patch.set_alpha(0)
        ax.add_artist(ao)

    def _plot_features(self, plot_obj, feature, ax):

        feature_dict = {
            'title': self._plot_title,
            'xlabel': self._plot_xlabel,
            'ylabel': self._plot_ylabel,
            'colorbar': self._plot_colorbar,
            'stats': self._plot_stats,
            'legend': self._plot_legend,
            'text': self._plot_text,
            'grid': self._plot_grid,
            'xlim': self._set_xlim,
            'ylim': self._set_ylim,
            'xticks': self._set_xticks,
            'yticks': self._set_yticks,
            'xticklabels': self._set_xticklabels,
            'yticklabels': self._set_yticklabels,
            'invert_xaxis': self._invert_xaxis,
            'invert_yaxis': self._invert_yaxis,
            'xscale': self._set_xscale,
            'yscale': self._set_yscale,
            'map_features': self._add_map_features
        }

        if feature in feature_dict:
            feature_dict[feature](ax, vars(plot_obj)[feature])

    def _map_scatter(self, plotobj, ax):

        integer_field = bool('integer_field' in vars(plotobj) and plotobj.integer_field)

        if plotobj.data is None:
            skip = ['plottype', 'longitude', 'latitude', 'markersize', 'integer_field', 'colorbar']
            inputs = self._get_inputs_dict(skip, plotobj)
            cs = ax.scatter(
                plotobj.longitude, plotobj.latitude,
                s=plotobj.markersize, **inputs,
                transform=self.projection.transform
            )

            return cs  # PathCollection

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar', 'normalize', 'integer_field']
        inputs = self._get_inputs_dict(skip, plotobj)

        norm = None
        if integer_field:
            cmap = matplotlib.cm.get_cmap(inputs['cmap'])
            vmin = inputs['vmin']
            vmax = inputs['vmax']
            if vmin is None or vmax is None:
                raise ValueError("For integer_field=True, set both vmin and vmax.")
            norm = matplotlib.colors.BoundaryNorm(np.arange(vmin - 0.5, vmax, 1), cmap.N)

        cs = ax.scatter(
            plotobj.longitude, plotobj.latitude,
            c=plotobj.data, s=plotobj.markersize,
            **inputs, norm=norm, transform=self.projection.transform
        )

        return cs  # PathCollection

    def _map_gridded(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)

        cs = None
        if getattr(plotobj.longitude, "ndim", 2) == 3:
            tiles = plotobj.longitude.shape[-1]
            for i in range(tiles):
                cs = ax.pcolormesh(
                    plotobj.longitude[:, :, i],
                    plotobj.latitude[:, :, i],
                    plotobj.data[:, :, i],
                    **inputs, transform=self.projection.transform
                )
        else:
            cs = ax.pcolormesh(
                plotobj.longitude, plotobj.latitude, plotobj.data,
                **inputs, transform=self.projection.transform
            )

        return cs  # QuadMesh (last plotted if multiple tiles)

    def _map_contour(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        cs = ax.contour(
            plotobj.longitude, plotobj.latitude, plotobj.data,
            **inputs, transform=self.projection.transform
        )
        if getattr(plotobj, 'clabel', False):
            plt.clabel(cs, levels=plotobj.levels, use_clabeltext=True)

        return cs  # ContourSet

    def _map_filled_contour(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        cs = ax.contourf(
            plotobj.longitude, plotobj.latitude, plotobj.data,
            **inputs, transform=self.projection.projection
        )
        if getattr(plotobj, 'clabel', False):
            plt.clabel(cs, levels=plotobj.levels, use_clabeltext=True)

        return cs  # ContourSet

    def _density_scatter(self, plotobj, ax):
        """
        Uses Scatter Object to plot density scatter colored by
        2d histogram.
        """
        _idx = np.logical_and(~np.isnan(plotobj.x), ~np.isnan(plotobj.y))
        data, x_e, y_e = np.histogram2d(
            plotobj.x[_idx], plotobj.y[_idx],
            bins=plotobj.density['bins'],
            density=not plotobj.density['nsamples']
        )
        if plotobj.density['nsamples']:
            data = data / np.count_nonzero(_idx) * 100.0

        z = interpn(
            (0.5 * (x_e[1:] + x_e[:-1]), 0.5 * (y_e[1:] + y_e[:-1])),
            data, np.vstack([plotobj.x, plotobj.y]).T,
            method=plotobj.density['interp'], bounds_error=False
        )
        z[np.where(np.isnan(z))] = 0.0
        if plotobj.density['sort']:
            idx = z.argsort()
            x, y, z = plotobj.x[idx], plotobj.y[idx], z[idx]
        else:
            x, y = plotobj.x, plotobj.y

        cs = ax.scatter(
            x, y, c=z, s=plotobj.markersize,
            cmap=plotobj.density['cmap'], label=plotobj.label
        )

        return cs  # PathCollection

    def _scatter(self, plotobj, ax):
        """
        Uses Scatter object to plot on axis.
        """
        if hasattr(plotobj, 'density'):
            cs = self._density_scatter(plotobj, ax)
        else:
            skip = ['plottype', 'plot_ax', 'x', 'y', 'markersize',
                    'do_linear_regression', 'linear_regression', 'density', 'channel']
            inputs = self._get_inputs_dict(skip, plotobj)
            cs = ax.scatter(plotobj.x, plotobj.y, s=plotobj.markersize, **inputs)

        # optional regression overlay (not a mappable)
        if getattr(plotobj, "do_linear_regression", False):
            if len(plotobj.x) and len(plotobj.y):
                y_pred, r_sq, intercept, slope = get_linear_regression(plotobj.x, plotobj.y)
                label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
                style = getattr(plotobj, "linear_regression", {})
                if "color" not in style:
                    point_color = getattr(plotobj, "color", None)
                    if point_color is not None:
                        style["color"] = point_color
                ax.plot(plotobj.x, y_pred, label=label, **style)

        return cs  # PathCollection

    def _gridded(self, plotobj, ax):
        """
        Uses Gridded object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        cs = ax.pcolormesh(plotobj.x, plotobj.y, plotobj.z, **inputs)

        return cs  # QuadMesh

    def _contour(self, plotobj, ax):
        """
        Uses ContourPlot object to plot on axis.
        """
        skip = ['plottype', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        cs = ax.contour(plotobj.x, plotobj.y, plotobj.z, **inputs)

        return cs  # ContourSet

    def _contourf(self, plotobj, ax):
        """
        Use FilledContourPlot object to plot on axis.
        """
        skip = ['plottype', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        cs = ax.contourf(plotobj.x, plotobj.y, plotobj.z, **inputs)

        return cs  # ContourSet

    def _histogram(self, plotobj, ax):
        """
        Uses Histogram object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'data']
        inputs = self._get_inputs_dict(skip, plotobj)
        _, _, patches = ax.hist(plotobj.data, **inputs)

        return patches  # list[Rectangle] (not a ScalarMappable)

    def _density(self, plotobj, ax):
        """
        Uses Density object to plot on axis.
        """
        import seaborn as sns
        skip = ['plottype', 'plot_ax', 'data']
        inputs = self._get_inputs_dict(skip, plotobj)
        artist = sns.kdeplot(data=plotobj.data, ax=ax, **inputs)

        return artist  # Axes/Line2D-like (not a ScalarMappable)

    def _lineplot(self, plotobj, ax):
        """
        Uses LinePlot object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)
        lines = ax.plot(plotobj.x, plotobj.y, **inputs)

        return lines[0] if lines else None  # Line2D (not a ScalarMappable)

    def _skewt(self, plotobj, ax):
        """
        Creates a skewt-logp profile plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)
        # Plot data using log scaling Y
        lines = ax.semilogy(plotobj.x, plotobj.y, **inputs)

        # Disables the log-formatting that comes with semilogy
        ax.yaxis.set_major_formatter(ScalarFormatter())
        ax.yaxis.set_minor_formatter(NullFormatter())

        # Setting custom ylim and xlims; can be changed
        ax.set_yticks(np.linspace(100, 1000, 10))
        ax.set_ylim(1050, 100)

        ax.xaxis.set_major_locator(MultipleLocator(10))
        ax.set_xlim(-45, 30)

        return lines[0] if lines else None  # Line2D (not a ScalarMappable)

    def _verticalline(self, plotobj, ax):
        """
        Uses VerticalLine object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x']
        inputs = self._get_inputs_dict(skip, plotobj)
        ln = ax.axvline(plotobj.x, **inputs)

        return ln  # Line2D

    def _horizontalline(self, plotobj, ax):
        """
        Uses HorizontalLine object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)
        ln = ax.axhline(plotobj.y, **inputs)

        return ln  # Line2D

    def _horizontalspan(self, plotobj, ax):
        """
        Uses HorizontalSpan object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'ymin', 'ymax']
        inputs = self._get_inputs_dict(skip, plotobj)
        poly = ax.axhspan(plotobj.ymin, plotobj.ymax, **inputs)

        return poly  # PolyCollection

    def _barplot(self, plotobj, ax):
        """
        Uses BarPlot object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'height']
        inputs = self._get_inputs_dict(skip, plotobj)
        cont = ax.bar(plotobj.x, plotobj.height, **inputs)

        return cont  # BarContainer (not a ScalarMappable)

    def _hbar(self, plotobj, ax):
        """
        Uses HorizontalBar object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'y', 'width']
        inputs = self._get_inputs_dict(skip, plotobj)
        cont = ax.barh(plotobj.y, plotobj.width, **inputs)

        return cont  # BarContainer (not a ScalarMappable)

    def _boxandwhisker(self, plotobj, ax):
        """
        Uses BoxandWhiskerPlot object to plot on axis.
        """
        skip = ['plottype', 'data']
        inputs = self._get_inputs_dict(skip, plotobj)

        if 'labels' in inputs:  # defensive against old kw
            raise TypeError("BoxandWhiskerPlot no longer supports 'labels'; use 'tick_labels' (Matplotlib 3.9+).")

        bp = ax.boxplot(plotobj.data, **inputs)

        return bp  # dict of artists (not a ScalarMappable)

    def _get_inputs_dict(self, skipvars, plotobj):
        """
        Creates dictionary for plot inputs. Skips variables
        in 'skipvars' list.
        """
        inputs = {}
        for v in [v for v in vars(plotobj) if v not in skipvars]:
            val = getattr(plotobj, v)
            if val is not None:
                inputs[v] = val

        return inputs

    def _plot_title(self, ax, title):
        """
        Add title on specified ax.
        """
        ax.set_title(**title)

    def _plot_xlabel(self, ax, xlabel):
        """
        Add xlabel on specified ax.
        """
        ax.set_xlabel(**xlabel)

    def _plot_ylabel(self, ax, ylabel):
        """
        Add ylabel on specified ax.
        """
        ax.set_ylabel(**ylabel)

    def _last_mappable_for_ax(self, ax: plt.Axes) -> Optional[Any]:
        """
        Return the most recently-added ScalarMappable for a given Axes.

        Uses the adapter-tracked value first (set when a layer returns a
        mappable). Falls back to scanning Axes collections/images in reverse
        (newest-first). Intentionally ignores 'containers' (e.g., BarContainer),
        which are not ScalarMappable and cannot be used for colorbars.
        """
        m = getattr(self, "_ax_last_mappable", {}).get(ax)
        if isinstance(m, ScalarMappable):
            return m

        # Fallback: newest-first among valid ScalarMappables
        for coll in reversed(ax.collections):
            if isinstance(coll, ScalarMappable):
                return coll
        for img in reversed(ax.images):
            if isinstance(img, ScalarMappable):
                return img

        return None

    def _plot_colorbar(self, ax, colorbar):
        """
        Add colorbar on specified ax or for total figure (single_cbar).
        Uses the most recently-added mappable on this axes.
        """
        mappable = self._last_mappable_for_ax(ax)
        if mappable is None:
            return

        if colorbar['single_cbar']:
            # Only on the bottom-right subplot
            if self._is_last_subplot(ax):
                cbar_ax = self.fig.add_axes(colorbar['cbar_loc'])
                cb = self.fig.colorbar(mappable, cax=cbar_ax, **colorbar['kwargs'])
                if colorbar['label'] is not None:
                    cb.set_label(colorbar['label'], fontsize=colorbar['fontsize'])
            return

        # per-axes colorbar
        cb = self.fig.colorbar(mappable, ax=ax, **colorbar['kwargs'])
        if colorbar['label'] is not None:
            cb.set_label(colorbar['label'], fontsize=colorbar['fontsize'])

    def _plot_stats(self, ax, stats):
        """
        Add annotated stats on specified ax.
        """
        # loop through the dictionary and create the string to annotate
        outstr = ''
        for key, value in stats['stats'].items():
            outstr = outstr + f'{key}: {value}    '

        ax.annotate(outstr, xy=(stats['xloc'], stats['yloc']),
                    xycoords='axes fraction', ha=stats['ha'],
                    **stats['kwargs'])

    def _plot_legend(self, ax, legend):
        """
        Add legend on specified ax.
        """
        leg = ax.legend(**legend)

        # Matplotlib versions differ in attribute name
        handles = getattr(leg, "legend_handles", None) or getattr(leg, "legendHandles", [])

        for h in handles:
            # PathCollection (scatter) has a public setter
            if hasattr(h, "set_sizes"):
                h.set_sizes([20])
            # Fallback for older MPL where only the private attr exists
            elif hasattr(h, "_sizes"):
                h._sizes = [20]

    def _plot_text(self, ax, text_in):
        """
        Add text on specified ax.
        """
        for text in text_in:
            if text['transform'] not in ['datacoords', 'axcoords']:
                raise ValueError('Transform input is not valid. ' +
                                 'Valid options include ["datacoords", ' +
                                 '"axcoords"].')

            transform = ax.transAxes if text['transform'] == 'axcoords' else ax.transData

            ax.text(text['xloc'], text['yloc'],
                    text['text'], transform=transform,
                    **text['kwargs'])

    def _plot_grid(self, ax, grid):
        """
        Add grid on specified ax.
        """
        try:
            ax.gridlines(crs=ccrs.PlateCarree(), **grid)
        except AttributeError:
            ax.grid(**grid)

    def _set_xlim(self, ax, xlim):
        """
        Set x-limits on specified ax.
        """
        ax.set_xlim(**xlim)

    def _set_ylim(self, ax, ylim):
        """
        Set y-limits on specified ax.
        """
        ax.set_ylim(**ylim)

    def _as_mpl_dates(self, ticks):
        """
        Convert a list of datetime-like objects to Matplotlib date numbers.
        Returns (converted_ticks, is_datetime).
        Accepts: datetime.datetime, datetime.date, numpy.datetime64, pandas.Timestamp.
        """
        if not ticks:
            return ticks, False

        first = ticks[0]

        # Python datetime/date
        is_dt = isinstance(first, (datetime.datetime, datetime.date))

        # numpy.datetime64
        try:
            is_dt = is_dt or isinstance(first, np.datetime64)
        except Exception:
            pass

        # pandas.Timestamp (optional)
        try:
            is_dt = is_dt or hasattr(first, "to_pydatetime")
        except Exception:
            pass

        if is_dt:
            return mdates.date2num(ticks), True

        return ticks, False

    def _apply_ticks(self, ax, axis: str, spec: dict, *, latlon: bool = False) -> None:
        """
        Install locators/formatters for x|y ticks in a single place.

        spec keys (all optional):
          - ticks: list[Any]  (numbers, datetimes, etc.)
          - minor: bool       (default False)
          - formatter: matplotlib Formatter or callable
          - date_format: str  (applied via DateFormatter when datetime & major)
          - clear_minor: bool (default True; when setting major ticks, clear minor)
        """
        ticks = spec.get("ticks", [])
        minor = bool(spec.get("minor", False))
        formatter = spec.get("formatter")
        date_fmt = spec.get("date_format")
        clear_minor = spec.get("clear_minor", True)

        if latlon:
            if axis == "x":
                ax.set_xticks(ticks, crs=ccrs.PlateCarree())
                ax.xaxis.set_major_formatter(LongitudeFormatter(zero_direction_label=True))
            else:
                ax.set_yticks(ticks, crs=ccrs.PlateCarree())
                ax.yaxis.set_major_formatter(LatitudeFormatter())
            return

        ticks2, is_dt = self._as_mpl_dates(ticks)
        locator = FixedLocator(ticks2)

        if axis == "x":
            (ax.xaxis.set_minor_locator if minor else ax.xaxis.set_major_locator)(locator)

            if not minor:
                if formatter is not None:
                    ax.xaxis.set_major_formatter(formatter)
                elif is_dt:
                    ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt or "%Y-%m-%d\n%H:%M"))

                if clear_minor:
                    ax.xaxis.set_minor_locator(NullLocator())

        else:
            (ax.yaxis.set_minor_locator if minor else ax.yaxis.set_major_locator)(locator)

            if not minor:
                if formatter is not None:
                    ax.yaxis.set_major_formatter(formatter)
                elif is_dt:
                    ax.yaxis.set_major_formatter(mdates.DateFormatter(date_fmt or "%Y-%m-%d\n%H:%M"))

                if clear_minor:
                    ax.yaxis.set_minor_locator(NullLocator())

    def _set_xticks(self, ax, xticks, latlon=False):
        """
        Set x-ticks on specified ax.
        """
        self._apply_ticks(ax, "x", xticks, latlon=latlon)

    def _set_yticks(self, ax, yticks, latlon=False):
        """
        Set y-ticks on specified ax.
        """
        self._apply_ticks(ax, "y", yticks, latlon=latlon)

    def _set_xticklabels(self, ax, xticklabels):
        """
        Set x-tick labels on specified ax.

        Accepts:
          - labels: list[str] for MAJOR ticks
          - minor: bool (default False): minor labels are not supported
          - date_format: str: prefer a DateFormatter instead of static labels
          - kwargs: dict: text kwargs (rotation, ha, fontsize, etc.)
        """
        labels = xticklabels.get("labels", [])
        minor = bool(xticklabels.get("minor", False))
        kwargs = xticklabels.get("kwargs", {})
        date_fmt = xticklabels.get("date_format")

        if minor:
            raise ValueError("Setting MINOR tick labels is not supported; use a custom Formatter.")

        # If datetime formatting is requested, prefer a DateFormatter.
        if date_fmt is not None:
            ax.xaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
            return

        current_ticks = ax.get_xticks(minor=False)
        if len(labels) != len(current_ticks):
            raise ValueError(
                f"Len of xtick labels ({len(labels)}) != len of xticks ({len(current_ticks)}). "
                "Set ticks appropriately or supply matching labels."
            )
        ax.set_xticklabels(labels, **kwargs)

    def _set_yticklabels(self, ax, yticklabels):
        """
        Set y-tick labels on specified ax.

        Accepts:
          - labels: list[str] for MAJOR ticks
          - minor: bool (default False): minor labels are not supported
          - date_format: str: prefer a DateFormatter instead of static labels
          - kwargs: dict: text kwargs (rotation, ha, fontsize, etc.)
        """
        labels = yticklabels.get("labels", [])
        minor = bool(yticklabels.get("minor", False))
        kwargs = yticklabels.get("kwargs", {})
        date_fmt = yticklabels.get("date_format")

        if minor:
            raise ValueError("Setting MINOR tick labels is not supported; use a custom Formatter.")

        # If datetime formatting is requested, prefer a DateFormatter.
        if date_fmt is not None:
            ax.yaxis.set_major_formatter(mdates.DateFormatter(date_fmt))
            return

        current_ticks = ax.get_yticks(minor=False)
        if len(labels) != len(current_ticks):
            raise ValueError(
                f"Len of ytick labels ({len(labels)}) != len of yticks ({len(current_ticks)}). "
                "Set ticks appropriately or supply matching labels."
            )
        ax.set_yticklabels(labels, **kwargs)

    def _invert_xaxis(self, ax, invert_xaxis):
        """
        Invert x-axis on specified ax.
        """
        if invert_xaxis:
            ax.invert_xaxis()

    def _invert_yaxis(self, ax, invert_yaxis):
        """
        Invert y-axis on specified ax.
        """
        if invert_yaxis:
            ax.invert_yaxis()

    def _set_xscale(self, ax, xscale):
        """
        Set x-scale on specified ax.
        """
        ax.set_xscale(xscale)

    def _set_yscale(self, ax, yscale):
        """
        Set y-scale on specified ax.
        """
        ax.set_yscale(yscale)

    def _sharex(self, ax):
        """
        If sharex axis is True, will find where to hide xticklabels.
        """
        if not self._is_last_row(ax):
            plt.setp(ax.get_xticklabels(), visible=False)

    def _sharey(self, ax):
        """
        If sharey axis is True, will find where to hide yticklabels.
        """
        if not self._is_first_col(ax):
            plt.setp(ax.get_yticklabels(), visible=False)

    def _subplot_spec(self, ax):
        """
        Return a tuple (ss, gs) where:
            - ss is a matplotlib SubplotSpec object for the given axis.
            - gs is the corresponding matplotlib GridSpec object.
        Returns (None, None) if ax is not a GridSpec subplot.
        """
        try:
            ss = ax.get_subplotspec()
            return ss, ss.get_gridspec()
        except AttributeError:
            return None, None

    def _is_first_col(self, ax) -> bool:
        ss, _ = self._subplot_spec(ax)
        return bool(ss and ss.colspan.start == 0)

    def _is_last_col(self, ax) -> bool:
        ss, gs = self._subplot_spec(ax)
        return bool(ss and gs and ss.colspan.stop == gs.ncols)

    def _is_first_row(self, ax) -> bool:
        ss, _ = self._subplot_spec(ax)
        return bool(ss and ss.rowspan.start == 0)

    def _is_last_row(self, ax) -> bool:
        ss, gs = self._subplot_spec(ax)
        return bool(ss and gs and ss.rowspan.stop == gs.nrows)

    def _is_last_subplot(self, ax) -> bool:
        """Bottom-right subplot in the current GridSpec."""
        ss, gs = self._subplot_spec(ax)
        return bool(ss and gs and ss.rowspan.stop == gs.nrows and ss.colspan.stop == gs.ncols)

    def _add_map_features(self, ax, map_features):
        """
        Factory to add map features.
        """
        feature_dict = {
            'coastline': cfeature.COASTLINE,
            'borders': cfeature.BORDERS,
            'states': cfeature.STATES,
            'lakes': cfeature.LAKES,
            'rivers': cfeature.RIVERS,
            'land': cfeature.LAND,
            'ocean': cfeature.OCEAN
        }

        for feat in map_features:
            try:
                ax.add_feature(feature_dict[feat])
            except KeyError:
                raise TypeError(f'{feat} is not a valid map feature.' +
                                'Current map features supported are:\n' +
                                f'{" | ".join(feature_dict.keys())}"')
