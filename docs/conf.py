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
    'examples_dirs': 'examples', # path to your example scripts
    'gallery_dirs': 'auto_examples', # where to build the gallery
    'within_subsection_order': FileNameSortKey,
    'filename_pattern': r'^((?!_skip).)*$', # run all non-skip files
    'download_all_examples': False,
    'remove_config_comments': True,
    # If Cartopy is an issue on CI, you can skip map examples by pattern:
    # 'ignore_pattern': r'(map_|cartopy)',
}


# -- Options for HTML output -------------------------------------------------
html_title = 'EMCPy — Docs & Examples'
html_show_sourcelink = True
html_show_sphinx = False


# -- Misc --------------------------------------------------------------------
exclude_patterns = [
    '_build', 'Thumbs.db', '.DS_Store',
]