__all__ = ['K_to_C', 'K_to_F', 'C_to_K', 'C_to_F', 'F_to_C',
           'mps_to_MPH', 'MPH_to_mps', 'mm_to_inches', 'inches_to_mm']


# Temperature
def K_to_C(K):
    """
    Convert Kelvin to Celsius

    Args:
        K : (float, or array of floats) temperature in kelvin
    Returns:
        The input temperature in degrees celsius
    """
    return K - 273.15


def K_to_F(K):
    """
    Convert Kelvin to Fahrenheit

    Args:
        K : (float, or array of floats) temperature in kelvin
    Returns:
        The input temperature in degrees fahrenheit
    """
    return (K-273.15)*9/5.+32


def C_to_K(T_C):
    """
    Convert Celsius to Kelvin

    Args:
        T_C : (float, or array of floats) temperature in degrees celsius
    Returns:
        The input temperature in kelvin
    """
    return T_C + 273.15


def C_to_F(C):
    """
    Convert Celsius to Fahrenheit

    Args:
        C : (float, or array of floats) temperature in degrees celsius
    Returns:
        The input temperature in degrees fahrenheit
    """
    return C*9/5.+32


def F_to_C(F):
    """
    Convert Fahrenheit to Celsius

    Args:
        F : (float, or array of floats) temperature in degrees fahrenheit
    Returns:
        The input temperature in degrees celsius
    """
    return (F-32) * 5/9


# Wind
def mps_to_MPH(mps):
    """
    Convert meters per second to miles per hour

    Args:
        mps : (float, or array of floats) speed in meters per second
    Returns:
        The input speed in miles per hour
    """
    return mps * 2.2369


def MPH_to_mps(MPH):
    """
    Convert miles per hour to meters per second

    Args:
        MPH : (float, or array of floats) speed in miles per hour
    Returns:
        The input speed in meters per second
    """
    return MPH / 2.2369


# Precipitation
def mm_to_inches(mm):
    """
    Convert millimeters to inches

    Args:
        mm : (float, or array of floats) length in millimeters
    Returns:
        The input length in inches
    """
    return mm / 25.4


def inches_to_mm(inches):
    """
    Convert inches to millimeters

    Args:
        inches : (float, or array of floats) length in inches
    Returns:
        The input length in millimeters
    """
    return inches * 25.4
