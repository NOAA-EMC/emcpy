# Example template
Use this template when adding a new example to the gallery.
It ensures consistency and makes contributions easy to review.
---
## Title
One-line summary of what the example shows.

## What it demonstrates
- List the main features (e.g., "Skew-T with winds", "Integer field with discrete colormap").

## Script
Place a `.py` file in `docs/examples/` with a header like this:
```python
"""
Skew-T with winds
=================
This example shows how to plot a Skew-T with temperature, dewpoint, and wind barbs.
It uses EMCPy SkewT class and Cartopy for background features.
"""
```

Then include a concise but complete script (ideally <150 lines).
Prefer **synthetic data** unless you need a small real dataset.
---
## Data policy
- Use synthetic arrays generated in code whenever possible.
- If using real data, keep files <5 MB and store them in `docs/_static/data/`.
- Always provide attribution for external datasets.

```{tip}
When in doubt, look at an existing example in `docs/examples/` and mirror its structure.
```