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

    setupData = DocumentReader(SETUP_FILE).getString()
    setup = toml.loads(setupData)

    #this needs to be set before LaTeX body is 
    if 'chapterPagebreak' in setup['latex'] and setup['latex']['chapterPagebreak'].lower() == "true":
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
        
    #setup general substitutions
    title = setup['general']['title']
    subtitle = setup['general']['subtitle']
    author = setup['general']['author']
    language = setup['general']['language']
    
       
    #setup latex substitutions
    preliminaries = ""
    appendix = ""
    if 'tableOfContents' in setup['latex'] and setup['latex']['tableOfContents'].lower() == "true":
        latexFirstPageSetup = "\\thispagestyle{empty}\n\n{\\large\n"
        if 'contentsTitle' in setup['latex'] and setup['latex']['contentsTitle'] != "":
            latexContentsTitle = setup['latex']['contentsTitle']
            latexFirstPageSetup += "\n{\\vspace{0.5cm}\\noindent\\LARGE %s}\n\n" % latexContentsTitle
        latexFirstPageSetup += "\\vspace{0.5cm}\\noindent\\begin{tabular}{lr}\n"
        for chapter in latexChapters:
            latexFirstPageSetup += chapter['name'] + " & \\pageref{" + chapter['id'] + "} \\\\\n"
        latexFirstPageSetup += "\\end{tabular}\n"
        latexFirstPageSetup += "}\n\n" 
        if latexChapterPagebreak or 'tableOfContentsPagebreak' in setup['latex'] and setup['latex']['tableOfContentsPagebreak'].lower() == "true":
            latexFirstPageSetup += "\clearpage\n\n"
        else:
            latexFirstPageSetup += "\\vspace{0.5cm}\n\n"
    else:
        latexFirstPageSetup = ""
    if 'bookPrint' in setup['latex'] and setup['latex']['bookPrint'].lower() == "true":
        latexDocumentType = "scrbook"
        
        #adding preliminary pages     
        for root, dirs, files in os.walk(PRELIMINARIES_PATH):
            for name in files:
                log.info("adding preliminary page " + name)
                preliminaries += "\\input{" + PRELIMINARIES_LATEX_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
        #adding appendix pages
        for root, dirs, files in os.walk(APPENDIX_PATH):
            for name in files:
                log.info("adding appendix page " + name)
                appendix += "\\input{" + APPENDIX_LATEX_PATH + name[:len(name)-4] + "}\n\\clearpage\n"
    else:
        latexDocumentType = "scrreprt"
        latexFirstPageSetup = "\\thispagestyle{empty}\n\n\\printtitle\n" + latexFirstPageSetup
    latexGeometry = "\\usepackage["
    if 'isbn' in setup['latex']:
        isbn = setup['latex']['isbn']
    else:
        isbn = ""
    if 'pageFormat' in setup['latex']:
        latexGeometry += "%spaper" % setup['latex']['pageFormat']
    elif 'pageWidth' in setup['latex'] and 'pageHeight' in setup['latex']:
        latexGeometry += "paperwidth=%s, paperheight=%s" % (setup['latex']['pageWidth'], setup['latex']['pageHeight'], )
    else:
        #default
        latexGeometry += "a5paper"
    if 'bindingOffset' in setup['latex']:
        latexGeometry += ", bindingoffset=%s" % setup['latex']['bindingOffset']
    latexGeometry += ", heightrounded, vmarginratio=1:1]{geometry}"
    if 'fontSize' in setup['latex']:
        latexFontSize = "fontsize=%spt," % setup['latex']['fontSize']
    else:
        latexFontSize = "fontsize=11pt,"
    if 'title' in setup['latex']:
        latexTitle = setup['latex']['title']
    else:
        latexTitle = title
    if 'subtitle' in setup['latex']:
        latexSubtitle = setup['latex']['subtitle']
    else:
        latexSubtitle = subtitle
    printTitle = "\\begin{center}\n"
    if setup['latex']['printAuthorOnTitle'] == 'true':
        printTitle += "{\\large \\storyauthor}\n\n\\vspace{0.6cm}\n"   
    printTitle += "{\\huge \\storytitle}\n"
    if latexSubtitle != "":
        printTitle += "\n\\vspace{0.3cm}\n{\\large \\storysubtitle}\n"
        #latexSubtitle = '\n\\vspace{0.1cm}\n\n\\noindent\n\\textit{%s}\n' % latexSubtitle
    printTitle += "\\end{center}\n"

    latexHalfTitle = latexTitle
    if 'halfTitle' in setup['latex']:
        latexHalfTitle = setup['latex']['halfTitle']

    pdfSubject = setup['latex']['pdfsubject']
    pdfKeywords = setup['latex']['pdfkeywords']
    hasColorLinks = setup['latex']['hascolorlinks']
    urlColor = setup['latex']['urlcolor']
    linkColor = setup['latex']['linkcolor']    
    
    #substitute latex
    latexTemplate = string.Template(DocumentReader(LATEX_TEMPLATE).getString())
    latexDoc = latexTemplate.substitute(isbn=isbn, document_type=latexDocumentType, geometry=latexGeometry, font_size=latexFontSize, title=latexTitle, subtitle=latexSubtitle, half_title=latexHalfTitle, print_title=printTitle, author=author, first_page_setup=latexFirstPageSetup, i_head=author, o_head=latexTitle, pdf_title=latexTitle, pdf_author=author, pdf_subject=pdfSubject, pdf_keywords=pdfKeywords, has_color_links=hasColorLinks, url_color=urlColor, link_color=linkColor, preliminaries=preliminaries, appendix=appendix)

    with open(OUTFILE_LATEX_DOC, "wb") as f:
        f.write(latexDoc.encode("utf-8"))
    log.info("Wrote UTF-8-encoded LATEX document: %s.", OUTFILE_LATEX_DOC)

    # Push original contents through HTML filters (same order, order matters).
    outputHtml = inputMarkup
    for f in filters:
        log.info("Process with %s", f)
        outputHtml = f.to_html(outputHtml)
        log.info("Done.")

    log.info("Read HTML template file: %s.", HTML_TEMPLATE)
    with open(HTML_TEMPLATE, "rb") as f:
        htmltemplate = string.Template(f.read().decode("utf-8").strip())

    log.info("Perform HTML template substitution")
    #setup html substitutions
    lang = language
    locale = setup['html']['locale']
    if 'title' in setup['html']:
        htmlTitle = setup['html']['title']
    else:
        htmlTitle = title
    if 'subtitle' in setup['html']:
        htmlSubtitle = setup['html']['subtitle']
    else:
        htmlSubtitle = subtitle
    if htmlSubtitle == "":
        subtitleTag = ""
    else:
        subtitleTag = '<p class="subtitle">%s</p>\n' % htmlSubtitle
    headerTitle = setup['html']['headertitle']
    metaDescription = setup['html']['metadescription']
    url = setup['html']['url']
    siteName = setup['html']['sitename']
    if 'previewimage' in setup['html']:
        ogImageTag = '<meta property="og:image" content="%s" />' % setup['html']['previewimage']
    else:
        ogImageTag = ""
    #substitute html
    htmldoc = htmltemplate.substitute(html_content=outputHtml, lang=lang, locale=locale, header_title=headerTitle, title=htmlTitle, subtitle_tag=subtitleTag, author=author, meta_description=metaDescription, url=url, site_name=siteName, og_image_tag=ogImageTag)

    with open(OUTFILE_HTML, "wb") as f:
        f.write(htmldoc.encode("utf-8"))
    log.info("Wrote UTF-8-encoded HTML document: %s.", OUTFILE_HTML)

    
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
