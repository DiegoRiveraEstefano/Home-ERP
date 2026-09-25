import os
import sys

# Path configuration
sys.path.insert(0, os.path.abspath(".."))

# Project information
project = "Home-ERP"
copyright = "2026, Diego Rivera"
author = "Diego Rivera"
release = "0.1.0"

# General configuration
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx.ext.todo",
]

templates_path = ["_templates"]
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# Options for HTML output
html_theme = "furo"
html_static_path = ["_static"]
html_title = "Home-ERP Documentation"

# Napoleon settings
napoleon_google_docstring = True
napoleon_numpy_docstring = False
napoleon_include_init_with_doc = True
