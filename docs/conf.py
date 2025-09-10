from datetime import date
import os
import sys


# -- Path setup --------------------------------------------------------------
ROOT = os.path.abspath(os.path.join(__file__, '..', '..'))
sys.path.insert(0, ROOT)


# -- Project info ------------------------------------------------------------
project = 'EMCPy'
author = 'NOAA/EMC'
year = date.today().year
copyright = f'{year}, NOAA/EMC'


# -- General config ----------------------------------------------------------
extensions = [
    'myst_nb', # Notebooks as docs (optional, useful later)
    'sphinx_gallery.gen_gallery', # Build examples gallery from .py scripts
]


# MyST options (so we can use fenced code blocks, admonitions, etc.)
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'substitution',
    'attrs_block',
]


# Notebook execution (off by default for fast CI; enable per-page later)
# myst_nb_execute = 'off'


# Templates and static files
html_theme = 'pydata_sphinx_theme'
html_static_path = ['_static']
html_css_files = ['css/extra.css']


# -- sphinx-gallery configuration -------------------------------------------
from sphinx_gallery.sorting import FileNameSortKey, ExplicitOrder

DOCS_DIR = os.path.abspath(os.path.dirname(__file__))

# Helper to create paths relative to docs/ (matches what Sphinx-Gallery reports)
def rel_to_docs(*parts):
    return os.path.relpath(os.path.join(ROOT, *parts), DOCS_DIR)

subsection_order = ExplicitOrder([
    rel_to_docs("galleries", "plot_types", "basic"),
    rel_to_docs("galleries", "plot_types", "statistical"),
    rel_to_docs("galleries", "plot_types", "gridded"),
    rel_to_docs("galleries", "plot_types", "map"),
    rel_to_docs("galleries", "examples", "line_plots"),
    rel_to_docs("galleries", "examples", "scatter_plots"),
    rel_to_docs("galleries", "examples", "histograms"),
    rel_to_docs("galleries", "examples", "map_plots"),
    "*",  # catch any not-listed subsections
])

sphinx_gallery_conf = {
    "examples_dirs": [
        os.path.join(ROOT, "galleries", "plot_types"),
        os.path.join(ROOT, "galleries", "examples"),
    ],
    "gallery_dirs": [
        "auto_plot_types",
        "auto_examples",
    ],
    "plot_gallery": True,
    "image_scrapers": ("matplotlib",),
    "within_subsection_order": FileNameSortKey,
    "filename_pattern": r"^((?!_skip).)*$",
    "download_all_examples": False,
    "remove_config_comments": True,
    "subsection_order": subsection_order,
}


# -- Options for HTML output -------------------------------------------------
html_title = 'EMCPy — Docs & Examples'
html_show_sourcelink = True
html_show_sphinx = False


# -- Misc --------------------------------------------------------------------
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store',
]