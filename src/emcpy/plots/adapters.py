# emcpy/plots/adapters.py
from __future__ import annotations
from dataclasses import dataclass, field
from typing import Any, Dict, Optional, Protocol
import numpy as np

@dataclass
class AxState:
    ax: Any
    mappables: list[Any] = field(default_factory=list)

class LayerAdapter(Protocol):
    plottype: str
    def render(self, fig, st: AxState, layer) -> Optional[Any]: ...

_REGISTRY: Dict[str, LayerAdapter] = {}

def register(cls):
    _REGISTRY[cls.plottype] = cls()
    return cls

def get_adapter(kind: str) -> LayerAdapter:
    try:
        return _REGISTRY[kind]
    except KeyError as e:
        raise KeyError(f"Unknown plottype '{kind}'. Registered: {list(_REGISTRY)}") from e

# ---------------- Adapters (call existing renderers; add validation) ----------------

@register
class ScatterAdapter:
    plottype = "scatter"
    def render(self, fig, st: AxState, layer):
        x = np.asarray(layer.x); y = np.asarray(layer.y)
        if x.shape != y.shape:
            raise ValueError(f"Scatter: x and y must have same shape; got {x.shape} vs {y.shape}.")
        return fig._scatter(layer, st.ax)  # must return the PathCollection

@register
class LineAdapter:
    plottype = "line_plot"
    def render(self, fig, st: AxState, layer):
        x = np.asarray(layer.x); y = np.asarray(layer.y)
        if x.shape != y.shape:
            raise ValueError(f"LinePlot: x and y must have same shape; got {x.shape} vs {y.shape}.")
        return fig._lineplot(layer, st.ax)

@register
class HistogramAdapter:
    plottype = "histogram"
    def render(self, fig, st: AxState, layer):
        return fig._histogram(layer, st.ax)

@register
class DensityAdapter:
    plottype = "density"
    def render(self, fig, st: AxState, layer):
        try:
            import seaborn as _  # noqa
        except Exception as e:
            raise RuntimeError("Density layer requires 'seaborn' to be installed.") from e
        return fig._density(layer, st.ax)

@register
class GriddedAdapter:
    plottype = "gridded_plot"

    def render(self, fig, st: AxState, layer):
        # Pull arrays
        x = np.asanyarray(layer.x)
        y = np.asanyarray(layer.y)
        z = np.asanyarray(layer.z)

        # Collect kwargs the same way the legacy renderer did
        inputs = fig._get_inputs_dict(['plottype', 'plot_ax', 'x', 'y', 'z', 'colorbar'], layer)
        # Ensure shading is 'auto' unless explicitly overridden
        inputs.setdefault('shading', 'auto')

        # 1-D coords: accept centers or edges
        if x.ndim == 1 and y.ndim == 1:
            nx, ny = len(x), len(y)
            zy, zx = z.shape
            if (zy, zx) not in ((ny, nx), (ny - 1, nx - 1)):
                raise ValueError(
                    "GriddedPlot: incompatible shapes: "
                    f"x(len)={nx}, y(len)={ny}, z.shape={z.shape}. "
                    "Expected (ny, nx) for center coords or (ny-1, nx-1) for edge coords."
                )
            qm = st.ax.pcolormesh(x, y, z, **inputs)
            return qm  # QuadMesh

        # 2-D meshgrid coords: accept same-shape or edge-shape
        if x.ndim == 2 and y.ndim == 2:
            if x.shape != y.shape:
                raise ValueError(f"GriddedPlot: X and Y must share shape; got {x.shape} vs {y.shape}.")
            if z.shape == x.shape or z.shape == (x.shape[0] - 1, x.shape[1] - 1):
                qm = st.ax.pcolormesh(x, y, z, **inputs)
                return qm  # QuadMesh
            raise ValueError(
                "GriddedPlot (meshgrid): incompatible shapes: "
                f"X/Y shape={x.shape}, Z shape={z.shape}. "
                "Expected Z to match X/Y or be one smaller in each dimension (edges)."
            )

        raise ValueError(
            f"GriddedPlot: unsupported coordinate dims: x.ndim={x.ndim}, y.ndim={y.ndim}. "
            "Use 1-D (monotonic) or 2-D meshgrid coordinates."
        )

@register
class ContourAdapter:
    plottype = "contour"
    def render(self, fig, st: AxState, layer):
        z = np.asarray(layer.z)
        if z.ndim != 2:
            raise ValueError(f"ContourPlot: z must be 2D; got {z.ndim}D.")
        return fig._contour(layer, st.ax)  # return ContourSet

