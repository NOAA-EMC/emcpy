# coding: utf-8 -*-

'''
utils.py contains handy utility functions
'''

import numpy as _np
import pickle as _pickle
import pandas as _pd
from timeit import default_timer as timer

__all__ = [
    'float10Power', 'roundNumber',
    'pickle', 'unpickle',
    'writeHDF', 'readHDF',
    'EmptyDataFrame',
    'printcolour', 'tictoc'
]


def float10Power(value):
    '''
    Args:
        value: value to get the 10^(exponent)
    Returns:
        The input value expressed as 10^(exponent).
    '''
    if value == 0:
        return 0
    d = _np.log10(abs(value))
    if d >= 0:
        d = _np.ceil(d) - 1.
    else:
        d = _np.floor(d)
    return d


def roundNumber(value):
    '''
    Round the number to the nearest 10th.
    Args:
        value: Number to be rounded
    Returns:
        The input value rounded to nearest 10th

    Examples
    --------
        0.01231 => 0.01
        0.0164  => 0.02
        2.3     => 2.0
        2.8     => 3.0
        6.2     => 10
        59      => 60
    '''

    d = float10Power(value)
    round_value = _np.round(abs(value)/10**d) * 10**d * _np.sign(value)

    return round_value


def pickle(filename, data, mode='wb'):
    '''
    Pickle `data` into a file
    Args:
        filename: (str) filename to pickle to
        data: (object) data to pickle
        mode: (str, optional, default='wb') mode to pickle
    '''
    print(f'pickling ... {filename}')
    try:
        _pickle.dump(data, open(filename, mode))
    except _pickle.PicklingError:
        raise
    return


def unpickle(filename, mode='rb'):
    '''
    Args:
        filename: (str) filename to unpickle to
        mode: (str, optional, default='rb') mode to unpickle
    Returns:
        The unpickled data from filename
    '''
    print(f'unpickling ... {filename}')
    try:
        data = _pickle.load(open(filename, mode))
    except _pickle.UnpicklingError:
        raise
    return data


def writeHDF(filename, variable_name, data, complevel=0, complib=None, fletcher32=False):
    '''
    Args:
        filename: (str) HDF5 filename to write to
        variable_name: (str) name of the variable to write to
        data: (array like) variable data array
        complevel: (int, optional, default=0) compression level
        complib: (str, optional, default=None) compression library to choose from
        fletcher32: (bool, optional, default=False) compression related option
    '''
    print(f'writing ... {filename}')
    try:
        hdf = _pd.HDFStore(filename,
                           complevel=complevel, complib=complib,
                           fletcher32=fletcher32)
        hdf.put(variable_name, data, format='table', append=True)
        hdf.close()
    except RuntimeError:
        raise
    return


def readHDF(filename, variable_name, **kwargs):
    '''
    Args:
        filename: (string) HDF5 filename to read from
        variable_name: (string) name of the variable to read from file
        **kwargs: additional arguments to pandas.read_hdf()
    Returns:
        A Pandas DataFrame of data read from filename for variable_name
    '''
    print(f'reading ... {filename}')
    try:
        data = _pd.read_hdf(filename, variable_name, **kwargs)
    except RuntimeError:
        raise
    return data


def EmptyDataFrame(columns, names, dtype=None):
    '''
    Create an empty Multi-index DataFrame
    Args:
        columns: (list of strings) name of all columns; including indices
        names: (list of strings) name of index columns
    Returns:
        A Multi-index Pandas DataFrame object
    '''

    levels = [[] for i in range(len(names))]
    labels = [[] for i in range(len(names))]
    indices = _pd.MultiIndex(levels=levels, labels=labels, names=names)
    df = _pd.DataFrame(index=indices, columns=columns, dtype=dtype)

    return df


def printcolour(text, colour='red'):
    '''
    Print the input text to stdout in color
    Args:
        text: (str) ascii text
        color: (str, optional, default='red') choice of color for text
    '''

    colours = {
        'default': '\033[1;m',
        'gray': '\033[1;30m',
        'red': '\033[1;31m',
        'green': '\033[1;32m',
        'yellow': '\033[1;33m',
        'blue': '\033[1;34m',
        'magenta': '\033[1;35m',
        'cyan': '\033[1;36m',
        'white': '\033[1;37m',
        'crimson': '\033[1;38m'
    }
    print(colours[colour] + text + colours['default'])
    return


printcolor = printcolour


def tic():
    return timer()

def toc(tic=tic, string=""):
    toc = timer()
    time = toc-tic
    hrs = str(int(time/3600)).zfill(2)
    mins = str(int(time%3600/60)).zfill(2)
    secs = str(int(time%3600%60)).zfill(2)
    print("%sTotal elapsed time: (%1.2fs), %s:%s:%s"%(string, time, hrs, mins, secs))
