import numpy as np

__all__ = ['MapScatter', 'MapGridded', 'MapContour', 'MapFilledContour']


def _nanabsmax(a) -> float:
    """Return nan-robust max(|a|). For empty/all-nan, return -inf."""
    try:
        return float(np.nanmax(np.abs(a)))
    except ValueError:
        # Raised when array is empty; treat as "no signal"
        return float("-inf")


def _assert_latlon_not_swapped(latitude, longitude, context: str) -> None:
    """
    Heuristic check that helps catch swapped (lon, lat) inputs.

    If the latitude magnitude exceeds 90° while the longitude magnitude is
    within 180°, we assume the user passed (lon, lat) and raise a helpful error.

    Parameters
    ----------
    latitude, longitude : array-like
        Arrays to test (not modified).
    context : str
        Prefix for the error message (e.g., 'MapScatter', 'MapGridded', ...).
    """
    lat_abs_max = _nanabsmax(latitude)
    lon_abs_max = _nanabsmax(longitude)

    # Only trigger when we have a meaningful signal
    if lat_abs_max > 90 and lon_abs_max <= 180:
        raise ValueError(
            f"{context}: latitude values exceed 90°, which suggests you passed "
            f"longitude first. Constructor order is (latitude, longitude, data)."
        )


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
        _assert_latlon_not_swapped(self.latitude, self.longitude, "MapScatter")

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
        - 1D **edges** of length ny+1 (paired with 1D longitude edges), or
        - 2D/3D arrays (ny[, nx[, ntile]]) of **centers** or **edges**.
    longitude : array-like
        Same shape rules as `latitude`.
    data : array-like
        - If latitude/longitude are 1D edges: shape (ny, nx).
        - If latitude/longitude are 2D/3D: either centers (ny, nx[, ntile])
          or edges (ny+1, nx+1[, ntile]).

    Notes
    -----
    - Validates that latitude/longitude shapes match (for 2D/3D), or are both 1D.
    - Supports tiled data when lat/lon are 2D/3D with tiles in the last dim.
    - Latitude plausibility check helps catch swapped (lon, lat) order.
    """

    def __init__(self, latitude, longitude, data):

        self.plottype = 'map_gridded'

        lat = np.asarray(latitude)
        lon = np.asarray(longitude)
        Z = np.asarray(data)

        # ---- accept 1D edge arrays (lon, lat) with 2D centers Z ----
        if lat.ndim == 1 and lon.ndim == 1:
            ny = lat.size - 1
            nx = lon.size - 1
            if ny <= 0 or nx <= 0:
                raise ValueError("MapGridded: 1D edge arrays must have length >= 2.")

            if Z.ndim != 2 or Z.shape != (ny, nx):
                raise ValueError(
                    "MapGridded: with 1D edge latitude/longitude, "
                    "data must be 2D with shape (len(lat)-1, len(lon)-1)."
                )

            self.latitude = lat
            self.longitude = lon
            self.data = Z

        else:
            # ---- 2D/3D center/edge grids (tiles in last dim allowed) ----
            if lat.shape != lon.shape:
                raise ValueError(
                    "MapGridded: latitude and longitude must have the same shape "
                    "(either centers (ny, nx[, t]) or edges (ny+1, nx+1[, t]))."
                )
            if lat.ndim not in (2, 3):
                raise ValueError("MapGridded: latitude/longitude must be 2D or 3D.")

            # Extract spatial/tile dims
            lat_ny, lat_nx = lat.shape[0], lat.shape[1]
            lat_nt = 1 if lat.ndim == 2 else lat.shape[2]

            if Z.ndim == 2:
                dat_ny, dat_nx, dat_nt = Z.shape[0], Z.shape[1], 1
            elif Z.ndim == 3:
                dat_ny, dat_nx, dat_nt = Z.shape
            else:
                raise ValueError("MapGridded: data must be 2D or 3D.")

            # Same tiling (or broadcastable)
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

            self.latitude = lat
            self.longitude = lon
            self.data = Z

        # ---- plausibility check for swapped inputs ----
        _assert_latlon_not_swapped(self.latitude, self.longitude, "MapGridded")

        # ---- plotting defaults ----
        self.cmap = 'viridis'
        self.shading = 'auto'     # good default for pcolormesh
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = True
        self.integer_field = False


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
        _assert_latlon_not_swapped(self.latitude, self.longitude, "MapContour")

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
        _assert_latlon_not_swapped(self.latitude, self.longitude, "MapFilledContour")

        # ---- plotting defaults ----
        self.levels = None
        self.clabel = False
        self.colors = None
        self.cmap = 'viridis'
        self.vmin = None
        self.vmax = None
        self.alpha = None
        self.colorbar = False
