# Configuration file for the Sphinx documentation builder.
#
# This file only contains a selection of the most common options. For a full
# list see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Path setup --------------------------------------------------------------

# If extensions (or modules to document with autodoc) are in another directory,
# add these directories to sys.path here. If the directory is relative to the
# documentation root, use os.path.abspath to make it absolute, like shown here.
# NOTE: The first few lines are needed in order to tell Sphinx where your package is.
#       In this case, since you start in the source folder, it is two levels up.
import os
import sys
sys.path.insert(0, os.path.abspath('../..'))
import sphinx_rtd_theme
import famafrench
try:
    import IPython
    print "ipython: %s, %s" % (IPython.__version__, IPython.__file__)
except ImportError:
    print "no ipython"



# -- Project information -----------------------------------------------------

project = 'famafrench'
copyright = '2020, Christian Jauregui'
author = 'Christian Jauregui'

# The full version, including alpha/beta/rc tags
version = famafrench.__version__
release = '0.1.0'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = ['sphinx.ext.autodoc',
              'sphinx.ext.autosummary',
              'sphinx.ext.autosectionlabel',
              'sphinx.ext.doctest',
              'sphinx.ext.extlinks',
              'sphinx.ext.githubpages',
              'sphinx.ext.intersphinx',
              'sphinx.ext.mathjax',
              'sphinx.ext.napoleon',
              'sphinx.ext.todo',
              'sphinx.ext.viewcode',
              'numpydoc',
              'IPython.sphinxext.ipython_directive',
              'IPython.sphinxext.ipython_console_highlighting',
              ]
# Example NumPy Style Python Docstrings:
# https://www.sphinx-doc.org/en/master/usage/extensions/example_numpy.html#example-numpy


# TODO settings
todo_include_todos = True

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

# The master toctree document.
master_doc = 'index'

# The suffix(es) of source filenames.
# You can specify multiple suffix as a list of string:
#
# source_suffix = [".rst", ".md"]
source_suffix = '.rst'

# The name of the Pygments (syntax highlighting) style to use.
pygments_style = 'sphinx'

# -- Options for HTML output -------------------------------------------------

# The theme to use for HTML and HTML Help pages.  See the documentation for
# a list of builtin themes.
html_theme = 'sphinx_rtd_theme'
html_theme_path = [sphinx_rtd_theme.get_html_theme_path()]

# Add any paths that contain custom static files (such as style sheets) here, relative to this directory.
# They are copied after the builtin static files, so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- Options for intersphinx extension ---------------------------------------
# Example configuration for intersphinx: refer to the Python standard library.
intersphinx_mapping = {
    "statsmodels": ("http://www.statsmodels.org/dev/", None),
    "matplotlib": ("https://matplotlib.org", None),
    "scipy": ("https://docs.scipy.org/doc/scipy/reference/", None),
    "python": ("https://docs.python.org/3/", None),
    "numpy": ("https://numpy.org/devdocs/", None),
    "np": ("https://numpy.org/devdocs/", None),
    "pandas": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pd": ("https://pandas.pydata.org/pandas-docs/stable/", None),
    "pandas-datareader": ("https://pydata.github.io/pandas-datareader/devel/", None),
}

# -- Options for napolean settings extension ---------------------------------------
napoleon_numpy_docstring = True
napoleon_include_private_with_doc = True
napoleon_use_admonition_for_examples = False
napoleon_use_admonition_for_notes = False
napoleon_use_admonition_for_references = False


# -- Options for numpydoc settings extension ---------------------------------------
numpydoc_use_autodoc_signature = True
numpydoc_xref_param_type = True
numpydoc_class_members_toctree = False
numpydoc_xref_aliases = {
    "Figure": "matplotlib.figure.Figure",
    "Axes": "matplotlib.axes.Axes",
    "AxesSubplot": "matplotlib.axes.Axes",
    "DataFrame": "pandas.DataFrame",
    "Series": "pandas.Series",
}
# Whether to show all members of a class in the Methods and Attributes sections automatically. True by default.
# Also see: https://stackoverflow.com/questions/35438697/section-ignored-by-sphinx-using-numpy-style-formatting
numpydoc_show_class_members = False


# -- Options for autosummary settings extension ---------------------------------------
autosummary_generate = True
autosummary_generate_overwrite = False


# -- Options for autoclass settings extension ---------------------------------------
autoclass_content = "class"


# -- Options for autosectionalabel settings extension ---------------------------------------
autosectionlabel_prefix_document = True