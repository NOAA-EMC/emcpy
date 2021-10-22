import numpy as np
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot

x1 = [1, 2, 3, 4]
y1 = [1, 2, 3, 4]

x2 = [10, 15, 20, 25]
y2 = [0, 5, 10, 15]

# Create line plot object
lp = LinePlot(x1, y1)
lp.label = 'line 1'

# Create plot and draw data
myplt = CreatePlot()
plt_list = [lp]
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Line Plot, 2 X Axes ')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')

# Add secondary xaxis
myplt.add_xlabel(xlabel='Secondary X Axis Label', xaxis='secondary')