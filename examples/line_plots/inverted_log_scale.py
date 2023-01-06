import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure

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

# Set new y labels
ylabels = [0, 50, 100, 500, 1000, 2000]
plot1.set_yticklabels(labels=ylabels)

# Create figure
fig = CreateFigure()
fig.plot_list = [plot1]
fig.create_figure()
fig.save_figure('inverted_log_scale_line_plot.png')
