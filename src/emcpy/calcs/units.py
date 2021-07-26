__all__ = ['K_to_C', 'K_to_F', 'C_to_K', 'C_to_F', 'F_to_C', 'mps_to_MPH',
           'mm_to_inches']

# Temperature
def K_to_C(K):
    """
    K_to_C : Convert Kelvin to Celsius

    K_to_C(K)

    INPUT:
      K - temperature in kelvin
    OUTPUT:
      C - temperature in degrees celsius
    """
    return K - 273.15


def K_to_F(K):
    """
    K_to_F : Convert Kelvin to Fahrenheit

    K_to_F(K)

    INPUT:
      K - temperature in kelvin
    OUTPUT:
      F - temperature in degrees fahrenheit
    """
    return (K-273.15)*9/5.+32


def C_to_K(T_C):
    """
    C_to_K : Convert Celsius to Kelvin

    C_to_K(T_C)

    INPUT:
      T_C - temperature in degrees celsius
    OUTPUT:
      K - temperature in kelvin
    """
    return T_C + 273.15


def C_to_F(C):
    """
    C_to_F : Convert Celsius to Fahrenheit

    C_to_F(K)

    INPUT:
      C - temperature in degrees celsius
    OUTPUT:
      F - temperature in degrees fahrenheit
    """
    return C*9/5.+32


def F_to_C(F):
    """
    F_to_C : Convert Fahrenheit to Celsius

    F_to_C(F)

    INPUT:
      F - temperature in degrees fahrenheit
    OUTPUT:
      C - temperature in degrees celsius
    """
    return (F-32) * 5/9


# Wind
def mps_to_MPH(mps):
    """
    mps_to_MPH : Convert meters per second to miles per hour

    mps_to_MPH(mps)

    INPUT:
      mps - speed in meters per second
    OUTPUT:
      MPH - speed in miles per hour
    """
    return mps * 2.2369


# Precipitation
def mm_to_inches(mm):
    """
    mm_to_inches : Convert millimeters to inches

    mm_to_inches(mm)

    INPUT:
      mm - length in millimeters
    OUTPUT:
      inches - length in inches
    """
    return mm * 0.0394
