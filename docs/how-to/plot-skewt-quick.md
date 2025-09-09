# How to plot a minimal Skew-T
A Skew-T log-p diagram is a standard meteorological tool for visualizing vertical profiles of the
atmosphere.

This guide shows the shortest path to a simple Skew-T-style plot.
```python
import numpy as np
import matplotlib.pyplot as plt
# Synthetic profile
p = np.geomspace(1000, 100, 60) # pressure (hPa)
t = 15 - 6.5 * np.log(1000 / p) # temperature (°C, toy lapse rate)
fig, ax = plt.subplots(figsize=(5, 5))
# Replace with EMCPy Skew-T call if available, e.g.:
# from emcpy.plots.skewt_projection import SkewXAxes
# from emcpy.plots.skewt import SkewT
# skew = SkewT(ax)
# skew.plot(p, t)
ax.plot(t, p) # placeholder
ax.set_ylim(1000, 100)
ax.set_xlabel("Temperature (°C)")
ax.set_ylabel("Pressure (hPa)")
ax.set_title("Skew-T (synthetic)")
ax.grid(True, alpha=0.3)
plt.show()
```
```{note}
This is a bare-bones example to demonstrate the structure.
See the [Examples gallery](../auto_examples/index.rst) for a **full Skew-T with dewpoint, winds, and
annotations (LCL/LFC)**.
```