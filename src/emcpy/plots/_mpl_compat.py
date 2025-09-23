"""
Matplotlib compatibility helpers for EMCPy plot layers.
Keep backend/version-specific translations out of plot classes/renderers.
"""
from __future__ import annotations

from typing import Tuple, Dict, Any, Optional
import matplotlib as mpl

# Robust version check with graceful fallback (no hard dep on `packaging`)
try:
    from packaging.version import Version  # type: ignore

    _MPL_VER = Version(mpl.__version__)

    def _mpl_ge(ver: str) -> bool:
        return _MPL_VER >= Version(ver)
except Exception:
    def _mpl_ge(ver: str) -> bool:
        def _to_tuple(s: str):
            parts = []
            for p in s.split("."):
                try:
                    parts.append(int("".join(ch for ch in p if ch.isdigit())))
                except Exception:
                    parts.append(0)
            return tuple(parts[:3] or (0, 0, 0))
        return _to_tuple(mpl.__version__) >= _to_tuple(ver)


def boxplot_kwargs(layer: Any) -> Tuple[Dict[str, Any], Optional[str]]:
    """
    Normalize a BoxandWhiskerPlot layer into kwargs for Axes.boxplot,
    abstracting Matplotlib API differences.

    Returns
    -------
    inputs : dict
        Safe kwargs to pass to `ax.boxplot(...)` across MPL versions.
    legend_label : Optional[str]
        A label string to attach to one of the returned artists for legend use.
        (Do NOT forward this label in `inputs`—older MPL errors on `label=`.)
    """
    # Collect only supported/known kwargs for boxplot.
    allowed = {
        "notch", "sym", "whis", "bootstrap", "usermedians", "conf_intervals",
        "positions", "widths", "patch_artist", "manage_ticks", "autorange",
        "meanline", "zorder",
        # style/props dicts (forward if present)
        "boxprops", "flierprops", "medianprops", "meanprops", "capprops", "whiskerprops",
        # NB: showmeans is valid for boxplot; showmedians is not a boxplot kw
        "showmeans", "showcaps", "showbox", "showfliers",
    }

    inputs: Dict[str, Any] = {}
    for k in allowed:
        if hasattr(layer, k):
            v = getattr(layer, k)
            if v is not None:
                inputs[k] = v

    # ---- orientation -> vert (MPL < 3.9 uses 'vert'; 3.9 also still supports it) ----
    if hasattr(layer, "vert") and getattr(layer, "vert") is not None:
        inputs["vert"] = bool(getattr(layer, "vert"))
    else:
        orient = getattr(layer, "orientation", "vertical")
        s = str(orient).lower() if orient is not None else "vertical"
        if s in ("h", "horizontal"):
            inputs["vert"] = False
        elif s in ("v", "vertical"):
            inputs["vert"] = True
        else:
            raise ValueError(
                "BoxandWhiskerPlot.orientation must be 'vertical'/'v' or 'horizontal'/'h'"
            )

    # ---- labels vs tick_labels (MPL 3.9 change) ----
    tick_labels = getattr(layer, "tick_labels", None)
    legacy_labels = getattr(layer, "labels", None)
    if tick_labels is not None and legacy_labels is not None and tick_labels != legacy_labels:
        raise ValueError(
            "BoxandWhiskerPlot: both 'tick_labels' and legacy 'labels' are set with different values."
        )
    labels_effective = tick_labels if tick_labels is not None else legacy_labels
    if labels_effective is not None:
        if _mpl_ge("3.9.0"):
            inputs["tick_labels"] = labels_effective
        else:
            inputs["labels"] = labels_effective

    # Legend label is handled by the renderer after plotting
    legend_label = getattr(layer, "label", None)

    # Never pass `label` to ax.boxplot (older MPL raises TypeError)
    inputs.pop("label", None)

    return inputs, legend_label
