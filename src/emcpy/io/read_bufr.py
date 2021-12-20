import ncepbufr
import numpy as np
import pandas as pd
import yaml
import os
from pathlib import Path


class ReadBUFR:

    def __init__(self, file):
        """
        Initialize a BUFR file object.

        Args:
            file : (str) path to prep BUFR file
        """

        self.file = file

    def read_radiance(self, sensor, satellite):
        """
        Open and grab all data from BUFR file that falls within sensor
        and satellite inputs.

        Args:
            sensor : (str) string of sensor
            satellite : (str) string of satellite
        Returns:
            df : pandas dataframe with information
        """
        self.hdstr1 = 'SAID SIID FOVN YEAR MNTH DAYS HOUR MINU SECO CLAT CLON CLATH CLONH HOLS'
        self.hdstr2 = 'SAZA SOZA BEARAZ SOLAZI'

        df_dict = {
            'datetime': [],
            'channel': [],
            'latitude': [],
            'longitude': [],
            'satellite_zenith_angle': [],
            'solar_zenith_angle': [],
            'bearing_or_azimuth': [],
            'solar_azimuth': [],
            'brightness temperature': []
        }

        _emcpy_dir = Path(__file__).parent.parent.absolute()
        var_yaml = os.path.join(_emcpy_dir,
                                'cfg',
                                'bufr_codes.yaml')

        # read YAML into dictionary
        with open(var_yaml) as yamlfile:
            bufr_dict = yaml.load(yamlfile, Loader=yaml.FullLoader)

        sensor_id = bufr_dict['sensor'][sensor]
        sat_id = bufr_dict['satellite'][satellite]

        bufr = ncepbufr.open(self.file)
        bufr.print_table()
        while bufr.advance() == 0:
            while bufr.load_subset() == 0:
                hdr1 = bufr.read_subset(self.hdstr1).squeeze()
                if sat_id == int(hdr1[0]) and sensor_id == int(hdr1[1]):
                    hdr2 = bufr.read_subset(self.hdstr2).squeeze()

                    str_datetime = '%04i%02i%02i%02i%02i%02i' % tuple(hdr1[3:9])

                    channels = bufr.read_subset('CHNM', rep=True).squeeze()  # channels
                    tb = bufr.read_subset('TMBR', rep=True).squeeze()  # brightness temp

                    for k, chan in enumerate(channels):
                        df_dict['datetime'].append(str_datetime)
                        df_dict['latitude'].append(hdr1[9])
                        df_dict['longitude'].append(hdr1[10])
                        df_dict['satellite_zenith_angle'].append(hdr2[0])
                        df_dict['solar_zenith_angle'].append(hdr2[1])
                        df_dict['bearing_or_azimuth'].append(hdr2[2])
                        df_dict['solar_azimuth'].append(hdr2[3])
                        df_dict['channel'].append(int(chan))
                        df_dict['brightness temperature'].append(tb[k])

        bufr.close()

        df = pd.DataFrame(df_dict)
        df.set_index('channel', inplace=True)

        return df
