import numpy as np
import matplotlib.pyplot as plt
from matplotlib.colors import Normalize
from scipy.interpolate import interpn
from emcpy.stats import get_linear_regression

__all__ = ['scatter']


def _density_scatter(x, y, ax=None, sort=True, bins=20, **kwargs):
    """
    Creates scatter plot colored by 2d histogram
    """
    data, x_e, y_e = np.histogram2d(x, y, bins=bins, density=True)
    z = interpn((0.5*(x_e[1:] + x_e[:-1]), 0.5*(y_e[1:]+y_e[:-1])),
                data, np.vstack([x, y]).T, method="splinef2d",
                bounds_error=False)
    # To be sure to plot all data
    z[np.where(np.isnan(z))] = 0.0
    # Sort the points by density, so that the densest points are plotted last
    if sort:
        idx = z.argsort()
        x, y, z = x[idx], y[idx], z[idx]
    ax.scatter(x, y, c=z, **kwargs)
    norm = Normalize(vmin=np.min(z), vmax=np.max(z))

    return ax


def _gen_scatter(x, y, plotopts):
    """
    Generate scatter plot from x and y.
    """
    fig = plt.figure(figsize=(8, 6))
    ax = fig.add_subplot(111)

    if plotopts['density']:
        ax = _density_scatter(x, y, ax=ax, bins=[100, 100],
                              s=4, cmap=plotopts['cmap'])
    else:
        plt.scatter(x, y, s=4, color=plotopts['color'],
                    label=f'n={np.count_nonzero(~np.isnan(x))}')

    if plotopts['linear_regression']:
        y_pred, r_sq, intercept, slope = get_linear_regression(x, y)
        label = f"y = {slope:.4f}x + {intercept:.4f}\nR\u00b2 : {r_sq:.4f}"
        ax.plot(x, y_pred, color=plotopts['r color'], linewidth=1, label=label)

    plt.grid(plotopts['grid'])
    plt.legend(loc='upper left', fontsize=11)
    plt.title(plotopts['title'], loc='left')
    plt.title(plotopts['time title'], loc='right', fontweight='semibold')
    plt.xlabel(plotopts['xlabel'], fontsize=12)
    plt.ylabel(plotopts['ylabel'], fontsize=12)

    return fig


def scatter(x, y, linear_regression=True, density=False,
            color='darkgray', cmap='magma', r_color='black',
            grid=False, title='EMCPy Scatter Plot', time_title=None,
            xlabel=None, ylabel=None):
    """
    Returns a figure of a scatter plot given x and y.

    Parameters
    ----------
        x, y : (array type) The data required to create scatter plot
        linear_regression : (bool, optional, default=True) To perform a linear regression and plot the line on the figure
        density : (bool, optional, default=False) Plot a density scatter plot
        color : (str, optional, default='darkgray') Color of scatter plot dots
        cmap : (str, optional, default='magma') Color map of density scatter plot
        r_color : (str, optional, default='black') Color of regression line when linear_regression=True
        grid : (bool, optional, default=False) Plot grid on scatter plot
        title : (str, optional, default='EmcPy Scatter Plot') Title to add to plot
        time_title : (str, optional, default=None) Secondary title for date/cycle to add to plot
        xlabel : (str, optional, default=None) X label on plot
        ylabel : (str, optional, default=None) Y label on plot

    Returns
    -------
        fig : (matplotlib figure object) Figure of the scatter plot
    """

    plotopts = {'linear_regression': linear_regression, 'density': density,
                'color': color, 'cmap': cmap, 'r color': r_color,
                'grid': grid, 'title': title, 'time title': time_title,
                'xlabel': xlabel, 'ylabel': ylabel}

    fig = _gen_scatter(x, y, plotopts)

    return fig
