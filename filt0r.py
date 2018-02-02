# -*- coding: utf-8 -*-
# Copyright 2015 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import re
import os
import sys
import string
import logging
import toml


logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)

SETUP_FILE = "setup.toml"
OUTFILE_LATEX_BODY = "latex/latex-body.tex"
OUTFILE_LATEX_DOC = "latex/latex-document.tex"
OUTFILE_HTML = "html/index.html"
LATEX_TEMPLATE = "latex/latex-document.tpl.tex"
HTML_TEMPLATE = "html/index.tpl.html"
PRELIMINARIES_PATH = "latex/bookPreliminaries"
PRELIMINARIES_LATEX_PATH = "bookPreliminaries/"
APPENDIX_PATH = "latex/bookAppendix"
APPENDIX_LATEX_PATH = "bookAppendix/"

latexChapterPagebreak = False
latexChapters = []
        
def main():
    if len(sys.argv) < 2:
        sys.exit("First argument must be path to document source.")
    infilePath = sys.argv[1]
    inputMarkup = DocumentReader(infilePath).getString()
    
    setupFilePath = SETUP_FILE
    if len(sys.argv) > 2:
        setupFilePath = sys.argv[2]
    setup = Setup(setupFilePath)

    #this needs to be set before LaTeX body is created
    if setup.latex.chapterPagebreak: #'chapterPagebreak' in setup['latex'] and setup['latex']['chapterPagebreak'].lower() == "true":
        global latexChapterPagebreak 
        latexChapterPagebreak = True

    filters = [
        FilterConvertLineEndings(),  # needs to be done first
        FilterMaskEscapedCharacters(), # needs to be done second
        FilterHyphens(),
        FilterSectionsParagraphs(), # introduces HTML-minuses, must run after FilterHyphens
        FilterHeadlines(),
        FilterImages(), # has to be done before FilterFootnotes
        FilterFootnotes(),
        FilterQuotes(),
        FilterBold(), # has to be done before FilterItalics
        FilterItalics(),
        FilterDots(),
        FilterRestoreEscapedCharacters(), # needs to be done last
    ]
        
    # Push original contents through all LaTeX filters (order matters).
    outputLatex = inputMarkup
    for f in filters:
        log.info("Process with %s", f)
        outputLatex = f.to_latex(outputLatex)
        log.info("Done.")
    with open(OUTFILE_LATEX_BODY, "wb") as f:
        f.write(outputLatex.encode("utf-8"))
    log.info("Wrote UTF-8-encoded LaTeX source file: %s.", OUTFILE_LATEX_BODY)   
       
    #setup latex substitutions
    latexFirstPageSetup = ""
    if setup.latex.tableOfContents:
        latexFirstPageSetup = "\\thispagestyle{empty}\n\n{\\large\n"
        if setup.latex.latexContentsTitle:
            latexFirstPageSetup += "\n{\\vspace{0.5cm}\\noindent\\LARGE %s}\n\n" % setup.latex.latexContentsTitle
        latexFirstPageSetup += "\\vspace{0.5cm}\\noindent\\begin{tabular}{lr}\n"
        for chapter in latexChapters:
            latexFirstPageSetup += chapter['name'] + " & \\pageref{" + chapter['id'] + "} \\\\\n"
        latexFirstPageSetup += "\\end{tabular}\n"
        latexFirstPageSetup += "}\n\n" 
        if setup.latex.chapterPagebreak or setup.latex.tableOfContentsPagebreak:
            latexFirstPageSetup += "\clearpage\n\n"
        else:
            latexFirstPageSetup += "\\vspace{0.5cm}\n\n"
    if not setup.latex.bookPrint:
        latexFirstPageSetup = "\\thispagestyle{empty}\n\n\\printtitle\n" + latexFirstPageSetup
     
    
    #substitute latex
    latexTemplate = string.Template(DocumentReader(LATEX_TEMPLATE).getString())
    latexDoc = latexTemplate.substitute(isbn=setup.latex.isbn, document_type=setup.latex.latexDocumentType, geometry=setup.latex.latexGeometry, font_size=setup.latex.latexFontSize, title=setup.latex.latexTitle, subtitle=setup.latex.latexSubtitle, half_title=setup.latex.latexHalfTitle, print_title=setup.latex.printTitle, author=setup.general.author, first_page_setup=latexFirstPageSetup, i_head=setup.general.author, o_head=setup.latex.latexTitle, pdf_title=setup.latex.latexTitle, pdf_author=setup.general.author, pdf_subject=setup.latex.pdfSubject, pdf_keywords=setup.latex.pdfKeywords, has_color_links=setup.latex.hasColorLinks, url_color=setup.latex.urlColor, link_color=setup.latex.linkColor, preliminaries=setup.latex.preliminaries, appendix=setup.latex.appendix)

    with open(OUTFILE_LATEX_DOC, "wb") as f:
        f.write(latexDoc.encode("utf-8"))
    log.info("Wrote UTF-8-encoded LATEX document: %s.", OUTFILE_LATEX_DOC)

    htmlGenerator = HtmlGenerator(setup, inputMarkup, filters, HTML_TEMPLATE, OUTFILE_HTML)
    htmlGenerator.createOutputFile()

