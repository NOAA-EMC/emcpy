import numpy as np
import matplotlib.pyplot as plt
import cartopy.crs as ccrs
from emcpy.utils import roundNumber
from emcpy.plots import domains

__all__ = ['spatial']


def _map_scatter(latitude, longitude, data, domain, plotmap, plotopts):
    """
    Plot 1-dimensional data as scatter.
    """
    fig = plt.figure(figsize=plotopts['figsize'])

    if plotmap:
        ax = get_domain(fig, domain)
        cs = plt.scatter(longitude, latitude, c=data,
                         s=plotopts['marker size'], vmin=plotopts['vmin'],
                         vmax=plotopts['vmax'], cmap=plotopts['cmap'],
                         transform=ccrs.PlateCarree())
        if plotopts['grid']:
            ax.gridlines(crs=ccrs.PlateCarree())

    else:
        ax = fig.add_subplot()
        cs = plt.scatter(longitude, latitude, c=data,
                         s=plotopts['marker size'], vmin=plotopts['vmin'],
                         vmax=plotopts['vmax'], cmap=plotopts['cmap'])
        plt.grid(plotopts['grid'])

    cax = fig.add_axes([ax.get_position().x1 + 0.02,
                        ax.get_position().y0, 0.025,
                        ax.get_position().height])
    
    cb = plt.colorbar(cs, extend='both', cax=cax)
    cb.set_label(plotopts['cbar label'])

    plt.title(plotopts['title'], loc='left')
    plt.title(plotopts['time title'], loc='right', fontweight='semibold')

    return fig


def _map_pcolormesh(latitude, longitude, data, domain, plotmap, plotopts):
    """
    Plot 2-dimensional data on a map as pcolormesh.
    """
    fig = plt.figure(figsize=plotopts['figsize'])

    if plotmap:
        ax = get_domain(fig, domain)
        cs = ax.pcolormesh(longitude, latitude, data, cmap=plotopts['cmap'],
                           vmin=plotopts['vmin'], vmax=plotopts['vmax'],
                           transform=ccrs.PlateCarree())
        if plotopts['grid']:
            ax.gridlines(crs=ccrs.PlateCarree())

    else:
        ax = fig.add_subplot()
        cs = plt.pcolormesh(longitude, latitude, data, cmap=plotopts['cmap'],
                            vmin=plotopts['vmin'], vmax=plotopts['vmax'])
        plt.grid(plotopts['grid'])

    cax = fig.add_axes([ax.get_position().x1 + 0.02,
                        ax.get_position().y0, 0.025,
                        ax.get_position().height])
    
    cb = plt.colorbar(cs, extend='both', cax=cax)
    cb.set_label(plotopts['cbar label'])

    plt.title(plotopts['title'], loc='left')
    plt.title(plotopts['time title'], loc='right', fontweight='semibold')

    return fig


def map2d(latitude, longitude, data, domain='global', plotmap=True,
          figsize=(10, 8), cmap='viridis', markersize=10, grid=False,
          vmin=None, vmax=None, title='EMCPy Map Plot', time_title=None,
          cbar_label=None):
    """
    Plot a spatial map of desired data.

    Args:
        latitude : (array type) Latitude array for spatial data
        longitude : (array type) Longitude array for spatial data
        data : (array type) Spatial data to be plotted
        domain : (str, default='global') Map domain for plot
        plotmap : (bool, default=True) Plots data with a background map
        figsize : (tuple, default=(10,8)) Figure size
        cmap : (str, optional, default='viridis') Color map of data
        markersize : (int, optional, default=10) Marker size for 1D data types
        grid : (bool, optional, default=False) Plot grid on spatial plot
        vmin : (int, optional, default=None) Minimum value displayed on plot
        vmax : (int, optional, default=None) Maximum value displayed on plot
        title : (str, optional, default='EMCPy Map Plot') Plot title
        time_title : (str, optional, default=None) Secondary title for
                     date/cycle to add to plot
        cbar_label : (str, optional, deafult=None) Colorbar label

    Returns:
        A matplotlib figure object of the 2d plot
    """

    # If no vmin/vmax given, make the min/max of data
    if vmin is None:
        vmin = np.nanmin(data)

    if vmax is None:
        vmax = np.nanmax(data)

    # Dictionary of plot options
    plotopts = {'figsize': figsize, 'cmap': cmap, 'marker size': markersize,
                'vmin': roundNumber(vmin), 'vmax': roundNumber(vmax),
                'grid': grid, 'title': title, 'time title': time_title,
                'cbar label': cbar_label}

    # Plot scatter for 1D data; pcolormesh for 2D data
    if len(data.shape) == 1:
        fig = _map_scatter(latitude, longitude, data, domain,
                           plotmap, plotopts)
    elif len(data.shape) == 2:
        fig = _map_pcolormesh(latitude, longitude, data, domain,
                              plotmap, plotopts)
    else:
        raise TypeError('Data is not 1D or 2D. Please enter correct ' +
                        'dimension data.')

    return fig
