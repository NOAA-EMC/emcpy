__all__ = ['K_to_C', 'K_to_F', 'C_to_K', 'C_to_F', 'F_to_C',
           'mps_to_MPH', 'MPH_to_mps', 'mm_to_inches', 'inches_to_mm']


# Temperature
def K_to_C(K):
    """
    Convert Kelvin to Celsius

    Parameters
    ----------
        K : temperature in kelvin
    Returns
    -------
        C : temperature in degrees celsius
    """
    return K - 273.15


def K_to_F(K):
    """
    Convert Kelvin to Fahrenheit

    Parameters
    ----------
        K : temperature in kelvin
    Returns
    -------
        F : temperature in degrees fahrenheit
    """
    return (K-273.15)*9/5.+32


def C_to_K(T_C):
    """
    Convert Celsius to Kelvin

    Parameters
    ----------
        T_C : temperature in degrees celsius
    Returns
    -------
        K : temperature in kelvin
    """
    return T_C + 273.15


def C_to_F(C):
    """
    Convert Celsius to Fahrenheit

    Parameters
    ----------
        C : temperature in degrees celsius
    Returns
    -------
        F : temperature in degrees fahrenheit
    """
    return C*9/5.+32


def F_to_C(F):
    """
    Convert Fahrenheit to Celsius

    Parameters
    ----------
        F : temperature in degrees fahrenheit
    Returns
    -------
        C : temperature in degrees celsius
    """
    return (F-32) * 5/9


# Wind
def mps_to_MPH(mps):
    """
    Convert meters per second to miles per hour

    Parameters
    ----------
        mps : speed in meters per second
    Returns
    -------
        MPH : speed in miles per hour
    """
    return mps * 2.2369


def MPH_to_mps(MPH):
    """
    Convert miles per hour to meters per second

    Parameters
    ----------
        MPH : speed in miles per hour
    Returns
    -------
        mps : speed in meters per second
    """
    return MPH / 2.2369


# Precipitation
def mm_to_inches(mm):
    """
    Convert millimeters to inches

    Parameters
    ----------
        mm : length in millimeters
    Returns
    -------
        inches : length in inches
    """
    return mm * 0.0394


def inches_to_mm(inches):
    """
    Convert millimeters to inches

    Parameters
    ----------
        inches : length in inches
    Returns
    -------
        mm : length in millimeters
    """
    return inches / 0.0394
