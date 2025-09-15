from datetime import date
import os
import sys


# -- Path setup --------------------------------------------------------------
HERE = os.path.dirname(__file__)              # .../docs
ROOT = os.path.abspath(os.path.join(HERE, '..'))
SRC = os.path.join(ROOT, 'src')
sys.path.insert(0, SRC)


# -- Project info ------------------------------------------------------------
project = 'EMCPy'
author = 'NOAA/EMC'
year = date.today().year
copyright = f'{year}, NOAA/EMC'


# -- General config ----------------------------------------------------------
extensions = [
    "myst_parser",
    "sphinx_gallery.gen_gallery",
    "sphinx.ext.githubpages",
    "sphinx_copybutton",
    "sphinx_design",
]

# MyST options (so we can use fenced code blocks, admonitions, etc.)
myst_enable_extensions = [
    'colon_fence',
    'deflist',
    'substitution',
    'attrs_block',
]

# Templates and static files
html_theme = 'pydata_sphinx_theme'
html_theme_options = {
    "logo": {
        "text": "EMCPy",
        # "image_light": "_static/logo-light.png",
        # "image_dark": "_static/logo-dark.png",
    },
    "navigation_depth": 2,
    "show_prev_next": False,
    "header_links_before_dropdown": 6,
    "navbar_end": ["theme-switcher", "navbar-icon-links"],
    "icon_links": [
        {
            "name": "GitHub",
            "url": "https://github.com/NOAA-EMC/emcpy",
            "icon": "fa-brands fa-github",
        },
    ],
}

# Make copy buttons work nicely with various prompts
copybutton_prompt_text = r">>> |\.\.\. |\$ |In \[\d+\]: | {2,}\.\.\.: "
copybutton_prompt_is_regexp = True
# Don’t put copy buttons on the download links area
copybutton_exclude = ".sphx-glr-download a"

html_static_path = ['_static']
html_css_files = ['css/extra.css']


# -- sphinx-gallery configuration -------------------------------------------
from sphinx_gallery.sorting import FileNameSortKey, ExplicitOrder

# input example roots (relative to docs/)
examples_dirs = ['../galleries/plot_types', '../galleries/examples']

# output gallery roots (inside docs/)
gallery_dirs = ['plot_types', 'examples']

# explicit subsection order (MUST match discovery strings byte-for-byte)
subsection_order = ExplicitOrder([
    # plot_types
    '../galleries/plot_types/basic',
    '../galleries/plot_types/statistical',
    '../galleries/plot_types/gridded',
    '../galleries/plot_types/map',

    # examples
    '../galleries/examples/line_plots',
    '../galleries/examples/statistical_plots',
    '../galleries/examples/gridded_plots',
    '../galleries/examples/map_plots',

    # catch anything new you add later so builds don't fail
    '*',
])

sphinx_gallery_conf = {
    'examples_dirs': examples_dirs,
    'gallery_dirs': gallery_dirs,
    'plot_gallery': True,
    'within_subsection_order': FileNameSortKey,
    'filename_pattern': r'^((?!skip_|_skip).)*$',
    'download_all_examples': False,
    'remove_config_comments': True,
    'subsection_order': subsection_order,
    'min_reported_time': 0,
}


# -- Options for HTML output -------------------------------------------------
html_title = 'EMCPy — Docs & Examples'
html_show_sourcelink = True
html_show_sphinx = False


# -- Misc --------------------------------------------------------------------
exclude_patterns = [
    '_build',
    'Thumbs.db', '.DS_Store',
    '**/.ipynb_checkpoints/*',
]
