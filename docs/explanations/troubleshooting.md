# Troubleshooting
Common issues and their solutions when working with EMCPy.
---
## Maps lack coastlines or borders
Cartopy requires shapefile data. If coastlines don’t render:
- Ensure Cartopy has downloaded the required Natural Earth data files. Files can be downloaded here: https://www.naturalearthdata.com/downloads/
- Further instructions on shapefiles can be found here: https://scitools.org.uk/cartopy/docs/v0.15/tutorials/using_the_shapereader.html
- Clear the Cartopy cache if files are corrupted.
```python
import cartopy
print(cartopy.config['data_dir'])
```
---
## Backend errors on HPC clusters
Most HPC systems don’t support interactive backends.
Force Matplotlib to use a non-GUI backend:
```python
import matplotlib
matplotlib.use("Agg")
```
---
## Fonts look inconsistent on CI vs local
Set an explicit font family to make plots consistent across systems:
```python
import matplotlib.pyplot as plt
plt.rcParams["font.family"] = "DejaVu Sans"
```
---
## Colorbars show non-integer ticks
When plotting integer categories, use `BoundaryNorm` and specify tick values manually:
```python
from matplotlib.colors import BoundaryNorm
bounds = [-0.5, 0.5, 1.5, 2.5, 3.5]
norm = BoundaryNorm(bounds, ncolors=4, clip=True)
```
```{tip}
If you encounter a problem not listed here, please open an issue on the EMCPy GitHub repository with
a minimal reproducible example.
```