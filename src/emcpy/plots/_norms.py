from __future__ import annotations
from typing import Iterable, Optional, Sequence
import numpy as np
from matplotlib.colors import Normalize, BoundaryNorm, TwoSlopeNorm


def compute_norm(
    *, integer_field: bool,
    vmin: float | None,
    vmax: float | None,
    levels: Sequence[float] | None = None,
    ncolors: int | None = None,
    clip: bool = False,
    center: float | None = None,
):
    """
    Choose a Matplotlib norm for a plot, with robust handling of integer categories
    and diverging (centered) continuous data.

    - If integer_field is True: unchanged from before (BoundaryNorm path). `center`
      is ignored for integer/categorical fields — it has no meaning there.
    - Else, if `center` is given: build a TwoSlopeNorm around it. Requires vmin/vmax
      (caller is expected to have inferred these from data already if not user-set).
      If the data doesn't actually straddle `center`, the bound on the non-spanning
      side is nudged just past `center` so TwoSlopeNorm doesn't raise.
    - Else: original continuous behavior (Normalize / BoundaryNorm from levels).
    """
    # Integer categories → discrete bins with half-step edges (unchanged)
    if integer_field:
        if levels is not None:
            b = np.asarray(levels, dtype=float)
            if b.ndim != 1 or b.size < 2:
                return None
            if np.allclose(b, np.round(b)):
                lo = int(np.floor(b.min()))
                hi = int(np.ceil(b.max()))
                boundaries = np.arange(lo - 0.5, hi + 1.5, 1.0)
            else:
                boundaries = b
            return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

        if vmin is None or vmax is None:
            raise ValueError("integer_field=True requires `levels` or both `vmin` and `vmax`.")
        lo = int(np.floor(vmin))
        hi = int(np.ceil(vmax))
        boundaries = np.arange(lo - 0.5, hi + 1.5, 1.0)
        return BoundaryNorm(boundaries, ncolors or 256, clip=clip)

    # Diverging / centered continuous data
    if center is not None:
        if vmin is None or vmax is None:
            raise ValueError("center=<value> requires both `vmin` and `vmax` "
                             "(infer them from data upstream if not user-set).")
        if vmin == vmax:
            raise ValueError("vmin and vmax must differ when using a centered norm.")

        span = max(abs(vmax - vmin), 1e-9)
        eps = span * 0.01
        if vmin >= center:
            vmin = center - eps
        if vmax <= center:
            vmax = center + eps

        return TwoSlopeNorm(vcenter=center, vmin=vmin, vmax=vmax)

    # Continuous case (unchanged)
    if levels is not None:
        b = np.asarray(levels, dtype=float)
        if b.ndim == 1 and b.size >= 2:
            return BoundaryNorm(b, ncolors or 256, clip=clip)

    if vmin is None or vmax is None:
        return None
    return Normalize(vmin=vmin, vmax=vmax, clip=clip)