class Setup(object):
    def __init__(self, setupFilePath):
        setupFileString = DocumentReader(setupFilePath).getString()
        self.setupToml = toml.loads(setupFileString)
        self.general = GeneralSetupData(self.setupToml)
        self.html = HtmlSetupData(self.setupToml, self.general)
        self.latex = LatexSetupData(self.setupToml, self.general)
    
class GeneralSetupData(object):
    def __init__(self, setupToml):
        self.title = setupToml['general']['title']
        self.subtitle = setupToml['general']['subtitle']
        self.author = setupToml['general']['author']
        self.language = setupToml['general']['language']   

class HtmlSetupData(object):        
    def __init__(self, setupToml, general):
        self.locale = setupToml['html']['locale']
        if 'title' in setupToml['html']:
            self.title = setupToml['html']['title']
        else:
            self.title = general.title
        if 'subtitle' in setupToml['html']:
            self.subtitle = setupToml['html']['subtitle']
        else:
            self.subtitle = general.subtitle
        if self.subtitle == "":
            self.subtitleTag = ""
        else:
            self.subtitleTag = '<p class="subtitle">%s</p>\n' % self.subtitle
        self.headerTitle = setupToml['html']['headertitle']
        self.metaDescription = setupToml['html']['metadescription']
        self.url = setupToml['html']['url']
        self.siteName = setupToml['html']['sitename']
        if 'previewimage' in setupToml['html']:
            self.ogImageTag = '<meta property="og:image" content="%s" />' % setupToml['html']['previewimage']
        else:
            self.ogImageTag = ""
 
