import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots.plots import Scatter
from emcpy.plots.create_plots import CreatePlot
from emcpy.stats import get_linear_regression

# Create test data
rng = np.random.RandomState(0)
x = rng.randn(100)
y = rng.randn(100)

# Create Scatter object
sctr = Scatter(x, y)
# Add linear regression feature in scatter object
sctr.add_linear_regression()

# Create Plot and draw data
myplt = CreatePlot()
plt_list = [sctr]
myplt.draw_data(plt_list)

# Add features
myplt.add_title(label='Test Scatter Plot')
myplt.add_xlabel(xlabel='X Axis Label')
myplt.add_ylabel(ylabel='Y Axis Label')
myplt.add_legend()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('scatter_w_regression.png')
