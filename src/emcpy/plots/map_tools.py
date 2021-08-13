import cartopy.crs as ccrs


class Domain:

    def __init__(self, domain='global', dd=dict()):
        """
        Class constructor that stores extent, xticks, and
        yticks for the domain given.

        Args:
            domain : (str; default='global') domain name to grab info
            dd : (dict) dictionary to add custom xticks, yticks
        """
        domain = domain.lower()

        map_domains = {
            "global": self._global,
            "conus": self._conus,
            "north america": self._north_america,
            "europe": self._europe,
            "custom": self._custom
        }

        try:
            map_domains[domain](dd=dd)
        except KeyError:
            raise TypeError(f'{domain} is not a valid domain.' +
                            'Current domains supported are:\n' +
                            f'{" | ".join(map_domains.keys())}"')

    def _global(self, dd=dict()):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a global domain.
        """
        self.extent = (-180, 180, -90, 90)
        self.xticks = dd.get('xticks', (-180, -120, -60,
                                        0, 60, 120, 180))
        self.yticks = dd.get('yticks', (-90, -60, -30, 0,
                                        30, 60, 90))

    def _north_america(self, dd=dict()):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a north american domain.
        """
        self.extent = (-170, -50, 7.5, 75)
        self.xticks = dd.get('xticks', (-170, -150, -130, -110,
                                        -90, -70, -50))
        self.yticks = dd.get('yticks', (10, 30, 50, 70))

    def _conus(self, dd=dict()):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a contiguous United States domain.
        """
        self.extent = (-130, -65, 20, 55)
        self.xticks = dd.get('xticks', (-130, -120, -110, -100,
                                        -90, -80, -70, -60))
        self.yticks = dd.get('yticks', (25, 35, 45, 55))

    def _europe(self, dd=dict()):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a European domain.
        """
        self.extent = (-12.5, 40, 30, 70)
        self.xticks = dd.get('xticks', (-10, 0, 10, 20, 30, 40))
        self.yticks = dd.get('yticks', (30, 40, 50, 60, 70))

    def _custom(self, dd=dict()):
        """
        Sets extent, longitude xticks, and latitude yticks
        for a Custom domain.
        """
        self.extent = dd.extent
        self.xticks = dd.xticks
        self.yticks = dd.yticks


class MapProjection:

    def __init__(self, projection='plcarr',
                 cenlon=None,
                 cenlat=None,
                 globe=None):
        """
        Class constructor that stores projection cartopy object
        for the projection given.

        Args:
            projection : (str; default='plcarr') projection name to grab info
            cenlon : (int, float; default=None) central longitude
            cenlat : (int, float; default=None) central latitude
            globe : (default=None) if ommited, creates a globe for map
        """
        self.str_projection = projection

        self.cenlon = cenlon
        self.cenlat = cenlat
        self.globe = globe

        map_projections = {
            "plcarr": self._platecarree,
            "mill": self._miller,
            "npstere": self._npstereo,
            "spstere": self._spstereo
        }

        try:
            map_projections[projection]()
        except KeyError:
            raise TypeError(f'{projection} is not a valid projection.' +
                            'Current projections supported are:\n' +
                            f'{" | ".join(map_projections.keys())}"')

    def __str__(self):
        return self.str_projection

    def _platecarree(self):
        """Creates projection using PlateCarree from Cartopy."""
        self.cenlon = 0 if self.cenlon is None else self.cenlon

        self.projection = ccrs.PlateCarree(central_longitude=self.cenlon,
                                           globe=self.globe)

    def _miller(self):
        """Creates projection using Miller from Cartopy."""
        self.cenlon = 0 if self.cenlon is None else self.cenlon

        self.projection = ccrs.Miller(central_longitude=self.cenlon,
                                      globe=self.globe)

    def _npstereo(self):
        """
        Creates projection using Orthographic from Cartopy and
        orients it from central latitude 90 degrees.
        """
        self.cenlon = -90 if self.cenlon is None else self.cenlon

        self.projection = ccrs.Orthographic(central_longitude=self.cenlon,
                                            central_latitude=90,
                                            globe=self.globe)

    def _spstereo(self):
        """
        Creates projection using Orthographic from Cartopy and
        orients it from central latitude -90 degrees.
        """
        self.cenlon = 0 if self.cenlon is None else self.cenlon

        self.projection = ccrs.Orthographic(central_longitude=self.cenlon,
                                            central_latitude=-90,
                                            globe=self.globe)
