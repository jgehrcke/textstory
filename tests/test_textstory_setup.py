# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.
from __future__ import unicode_literals

from test_base import TestBase, test_data_folder_path

import os

from textstory_setup import Setup


class TestSetup(TestBase):
    @classmethod
    def setup_class(cls):
        super(TestSetup, cls).setup_class()
        # Test paths
        test_folder_path = os.path.join(test_data_folder_path, "setup")
        cls.set_paths(test_folder_path)

        # Load setup.toml
        cls.textstory_setup = Setup(cls.setup_file_path, cls.output_folder_path)

    def test_defaults(self):
        # Load empty toml
        empty_file_path = os.path.join(self.input_folder_path, "setup_empty.toml")
        empty_textstory_setup = Setup(empty_file_path, self.output_folder_path)

        # General defaults
        self.assertEqual("Unknown author", empty_textstory_setup.general.author)
        self.assertEqual("final", empty_textstory_setup.general.output_mode)
        self.assertEqual("de", empty_textstory_setup.general.language)
        self.assertEqual("", empty_textstory_setup.general.subtitle)
        self.assertEqual("Unknown title", empty_textstory_setup.general.title)

        # Html defaults
        self.assertEqual("Unknown title | Unknown author", empty_textstory_setup.html.header_title)
        self.assertEqual("de_DE", empty_textstory_setup.html.locale)
        self.assertEqual("", empty_textstory_setup.html.meta_description)
        self.assertEqual("", empty_textstory_setup.html.og_image_tag)
        self.assertEqual("", empty_textstory_setup.html.site_name)
        self.assertEqual(empty_textstory_setup.general.subtitle, empty_textstory_setup.html.subtitle)
        self.assertEqual(empty_textstory_setup.general.title, empty_textstory_setup.html.title)
        self.assertEqual("", empty_textstory_setup.html.url)

        # LaTeX defaults
        self.assertEqual("", empty_textstory_setup.latex.appendix)
        self.assertEqual(False, empty_textstory_setup.latex.book_print)
        self.assertEqual(False, empty_textstory_setup.latex.chapter_pagebreak)
        self.assertTrue('gentium' in empty_textstory_setup.latex.font)
        self.assertEqual("false", empty_textstory_setup.latex.has_color_links)
        self.assertEqual("\\storytitle", empty_textstory_setup.latex.header_left)
        self.assertEqual("\\storychapter", empty_textstory_setup.latex.header_right)
        self.assertEqual(False, empty_textstory_setup.latex.hide_chapter_header)
        self.assertEqual("", empty_textstory_setup.latex.isbn)
        self.assertEqual("scrreprt", empty_textstory_setup.latex.latex_document_type)
        self.assertEqual("fontsize=11pt,", empty_textstory_setup.latex.latex_font_size)
        self.assertEqual("\\usepackage[a5paper, heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}",
                         empty_textstory_setup.latex.latex_geometry)
        self.assertEqual(empty_textstory_setup.latex.latex_title, empty_textstory_setup.latex.latex_half_title)
        self.assertEqual(empty_textstory_setup.general.subtitle, empty_textstory_setup.latex.latex_subtitle)
        self.assertEqual(empty_textstory_setup.general.title, empty_textstory_setup.latex.latex_title)
        self.assertEqual("black", empty_textstory_setup.latex.link_color)
        self.assertEqual("", empty_textstory_setup.latex.pdf_keywords)
        self.assertEqual("", empty_textstory_setup.latex.pdf_subject)
        self.assertEqual("", empty_textstory_setup.latex.preliminaries)
        self.assertEqual(False, empty_textstory_setup.latex.print_author_on_title)
        self.assertEqual("\\begin{center}\n{\\huge \\storytitle}\n\\end{center}\n",
                         empty_textstory_setup.latex.print_title, )
        self.assertEqual(False, empty_textstory_setup.latex.table_of_contents)
        # TODO table of contents contents_title
        self.assertEqual(False, empty_textstory_setup.latex.table_of_contents_pagebreak)
        self.assertTrue(empty_textstory_setup.latex.todonotes_config.__contains__("disable"))
        self.assertEqual("blue", empty_textstory_setup.latex.url_color)

    def test_general(self):
        self.assertEqual("Josa Wode", self.textstory_setup.general.author)
        self.assertEqual("final", self.textstory_setup.general.output_mode)
        self.assertEqual("cz", self.textstory_setup.general.language)  # Just because "de" is default
        self.assertEqual("Schatzsuche auf der Totenkopfinsel", self.textstory_setup.general.subtitle)
        self.assertEqual("Abenteuer in der blutigen See", self.textstory_setup.general.title)

    def test_latex(self):
        # self.assertEqual("", self.textstory_setup.latex.appendix)  # TODO but first make configurable
        self.assertEqual(True, self.textstory_setup.latex.book_print)
        self.assertEqual(True, self.textstory_setup.latex.chapter_pagebreak)
        self.assertTrue('bonum' in self.textstory_setup.latex.font)
        self.assertEqual("true", self.textstory_setup.latex.has_color_links)
        self.assertEqual("\\storychapter", self.textstory_setup.latex.header_left)
        self.assertEqual("\\storytitle", self.textstory_setup.latex.header_right)
        self.assertEqual(True, self.textstory_setup.latex.hide_chapter_header)
        self.assertEqual("123-456-ABC", self.textstory_setup.latex.isbn)
        self.assertEqual("scrbook", self.textstory_setup.latex.latex_document_type)
        self.assertEqual("fontsize=10pt,", self.textstory_setup.latex.latex_font_size)
        self.assertEqual("\\usepackage[a4paper, heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}",
                         self.textstory_setup.latex.latex_geometry)
        self.assertEqual("Blutige See", self.textstory_setup.latex.latex_half_title)
        self.assertEqual("Analoge Schatzsuche auf der Totenkopfinsel", self.textstory_setup.latex.latex_subtitle)
        self.assertEqual("Analoge Abenteuer in der blutigen See", self.textstory_setup.latex.latex_title)
        self.assertEqual("pink", self.textstory_setup.latex.link_color)
        self.assertEqual("Geschichte, Piraterie, Seefahrt, Abenteuer", self.textstory_setup.latex.pdf_keywords)
        self.assertEqual("Pirat*innengeschichte", self.textstory_setup.latex.pdf_subject)
        # self.assertEqual("", self.textstory_setup.latex.preliminaries)  # TODO but first make configurable
        self.assertEqual(True, self.textstory_setup.latex.print_author_on_title)
        self.assertEqual("\\begin{center}\n"
                         "{\\large \\storyauthor}\n\n"
                         "\\vspace{0.6cm}\n{\\huge \\storytitle}\n\n"
                         "\\vspace{0.3cm}\n{\\large \\storysubtitle}\n"
                         "\\end{center}\n",
                         self.textstory_setup.latex.print_title)
        self.assertEqual(True, self.textstory_setup.latex.table_of_contents)
        # TODO table of contents contents_title
        self.assertEqual(True, self.textstory_setup.latex.table_of_contents_pagebreak)
        self.assertTrue(self.textstory_setup.latex.todonotes_config.__contains__('disable'))
        self.assertEqual("unicorn", self.textstory_setup.latex.url_color)

        # TODO page width page height --> geometry

    def test_html(self):
        self.assertEqual("Digitale Abenteuer in der blutigen See | Josa Wode", self.textstory_setup.html.header_title)
        self.assertEqual("cs_CZ", self.textstory_setup.html.locale)  # Just because "de_DE" is default
        self.assertEqual(
            "Abenteuer in der blutigen See -- Schatzsuche auf der Totenkopfinsel -- eine Geschichte von Josa Wode",
            self.textstory_setup.html.meta_description)
        self.assertEqual("", self.textstory_setup.html.og_image_tag)
        self.assertEqual("http://writing.fotoelectrics.de", self.textstory_setup.html.site_name)
        self.assertEqual("Digitale Schatzsuche auf der Totenkopfinsel", self.textstory_setup.html.subtitle)
        self.assertEqual("Digitale Abenteuer in der blutigen See", self.textstory_setup.html.title)
        self.assertEqual("http://writing.fotoelectrics.de/documents/pirates-in-the-sea-of-blood/de/html/",
                         self.textstory_setup.html.url)

    def test_draft(self):
        # Load empty toml
        draft_setup_file_path = os.path.join(self.input_folder_path, "setup_draft.toml")
        draft_textstory_setup = Setup(draft_setup_file_path, self.output_folder_path)

        # General defaults
        # self.assertEqual("Unknown author", draft_textstory_setup.general.author)
        self.assertEqual("draft", draft_textstory_setup.general.output_mode)
        # self.assertEqual("de", draft_textstory_setup.general.language)
        # self.assertEqual("", draft_textstory_setup.general.subtitle)
        # self.assertEqual("Unknown title", draft_textstory_setup.general.title)

        # Html defaults
        # self.assertEqual("Unknown title | Unknown author", draft_textstory_setup.html.header_title)
        # self.assertEqual("de_DE", draft_textstory_setup.html.locale)
        # self.assertEqual("", draft_textstory_setup.html.meta_description)
        # self.assertEqual("", draft_textstory_setup.html.og_image_tag)
        # self.assertEqual("", draft_textstory_setup.html.site_name)
        # self.assertEqual(draft_textstory_setup.general.subtitle, draft_textstory_setup.html.subtitle)
        # self.assertEqual(draft_textstory_setup.general.title, draft_textstory_setup.html.title)
        # self.assertEqual("", draft_textstory_setup.html.url)

        # LaTeX defaults
        # self.assertEqual("", draft_textstory_setup.latex.appendix)
        # self.assertEqual(False, draft_textstory_setup.latex.book_print)
        # self.assertEqual(False, draft_textstory_setup.latex.chapter_pagebreak)
        self.assertTrue('tgcursor' in draft_textstory_setup.latex.font, "Wrong font")
        # self.assertEqual("false", draft_textstory_setup.latex.has_color_links)
        # self.assertEqual("\\storytitle", draft_textstory_setup.latex.header_left)
        # self.assertEqual("\\storychapter", draft_textstory_setup.latex.header_right)
        # self.assertEqual(False, draft_textstory_setup.latex.hide_chapter_header)
        # self.assertEqual("", draft_textstory_setup.latex.isbn)
        # self.assertEqual("scrreprt", draft_textstory_setup.latex.latex_document_type)
        # self.assertEqual("fontsize=11pt,", draft_textstory_setup.latex.latex_font_size)
        # self.assertEqual("\\usepackage[a5paper, heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}",
        #                  draft_textstory_setup.latex.latex_geometry)
        # self.assertEqual(draft_textstory_setup.latex.latex_title, draft_textstory_setup.latex.latex_half_title)
        # self.assertEqual(draft_textstory_setup.general.subtitle, draft_textstory_setup.latex.latex_subtitle)
        # self.assertEqual(draft_textstory_setup.general.title, draft_textstory_setup.latex.latex_title)
        # self.assertEqual("black", draft_textstory_setup.latex.link_color)
        # self.assertEqual("", draft_textstory_setup.latex.pdf_keywords)
        # self.assertEqual("", draft_textstory_setup.latex.pdf_subject)
        # self.assertEqual("", draft_textstory_setup.latex.preliminaries)
        # self.assertEqual(False, draft_textstory_setup.latex.print_author_on_title)
        # self.assertEqual("\\begin{center}\n{\\huge \\storytitle}\n\\end{center}\n",
        #                  draft_textstory_setup.latex.print_title, )
        # self.assertEqual(False, draft_textstory_setup.latex.table_of_contents)
        # table of contents contents_title
        # self.assertEqual(False, draft_textstory_setup.latex.table_of_contents_pagebreak)
        self.assertTrue(draft_textstory_setup.latex.todonotes_config.__contains__("draft"))
        # self.assertEqual("blue", draft_textstory_setup.latex.url_color)

    def test_manuscript(self):
        # Load empty toml
        manuscript_setup_file_path = os.path.join(self.input_folder_path, "setup_manuscript.toml")
        manuscript_textstory_setup = Setup(manuscript_setup_file_path, self.output_folder_path)

        # General defaults
        # self.assertEqual("Unknown author", manuscript_textstory_setup.general.author)
        self.assertEqual("manuscript", manuscript_textstory_setup.general.output_mode)
        # self.assertEqual("de", manuscript_textstory_setup.general.language)
        # self.assertEqual("", manuscript_textstory_setup.general.subtitle)
        # self.assertEqual("Unknown title", manuscript_textstory_setup.general.title)

        # Html defaults
        # self.assertEqual("Unknown title | Unknown author", manuscript_textstory_setup.html.header_title)
        # self.assertEqual("de_DE", manuscript_textstory_setup.html.locale)
        # self.assertEqual("", manuscript_textstory_setup.html.meta_description)
        # self.assertEqual("", manuscript_textstory_setup.html.og_image_tag)
        # self.assertEqual("", manuscript_textstory_setup.html.site_name)
        # self.assertEqual(manuscript_textstory_setup.general.subtitle, manuscript_textstory_setup.html.subtitle)
        # self.assertEqual(manuscript_textstory_setup.general.title, manuscript_textstory_setup.html.title)
        # self.assertEqual("", manuscript_textstory_setup.html.url)

        # LaTeX defaults
        # self.assertEqual("", manuscript_textstory_setup.latex.appendix)
        # self.assertEqual(False, manuscript_textstory_setup.latex.book_print)
        # self.assertEqual(False, manuscript_textstory_setup.latex.chapter_pagebreak)
        self.assertTrue('tgcursor' in manuscript_textstory_setup.latex.font)
        # self.assertEqual("false", manuscript_textstory_setup.latex.has_color_links)
        # self.assertEqual("\\storytitle", manuscript_textstory_setup.latex.header_left)
        # self.assertEqual("\\storychapter", manuscript_textstory_setup.latex.header_right)
        # self.assertEqual(False, manuscript_textstory_setup.latex.hide_chapter_header)
        # self.assertEqual("", manuscript_textstory_setup.latex.isbn)
        # self.assertEqual("scrreprt", manuscript_textstory_setup.latex.latex_document_type)
        # self.assertEqual("fontsize=11pt,", manuscript_textstory_setup.latex.latex_font_size)
        # self.assertEqual("\\usepackage[a5paper, heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}",
        #                  manuscript_textstory_setup.latex.latex_geometry)
        # self.assertEqual(manuscript_textstory_setup.latex.latex_title, manuscript_textstory_setup.latex.latex_half_title)
        # self.assertEqual(manuscript_textstory_setup.general.subtitle, manuscript_textstory_setup.latex.latex_subtitle)
        # self.assertEqual(manuscript_textstory_setup.general.title, manuscript_textstory_setup.latex.latex_title)
        # self.assertEqual("black", manuscript_textstory_setup.latex.link_color)
        # self.assertEqual("", manuscript_textstory_setup.latex.pdf_keywords)
        # self.assertEqual("", manuscript_textstory_setup.latex.pdf_subject)
        # self.assertEqual("", manuscript_textstory_setup.latex.preliminaries)
        # self.assertEqual(False, manuscript_textstory_setup.latex.print_author_on_title)
        # self.assertEqual("\\begin{center}\n{\\huge \\storytitle}\n\\end{center}\n",
        #                  manuscript_textstory_setup.latex.print_title, )
        # self.assertEqual(False, manuscript_textstory_setup.latex.table_of_contents)
        # table of contents contents_title
        # self.assertEqual(False, manuscript_textstory_setup.latex.table_of_contents_pagebreak)
        self.assertTrue(manuscript_textstory_setup.latex.todonotes_config.__contains__("disable"))
        # self.assertEqual("blue", manuscript_textstory_setup.latex.url_color)