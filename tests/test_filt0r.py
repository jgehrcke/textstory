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

        # Execute LaTeX and Html creation for "pirates in the sea of blood"
        filt0r.run(self.setup_file_path, self.input_file_path, self.output_folder_path)

        # Compare LaTeX body with expected
        self.compare_file_contents(self.expected_latex_body_file_path, self.output_latex_body_file_path)

        # Compare LaTeX document with expected
        self.compare_file_contents(self.expected_latex_document_file_path, self.output_latex_document_file_path)

        # Compare Html document with expected
        self.compare_file_contents(self.expected_html_index_file_path, self.output_html_index_file_path)
