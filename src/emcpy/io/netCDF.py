# coding: utf-8 -*-

'''
netCDF.py contains utility functions for netCDF files
'''

__all__ = ['variable_exist', 'read_netCDF_var']

import numpy as _np
from netCDF4 import Dataset as _Dataset


def print_variables(filename):
    '''
    prints all available variables in a netCDF file

    Args:
        filename : (str) netCDF filename
    '''
    try:
        nc = _Dataset(filename, 'r')
    except IOError:
        raise IOError(f'Unable to open {filename}')
    print(nc.variables.keys())


def variable_exist(filename, variable_name):
    '''
    Check if a variable exists in a netCDF file

    Args:
        filename : (str) netCDF filename
        variable_name : (str) variable name to check within filename
    Returns:
        True or False if variable is present
    '''

    result = False

    try:
        nc = _Dataset(filename, 'r')
    except IOError:
        raise IOError(f'Unable to open {filename}')

    if variable_name in list(nc.variables.keys()):
        result = True

    try:
        nc.close()
    except IOError:
        raise IOError(f'Unable to close {filename}')

    return result


def read_netCDF_var(filename, variable_name, oneD=False, ftime=-1, flevel=-1):
    '''
    Read a variable from a netCDF file

    Args:
        filename : (str) netCDF filename
        variable_name : (str) variable name to check within filename
        oneD : (bool, optional, default=False) Is variable_name a one-dimensional variable?
        ftime : (int, optional, default=-1) time index range to retrieve data for
        flevel : (int, optional, default=-1) level index range to retrieve data for
    Returns:
        An array of data for variable_name
    '''
    try:
        nc = _Dataset(filename, 'r')
    except IOError:
        raise IOError(f'Unable to open {filename}')

    if not variable_exist(filename, variable_name):
        raise Execption(f'netCDF: variable {variable_name} does not exist in {filename}')

    if oneD:
        var = nc.variables[variable_name][:]
    else:
        if (ftime == -1) and (flevel == -1):
            var = nc.variables[variable_name][:, :]
        elif (ftime == -1) and (flevel != -1):
            var = nc.variables[variable_name][flevel, :, :]
        elif (ftime != -1) and (flevel == -1):
            var = nc.variables[variable_name][ftime, :, :]
        elif (ftime != -1) and (flevel != -1):
            var = nc.variables[variable_name][ftime, flevel, :, :]

    try:
        nc.close()
    except IOError:
        raise IOError(f'Unable to close {filename}')

    result = _np.squeeze(var)
    return result
