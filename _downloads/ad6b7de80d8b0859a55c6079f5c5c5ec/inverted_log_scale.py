"""
Invert log scale
----------------

This example shows how to create an inverted
y-axis that also uses a log scale. This is useful
if you are looking at a column of data throughout
the atmosphere and the y-axis is pressure.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():

    x = [0, 401, 1039, 2774, 2408, 512]
    y = [0, 45, 225, 510, 1200, 1820]

    # Create line plot object
    lp = LinePlot(x, y)

    # Create plot object and add features
    plot1 = CreatePlot()
    plot1.plot_layers = [lp]
    plot1.add_title(label='Test Line Plot, Inverted Log Scale')
    plot1.add_xlabel(xlabel='X Axis Label')
    plot1.add_ylabel(ylabel='Y Axis Label')

    # Set y-scale to log and invert
    plot1.set_yscale('log')
    plot1.invert_yaxis()

    # Set explicit y-ticks and matching labels.
    # NOTE: 0 is intentionally omitted -- log(0) is undefined, so a tick
    # at 0 has no valid position on a log-scaled axis. Relying on an
    # implicit tick count from the auto LogLocator is what broke here;
    # ticks are now set explicitly so label count always matches.
    ylabels = [50, 100, 500, 1000, 2000]
    plot1.set_yticks(ticks=ylabels)
    plot1.set_yticklabels(labels=ylabels)

    # Create figure
    fig = CreateFigure()
    fig.plot_list = [plot1]
    fig.create_figure()

    plt.show()


if __name__ == '__main__':
    main()
