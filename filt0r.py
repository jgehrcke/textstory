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
        FilterHyphens(),
        FilterSectionsParagraphs(), # introduces HTML-minuses, must run after FilterHyphens
        FilterFootnotes(),
        FilterQuotes(),
        FilterDots(),
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


class FilterDots(Filter):
    def to_html(self, s):
        return s.replace("...", "&hellip;")

    def to_latex(self, s):
        return s.replace("...", r"\dots ")


class FilterQuotes(Filter):
    def to_html(self, s):
        def replacefunc(matchobj):
            # Extract quote content.
            quote = matchobj.group(1)
            # Implement paragraphs with vspace and w/o indentation.
            quote = quote.replace(
                '<p class=$DQ$indent$DQ$>', "<p><br />")
            # Implement LaTeX command.
            result = "»%s«" % (quote, )
            return result

        pattern = '"(.*?)"'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        # Restore HTML doublequotes:
        new = new.replace("$DQ$", '"')
        return new

    def to_latex(self, s):
        def replacefunc(matchobj):
            """
            Paragraphs within quotations should not be indented.
            In this func, also filter the quote *contents* to implement
            this criterion. Like this:

            quote = quote.replace("\n\n", "\n\\noindent\n")
            result = "\\enquote{%s}" % quote

            This filter should be invoked late.
            """
            # Extract quote content.
            quote = matchobj.group(1)
            # Implement paragraphs with vspace and w/o indentation.
            quote = quote.replace(
                "\n\n", "\n\n\\vspace{\\baselineskip}\\noindent\n")
            # Implement LaTeX command.
            result = "\\enquote{%s}" % quote
            return result

        # From re.subn docs. "If repl is a function, it is called for every
        # non-overlapping occurrence of pattern. The function takes a single match
        # object argument, and returns the replacement string."
        # Make the search non-greedy, and search across newlines.
        pattern = '"(.*?)"'
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
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


class FilterHyphens(Filter):
    def to_html(self, s):
        new = s.replace(" -- ", " &mdash; ")
        # One of Josa's quite special cases!
        new = new.replace(" --,", " &mdash;, ")
        # All minuses that are left over should be interpreted as n dashes:
        #new = new.replace("-", "&ndash;")
        return new

    def to_latex(self, s):
        new = s.replace(" -- ", " --- ")
        # One of Josa's quite special cases!
        new = new.replace(" --,", " ---,")
        return new


class FilterFootnotes(Filter):
    def _convert(self, s, replacement):
        pattern = "\[(.*?)\]"
        new, n = re.subn(pattern, replacement, s, flags=re.DOTALL)
        log.info("Made %s footnote replacements.", n)
        return new

    def to_html(self, s):
        repl = (
            '<label for="sn-tufte-handout" class="margin-toggle sidenote-number">'
            '</label><input type="checkbox" id="sn-tufte-handout" class="margin-toggle"/>.'
            '<span class="sidenote">\\1</span>')
        # Temporarily shim HTML double quotes.
        repl = repl.replace('"', "$DQ$")
        return self._convert(s, repl)

    def to_latex(self, s):
        return self._convert(s, r"\\footnote{\1}")


if __name__ == "__main__":
    main()
