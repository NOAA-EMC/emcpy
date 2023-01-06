import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure

x = [1, 2, 3, 4, 5]
y = [1, 2, 3, 4, 5]

# Create line plot object
lp = LinePlot(x, y)
lp.label = 'line'

# Add line plot object to list
plt_list = [lp]

# Create Plot and draw data
myplt = CreatePlot()
myplt.plot_layers = plt_list

# Add plot features
myplt.add_title(label='Test Line Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend(loc='upper left')

# Return matplotlib figure
fig = CreateFigure()
fig.plot_list = [myplt]
fig.create_figure()
fig.tight_layout()
fig.save_figure('line_plot.png')
