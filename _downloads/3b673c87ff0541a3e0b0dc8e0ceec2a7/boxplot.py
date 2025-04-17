"""
Box Plot
--------

Below is an example of how to plot a box
plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import BoxandWhiskerPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():
    # Create box and whisker plot

    # Grab sample data
    data = _getBoxPlotData()

    # Create box plot object
    bwp = BoxandWhiskerPlot(data)
    bwp.label = 'Box Plot data'

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [bwp]
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')
    plot1.add_title('Test Box and Whisker Plot')
    plot1.add_legend(loc='upper left')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


def _getBoxPlotData():
    # Generate test data for box and whisker plot

    # Fixing random state for reproducibility
    np.random.seed(19680801)

    data = [np.random.normal(0, std, 100) for std in range(6, 10)]

    return data


if __name__ == '__main__':
    main()
