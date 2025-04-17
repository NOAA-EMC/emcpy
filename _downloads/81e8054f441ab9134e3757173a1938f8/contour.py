"""
Contour
-------

Below is an example of how to plot a contour
plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import ContourPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create contourf plot

    # Grab sample data
    x, y, z = _getContourData()

    # Create contour plot object
    cp = ContourPlot(x, y, z)
    cp.linestyles = '--'
    cp.colors = 'green'

    # Create plot and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [cp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Contour Plot')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


def _getContourData():
    # Generate test data for contour plots

    x = np.linspace(-3, 15, 50).reshape(1, -1)
    y = np.linspace(-3, 15, 20).reshape(-1, 1)
    z = np.cos(x)*2 - np.sin(y)*2

    x, y = x.flatten(), y.flatten()

    return x, y, z


if __name__ == '__main__':
    main()
