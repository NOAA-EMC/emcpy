"""
Bar Plot
--------

Below is an example of how to plot a bar
plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import BarPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create bar plot

    # Grab sample bar plot data
    x_pos, heights = _getBarData()

    # Create bar plot object
    bar = BarPlot(x_pos, heights)
    bar.color = 'tab:red'

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [bar]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title("Bar Plot")

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


def _getBarData():
    # Generate test data for bar graphs

    x = ['a', 'b', 'c', 'd', 'e', 'f']
    heights = [5, 6, 15, 22, 24, 8]

    x_pos = [i for i, _ in enumerate(x)]

    return x_pos, heights


if __name__ == '__main__':
    main()
