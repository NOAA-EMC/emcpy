"""
Error Bars
==========

Asymmetric error bars using the :class:`ErrorBar` layer.
"""
import numpy as np

from emcpy.plots.plots import LinePlot, ErrorBar
from emcpy.plots.create_plots import CreatePlot, CreateFigure

rng = np.random.default_rng(42)
x = np.linspace(0, 10, 25)
y = np.sin(x) + 0.2 * rng.standard_normal(x.size)

err_lo = 0.15 + 0.05 * rng.random(x.size)
err_hi = 0.20 + 0.05 * rng.random(x.size)

p = CreatePlot()
layers = []

lp = LinePlot(x, np.sin(x))
lp.linewidth = 2
lp.label = "model"
layers.append(lp)

eb = ErrorBar(x, y)
eb.yerr = [err_lo, err_hi]  # asymmetric y errors
eb.fmt = "o"
eb.capsize = 3
eb.label = "observations"
layers.append(eb)

p.plot_layers = layers
p.add_title("Error Bars")
p.add_xlabel("x")
p.add_ylabel("value")
p.add_grid()
p.add_legend(loc="upper right", frameon=False)

fig = CreateFigure(1, 1, figsize=(7.5, 4))
fig.plot_list = [p]
fig.create_figure()
fig.tight_layout()
