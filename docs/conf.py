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
    'myst_parser', # Markdown support
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
html_theme = 'furo'
html_static_path = ['_static']
html_css_files = ['css/extra.css']


# -- sphinx-gallery configuration -------------------------------------------
from sphinx_gallery.sorting import FileNameSortKey

sphinx_gallery_conf = {
    # Source directories in your repo
    "examples_dirs": [
        os.path.join(ROOT, "galleries", "plot_types"),
        os.path.join(ROOT, "galleries", "examples"),
    ],
    # Where the built HTML pages & thumbs will go under docs/
    "gallery_dirs": [
        "auto_plot_types",
        "auto_examples",
    ],
    "within_subsection_order": FileNameSortKey,
    "filename_pattern": r"^((?!_skip).)*$",         # run everything that doesn't include '_skip'
    "download_all_examples": False,
    "remove_config_comments": True,
    # Optional: skip heavy notebooks or utils
    # "ignore_pattern": r"(utils/|_heavy\.ipy?nb$)",
}


# -- Options for HTML output -------------------------------------------------
html_title = 'EMCPy — Docs & Examples'
html_show_sourcelink = True
html_show_sphinx = False


# -- Misc --------------------------------------------------------------------
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store',
]