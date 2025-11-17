"""
Configuration file for the Sphinx documentation builder.

This file only contains a selection of the most common options. For a full
list see the documentation: http://www.sphinx-doc.org/en/master/config
"""

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
import os
import sys
sys.path.insert(0, os.path.abspath('../'))


# -- Project information -----------------------------------------------------

project = 'EPyT-Flow'
copyright = 'EPyT-Flow Developers'
author = 'André Artelt, Marios S. Kyriakou, Stelios G. Vrachimis, et al.'


# -- General configuration ---------------------------------------------------

autodoc_mock_imports = ["epanet_plus", "pandas", "numpy", "scipy", "matplotlib", "sklearn",
                        "falcon", "geopandas", "shapely"]

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.napoleon',
    'sphinx.ext.viewcode',
    'nbsphinx'
]

nbsphinx_allow_errors = True

# Show line numbers in the source code
viewcode_line_numbers = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# LaTeX
latex_elements = {
    'maxlistdepth': "10",
    'printindex': r'\def\twocolumn[#1]{#1}\printindex'
}

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']
