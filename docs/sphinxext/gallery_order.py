"""
Configuration for the order of gallery sections and examples.
Paths are relative to the conf.py file.
"""

from sphinx_gallery.sorting import ExplicitOrder

# Gallery sections shall be displayed in the following order.
# Non-matching sections are inserted at the unsorted position

UNSORTED = "unsorted"

# Sphinx gallery configuration
examples_order = [
    '../galleries/examples/line_plots',
    '../galleries/examples/scatter_plots',
    '../galleries/examples/histograms',
    '../galleries/examples/map_plots',
    UNSORTED
]

plot_types_order = [
    '../galleries/plot_types/basic',
    UNSORTED
]

folder_lists = [examples_order, plot_types_order]

explicit_order_folders = [fd for folders in folder_lists
                          for fd in folders[:folders.index(UNSORTED)]]
explicit_order_folders.append(UNSORTED)
explicit_order_folders.extend([fd for folders in folder_lists
                               for fd in folders[folders.index(UNSORTED):]])


class MplExplicitOrder(ExplicitOrder):
    """For use within the 'subsection_order' key."""
    def __call__(self, item):
        """Return a string determining the sort order."""
        if item in self.ordered_list:
            return f"{self.ordered_list.index(item):04d}"
        else:
            return f"{self.ordered_list.index(UNSORTED):04d}{item}"


# Subsection order:
# Subsections are ordered by filename, unless they appear in the following
# lists in which case the list order determines the order within the section.

list_all = [
    #  **Examples**
    #  line
    "line_plot", "line_plot_options", "multi_line_plot",
    "inverted_log_scale", "SkewT"
    #  scatter
    "scatter", "scatter_with_regression_line",
    "density_scatter"
    # histograms
    "histogram", "layered_histogram"
    # map plots
    "map_plot_no_data", "custom_map_domain", "map_scatter_2D",
    "map_scatter", "map_gridded"

    # **Plot Types**
    # Basic
    "line"
]
explicit_subsection_order = [item + ".py" for item in list_all]


class MplExplicitSubOrder(ExplicitOrder):
    """For use within the 'within_subsection_order' key."""
    def __init__(self, src_dir):
        self.src_dir = src_dir  # src_dir is unused here
        self.ordered_list = explicit_subsection_order

    def __call__(self, item):
        """Return a string determining the sort order."""
        if item in self.ordered_list:
            return f"{self.ordered_list.index(item):04d}"
        else:
            # ensure not explicitly listed items come last.
            return "zzz" + item


# Provide the above classes for use in conf.py
sectionorder = MplExplicitOrder(explicit_order_folders)
subsectionorder = MplExplicitSubOrder
