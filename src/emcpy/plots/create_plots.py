# This work developed by NOAA/NWS/EMC under the Apache 2.0 license.
from __future__ import annotations
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
from typing import Any, List, Optional, Mapping, MutableMapping
from emcpy.plots.adapters import get_adapter
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.skewt_projection import SkewXAxes
from emcpy.plots._norms import compute_norm
from emcpy.plots._validate import require_1d, require_2d, require_same_length, require_same_shape2d
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

    def add_stats_dict(
        self,
        stats_dict: Optional[Mapping[str, Any]] = None,
        xloc: float = 0.5,
        yloc: float = -0.1,
        ha: str = "center",
        **kwargs: Any
    ) -> None:

        stats: MutableMapping[str, Any] = dict(stats_dict) if stats_dict is not None else {}
        kw: dict[str, Any] = dict(kwargs) if kwargs else {}

        self.stats = {
            "stats": stats,
            "xloc": float(xloc),
            "yloc": float(yloc),
            "ha": ha,
            "kwargs": kw,
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

                cenlon = getattr(plot_obj, "cenlon", None)
                cenlat = getattr(plot_obj, "cenlat", None)
                # fall back to domain defaults if not set on the plot
                if cenlon is None:
                    cenlon = getattr(self.domain, "cenlon", None)
                if cenlat is None:
                    cenlat = getattr(self.domain, "cenlat", None)
                self.projection = MapProjection(plot_obj.projection, cenlon=cenlon, cenlat=cenlat)
                ax = self.fig.add_subplot(gs[i], projection=self.projection.projection)

                # fixed
                if str(self.projection) not in ['npstere', 'spstere']:
                    ax.set_extent(self.domain.extent, crs=ccrs.PlateCarree())
                    if str(self.projection) not in ['lambert']:
                        ax.set_xticks(self.domain.xticks, crs=ccrs.PlateCarree())
                        ax.set_yticks(self.domain.yticks, crs=ccrs.PlateCarree())
                        lon_formatter = LongitudeFormatter(zero_direction_label=False)
                        lat_formatter = LatitudeFormatter()
                        ax.xaxis.set_major_formatter(lon_formatter)
                        ax.yaxis.set_major_formatter(lat_formatter)
                else:
                    ax.set_extent(self.domain.extent, crs=ccrs.PlateCarree())
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
        Always treat map-layer inputs as geographic lon/lat.
        """
        return ccrs.PlateCarree()

    def _map_scatter(self, plotobj, ax):
        """
        Render MapScatter layer.
        - If `plotobj.data` is None: solid-color points (no colormap).
        - If numeric: apply shared normalization policy (BoundaryNorm for integer_field).
        """
        xform = self._map_transform()

        # Unlabeled points (no scalar mapping/colorbar)
        if plotobj.data is None:
            skip = ['plottype', 'longitude', 'latitude', 'markersize', 'integer_field', 'colorbar']
            inputs = self._get_inputs_dict(skip, plotobj)

            lon = require_1d("longitude", plotobj.longitude)
            lat = require_1d("latitude", plotobj.latitude)
            require_same_length("longitude", lon, "latitude", lat)

            ms = getattr(plotobj, "markersize", None)
            if ms is not None and hasattr(ms, "__len__"):
                require_same_length("markersize", ms, "longitude", lon)

            for k in ('c', 'color', 'facecolor', 'facecolors'):
                inputs.pop(k, None)

            return ax.scatter(lon, lat, s=plotobj.markersize, transform=xform, **inputs)

        # Scalar-mapped points
        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar', 'normalize', 'integer_field']
        inputs = self._get_inputs_dict(skip, plotobj)

        lon = require_1d("longitude", plotobj.longitude)
        lat = require_1d("latitude", plotobj.latitude)
        require_same_length("longitude", lon, "latitude", lat)

        if hasattr(plotobj.data, "__len__"):
            require_same_length("data", plotobj.data, "longitude", lon)

        for k in ('c', 'color', 'facecolor', 'facecolors'):
            inputs.pop(k, None)

        # Apply norm only if data are numeric
        try:
            arr = np.asarray(plotobj.data)
            is_numeric = arr.ndim > 0 and arr.dtype.kind in {'i', 'u', 'f'}
        except Exception:
            is_numeric = False
        if is_numeric:
            self._apply_norm_from_layer(inputs, plotobj)

        cs = ax.scatter(lon, lat, c=plotobj.data, s=plotobj.markersize, transform=xform, **inputs)

        return cs  # PathCollection (ScalarMappable)

    def _map_gridded(self, plotobj, ax):
        """
        Plot gridded data on a map with consistent normalization.
        Accepts:
          - 1D lon/lat (centers or edges)
          - 2D lon/lat same shape as Z (centers)
          - 2D lon/lat with shape (Z.shape[0]+1, Z.shape[1]+1) (edges)
        Returns the mappable from pcolormesh.
        """
        skip = [
            "plottype", "longitude", "latitude", "data",
            "markersize", "colorbar", "integer_field", "normalize",
        ]
        inputs: dict[str, Any] = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()

        # Validate data
        Z = require_2d("data", plotobj.data)
        nrows, ncols = Z.shape

        # Coords can be 1D or 2D
        lon = np.asarray(plotobj.longitude)
        lat = np.asarray(plotobj.latitude)

        # Decide allowed shapes and set shading appropriately
        if lon.ndim == 2 or lat.ndim == 2:
            if not (lon.ndim == 2 and lat.ndim == 2):
                raise ValueError("MapGridded: when using 2D coordinates, both longitude and latitude must be 2D.")
            # 2D centers: same shape as Z
            if lon.shape == (nrows, ncols) and lat.shape == (nrows, ncols):
                # centers; let 'auto' decide or keep user-provided shading
                inputs.setdefault("shading", "auto")
                X, Y = lon, lat
            # 2D edges: one larger in both dims
            elif lon.shape == (nrows + 1, ncols + 1) and lat.shape == (nrows + 1, ncols + 1):
                # edges require flat shading to avoid seams
                inputs.setdefault("shading", "flat")
                X, Y = lon, lat
            else:
                raise ValueError(
                    "MapGridded: 2D longitude/latitude must either match Z.shape "
                    f"({nrows}, {ncols}) or be edges with shape ({nrows+1}, {ncols+1}); "
                    f"got lon {lon.shape}, lat {lat.shape}, Z {Z.shape}."
                )
        else:
            # 1D centers or edges are fine: lengths can be N or N+1
            lon = require_1d("longitude", lon)
            lat = require_1d("latitude", lat)
            nx_ok = len(lon) in {ncols, ncols + 1}
            ny_ok = len(lat) in {nrows, nrows + 1}
            if not (nx_ok and ny_ok):
                raise ValueError(
                    "MapGridded: for 1D longitude/latitude, expected len(lon) in "
                    f"{{{ncols}, {ncols+1}}} and len(lat) in {{{nrows}, {nrows+1}}}; "
                    f"got len(lon)={len(lon)}, len(lat)={len(lat)}, Z.shape={Z.shape}."
                )
            # Let MPL infer; but encourage seam-free for edges
            if len(lon) == ncols + 1 and len(lat) == nrows + 1:
                inputs.setdefault("shading", "flat")
            else:
                inputs.setdefault("shading", "auto")
            X, Y = lon, lat

        # Normalize consistently (also infers bounds from data for integer_field)
        self._apply_norm_from_layer(inputs, plotobj)

        Zm = np.ma.masked_invalid(np.asarray(Z))
        return ax.pcolormesh(X, Y, Zm, transform=xform, **inputs)

    def _map_contour(self, plotobj, ax):
        """
        Render MapContour layer.
        """
        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar', 'clabel']
        inputs = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()

        Z = require_2d("data", plotobj.data)
        lon = np.asarray(plotobj.longitude)
        lat = np.asarray(plotobj.latitude)
        if lon.ndim == 2 or lat.ndim == 2:
            require_same_shape2d("longitude", lon, "data", Z)
            require_same_shape2d("latitude", lat, "data", Z)
        else:
            lon = require_1d("longitude", lon)
            lat = require_1d("latitude", lat)

        self._apply_norm_from_layer(inputs, plotobj, keep_levels=True)

        cs = ax.contour(lon, lat, np.asarray(Z), transform=xform, **inputs)
        if getattr(plotobj, 'clabel', False):
            plt.clabel(cs, levels=getattr(plotobj, 'levels', None), use_clabeltext=True)

        return cs

    def _map_filled_contour(self, plotobj, ax):
        """
        Render MapFilledContour layer.
        """
        skip = ['plottype', 'longitude', 'latitude', 'data', 'colorbar', 'clabel']
        inputs = self._get_inputs_dict(skip, plotobj)
        xform = self._map_transform()

        Z = require_2d("data", plotobj.data)
        lon = np.asarray(plotobj.longitude)
        lat = np.asarray(plotobj.latitude)
        if lon.ndim == 2 or lat.ndim == 2:
            require_same_shape2d("longitude", lon, "data", Z)
            require_same_shape2d("latitude", lat, "data", Z)
        else:
            lon = require_1d("longitude", lon)
            lat = require_1d("latitude", lat)

        self._apply_norm_from_layer(inputs, plotobj, keep_levels=True)

        cs = ax.contourf(lon, lat, np.asarray(Z), transform=xform, **inputs)
        if getattr(plotobj, 'clabel', False):
            plt.clabel(cs, levels=getattr(plotobj, 'levels', None), use_clabeltext=True)

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

    def _is_numeric_arraylike(self, x: Any) -> bool:
        try:
            a = np.asarray(x)
            return a.ndim > 0 and a.dtype.kind in {"i", "u", "f"}  # int/uint/float
        except Exception:
            return False

    def _scatter(self, plotobj, ax: Axes) -> PathCollection:
        """
        Uses Scatter object to plot on axis.
        Returns the PathCollection (mappable when `c` is provided).
        """
        if hasattr(plotobj, "density"):
            return self._density_scatter(plotobj, ax)

        skipvars = ["plottype", "plot_ax", "x", "y", "markersize", "do_linear_regression",
                    "linear_regression", "density", "channel"]
        inputs: dict[str, Any] = self._get_inputs_dict(skipvars, plotobj)

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        ms = getattr(plotobj, "markersize", None)
        if ms is not None and hasattr(ms, "__len__"):
            require_same_length("markersize", ms, "x", x)

        c_val = getattr(plotobj, "c", None)
        if c_val is not None and hasattr(c_val, "__len__"):
            require_same_length("c", c_val, "x", x)

        if self._is_numeric_arraylike(c_val):
            self._apply_norm_from_layer(inputs, plotobj)
            inputs.pop("c", None)
            inputs.pop("color", None)
            inputs.pop("facecolor", None)
            inputs.pop("facecolors", None)
            cs = ax.scatter(x, y, s=plotobj.markersize, c=c_val, **inputs)
        else:
            inputs.pop("c", None)
            cs = ax.scatter(x, y, s=plotobj.markersize, **inputs)

        if getattr(plotobj, "do_linear_regression", False) and len(x) and len(y):
            y_pred, r_sq, intercept, slope = get_linear_regression(x, y)
            label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
            style = dict(getattr(plotobj, "linear_regression", {}) or {})
            if "color" not in style and hasattr(plotobj, "color"):
                style["color"] = plotobj.color
            ax.plot(x, y_pred, label=label, **style)

        return cs

    def _gridded(self, plotobj, ax):
        """
        Uses Gridded object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)
        inputs.setdefault("shading", "auto")

        Z = require_2d("z", plotobj.z)
        x_arr = np.asarray(plotobj.x)
        y_arr = np.asarray(plotobj.y)

        if x_arr.ndim == 2 or y_arr.ndim == 2:
            if not (x_arr.ndim == 2 and y_arr.ndim == 2):
                raise ValueError("Gridded: when using 2D coordinates, both x and y must be 2D.")
            require_same_shape2d("x", x_arr, "z", Z)
            require_same_shape2d("y", y_arr, "z", Z)
            X, Y = x_arr, y_arr
        else:
            # Accept centers (N, M) or edges (N+1, M+1)
            x1 = require_1d("x", x_arr)
            y1 = require_1d("y", y_arr)
            nrows, ncols = Z.shape
            nx_ok = len(x1) in {ncols, ncols + 1}
            ny_ok = len(y1) in {nrows, nrows + 1}
            if not (nx_ok and ny_ok):
                raise ValueError(
                    "Gridded: for 1D x/y, expected len(x) in {Z.shape[1], Z.shape[1]+1} and "
                    "len(y) in {Z.shape[0], Z.shape[0]+1}; "
                    f"got len(x)={len(x1)}, len(y)={len(y1)}, Z.shape={Z.shape}."
                )
            X, Y = x1, y1

        self._apply_norm_from_layer(inputs, plotobj)  # continuous or integer_field
        Zm = np.ma.masked_invalid(np.asarray(Z))
        qm = ax.pcolormesh(X, Y, Zm, **inputs)

        return qm  # QuadMesh

    def _contour(self, plotobj, ax):
        """
        Render Contour layer.
        """
        skip = ['plottype', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)

        Z = require_2d("z", plotobj.z)
        x_arr = np.asarray(plotobj.x)
        y_arr = np.asarray(plotobj.y)

        if x_arr.ndim == 1 and y_arr.ndim == 1:
            nrows, ncols = Z.shape
            if len(x_arr) != ncols or len(y_arr) != nrows:
                raise ValueError(
                    "Contour: for 1D x/y, expected len(x)==Z.shape[1] and len(y)==Z.shape[0]; "
                    f"got len(x)={len(x_arr)}, len(y)={len(y_arr)}, Z.shape={Z.shape}."
                )
            X, Y = x_arr, y_arr
        elif x_arr.ndim == 2 and y_arr.ndim == 2:
            require_same_shape2d("x", x_arr, "z", Z)
            require_same_shape2d("y", y_arr, "z", Z)
            X, Y = x_arr, y_arr
        else:
            raise ValueError("Contour: x and y must both be 1D or both be 2D to match Z.")

        self._apply_norm_from_layer(inputs, plotobj, keep_levels=True)
        cs = ax.contour(X, Y, np.asarray(Z), **inputs)

        return cs  # ContourSet

    def _contourf(self, plotobj, ax):
        """
        Render FilledContourPlot layer.
        """
        skip = ['plottype', 'x', 'y', 'z', 'colorbar']
        inputs = self._get_inputs_dict(skip, plotobj)

        Z = require_2d("z", plotobj.z)
        x_arr = np.asarray(plotobj.x)
        y_arr = np.asarray(plotobj.y)

        if x_arr.ndim == 1 and y_arr.ndim == 1:
            nrows, ncols = Z.shape
            if len(x_arr) != ncols or len(y_arr) != nrows:
                raise ValueError(
                    "FilledContour: for 1D x/y, expected len(x)==Z.shape[1] and len(y)==Z.shape[0]; "
                    f"got len(x)={len(x_arr)}, len(y)={len(y_arr)}, Z.shape={Z.shape}."
                )
            X, Y = x_arr, y_arr
        elif x_arr.ndim == 2 and y_arr.ndim == 2:
            require_same_shape2d("x", x_arr, "z", Z)
            require_same_shape2d("y", y_arr, "z", Z)
            X, Y = x_arr, y_arr
        else:
            raise ValueError("FilledContour: x and y must both be 1D or both be 2D to match Z.")

        self._apply_norm_from_layer(inputs, plotobj, keep_levels=True)
        cs = ax.contourf(X, Y, np.asarray(Z), **inputs)

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

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        lines = ax.plot(x, y, **inputs)
        return lines[0] if lines else None  # Line2D (not a ScalarMappable)

    def _skewt(self, plotobj, ax):
        """
        Creates a skewt-logp profile plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'x', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        # Plot data using log scaling Y
        lines = ax.semilogy(x, y, **inputs)

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

        x = require_1d("x", plotobj.x)
        h = require_1d("height", plotobj.height)
        require_same_length("x", x, "height", h)

        # Optional shape checks for array-like kwargs
        yerr = inputs.get("yerr", None)
        if yerr is not None and hasattr(yerr, "__len__"):
            ye = np.asarray(yerr)
            if not (ye.shape == (len(h),) or (ye.ndim == 2 and ye.shape == (2, len(h)))):
                raise ValueError(
                    f"yerr must be length-N or shape (2, N); got shape {ye.shape} for N={len(h)}."
                )

        xerr = inputs.get("xerr", None)
        if xerr is not None and hasattr(xerr, "__len__"):
            xe = np.asarray(xerr)
            if not (xe.shape == (len(h),) or (xe.ndim == 2 and xe.shape == (2, len(h)))):
                raise ValueError(
                    f"xerr must be length-N or shape (2, N); got shape {xe.shape} for N={len(h)}."
                )

        bottom = inputs.get("bottom", None)
        if bottom is not None and hasattr(bottom, "__len__"):
            require_same_length("bottom", bottom, "height", h)

        cont = ax.bar(x, h, **inputs)

        return cont  # BarContainer (not a ScalarMappable)

    def _hbar(self, plotobj, ax):
        """
        Uses HorizontalBar object to plot on axis.
        """
        skip = ['plottype', 'plot_ax', 'y', 'width']
        inputs = self._get_inputs_dict(skip, plotobj)

        y = require_1d("y", plotobj.y)
        w = require_1d("width", plotobj.width)
        require_same_length("y", y, "width", w)

        # Optional shape checks for array-like kwargs
        xerr = inputs.get("xerr", None)
        if xerr is not None and hasattr(xerr, "__len__"):
            xe = np.asarray(xerr)
            if not (xe.shape == (len(w),) or (xe.ndim == 2 and xe.shape == (2, len(w)))):
                raise ValueError(
                    f"xerr must be length-N or shape (2, N); got shape {xe.shape} for N={len(w)}."
                )

        yerr = inputs.get("yerr", None)
        if yerr is not None and hasattr(yerr, "__len__"):
            ye = np.asarray(yerr)
            if not (ye.shape == (len(w),) or (ye.ndim == 2 and ye.shape == (2, len(w)))):
                raise ValueError(
                    f"yerr must be length-N or shape (2, N); got shape {ye.shape} for N={len(w)}."
                )

        left = inputs.get("left", None)
        if left is not None and hasattr(left, "__len__"):
            require_same_length("left", left, "width", w)

        cont = ax.barh(y, w, **inputs)
        return cont  # BarContainer (not a ScalarMappable)

    def _boxandwhisker(self, plotobj, ax):
        """
        Uses BoxandWhiskerPlot object to plot on axis.
        """
        inputs, legend_label = plotobj.to_mpl_kwargs()

        # Normalize kwargs based on what this Matplotlib build supports
        supports_orientation = self._supports_kw(ax.boxplot, "orientation")
        if supports_orientation and "vert" in inputs and "orientation" not in inputs:
            # Upgrade: avoid PendingDeprecationWarning on newer MPL
            inputs["orientation"] = "vertical" if inputs.pop("vert") else "horizontal"
        elif (not supports_orientation) and "orientation" in inputs:
            # Downgrade: MPL < 3.8 expects vert=
            orient = str(inputs.pop("orientation")).lower()
            inputs["vert"] = orient.startswith("v")

        bp = ax.boxplot(plotobj.data, **inputs)

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

        x = require_1d("x", plotobj.x)
        y1 = require_1d("y1", plotobj.y1)
        y2 = require_1d("y2", plotobj.y2)
        require_same_length("x", x, "y1", y1)
        require_same_length("x", x, "y2", y2)

        poly = ax.fill_between(x, y1, y2, **inputs)

        return poly  # PolyCollection (not a ScalarMappable)

    def _errorbar(self, plotobj, ax):
        """
        Render ErrorBar layer.
        """
        skip = ['plottype', 'x', 'y']
        inputs = self._get_inputs_dict(skip, plotobj)

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        # Optional: validate xerr/yerr if they are array-like (not scalars)
        xerr = inputs.get("xerr", None)
        if xerr is not None and hasattr(xerr, "__len__"):
            xe = np.asarray(xerr)
            # Accept shape (N,) or (2, N) for asymmetric errors
            if not (xe.shape == (len(x),) or (xe.ndim == 2 and xe.shape == (2, len(x)))):
                raise ValueError(
                    f"xerr must be length-N or shape (2, N); got shape {xe.shape} for N={len(x)}."
                )

        yerr = inputs.get("yerr", None)
        if yerr is not None and hasattr(yerr, "__len__"):
            ye = np.asarray(yerr)
            if not (ye.shape == (len(y),) or (ye.ndim == 2 and ye.shape == (2, len(y)))):
                raise ValueError(
                    f"yerr must be length-N or shape (2, N); got shape {ye.shape} for N={len(y)}."
                )

        cont = ax.errorbar(x, y, **inputs)
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
        skip = ['plottype', 'x', 'y', 'C', 'colorbar', 'colorbar_label', 'colorbar_location']
        inputs = self._get_inputs_dict(skip, plotobj)

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        C = getattr(plotobj, "C", None)
        if C is not None and hasattr(C, "__len__"):
            require_same_length("C", C, "x", x)
            if inputs.get("bins") == "log" and np.any(np.asarray(C) <= 0):
                raise ValueError("HexBin with bins='log' requires C > 0.")

        self._apply_norm_from_layer(inputs, plotobj)
        hb = ax.hexbin(x, y, C=getattr(plotobj, 'C', None), **inputs)

        return hb  # PolyCollection (ScalarMappable)

    def _hist2d(self, plotobj, ax):
        """
        Render Hist2D layer.
        """
        skip = ['plottype', 'x', 'y', 'colorbar', 'colorbar_label', 'colorbar_location']
        inputs = self._get_inputs_dict(skip, plotobj)

        x = require_1d("x", plotobj.x)
        y = require_1d("y", plotobj.y)
        require_same_length("x", x, "y", y)

        self._apply_norm_from_layer(inputs, plotobj)

        h, xedges, yedges, img = ax.hist2d(x, y, **inputs)
        alpha = getattr(plotobj, "alpha", None)
        if alpha is not None:
            img.set_alpha(alpha)

        return img  # QuadMesh (ScalarMappable)

    def _supports_kw(self, func, name: str) -> bool:
        try:
            return name in inspect.signature(func).parameters
        except Exception:
            return False

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

    def _apply_norm_from_layer(self, inputs: dict[str, Any], layer: Any, *, keep_levels: bool = False) -> None:
        """
        Mutate `inputs` in-place to include a Matplotlib `norm` derived from the layer.

        - Reads: layer.integer_field, layer.vmin, layer.vmax, layer.levels (if present)
        - If integer_field and neither levels nor (vmin & vmax) are provided, infer
          vmin/vmax from numeric data on the layer: c/data/z/C.
        - If a norm is added, removes vmin/vmax from `inputs` to avoid double-specification.
        - For contour/contourf, pass keep_levels=True to preserve 'levels' in `inputs`.
        """
        if "norm" in inputs:
            return  # caller already set a norm explicitly

        integer_field = bool(getattr(layer, "integer_field", False))
        vmin = inputs.get("vmin", getattr(layer, "vmin", None))
        vmax = inputs.get("vmax", getattr(layer, "vmax", None))
        levels = inputs.get("levels", getattr(layer, "levels", None))

        # If integer categories and nothing provided, try to infer from data
        if integer_field and levels is None and (vmin is None or vmax is None):
            # Candidate data arrays in priority order
            candidates = [
                inputs.get("c", None),           # if caller passed through
                getattr(layer, "c", None),       # scatter-style
                getattr(layer, "data", None),    # map_scatter / map_gridded
                getattr(layer, "z", None),       # gridded
                getattr(layer, "C", None),       # hexbin w/ C
            ]
            arr = None
            for cand in candidates:
                if cand is not None:
                    try:
                        arr = np.asarray(cand)
                        break
                    except Exception:
                        arr = None
            if arr is not None:
                with np.errstate(invalid="ignore"):
                    arr = arr[np.isfinite(arr)]
                if arr.size:
                    vmin = float(np.floor(arr.min()))
                    vmax = float(np.ceil(arr.max()))

        # If we inferred an integer range that collapses to a single value,
        # widen it by 1 so we get at least one bin (three boundaries).
        if integer_field and levels is None and (vmin is not None) and (vmax is not None):
            if np.isclose(vmin, vmax):
                vmax = vmin + 1.0

        # Let the centralized policy build the norm (raises if still insufficient)
        norm = compute_norm(
            integer_field=integer_field,
            vmin=vmin,
            vmax=vmax,
            levels=levels,
        )
        if norm is not None:
            inputs["norm"] = norm
            inputs.pop("vmin", None)
            inputs.pop("vmax", None)
            if not keep_levels:
                inputs.pop("levels", None)

    def _apply_integer_colorbar_ticks(self, cbar) -> None:
        """
        If the mappable uses BoundaryNorm with ~unit-spaced boundaries, set
        integer-centered ticks and labels: bins [k, k+1) → tick at k+0.5 labeled 'k'.
        No-op for non-BoundaryNorm or non-uniform boundaries.
        """
        m = cbar.mappable
        norm = getattr(m, "norm", None)
        try:
            from matplotlib.colors import BoundaryNorm
            import numpy as _np
        except Exception:
            return

        if not isinstance(norm, BoundaryNorm):
            return

        boundaries = _np.asarray(norm.boundaries, dtype=float)
        if boundaries.ndim != 1 or boundaries.size < 2:
            return

        # Only do the nice integer look when bins are ~1 apart
        diffs = _np.diff(boundaries)
        if not _np.allclose(diffs, diffs[0]) or not _np.isclose(diffs[0], 1.0):
            return

        centers = 0.5 * (boundaries[:-1] + boundaries[1:])
        labels = [str(int(round(b))) for b in boundaries[:-1]]

        # Works for both orientations
        cbar.set_ticks(centers)
        cbar.set_ticklabels(labels)

    def _auto_extend_for_colorbar(self, cbar) -> None:
        """
        Infer extend={'neither','min','max','both'} from mappable vs. norm boundaries.
        """
        try:
            from matplotlib.colors import BoundaryNorm
            import numpy as _np
        except Exception:
            return

        m = cbar.mappable
        arr = m.get_array()
        if arr is None:
            return
        arr = _np.asarray(arr)
        arr = arr[_np.isfinite(arr)]
        if arr.size == 0:
            return

        extend = "neither"
        n = getattr(m, "norm", None)

        # Continuous: compare vs. Normalize limits if present
        vmin = getattr(n, "vmin", None)
        vmax = getattr(n, "vmax", None)
        if vmin is not None and vmax is not None:
            if arr.min() < vmin and arr.max() > vmax:
                extend = "both"
            elif arr.min() < vmin:
                extend = "min"
            elif arr.max() > vmax:
                extend = "max"

        # BoundaryNorm: compare vs. first/last boundary
        from matplotlib.colors import BoundaryNorm
        if isinstance(n, BoundaryNorm):
            lo, hi = float(n.boundaries[0]), float(n.boundaries[-1])
            if arr.min() < lo and arr.max() > hi:
                extend = "both"
            elif arr.min() < lo:
                extend = "min"
            elif arr.max() > hi:
                extend = "max"

        try:
            cbar.set_extend(extend)
        except Exception:
            pass

    def _plot_colorbar(self, ax, colorbar):
        """
        Add colorbar on specified ax or for total figure (single_cbar).
        Uses the most recently-added mappable on this axes.
        """
        mappable = self._last_mappable_for_ax(ax)
        if mappable is None:
            return

        # Single shared colorbar on the designated subplot only
        if colorbar['single_cbar']:
            if self._is_last_subplot(ax):
                cbar_ax = self.fig.add_axes(colorbar['cbar_loc'])
                cb = self.fig.colorbar(mappable, cax=cbar_ax, **colorbar['kwargs'])
                # Integer-friendly ticks if applicable
                self._apply_integer_colorbar_ticks(cb)
                self._auto_extend_for_colorbar(cb)
                if colorbar['label'] is not None:
                    cb.set_label(colorbar['label'], fontsize=colorbar['fontsize'])
            return

        # Per-axes colorbar
        cb = self.fig.colorbar(mappable, ax=ax, **colorbar['kwargs'])
        self._apply_integer_colorbar_ticks(cb)
        self._auto_extend_for_colorbar(cb)
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
