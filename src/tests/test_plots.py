import emcpy.plots
import numpy as np

def test_plot_scatter():
    # create random x and y data
    x_data = np.random.rand(100)
    y_data = np.random.rand(100)
    # generate scatter plot
    fig = emcpy.plots.scatter(x_data, y_data, linear_regression=True,
                              grid=False, title='Test Scatter Plot',
                              time_title='Random time',
                              xlabel='Random X', ylabel='Random Y',
                              )
    # save figure as PNG
    fig.savefig('test_plot_scatter.png')

def test_plot_map2d_scatter_conus():
    # generate a diagonal line across the US
    lat = np.linspace(35, 50, 30)
    lon = np.linspace(-70, -120, 30)
    # create some fake temperature obs
    data1 = np.linspace(310, 290, 30)
    # generate plot of points on a map
    fig = emcpy.plots.map2d(lat, lon, data1, domain='conus',
                            cmap='jet', markersize=20, grid=True,
                            title='Test CONUS 1D Data',
                            time_title='YYYYMMDDHH',
                            cbar_label='Temperature (K)',
                            )
    # save figure as PNG
    fig.savefig('test_plot_map2d_scatter_conus.png',
                bbox_inches='tight', pad_inches=0.1)

def test_plot_map2d_pcolormesh_global():
    # create some lat, lon values
    lat, lon = np.mgrid[30:55:1, 235:290:1]
    # create some temperature values
    data2d = np.random.randint(low=270, high=310, size=(25,55))
    # generate plot of 2D data on a map
    fig = emcpy.plots.map2d(lat, lon, data2d, domain='global',
                            grid=True, title='Test Global 2D Data',
                            time_title='YYYYMMDDHH',
                            cbar_label='Temperature (K)',
                            )
    # save figure as PNG
    fig.savefig('test_plot_pcolormesh_global.png',
                bbox_inches='tight', pad_inches=0.1)

def test_plot_map2d_pcolormesh_nomap():
    # create some lat, lon values
    lat, lon = np.mgrid[30:55:1, 235:290:1]
    # create some temperature values
    data2d = np.random.randint(low=270, high=310, size=(25,55))
    # generate plot of 2D data on a map
    fig = emcpy.plots.map2d(lat, lon, data2d, domain='global', plotmap=False,
                            grid=True, title='Test No Map Projection 2D Data',
                            time_title='YYYYMMDDHH',
                            cbar_label='Temperature (K)',
                            )
    # save figure as PNG
    fig.savefig('test_plot_pcolormesh_nomap.png',
                bbox_inches='tight', pad_inches=0.1)
