import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot

x1 = [0, 401, 1039, 2774, 2408]
x2 = [500, 250, 710, 1515, 1212]
x3 = [400, 150, 910, 1215, 850]
y1 = [0, 2.5, 5, 7.5, 12.5]
y2 = [1, 5, 6, 8, 10]
y3 = [1, 4, 5.5, 9, 10.5]

# Create line plot object
lp1 = LinePlot(x1, y1)
lp1.label = 'line 1'

# Create line 2 plot object
lp2 = LinePlot(x2, y2)
lp2.color = 'tab:green'
lp2.label = 'line 2'

# Create line 3 plot object
lp3 = LinePlot(x3, y3)
lp3.color = 'tab:red'
lp3.label = 'line 3'

# Add line plot objects to list
plt_list = [lp1, lp2, lp3]

# Create Plot and draw data
myplt = CreatePlot()
myplt.draw_data(plt_list)

# Add plot features
myplt.add_title(label='Test Line Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('multi_line_plot.png')
