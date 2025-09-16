from __future__ import annotations
from typing import Iterable, Optional, Sequence
import numpy as np
from matplotlib.colors import Normalize, BoundaryNorm


def compute_norm(
    *,
    integer_field: bool,
    vmin: Optional[float] = None,
    vmax: Optional[float] = None,
    levels: Optional[Sequence[float]] = None,
    ncolors: Optional[int] = None,
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
    if integer_field:
        if levels is not None:
            boundaries = np.asarray(levels, dtype=float)
            if boundaries.ndim != 1 or boundaries.size < 2:
                raise ValueError("`levels` must be a 1D sequence with at least 2 values.")
            # ensure monotonic
            if not (np.all(np.diff(boundaries) > 0) or np.all(np.diff(boundaries) < 0)):
                raise ValueError("`levels` must be strictly monotonic for BoundaryNorm.")
            # ascending order is standard
            if boundaries[0] > boundaries[-1]:
                boundaries = boundaries[::-1]
            return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

        # No levels; derive integer bin edges from vmin/vmax
        if vmin is None or vmax is None:
            raise ValueError("integer_field=True requires `levels` or both `vmin` and `vmax`.")
        if vmin == vmax:
            raise ValueError("`vmin` must differ from `vmax` for integer_field=True.")
        lo = int(np.floor(vmin))
        hi = int(np.ceil(vmax))
        # +2 because BoundaryNorm expects boundaries length = nbins + 1
        boundaries = np.arange(lo, hi + 2, dtype=float)
        return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

    # Continuous case
    if vmin is None or vmax is None:
        return Normalize()
    if vmin == vmax:
        raise ValueError("`vmin` must differ from `vmax` for continuous normalization.")
    return Normalize(vmin=vmin, vmax=vmax)
