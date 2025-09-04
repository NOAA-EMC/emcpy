import numpy as np
import pytest

from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots.plots import LinePlot


def test_invert_methods_dont_shadow_and_apply_x(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    assert callable(getattr(plot, "invert_xaxis"))

    plot.invert_xaxis()
    assert callable(getattr(plot, "invert_xaxis")), "invert_xaxis() must not be shadowed by a bool"

    fig, ax = single_axes(plot)
    # Use truthiness or cast to bool; avoids numpy.bool_ vs True identity issues
    assert bool(ax.xaxis_inverted())

def test_invert_methods_dont_shadow_and_apply_y(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    assert callable(getattr(plot, "invert_yaxis"))

    plot.invert_yaxis()
    assert callable(getattr(plot, "invert_yaxis")), "invert_yaxis() must not be shadowed by a bool"

    fig, ax = single_axes(plot)
    assert bool(ax.yaxis_inverted())


def test_legacy_bool_attribute_still_work_x(single_axes):
    # Backward compatibility: older code might set plot.invert_xaxis = True
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    # Simulate legacy usage:
    setattr(plot, "invert_xaxis", True)

    fig, ax = single_axes(plot)
    assert ax.xaxis_inverted() is True


def test_legacy_bool_attribute_still_work_y(single_axes):
    plot = CreatePlot(plot_layers=[LinePlot([0, 1], [0, 1])])
    setattr(plot, "invert_yaxis", True)

    fig, ax = single_axes(plot)
    assert ax.yaxis_inverted() is True
