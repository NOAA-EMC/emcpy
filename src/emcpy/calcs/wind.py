import numpy as np

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
        u : (array like) u (easterly) wind component
        v : (array like) v (northerly) wind component
        direction: (bool, optional, default=False)
    Returns
    -------
        wspd: (numpy array) wind speed
        wdir: (numpy array) wind direction (if direction=True)
    """
    u = np.array(u)
    v = np.array(v)

    wdir = (270 - np.rad2deg(np.arctan2(v, u))) % 360
    wspd = np.sqrt(u * u + v * v)

    return wspd, wdir if direction else wspd


def spddir_to_uv(wspd, wdir):
    """
    Calculate the u and v wind components from wind speed and direction.
    Parameters
    ----------
        wspd : (array like) wind speed
        wdir : (array like) wind direction in degrees
    Returns
    -------
        u : (numpy array) eastward wind component
        v : (numpy array) northward wind component
    """
    wspd = np.array(wspd, dtype=float)
    wdir = np.array(wdir, dtype=float)

    rad = 4.0 * np.arctan(1) / 180.
    u = -wspd * np.sin(rad * wdir)
    v = -wspd * np.cos(rad * wdir)

    # If the speed is zero, then u and v should be set to zero (not NaN)
    if wspd == 0:
        u = float(0)
        v = float(0)

    return u, v
