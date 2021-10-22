import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import Histogram
from emcpy.plots.create_plots import CreatePlot

# Generate test data for histogram plots
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
data = mu + sigma * np.random.randn(437)

# Create histogram object
hst = Histogram(data)
hst.color = 'tab:green'
hst.alpha = 0.7
hst.label = 'data'

# Create histogram plot and draw data
myplt = CreatePlot()
plt_list = [hst]
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Histogram Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('histogram.png')
