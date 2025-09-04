# src/tests/plotting/test_adapters.py
import pytest

from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.plots import LinePlot
from emcpy.plots.adapters import get_adapter, register, _ADAPTERS


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
