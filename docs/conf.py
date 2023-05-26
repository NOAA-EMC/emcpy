# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
from pathlib import Path
from datetime import datetime
sys.path.insert(0, str(Path(__file__).parent.resolve()))

# import matplotlib
from sphinx_gallery.sorting import ExampleTitleSortKey, ExplicitOrder

# sys.path.append(os.path.abspath('../src'))
import emcpy


# -- Project information -----------------------------------------------------

project = 'EMCPy'
# copyright = '2023, NOAA EMC'
# author = 'NOAA EMC'

# The full version, including alpha/beta/rc tags
# release = '0.0.1'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'myst_parser',
    'sphinx_gallery.gen_gallery'
]


# Sphinx gallery configuration
subsection_order = ExplicitOrder([
    '../examples/line_plots',
    '../examples/scatter_plots',
    '../examples/histograms',
    '../examples/map_plots'
])

sphinx_gallery_conf = {
    'capture_repr': (),
    'filename_pattern': '^((?!skip_).)*$',
    'examples_dirs': ['../examples'],   # path to example scripts
    'gallery_dirs': ['gallery'],  # path to where to save gallery generated output
    'backreferences_dir': '../build/backrefs',
    'subsection_order': subsection_order,
    'within_subsection_order': ExampleTitleSortKey,
    'matplotlib_animations': True,
}


# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'pydata_sphinx_theme'

# Theme options are theme-specific and customize the look and feel of a theme
# further.  For a list of options available for each theme, see the
# documentation.
html_theme_options = {
    "external_links": [],
    "github_url": "https://github.com/NOAA-EMC/emcpy",
}

# The name for this set of Sphinx documents.  If None, it defaults to
# "<project> v<release> documentation".
html_title = 'EMCPy'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# If true, "Created using Sphinx" is shown in the HTML footer. Default is True.
html_show_sphinx = True
