import numpy as np
from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots.map_plots import MapGridded


def test_integer_field_requires_bounds_or_levels():
    lat = np.linspace(-10, 10, 5)
    lon = np.linspace(0, 20, 5)
    LON, LAT = np.meshgrid(lon, lat)
    Z = np.ones((5, 5), dtype=int) * 3
    mg = MapGridded(LAT, LON, Z)
    mg.integer_field = True
    p = CreatePlot(projection="plcarr", domain="global", plot_layers=[mg])
    fig = CreateFigure(1, 1)
    fig.plot_list = [p]
    # supply vmin/vmax to avoid ValueError
    mg.vmin = 0
    mg.vmax = 5
    fig.create_figure()
    fig.close_figure()
