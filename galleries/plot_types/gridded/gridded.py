"""
Gridded
-------

Below is an example of how to plot a gridded
plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt
from scipy.ndimage import gaussian_filter

from emcpy.plots.plots import GriddedPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create gridded plot

    # Grab sample data
    x, y, z = _getGriddedData()

    # Create gridded object
    gp = GriddedPlot(x, y, z)
    gp.cmap = 'plasma'

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [gp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Gridded Plot')
    plot1.add_colorbar(orientation='vertical')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


def _getGriddedData():
    # Generate test data for gridded data

    x = np.linspace(0, 1, 51)
    y = np.linspace(0, 1, 51)
    r = np.random.RandomState(25)
    z = gaussian_filter(r.random_sample([50, 50]), sigma=5, mode='wrap')

    return x, y, z


if __name__ == '__main__':
    main()
