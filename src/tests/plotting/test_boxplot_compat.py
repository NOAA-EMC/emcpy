import types
from emcpy.plots._mpl_compat import boxplot_kwargs

def _layer(**attrs):
    # simple shim to mimic a BoxandWhiskerPlot instance
    L = types.SimpleNamespace(plottype="boxandwhisker", data=[ [1,2,3] ])
    for k, v in attrs.items():
        setattr(L, k, v)
    return L

def test_orientation_vertical_default():
    L = _layer(orientation="vertical")
    kw, lab = boxplot_kwargs(L)
    assert kw["vert"] is True
    assert "labels" not in kw and "tick_labels" not in kw

def test_orientation_horizontal():
    L = _layer(orientation="h")
    kw, _ = boxplot_kwargs(L)
    assert kw["vert"] is False

def test_tick_labels_version_switch():
    L = _layer(tick_labels=["A","B"])
    kw, _ = boxplot_kwargs(L)
    assert ("tick_labels" in kw) ^ ("labels" in kw)  # exactly one present

def test_conflicting_labels_raises():
    L = _layer(tick_labels=["A"], labels=["B"])
    try:
        boxplot_kwargs(L)
        assert False, "expected ValueError"
    except ValueError:
        pass

def test_legend_label_not_forwarded():
    L = _layer(label="Series X")
    kw, lab = boxplot_kwargs(L)
    assert "label" not in kw
    assert lab == "Series X"
