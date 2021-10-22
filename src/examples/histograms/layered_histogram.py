import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import Histogram
from emcpy.plots.create_plots import CreatePlot

# Generate test data for histogram plots
mu = 100  # mean of distribution
sigma = 15  # standard deviation of distribution
data1 = mu + sigma * np.random.randn(450)
data2 = mu + sigma * np.random.randn(225)

# Create histogram objects
hst1 = Histogram(data1)
hst1.color = 'tab:green'
hst1.alpha = 0.7
hst1.label = 'data 1'

hst2 = Histogram(data2)
hst2.color = 'tab:purple'
hst2.alpha = 0.7
hst2.label = 'data 2'

# Create histogram plot and draw data
myplt = CreatePlot()
plt_list = [hst1, hst2]
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Histogram Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('layered_histogram.png')
