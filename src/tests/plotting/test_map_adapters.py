# src/tests/plotting/test_map_adapters.py
import numpy as np
import pytest
import matplotlib.colors as mcolors

pytest.importorskip("cartopy")  # skip entire module if cartopy missing

from matplotlib.collections import PathCollection, QuadMesh
from matplotlib.contour import ContourSet
from matplotlib.colors import BoundaryNorm

from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.map_plots import MapScatter, MapGridded, MapContour, MapFilledContour


def _basic_map_plot(layer):
    plot = CreatePlot(plot_layers=[layer])
    plot.projection = "plcarr"
    plot.domain = "global"
    return plot


def test_map_scatter_with_data_mappable_and_colorbar(single_axes):
    lat = np.linspace(10, 30, 20)
    lon = np.linspace(-120, -90, 20)
    data = np.linspace(200, 300, 20)
    s = MapScatter(latitude=lat, longitude=lon, data=data)
    s.cmap = "viridis"
    s.markersize = 30

    plot = _basic_map_plot(s)
    plot.add_colorbar(label="units")

    fig, ax = single_axes(plot)
    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, PathCollection)
    assert len(fig.fig.axes) == 2


def test_map_scatter_plain_points_no_colorbar(single_axes):
    lat = np.linspace(35, 40, 5)
    lon = np.linspace(-105, -95, 5)
    s = MapScatter(latitude=lat, longitude=lon)
    s.color = "tab:red"
    s.markersize = 25

    plot = _basic_map_plot(s)
    plot.add_colorbar(label="ignored")
    fig, ax = single_axes(plot)

    assert len(fig.fig.axes) == 1


def test_map_scatter_integer_field_auto_bounds():
    import matplotlib.colors as mcolors
    lat = np.linspace(30, 40, 5)
    lon = np.linspace(-100, -90, 5)
    data = np.array([0, 1, 2, 3, 4])
    s = MapScatter(latitude=lat, longitude=lon, data=data)
    s.integer_field = True  # auto-discrete bounds now

    plot = _basic_map_plot(s)
    plot.add_colorbar()

    fig = CreateFigure(nrows=1, ncols=1)
    fig.plot_list = [plot]
    fig.create_figure()

    # Grab the scatter PathCollection (mappable) from the axes
    ax = fig.fig.axes[0]
    mappables = [c for c in ax.collections if getattr(c, "get_array", None)]
    assert mappables, "Expected at least one mappable collection"
    pc = mappables[-1]

    # Discrete norm must be BoundaryNorm with half-step boundaries
    assert isinstance(pc.norm, mcolors.BoundaryNorm)
    boundaries = pc.norm.boundaries
    assert boundaries is not None and len(boundaries) >= 2
    # First/last boundaries should be k-0.5 and k+0.5 around the integer range
    assert abs(boundaries[0] - (-0.5)) < 1e-12
    assert abs(boundaries[-1] - (4.5)) < 1e-12


def test_map_gridded_edges_ok_and_colorbar(single_axes):
    lon = np.linspace(0, 360, 51)   # edges
    lat = np.linspace(-90, 90, 51)  # edges
    Z = np.random.RandomState(0).rand(50, 50)  # centers

    g = MapGridded(lon, lat, Z)
    g.cmap = "plasma"

    plot = _basic_map_plot(g)
    plot.add_colorbar(label="plasma")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, QuadMesh)
    assert len(fig.fig.axes) == 2


def test_map_gridded_integer_field_auto_bounds():
    import matplotlib.colors as mcolors
    lon = np.linspace(-100, -90, 21)
    lat = np.linspace(  30,  40, 11)
    LON, LAT = np.meshgrid(lon, lat)
    Z = np.floor(3 * np.sin(np.radians(LAT)) + 3).astype(int)  # integers 0..5

    g = MapGridded(latitude=LAT, longitude=LON, data=Z)
    g.integer_field = True

    plot = _basic_map_plot(g)
    plot.add_colorbar()

    fig = CreateFigure(nrows=1, ncols=1)
    fig.plot_list = [plot]
    fig.create_figure()

    ax = fig.fig.axes[0]
    # pcolormesh returns a QuadMesh (ScalarMappable)
    meshes = [im for im in ax.collections + ax.images if hasattr(im, "get_array")]
    assert meshes, "Expected a ScalarMappable (QuadMesh) from pcolormesh"
    qm = meshes[-1]
    assert isinstance(qm.norm, mcolors.BoundaryNorm)
    boundaries = qm.norm.boundaries
    assert boundaries is not None and len(boundaries) > 2
    # Boundaries should bracket integer classes (around min/max with +/-0.5)
    assert boundaries[0] <= (Z.min() - 0.5) + 1e-12
    assert boundaries[-1] >= (Z.max() + 0.5) - 1e-12


def test_map_contour_returns_contourset_and_colorbar(single_axes):
    lon = np.linspace(0, 360, 40)
    lat = np.linspace(-60, 60, 30)
    LON, LAT = np.meshgrid(lon, lat)
    Z = np.cos(np.deg2rad(LAT)) * np.cos(2 * np.deg2rad(LON))

    c = MapContour(LON, LAT, Z)
    c.levels = np.linspace(-1.0, 1.0, 11)
    c.colors = "k"

    plot = _basic_map_plot(c)
    plot.add_colorbar(label="contour")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m, ContourSet)
    assert len(fig.fig.axes) == 2


def test_map_filled_contour_single_cbar_last_subplot():
    plots = []
    for seed in (0, 1, 2, 3):
        rng = np.random.RandomState(seed)
        lon = np.linspace(0, 360, 40)
        lat = np.linspace(-60, 60, 30)
        LON, LAT = np.meshgrid(lon, lat)
        Z = rng.rand(*LON.shape)

        cf = MapFilledContour(LON, LAT, Z)
        cf.cmap = "viridis"

        p = _basic_map_plot(cf)
        p.add_colorbar(orientation="horizontal", single_cbar=True, label="CF")
        plots.append(p)

    fig = CreateFigure(nrows=2, ncols=2, figsize=(8, 6))
    fig.plot_list = plots
    fig.create_figure()

    assert len(fig.fig.axes) == 5  # 4 plots + 1 shared cbar


@pytest.mark.skipif(not pytest.importorskip("cartopy"), reason="Cartopy missing")
def test_map_scatter_integer_field_applies_boundarynorm(single_axes):
    lat = np.array([0, 1, 2, 3])
    lon = np.array([0, 1, 2, 3])
    vals = np.array([0, 1, 2, 3])

    layer = MapScatter(latitude=lat, longitude=lon, data=vals)
    layer.integer_field = True
    layer.vmin = 0
    layer.vmax = 3

    plot = CreatePlot(plot_layers=[layer], projection="plcarr", domain="global")
    fig, ax = single_axes(plot)

    m = fig._last_mappable_for_ax(ax)
    assert isinstance(m.norm, BoundaryNorm)
