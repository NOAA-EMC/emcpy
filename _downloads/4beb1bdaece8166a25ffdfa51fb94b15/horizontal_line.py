"""
Horizontal Line Plot
--------------------

Below is an example of how to plot a horizontal
line using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import HorizontalLine
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():

    y = 5

    # Create vertical line plot object
    hlp = HorizontalLine(y)
    hlp.label = 'Horizontal Line'

    # Add vertical line plot object to list
    plt_list = [hlp]

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [hlp]
    plot1.add_title('Horizontal Line Plot')
    plot1.add_xlabel('X Axis Label')
    plot1.add_ylabel('Y Axis Label')
    plot1.add_legend(loc='upper right')

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
