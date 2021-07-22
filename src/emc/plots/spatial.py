import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from matplotlib import rcParams, ticker, cm
import cartopy.feature as cfeature
import cartopy.crs as ccrs
import matplotlib.colors as mcolors
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter


def _global(latitude, longitude, data, **kwargs):
    """
    Plot data on global domain.
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

    cs = plt.scatter(longitude, latitude, c=data, s=10,
                     vmin=kwargs['vmin'], vmax=kwargs['vmax'],
                     cmap=kwargs['cmap'], transform=ccrs.PlateCarree())

    cb = plt.colorbar(cs, shrink=0.5, pad=.03, extend='both')
    cb.set_label(kwargs['cbar_label'])

    plt.title(kwargs['title'], loc='left')
    plt.title(kwargs['cycle'], loc='right', fontweight='semibold')

    return fig


def _conus(latitude, longitude, data, **kwargs):
    """
    Plot data on CONUS domain.
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

    cs = plt.scatter(longitude, latitude, c=data, s=10,
                     vmin=kwargs['vmin'], vmax=kwargs['vmax'],
                     cmap=kwargs['cmap'], transform=ccrs.PlateCarree())

    cb = plt.colorbar(cs, shrink=0.5, pad=.03, extend='both')
    cb.set_label(kwargs['cbar_label'])

    plt.title(kwargs['title'], loc='left')
    plt.title(kwargs['cycle'], loc='right', fontweight='semibold')

    return fig


def _north_america():
    """
    Plot data on CONUS domain.
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

    cs = plt.scatter(longitude, latitude, c=data, s=10,
                     vmin=kwargs['vmin'], vmax=kwargs['vmax'],
                     cmap=kwargs['cmap'], transform=ccrs.PlateCarree())

    cb = plt.colorbar(cs, shrink=0.5, pad=.03, extend='both')
    cb.set_label(kwargs['cbar_label'])

    plt.title(kwargs['title'], loc='left')
    plt.title(kwargs['cycle'], loc='right', fontweight='semibold')

    return fig


def spatial(latitude, longitude, data, domain='global', cmap='viridis',
            vmin=None, vmin=None, title=None, cycle=None, cbar_label=None):
    """
    Plot a spatial map of desired data.
    Paramaters
    ----------
    Required:
    latitude, longitude, data : array type
    domain : domain of map (str)

    Optional:
    cmap : colormap (str)
           (https://matplotlib.org/stable/gallery/color/colormap_reference.html)
    vmin : minumum value of data
    vmax : maximum value of data
    title : plot title (str)
    cycle : cycle of data (str)
    cbar_label : colorbar label
    """

    # Make string lowercase
    domain = domain.lower()

    # Dictionary of kwargs
    kwargs = {'cmap': cmap, 'vmin': vmin, 'vmax': vmax,
              'title': title, 'cycle': cycle, 'cbar_label': cbar_label}

    if domain == 'global':
        fig = _global(latitude, longitude, data, **kwargs)

    elif domain == 'conus':
        fig = _conus(latitude, longitude, data, **kwargs)

    elif domain == 'north america':
        fig = _north_america(latitude, longitude, data, **kwargs)

    return fig
