import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import Scatter
from emcpy.plots.create_plots import CreatePlot

# Create test data
x = np.random.normal(size=1000)
y = x * 10 + np.random.normal(size=1000)

# Create Scatter object
sctr = Scatter(x, y)
# Add density scatter feature in object
sctr.density_scatter()

# Create Plot and draw data
myplt = CreatePlot()
plt_list = [sctr]
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Density Scatter Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('density_scatter.png')
