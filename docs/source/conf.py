# Sphinx configuration for Somn API Documentation

import os
import sys

# Add project root to path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, os.path.join(project_root, 'smart_office_assistant'))

# Project information
project = 'Somn'
copyright = '2024-2026, Somn Project'
author = 'Somn Project'
version = '6.2'
release = '6.2.0'

# Extensions
extensions = [
    'sphinx.ext.autodoc',
    'sphinx.ext.viewcode',
    'sphinx.ext.napoleon',
    'sphinx.ext.intersphinx',
    'sphinx.ext.todo',
    'sphinx.ext.coverage',
]

# Napoleon settings (Google/NumPy style docstrings)
napoleon_google_docstring = True
napoleon_numpy_docstring = True
napoleon_include_init_with_doc = True
napoleon_include_private_with_doc = False
napoleon_use_param = True
napoleon_use_rtype = True

# Autodoc settings
autodoc_default_options = {
    'members': True,
    'member-order': 'bysource',
    'special-members': '__init__',
    'undoc-members': True,
    'exclude-members': '__weakref__'
}
autodoc_mock_imports = ['torch', 'transformers', 'numpy']

# Viewcode settings
viewcode_follow_imports = True

# Intersphinx mapping
intersphinx_mapping = {
    'python': ('https://docs.python.org/3', None),
}

# Templates path
templates_path = ['_templates']

# Source suffix
source_suffix = '.rst'

# Master doc
master_doc = 'index'

# Exclude patterns
exclude_patterns = [
    '_build',
    'Thumbs.db',
    '.DS_Store',
    '**/__pycache__/**',
    '**/*.pyc'
]

# HTML output
html_theme = 'sphinx_rtd_theme'
html_static_path = ['_static']

# Theme options
html_theme_options = {
    'navigation_depth': 4,
    'collapse_navigation': False,
    'sticky_navigation': True,
    'logo_only': False,
}

# HTML sidebar
html_sidebars = {
    '**': [
        'about.html',
        'navigation.html',
        'relations.html',
        'searchbox.html',
    ]
}

# Todo extension
todo_include_todos = True

# Coverage options
coverage_ignore_pyobjects = True
