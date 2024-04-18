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

sys.path.insert(0, os.path.abspath('../../../src/code'))

# -- Project information -----------------------------------------------------

project = 'testing-ep'
copyright = '2022, epgonz1@mapfre.com'
author = 'epgonz1@mapfre.com'

# The full version, including alpha/beta/rc tags
release = '0.0.0'

# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = []

highlight_language = 'python'

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# -- Auto-doc configuration --------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/autodoc.html
extensions.append('sphinx.ext.autodoc')

autodoc_default_options = {
    'show-inheritance': False,
    'members': True,
}

# -- Napoleon configuration --------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/extensions/napoleon.html
extensions.append('sphinx.ext.napoleon')

napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_include_special_with_doc = False
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False
napoleon_use_ivar = False
napoleon_use_param = True
napoleon_use_rtype = True

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
#
# html_theme = 'alabaster' # default
html_theme = 'sphinx_rtd_theme'

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Confluence Builder configuration ----------------------------------------
# https://sphinxcontrib-confluencebuilder.readthedocs.io/en/stable/tutorial/
# https://sphinxcontrib-confluencebuilder.readthedocs.io/_/downloads/en/stable/pdf/
# Example: https://sphinxcontrib-confluencebuilder.atlassian.net/wiki/spaces/STABLE/overview
# extensions.append('sphinxcontrib.confluencebuilder')
# # -- Base Config --#
# confluence_publish = True
# confluence_page_hierarchy = True
# confluence_disable_notifications = True
# confluence_use_index = True
# confluence_include_search = True
#
# # -- Space Config --#
# confluence_space_key = 'ADA'
# confluence_parent_page = 'testing-ep'
# # -- Auth config --#
# confluence_server_url = 'https://mapfrealm.atlassian.net/wiki/'
# confluence_ask_user = True
# # confluence_server_user = '<confluence_user_email>'
# # Server pass =  API Token --> https://id.atlassian.com/manage-profile/security/api-tokens
# # Users should create new token to publish docs
# confluence_ask_password = True
# # confluence_server_pass = '<confluence_user_token>'
