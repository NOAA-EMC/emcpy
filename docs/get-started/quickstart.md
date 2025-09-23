# Quickstart
Here’s the shortest path from a clean environment to a plot with EMCPy.
```python
import numpy as np
import matplotlib.pyplot as plt
x = np.linspace(0, 10, 200)
y = np.sin(x)
fig, ax = plt.subplots(figsize=(6, 3))
ax.plot(x, y, lw=2, label="signal")
ax.scatter(x[::10], y[::10], s=18, alpha=0.8, label="samples")
ax.set(title="Hello EMCPy", xlabel="x", ylabel="sin(x)")
ax.legend(frameon=False)
fig.tight_layout()
plt.show()
```
---
## Next steps
- Explore the [Examples gallery](../examples/index) for real-world plots.
- Read [Explanations](../explanations/index.md) to understand design choices.