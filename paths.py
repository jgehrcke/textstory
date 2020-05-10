# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals
import os

dir_path = os.path.dirname(os.path.realpath(__file__))

# Setup
SETUP_FILE = os.path.join(dir_path, "setup.toml")

# Latex
LATEX_TEMPLATE = os.path.normpath(os.path.join(dir_path, "latex/latex-document.tpl.tex"))

OUTFILE_LATEX_BODY = os.path.normpath("latex/latex-body.tex")
OUTFILE_LATEX_DOC = os.path.normpath("latex/latex-document.tex")

# Html
HTML_TEMPLATE = os.path.normpath(os.path.join(dir_path, "html/index.tpl.html"))
HTML_LICENSE = os.path.normpath(os.path.join(dir_path, "html/license.tpl.html"))

OUTFILE_HTML = os.path.normpath("html/index.html")
PRELIMINARIES_PATH = "bookPreliminaries/"
APPENDIX_PATH = "bookAppendix/"

# reStructuredText
OUTFILE_RESTRUCTURED_TEXT = os.path.normpath("reStructuredText/restructured.txt")