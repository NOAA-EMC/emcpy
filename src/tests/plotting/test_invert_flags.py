import os
from contextlib import nullcontext as does_not_raise
import numpy as np
import pytest

from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots.plots import LinePlot


def _legacy_warn_ctx():
    # Matches the library behavior if you gated the warning on EMCPY_WARN_ON_LEGACY_INVERT
    return (
        pytest.warns(DeprecationWarning)
        if os.environ.get("EMCPY_WARN_ON_LEGACY_INVERT") == "1"
        else does_not_raise()
    )


def test_invert_methods_dont_shadow_and_apply_x(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    assert callable(getattr(plot, "invert_xaxis"))

    plot.invert_xaxis()
    assert callable(getattr(plot, "invert_xaxis"))

    fig, ax = single_axes(plot)
    assert bool(ax.xaxis_inverted())


def test_invert_methods_dont_shadow_and_apply_y(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    assert callable(getattr(plot, "invert_yaxis"))

    plot.invert_yaxis()
    assert callable(getattr(plot, "invert_yaxis"))

    fig, ax = single_axes(plot)
    assert bool(ax.yaxis_inverted())


def test_legacy_bool_attribute_still_work_x(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    setattr(plot, "invert_xaxis", True)

    with _legacy_warn_ctx():
        fig, ax = single_axes(plot)
    assert bool(ax.xaxis_inverted())


def test_legacy_bool_attribute_still_work_y(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    setattr(plot, "invert_yaxis", True)

    with _legacy_warn_ctx():
        fig, ax = single_axes(plot)
    assert bool(ax.yaxis_inverted())
