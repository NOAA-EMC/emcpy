"""
Creating a simple histogram
---------------------------

Below is an example of how to plot a basic
histogram plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import Histogram
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Generate test data for histogram plots
    mu = 100  # mean of distribution
    sigma = 15  # standard deviation of distribution
    data = mu + sigma * np.random.randn(437)

    # Create histogram object
    hst = Histogram(data)
    hst.color = 'tab:green'
    hst.alpha = 0.7
    hst.label = 'data'

    # Create histogram plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [hst]
    plot1.add_title(label='Test Histogram Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_legend()

    # Create figure and save as png
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
