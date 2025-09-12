"""
Violin Plot (EMCPy)
===================

Distribution comparison using :class:`ViolinPlot`.
"""
import numpy as np

from emcpy.plots.plots import ViolinPlot
from emcpy.plots.create_plots import CreatePlot, CreateFigure

rng = np.random.default_rng(0)
groups = [rng.normal(0.0, 1.0, 400),
          rng.normal(0.5, 0.8, 400),
          rng.normal(-0.3, 1.2, 400)]

p = CreatePlot()
layers = []

vio = ViolinPlot(groups)
vio.showmedians = True
vio.alpha = 0.8
layers.append(vio)

p.plot_layers = layers
p.add_title("Violin Plot")
p.add_ylabel("value")
p.set_xticks([0, 1, 2])
p.set_xticklabels(["A", "B", "C"])

fig = CreateFigure(1, 1, figsize=(7.2, 4))
fig.plot_list = [p]
fig.create_figure()
fig.tight_layout()
