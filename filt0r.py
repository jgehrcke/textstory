# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import os
import sys
from distutils import dir_util, file_util
import string

from documentreader import DocumentReader
from filters import get_filters, get_latex_chapters
from logger import log
from paths import dir_path, SETUP_FILE, LATEX_TEMPLATE, HTML_TEMPLATE, HTML_LICENSE, OUTFILE_LATEX_BODY, \
    OUTFILE_LATEX_DOC, OUTFILE_HTML, PRELIMINARIES_PATH, APPENDIX_PATH
from textstory_setup import Setup


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

    # Setup
    log.info("***************** Running setup *****************")
    setup = Setup(setup_file_path, input_file_path, output_folder_path)
    log.info("Done with setup.")

    run_with_setup(setup)


def run_with_setup(setup):
    input_markup = DocumentReader(setup.input_file_path).get_string()

    filters = get_filters(setup)
    
    outfile_latex_doc = os.path.normpath(os.path.join(dir_path, OUTFILE_LATEX_DOC))
    outfile_latex_body = os.path.normpath(os.path.join(dir_path, OUTFILE_LATEX_BODY))
    outfile_html = os.path.normpath(os.path.join(dir_path, OUTFILE_HTML))
    
    if setup.output_folder_path is not None:
        # prepare output folder
        setup.output_folder_path = os.path.normpath(setup.output_folder_path)
        # tests/create output folder path
        if not os.path.isdir(setup.output_folder_path):
            # create if not existent
            if not os.path.exists(setup.output_folder_path):
                try:
                    os.makedirs(setup.output_folder_path)
                    log.info("Created output directory: " + str(setup.output_folder_path))
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
        latex_output_path = os.path.join(setup.output_folder_path, 'latex')
        html_output_path = os.path.join(setup.output_folder_path, 'html')
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
        outfile_latex_doc = os.path.normpath(os.path.join(setup.output_folder_path, OUTFILE_LATEX_DOC))
        outfile_latex_body = os.path.normpath(os.path.join(setup.output_folder_path, OUTFILE_LATEX_BODY))
        outfile_html = os.path.normpath(os.path.join(setup.output_folder_path, OUTFILE_HTML))
    
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
            longest_chapter_title = ""
            for chapter in get_latex_chapters():
                if len(chapter['name']) > len(longest_chapter_title):
                    longest_chapter_title = chapter['name']
            latex_first_page_setup += "%%%% Calculate width for table of contents\n" \
                                      "\\newlength{\\toctextwidth}\n" \
                                      "\\setlength{\\toctextwidth}{\\minof{0.8\\linewidth}{\\widthof{%s}}}\n\n" \
                                      % longest_chapter_title
            latex_first_page_setup += "\\vspace{0.5cm}\\noindent" \
                                      "\\begin{supertabular}{p{\\toctextwidth}p{0.1\\toctextwidth}}\n"
            for chapter in get_latex_chapters():
                latex_first_page_setup += chapter['name'] + " & \\hfill\\pageref{" + chapter['id'] + "} \\\\\n"
            latex_first_page_setup += "\\end{supertabular}\n"
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
                                                   font=setup.latex.font,
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
                                                   appendix=setup.latex.appendix,
                                                   todonotes_config=setup.latex.todonotes_config)
 
    def create_output(self):
        # writing latex document
        with open(self.output_doc_file_path, "wb") as f:
            f.write(self.latex_doc.encode("utf-8"))
        log.info("Wrote UTF-8-encoded LaTeX document: %s.", self.output_doc_file_path)
        # writing latex document body
        with open(self.output_body_file_path, "wb") as f:
            f.write(self.output_latex.encode("utf-8"))
        log.info("Wrote UTF-8-encoded LaTeX document body: %s.", self.output_body_file_path)


if __name__ == "__main__":
    main()
