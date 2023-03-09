__all__ = ['MapScatter', 'MapGridded', 'MapContour',
           'MapContourf']


class MapScatter:

    def __init__(self, latitude, longitude, data=None):
        """
        Constructor for MapScatter.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type; default=None) data to be plotted
        """
        self.plottype = 'map_scatter'

        self.latitude = latitude
        self.longitude = longitude
        self.data = data

        self.marker = 'o'
        self.markersize = 5
        if data is None:
            self.color = 'tab:blue'
        else:
            self.cmap = 'viridis'
        self.linewidths = 1.5
        self.edgecolors = None
        self.alpha = None
        self.vmin = None
        self.vmax = None
        self.label = None
        self.colorbar = False if data is None else True


class MapGridded:

    def __init__(self, latitude, longitude, data):
        """
        Constructor for MapGridded.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type) data to be plotted
        """
        self.plottype = 'map_gridded'

        self.latitude = latitude
        self.longitude = longitude
        self.data = data

        self.cmap = 'viridis'
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = True


class MapContour:

    def __init__(self, latitude, longitude, data):
        """
        Constructor for MapContour.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type) data to be plotted
        """
        self.plottype = 'map_contour'

        self.latitude = latitude
        self.longitude = longitude
        self.data = data

        self.levels = None
        self.clabel = False
        self.colors = 'black'
        self.linewidths = 1.5
        self.linestyles = '-'
        self.cmap = None
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = False
