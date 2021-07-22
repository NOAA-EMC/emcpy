# coding: utf-8 -*-

'''
netCDF.py contains utility functions for netCDF files
'''

__all__ = ['variable_exist', 'read_netCDF_var']

import numpy as _np
from netCDF4 import Dataset as _Dataset


def variable_exist(fname, vname, debug=False):
    '''
    Check if a variable in a file exists
    '''

    result = False

    try:
        nc = _Dataset(fname, 'r')
    except IOError:
        raise IOError('Unable to open %s' % fname)

    if (vname in list(nc.variables.keys())):
        result = True

    try:
        nc.close()
    except IOError:
        raise IOError('Unable to close %s' % fname)

    return result


def read_netCDF_var(fname, vname, oneD=False, ftime=-1, flevel=-1):
    '''
    Read a variable from a netCDF file
    '''
    try:
        nc = _Dataset(fname, 'r')
    except IOError:
        raise IOError('Unable to open %s' % fname)

    if (not variable_exist(fname, vname)):
        raise Execption('variable %s does not exist in %s') % (vname, fname)

    if (oneD):
        var = nc.variables[vname][:]
    else:
        if ((ftime == -1) and (flevel == -1)):
            var = nc.variables[vname][:, :]
        elif ((ftime == -1) and (flevel != -1)):
            var = nc.variables[vname][flevel, :, :]
        elif ((ftime != -1) and (flevel == -1)):
            var = nc.variables[vname][ftime, :, :]
        elif ((ftime != -1) and (flevel != -1)):
            var = nc.variables[vname][ftime, flevel, :, :]

    try:
        nc.close()
    except IOError:
        raise IOError('Unable to close %s' % fname)

    return _np.squeeze(var)
