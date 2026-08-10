import numpy as np
import pytest
from matplotlib.colors import TwoSlopeNorm

from emcpy.plots.plots import HeatMap
from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots._norms import compute_norm


def _heatmap_data():
    x = ["08/09 00Z", "08/09 06Z", "08/09 12Z", "08/09 18Z"]
    y = ["TEMP", "UWND", "VWND"]
    data = np.array([
        [0.12, -0.34, 0.05, np.nan],
        [-1.2, -0.9, -1.1, -1.0],
        [0.8, 0.75, np.nan, 0.6],
    ])
    return x, y, data


def test_heatmap_basic_renders(single_axes):
    x, y, data = _heatmap_data()
    plot = CreatePlot(plot_layers=[HeatMap(x, y, data)])
    fig, ax = single_axes(plot)
    assert fig._last_mappable_for_ax(ax) is not None
    assert [t.get_text() for t in ax.get_xticklabels()] == x
    assert [t.get_text() for t in ax.get_yticklabels()] == y


def test_heatmap_masks_nan_and_skips_annotation(single_axes):
    x, y, data = _heatmap_data()
    plot = CreatePlot(plot_layers=[HeatMap(x, y, data)])
    fig, ax = single_axes(plot)
    n_finite = np.isfinite(data).sum()
    assert len(ax.texts) == n_finite


def test_heatmap_annotate_false_adds_no_text(single_axes):
    x, y, data = _heatmap_data()
    layer = HeatMap(x, y, data)
    layer.annotate = False
    plot = CreatePlot(plot_layers=[layer])
    _, ax = single_axes(plot)
    assert len(ax.texts) == 0


def test_heatmap_center_uses_diverging_norm(single_axes):
    x, y, data = _heatmap_data()
    layer = HeatMap(x, y, data)
    layer.center = 0.0
    plot = CreatePlot(plot_layers=[layer])
    fig, ax = single_axes(plot)
    qm = fig._last_mappable_for_ax(ax)
    assert isinstance(qm.norm, TwoSlopeNorm)
    assert qm.norm.vcenter == 0.0


def test_heatmap_center_ignored_when_data_all_one_side(single_axes):
    # All-positive data with center=0.0 shouldn't raise; bound gets nudged.
    x, y = ["a", "b"], ["r1"]
    data = np.array([[1.0, 2.0]])
    layer = HeatMap(x, y, data)
    layer.center = 0.0
    plot = CreatePlot(plot_layers=[layer])
    fig, ax = single_axes(plot)
    qm = fig._last_mappable_for_ax(ax)
    assert isinstance(qm.norm, TwoSlopeNorm)
    assert qm.norm.vmin < 0.0 < qm.norm.vmax


def test_heatmap_shape_mismatch_raises(single_axes):
    x, y = ["a", "b", "c"], ["r1", "r2"]
    data = np.zeros((3, 3))  # wrong: should be (2, 3)
    plot = CreatePlot(plot_layers=[HeatMap(x, y, data)])
    with pytest.raises(ValueError, match="data.shape must be"):
        single_axes(plot)


def test_heatmap_center_with_integer_field_raises(single_axes):
    x, y = ["a", "b"], ["r1"]
    layer = HeatMap(x, y, np.array([[1.0, 2.0]]))
    layer.center = 0.0
    layer.integer_field = True
    plot = CreatePlot(plot_layers=[layer])
    with pytest.raises(ValueError, match="not meaningful"):
        single_axes(plot)


def test_compute_norm_center_basic():
    norm = compute_norm(integer_field=False, vmin=-2.0, vmax=3.0, center=0.0)
    assert isinstance(norm, TwoSlopeNorm)
    assert norm.vmin == -2.0 and norm.vmax == 3.0 and norm.vcenter == 0.0


def test_compute_norm_center_requires_bounds():
    with pytest.raises(ValueError, match="requires both"):
        compute_norm(integer_field=False, vmin=None, vmax=None, center=0.0)
