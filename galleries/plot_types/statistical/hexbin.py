"""
HexBin
======

Density of points with :class:`HexBin` and a colorbar.
"""
import numpy as np

from emcpy.plots.plots import HexBin
from emcpy.plots.create_plots import CreatePlot, CreateFigure

rng = np.random.default_rng(2)
x = rng.normal(size=5000)
y = x * 0.5 + rng.normal(scale=0.7, size=5000)

p = CreatePlot()
layers = []

hb = HexBin(x, y)
hb.gridsize = 35
hb.cmap = "viridis"
layers.append(hb)

p.plot_layers = layers
p.add_title("HexBin")
p.add_xlabel("x")
p.add_ylabel("y")
p.add_grid(alpha=0.3)
p.add_colorbar(label="count")

fig = CreateFigure(1, 1, figsize=(6.8, 5.2))
fig.plot_list = [p]
fig.create_figure()
fig.tight_layout()
