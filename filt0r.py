# -*- coding: utf-8 -*-
# Copyright (c) 2015-2018 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import re
import os
import sys
from distutils import dir_util, file_util
import string
import logging
import toml

PY2 = sys.version_info.major == 2

logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)

dir_path = os.path.dirname(os.path.realpath(__file__))

SETUP_FILE = os.path.join(dir_path, "setup.toml")

LATEX_TEMPLATE = os.path.normpath(os.path.join(dir_path, "latex/latex-document.tpl.tex"))

HTML_TEMPLATE = os.path.normpath(os.path.join(dir_path, "html/index.tpl.html"))
HTML_LICENSE = os.path.normpath(os.path.join(dir_path, "html/license.tpl.html"))

OUTFILE_LATEX_BODY = os.path.normpath("latex/latex-body.tex")
OUTFILE_LATEX_DOC = os.path.normpath("latex/latex-document.tex")
PRELIMINARIES_PATH = "bookPreliminaries/"
APPENDIX_PATH = "bookAppendix/"

OUTFILE_HTML = os.path.normpath("html/index.html")

latex_chapters = []

        
def main():   
    # checking command line args
    
    # required arg 1: input document
    if len(sys.argv) < 2:
        sys.exit("First argument must be path to document source.")
    infile_path = sys.argv[1]
    
    # optional arg 2: setup file path (otherwise using default)
    setup_file_path = SETUP_FILE
    if len(sys.argv) > 2:
        setup_file_path = sys.argv[2]
    try:
        run(setup_file_path, infile_path)
    except SystemExit as e:
        log.info(str(e.args[0]))
        log.info("Abort.")
        return