@register
class FilledContourAdapter:
    plottype = "contourf"
    def render(self, fig, st: AxState, layer):
        z = np.asarray(layer.z)
        if z.ndim != 2:
            raise ValueError(f"FilledContourPlot: z must be 2D; got {z.ndim}D.")
        return fig._contourf(layer, st.ax)  # return ContourSet

@register
class VerticalLineAdapter:
    plottype = "vertical_line"
    def render(self, fig, st, layer):
        # numeric sanity
        try:
            float(layer.x)
        except Exception as e:
            raise ValueError(f"VerticalLine: x must be numeric; got {layer.x!r}.") from e
        return fig._verticalline(layer, st.ax)  # likely returns Line2D (or None in current impl)

@register
class HorizontalLineAdapter:
    plottype = "horizontal_line"
    def render(self, fig, st, layer):
        try:
            float(layer.y)
        except Exception as e:
            raise ValueError(f"HorizontalLine: y must be numeric; got {layer.y!r}.") from e
        return fig._horizontalline(layer, st.ax)

@register
class HorizontalSpanAdapter:
    plottype = "horizontal_span"
    def render(self, fig, st, layer):
        # ensure bounds are finite; allow ymin > ymax (Matplotlib handles both)
        for name, val in (("ymin", layer.ymin), ("ymax", layer.ymax)):
            try:
                float(val)
            except Exception as e:
                raise ValueError(f"HorizontalSpan: {name} must be numeric; got {val!r}.") from e
        return fig._horizontalspan(layer, st.ax)  # PolyCollection (or None)

@register
class BarAdapter:
    plottype = "bar_plot"
    def render(self, fig, st, layer):
        # Basic length check; Matplotlib is flexible with scalars, but we give clearer errors.
        x = np.asarray(layer.x)
        h = np.asarray(layer.height)
        if x.shape != h.shape:
            raise ValueError(f"BarPlot: x and height must have same shape; got {x.shape} vs {h.shape}.")
        return fig._barplot(layer, st.ax)  # BarContainer

@register
class HorizontalBarAdapter:
    plottype = "horizontal_bar"
    def render(self, fig, st, layer):
        y = np.asarray(layer.y)
        w = np.asarray(layer.width)
        if y.shape != w.shape:
            raise ValueError(f"HorizontalBar: y and width must have same shape; got {y.shape} vs {w.shape}.")
        return fig._hbar(layer, st.ax)  # BarContainer

@register
class SkewTAdapter:
    plottype = "skewt"
    def render(self, fig, st, layer):
        x = np.asarray(layer.x); y = np.asarray(layer.y)
        if x.shape != y.shape:
            raise ValueError(f"SkewT: x and y must have same shape; got {x.shape} vs {y.shape}.")
        # Axis is already created with projection='skewx' in CreateFigure; just draw.
        return fig._skewt(layer, st.ax)  # returns list[Line2D] or None in current impl

@register
class BoxWhiskerAdapter:
    plottype = "boxandwhisker"
    def render(self, fig, st: AxState, layer):
        if getattr(layer, "tick_labels", None) is not None:
            n = len(layer.data) if hasattr(layer.data, "__len__") else None
            if n is not None and len(layer.tick_labels) != n:
                raise ValueError(f"BoxandWhiskerPlot: tick_labels length {len(layer.tick_labels)} "
                                 f"must match number of boxes {n}.")
        return fig._boxandwhisker(layer, st.ax)

# Map variants
@register
class MapScatterAdapter:
    plottype = "map_scatter"

    def render(self, fig, st: AxState, layer):
        # Pull arrays
        lon = np.asanyarray(layer.longitude)
        lat = np.asanyarray(layer.latitude)
        data = getattr(layer, "data", None)

        # Collect kwargs like legacy renderer (leave out core data fields)
        if data is None:
            skip = ['plottype', 'longitude', 'latitude', 'markersize', 'integer_field', 'colorbar']
        else:
            skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar', 'normalize', 'integer_field']
        inputs = fig._get_inputs_dict(skip, layer)

        # Choose the CRS that represents the coordinate system of (lon, lat)
        transform = getattr(getattr(fig, "projection", None), "transform", ccrs.PlateCarree())

        # Plain 2D scatter (no color mapping)
        if data is None:
            pc = st.ax.scatter(lon, lat, s=layer.markersize, transform=transform, **inputs)
            return pc  # PathCollection

        # Colored scatter
        integer_field = bool(getattr(layer, "integer_field", False))
        norm = None
        if integer_field:
            # Require vmin/vmax to build integer bin boundaries
            cmap_name = inputs.get('cmap', None) or matplotlib.rcParams.get('image.cmap', 'viridis')
            cmap = matplotlib.cm.get_cmap(cmap_name)
            vmin = inputs.get('vmin', None)
            vmax = inputs.get('vmax', None)
            if vmin is None or vmax is None:
                raise ValueError("MapScatter with integer_field=True requires both vmin and vmax.")
            norm = BoundaryNorm(np.arange(vmin - 0.5, vmax, 1), cmap.N)

        pc = st.ax.scatter(lon, lat, c=data, s=layer.markersize, norm=norm, transform=transform, **inputs)

        return pc  # PathCollection

