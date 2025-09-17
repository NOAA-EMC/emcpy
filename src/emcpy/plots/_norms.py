from __future__ import annotations
from typing import Iterable, Optional, Sequence
import numpy as np
from matplotlib.colors import Normalize, BoundaryNorm


def compute_norm(
    *, integer_field: bool,
    vmin: float | None,
    vmax: float | None,
    levels: Optional[np.ndarray] = None,
    ncolors: int | None = None,
    clip: bool = False,
):
    """
    Choose a Matplotlib norm for a plot, with robust handling of integer categories.

    - If integer_field is True:
        - If `levels` given, use those as bin boundaries (must be monotonic and >= 2 long)
        - Else require both vmin & vmax and build integer bin edges: [floor(vmin), ..., ceil(vmax)+1]
        - Returns BoundaryNorm(boundaries, ncolors or 256, clip=False)
    - Else:
        - If vmin/vmax both None -> Normalize() (auto)
        - If exactly one is None -> Normalize() (auto)
        - If vmin == vmax -> ValueError
        - Else -> Normalize(vmin, vmax)
    """
    # Integer categories → discrete bins with half-step edges
    if integer_field:
        if levels is not None:
            b = np.asarray(levels, dtype=float)
            if b.ndim != 1 or b.size < 2:
                return None
            # If the levels look like integer class centers, convert to edges
            if np.allclose(b, np.round(b)):
                lo = int(np.floor(b.min()))
                hi = int(np.ceil(b.max()))
                boundaries = np.arange(lo - 0.5, hi + 1.5, 1.0)
            else:
                # Already explicit edges; trust the caller
                boundaries = b
            return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

        if vmin is None or vmax is None:
            raise ValueError("integer_field=True requires `levels` or both `vmin` and `vmax`.")
        lo = int(np.floor(vmin))
        hi = int(np.ceil(vmax))
        boundaries = np.arange(lo - 0.5, hi + 1.5, 1.0)
        return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

    # Continuous case
    if levels is not None:
        b = np.asarray(levels, dtype=float)
        if b.ndim == 1 and b.size >= 2:
            return BoundaryNorm(b, ncolors or 256, clip=clip)

    if vmin is None or vmax is None:
        return None
    return Normalize(vmin=vmin, vmax=vmax, clip=clip)
    