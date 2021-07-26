import emcpy.calcs.units


def test_convert_units_temp():
    # start with celsius
    deg_C = 0
    # test if it converts to fahrenheit properly
    deg_F = emcpy.calcs.units.C_to_F(deg_C)
    assert deg_F == 32.
    # test if it converts to kelvin properly
    kelvin = emcpy.calcs.units.C_to_K(deg_C)
    assert kelvin == 273.15
    # convert F to C
    assert emcpy.calcs.units.F_to_C(deg_F) == deg_C
    # convert K back to C
    assert emcpy.calcs.units.K_to_C(kelvin) == deg_C
    # convert K to F
    assert emcpy.calcs.units.K_to_F(kelvin) == deg_F


def test_convert_units_winds():
    # convert m/s to miles per hour
    assert emcpy.calcs.units.mps_to_MPH(10.0) == 22.369


def test_convert_units_rainfall():
    # convert mm to inches
    assert emcpy.calcs.units.mm_to_inches(100) == 3.94
