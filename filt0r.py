# -*- coding: utf-8 -*-
# Copyright 2015 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import re
import os
import sys
import string
import logging


logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)


OUTFILE_LATEX = "latex/latex-body.tex"
OUTFILE_HTML = "html/index.html"
HTML_TEMPLATE = "html/index.tpl.html"


def main():
    if len(sys.argv) < 2:
        sys.exit("First argument must be path to document source.")
    infile_path = sys.argv[1]
    if not os.path.isfile(infile_path):
        sys.exit("File not found: %s" % infile_path)
    with open(infile_path, "rb") as f:
        inputtext = f.read().decode("utf-8").strip()
    filters = [
        FilterMaskEscapedCharacters(), # needs to be done first
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
    outputlatex = inputtext
    for f in filters:
        log.info("Process with %s", f)
        outputlatex = f.to_latex(outputlatex)
        log.info("Done.")
    with open(OUTFILE_LATEX, "wb") as f:
        f.write(outputlatex.encode("utf-8"))
    log.info("Wrote UTF-8-encoded LaTeX source file: %s.", OUTFILE_LATEX)

    # Push original contents through HTML filters (same order, order matters).
    outputhtml = inputtext
    for f in filters:
        log.info("Process with %s", f)
        outputhtml = f.to_html(outputhtml)
        log.info("Done.")

    log.info("Read HTML template file: %s.", HTML_TEMPLATE)
    with open(HTML_TEMPLATE, "rb") as f:
        htmltemplate = string.Template(f.read().decode("utf-8").strip())

    log.info("Perform HTML template substitution")
    htmldoc = htmltemplate.substitute(html_content=outputhtml)

    with open(OUTFILE_HTML, "wb") as f:
        f.write(htmldoc.encode("utf-8"))
    log.info("Wrote UTF-8-encoded HTML document: %s.", OUTFILE_HTML)


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
            result = "\n{\\vspace{0.5cm}\\noindent\\LARGE %s}" % text
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
        new = s.replace(" -- ", " &ndash; ")
        # One of Josa's quite special cases!
        new = new.replace(" --,", " &ndash;, ")
        return new

    def to_latex(self, s):
        # new = s.replace(" -- ", " --- ")
        # # One of Josa's quite special cases!
        # new = new.replace(" --,", " ---,")
        # return new
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
