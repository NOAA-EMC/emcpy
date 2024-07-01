"""
Vertical Line Plot
------------------

Below is an example of how to plot a vertical
line using EMCPy's plotting method.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import VerticalLine
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():

    x = 5

    # Create vertical line plot object
    vlp = VerticalLine(x)
    vlp.label = 'Vertical Line'

    # Add vertical line plot object to list
    plt_list = [vlp]

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [vlp]
    plot1.add_title('Vertical Line Plot')
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
