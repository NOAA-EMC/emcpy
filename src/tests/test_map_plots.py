import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots import CreateMap
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.map_plots import MapScatter, MapGridded


def test_plot_global_map_no_features():
    # Create global map with no data using
    # PlateCarree projection and no coastlines
    mymap = CreateMap(fig=plt.figure(figsize=(12, 8)),
                      domain=Domain('global'),
                      proj_obj=MapProjection('plcarr'))

    # return the figure from the map object
    fig = mymap.return_figure()

    # save figure as PNG
    fig.savefig('test_plot_global_map_no_features.png')


def test_plot_global_map_coastlines():
    # Create global map with no data using
    # PlateCarree projection and coastlines
    mymap = CreateMap(fig=plt.figure(figsize=(12, 8)),
                      domain=Domain('global'),
                      proj_obj=MapProjection('plcarr'))
    # Add coastlines
    mymap.add_features(['coastlines'])
    # Add x and y labels
    mymap.add_xlabel(xlabel='longitude')
    mymap.add_ylabel(ylabel='latitude')
    # return the figure from the map object
    fig = mymap.return_figure()

    # save figure as PNG
    fig.savefig('test_plot_global_map_coastlines.png')


def test_plot_map_scatter_conus():
    # Create scatter plot on CONUS domian
    mymap = CreateMap(fig=plt.figure(figsize=(12, 8)),
                      domain=Domain('conus'),
                      proj_obj=MapProjection('plcarr'))
    # Add coastlines
    mymap.add_features(['coastlines'])

    # generate a diagonal line across the US
    scatterobj = MapScatter(latitude=np.linspace(35, 50, 30),
                            longitude=np.linspace(-70, -120, 30),
                            data=np.linspace(200, 300, 30))
    # change colormap and markersize
    scatterobj.cmap = 'Blues'
    scatterobj.markersize = 25

    # Draw data onto map
    mymap.draw_data([scatterobj])

    # Add plot features
    mymap.add_colorbar(label='colorbar label',
                       label_fontsize=12, extend='neither')
    mymap.add_title(label='EMCPy Map', loc='center',
                    fontsize=20)
    mymap.add_xlabel(xlabel='longitude')
    mymap.add_ylabel(ylabel='latitude')

    # annotate some stats
    stats_dict = {
        'nobs': len(np.linspace(200, 300, 30)),
        'vmin': 200,
        'vmax': 300,
    }
    mymap.add_stats_dict(stats_dict=stats_dict)

    # return the figure from the map object
    fig = mymap.return_figure()

    # save figure as PNG
    fig.savefig('test_plot_map_scatter_conus.png')


def test_plot_map_gridded_global():
    # Create 2d gridded plot on global domian
    mymap = CreateMap(fig=plt.figure(figsize=(12, 8)),
                      domain=Domain('global'),
                      proj_obj=MapProjection('plcarr'))
    mymap.add_features(['coastlines'])

    # Create random gridded data
    lat, lon = np.mgrid[30:55:1, 235:290:1]
    data = np.random.randint(low=200, high=300, size=(25, 55))

    griddedobj = MapGridded(lat, lon, data)
    griddedobj.cmap = 'plasma'

    # Draw data onto map
    mymap.draw_data([griddedobj])

    # Add plot features
    mymap.add_colorbar(label='colorbar label',
                       label_fontsize=12, extend='neither')
    mymap.add_title(label='2D Gridded Data', fontsize=20)
    mymap.add_xlabel(xlabel='longitude')
    mymap.add_ylabel(ylabel='latitude')
    # return the figure from the map object
    fig = mymap.return_figure()

    # save figure as PNG
    fig.savefig('test_plot_map_gridded_global.png')


def test_plot_map_multidata_conus():
    # Plot scatter and gridded data on CONUS domain
    mymap = CreateMap(fig=plt.figure(figsize=(12, 8)),
                      domain=Domain('conus'),
                      proj_obj=MapProjection('plcarr'))
    mymap.add_features(['coastlines'])

    # Create random gridded data
    lat, lon = np.mgrid[30:55:1, 235:290:1]
    data = np.random.randint(low=200, high=300, size=(25, 55))

    griddedobj = MapGridded(lat, lon, data)
    griddedobj.cmap = 'gist_earth'

    # generate a diagonal line across the US
    scatterobj = MapScatter(latitude=np.linspace(35, 50, 30),
                            longitude=np.linspace(-70, -120, 30),
                            data=np.linspace(200, 300, 30))
    # change colormap and markersize
    scatterobj.cmap = 'Reds'
    scatterobj.markersize = 100
    # set colorbar=False so the gridded data is on colorbar
    scatterobj.colorbar = False

    # Draw data onto map in layered order
    mymap.draw_data([griddedobj, scatterobj])

    # Add plot features
    mymap.add_colorbar(label='colorbar label',
                       label_fontsize=12, extend='neither')
    mymap.add_title(label='2D Gridded Data and Scatter Data',
                    loc='left', fontsize=20)
    mymap.add_title(label='YYYYMMDDHHMM',
                    loc='right', fontsize=14,
                    fontweight='semibold')
    mymap.add_xlabel(xlabel='longitude')
    mymap.add_ylabel(ylabel='latitude')
    mymap.add_grid()
    # return the figure from the map object
    fig = mymap.return_figure()

    # save figure as PNG
    fig.savefig('test_plot_map_multidata_conus.png')
