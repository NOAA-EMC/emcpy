import numpy as _np

__all__ = ['uv_to_spddir', 'spddir_to_uv']


def uv_to_spddir(u, v, direction=False):
    """
    Calculates the wind speed from u and v components.
    Will calculate direction as well if parameter direction = True.

    Takes into account the wind direction coordinates is different than
    the trig unit circle coordinate. If the wind direction is 360,
    then return zero.
    Parameters
    ----------
        u, v: array_like
        u (easterly) and v (northerly) wind component.
        direction: boolean (optional)
    Returns
    -------
        Wind speed (and direction if direction=True)
    """
    u = _np.array(u)
    v = _np.array(v)

    wdir = (270 - _np.rad2deg(_np.arctan2(v, u))) % 360
    wspd = _np.sqrt(u * u + v * v)

    return wspd, wdir if direction else wspd


def spddir_to_uv(wspd, wdir):
    """
    Calculate the u and v wind components from wind speed and direction.
    Parameters
    ----------
        wspd, wdir : array_like
        Arrays of wind speed and wind direction (in degrees)
    Returns
    -------
        u and v wind components
    """
    wspd = _np.array(wspd, dtype=float)
    wdir = _np.array(wdir, dtype=float)

    rad = 4.0 * _np.arctan(1) / 180.
    u = -wspd * _np.sin(rad * wdir)
    v = -wspd * _np.cos(rad * wdir)

    # If the speed is zero, then u and v should be set to zero (not NaN)
    if wspd == 0:
        u = float(0)
        v = float(0)

    return u, v
