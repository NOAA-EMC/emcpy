"""
Creating a simple scatter plot
------------------------------

Below is an example of how to plot a basic
scatter plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import Scatter
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create test data
    rng = np.random.RandomState(0)
    x = rng.randn(100)
    y = rng.randn(100)

    # Create Scatter object
    sctr1 = Scatter(x, y)

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [sctr1]
    plot1.add_title(label='Test Scatter Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
