# -*- coding: utf-8 -*-
# Copyright 2015 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import re
import string
import logging


logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)


INFILE = "doc.txt"
OUTFILE_LATEX = "latex/latex-body.tex"
OUTFILE_HTML = "html/index.html"
HTML_TEMPLATE = "html/index.tpl.html"


def main():
    with open(INFILE, "rb") as f:
        inputtext = f.read().decode("utf-8").strip()
    filters = [
        FilterFootnotes(),
        FilterSpacedHyphens(),
        FilterSectionsParagraphs(),
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
        pass

    def to_latex(self, s):
        new = s.replace("...", r"\dots ")
        return new.replace("…", r"\dots ")


class FilterQuotes(Filter):
    def to_html(self, s):
        pass

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
        pattern = "„(.*?)“"
        new, n = re.subn(pattern, replacefunc, s, flags=re.DOTALL)
        log.info("Made %s quotation replacements.", n)
        return new


class FilterSectionsParagraphs(Filter):
    def to_html(self, s):
        pass

    def to_latex(self, s):
        two_lf_temp = "$2LF$"
        vspace = "\n\n\\vspace{0.5cm}\\noindent\n"
        # First remember and shim places with two LF.
        new = s.replace("\n\n", two_lf_temp)
        # Replace single LF by two LF (real paragraph)
        new = new.replace("\n", "\n\n")
        # Replace original two-LF places with markup for new section.
        new = new.replace(two_lf_temp, vspace)
        return new


class FilterSpacedHyphens(Filter):
    def to_html(self, s):
        pass

    def to_latex(self, s):
        new = s.replace(" - ", " --- ")
        new = new.replace(" – ",  " --- ")
        # One of Josa's quite special cases!
        new = new.replace(" –,", " ---,")
        return new


class FilterFootnotes(Filter):
    def to_html(self, s):
        pass

    def to_latex(self, s):
        pattern = "{(.*?)}"
        repl = r"\\footnote{\1}"
        new, n = re.subn(pattern, repl, s, flags=re.DOTALL)
        log.info("Made %s footnote replacements.", n)
        return new


if __name__ == "__main__":
    main()
