__all__ = ['spatial']

import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import rcParams, ticker, cm
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def _global():
    """
    Return fig, ax on global domain.
    """
    fig = plt.figure(figsize=(12, 10))
    ax = fig.add_subplot(1, 1, 1,
                         projection=ccrs.PlateCarree(central_longitude=0))
    ax.add_feature(cfeature.GSHHSFeature(scale='auto'))
    ax.set_extent([-180, 180, -90, 90])
    ax.set_xticks([-180, -120, -60, 0, 60, 120, 180], crs=ccrs.PlateCarree())
    ax.set_yticks([-90, -60, -30, 0, 30, 60, 90], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    return fig, ax


def _north_america():
    """
    Return fig, ax on CONUS domain.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1,
                         projection=ccrs.PlateCarree(central_longitude=0))
    ax.add_feature(cfeature.GSHHSFeature(scale='auto'))
    ax.set_extent([-170, -50, 7.5, 75])
    ax.set_xticks([-170, -150, -130, -110, -90, -70, -50],
                  crs=ccrs.PlateCarree())
    ax.set_yticks([10, 30, 50, 70], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    return fig, ax


def _conus():
    """
    Return fig, ax on CONUS domain.
    """
    fig = plt.figure(figsize=(10, 8))
    ax = fig.add_subplot(1, 1, 1,
                         projection=ccrs.PlateCarree(central_longitude=0))
    ax.add_feature(cfeature.GSHHSFeature(scale='auto'))
    ax.set_extent([-130, -60, 10, 60])
    ax.set_xticks([-130, -120, -110, -100, -90, -80, -70, -60],
                  crs=ccrs.PlateCarree())
    ax.set_yticks([10, 20, 30, 40, 50, 60], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)

    return fig, ax


def _spatial_scatter(fig, ax, longitude, latitude, data, plotopts):
    """
    Plot 1-dimensional data on a map as scatter.
    """
    cs = plt.scatter(latitude, longitude, c=data, s=plotopts['marker size'],
                     vmin=plotopts['vmin'], vmax=plotopts['vmax'],
                     cmap=plotopts['cmap'], transform=ccrs.PlateCarree())

    cb = plt.colorbar(cs, shrink=0.5, pad=.03, extend='both')
    cb.set_label(plotopts['cbar label'])

    plt.grid(plotopts['grid'])
    plt.title(plotopts['title'], loc='left')
    plt.title(plotopts['cycle'], loc='right', fontweight='semibold')

    return fig


def _spatial_pcolormesh(fig, ax, longitude, latitude, data, plotopts):
    """
    Plot 2-dimensional data on a map as pcolormesh.
    """
    cs = plt.pcolormesh(lon, lat, data, cmap=plotopts['cmap'],
                        vmin=plotopts['vmin'], vmax=plotopts['vmax'],
                        transform=ccrs.PlateCarree())

    cb = plt.colorbar(cs, shrink=0.5, pad=.03, extend='both')
    cb.set_label(plotopts['cbar label'])

    plt.grid(plotopts['grid'])
    plt.title(plotopts['title'], loc='left')
    plt.title(plotopts['cycle'], loc='right', fontweight='semibold')

    return fig


def spatial(latitude, longitude, data, domain='global', cmap='viridis',
            markersize=10, grid=False, vmin=None, vmax=None, title=None,
            cycle=None, cbar_label=None):
    """
    Plot a spatial map of desired data.

    Paramaters
    ----------
    latitude : array type
        Latitude array for spatial data
    longitude : array type
        Longitude array for spatial data
    data : array type
        Spatial data to be plotted
    domain : str
        Plot domain of map
    cmap : str, optional
        Color map of spatial plot (default is 'viridis')
    markersize : int, optional
        Marker size for 1D data types (default is 10)
    grid : bool, optional
        Plot grid on spatial plot (default is False)
    vmin : int, optional
        Minimum value to be displayed on spatial plot (default is data.min())
    vmax : int, optional
        Maximum value to be displayed on spatial plot (default is data.max())
    title : str, optional
        Plot title (default is 'EMCPy Spatial Plot')
    cycle : str, optional
        Data data/cycle (default is None)
    cbar_label : str, optional
        Colorbar label (default is None)

    Returns
    -------
    fig
        Figure of spatial plot
    """


    # Make string lowercase
    domain = domain.lower()

    # Dictionary of kwargs
    plotopts = {'cmap': cmap, 'marker size': markersize, 'vmin': vmin,
                'vmax': vmax, 'grid': grid, 'title': title, 'cycle': cycle,
                'cbar label': cbar_label}

    # Get domain fig/ax
    if domain == 'global':
        fig, ax = _global()

    elif domain == 'conus':
        fig, ax = _conus()

    elif domain == 'north america':
        fig, ax = _north_america()

    else:
        raise TypeError(f'{domain} is not a valid domain. Current ' +
                        'domains supported are: global, conus, north america')

    # Plot scatter for 1D data; pcolormesh for 2D data
    if len(data.shape) == 1:
        fig = _spatial_scatter(fig, ax, latitude, longitude, data, plotopts)
    elif len(data.shape) == 2:
        fig = _spatial_pcolormesh(fig, ax, latitude, longitude, data, plotopts)
    else:
        raise TypeError('Data is not 1D or 2D. Please enter correct ' +
                        'dimension data.')

    return fig
