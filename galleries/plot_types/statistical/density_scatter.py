"""
Density Scatter Plot
--------------------

The following example shows how to create
a density scatter plot.
"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import Scatter
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create test data
    x = np.random.normal(size=1000)
    y = x * 10 + np.random.normal(size=1000)

    # Create Scatter object
    sctr1 = Scatter(x, y)
    # Add density scatter feature in object
    sctr1.density_scatter()

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [sctr1]
    plot1.add_title(label='Density Scatter Plot')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_legend()

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