class LatexSetupData(object):        
    def __init__(self, setupToml, general): 

        #table of contents setup
        if 'tableOfContents' in setupToml['latex'] and setupToml['latex']['tableOfContents'].lower() == "true":
            self.tableOfContents = True
            if 'contentsTitle' in setupToml['latex'] and setupToml['latex']['contentsTitle'] != "":
                self.latexContentsTitle = setupToml['latex']['contentsTitle']
            if 'tableOfContentsPagebreak' in setupToml['latex'] and setupToml['latex']['tableOfContentsPagebreak'].lower() == "true":
                self.tableOfContentsPagebreak = True
            else:
                self.tableOfContentsPagebreak = False
        else:
            self.tableOfContents = False
        
        #book print setup
        self.preliminaries = ""
        self.appendix = ""
        if 'bookPrint' in setupToml['latex'] and setupToml['latex']['bookPrint'].lower() == "true":
            self.bookPrint = True
            self.latexDocumentType = "scrbook"
            
            #adding preliminary pages     
            for root, dirs, files in os.walk(PRELIMINARIES_PATH):
                if files:
                    log.info("Preliminary pages:")
                for name in files:
                    log.info("  " + name)
                    self.preliminaries += "\\input{" + PRELIMINARIES_LATEX_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
            #adding appendix pages
            for root, dirs, files in os.walk(APPENDIX_PATH):
                if files:
                    log.info("Appendix pages:")
                for name in files:
                    log.info("  " + name)
                    self.appendix += "\\input{" + APPENDIX_LATEX_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
        else:
            self.bookPrint = False
            self.latexDocumentType = "scrreprt"
            
        #chapter pagebreak
        if 'chapterPagebreak' in setupToml['latex'] and setupToml['latex']['chapterPagebreak'].lower() == "true":
            self.chapterPagebreak = True
        else:
            self.chapterPagebreak = True

        #isbn
        if 'isbn' in setupToml['latex']:
            self.isbn = setupToml['latex']['isbn']
        else:
            self.isbn = ""
        
        #geometry
        self.latexGeometry = "\\usepackage["
        if 'pageFormat' in setupToml['latex']:
            self.latexGeometry += "%spaper" % setupToml['latex']['pageFormat']
        elif 'pageWidth' in setupToml['latex'] and 'pageHeight' in setupToml['latex']:
            self.latexGeometry += "paperwidth=%s, paperheight=%s" % (setupToml['latex']['pageWidth'], setupToml['latex']['pageHeight'], )
        else:#default            
            self.latexGeometry += "a5paper"
        if 'bindingOffset' in setupToml['latex']:
            self.latexGeometry += ", bindingoffset=%s" % setupToml['latex']['bindingOffset']
        self.latexGeometry += ", heightrounded, vmarginratio=1:1]{geometry}"
        
        #font size
        if 'fontSize' in setupToml['latex']:
            self.latexFontSize = "fontsize=%spt," % setupToml['latex']['fontSize']
        else:
            self.latexFontSize = "fontsize=11pt,"
        
        #title setup
        if 'title' in setupToml['latex']:
            self.latexTitle = setupToml['latex']['title']
        else:
            self.latexTitle = general.title
        if 'subtitle' in setupToml['latex']:
            self.latexSubtitle = setupToml['latex']['subtitle']
        else:
            self.latexSubtitle = general.subtitle
        self.printTitle = "\\begin{center}\n"
        if setupToml['latex']['printAuthorOnTitle'] == 'true':
            self.printTitle += "{\\large \\storyauthor}\n\n\\vspace{0.6cm}\n"   
        self.printTitle += "{\\huge \\storytitle}\n"
        if self.latexSubtitle != "":
            self.printTitle += "\n\\vspace{0.3cm}\n{\\large \\storysubtitle}\n"
        self.printTitle += "\\end{center}\n"
        self.latexHalfTitle = self.latexTitle
        if 'halfTitle' in setupToml['latex']:
            self.latexHalfTitle = setupToml['latex']['halfTitle']

        #pdf keywords
        self.pdfSubject = setupToml['latex']['pdfsubject']
        self.pdfKeywords = setupToml['latex']['pdfkeywords']
        self.hasColorLinks = setupToml['latex']['hascolorlinks']
        self.urlColor = setupToml['latex']['urlcolor']
        self.linkColor = setupToml['latex']['linkcolor']        
    
class HtmlGenerator(object):
    def __init__(self, setup, inputMarkup, filters, templateFilePath, outputFilePath):
        self.templateFilePath = templateFilePath
        self.outputFilePath = outputFilePath
        self.applyFilters(filters, inputMarkup)
        self.substitute(setup)

    def applyFilters(self, filters, inputMarkup):
        # Push original contents through HTML filters (same order, order matters).
        self.outputHtml = inputMarkup
        for f in filters:
            log.info("Process with %s", f)
            self.outputHtml = f.to_html(self.outputHtml)
            log.info("Done.")   

    def substitute(self, setup):
        log.info("Performing HTML template substitution")
        htmlTemplate = string.Template(DocumentReader(self.templateFilePath).getString())
        self.htmlDoc = htmlTemplate.substitute(html_content=self.outputHtml, lang=setup.general.language, locale=setup.html.locale, header_title=setup.html.headerTitle, title=setup.html.title, subtitle_tag=setup.html.subtitleTag, author=setup.general.author, meta_description=setup.html.metaDescription, url=setup.html.url, site_name=setup.html.siteName, og_image_tag=setup.html.ogImageTag)    
        
    def createOutputFile(self):
        with open(self.outputFilePath, "wb") as f:
            f.write(self.htmlDoc.encode("utf-8"))
        log.info("Wrote UTF-8-encoded HTML document: %s.", self.outputFilePath)    
    
