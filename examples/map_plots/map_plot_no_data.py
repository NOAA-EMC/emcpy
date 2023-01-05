import matplotlib.pyplot as plt
from emcpy.plots import CreatePlot, CreateFigure
from emcpy.plots.map_tools import Domain, MapProjection

# Create global map with no data using
# PlateCarree projection and coastlines
plot1 = CreatePlot()
plot1.projection = 'plcarr'
plot1.domain = 'global'
plot1.add_map_features(['coastline', 'land', 'ocean'])
plot1.add_xlabel(xlabel='longitude')
plot1.add_ylabel(ylabel='latitude')

fig = CreateFigure()
fig.plot_list = [plot1]
fig.create_figure()
fig.save_figure('map_plot_no_data.png')
