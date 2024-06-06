"""
Create a custom map domain
--------------------------

EMCPy's map domain includes a feature
to create a custom dictionary with specified
lat and lon inputs to create a specific map
domain. This is helpful for users who want to
look at a specific domain that is not included in EMCPy.
"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.map_tools import Domain, MapProjection


def main():
    # Create dictionary with information pertaining to
    # Africa domain
    africa_dict = {
        "extent": (-20, 55, -35, 35),
        "xticks": (-15, 0, 15, 30, 45),
        "yticks": (-30, -15, 0, 15, 30),
        "cenlon": 20.,
        "cenlat": -10.
    }

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.projection = 'plcarr'
    # Add data as a tuple with 'custom' as domain name
    # and `africa_dict` as dictionary
    plot1.domain = ('custom', africa_dict)
    plot1.add_map_features(['coastline'])
    plot1.add_xlabel(xlabel='longitude')
    plot1.add_ylabel(ylabel='latitude')
    plot1.add_title(label='Custom Africa Domain', loc='center',
                    fontsize=12)

    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
