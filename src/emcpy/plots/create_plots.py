# This work developed by NOAA/NWS/EMC under the Apache 2.0 license.
import os
import warnings
import emcpy
import numpy as np
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
from cartopy.mpl.geoaxes import GeoAxes
from matplotlib import colormaps as _cmaps
from matplotlib.cm import ScalarMappable
from matplotlib.contour import ContourSet
from matplotlib.offsetbox import OffsetImage, AnchoredOffsetbox
from matplotlib.ticker import MultipleLocator, FixedLocator, NullLocator
from matplotlib.ticker import NullFormatter, ScalarFormatter
from matplotlib.projections import register_projection
from emcpy.plots.adapters import get_adapter
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.skewt_projection import SkewXAxes
from emcpy.stats.stats import get_linear_regression

__all__ = ['CreateFigure', 'CreatePlot']

# Register SkewXAxes projection exactly once
try:
    register_projection(SkewXAxes)
except ValueError:
    pass


@dataclass
class AxState:
    ax: plt.Axes
    mappables: List[Any] = field(default_factory=list)
    is_map: bool = False


class CreatePlot:
    """
    Creates a figure to plot data as a scatter plot,
    histogram, density or line plot.
    """
    def __init__(self, plot_layers=None, projection=None,
                 domain=None):
        self.plot_layers = [] if plot_layers is None else list(plot_layers)

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

    def add_map_features(self, feature_list=None):

        self.map_features = ['coastline'] if feature_list is None else feature_list

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

    def set_xticks(self, ticks=None, minor=False, formatter=None, date_format=None, clear_minor=True):

        self.xticks = {
            "ticks": [] if ticks is None else ticks,
            "minor": minor,
            "formatter": formatter,
            "date_format": date_format,
            "clear_minor": clear_minor,
        }

    def set_yticks(self, ticks=None, minor=False, formatter=None, date_format=None, clear_minor=True):

        self.yticks = {
            "ticks": [] if ticks is None else ticks,
            "minor": minor,
            "formatter": formatter,
            "date_format": date_format,
            "clear_minor": clear_minor,
        }

    def set_xticklabels(self, labels=None, minor=False, date_format=None, **kwargs):

        self.xticklabels = {
            "labels": [] if labels is None else labels,
            "minor": minor,
            "date_format": date_format,
            "kwargs": kwargs,
        }

    def set_yticklabels(self, labels=None, minor=False, date_format=None, **kwargs):

        self.yticklabels = {
            "labels": [] if labels is None else labels,
            "minor": minor,
            "date_format": date_format,
            "kwargs": kwargs,
        }

    def invert_xaxis(self):

        setattr(self, "_invert_x", True)

    def invert_yaxis(self):

        setattr(self, "_invert_y", True)

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

    def add_twinx(self, *layers):
        """
        Enable a secondary y-axis (twinx). Optionally pass one or more layers
        that should be rendered on the right-hand axis.
        """
        if layers:
            if not hasattr(self, "twin_layers"):
                self.twin_layers = []
            self.twin_layers.extend(layers)
        self._use_twinx = True

    def add_twin_ylabel(self, ylabel, labelpad=None, loc='center', **kwargs):
        """
        Y label for the secondary y-axis.
        """
        self.twin_ylabel = {
            'ylabel': ylabel,
            'labelpad': labelpad,
            'loc': loc,
            **kwargs
        }

    def set_twin_ylim(self, bottom=None, top=None):
        self.twin_ylim = {'bottom': bottom, 'top': top}

    def set_twin_yscale(self, scale):
        valid_scales = ['log', 'linear', 'symlog', 'logit']
        if scale not in valid_scales:
            raise ValueError(f'requested scale {scale} is invalid. Valid '
                             f'choices are: {" | ".join(valid_scales)}')
        self.twin_yscale = scale

    def set_twin_yticks(self, ticks=None, minor=False, formatter=None, date_format=None, clear_minor=True):
        self.twin_yticks = {
            "ticks": [] if ticks is None else ticks,
            "minor": minor,
            "formatter": formatter,
            "date_format": date_format,
            "clear_minor": clear_minor,
        }

    def set_twin_yticklabels(self, labels=None, minor=False, date_format=None, **kwargs):
        self.twin_yticklabels = {
            "labels": [] if labels is None else labels,
            "minor": minor,
            "date_format": date_format,
            "kwargs": kwargs,
        }

    def set_time_axis(self, major="month", minor="week", fmt="%b %Y", rotate=30, ha="right"):
        """
        Configure a time-aware x-axis with common defaults.

        Parameters
        ----------
        major : {"year","quarter","month","week","day","hour"}, default "month"
        minor : {"quarter","month","week","day","hour",None}, default "week"
        fmt   : str, date format passed to DateFormatter, default "%b %Y"
        rotate: int, rotation for tick labels, default 30
        ha    : str, horizontalalignment for tick labels, default "right"
        """
        self.time_axis = {
            "major": major,
            "minor": minor,
            "fmt": fmt,
            "rotate": rotate,
            "ha": ha,
        }


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

            # --- Optional secondary y-axis (twinx) ---
            ax_twin = None
            if getattr(plot_obj, "_use_twinx", False) or getattr(plot_obj, "twin_layers", None):
                ax_twin = ax.twinx()

            # --- Per-axes rendering state (primary) ---
            st = AxState(ax=ax)  # adapters append any mappables they create

            # --- Render each primary-layer via the adapter registry ---
            for layer in plot_obj.plot_layers:
                adapter = get_adapter(layer.plottype)  # raises KeyError if unknown
                mappable = adapter.render(self, st, layer)
                if mappable is not None:
                    st.mappables.append(mappable)

            # --- Render twinx layers (if any) ---
            if ax_twin is not None:
                st_twin = AxState(ax=ax_twin)
                for layer in getattr(plot_obj, "twin_layers", []):
                    adapter = get_adapter(layer.plottype)
                    mappable = adapter.render(self, st_twin, layer)
                    if mappable is not None:
                        st_twin.mappables.append(mappable)

            # --- Plot figure/axes features (title, labels, ticks, colorbar, etc.) on primary ---
            for feat in vars(plot_obj).keys():
                self._plot_features(plot_obj, feat, ax)

            # Apply invert flags on primary
            self._apply_invert_flags(plot_obj, ax)

            # --- Shared axes label hiding (primary only) ---
            if self.sharex:
                self._sharex(ax)
            if self.sharey:
                self._sharey(ax)

            # Final per-axes polish (e.g., time-axis formatting) on primary
            self._finalize_axis(ax, plot_obj)

            # --- Apply twin-axis specific features & finalize (if present) ---
            if ax_twin is not None:
                if hasattr(plot_obj, 'twin_ylabel'):
                    self._plot_ylabel(ax_twin, plot_obj.twin_ylabel)
                if hasattr(plot_obj, 'twin_ylim'):
                    self._set_ylim(ax_twin, plot_obj.twin_ylim)
                if hasattr(plot_obj, 'twin_yscale'):
                    self._set_yscale(ax_twin, plot_obj.twin_yscale)
                if hasattr(plot_obj, 'twin_yticks'):
                    self._set_yticks(ax_twin, plot_obj.twin_yticks)
                if hasattr(plot_obj, 'twin_yticklabels'):
                    self._set_yticklabels(ax_twin, plot_obj.twin_yticklabels)

                # No sharey logic for twin axis; x is shared implicitly
                self._finalize_axis(ax_twin, plot_obj)

    def add_suptitle(self, text, **kwargs):
        """
        Add super title to figure. Useful for subplots.
        """
        if hasattr(self, 'fig'):
            self.fig.suptitle(text, **kwargs)

    def add_shared_colorbar(self, mappable, axes, *, location: str = "right", label: str | None = None):
        """
        Add a single colorbar shared across the given axes (list of Axes).

        Parameters
        ----------
        mappable : matplotlib.cm.ScalarMappable
            The mappable returned by a plotting call (e.g., hexbin, pcolormesh).
        axes : list[matplotlib.axes.Axes] or matplotlib.axes.Axes
            Axes to which the colorbar should be associated.
        location : {"right", "left", "top", "bottom"}, default "right"
            Where to draw the colorbar relative to the axes grid.
        label : str, optional
            Colorbar label text.
        """
        if not isinstance(axes, (list, tuple)):
            axes = [axes]
        cbar = self.fig.colorbar(mappable, ax=axes, location=location)
        if label:
            cbar.set_label(label)
        return cbar

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
            'xscale': self._set_xscale,
            'yscale': self._set_yscale,
            'map_features': self._add_map_features
        }

        if feature in feature_dict:
            feature_dict[feature](ax, vars(plot_obj)[feature])

    def _map_transform(self):
        """
        Return the CRS to be used as the data transform for map layers.

        Preference order:
          1) self.projection.transform  (explicit data CRS, e.g., PlateCarree for lat/lon)
          2) self.projection.projection (axes projection as a fallback)
          3) cartopy.crs.PlateCarree()  (final fallback with a warning)

        This makes _map_* renderers robust even if MapProjection is extended
        or customized and one of the attributes is missing.
        """
        tr = getattr(self.projection, "transform", None)
        if tr is not None:
            return tr

        pr = getattr(self.projection, "projection", None)
        if pr is not None:
            return pr

        warnings.warn(
            "MapProjection has neither 'transform' nor 'projection'; "
            "defaulting to PlateCarree().",
            RuntimeWarning,
            stacklevel=3,
        )

        return ccrs.PlateCarree()

    def _map_scatter(self, plotobj, ax):

        integer_field = bool(getattr(plotobj, "integer_field", False))
        xform = self._map_transform()

        if plotobj.data is None:
            # unlabeled points (no scalar mapping)
            skip = ['plottype', 'longitude', 'latitude', 'markersize', 'integer_field', 'colorbar']
            inputs = self._get_inputs_dict(skip, plotobj)
            cs = ax.scatter(
                plotobj.longitude, plotobj.latitude,
                s=plotobj.markersize, **inputs, transform=xform
            )
            return cs  # PathCollection (not scalar-mappable)

        # scalar-mapped points
        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize',
                'colorbar', 'normalize', 'integer_field']
        inputs = self._get_inputs_dict(skip, plotobj)

        norm = None
        if integer_field:
            vmin = inputs.get('vmin')
            vmax = inputs.get('vmax')
            if vmin is None or vmax is None:
                raise ValueError(
                    "For integer_field=True, both vmin and vmax must "
                    "be provided on the MapScatter layer."
                )
            cmap_name = inputs.get('cmap', 'viridis')
            cmap = _cmaps.get_cmap(cmap_name)
            norm = matplotlib.colors.BoundaryNorm(
                np.arange(vmin - 0.5, vmax + 0.5, 1), cmap.N
            )
            inputs.setdefault('cmap', cmap)
            # IMPORTANT: cannot pass vmin/vmax together with a norm
            inputs.pop('vmin', None)
            inputs.pop('vmax', None)

        # If we’re passing c=..., drop conflicting color keys
        inputs.pop('c', None)
        inputs.pop('color', None)
        inputs.pop('facecolor', None)
        inputs.pop('facecolors', None)

        cs = ax.scatter(
            plotobj.longitude, plotobj.latitude,
            c=plotobj.data, s=plotobj.markersize,
            **inputs, norm=norm, transform=xform
        )

        return cs

    def _map_gridded(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()

        cs = None
        if getattr(plotobj.longitude, "ndim", 2) == 3:
            tiles = plotobj.longitude.shape[-1]
            for i in range(tiles):
                cs = ax.pcolormesh(
                    plotobj.longitude[:, :, i],
                    plotobj.latitude[:, :, i],
                    plotobj.data[:, :, i],
                    **inputs, transform=xform
                )
        else:
            cs = ax.pcolormesh(
                plotobj.longitude, plotobj.latitude, plotobj.data,
                **inputs, transform=xform
            )

        return cs  # QuadMesh (last plotted if multiple tiles)

    def _map_contour(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar', 'clabel']
        inputs = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()
        cs = ax.contour(plotobj.longitude, plotobj.latitude, plotobj.data, **inputs, transform=xform)
        if getattr(plotobj, 'clabel', False):
            plt.clabel(cs, levels=plotobj.levels, use_clabeltext=True)

        return cs  # ContourSet

    def _map_filled_contour(self, plotobj, ax):

        skip = ['plottype', 'longitude', 'latitude', 'data', 'colorbar', 'clabel']
        inputs = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()
        cs = ax.contourf(plotobj.longitude, plotobj.latitude, plotobj.data, **inputs, transform=xform)
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
        Returns the PathCollection (mappable when `c` is provided).
        """
        # density mode uses a different path
        if hasattr(plotobj, 'density'):
            return self._density_scatter(plotobj, ax)

        skipvars = ['plottype', 'plot_ax', 'x', 'y',
                    'markersize', 'do_linear_regression',
                    'linear_regression', 'density', 'channel']
        inputs = self._get_inputs_dict(skipvars, plotobj)

        # If the layer provided a scalar/array color via `c`, remove conflicting color keys
        c_val = getattr(plotobj, 'c', None)
        if c_val is not None:
            # kill all conflicting color sources
            inputs.pop('c', None)
            inputs.pop('color', None)
            inputs.pop('facecolor', None)
            inputs.pop('facecolors', None)
            cs = ax.scatter(plotobj.x, plotobj.y, s=plotobj.markersize, c=c_val, **inputs)
        else:
            cs = ax.scatter(plotobj.x, plotobj.y, s=plotobj.markersize, **inputs)

        # Optional regression line
        if getattr(plotobj, "do_linear_regression", False):
            if len(plotobj.x) and len(plotobj.y):
                y_pred, r_sq, intercept, slope = get_linear_regression(plotobj.x, plotobj.y)
                label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
                style = getattr(plotobj, "linear_regression", {})
                if "color" not in style and hasattr(plotobj, "color"):
                    style["color"] = plotobj.color
                ax.plot(plotobj.x, y_pred, label=label, **style)

        return cs

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
        # Let the object produce Matplotlib-ready kwargs
        inputs, legend_label = plotobj.to_mpl_kwargs()

        # Single call to Matplotlib (no version-specific kwargs left)
        bp = ax.boxplot(plotobj.data, **inputs)

        # Reattach legend label to an artist so add_legend() works
        if legend_label is not None:
            try:
                if bp.get('boxes'):
                    bp['boxes'][0].set_label(legend_label)
                elif bp.get('medians'):
                    bp['medians'][0].set_label(legend_label)
            except Exception:
                pass

        return bp  # dict of artists

    def _fillbetween(self, plotobj, ax):
        """
        Render FillBetween layer.
        """
        skip = ['plottype', 'x', 'y1', 'y2']
        inputs = self._get_inputs_dict(skip, plotobj)
        poly = ax.fill_between(
            plotobj.x, plotobj.y1, plotobj.y2,
            **inputs
        )
        return poly  # PolyCollection (not a ScalarMappable)

    def _errorbar(self, plotobj, ax):
        """
        Render ErrorBar layer.
        """
        skip = ['plottype', 'x', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)
        cont = ax.errorbar(
            plotobj.x, plotobj.y,
            **inputs
        )
        return cont  # ErrorbarContainer (not necessarily a ScalarMappable)

    def _violin(self, plotobj, ax):
        """
        Render ViolinPlot layer.
        """
        skip = ['plottype', 'data']
        inputs = self._get_inputs_dict(skip, plotobj)

        vio = ax.violinplot(
            plotobj.data,
            positions=inputs.pop('positions', None),
            widths=inputs.pop('widths', None),
            showmeans=inputs.pop('showmeans', False),
            showmedians=inputs.pop('showmedians', True),
            showextrema=inputs.pop('showextrema', True),
        )

        # Apply alpha to bodies if requested
        alpha = inputs.pop('alpha', None)
        if alpha is not None:
            for b in vio.get('bodies', []):
                b.set_alpha(alpha)

        return vio  # dict of artists

    def _hexbin(self, plotobj, ax):
        """
        Render HexBin layer.
        """
        skip = [
            'plottype', 'x', 'y', 'C',
            # colorbar-related fields are handled by CreatePlot.add_colorbar()
            'colorbar', 'colorbar_label', 'colorbar_location'
        ]
        inputs = self._get_inputs_dict(skip, plotobj)
        hb = ax.hexbin(
            plotobj.x, plotobj.y, C=getattr(plotobj, 'C', None),
            **inputs
        )

        return hb  # PolyCollection (ScalarMappable)

    def _hist2d(self, plotobj, ax):
        """
        Render Hist2D layer.
        """
        skip = [
            'plottype', 'x', 'y',
            # colorbar-related fields are handled by CreatePlot.add_colorbar()
            'colorbar', 'colorbar_label', 'colorbar_location'
        ]
        inputs = self._get_inputs_dict(skip, plotobj)
        h, xedges, yedges, img = ax.hist2d(
            plotobj.x, plotobj.y,
            **inputs
        )
        alpha = getattr(plotobj, "alpha", None)
        if alpha is not None:
            img.set_alpha(alpha)

        return img  # QuadMesh (ScalarMappable)

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

    def _is_colorbar_source(self, m) -> bool:
        """
        Return True if artist 'm' can meaningfully drive a colorbar.

        Accept:
          - ContourSet (levels/norm/cmap define the scale)
          - ScalarMappable with a non-empty data array (e.g., PathCollection with 'c=',
            QuadMesh from pcolormesh, Images, etc.)
        Reject:
          - Collections with only a constant facecolor (no scalar data attached)
          - Anything that isn't a ScalarMappable/ContourSet
        """
        if isinstance(m, ContourSet):
            return True
        if isinstance(m, ScalarMappable):
            arr = m.get_array()
            if arr is None:
                return False
            try:
                return np.size(arr) > 0
            except (TypeError, AttributeError):
                # If size introspection fails, err on the safe side and reject.
                return False

        return False

    def _last_mappable_for_ax(self, ax) -> Optional[Any]:
        """
        Return the most recently-added *valid* colorbar source on this Axes.
        """
        # Newest-first search across typical mappable containers
        for m in list(ax.collections[::-1]) + list(ax.images[::-1]) + list(ax.containers[::-1]):
            if self._is_colorbar_source(m):
                return m

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

        if leg is None:
            return

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
        if isinstance(ax, GeoAxes):
            latlon = True
        self._apply_ticks(ax, "x", xticks, latlon=latlon)

    def _set_yticks(self, ax, yticks, latlon=False):
        """
        Set y-ticks on specified ax.
        """
        if isinstance(ax, GeoAxes):
            latlon = True
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

    def _apply_invert_flags(self, plot_obj, ax):
        """
        Apply axis inversion honoring both the new method-based flags
        (set by CreatePlot.invert_xaxis()/invert_yaxis()) and the legacy
        boolean attributes (plot.invert_xaxis = True / plot.invert_yaxis = True).

        This runs after limits/scales/ticks so inversion is final and does
        not get undone by later adjustments.
        """
        # New method flags set by CreatePlot.invert_* methods
        use_x = bool(getattr(plot_obj, "_invert_x", False))
        use_y = bool(getattr(plot_obj, "_invert_y", False))

        # Legacy attributes: users might have set a boolean directly on the instance
        legacy_x_attr = getattr(plot_obj, "invert_xaxis", None)
        legacy_y_attr = getattr(plot_obj, "invert_yaxis", None)

        def _is_legacy_true(v) -> bool:
            # Accept Python bool and numpy.bool_ as "true"; ignore callables (the method)
            # and other non-bool types.
            import numpy as _np  # local import to avoid any surprises at import time
            return isinstance(v, (bool, _np.bool_)) and bool(v)

        legacy_x = _is_legacy_true(legacy_x_attr) and not use_x
        legacy_y = _is_legacy_true(legacy_y_attr) and not use_y

        if legacy_x or legacy_y:
            warnings.warn(
                "Setting 'invert_xaxis'/'invert_yaxis' as booleans is deprecated; "
                "call plot.invert_xaxis() / plot.invert_yaxis() instead.",
                DeprecationWarning,
                stacklevel=2,
            )

        # Perform inversion once per axis if any path requests it
        if use_x or legacy_x:
            ax.invert_xaxis()
        if use_y or legacy_y:
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

    def _apply_time_axis(self, ax, opts: Optional[dict]):
        """
        Apply time-axis locators/formatters to `ax` using options set on the plot
        via CreatePlot.set_time_axis(...). No-op if opts is None.
        """
        if not opts:
            return

        major_map = {
            "year": mdates.YearLocator(),
            "quarter": mdates.MonthLocator(bymonth=[1, 4, 7, 10]),
            "month": mdates.MonthLocator(),
            "week": mdates.WeekdayLocator(),  # Monday default
            "day": mdates.DayLocator(),
            "hour": mdates.HourLocator(),
        }
        minor_map = {
            "quarter": mdates.MonthLocator(bymonth=[1, 4, 7, 10]),
            "month": mdates.MonthLocator(),
            "week": mdates.WeekdayLocator(),
            "day": mdates.DayLocator(),
            "hour": mdates.HourLocator(),
            None: None,
        }

        major = major_map.get(opts.get("major", "month"), mdates.MonthLocator())
        minor = minor_map.get(opts.get("minor", "week"))

        ax.xaxis.set_major_locator(major)
        if minor is not None:
            ax.xaxis.set_minor_locator(minor)

        ax.xaxis.set_major_formatter(mdates.DateFormatter(opts.get("fmt", "%b %Y")))
        rotate = int(opts.get("rotate", 30))
        ha = opts.get("ha", "right")

        for lab in ax.get_xticklabels():
            lab.set_rotation(rotate)
            lab.set_ha(ha)

    def _finalize_axis(self, ax, plot_obj):
        """
        Final per-axes adjustments that should happen after features,
        inversion, and shared-label handling.
        """
        self._apply_time_axis(ax, getattr(plot_obj, "time_axis", None))

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
                                f'{" | ".join(feature_dict.keys())}')
