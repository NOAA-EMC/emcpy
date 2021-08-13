class MapScatter:

    plottype = 'map_scatter'

    def __init__(self, latitude, longitude, data):
        """
        Constructor for MapScatter.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type) data to be plotted
        """

        self.latitude = latitude
        self.longitude = longitude
        self.data = data

        self.marker = 'o'
        self.markersize = 5
        self.cmap = 'viridis'
        self.edgecolors = None
        self.alpha = None
        self.vmin = None
        self.vmax = None
        self.colorbar = True


class MapGridded:

    plottype = 'map_gridded'

    def __init__(self, latitude, longitude, data):
        """
        Constructor for MapGridded.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type) data to be plotted
        """

        self.latitude = latitude
        self.longitude = longitude
        self.data = data

        self.cmap = 'viridis'
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = True


class MapContour:

    plottype = 'map_contour'

    def __init__(self, latitude, longitude, data):
        """
        Constructor for MapScatter.

        Args:
            latitude : (array type) Latitude data
            longitude : (array type) Longitude data
            data : (array type) data to be plotted
        """

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
