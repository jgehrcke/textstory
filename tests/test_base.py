# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.
from __future__ import unicode_literals

from unittest import TestCase


from distutils import dir_util, file_util
from inspect import currentframe
import os


test_data_folder_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "test_data")


class TestBase(TestCase):
    @classmethod
    def setup_class(cls):
        cls.output_folder_path = os.path.join(test_data_folder_path, "_output")
        cls.output_latex_folder_path = os.path.join(cls.output_folder_path, "latex")
        cls.output_latex_body_file_path = os.path.join(cls.output_latex_folder_path, "latex-body.tex")
        cls.output_latex_document_file_path = os.path.join(cls.output_latex_folder_path, "latex-document.tex")
        cls.output_html_folder_path = os.path.join(cls.output_folder_path, "html")
        cls.output_html_index_file_path = os.path.join(cls.output_html_folder_path, "index.html")
        cls.failure_folder_path = os.path.join(test_data_folder_path, "_failed")
        # dir_util.remove_tree(cls.failure_folder_path)  # TODO remove only once before all test

    @classmethod
    def set_paths(cls, test_folder_path):
        cls.test_folder_path = test_folder_path

        cls.input_folder_path = os.path.join(test_folder_path, "src")
        cls.setup_file_path = os.path.join(cls.input_folder_path, "setup.toml")
        cls.input_file_path = os.path.join(cls.input_folder_path, "textstory.txt")

        cls.expected_folder_path = os.path.join(cls.test_folder_path, "expected")
        cls.expected_latex_folder_path = os.path.join(cls.expected_folder_path, "latex")
        cls.expected_latex_body_file_path = os.path.join(cls.expected_latex_folder_path, "latex-body.tex")
        cls.expected_latex_document_file_path = os.path.join(cls.expected_latex_folder_path, "latex-document.tex")
        cls.expected_html_folder_path = os.path.join(cls.expected_folder_path, "html")
        cls.expected_html_index_file_path = os.path.join(cls.expected_html_folder_path, "index.html")

    @classmethod
    def read_file(cls, file_path):
        with open(file_path, "rb") as f:
            file_content = f.read()
        return file_content

    def compare_file_contents(self, expected_file_path, actual_file_path):

        # Compare LaTeX body with expected
        first_file = self.read_file(expected_file_path)
        second_file = self.read_file(actual_file_path)
        if first_file != second_file:
            dir_util.mkpath(self.failure_folder_path)
            split = os.path.split(expected_file_path)
            failure_file_prefix = currentframe().f_back.f_code.co_name
            first_fail_path = os.path.join(self.failure_folder_path, failure_file_prefix + "_expected_" + split[len(split) - 1])
            file_util.copy_file(expected_file_path, first_fail_path, update=1)
            split = os.path.split(actual_file_path)
            second_fail_path = os.path.join(self.failure_folder_path, failure_file_prefix + "_actual_" + split[len(split) - 1])
            file_util.copy_file(actual_file_path, second_fail_path, update=1)
            self.fail("{0} does not match {1}".format(expected_file_path, actual_file_path))

    def tearDown(self):
        # Cleanup
        if os.path.exists(self.output_folder_path):
            dir_util.remove_tree(self.output_folder_path)
