import matplotlib.pyplot as plt
from emcpy.plots import CreateMap
from emcpy.plots.map_tools import Domain, MapProjection

# Create global map with no data using
# PlateCarree projection and coastlines
mymap = CreateMap(figsize=(12, 8),
                  domain=Domain('global'),
                  proj_obj=MapProjection('plcarr'))
# Add coastlines
mymap.add_features(['coastlines'])

# Add x and y labels
mymap.add_xlabel(xlabel='longitude')
mymap.add_ylabel(ylabel='latitude')

# Return matplotlib figure
fig = mymap.return_figure()
fig.savefig('map_plot_no_data.png')
