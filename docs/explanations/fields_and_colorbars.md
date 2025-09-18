# Discrete fields and colorbars
---

Many EMCPy layers support integer (categorical) fields via ``integer_field=True``.
When enabled, EMCPy builds a discrete colormap using ``BoundaryNorm`` and
formats the colorbar for category-like values.

Normalization policy
--------------------

- If ``levels`` is provided:
  - If the values look like integer *class centers* (e.g., ``[0, 1, 2, 3]``), EMCPy
    converts them to half-step *edges* (e.g., ``[-0.5, 0.5, 1.5, 2.5, 3.5]``).
  - Otherwise, the given values are treated as explicit boundaries.
- Else, if both ``vmin`` and ``vmax`` are provided, edges are built from
  ``floor(vmin)`` to ``ceil(vmax)`` with unit steps.
- Else, EMCPy infers bounds from the data attached to the layer (e.g., ``c``,
  ``data``, ``z``, or ``C``). For constant integer fields, EMCPy widens the
  range by one class so the colorbar renders sensibly.

Colorbar behavior
-----------------

- When a ``BoundaryNorm`` with ~unit-spaced boundaries is detected, EMCPy
  centers colorbar ticks at bin centers (``k + 0.5``) and labels them with the
  corresponding integer class (``k``).
- The colorbar ``extend`` (``'neither' | 'min' | 'max' | 'both'``) is inferred
  automatically by comparing the data range against the normalization limits or
  boundaries.

Gridded coordinates (maps and regular axes)
-------------------------------------------

- 1D coordinates may be either centers (length ``N``) or edges (length ``N+1``).
- 2D coordinates must either match the data shape (centers) or be one larger in
  both dimensions (edges).
- For edge coordinates, EMCPy defaults to ``shading='flat'`` to avoid seams.

Example
-------

.. code-block:: python

   # Discrete map gridded example
   from emcpy.plots.map_plots import MapGridded
   from emcpy.plots.create_plots import CreatePlot, CreateFigure
   import numpy as np

   lon = np.linspace(-100, -90, 21)
   lat = np.linspace(30, 40, 11)
   LON, LAT = np.meshgrid(lon, lat)

   # Integer classes 0..5
   Z = np.floor(3 * np.sin(np.radians(LAT)) + 3).astype(int)

   g = MapGridded(latitude=LAT, longitude=LON, data=Z)
   g.integer_field = True          # enables discrete bins + integer-friendly colorbar
   g.cmap = "viridis"

   p = CreatePlot(projection="plcarr", domain="conus")
   p.plot_layers = [g]
   p.add_map_features(["coastline"])
   p.add_colorbar(label="Category")

   fig = CreateFigure(1, 1, figsize=(8, 4))
   fig.plot_list = [p]
   fig.create_figure()
   fig.tight_layout()

Tips
----

- For scatter layers, passing numeric ``c=...`` triggers the same normalization
  policy as above when ``integer_field=True``.
- For contour/contourf, ``levels`` are preserved as requested, while the
  normalization follows the same discrete rules.