def run(setup_file_path, input_file_path, output_folder_path=None):
    log.info("++++++++++ textstory-to-beautiful-latex-html ++++++++++")

    # initialize collecting of latex chapters
    global latex_chapters
    latex_chapters = []
    
    input_markup = DocumentReader(input_file_path).get_string()
    
    # Setup
    log.info("***************** Running setup *****************")
    setup = Setup(setup_file_path, output_folder_path)
    log.info("Done with setup.")
    
    filters = [
        FilterConvertLineEndings(),  # needs to be done first
        FilterMaskEscapedCharacters(),  # needs to be done second
        FilterHyphens(),
        FilterSectionsParagraphs(),  # introduces HTML-minuses, must run after FilterHyphens
        FilterHeadlines(setup.latex.chapter_pagebreak, setup.latex.hide_chapter_header),
        FilterImages(),  # has to be done before FilterFootnotes
        FilterFootnotes(),
        FilterQuotes(),
        FilterBold(),  # has to be done before FilterItalics
        FilterItalics(),
        FilterDots(),
        FilterRestoreEscapedCharacters(),  # needs to be done last
    ]
    
    outfile_latex_doc = os.path.normpath(os.path.join(dir_path, OUTFILE_LATEX_DOC))
    outfile_latex_body = os.path.normpath(os.path.join(dir_path, OUTFILE_LATEX_BODY))
    outfile_html = os.path.normpath(os.path.join(dir_path, OUTFILE_HTML))
    
    if output_folder_path is not None:
        # prepare output folder
        output_folder_path = os.path.normpath(output_folder_path)
        # test/create output folder path
        if not os.path.isdir(output_folder_path):
            # create if not existent
            if not os.path.exists(output_folder_path):
                try:
                    os.makedirs(output_folder_path)
                    log.info("Created output directory: " + str(output_folder_path))
                except Exception as e:
                    log.info("Failed creating output directory: " + type(e).__name__ + str(e.args))
                    log.info("Abort.")
                    return
            else:
                # abort: existent but not a dir
                log.info("Output folder path is invalid.")
                log.info("Abort.")
                return
        # create directory structure
        latex_output_path = os.path.join(output_folder_path, 'latex')
        html_output_path = os.path.join(output_folder_path, 'html')
        try:
            if not os.path.exists(latex_output_path):
                os.makedirs(latex_output_path)
            # preliminariesPath = os.path.join(latex_output_path, 'bookPreliminaries')
            # if not os.path.exists(preliminariesPath):
            #     os.makedirs(preliminariesPath)
            # appendixPath = os.path.join(latex_output_path, 'bookAppendix')
            # if not os.path.exists(appendixPath):
            #     os.makedirs(appendixPath)
            if not os.path.exists(html_output_path):
                os.makedirs(html_output_path)
        except Exception as e:
            log.info("Failed creating output subdirectories: " + type(e).__name__ + str(e.args))
            log.info("Abort.")
            return           

        # copy required files from latex template folders
        appendix_source_path = os.path.join(dir_path, 'latex', APPENDIX_PATH)
        if not os.path.exists(appendix_source_path):
            os.makedirs(appendix_source_path)
        dir_util.copy_tree(appendix_source_path,
                           os.path.join(latex_output_path, APPENDIX_PATH), update=1)
        # TODO appendix files from config?
        preliminaries_source_path = os.path.join(dir_path, 'latex', PRELIMINARIES_PATH)
        if not os.path.exists(preliminaries_source_path):
            os.makedirs(preliminaries_source_path)
        dir_util.copy_tree(preliminaries_source_path,
                           os.path.join(latex_output_path, PRELIMINARIES_PATH), update=1)
        # TODO preliminary files from config?
        dir_util.copy_tree(os.path.join(dir_path, 'latex', 'img'), 
                           os.path.join(latex_output_path, 'img'), update=1)
        latex_files = [
            'build.bash',
            'build.bat',
            'license.tex'  # TODO get license from config, allow not using license
        ]
        for file_name in latex_files:
            copy_file(file_name, 'latex', latex_output_path)
        
        # copy required files from html template folders
        dir_util.copy_tree(os.path.join(dir_path, 'html', 'css'), os.path.join(html_output_path, 'css'), update=1)
        dir_util.copy_tree(os.path.join(dir_path, 'html', 'img'), os.path.join(html_output_path, 'img'), update=1)
        html_files = [  # TODO get license from config, allow not using license
            'apple-touch-icon.png',
            'browserconfig.xml',
            'favicon.ico',
            'humans.txt',
            'tile.png',
            'tile-wide.png'
        ]
        for file_name in html_files:
            copy_file(file_name, 'html', html_output_path)
                
        # set outfile paths
        outfile_latex_doc = os.path.normpath(os.path.join(output_folder_path, OUTFILE_LATEX_DOC))
        outfile_latex_body = os.path.normpath(os.path.join(output_folder_path, OUTFILE_LATEX_BODY))
        outfile_html = os.path.normpath(os.path.join(output_folder_path, OUTFILE_HTML))
    
    # Create LaTeX
    log.info("***************** Creating LaTeX *****************")
    latex_generator = LatexGenerator(setup, input_markup, filters,
                                     LATEX_TEMPLATE, outfile_latex_doc, outfile_latex_body)
    latex_generator.create_output()
    log.info("Done creating LaTeX.")
    
    # Create HTML
    log.info("***************** Creating HTML *****************")
    html_generator = HtmlGenerator(setup, input_markup, filters, HTML_TEMPLATE, HTML_LICENSE, outfile_html)
    html_generator.create_output()
    log.info("Done creating HTML.")  


def copy_file(file_name, src_folder, dst_folder):
    file_util.copy_file(os.path.join(dir_path, src_folder, file_name), os.path.join(dst_folder, file_name), update=1)

        
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
                    self.preliminaries += "\\input{" + PRELIMINARIES_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
            # adding appendix pages
            for root, dirs, files in os.walk(appendix_path):
                if files:
                    log.info("Appendix pages:")
                for name in sorted(files):
                    log.info("  " + name)
                    self.appendix += "\\input{" + APPENDIX_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
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


class Generator(object):
    def __init__(self, setup, input_markup, filters, template_file_path):
        self.template_file_path = template_file_path
        self.apply_filters(filters, input_markup)
        self.substitute(setup)

    def apply_filters(self, filters, input_markup):
        pass
        
    def substitute(self, setup):
        pass

    def create_output(self):
        pass


