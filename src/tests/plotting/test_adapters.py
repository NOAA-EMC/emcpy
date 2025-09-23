# src/tests/plotting/test_adapters.py
import sys
import types
import numpy as np
import pytest

from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.plots import LinePlot
from emcpy.plots.adapters import get_adapter, register, _ADAPTERS, registered_plottypes


def test_unknown_plottype_raises_keyerror():
    with pytest.raises(KeyError, match="Unknown plottype"):
        get_adapter("definitely_not_real")


def test_registry_duplicate_plottype_rejected(monkeypatch):
    # Make a temporary dummy adapter with a unique plottype.
    @register
    class _TmpAdapter:
        plottype = "_tmp_kind"

        def render(self, fig, st, layer):
            return None

    # Attempt to register again should error.
    with pytest.raises(ValueError, match="already registered"):
        @register
        class _TmpAdapter2:
            plottype = "_tmp_kind"

            def render(self, fig, st, layer):
                return None

    # Cleanup (not strictly required, but keeps registry pristine if tests reorder)
    _ADAPTERS.pop("_tmp_kind", None)


def test_adapter_render_path_smoke(single_axes):
    # Any built-in layer should resolve to a registered adapter and render.
    lp = LinePlot([0, 1, 2], [0, 1, 4])
    plot = CreatePlot(plot_layers=[lp])
    fig, ax = single_axes(plot)
    # Line plots don't produce "mappables" (colorbar sources), so last mappable is None.
    assert fig._last_mappable_for_ax(ax) is None


def test_registry_registered_plottypes_exposes_known():
    pts = registered_plottypes()
    assert isinstance(pts, tuple)
    # A couple of canonical entries
    assert "scatter" in pts
    assert "line_plot" in pts
    # Unknown key yields helpful error
    with pytest.raises(KeyError, match="Unknown plottype"):
        get_adapter("definitely_not_a_real_plottype")


def test_density_adapter_raises_clear_message_when_seaborn_missing(monkeypatch, single_axes):
    # Pretend seaborn is missing
    monkeypatch.setitem(sys.modules, "seaborn", None)

    adapter = get_adapter("density")

    class _DummyLayer:
        plottype = "density"

        def __init__(self):
            self.data = np.random.randn(100)
            self.color = "tab:blue"
            self.fill = False

    # Build a valid fig/axes to satisfy adapter.render signature
    # (we don't draw anything; we just want the import check to run)
    from emcpy.plots.create_plots import CreatePlot
    from emcpy.plots.plots import LinePlot
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    fig, ax = single_axes(plot)
    st = types.SimpleNamespace(ax=ax)

    with pytest.raises(RuntimeError, match="requires 'seaborn'"):
        adapter.render(fig, st, _DummyLayer())
