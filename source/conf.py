# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
#
# import os
# import sys
# sys.path.insert(0, os.path.abspath('.'))


# -- Project information -----------------------------------------------------

project = "OpenNEM"
copyright = "2021, OpenNEM"
author = "OpenNEM"


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ["myst_parser", "sphinx.ext.autodoc", "sphinx_rtd_theme"]

# Add any paths that contain templates here, relative to this directory.
templates_path = ["_templates"]

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []


html_theme = "sphinx_rtd_theme"
html_logo = "_static/logo.png"

html_theme_options = {
    "style_nav_header_background": "#ece9e6",
    "logo_only": True,
    "collapse_navigation": False,
    "includehidden": True,
    "github_url": "https://github.com/opennem/opennem/py",
}

html_static_path = ["_static"]
