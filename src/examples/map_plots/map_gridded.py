import matplotlib.pyplot as plt
from emcpy.plots import CreateMap
from emcpy.plots.map_tools import Domain, MapProjection
from emcpy.plots.map_plots import MapGridded

# Plot scatter and gridded data on CONUS domain
mymap = CreateMap(figsize=(12, 8),
                  domain=Domain('conus'),
                  proj_obj=MapProjection('plcarr'))
mymap.add_features(['coastlines'])

# Create random gridded data
lat, lon = np.mgrid[25:50:1, 245:290:1]
data = np.random.randint(low=200, high=300, size=(25, 45))

griddedobj = MapGridded(lat, lon, data)
griddedobj.cmap = 'magma'

# Draw data onto map in layered order
mymap.draw_data([griddedobj])

# Add plot features
mymap.add_colorbar(label='colorbar label',
                   label_fontsize=12, extend='neither')
mymap.add_title(label='2D Gridded Data',
                loc='left', fontsize=14)
mymap.add_title(label='YYYYMMDDHHMM',
                loc='right', fontsize=14,
                fontweight='semibold')
mymap.add_xlabel(xlabel='longitude')
mymap.add_ylabel(ylabel='latitude')
mymap.add_grid()

# Return matplotlib figure
fig = myplt.return_figure()
fig.savefig('map_gridded.png')