class HtmlGenerator(Generator):
    def __init__(self, setup, input_markup, filters, template_file_path, license_file_path, output_file_path):
        self.output_file_path = output_file_path
        self.license_file_path = license_file_path
        self.output_html = ""
        self.html_doc = ""
        Generator.__init__(self, setup, input_markup, filters, template_file_path)

    def apply_filters(self, filters, input_markup):
        # Push original contents through HTML filters (same order, order matters).
        self.output_html = input_markup
        for f in filters:
            log.info("Process with %s", f)
            self.output_html = f.to_html(self.output_html)
            log.info("Done.")   

    def substitute(self, setup):
        log.info("Performing HTML template substitution")
        
        if setup.html.subtitle == "":
            subtitle_tag = ""
        else:
            subtitle_tag = '<p class="subtitle">%s</p>\n' % setup.html.subtitle
        
        if os.path.isfile(self.license_file_path):
            html_license = DocumentReader(self.license_file_path).get_string()
            if not html_license:
                html_license = ""
        else:
            html_license = ""
        
        html_template_string = DocumentReader(self.template_file_path).get_string()
        if not html_template_string:
            log.error("Could not read HTML template.")
            return
        html_template = string.Template(html_template_string)
        self.html_doc = html_template.substitute(html_content=self.output_html, license=html_license, 
                                                 lang=setup.general.language, locale=setup.html.locale, 
                                                 header_title=setup.html.header_title, title=setup.html.title,
                                                 subtitle_tag=subtitle_tag, author=setup.general.author, 
                                                 meta_description=setup.html.meta_description, url=setup.html.url,
                                                 site_name=setup.html.site_name, og_image_tag=setup.html.og_image_tag)
        
    def create_output(self):
        with open(self.output_file_path, "wb") as f:
            f.write(self.html_doc.encode("utf-8"))
        log.info("Wrote UTF-8-encoded HTML document: %s.", self.output_file_path)


class LatexGenerator(Generator):
    def __init__(self, setup, input_markup, filters, template_file_path, output_doc_file_path, output_body_file_path):
        self.output_doc_file_path = output_doc_file_path
        self.output_body_file_path = output_body_file_path
        self.output_latex = ""
        self.latex_doc = ""
        Generator.__init__(self, setup, input_markup, filters, template_file_path)
        
    def apply_filters(self, filters, input_markup):
        # Push original contents through all LaTeX filters (order matters).
        self.output_latex = input_markup
        for f in filters:
            log.info("Process with %s", f)
            self.output_latex = f.to_latex(self.output_latex)
            log.info("Done.")

    def substitute(self, setup):
        latex_first_page_setup = ""
        if setup.latex.table_of_contents:
            latex_first_page_setup = "\\thispagestyle{empty}\n\n{\\large\n"
            if setup.latex.latex_contents_title:
                latex_first_page_setup += "\n{\\vspace{0.5cm}\\noindent\\LARGE %s}\n\n" \
                                          % setup.latex.latex_contents_title
            latex_first_page_setup += "\\vspace{0.5cm}\\noindent\\begin{tabular}{lr}\n"
            for chapter in latex_chapters:
                latex_first_page_setup += chapter['name'] + " & \\pageref{" + chapter['id'] + "} \\\\\n"
            latex_first_page_setup += "\\end{tabular}\n"
            latex_first_page_setup += "}\n\n"
            if setup.latex.chapter_pagebreak or setup.latex.table_of_contents_pagebreak:
                latex_first_page_setup += "\\clearpage\n\n"
            else:
                latex_first_page_setup += "\\vspace{0.5cm}\n\n"
        if setup.latex.book_print:
            header = "\\ohead{\\thepage}\n"
            header += "\\cehead{" + setup.latex.header_left + "}\n"
            header += "\\cohead{" + setup.latex.header_right + "}\n"
        else:
            header = "\\setkomafont{pageheadfoot}{\\small\\textit}\n"
            header += "\\ihead{" + setup.latex.header_left + "}\n"
            header += "\\chead{\\thepage}\n"
            header += "\\ohead{" + setup.latex.header_right + "}\n"
            latex_first_page_setup = "\\thispagestyle{empty}\n\n\\printtitle\n" + latex_first_page_setup
               
        log.info("Performing LaTeX template substitution")
        latex_template_string = DocumentReader(self.template_file_path).get_string()
        if not latex_template_string:
            log.error("Could not read LaTeX template.")
            return
        latex_template = string.Template(latex_template_string)
        self.latex_doc = latex_template.substitute(isbn=setup.latex.isbn, 
                                                   document_type=setup.latex.latex_document_type,
                                                   geometry=setup.latex.latex_geometry,
                                                   font_size=setup.latex.latex_font_size,
                                                   title=setup.latex.latex_title,
                                                   subtitle=setup.latex.latex_subtitle,
                                                   half_title=setup.latex.latex_half_title,
                                                   print_title=setup.latex.print_title,
                                                   author=setup.general.author, 
                                                   first_page_setup=latex_first_page_setup, 
                                                   header=header,
                                                   pdf_title=setup.latex.latex_title,
                                                   pdf_author=setup.general.author, 
                                                   pdf_subject=setup.latex.pdf_subject,
                                                   pdf_keywords=setup.latex.pdf_keywords,
                                                   has_color_links=setup.latex.has_color_links,
                                                   url_color=setup.latex.url_color,
                                                   link_color=setup.latex.link_color,
                                                   preliminaries=setup.latex.preliminaries, 
                                                   appendix=setup.latex.appendix)
 
    def create_output(self):
        # writing latex document
        with open(self.output_doc_file_path, "wb") as f:
            f.write(self.latex_doc.encode("utf-8"))
        log.info("Wrote UTF-8-encoded LaTeX document: %s.", self.output_doc_file_path)
        # writing latex document body
        with open(self.output_body_file_path, "wb") as f:
            f.write(self.output_latex.encode("utf-8"))
        log.info("Wrote UTF-8-encoded LaTeX document body: %s.", self.output_body_file_path)


