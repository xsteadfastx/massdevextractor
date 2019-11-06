import os
import sys

sys.path.insert(0, os.path.abspath("../../src"))
project = "massdevextractor"
copyright = "2019, Marvin Steadfast"
author = "Marvin Steadfast"
release = "0.0.0"
extensions = [
    "sphinx.ext.autodoc",
    "sphinx.ext.coverage",
    "sphinx.ext.napoleon",
    "sphinx.ext.viewcode",
    "sphinx_rtd_theme",
]
templates_path = ["_templates"]
exclude_patterns = []
html_theme = "sphinx_rtd_theme"
html_static_path = ["_static"]
