"""
Histogram
---------

Below is an example of how to plot a histogram
using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import Histogram
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create histogram plot

    # Grab sample data
    data = _getHistData()

    # Create histogram object
    hst1 = Histogram(data)
    hst1.color = 'tab:green'
    hst1.label = 'data'

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [hst1]
    plot1.add_title(label='Histogram Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_legend(loc='upper right')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


def _getHistData():
    # Generate test data for histogram plots

    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    data = mu + sigma * np.random.randn(437)

    return data


if __name__ == '__main__':
    main()
