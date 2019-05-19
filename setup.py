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

    def get_bool(self, category, item, default):
        # test if entry is in setup toml
        if category not in self.setup_toml or item not in self.setup_toml[category]:
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


class GeneralSetupData(SetupData):
    def __init__(self, setup_toml):
        super(GeneralSetupData, self).__init__(setup_toml)
        self.title = setup_toml['general']['title']
        if 'subtitle' in setup_toml['general']:
            self.subtitle = setup_toml['general']['subtitle']
        else:
            self.subtitle = ""
        self.author = setup_toml['general']['author']
        self.language = setup_toml['general']['language']


class HtmlSetupData(SetupData):
    def __init__(self, setup_toml, general):
        super(HtmlSetupData, self).__init__(setup_toml)
        self.locale = setup_toml['html']['locale']
        if 'title' in setup_toml['html']:
            self.title = setup_toml['html']['title']
        else:
            self.title = general.title
        if 'subtitle' in setup_toml['html']:
            self.subtitle = setup_toml['html']['subtitle']
        else:
            self.subtitle = general.subtitle
        if 'headertitle' in setup_toml['html']:
            self.header_title = setup_toml['html']['headertitle']
        else:
            self.header_title = self.title + " | " + general.author
        self.meta_description = setup_toml['html']['metadescription']
        self.url = setup_toml['html']['url']
        self.site_name = setup_toml['html']['sitename']
        if 'previewimage' in setup_toml['html']:
            self.og_image_tag = '<meta property="og:image" content="%s" />' % setup_toml['html']['previewimage']
        else:
            self.og_image_tag = ""


class LatexSetupData(SetupData):
    def __init__(self, setup_toml, general, preliminaries_path, appendix_path):
        super(LatexSetupData, self).__init__(setup_toml)
        # table of contents setup
        if self.get_bool('latex', 'tableOfContents', False):
            self.table_of_contents = True
            if 'contentsTitle' in setup_toml['latex'] and setup_toml['latex']['contentsTitle'] != "":
                self.latex_contents_title = setup_toml['latex']['contentsTitle']
            if self.get_bool('latex', 'tableOfContentsPagebreak', False):
                self.table_of_contents_pagebreak = True
            else:
                self.table_of_contents_pagebreak = False
        else:
            self.table_of_contents = False

        # book print setup
        self.preliminaries = ""
        self.appendix = ""
        if self.get_bool('latex', 'bookPrint', False):
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
        if 'headerLeft' in setup_toml['latex']:
            self.header_left = setup_toml['latex']['headerLeft']
        else:
            self.header_left = "\\storytitle"
        if 'headerRight' in setup_toml['latex']:
            self.header_right = setup_toml['latex']['headerRight']
        else:
            self.header_right = "\\storychapter"

        # chapter page break
        self.chapter_pagebreak = self.get_bool('latex', 'chapterPagebreak', False)

        # header again
        self.hide_chapter_header = self.get_bool('latex', 'hideChapterHeader', None)
        if self.hide_chapter_header is None:
            self.hide_chapter_header = self.chapter_pagebreak

        # isbn
        if 'isbn' in setup_toml['latex']:
            self.isbn = setup_toml['latex']['isbn']
        else:
            self.isbn = ""

        # geometry
        self.latex_geometry = "\\usepackage["
        if 'pageFormat' in setup_toml['latex']:
            self.latex_geometry += "%spaper" % setup_toml['latex']['pageFormat']
        elif 'pageWidth' in setup_toml['latex'] and 'pageHeight' in setup_toml['latex']:
            self.latex_geometry += "paperwidth=%s, paperheight=%s" % (setup_toml['latex']['pageWidth'],
                                                                      setup_toml['latex']['pageHeight'],)
        else:  # default
            self.latex_geometry += "a5paper"
        if 'bindingOffset' in setup_toml['latex']:
            self.latex_geometry += ", bindingoffset=%s" % setup_toml['latex']['bindingOffset']
        self.latex_geometry += ", heightrounded, hmarginratio=1:1, vmarginratio=1:1]{geometry}"

        # font size
        if 'fontSize' in setup_toml['latex']:
            self.latex_font_size = "fontsize=%spt," % setup_toml['latex']['fontSize']
        else:
            self.latex_font_size = "fontsize=11pt,"

        # title setup
        if 'title' in setup_toml['latex']:
            self.latex_title = setup_toml['latex']['title']
        else:
            self.latex_title = general.title
        if 'subtitle' in setup_toml['latex']:
            self.latex_subtitle = setup_toml['latex']['subtitle']
        else:
            self.latex_subtitle = general.subtitle
        self.print_title = "\\begin{center}\n"
        self.print_author_on_title = self.get_bool('latex', 'printAuthorOnTitle', False)
        if self.print_author_on_title:
            self.print_title += "{\\large \\storyauthor}\n\n\\vspace{0.6cm}\n"
        self.print_title += "{\\huge \\storytitle}\n"
        if self.latex_subtitle != "":
            self.print_title += "\n\\vspace{0.3cm}\n{\\large \\storysubtitle}\n"
        self.print_title += "\\end{center}\n"
        self.latex_half_title = self.latex_title
        if 'halfTitle' in setup_toml['latex']:
            self.latex_half_title = setup_toml['latex']['halfTitle']

        # pdf keywords
        self.pdf_subject = setup_toml['latex']['pdfsubject']
        self.pdf_keywords = setup_toml['latex']['pdfkeywords']
        if 'hascolorlinks' in setup_toml['latex']:
            self.has_color_links = setup_toml['latex']['hascolorlinks']
        else:
            self.has_color_links = "false"
        if 'urlcolor' in setup_toml['latex']:
            self.url_color = setup_toml['latex']['urlcolor']
        else:
            self.url_color = "blue"
        if 'linkcolor' in setup_toml['latex']:
            self.link_color = setup_toml['latex']['linkcolor']
        else:
            self.link_color = "black"
