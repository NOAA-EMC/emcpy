import numpy as np
import yaml
from pathlib import Path
import os


class VariableSpecs:

    def __init__(self, variable, eval_type, var_yaml=None):

        # find default YAML if not specified
        if not var_yaml:
            _emcpy_dir = Path(__file__).parent.parent.absolute()
            var_yaml = os.path.join(_emcpy_dir,
                                    'cfg',
                                    'gdas_var_defaults.yaml')

        # read YAML into dictionary
        with open(var_yaml) as yamlfile:
            vardict = yaml.load(yamlfile, Loader=yaml.FullLoader)

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
