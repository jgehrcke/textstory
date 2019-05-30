# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals
import os
import sys

import toml

from logger import log
from documentreader import DocumentReader
from paths import dir_path, PRELIMINARIES_PATH, APPENDIX_PATH

PY2 = sys.version_info.major == 2


class Setup(object):
    def __init__(self, setup_file_path, output_folder_path=None):
        setup_file_string = DocumentReader(setup_file_path).get_string()
        self.setup_toml = toml.loads(setup_file_string)
        self.general = GeneralSetupData(self.setup_toml)
        self.html = HtmlSetupData(self.setup_toml, self.general)

        if output_folder_path is None:
            preliminaries_path = os.path.normpath(os.path.join(dir_path, 'latex', PRELIMINARIES_PATH))
            appendix_path = os.path.normpath(os.path.join(dir_path, 'latex', APPENDIX_PATH))
        else:
            preliminaries_path = os.path.normpath(os.path.join(output_folder_path, 'latex', PRELIMINARIES_PATH))
            appendix_path = os.path.normpath(os.path.join(output_folder_path, 'latex', APPENDIX_PATH))

        self.latex = LatexSetupData(self.setup_toml, self.general, preliminaries_path, appendix_path)


class SetupData(object):
    def __init__(self, setup_toml):
        self.setup_toml = setup_toml

    def is_entry_in_setup_toml(self, category, item):
        return category in self.setup_toml and item in self.setup_toml[category]

    def get_bool(self, category, item, default):
        if not self.is_entry_in_setup_toml(category, item):
            log.info("[" + category + "][" + item + "] not in setup TOML.")
            return default

        value = self.setup_toml[category][item]
        # if string, convert:
        if isinstance(value, basestring if PY2 else str):
            log.info("[" + category + "][" + item + "] string conversion, result: "
                     + str(value.lower() == "true") + ".")
            return value.lower() == "true"
        # actually already boolean:
        if isinstance(value, bool):
            return value
        # type mismatch
        log.warning("[" + category + "][" + item + "] wrong type, expected bool.")
        return default

    def get_string(self, category, item, default=""):
        if not self.is_entry_in_setup_toml(category, item):
            log.info("[" + category + "][" + item + "] not in setup TOML.")
            return default

        value = self.setup_toml[category][item]
        # return value if type matches
        if isinstance(value, basestring if PY2 else str):
            return value

        # type mismatch
        log.warning("[" + category + "][" + item + "] wrong type, expected string.")
        return default


class GeneralSetupData(SetupData):
    def __init__(self, setup_toml):
        super(GeneralSetupData, self).__init__(setup_toml)
        category = 'general'
        self.title = self.get_string(category, 'title', default="Unknown title")
        self.subtitle = self.get_string(category, 'subtitle')
        self.author = self.get_string(category, 'author', default="Unknown author")
        self.language = self.get_string(category, 'language', default="de")
        self.draft = self.get_bool(category, 'draft', default=False)


class HtmlSetupData(SetupData):
    def __init__(self, setup_toml, general):
        super(HtmlSetupData, self).__init__(setup_toml)
        category = 'html'
        self.locale = self.get_string(category, 'locale', 'de_DE')
        self.title = self.get_string(category, 'title', general.title)
        self.subtitle = self.get_string(category, 'subtitle', general.subtitle)
        header_default = ""
        if self.title and general.author:
            header_default = self.title + " | " + general.author
        self.header_title = self.get_string(category, 'headertitle', default=header_default)
        self.meta_description = self.get_string(category, 'metadescription', default="")
        self.url = self.get_string(category, 'url', default="")
        self.site_name = self.get_string(category, 'sitename', default="")
        preview_image = self.get_string(category, 'previewimage', default="")
        if preview_image:
            self.og_image_tag = '<meta property="og:image" content="%s" />' % setup_toml['html']['previewimage']
        else:
            self.og_image_tag = ""


