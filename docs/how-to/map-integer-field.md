# How to plot an integer field with discrete colors
Great for categories such as QC flags or launch status.
This example uses discrete bins and labeled ticks to keep the colorbar aligned with integers.

```python
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import BoundaryNorm
import cartopy.crs as ccrs
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.map_plots import MapScatter
lon = np.array([-120, -80, -75, -100])
lat = np.array([ 35, 40, 42, 30])
cat = np.array([ 0, 1, 2, 3])
bounds = np.array([-0.5, 0.5, 1.5, 2.5, 3.5])
norm = BoundaryNorm(bounds, ncolors=4, clip=True)
proj = MapProjection("plcarr")
domain = Domain("conus")
fig = plt.figure(figsize=(7, 4))
ax = plt.axes(projection=proj.projection)
proj.add_features(ax, domain=domain)
layer = MapScatter(latitude=lat, longitude=lon, data=cat)
layer.integer_field = True
layer.vmin, layer.vmax = 0, 3
layer.cmap = "tab10"
sc = ax.scatter(
lon, lat, c=cat, s=90, cmap=layer.cmap, norm=norm,
edgecolor="k", transform=ccrs.PlateCarree()
)
cb = plt.colorbar(sc, ax=ax, boundaries=bounds, ticks=[0, 1, 2, 3])
cb.set_label("Category")
ax.set_title("Discrete categories")
plt.show()
```
```{tip}
Use `BoundaryNorm` for crisp bin edges, and keep `vmin/vmax` aligned with your integer categories.
```