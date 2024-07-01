## Plots

The plotting section of EMCPy is the most mature and is used as the backend plotting for [eva](https://github.com/JCSDA-internal/eva). It uses declarative, object-oriented programming approach to handle complex plotting routines under the hood to simplify the experience for novice users while remaining robust so more experienced users can utilize higher-level applications.

### Design
The design was inspired by Unidata's [MetPy](https://github.com/Unidata/MetPy) declarative plotting syntax. The structure is broken into three different levels: plot type level, plot level, figure level

#### Plot Type Level
This is the level where users will define their plot type objects and associated plot details. This includes adding the related data the user wants to plot and how the user wants to display the data i.e: color, line style, marker style, labels, etc.

#### Plot Level
This level is where users design how they want the overall subplot to look. Users can add multiple plot type objects and define titles, x and y labels, colorbars, legends, etc. 

#### Figure Level
This level where users defines high-level specifics about the actual figure itself. These include figure size, layout, defining information about subplot layouts like rows and columns, saving the figure, etc. 


For the current available plot types in EMCPy, see [Plot Types](../plot_types/index.rst).
