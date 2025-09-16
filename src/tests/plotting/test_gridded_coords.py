import numpy as np
from emcpy.plots.create_plots import CreatePlot, CreateFigure
from emcpy.plots.plots import GriddedPlot


def _run(fig):
    fig.create_figure()
    fig.close_figure()


def test_pcolormesh_1d_centers():
    x = np.linspace(0, 1, 5)
    y = np.linspace(0, 1, 4)
    X, Y = np.meshgrid(x, y)
    Z = np.sin(X*Y)
    p = CreatePlot(plot_layers=[GriddedPlot(x, y, Z)])
    fig = CreateFigure(1, 1)
    fig.plot_list = [p]
    _run(fig)


def test_pcolormesh_2d_edges():
    xe = np.linspace(0, 1, 6)   # +1
    ye = np.linspace(0, 1, 5)   # +1
    Xe, Ye = np.meshgrid(xe, ye)
    xc = 0.5*(xe[:-1]+xe[1:])
    yc = 0.5*(ye[:-1]+ye[1:])
    Xc, Yc = np.meshgrid(xc, yc)
    Z = np.cos(2*np.pi*Xc)*np.sin(2*np.pi*Yc)
    p = CreatePlot(plot_layers=[GriddedPlot(Xe, Ye, Z)])
    fig = CreateFigure(1, 1)
    fig.plot_list = [p]
    _run(fig)
