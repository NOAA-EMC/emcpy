# tests/plotting/test_maps.py
import numpy as np
import pytest

from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots.map_plots import MapScatter, MapGridded, MapContour, MapFilledContour


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_global_map_no_features():
    plot = CreatePlot()
    plot.projection = "plcarr"
    plot.domain = "global"
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert "GeoAxes" in ax.__class__.__name__


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_global_map_coastlines_and_labels():
    plot = CreatePlot()
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_map_features(["coastline", "land", "ocean"])
    plot.add_xlabel(xlabel="longitude")
    plot.add_ylabel(ylabel="latitude")
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert ax.get_xlabel() == "longitude"
    assert ax.get_ylabel() == "latitude"


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_scatter_conus_with_colorbar():
    scatter = MapScatter(latitude=np.linspace(35, 50, 30),
                         longitude=np.linspace(-70, -120, 30),
                         data=np.linspace(200, 300, 30))
    scatter.cmap = "Blues"
    scatter.markersize = 25
    plot = CreatePlot(plot_layers=[scatter])
    plot.projection = "plcarr"
    plot.domain = "conus"
    plot.add_map_features(["coastline", "states"])
    plot.add_colorbar(label="colorbar label", fontsize=12)
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    assert len(fig.fig.axes) >= 2  # colorbar axes present


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_scatter_2d_no_colorbar():
    scatter = MapScatter(latitude=np.linspace(35, 50, 30),
                         longitude=np.linspace(-70, -120, 30))
    scatter.color = "tab:red"
    scatter.markersize = 25
    plot = CreatePlot(plot_layers=[scatter])
    plot.projection = "plcarr"
    plot.domain = "conus"
    plot.add_map_features(["coastline", "states"])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    assert len(fig.fig.axes) == 1


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_gridded_global():
    lats = np.linspace(25, 50, 25)
    lons = np.linspace(245, 290, 45)
    X, Y = np.meshgrid(lats, lons)
    Z = np.random.normal(size=X.shape)
    gridded = MapGridded(X, Y, Z)
    plot = CreatePlot(plot_layers=[gridded])
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_map_features(["coastline"])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert len(ax.collections) >= 1  # QuadMesh


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_contour_global_combo():
    x, y, z = _contour_data((20, 40))
    z = z * -1.5 * x
    contour = MapContour(x, y, z)
    gridded = MapGridded(x, y, z)
    plot = CreatePlot(plot_layers=[contour, gridded])
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_map_features(["coastline"])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert len(ax.collections) >= 2


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_filled_contour_global():
    x, y, z = _contour_data((20, 40))
    z = z * -1.5 * x
    contourf = MapFilledContour(x, y, z)
    contourf.cmap = "viridis"
    contour = MapContour(x, y, z)
    plot = CreatePlot(plot_layers=[contourf, contour])
    plot.projection = "plcarr"
    plot.domain = "global"
    plot.add_map_features(["coastline"])
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    ax = fig.fig.axes[0]
    assert len(ax.collections) >= 2


@pytest.mark.usefixtures("skip_if_no_cartopy")
def test_plot_map_multidata_conus_with_colorbar():
    lats = np.linspace(25, 50, 25)
    lons = np.linspace(245, 290, 45)
    X, Y = np.meshgrid(lats, lons)
    Z = np.random.normal(size=X.shape)
    gridded = MapGridded(X, Y, Z)
    scatter = MapScatter(
        latitude=np.linspace(35, 50, 30),
        longitude=np.linspace(-70, -120, 30),
        data=np.linspace(200, 300, 30),
    )
    scatter.cmap = "Reds"
    scatter.markersize = 100
    scatter.colorbar = False
    plot = CreatePlot(plot_layers=[gridded, scatter])
    plot.projection = "plcarr"
    plot.domain = "conus"
    plot.add_map_features(["coastline"])
    plot.add_colorbar(label="colorbar label", fontsize=12)
    fig = CreateFigure()
    fig.plot_list = [plot]
    fig.create_figure()
    assert len(fig.fig.axes) >= 2


def _contour_data(shape=(73, 145)):
    nlats, nlons = shape
    lats = np.linspace(-np.pi/2, np.pi/2, nlats)
    lons = np.linspace(0, 2*np.pi, nlons)
    lons, lats = np.meshgrid(lons, lats)
    wave = 0.75*(np.sin(2*lats)**8)*np.cos(4*lons)
    mean = 0.5*np.cos(2*lats)*((np.sin(2*lats))**2 + 2)
    lats = np.rad2deg(lats)
    lons = np.rad2deg(lons)
    data = wave + mean
    return lats, lons, data