class LatexSetupData(SetupData):
    def __init__(self, setup_toml, general, preliminaries_path, appendix_path):
        super(LatexSetupData, self).__init__(setup_toml)
        category = 'latex'

        # table of contents setup
        if self.get_bool(category, 'tableOfContents', False):
            self.table_of_contents = True
            contents_title = self.get_string(category, 'contentsTitle', default="")
            if contents_title != "":
                self.latex_contents_title = contents_title
        else:
            self.table_of_contents = False
        self.table_of_contents_pagebreak = self.get_bool(category, 'tableOfContentsPagebreak', False)

        # book print setup
        self.preliminaries = ""
        self.appendix = ""
        if self.get_bool(category, 'bookPrint', False):
            self.book_print = True
            self.latex_document_type = "scrbook"

            # adding preliminary pages
            for root, dirs, files in os.walk(preliminaries_path):
                if files:
                    log.info("Preliminary pages:")
                for name in sorted(files):
                    log.info("  " + name)
                    self.preliminaries += "\\input{" + PRELIMINARIES_PATH + name[:len(name) - 4] + "}\n\\clearpage\n"
            # adding appendix pages
            for root, dirs, files in os.walk(appendix_path):
                if files:
                    log.info("Appendix pages:")
                for name in sorted(files):
                    log.info("  " + name)
                    self.appendix += "\\input{" + APPENDIX_PATH + name[:len(name) - 4] + "}\n\\clearpage\n"
        else:
            self.book_print = False
            self.latex_document_type = "scrreprt"

        # header
        self.header_left = self.get_string(category, 'headerLeft', default="\\storytitle")
        self.header_right = self.get_string(category, 'headerRight', default="\\storychapter")

        # chapter page break
        self.chapter_pagebreak = self.get_bool(category, 'chapterPagebreak', False)

        # header again
        self.hide_chapter_header = self.get_bool(category, 'hideChapterHeader', default=self.chapter_pagebreak)

        # isbn
        self.isbn = self.get_string(category, 'isbn', default="")

        # geometry
        self.latex_geometry = "\\usepackage["
        page_format = self.get_string(category, 'pageFormat', default="")
        if general.draft:
            self.latex_geometry += "a4paper"
        elif page_format:
            self.latex_geometry += "%spaper" % page_format
        else:
            page_width = self.get_string(category, 'pageWidth', default="")
            page_height = self.get_string(category, 'pageHeight', default="")
            if page_width and page_height:
                self.latex_geometry += "paperwidth=%s, paperheight=%s" % (page_width, page_height,)
            else:  # default
                self.latex_geometry += "a5paper"
        binding_offset = self.get_string(category, 'bindingOffset', default="")
        if binding_offset:
            self.latex_geometry += ", bindingoffset=%s" % binding_offset
        self.latex_geometry += ", heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}"

        # font size
        font_size = self.get_string(category, 'fontSize', default="11")
        self.latex_font_size = "fontsize=%spt," % font_size

        # title setup
        self.latex_title = self.get_string(category, 'title', general.title)
        self.latex_subtitle = self.get_string(category, 'subtitle', general.subtitle)
        self.print_title = "\\begin{center}\n"
        self.print_author_on_title = self.get_bool(category, 'printAuthorOnTitle', default=False)
        if self.print_author_on_title:
            self.print_title += "{\\large \\storyauthor}\n\n\\vspace{0.6cm}\n"
        self.print_title += "{\\huge \\storytitle}\n"
        if self.latex_subtitle != "":
            self.print_title += "\n\\vspace{0.3cm}\n{\\large \\storysubtitle}\n"
        self.print_title += "\\end{center}\n"
        self.latex_half_title = self.get_string(category, 'halfTitle', self.latex_title)

        # pdf keywords
        self.pdf_subject = self.get_string(category, 'pdfsubject', default="")
        self.pdf_keywords = self.get_string(category, 'pdfkeywords', default="")
        self.has_color_links = self.get_string(category, 'hascolorlinks', default="false")
        self.url_color = self.get_string(category, 'urlcolor', default="blue")
        self.link_color = self.get_string(category, 'linkcolor', default="black")

        # comments
        self.todonotes_config = 'disable'
        if general.draft:
            self.todonotes_config = 'draft'
        self.todonotes_config += ', backgroundcolor=white, linecolor=black'
