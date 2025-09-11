import numpy as np

__all__ = ['MapScatter', 'MapGridded', 'MapContour', 'MapFilledContour']


class MapScatter:
    """
    Scatter points on a map.

    Parameters
    ----------
    latitude : array-like
        Latitudes (degrees). Must align in shape with `longitude`.
    longitude : array-like
        Longitudes (degrees). Must align in shape with `latitude`.
    data : array-like or None, optional
        Optional scalar values for color mapping. If None, points use a
        solid color (no colorbar). If provided, a colormap is used and
        a colorbar is enabled by default.

    Notes
    -----
    Constructor order is (latitude, longitude, data). This class validates:
      - `latitude` and `longitude` have the same shape (or broadcastable 1D lengths).
      - Latitude values look like latitudes (|lat| <= 90). If they look like
        longitudes, we raise a helpful error about parameter order.
    """

    def __init__(self, latitude, longitude, data=None):
        self.plottype = 'map_scatter'

        self.latitude = np.asarray(latitude)
        self.longitude = np.asarray(longitude)
        self.data = None if data is None else np.asarray(data)

        # ---- shape checks ----
        if self.latitude.shape != self.longitude.shape:
            # Allow 1D broadcastable case: both 1D with same length
            if not (self.latitude.ndim == 1 and self.longitude.ndim == 1 and
                    self.latitude.shape[0] == self.longitude.shape[0]):
                raise ValueError(
                    "MapScatter: latitude and longitude must have the same shape "
                    "or be 1D arrays of equal length."
                )

        # ---- plausibility check for swapped lat/lon ----
        lat_abs_max = np.nanmax(np.abs(self.latitude)) if self.latitude.size else 0
        lon_abs_max = np.nanmax(np.abs(self.longitude)) if self.longitude.size else 0
        if lat_abs_max > 90 and lon_abs_max <= 180:
            raise ValueError(
                "MapScatter: latitude values exceed 90°, which suggests you passed "
                "longitude first. Constructor order is (latitude, longitude, data)."
            )

        # ---- plotting defaults ----
        self.marker = 'o'
        self.markersize = 5
        self.linewidths = 1.5
        self.edgecolors = None
        self.alpha = None
        self.vmin = None
        self.vmax = None
        self.label = None

        # Discrete/categorical helper flag (used by renderer)
        self.integer_field = False

        if self.data is None:
            self.color = 'tab:blue'
            self.colorbar = False
        else:
            self.cmap = 'viridis'
            self.colorbar = True


class MapGridded:
    """
    Gridded field on a map (pcolormesh-style).

    Parameters
    ----------
    latitude : array-like
        Either a 2D array of **edges** (ny+1, nx+1) or **centers** (ny, nx).
        For tiled data, may be 3D with tiles in the last dimension.
    longitude : array-like
        Same shape rules as `latitude`.
    data : array-like
        If `latitude/longitude` are centers: shape (ny, nx) or (ny, nx, ntile).
        If they are edges: shape (ny, nx) or (ny, nx, ntile).

    Notes
    -----
    This class validates:
      - latitude/longitude shapes match each other.
      - Either CENTER grids (same shape as data) or EDGE grids (one larger
        in each spatial dimension than data).
      - Latitude values plausibly within [-90, 90]; if not, a helpful error
        suggests swapping the constructor order.
    """

    def __init__(self, latitude, longitude, data):
        self.plottype = 'map_gridded'

        self.latitude = np.asarray(latitude)
        self.longitude = np.asarray(longitude)
        self.data = np.asarray(data)

        # ---- shape checks ----
        if self.latitude.shape != self.longitude.shape:
            raise ValueError(
                "MapGridded: latitude and longitude must have the same shape "
                "(either centers (ny, nx[, t]) or edges (ny+1, nx+1[, t]))."
            )

        lat_shape = self.latitude.shape
        data_shape = self.data.shape

        def _spatial(shape):
            # Return (ny, nx, ntile) with ntile=1 if 2D
            if len(shape) == 2:
                return shape[0], shape[1], 1
            if len(shape) == 3:
                return shape[0], shape[1], shape[2]
            raise ValueError("MapGridded: arrays must be 2D or 3D (tiles in last dim).")

        lat_ny, lat_nx, lat_nt = _spatial(lat_shape)
        dat_ny, dat_nx, dat_nt = _spatial(data_shape)

        # Same tiling or no tiles
        if not (lat_nt == 1 or dat_nt == 1 or lat_nt == dat_nt):
            raise ValueError(
                "MapGridded: tile count mismatch between lat/lon and data "
                f"(lat/lon tiles={lat_nt}, data tiles={dat_nt})."
            )

        centers_ok = (lat_ny == dat_ny and lat_nx == dat_nx)
        edges_ok = (lat_ny == dat_ny + 1 and lat_nx == dat_nx + 1)

        if not (centers_ok or edges_ok):
            raise ValueError(
                "MapGridded: latitude/longitude must be either CENTER grids "
                f"(same size as data: {dat_ny}x{dat_nx}) or EDGE grids "
                f"({dat_ny+1}x{dat_nx+1}). Got lat/lon {lat_ny}x{lat_nx}."
            )

        # ---- plausibility check for swapped lat/lon ----
        lat_abs_max = np.nanmax(np.abs(self.latitude)) if self.latitude.size else 0
        lon_abs_max = np.nanmax(np.abs(self.longitude)) if self.longitude.size else 0
        if lat_abs_max > 90 and lon_abs_max <= 180:
            raise ValueError(
                "MapGridded: latitude values exceed 90°, which suggests you passed "
                "longitude first. Constructor order is (latitude, longitude, data)."
            )

        # ---- plotting defaults ----
        self.cmap = 'viridis'
        # Give a helpful default for pcolormesh; renderer passes through if present
        self.shading = 'auto'

        if self.latitude.ndim == 3:
            # Provide defaults that make tiled plots consistent
            self.vmin = np.nanmin(self.data)
            self.vmax = np.nanmax(self.data)
        else:
            self.vmin = None
            self.vmax = None

        self.alpha = None
        self.colorbar = True


