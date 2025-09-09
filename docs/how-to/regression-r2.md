# How to add a regression line and R²
Compute slope/intercept with EMCPy’s regression helper and overlay the fit.

```python
import numpy as np
import matplotlib.pyplot as plt
from emcpy.stats.stats import get_linear_regression
rng = np.random.default_rng(0)
x = np.linspace(0, 1, 100)
y = 2.0 * x + 0.2 + 0.1 * rng.standard_normal(x.size)
slope, intercept, r_value, p_value, std_err = get_linear_regression(x, y)
fig, ax = plt.subplots(figsize=(5.5, 3.5))
ax.scatter(x, y, s=12, alpha=0.75, label="obs")
ax.plot(x, slope * x + intercept, lw=2, label=f"fit: y={slope:.2f}x+{intercept:.2f}")
ax.text(0.02, 0.95, f"$R^2$ = {r_value**2:.3f}", transform=ax.transAxes, va="top")
ax.set(title="Regression with R²", xlabel="x", ylabel="y")
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
```
```{note}
For grouped datasets, compute a separate regression per category and overlay multiple lines.
```