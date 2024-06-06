"""
Line Plot Options
-----------------

This script shows several examples of the many
different line plot options. They follow the same
options as matplotlib.

"""

import numpy as np
import matplotlib.pyplot as plt

from emcpy.plots.plots import LinePlot, HorizontalLine
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def main():

    x1 = [1, 2, 3, 4, 5]
    y1 = [1, 2, 3, 4, 5]
    x2 = [1, 2, 3, 4, 5]
    y2 = [2, 4, 6, 8, 10]
    x3 = [1, 2, 3, 4, 5]
    y3 = [5, 4, 3, 2, 1]

    # Top plot
    plot1 = CreatePlot()  # Create  Plot
    plt_list = []  # initialize emtpy plot list
    lp = LinePlot(x1, y1)  # Create line plot object
    lp.color = "green"  # line color
    lp.linestyle = "-"  # line style
    lp.linewidth = 1.5  # line width
    lp.marker = "o"  # marker type
    lp.markersize = 4  # markersize
    lp.alpha = None  # transparency
    lp.label = "line1"  # give it a label
    plt_list.append(lp)  # Add line plot object to list

    lp = LinePlot(x2, y2)  # Create line plot object
    lp.color = "red"  # line color
    lp.linestyle = "-"  # line style
    lp.linewidth = 1.5  # line width
    lp.marker = "o"  # marker type
    lp.markersize = 4  # markersize
    lp.alpha = None  # transparency
    lp.label = "line2"  # give it a label
    plt_list.append(lp)  # Add line plot object to list

    # Bottom plot
    plot2 = CreatePlot()  # Create Plot
    plt_list2 = []  # initialize empty plot list
    lp = LinePlot(x3, y3)  # Create line plot object
    lp.color = "blue"  # line color
    lp.linestyle = "-"  # line style
    lp.linewidth = 1.5  # line width
    lp.marker = "o"  # marker type
    lp.markersize = 4  # markersize
    lp.alpha = None  # transparency
    lp.label = "line3"  # give it a label
    plt_list2.append(lp)  # Add line plot object to list

    lp = HorizontalLine(1)  # Draw horizontal line
    lp.color = "black"  # line color
    lp.linestyle = "-"  # line style
    lp.linewidth = 1.5  # line width
    lp.marker = None  # marker type
    lp.alpha = None  # transparency
    lp.label = None  # give it a label
    plt_list2.append(lp)  # Add line plot object to list

    plot1.plot_layers = plt_list  # draw plot1 (the top plot)
    plot2.plot_layers = plt_list2  # draw plot2 (the bottom plot)

    # Add plot features
    plot1.add_title(label="Test Line Plot 1")
    plot1.add_xlabel(xlabel="X Axis Label 1")
    plot1.add_ylabel(ylabel="Y Axis Label 1")
    plot1.add_grid()
    plot1.set_xticks(x1)
    plot1.set_xticklabels([str(item) for item in x1], rotation=0)
    yticks = np.arange(np.min(y2), np.max(y2) + 1, 1)
    plot1.set_yticks(yticks)
    plot1.set_yticklabels([str(item) for item in yticks], rotation=0)
    plot1.add_legend(loc="upper left", fancybox=True, framealpha=0.80)

    # Add plot features
    plot2.add_title(label="Test Line Plot 2")
    plot2.add_xlabel(xlabel="X Axis Label 2")
    plot2.add_ylabel(ylabel="Y Axis Label 2")
    plot2.add_grid()
    plot2.set_xticks(x2)
    plot2.set_xticklabels([str(item) for item in x2], rotation=0)
    yticks = np.arange(np.min(y2), np.max(y2) + 1, 1)
    plot2.set_yticks(yticks)
    plot2.set_yticklabels([str(item) for item in yticks], rotation=0)
    plot2.add_legend(loc="upper left", fancybox=True, framealpha=0.80)

    # Return matplotlib figure
    fig = CreateFigure(nrows=2, ncols=1, figsize=(8, 6))
    fig.plot_list = [plot1, plot2]
    fig.create_figure()
    fig.add_suptitle("Super Title")
    fig.tight_layout()

    plt.show()


if __name__ == '__main__':
    main()
