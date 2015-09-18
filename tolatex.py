# -*- coding: utf-8 -*-
# Copyright 2015 Jan-Philip Gehrcke. See LICENSE file for details.


from __future__ import unicode_literals
import re
import logging
logging.basicConfig(
    format='%(asctime)s:%(msecs)05.1f  %(levelname)s: %(message)s',
    datefmt='%H:%M:%S')
log = logging.getLogger()
log.setLevel(logging.INFO)


INFILE = "doc-manuell-prozessiert.txt"
OUTFILE = "latex-body.tex"


def main():
    with open(INFILE, "rb") as f:
        contents = f.read().decode("utf-8").strip()
    filters = [
        filter_footnotes,
        filter_spaced_hyphens,
        filter_sections_paragraphs,
        filter_quotes,
        filter_dots
    ]
    for f in filters:
        log.info("Process with %s", f.__name__)
        contents = f(contents)
        log.info("Done.")
    with open(OUTFILE, "wb") as f:
        f.write(contents.encode("utf-8"))
    log.info("Wrote %s.", OUTFILE)


def filter_sections_paragraphs(s):
    two_lf_temp = "$2LF$"
    vspace = "\n\n\\vspace{0.5cm}\\noindent\n"
    # First remember and shim places with two LF.
    new = s.replace("\n\n", two_lf_temp)
    # Replace single LF by two LF (real paragraph)
    new = new.replace("\n", "\n\n")
    # Replace original two-LF places with markup for new section.
    new = new.replace(two_lf_temp, vspace)
    return new


def filter_spaced_hyphens(s):
    new = s.replace(" - ", " --- ")
    new = new.replace(" – ",  " --- ")
    # One of Josa's quite special cases!
    new = new.replace(" –,", " ---,")
    return new


def filter_quotes(s):

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


def filter_footnotes(s):
    pattern = "{(.*?)}"
    repl = r"\\footnote{\1}"
    new, n = re.subn(pattern, repl, s, flags=re.DOTALL)
    log.info("Made %s footnote replacements.", n)
    return new


def filter_dots(s):
    new = s.replace("...", r"\dots ")
    return new.replace("…", r"\dots ")


if __name__ == "__main__":
    main()
