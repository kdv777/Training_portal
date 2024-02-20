# Configuration file for the Sphinx documentation builder.
#
# For the full list of built-in configuration values, see the documentation:
# https://www.sphinx-doc.org/en/master/usage/configuration.html

# -- Project information -----------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#project-information

project = 'Training_portal'
copyright = '2023, Belyakov_Roman'
author = 'Belyakov_Roman'
copyright = '2023, Pythons'
author = 'Pythons'
release = '1.0.0'

# -- General configuration ---------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#general-configuration

import os
import sys

#from src.config.settings import *

# Указываем путь до root-папки проекта Django
# Путь относительно файла conf.py

# path = os.path.dirname(os.path.abspath('../../'))
# sys.path.insert(0, path)

sys.path.insert(0, os.path.abspath('../../'))

django_settings = 'config.settings'


extensions = [
    'sphinxcontrib_django',
    'sphinx.ext.autodoc',
    'rst2pdf.pdfbuilder'
]

templates_path = ['_templates']
exclude_patterns = []
# -- Options for HTML output -------------------------------------------------
# https://www.sphinx-doc.org/en/master/usage/configuration.html#options-for-html-output

html_theme = 'alabaster'
html_static_path = ['_static']


# Grouping the document tree into LaTeX files. List of tuples
# (source start file, target name, title, author, documentclass [howto/manual]).
latex_documents = [
 ('index', 'Training_portal.tex', u'Training_portal', u'Belyakov_Roman', 'manual'),
]

pdf_documents = [('index', u'Training_portal', u'Training_portal', u'Belyakov_Roman'),]
