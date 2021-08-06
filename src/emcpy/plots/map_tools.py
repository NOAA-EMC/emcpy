import cartopy.crs as ccrs


class Domain:

    def __init__(self, domain='global'):

        domain = domain.lower()

        map_domains = {
            "global": self._global,
            "conus": self._conus,
            "north america": self._north_america,
            "europe": self._europe}

        map_domains[domain]()

        try:
            return map_domains[domain]()
        except KeyError:
            raise TypeError(f'{domain} is not a valid domain.' +
                            'Current domains supported are:\n' +
                            f'{" | ".join(map_domains.keys())}"')

    def _global(self):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a global domain.
        """
        self.extent = (-180, 180, -90, 90)
        self.xticks = (-180, -120, -60, 0, 60, 120, 180)
        self.yticks = (-90, -60, -30, 0, 30, 60, 90)

    def _north_america(self):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a north american domain.
        """
        self.extent = (-170, -50, 7.5, 75)
        self.xticks = (-170, -150, -130, -110, -90, -70, -50)
        self.yticks = (10, 30, 50, 70)

    def _conus(self):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a contiguous United States domain.
        """
        self.extent = (-130, -65, 20, 55)
        self.xticks = (-130, -120, -110, -100, -90, -80, -70, -60)
        self.yticks = (25, 35, 45, 55)

    def _europe(self):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a European domain.
        """
        self.extent = (-12.5, 40, 30, 70)
        self.xticks = (-10, 0, 10, 20, 30, 40)
        self.yticks = (30, 40, 50, 60, 70)


class MapProjection:

    def __init__(self, projection='plcarr',
                 cenlon=0,
                 cenlat=0,
                 globe=None):

        self.cenlon = cenlon
        self.cenlat = cenlat
        self.globe = globe

        map_projections = {
            "plcarr": self._platecarree,
            "mill": self._miller,
            "npstere": self._npstereo,
            "spstere": self._spstereo}

        try:
            map_projections[projection]()
        except KeyError:
            raise TypeError(f'{domain} is not a valid domain.' +
                            'Current domains supported are:\n' +
                            f'{" | ".join(map_projections.keys())}"')

    def _platecarree(self):
        """Creates projection using PlateCarree from Cartopy."""
        self.projection = ccrs.PlateCarree(central_longitude=self.cenlon,
                                           globe=self.globe)

    def _miller(self):
        """Creates projection using Miller from Cartopy."""
        self.projection = ccrs.Miller(central_longitude=self.cenlon,
                                      globe=self.globe)

    def _npstereo(self):
        """
        Creates projection using Orthographic from Cartopy and
        orients it from central latitude 90 degrees.
        """
        self.cenlat = 90 if self.cenlat == 0 else self.cenlat

        self.projection = ccrs.Orthographic(central_longtiude=self.cenlon,
                                            central_latitude=self.cenlat,
                                            globe=self.globe)

    def _spstereo(self):
        """
        Creates projection using Orthographic from Cartopy and
        orients it from central latitude -90 degrees.
        """
        self.cenlat = -90 if self.cenlat == 0 else self.cenlat

        self.projection = ccrs.Orthographic(central_longtiude=self.cenlon,
                                            central_latitude=self.cenlat,
                                            globe=self.globe)
