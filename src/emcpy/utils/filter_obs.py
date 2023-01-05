import numpy as _np


def filter_obs(
    code,
    codes,
    errorinv,
    lat,
    lon,
    pressure,
    use=1,
    p_max=1050.0,
    p_min=100.0,
    lat_max=90.0,
    lat_min=0.0,
    lon_max=360.0,
    lon_min=0.0,
    error_max=40.0,
    error_min=0.000001,
):
    """
    Create the bool array used to filter by. Considers obs filtered by the use flag,
    max/min pressure, latitude, longitude, and errors along with filtering by bufr
    code (e.g., 187 or 287).

    netCDF Args:
        code     : (array int) bufr ob codes from netCDF file <Observation_Type>
        codes    : (array int) bufr ob codes to filter by, see link
                   https://emc.ncep.noaa.gov/mmb/data_processing/prepbufr.doc/table_2.htm
        errorinv : (array float) from netCDF file <Errinv_Final>
        lat      : (array float) from netCDF file <Latitude>
        lon      : (array float) from netCDF file <Longitude>
        pressure : (array float) from netCDF file <Pressure>

     Filtering Args:
        use      : (int)   use flag for observation 1=used
        p_max    : (float) maximum pressure (mb) for including observation in calculations
        p_min    : (float) minimum pressure (mb) for including observation in calculations
        lat_max  : (float) maximum latitude (deg N) for including observation in calculations
        lat_min  : (float) minimum latitude (deg N) for including observation in calculations
        lon_max  : (float) maximum latitude (deg E) for including observation in calculations
        lon_min  : (float) minimum latitude (deg E) for including observation in calculations
        error_max: (float) maximum error standard deviation for including observation in calculations
        error_min: (float) minimum error standard deviation for including observation in calculations

    Returns:
        used : (array bool) observations to consider after all filtering
    """
    used = code == codes[0]  # initialize used
    for cd in codes:
        used = _np.logical_or(used, code == cd)  # loop over all codes provided

    error_min_inv = 1.0 / error_min
    error_max_inv = 1.0 / error_max
    # consider where use flag==1 and bound by error/lat/lon/pres
    used = _np.logical_and(used, use == 1)
    used = _np.logical_and(used, _np.logical_and(errorinv <= error_min_inv, errorinv >= error_max_inv))
    used = _np.logical_and(used, _np.logical_and(lat >= lat_min, lat <= lat_max))
    used = _np.logical_and(used, _np.logical_and(lon >= lon_min, lon <= lon_max))
    used = _np.logical_and(used, _np.logical_and(pressure >= p_min, pressure <= p_max))

    return used
