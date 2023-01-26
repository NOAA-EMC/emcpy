import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.map_plots import MapScatter, MapGridded, MapContour


def test_plot_global_map_no_features():
    # Create global map with no data using
    # PlateCarree projection and no coastlines
    plot1 = CreatePlot()
    plot1.projection = 'plcarr'
    plot1.domain = 'global'

    # return the figure from the map object
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_global_map_no_features.png')


def test_plot_global_map_coastlines():
    # Create global map with no data using
    # PlateCarree projection and coastlines
    plot1 = CreatePlot()
    plot1.projection = 'plcarr'
    plot1.domain = 'global'
    plot1.add_map_features(['coastline', 'land', 'ocean'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_global_map_coastlines.png')


def test_plot_map_scatter_conus():
    # Create scatter plot on CONUS domian
    scatter = MapScatter(latitude=np.linspace(35, 50, 30),
                         longitude=np.linspace(-70, -120, 30),
                         data=np.linspace(200, 300, 30))
    # change colormap and markersize
    scatter.cmap = 'Blues'
    scatter.markersize = 25

    plot1 = CreatePlot()
    plot1.plot_layers = [scatter]
    plot1.projection = 'plcarr'
    plot1.domain = 'conus'
    plot1.add_map_features(['coastline', 'states'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_title(label='EMCPy Map', loc='center',
                    fontsize=20)
    plot1.add_colorbar(label='colorbar label',
                       fontsize=12, extend='neither')

    # annotate some stats
    stats_dict = {
        'nobs': len(np.linspace(200, 300, 30)),
        'vmin': 200,
        'vmax': 300,
    }
    plot1.add_stats_dict(stats_dict=stats_dict, yloc=-0.175)

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_map_scatter_conus.png')


def test_plot_map_scatter_2D_conus():
    # Create scatter plot on CONUS domian
    scatter = MapScatter(latitude=np.linspace(35, 50, 30),
                         longitude=np.linspace(-70, -120, 30))
    # change colormap and markersize
    scatter.color = 'tab:red'
    scatter.markersize = 25

    plot1 = CreatePlot()
    plot1.plot_layers = [scatter]
    plot1.projection = 'plcarr'
    plot1.domain = 'conus'
    plot1.add_map_features(['coastline', 'states'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_title(label='EMCPy Map', loc='center',
                    fontsize=20)

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_map_scatter_2D_conus.png')


def test_plot_map_gridded_global():
    # Create 2d gridded plot on global domian
    lats = np.linspace(25, 50, 25)
    lons = np.linspace(245, 290, 45)
    X, Y = np.meshgrid(lons, lats)
    Z = np.random.normal(size=X.shape)

    gridded = MapGridded(X, Y, Z)
    gridded.cmap = 'plasma'

    plot1 = CreatePlot()
    plot1.plot_layers = [gridded]
    plot1.projection = 'plcarr'
    plot1.domain = 'global'
    plot1.add_map_features(['coastline'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_title(label='2D Gridded Data', loc='center')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_map_gridded_global.png')


def test_plot_map_contour_global():
    x, y, z = _getContourData((20, 40))
    z = z * -1.5 * y

    contour = MapContour(x, y, z)
    gridded = MapGridded(x, y, z)

    plot1 = CreatePlot()
    plot1.plot_layers = [contour, gridded]
    plot1.projection = 'plcarr'
    plot1.domain = 'global'
    plot1.add_map_features(['coastline'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_title(label='Contour Data', loc='center')

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_map_contour_global.png')


def test_plot_map_multidata_conus():
    # Plot scatter and gridded data on CONUS domain
    lats = np.linspace(25, 50, 25)
    lons = np.linspace(245, 290, 45)
    X, Y = np.meshgrid(lons, lats)
    Z = np.random.normal(size=X.shape)

    gridded = MapGridded(X, Y, Z)
    gridded.cmap = 'gist_earth'

    scatter = MapScatter(latitude=np.linspace(35, 50, 30),
                         longitude=np.linspace(-70, -120, 30),
                         data=np.linspace(200, 300, 30))
    # change colormap and markersize
    scatter.cmap = 'Reds'
    scatter.markersize = 100
    # set colorbar=False so the gridded data is on colorbar
    scatter.colorbar = False

    plot1 = CreatePlot()
    plot1.plot_layers = [gridded, scatter]
    plot1.projection = 'plcarr'
    plot1.domain = 'conus'
    plot1.add_map_features(['coastline'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_colorbar(label='colorbar label',
                       fontsize=12, extend='neither')
    plot1.add_title(label='2D Gridded Data and Scatter Data',
                    loc='left', fontsize=12)
    plot1.add_grid()

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()
    fig.save_figure('test_plot_map_multidata_conus.png')


def _getContourData(shape=(73, 145)):
    # Generate test data for contour plots
    nlats, nlons = shape
    lats = np.linspace(-np.pi / 2, np.pi / 2, nlats)
    lons = np.linspace(0, 2 * np.pi, nlons)
    lons, lats = np.meshgrid(lons, lats)
    wave = 0.75 * (np.sin(2 * lats) ** 8) * np.cos(4 * lons)
    mean = 0.5 * np.cos(2 * lats) * ((np.sin(2 * lats)) ** 2 + 2)

    lats = np.rad2deg(lats)
    lons = np.rad2deg(lons)
    data = wave + mean

    return lons, lats, data