class DocumentReader(object):
    def __init__(self, document_path):
        self.document_path = document_path
        if not os.path.isfile(self.document_path):
            raise SystemExit("File not found: %s" % self.document_path)
        log.info("Reading file: %s.", self.document_path)
        with open(self.document_path, "rb") as f:
            self.file_string = f.read()

    def get_string(self):
        try:
            return self.file_string.decode("utf-8").strip()
        except UnicodeDecodeError:
            raise SystemExit("Cannot read '" + self.document_path + "': UnicodeDecodeError.")


class Filter(object):
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__


# Lines beginning with ## will be formatted as headlines
class FilterHeadlines(Filter):
    def __init__(self, latex_chapter_pagebreak, latex_hide_chapter_header):
        self.latex_chapter_pagebreak = latex_chapter_pagebreak
        self.latex_hide_chapter_header = latex_hide_chapter_header
        super(FilterHeadlines, self).__init__()

    def to_html(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "<h2>%s</h2>" % (text, )
            return result

        pattern = '^<p.*>##\s*(.*?)</p>$'
        new, n = re.subn(pattern, replace_func, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            chapters_count = len(latex_chapters)
            label_text = str(chapters_count) + text
            latex_chapters.append({'id': label_text, 'name': text})
            result = "\n{\\label{%s}\\vspace{0.5cm}\\noindent\\LARGE %s}\n\\renewcommand{\\storychapter}{%s}" \
                     % (label_text, text, text, )
            if self.latex_chapter_pagebreak and chapters_count > 0:
                result = "\\clearpage\n\n" + result
            if self.latex_hide_chapter_header:
                result += "\n\\thispagestyle{empty}"
            return result

        pattern = '^##\s*(.*?)$'
        new, n = re.subn(pattern, replace_func, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new


class FilterDots(Filter):
    def to_html(self, s):
        return s.replace("...", "&hellip; ")

    def to_latex(self, s):
        return s.replace("...", r"\dots ")


class FilterQuotes(Filter):
    def to_html(self, s):
        def replace_func(match_obj):
            quote = match_obj.group(1)
            # Implement paragraphs with vertical space and w/o indentation.
            quote = quote.replace('<p class=$DQ$indent$DQ$>', "<p>")
            result = "»%s«" % (quote, )
            return result

        pattern = '"(.*?)"'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        # Restore HTML doublequotes.
        new = new.replace("$DQ$", '"')
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            """
            Paragraphs within quotations should not be indented.
            In this func, also filter the quote *contents* to implement
            this criterion.
            """
            # Extract quote content.
            quote = match_obj.group(1)
            # Implement paragraphs with vspace and w/o indentation.
            quote = quote.replace(
                "\n\n", "\n\n\\noindent\n")
            # Implement LaTeX command.
            result = "\\enquote{%s}" % quote
            return result

        # From re.subn docs. "If repl is a function, it is called for every
        # non-overlapping occurrence of pattern. The function takes a single
        # match object argument, and returns the replacement string."
        # Make the search non-greedy, and search across newlines.
        pattern = '"(.*?)"'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        return new


# Text surrounded by double underscores or double asterisks will be shown bold
class FilterBold(Filter):
    def to_html(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "<strong>%s</strong>" % (text, )
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = '\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n+m)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "{\\boldfont\\textbf{%s}}" % text
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = '\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n+m)
        return new


# Text surrounded by underscores or asterisks will be shown in italics
class FilterItalics(Filter):
    def to_html(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "<em>%s</em>" % (text, )
            return result

        pattern = '_(.*?)_'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = '\*(.*?)\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n+m)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            if "\n" in text:  # itshape works over multiple lines but gets easily disturbed
                result = "\\begin{itshape}%s\\end{itshape}" % text
            else:  # \textit can be combined with \textbf etc. but does not work over multiple lines
                result = "\\textit{%s}" % text
            return result

        pattern = '_(.*?)_'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = '\*(.*?)\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n+m)
        return new


class FilterImages(Filter):
    # ![Alt text](/path/to/img.jpg "optional title")
    pattern = '!\[(.*)\]\(([^")]*)(\s"(.*)")?\)'
    
    def to_html(self, s):
        def replace_func(match_obj):
            alt_text = match_obj.group(1)
            path = match_obj.group(2)
            title = match_obj.group(4)
            result = '<figure class=$DQ$textimage$DQ$>\n'
            result += '<img src=$DQ$%s$DQ$ alt=$DQ$%s$DQ$ ' % (path, alt_text, )
            # if title != None:
            #     result += 'title=$DQ$%s$DQ$ ' %(title, )
            result += ' />\n'
            if title is not None:
                result += '<figcaption>%s</figcaption>\n' % (title, )
            result += '</figure>'
            return result

        new, n = re.subn('^<p.*>' + self.pattern + '</p>$', replace_func, s, flags=re.MULTILINE)
        log.info("Made %s image replacements.", n)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            # alt_text = match_obj.group(1)
            path = match_obj.group(2)
            title = match_obj.group(4)
            result = '\\begin{figure}$squareBracketOpen$!ht$squareBracketClose$\n'
            result += '\\centering\n'
            max_height = '1.0\\textheight'
            caption = ''
            if title is not None:
                max_height = '0.9\\textheight'
                caption = '\\caption$asterisk${%s}\n' %(title, )
            result += '\\includegraphics$squareBracketOpen$max height=' + max_height \
                      + ',max width=1.0\\textwidth$squareBracketClose${%s}\n' % (path, )
            result += caption
            result += '\\end{figure}'
            return result
            
        new, n = re.subn(self.pattern, replace_func, s)
        log.info("Made %s image replacements.", n)
        return new


class FilterConvertLineEndings(Filter):
    @staticmethod
    def _convert(s):
        new = s.replace("\r\n", "\n")  # Windows
        new = new.replace("\r", "\n")  # Mac
        return new

    def to_html(self, s):
        return self._convert(s)

    def to_latex(self, s):
        return self._convert(s)


class FilterSectionsParagraphs(Filter):
    @staticmethod
    def _convert(s, section_separator, paragraph_separator):
        _tmp_section_spacer = "$NEWSECTION$"
        # First remember and shim places with two LF (section separator).
        new = s.replace("\n\n", _tmp_section_spacer)
        # Replace single LF with paragraph separator.
        new = new.replace("\n", paragraph_separator)
        # Replace original two-LFs with markup for new section.
        new = new.replace(_tmp_section_spacer, section_separator)
        return new

    def to_html(self, s):
        section_sep = "</p>\n</section>\n\n\n<section>\n<p>"
        # Temporarily shim HTML double quotes.
        paragraph_sep = '</p>\n\n<p class=$DQ$indent$DQ$>'
        new = self._convert(s, section_sep, paragraph_sep)
        new = "<section>\n<p>%s</p>\n</section>" % (new, )
        return new

    def to_latex(self, s):
        section_sep = "\n\n\\vspace{0.5cm}\\noindent\n"
        paragraph_sep = "\n\n"
        return self._convert(s, section_sep, paragraph_sep)


# structure for defining how to escape and restore special characters
class EscapeRoute(object):
    def __init__(self, original, temporary, html, latex):
        self.original = original
        self.temporary = temporary
        self.html = html
        self.latex = latex


"""
list of all allowed EscapeRoutes (\ needs to be escaped in python too, so theres a lot of \)

HTML:
& becomes &amp; (does not need to be escaped in original document)
< becomes &lt; (does not need to be escaped in original document)
> becomes &gt; (does not need to be escaped in original document)

LATEX:
& becomes \& (does not need to be escaped in original document)
% becomes \% (does not need to be escaped in original document)
$ becomes \$
# becomes \#
_ becomes \_
{ becomes \{
} becomes \}
~ becomes \textasciitilde (does not need to be escaped in original document)
^ becomes \textasciicircum (does not need to be escaped in original document)
\ becomes \textbackslash

TEXTSTORY MARKUP:
\   backslash
*   asterisk
_   underscore
{}  curly braces
[]  square brackets
#   hash mark
"   doublequote
!   exclamation mark (only needs to be escaped when followed by '[')
--  double minus

"""
escape_routes = [
    EscapeRoute('\\\\', '$escapeChar$', '\\', '\\textbackslash{}'),
    EscapeRoute('&', '$amp$', '&amp;', '\\&'),
    EscapeRoute('<', '$lt$', '&lt;', '<'),
    EscapeRoute('>', '$gt$', '&gt;', '>'),
    EscapeRoute('%', '$percent$', '%', '\\% '),
    EscapeRoute('\\$', '$dollar$', '$', '\\$ '),
    EscapeRoute('\\#', '$hash$', '#', '\\# '),
    EscapeRoute('\\_', '$underscore$', '_', '\\_ '),
    EscapeRoute('\\{', '$curlyBracketOpen$', '{', '\\{ '),
    EscapeRoute('\\}', '$curlyBracketClose$', '}', '\\} '),
    EscapeRoute('\\[', '$squareBracketOpen$', '[', '['),
    EscapeRoute('\\]', '$squareBracketClose$', ']', ']'),
    EscapeRoute('~', '$tilde$', '~', '\\textasciitilde{}'),
    EscapeRoute('^', '$circumflex$', '^', '\\textasciicircum{}'),
    EscapeRoute('\\*', '$asterisk$', '*', '*'),
    EscapeRoute('\\--', '$hyphen$', '--', '\\verb|--|'),
    EscapeRoute('\\"', '$doubleQuote$', '&quot;', '"{}'),
    EscapeRoute('\\!', '$exclamation$', '!', '!'),
    # EscapeRoute('\\', '', '', ''),
]


class FilterMaskEscapedCharacters(Filter):
    def _convert(self, s):
        new = s
        for i in escape_routes:
            new = new.replace(i.original, i.temporary)
        return new
           
    def to_html(self, s):
        return self._convert(s)
    
    def to_latex(self, s):
        return self._convert(s)


class FilterRestoreEscapedCharacters(Filter):
    def to_html(self, s):
        new = s
        for i in escape_routes:
            new = new.replace(i.temporary, i.html)
        return new

    def to_latex(self, s):
        new = s
        for i in escape_routes:
            new = new.replace(i.temporary, i.latex)
        return new


class FilterHyphens(Filter):
    def to_html(self, s):
        new = s.replace("---", "&mdash;")
        new = new.replace("--", "&ndash;")
        return new

    def to_latex(self, s):
        # actually nothing to do:
        return s


class FilterFootnotes(Filter):
    def _convert(self, s, replacement):
        pattern = "\[(.*?)\]"
        new, n = re.subn(pattern, replacement, s, flags=re.DOTALL)
        log.info("Made %s footnote replacements.", n)
        return new

    @staticmethod
    def _repair_footnote_ids(s):
        html_id = 'sn-tufte-handout'
        index = 1
        while True:
            s, n = re.subn(html_id + '(?!\d)', (html_id + str(index)), s, 2)
            index += 1
            if n < 2:
                break
        return s

    def to_html(self, s):
        replacement = (
            '<label for="sn-tufte-handout" class="margin-toggle sidenote-number">'
            '</label><input type="checkbox" id="sn-tufte-handout" class="margin-toggle"/>'
            '<span class="sidenote">\\1</span>')
        # Temporarily shim HTML double quotes.
        replacement = replacement.replace('"', "$DQ$")
        return self._repair_footnote_ids(self._convert(s, replacement))

    def to_latex(self, s):
        return self._convert(s, r"\\footnote{\1}")


if __name__ == "__main__":
    main()
