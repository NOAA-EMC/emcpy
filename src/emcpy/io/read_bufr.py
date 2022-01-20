import ncepbufr
import numpy as np
import pandas as pd
import yaml
import os
from pathlib import Path
import yaml


class ReadBUFR:

    def __init__(self, input_yaml):
        """
        Initialize a BUFR file object.

        Args:
            input_yaml : (str) path to input yaml file
        """

        with open(input_yaml) as yamlfile:
            input_yaml = yaml.load(yamlfile, Loader=yaml.FullLoader)

        if 'radiance' in [*input_yaml.keys()]:
            self.bufr_file = input_yaml['radiance']['obsdatain']
            self.inputs = input_yaml['radiance']['inputs']
            self.variables = input_yaml['radiance']['variables']

    def read_radiance(self):
        """
        Open and read bufr file containing radiance data.
        """
        # Get BUFR codes
        _emcpy_dir = Path(__file__).parent.parent.absolute()
        var_yaml = os.path.join(_emcpy_dir,
                                'cfg',
                                'bufr_codes.yaml')

        # Get input sensor, satellite, channels
        sensor = self.inputs['sensor']
        satellite = self.inputs['satellite']
        channels = self._channel_list(self.inputs['channels'])

        # read YAML into dictionary
        with open(var_yaml) as yamlfile:
            bufr_dict = yaml.load(yamlfile, Loader=yaml.FullLoader)

        sensor_id = bufr_dict['sensor'][sensor]
        sat_id = bufr_dict['satellite'][satellite]

        # Create output dictionary
        df_dict = {}
        for key in self.variables.keys():
            df_dict[key] = []

        # Open BUFR and store into dataframe
        bufr = ncepbufr.open(self.bufr_file)
        while bufr.advance() == 0:
            while bufr.load_subset() == 0:
                said = bufr.read_subset('SAID', rep=True).squeeze()
                siid = bufr.read_subset('SIID', rep=True).squeeze()

                # Grab only data from input sensor and satellite
                if sat_id == said and sensor_id == siid:
                    # Loop through variables
                    for var in self.variables.keys():
                        if var == 'timestamp':
                            mnemonic = ' '.join(self.variables[var]['datetime'].values())
                            dt_hdr = bufr.read_subset(mnemonic).squeeze()
                            data = '%04i%02i%02i%02i%02i' % tuple(dt_hdr)
                        else:
                            mnemonic = self.variables[var]['mnemonic']
                            data = bufr.read_subset(mnemonic).squeeze()

                        for k, chan in enumerate(channels):
                            if type(data) is list:
                                df_dict[var].append(float(data[k]))
                            elif var == 'channelNumber':
                                df_dict[var].append(int(chan))
                            else:
                                df_dict[var].append(data)
        bufr.close()

        df = pd.DataFrame(df_dict)

        return df

    def read_aircraft(self):
        """
        Open and read bufr file for aircraft data.
        """

        # Create output dictionary
        df_dict = {}
        for key in self.variables.keys():
            df_dict[key] = []

        # Open BUFR and store into dataframe
        bufr = ncepbufr.open(self.bufr_file)
        while bufr.advance() == 0:
            while bufr.load_subset() == 0:
                for var in self.variables.keys():
                    if var == 'timestamp':
                        mnemonic = ' '.join(self.variables[var]['datetime'].values())
                        dt_hdr = bufr.read_subset(mnemonic).squeeze()
                        data = '%04i%02i%02i%02i%02i' % tuple(dt_hdr)
                    else:
                        mnemonic = self.variables[var]['mnemonic']
                        data = bufr.read_subset(mnemonic).squeeze()

                    df_dict[var].append(data)

        bufr.close()

        df = pd.DataFrame(df_dict)

        return df

    def _channel_list(self, input_chans):
        """
        Create of list of channels from a str input that could contain
        a '-' or ',' characters

        Args:
            input_chans: (str) input string
        """
        chan_groups = [x.strip() for x in input_chans.split(',')]
        channels = []

        for c in chan_groups:
            if '-' in c:
                comps = c.split('-')
                x = range(int(comps[0]), int(comps[1])+1)
                channels.extend(x)
            else:
                channels.extend([int(c)])

        return channels
