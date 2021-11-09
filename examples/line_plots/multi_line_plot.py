import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import LinePlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure


def _getLineData():
    # generate test data for line plots

    x1 = [0, 401, 1039, 2774, 2408]
    x2 = [500, 250, 710, 1515, 1212]
    x3 = [400, 150, 910, 1215, 850]
    y1 = [0, 2.5, 5, 7.5, 12.5]
    y2 = [1, 5, 6, 8, 10]
    y3 = [1, 4, 5.5, 9, 10.5]

    return x1, y1, x2, y2, x3, y3


# create line plot with two sets of axes
# sharing a common y axis

x1, y1, x2, y2, x3, y3 = _getLineData()
lp1 = LinePlot(x1, y1)
lp1.label = 'line 1'

lp2 = LinePlot(x2, y2)
lp2.color = 'tab:green'
lp2.label = 'line 2'
lp2.use_shared_ay()

lp3 = LinePlot(x3, y3)
lp3.color = 'tab:red'
lp3.label = 'line 3'
lp3.use_shared_ay()

myplt = CreatePlot()
plt_list = [lp1, lp2, lp3]
myplt.draw_data(plt_list)

myplt.add_title(label='Test Line Plot, 2 X Axes ')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_xlabel(xlabel='Secondary X Axis Label', xaxis='secondary')

fig = myplt.return_figure()
fig.add_legend(plotobj=myplt, loc='upper right')
fig.savefig('multi_line_plot.png')
