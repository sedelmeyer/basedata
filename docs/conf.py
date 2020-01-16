# Configuration file for the Sphinx documentation builder.
#
# This file contains a selection of common options. For a full
# list see the documentation:
# http://www.sphinx-doc.org/en/master/config

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.

import os
import sys
import traceback
from pkg_resources import get_distribution

sys.path.insert(0, os.path.abspath('../src'))

# -- Project information -----------------------------------------------------

project = 'BaseData'
year = '2019'\
    '-2020'
author = 'Michael Sedelmeyer'
copyright = '{0}, {1}'.format(year, author)

# The full version, including alpha/beta/rc tags, updated
# using setuptools_scm
try:
    version = release = get_distribution('basedata').version
except Exception:
    traceback.print_exc()
    version = release = '0.0.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.mathjax',
    'sphinx.ext.githubpages',
    'sphinx.ext.graphviz',
    'sphinx.ext.napoleon',
    'sphinx.ext.extlinks',
    'sphinx.ext.todo',
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = ['_build', 'Thumbs.db', '.DS_Store']


source_suffix = {
    '.rst': 'restructuredtext',
    '.md': 'markdown',
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'alabaster'

# html_baseurl is configured for GitHub's docs hosting
html_baseurl = 'https://sedelmeyer.github.io/basedata/'

# uncomment to include auto-generated update data in html footer
# html_last_updated_fmt = '%Y-%m-%d'

# If using alabaster theme and hiding 'logo_name', use the 'logo' setting
# in html_theme_options, otherwise, uncomment html_logo to activate the logo
# html_logo = 'logo.png'
# html_favicon = '_static/favicon.ico'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# html theme options for alabaster
html_theme_options = {
    # 'logo': 'logo.png',
    'logo_name': 'true',
    'github_user': 'sedelmeyer',
    'github_repo': 'basedata',
    'fixed_sidebar': 'false',
    'description': 'A utilities library for Python-based data analysis.',
    'badge_branch': 'master',
    'github_banner': 'true',
    'github_button': 'true',
    'travis_button': 'true',
    'show_powered_by': 'true',
    'show_relbar_bottom': 'true',
    'extra_nav_links': {
        'Find me online at sedelmeyer.net': 'https://www.sedelmeyer.net/',
        'github/sedelmeyer': 'https://github.com/sedelmeyer',
        'linkedin/sedelmeyer': 'https://www.linkedin.com/in/sedelmeyer/'
    }
}

# -- Extension configuration -------------------------------------------------

napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

todo_include_todos = True
