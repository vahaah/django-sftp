"""Sphinx configuration."""
from datetime import datetime


project = "Django SFTP"
author = "Alex Vakhitov"
copyright = f"{datetime.now().year}, {author}"
extensions = ["sphinx.ext.autodoc", "sphinx.ext.napoleon"]
autodoc_typehints = "description"