class DocumentReader(object):
    def __init__(self, documentPath):
        self.documentPath = documentPath
        if not os.path.isfile(self.documentPath):
            sys.exit("File not found: %s" % self.documentPath)        
        log.info("Reading file: %s.", self.documentPath)
        with open(self.documentPath, "rb") as f:
            self.fileString = f.read().decode("utf-8").strip()
            
    def getString(self):
        return self.fileString

class Filter(object):
    def __init__(self):
        pass

    def __str__(self):
        return self.__class__.__name__

# Lines beginning with ## will be formatted as headlines
class FilterHeadlines(Filter):
    def to_html(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            result = "<h2>%s</h2>" % (text, )
            return result

        pattern = '^<p.*>##\s*(.*?)</p>$'
        new, n = re.subn(pattern, replacefunc, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            chaptersCount = len(latexChapters)
            labelText = str(chaptersCount) + text
            latexChapters.append({'id':labelText, 'name':text})
            result = "\n{\\label{%s}\\vspace{0.5cm}\\noindent\\LARGE %s}" % (labelText, text, )
            if latexChapterPagebreak and chaptersCount > 0:
                result = "\\clearpage\n\n" + result
            return result

        pattern = '^##\s*(.*?)$'
        new, n = re.subn(pattern, replacefunc, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new

class FilterDots(Filter):
    def to_html(self, s):
        return s.replace("...", "&hellip; ")

    def to_latex(self, s):
        return s.replace("...", r"\dots ")


class FilterQuotes(Filter):
    def to_html(self, s):
        def replacefunc(matchobj):
            quote = matchobj.group(1)
            # Implement paragraphs with vertical space and w/o indentation.
            quote = quote.replace('<p class=$DQ$indent$DQ$>', "<p>")
            result = "»%s«" % (quote, )
            return result

        pattern = '"(.*?)"'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        # Restore HTML doublequotes.
        new = new.replace("$DQ$", '"')
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            """
            Paragraphs within quotations should not be indented.
            In this func, also filter the quote *contents* to implement
            this criterion.
            """
            # Extract quote content.
            quote = matchobj.group(1)
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
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        return new

# Text surrounded by double underscores or double asterisks will be shown bold
class FilterBold(Filter):
    def to_html(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            result = "<strong>%s</strong>" % (text, )
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        pattern = '\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replacefunc, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n+m)
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            result = "\\textbf{%s}" % text
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        pattern = '\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replacefunc, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n+m)
        return new
		
# Text surrounded by underscores or asterisks will be shown in italics
class FilterItalics(Filter):
    def to_html(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            result = "<em>%s</em>" % (text, )
            return result

        pattern = '_(.*?)_'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        pattern = '\*(.*?)\*'
        new, m = re.subn(pattern, replacefunc, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n+m)
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            text = matchobj.group(1)
            result = "\\textit{%s}" % text
            return result

        pattern = '_(.*?)_'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        pattern = '\*(.*?)\*'
        new, m = re.subn(pattern, replacefunc, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n+m)
        return new

class FilterImages(Filter):
    #![Alt text](/path/to/img.jpg "optional title")
    pattern = '!\[(.*)\]\(([^")]*)(\s"(.*)")?\)'
    
    def to_html(self, s):
        def replacefunc(matchobj):
            altText = matchobj.group(1)
            path = matchobj.group(2)
            title = matchobj.group(4)
            result = '<figure class=$DQ$textimage$DQ$>\n'
            result += '<img src=$DQ$%s$DQ$ alt=$DQ$%s$DQ$ ' % (path, altText, )
            #if title != None:
            #    result += 'title=$DQ$%s$DQ$ ' %(title, )
            result += ' />\n'
            if title != None:
                result += '<figcaption>%s</figcaption>\n' % (title, )
            result += '</figure>'
            return result

        new, n = re.subn('^<p.*>' + self.pattern + '</p>$', replacefunc, s, flags=re.MULTILINE)
        log.info("Made %s image replacements.", n)
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            altText = matchobj.group(1)
            path = matchobj.group(2)
            title = matchobj.group(4)
            result = '\\begin{figure}$squareBracketOpen$!ht$squareBracketClose$\n'
            result += '\\centering\n'
            maxHeight = '1.0\\textheight'
            caption = ''
            if title != None:
                maxHeight = '0.9\\textheight'
                caption = '\\caption$asterisk${%s}\n' %(title, )
            result += '\\includegraphics$squareBracketOpen$max height=' + maxHeight + ',max width=1.0\\textwidth$squareBracketClose${%s}\n' % (path, )
            result += caption
            result += '\\end{figure}'
            return result
            
        new, n = re.subn(self.pattern, replacefunc, s)
        log.info("Made %s image replacements.", n)
        return new

class FilterConvertLineEndings(Filter):
    
    def _convert(self, s):
        new = s.replace("\r\n", "\n") # Windows
        new = new.replace("\r", "\n") # Mac
        return new

    def to_html(self, s):
        return self._convert(s)

    def to_latex(self, s):
        return self._convert(s)

class FilterSectionsParagraphs(Filter):

    def _convert(self, s, secsep, parsep):
        _tmp_sectionspacer = "$NEWSECTION$"
        # First remember and shim places with two LF (section separator).
        new = s.replace("\n\n", _tmp_sectionspacer)
        # Replace single LF with paragraph separator.
        new = new.replace("\n", parsep)
        # Replace original two-LFs with markup for new section.
        new = new.replace(_tmp_sectionspacer, secsep)
        return new

    def to_html(self, s):
        sectionsep = "</p>\n</section>\n\n\n<section>\n<p>"
        # Temporarily shim HTML double quotes.
        paragraphsep = '</p>\n\n<p class=$DQ$indent$DQ$>'
        new = self._convert(s, sectionsep, paragraphsep)
        new = "<section>\n<p>%s</p>\n</section>" % (new, )
        return new

    def to_latex(self, s):
        sectionsep = "\n\n\\vspace{0.5cm}\\noindent\n"
        paragraphsep = "\n\n"
        return self._convert(s, sectionsep, paragraphsep)

#structure for defining how to escape and restore special characters
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
escapeRoutes = [
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
    #EscapeRoute('\\', '', '', ''),
]

class FilterMaskEscapedCharacters(Filter):
    def _convert(self, s):
        new = s
        for i in escapeRoutes:
            new = new.replace(i.original, i.temporary)
        return new
           
    def to_html(self, s):
        return self._convert(s)
    
    def to_latex(self, s):
        return self._convert(s)

class FilterRestoreEscapedCharacters(Filter):
    def to_html(self, s):
        new = s
        for i in escapeRoutes:
            new = new.replace(i.temporary, i.html)
        return new
    
    def to_latex(self, s):
        new = s
        for i in escapeRoutes:
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

    def _repair_footnote_ids(self, s):
        id = 'sn-tufte-handout'
        index = 1
        while True:
            s, n = re.subn(id + '(?!\d)', (id + str(index)), s, 2)
            index += 1
            if n < 2: break
        return s

    def to_html(self, s):
        repl = (
            '<label for="sn-tufte-handout" class="margin-toggle sidenote-number">'
            '</label><input type="checkbox" id="sn-tufte-handout" class="margin-toggle"/>'
            '<span class="sidenote">\\1</span>')
        # Temporarily shim HTML double quotes.
        repl = repl.replace('"', "$DQ$")
        return self._repair_footnote_ids(self._convert(s, repl))

    def to_latex(self, s):
        return self._convert(s, r"\\footnote{\1}")


if __name__ == "__main__":
    main()
