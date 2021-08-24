import numpy as np

vardict = {
    'temperature': {
        'name': 'temperature',
        'short name': 't',
        'variable type': 'conventional',
        'units': 'K',
        'range': [220, 320],
        'contour interval': 5,
        'diff range': [-5, 5],
        'diff contour interval': 0.5,
        'cmap': 'rainbow'
    },
    'specific humidity': {
        'name': 'specific humidity',
        'short name': 'q',
        'variable type': 'conventional',
        'units': 'kg/kg',
        'range': [0, 0.030],
        'contour interval': 0.0025,
        'diff range': [-0.005, 0.005],
        'diff contour interval': 0.001,
        'cmap': 'YlGnBu'
    },
    'u': {
        'name': 'zonal wind',
        'short name': 'u',
        'variable type': 'conventional',
        'units': 'm/s',
        'range': [-50, 50],
        'contour interval': 5,
        'diff range': [-5, 5],
        'diff contour interval': 0.5,
        'cmap': 'PuOr'
    },
    'v': {
        'name': 'meridional wind',
        'short name': 'v',
        'variable type': 'conventional',
        'units': 'm/s',
        'range': [-50, 50],
        'contour interval': 5,
        'diff range': [-5, 5],
        'diff contour interval': 0.5,
        'cmap': 'PuOr'
    },
    'wind speed': {
        'name': 'wind speed',
        'short name': 'wndspd',
        'variable type': 'conventional',
        'units': 'm/s',
        'range': [0, 75],
        'contour interval': 5,
        'diff range': [-5, 5],
        'diff contour interval': 0.5,
        'cmap': 'viridis'
    },
    'brightness temperature': {
        'name': 'brightness temperature',
        'short name': 'bt',
        'variable type': 'radiance',
        'units': 'K',
        'range': [220, 320],
        'contour interval': 5,
        'diff range': [-5, 5],
        'diff contour interval': 0.5,
        'cmap': 'rainbow'
    }
}


class VariableSpecs:

    def __init__(self, variable, eval_type):

        if variable not in vardict.keys():
            raise ValueError(f'{variable} is not a valid variable. ' +
                             'Current variables supported are:\n' +
                             f'{" | ".join(vardict.keys())}')

        if eval_type not in ['magnitude', 'diff']:
            raise ValueError(f'{eval_type} is not a evaluation ' +
                             'type. Current options supported are:\n' +
                             'magnitude | diff ')

        self.eval_type = eval_type
        self.name = vardict[variable].get('name', 'VariableName')
        self.sname = vardict[variable].get('short name', 'VName')
        self.type = vardict[variable].get('variable type', 'VariableType')
        self.units = vardict[variable].get('units', 'VariableUnits')

        self.range = vardict[variable].get('diff range', [-1, 1]) if \
            eval_type in ['diff'] else vardict[variable].get('range', [-1, 1])
        self.contour_int = vardict[variable]['diff contour interval'] \
            if eval_type in ['diff'] else vardict[variable]['contour interval']
        self.contours = np.arange(self.range[0],
                                  self.range[-1]+self.contour_int,
                                  self.contour_int)
        self.cmap = 'coolwarm' if eval_type in ['diff'] else \
            vardict[variable]['cmap']
        self.vmin = vardict[variable]['diff range'][0] if eval_type in \
            ['diff'] else vardict[variable]['range'][0]
        self.vmax = vardict[variable]['diff range'][-1] if eval_type in \
            ['diff'] else vardict[variable]['range'][-1]
