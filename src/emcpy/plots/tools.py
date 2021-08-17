class ColorbarPreset:
    """
    Class that has pre-determined vmin, vmax,
    and cmap values depending on the variable
    and evaluation type.
    """
    def __init__(self, variable, eval_type):
        """
        Class constructor.

        Args:
            variable : (str) variable of interest
            eval_type : (str) evaluation type
        """

        cbar_d = {
            'brightness temperature': {
                'diff': {
                    'vmax': 5,
                    'vmin': -5,
                    'cmap': 'coolwarm'
                },
                'magnitude': {
                    'vmax': 320,
                    'vmin': 220,
                    'cmap': 'rainbow'
                }
            },
            'specific humidity': {
                'diff': {
                    'vmax': 0.005,
                    'vmin': -0.005,
                    'cmap': 'coolwarm'
                },
                'magnitude': {
                    'vmax': 0.025,
                    'vmin': 0,
                    'cmap': 'YlGnBu'
                }
            },
            'temperature': {
                'diff': {
                    'vmax': 5,
                    'vmin': -5,
                    'cmap': 'coolwarm'
                },
                'magnitude': {
                    'vmax': 320,
                    'vmin': 220,
                    'cmap': 'rainbow'}
            },
            'wind speed': {
                'diff': {
                    'vmax': 5,
                    'vmin': -5,
                    'cmap': 'coolwarm'
                },
                'magnitude': {
                    'vmax': 75,
                    'vmin': 0,
                    'cmap': 'viridis'
                },
            },
            'wind': {
                'diff': {
                    'vmax': 5,
                    'vmin': -5,
                    'cmap': 'coolwarm'
                },
                'magnitude': {
                    'vmax': 50,
                    'vmin': -50,
                    'cmap': 'viridis'
                }
            }
        }

        variable = 'wind' if variable in ['uwind', 'vwind', 'ugrd', 'vgrd'] \
                   else variable

        try:
            self.vmin = cbar_d[variable][eval_type]['vmin']
            self.vmax = cbar_d[variable][eval_type]['vmax']
            self.cbar = cbar_d[variable][eval_type]['cmap']

        except KeyError:
            if variable not in cbar_d.keys():
                raise TypeError(f'{variable} is not a valid variable.' +
                                'Current variables supported are:\n' +
                                f'{" | ".join(cbar_d.keys())}')
            else:
                raise TypeError(f'{eval_type} is not a valid evaluation' +
                                'type. Current options supported are:\n' +
                                f'{" | ".join(cbar_d[variable].keys())}')
