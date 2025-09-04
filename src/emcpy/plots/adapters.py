# emcpy/plots/adapters.py
from __future__ import annotations
import numpy as np
from typing import Any, ClassVar, Dict, Optional, Protocol, TYPE_CHECKING

if TYPE_CHECKING:
    # Avoids runtime circular imports while keeping type safety
    from .create_plots import CreateFigure, AxState


class LayerAdapter(Protocol):
    """Interface that all layer adapters implement."""
    # Class-level key used to register this adapter
    plottype: ClassVar[str]

    def render(self, fig: "CreateFigure", st: "AxState", layer: Any) -> Optional[Any]:
        """Render a single layer onto the given axes state and return the created artist, if any."""
        ...


# Registry of plottype -> adapter class (not instances)
_ADAPTERS: Dict[str, type[LayerAdapter]] = {}


def register(cls: type[LayerAdapter]):
    """Class decorator to register a LayerAdapter by its `plottype`."""
    pt = getattr(cls, "plottype", None)
    if not isinstance(pt, str) or not pt:
        raise ValueError(f"{cls.__name__} must define a non-empty 'plottype' class attribute.")
    if pt in _ADAPTERS:
        raise ValueError(f"Adapter for plottype '{pt}' already registered: "
                         f"{_ADAPTERS[pt].__name__}")
    _ADAPTERS[pt] = cls
    return cls


def get_adapter(kind: str) -> LayerAdapter:
    """Return a fresh adapter instance for the given plottype."""
    try:
        adapter_cls = _ADAPTERS[kind]
    except KeyError as e:
        raise KeyError(f"Unknown plottype '{kind}'. Registered: {list(_ADAPTERS)}") from e
    return adapter_cls()


def registered_plottypes() -> tuple[str, ...]:
    """
    Return the names of all registered layer plottypes.

    The order matches adapter registration (dict insertion order in Python 3.7+).
    Useful for tests, debugging, or surfacing supported `plottype` values.

    Returns
    -------
    tuple[str, ...]
        Registered plottype names, e.g. ("scatter", "line_plot", ...).
    """
    return tuple(_ADAPTERS.keys())

# ---------------- Adapters (call existing renderers; add validation) ----------------


@register
class ScatterAdapter:
    plottype = "scatter"

    def render(self, fig, st: AxState, layer):
        x = np.asarray(layer.x)
        y = np.asarray(layer.y)
        if x.shape != y.shape:
            raise ValueError(f"Scatter: x and y must have same shape; got {x.shape} vs {y.shape}.")
        return fig._scatter(layer, st.ax)  # must return the PathCollection


@register
class LineAdapter:
    plottype = "line_plot"

    def render(self, fig, st: AxState, layer):
        x = np.asarray(layer.x)
        y = np.asarray(layer.y)
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
        except ImportError as e:
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
        x = np.asarray(layer.x)
        y = np.asarray(layer.y)
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
        return fig._map_scatter(layer, st.ax)


@register
class MapGriddedAdapter:
    plottype = "map_gridded"

    def render(self, fig, st: AxState, layer):
        return fig._map_gridded(layer, st.ax)


@register
class MapContourAdapter:
    plottype = "map_contour"

    def render(self, fig, st: AxState, layer):
        return fig._map_contour(layer, st.ax)


@register
class MapFilledContourAdapter:
    plottype = "map_filled_contour"

    def render(self, fig, st: AxState, layer):
        return fig._map_filled_contour(layer, st.ax)
