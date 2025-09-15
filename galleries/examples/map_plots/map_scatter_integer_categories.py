"""
Map scatter (integer categories)
================================

Integer categories with an automatic discrete color scale and colorbar.
"""

import numpy as np
from emcpy.plots.map_plots import MapScatter
from emcpy.plots.create_plots import CreatePlot, CreateFigure

rng = np.random.default_rng(1)
n = 600
lat = rng.uniform(25, 49, n)
lon = rng.uniform(-125, -67, n)
cat = rng.integers(0, 7, n)  # 7 classes

p = CreatePlot(projection="plcarr", domain="conus")
ms = MapScatter(lat, lon, data=cat)
ms.integer_field = True      # auto BoundaryNorm + discrete ticks
ms.cmap = "tab10"
ms.markersize = 10

p.plot_layers = [ms]
p.add_map_features(["states", "coastline"])
p.add_colorbar(label="Category")
p.add_title("Map scatter (integer categories)")
p.add_grid()

fig = CreateFigure(1, 1, figsize=(9, 5.2))
fig.plot_list = [p]
fig.create_figure()
fig.tight_layout()
