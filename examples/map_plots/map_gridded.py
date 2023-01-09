import numpy as np
import matplotlib.pyplot as plt
from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.map_plots import MapGridded

# Create 2d gridded plot on global domian
lats = np.linspace(25, 50, 25)
lons = np.linspace(245, 290, 45)
X, Y = np.meshgrid(lons, lats)
Z = np.random.normal(size=X.shape)

# Create gridded map object
gridded = MapGridded(X, Y, Z)
gridded.cmap = 'plasma'

# Create plot object and add features
plot1 = CreatePlot()
plot1.plot_layers = [gridded]
plot1.projection = 'plcarr'
plot1.domain = 'conus'
plot1.add_map_features(['coastline'])
plot1.add_xlabel(xlabel='longitude')
plot1.add_ylabel(ylabel='latitude')
plot1.add_title(label='2D Gridded Data', loc='center')
plot1.add_grid()
plot1.add_colorbar(label='colorbar label',
                   fontsize=12, extend='neither')

# Create figure
fig = CreateFigure()
fig.plot_list = [plot1]
fig.create_figure()
fig.save_figure('map_gridded.png')
