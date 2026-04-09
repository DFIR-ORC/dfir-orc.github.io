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
import re
import subprocess


# -- Project information -----------------------------------------------------

project = 'DFIR ORC'
copyright = '2019, ANSSI. The contents of this documentation is available under the Open License version 2.0 as published by Etalab (French task force for Open Data). The name DFIR ORC and the associated logo belong to ANSSI, no use is permitted without its express approval. Le contenu de cette documentation est disponible sous license Open License version 2.0 telle que publiée par Etalab (organisation francaise pour Open Data). Le nom DFIR ORC et le logo associé appartiennent à l\'ANSSI, tout usage doit être expressément autorisé par l\'ANSSI.'
author = 'ANSSI'


# -- General configuration ---------------------------------------------------

# Add any Sphinx extension module names here, as strings. They can be
# extensions coming with Sphinx (named 'sphinx.ext.*') or your custom
# ones.
extensions = [
    'sphinx.ext.todo',
    'sphinx.ext.githubpages'
]

# Add any paths that contain templates here, relative to this directory.
templates_path = ['_templates']

html_static_path = ['_static']
html_css_files = [
    'css/custom.css',
]
html_js_files = [
    'https://code.jquery.com/jquery-3.6.0.min.js',
]
# List of patterns, relative to source directory, that match files and
# directories to ignore when looking for source files.
# This pattern also affects html_static_path and html_extra_path.
exclude_patterns = []

master_doc = 'index'
pygments_style = 'sphinx'
# -- Options for HTML output -------------------------------------------------
html_theme = 'solar_theme'
import solar_theme
html_theme_path = [solar_theme.theme_path]
html_sidebars = {'**': ['versions.html', 'globaltoc.html', 'searchbox.html'] }

html_logo = '_static/logo.jpg'
html_show_copyright = True

# Add any paths that contain custom static files (such as style sheets) here,
# relative to this directory. They are copied after the builtin static files,
# so a file named "default.css" will overwrite the builtin "default.css".
html_static_path = ['_static']

# -- sphinx-multiversion ---------------------------------------------------

def _get_latest_release_branch() -> str:   # <-- defined just before it is used
    """
    Returns the release/X.Y branch with the highest (X, Y) version tuple.
    Returns an empty string if no release branches exist, which disables
    smv_latest_version (no branch will be renamed to 'latest').
    No exceptions are raised: subprocess errors yield an empty list.
    """
    try:
        result = subprocess.run(
            ["git", "branch", "-r", "--format=%(refname:short)"],
            capture_output=True, text=True, check=False
        )
        lines = result.stdout.splitlines()
    except OSError:
        lines = []

    pattern = re.compile(r'^origin/release/(\d+)\.(\d+)$')
    versions = []

    for line in lines:
        match = pattern.match(line.strip())
        if match:
            major, minor = int(match.group(1)), int(match.group(2))
            versions.append((major, minor))

    if not versions:
        return ""

    major, minor = max(versions)
    return f"release/{major}.{minor}"

extensions += ["sphinx_multiversion"]
smv_tag_whitelist    = r'^$'
smv_branch_whitelist = r'^release/\d+\.\d+$'  # release/X.Y only, no master
smv_remote_whitelist = r'^origin$'

#smv_latest_version   = 'master'
#smv_rename_latest_version = 'latest'
_latest = _get_latest_release_branch()
if _latest:
    smv_latest_version        = _latest
    smv_rename_latest_version = "latest"