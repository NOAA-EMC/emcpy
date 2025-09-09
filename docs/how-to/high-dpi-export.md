# How to export crisp figures (PNG/SVG/PDF)
Use consistent export settings for publication-quality images.

```python
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 2*np.pi, 400)
y = np.sin(x)
fig, ax = plt.subplots(figsize=(6.5, 3.5))
ax.plot(x, y)
ax.set(title="High-DPI export example", xlabel="x (rad)", ylabel="sin(x)")
fig.tight_layout()
# PNG raster: web-friendly
fig.savefig("export_example.png", dpi=300, bbox_inches="tight")
# SVG vector: ideal for docs
fig.savefig("export_example.svg", bbox_inches="tight")
# PDF vector: print-ready
fig.savefig("export_example.pdf", bbox_inches="tight")
```
```{tip}
- Prefer vector formats (`.svg`, `.pdf`) for lines and text.
- Use raster (`.png`) for dense images like heatmaps.
- Add `bbox_inches="tight"` to trim whitespace.
```