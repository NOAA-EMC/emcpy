import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot

x = [0, 401, 1039, 2774, 2408, 512]
y = [0, 45, 225, 510, 1200, 1820]

# Create line plot object
lp = LinePlot(x, y)
plt_list = [lp]

# Create plot and draw data
myplt = CreatePlot()
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Line Plot, Inverted Log Scale')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')

# Set y-scale to log and invert
myplt.set_yscale('log')
myplt.invert_yaxis()

# Set new y labels
ylabels = [0, 50, 100, 500, 1000, 2000]
myplt.set_yticklabels(labels=ylabels)

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('inverted_log_scale_line_plot.png')