@register
class MapGriddedAdapter:
    plottype = "map_gridded"

    def render(self, fig, st: AxState, layer):
        # Pull arrays in the map naming convention
        X = np.asanyarray(layer.longitude)
        Y = np.asanyarray(layer.latitude)
        Z = np.asanyarray(layer.data)

        # Mirror legacy kwargs behavior, but default shading='auto'
        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar']
        inputs = fig._get_inputs_dict(skip, layer)
        inputs.setdefault('shading', 'auto')

        # Prefer the projection used when the Axes was created
        transform = getattr(getattr(fig, "projection", None), "transform", ccrs.PlateCarree())

        # --- 3D tiled case: (..., tiles) on the last axis
        if X.ndim == 3 and Y.ndim == 3 and Z.ndim == 3:
            if X.shape[:2] != Y.shape[:2] or X.shape != Z.shape:
                raise ValueError(
                    f"MapGridded (tiles): X,Y,Z shapes must match; got {X.shape}, {Y.shape}, {Z.shape}."
                )
            qm = None
            tiles = X.shape[-1]
            for i in range(tiles):
                qm = st.ax.pcolormesh(X[:, :, i], Y[:, :, i], Z[:, :, i],
                                      transform=transform, **inputs)
            return qm  # QuadMesh from the last tile

        # --- 2D meshgrid case
        if X.ndim == 2 and Y.ndim == 2:
            if X.shape != Y.shape:
                raise ValueError(f"MapGridded: X and Y must share shape; got {X.shape} vs {Y.shape}.")
            if Z.shape == X.shape or Z.shape == (X.shape[0] - 1, X.shape[1] - 1):
                return st.ax.pcolormesh(X, Y, Z, transform=transform, **inputs)
            raise ValueError(
                "MapGridded (meshgrid): incompatible shapes: "
                f"X/Y={X.shape}, Z={Z.shape}. "
                "Expected Z to match X/Y or be one smaller in each dimension (edges)."
            )

        # --- 1D coordinate vectors (allowed; pcolormesh will grid them)
        if X.ndim == 1 and Y.ndim == 1 and Z.ndim == 2:
            nx, ny = len(X), len(Y)
            zy, zx = Z.shape
            if (zy, zx) in ((ny, nx), (ny - 1, nx - 1)):
                return st.ax.pcolormesh(X, Y, Z, transform=transform, **inputs)
            raise ValueError(
                "MapGridded (1D coords): incompatible shapes: "
                f"x(len)={nx}, y(len)={ny}, Z={Z.shape}. "
                "Expected (ny, nx) for centers or (ny-1, nx-1) for edges."
            )

        raise ValueError(
            f"MapGridded: unsupported coordinate dims "
            f"(lon.ndim={X.ndim}, lat.ndim={Y.ndim}, data.ndim={Z.ndim})."
        )

@register
class MapContourAdapter:
    plottype = "map_contour"

    def render(self, fig, st: AxState, layer):
        # Arrays: longitude (X), latitude (Y), data (Z)
        X = np.asanyarray(layer.longitude)
        Y = np.asanyarray(layer.latitude)
        Z = np.asanyarray(layer.data)

        skip = ['plottype', 'longitude', 'latitude', 'data', 'markersize', 'colorbar']
        inputs = fig._get_inputs_dict(skip, layer)

        transform = getattr(getattr(fig, "projection", None), "transform", ccrs.PlateCarree())

        cs = st.ax.contour(X, Y, Z, transform=transform, **inputs)  # ContourSet

        # Optional inline labels
        if getattr(layer, 'clabel', False):
            # Use provided levels if present; contour already computed levels otherwise
            plt.clabel(cs, levels=getattr(layer, 'levels', None), use_clabeltext=True)

        return cs  # ContourSet

@register
class MapFilledContourAdapter:
    plottype = "map_filled_contour"
    def render(self, fig, st: AxState, layer):
        return fig._map_filled_contour(layer, st.ax)
