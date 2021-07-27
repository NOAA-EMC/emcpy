import cartopy.feature as cfeature
import cartopy.crs as ccrs
from cartopy.mpl.ticker import LongitudeFormatter, LatitudeFormatter
import matplotlib.pyplot as plt

__all__ = ['get_domain']


def _global():
    """
    Return ax on global domain.
    """
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

    return ax


def _north_america():
    """
    Return ax on CONUS domain.
    """
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

    return ax


def _conus():
    """
    Return ax on CONUS domain.
    """
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

    return ax


def _europe():
    """
    Returns ax on Europe domain.
    """
    ax = fig.add_subplot(1, 1, 1,
                         projection=ccrs.PlateCarree(central_longitude=0))
    ax.add_feature(cfeature.GSHHSFeature(scale='auto'))
    ax.set_extent([-12.5, 40, 30, 70])
    ax.set_xticks([-10, 0, 10, 20, 30, 40],
                  crs=ccrs.PlateCarree())
    ax.set_yticks([30, 40, 50, 60, 70], crs=ccrs.PlateCarree())
    lon_formatter = LongitudeFormatter(zero_direction_label=False)
    lat_formatter = LatitudeFormatter()
    ax.xaxis.set_major_formatter(lon_formatter)
    ax.yaxis.set_major_formatter(lat_formatter)


def get_domain(domain):
    """
    Factory function to grab correct ax based on inputted domain.
    Parameters
    ----------
        domain : (str) domain to be plotted on map

    Returns
    -------
        ax : axis used to plot map on a figure
    """
    domain = domain.lower()

    map_domains = {
        "global": _global,
        "conus": _conus,
        "north america": _north_america,
        "europe": _europe
    }

    try:
        return map_domains[domain]()
    except KeyError:
        raise TypeError(f'{domain} is not a valid domain. Current ' +
                        'domains supported are:\n' +
                        'global | conus | north america | europe')
