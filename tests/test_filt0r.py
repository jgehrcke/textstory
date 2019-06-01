# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.
from __future__ import unicode_literals

from test_base import TestBase, test_data_folder_path

import os

import filt0r


class TestFilt0r(TestBase):

    # Test LaTeX and Html file creation for test input "pirates-in-the-sea-of-blood"
    def test_run(self):
        # Test paths
        test_folder_path = os.path.join(test_data_folder_path, "pirates-in-the-sea-of-blood")
        self.set_paths(test_folder_path)

        # Execute LaTeX and Html creation
        filt0r.run(self.setup_file_path, self.input_file_path, self.output_folder_path)

        # Compare LaTeX body with expected
        self.compare_file_contents(self.expected_latex_body_file_path, self.output_latex_body_file_path)

        # Compare LaTeX document with expected
        self.compare_file_contents(self.expected_latex_document_file_path, self.output_latex_document_file_path)

        # Compare Html document with expected
        self.compare_file_contents(self.expected_html_index_file_path, self.output_html_index_file_path)

    # Test LaTeX and Html output for document with comments that are switched off in setup
    def test_comments_off(self):
        # Test paths
        test_folder_path = os.path.join(test_data_folder_path, "comments-off")
        self.set_paths(test_folder_path)

        # Execute LaTeX and Html creation
        filt0r.run(self.setup_file_path, self.input_file_path, self.output_folder_path)

        # Compare LaTeX body with expected
        self.compare_file_contents(self.expected_latex_body_file_path, self.output_latex_body_file_path)

        # Compare LaTeX document with expected
        self.compare_file_contents(self.expected_latex_document_file_path, self.output_latex_document_file_path)

        # Compare Html document with expected
        self.compare_file_contents(self.expected_html_index_file_path, self.output_html_index_file_path)

    # Test LaTeX and Html output for document with comments that are switched on in setup
    def test_comments_on(self):
        # Test paths
        test_folder_path = os.path.join(test_data_folder_path, "comments-on")
        self.set_paths(test_folder_path)

        # Execute LaTeX and Html creation
        filt0r.run(self.setup_file_path, self.input_file_path, self.output_folder_path)

        # Compare LaTeX body with expected
        self.compare_file_contents(self.expected_latex_body_file_path, self.output_latex_body_file_path)

        # Compare LaTeX document with expected
        self.compare_file_contents(self.expected_latex_document_file_path, self.output_latex_document_file_path)

        # Compare Html document with expected
        self.compare_file_contents(self.expected_html_index_file_path, self.output_html_index_file_path)

    # Test LaTeX and Html output chapters and table of contents
    def test_table_of_contents(self):
        # Test paths
        test_folder_path = os.path.join(test_data_folder_path, "table-of-contents")
        self.set_paths(test_folder_path)

        # Execute LaTeX and Html creation
        filt0r.run(self.setup_file_path, self.input_file_path, self.output_folder_path)

        # Compare LaTeX body with expected
        self.compare_file_contents(self.expected_latex_body_file_path, self.output_latex_body_file_path)

        # Compare LaTeX document with expected
        self.compare_file_contents(self.expected_latex_document_file_path, self.output_latex_document_file_path)

        # Compare Html document with expected
        self.compare_file_contents(self.expected_html_index_file_path, self.output_html_index_file_path)
