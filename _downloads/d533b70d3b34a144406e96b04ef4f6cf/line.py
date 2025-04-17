"""
Line Plot
---------

Below is an example of how to plot a basic
line plot using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():

    x = [1, 2, 3, 4, 5]
    y = [1, 2, 3, 4, 5]

    # Create line plot object
    lp = LinePlot(x, y)
    lp.label = 'line'

    # Add line plot object to list
    plt_list = [lp]

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [lp]
    plot1.add_title('Line Plot')
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