class MapContour:
    """
    Contour lines on a map.

    Parameters
    ----------
    latitude : array-like, shape (ny, nx) or (ny, nx, ntile)
        **Center** grid only (contour expects centers).
    longitude : array-like, same shape as `latitude`
    data : array-like, shape (ny, nx) or (ny, nx, ntile)
        Field values to contour.

    Notes
    -----
    Validates that latitude/longitude **match data shape exactly** (centers).
    Also checks that latitude values plausibly lie within [-90, 90].
    """

    def __init__(self, latitude, longitude, data):
        self.plottype = 'map_contour'

        self.latitude = np.asarray(latitude)
        self.longitude = np.asarray(longitude)
        self.data = np.asarray(data)

        # ---- shape checks (centers only) ----
        if self.latitude.shape != self.longitude.shape or self.latitude.shape != self.data.shape:
            raise ValueError(
                "MapContour: latitude, longitude, and data must have the same shape "
                "(center grid)."
            )

        # ---- plausibility check for swapped lat/lon ----
        lat_abs_max = np.nanmax(np.abs(self.latitude)) if self.latitude.size else 0
        lon_abs_max = np.nanmax(np.abs(self.longitude)) if self.longitude.size else 0
        if lat_abs_max > 90 and lon_abs_max <= 180:
            raise ValueError(
                "MapContour: latitude values exceed 90°, which suggests you passed "
                "longitude first. Constructor order is (latitude, longitude, data)."
            )

        # ---- plotting defaults ----
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


class MapFilledContour:
    """
    Filled contours on a map.

    Parameters
    ----------
    latitude : array-like, shape (ny, nx) or (ny, nx, ntile)
        **Center** grid only (contourf expects centers).
    longitude : array-like, same shape as `latitude`
    data : array-like, shape (ny, nx) or (ny, nx, ntile)
        Field values to contour.

    Notes
    -----
    Validates that latitude/longitude **match data shape exactly** (centers).
    Also checks that latitude values plausibly lie within [-90, 90].
    """

    def __init__(self, latitude, longitude, data):
        self.plottype = 'map_filled_contour'

        self.latitude = np.asarray(latitude)
        self.longitude = np.asarray(longitude)
        self.data = np.asarray(data)

        # ---- shape checks (centers only) ----
        if self.latitude.shape != self.longitude.shape or self.latitude.shape != self.data.shape:
            raise ValueError(
                "MapFilledContour: latitude, longitude, and data must have the same shape "
                "(center grid)."
            )

        # ---- plausibility check for swapped lat/lon ----
        lat_abs_max = np.nanmax(np.abs(self.latitude)) if self.latitude.size else 0
        lon_abs_max = np.nanmax(np.abs(self.longitude)) if self.longitude.size else 0
        if lat_abs_max > 90 and lon_abs_max <= 180:
            raise ValueError(
                "MapFilledContour: latitude values exceed 90°, which suggests you passed "
                "longitude first. Constructor order is (latitude, longitude, data)."
            )

        # ---- plotting defaults ----
        self.levels = None
        self.clabel = False
        self.colors = None
        self.cmap = 'viridis'
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = False
