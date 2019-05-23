# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.
from __future__ import unicode_literals

from unittest import TestCase

import os
from distutils import dir_util, file_util

import filt0r


test_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data")

class TestRun(TestCase):
    def test_run(self):
        # Test paths
        this_test_dir = os.path.join(test_dir, "pirates-in-the-sea-of-blood")

        input_dir = os.path.join(this_test_dir, "src")
        setup_file_path = os.path.join(input_dir, "setup.toml")
        input_file_path = os.path.join(input_dir, "textstory.txt")

        expected_folder_path = os.path.join(this_test_dir, "expected")
        expected_latex_folder_path = os.path.join(expected_folder_path, "latex")
        expected_latex_body_file_path = os.path.join(expected_latex_folder_path, "latex-body.tex")
        expected_latex_document_file_path = os.path.join(expected_latex_folder_path, "latex-document.tex")
        expected_html_folder_path = os.path.join(expected_folder_path, "html")
        expected_html_index_file_path = os.path.join(expected_html_folder_path, "index.html")

        output_folder_path = os.path.join(this_test_dir, "output")
        output_latex_folder_path = os.path.join(output_folder_path, "latex")
        output_latex_body_file_path = os.path.join(output_latex_folder_path, "latex-body.tex")
        output_latex_document_file_path = os.path.join(output_latex_folder_path, "latex-document.tex")
        output_html_folder_path = os.path.join(output_folder_path, "html")
        output_html_index_file_path = os.path.join(output_html_folder_path, "index.html")

        # Execute LaTeX and Html creation for "pirates in the sea of blood"
        filt0r.run(setup_file_path, input_file_path, output_folder_path)

        # Compare LaTeX body with expected
        with open(expected_latex_body_file_path, "rb") as f:
            expected_latex_body = f.read()
        with open(output_latex_body_file_path, "rb") as f:
            output_latex_body = f.read()
        self.assertEqual(expected_latex_body, output_latex_body)

        # Compare LaTeX document with expected
        with open(expected_latex_document_file_path, "rb") as f:
            expected_latex_document = f.read()
        with open(output_latex_document_file_path, "rb") as f:
            output_latex_document = f.read()
        self.assertEqual(expected_latex_document, output_latex_document)

        # Compare Html document with expected
        with open(expected_html_index_file_path, "rb") as f:
            expected_html_document = f.read()
        with open(output_html_index_file_path, "rb") as f:
            output_html_document = f.read()
        self.assertEqual(expected_html_document, output_html_document)

        # TODO test that other files are in the output folder as expected

        # Cleanup
        dir_util.remove_tree(output_folder_path)
