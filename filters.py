# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals
import re

from escaperoutes import escape_all, escape_to_html, escape_to_latex, get_escape
from logger import log

latex_chapters = None


def get_latex_chapters():
    if latex_chapters is None:
        return []
    return latex_chapters.chapters


def get_filters(setup):
    # initialize collecting of latex chapters
    global latex_chapters
    latex_chapters = ChapterCollector()

    filters = [
        FilterConvertLineEndings(),  # do first
        FilterMaskEscapedCharacters(),  # do second
        FilterHyphens(),
        FilterSectionsParagraphs(),  # introduces HTML-minuses, do after FilterHyphens
        FilterHeadlines(setup.latex.chapter_pagebreak, setup.latex.hide_chapter_header),
        FilterImages(),  # do before FilterFootnotes
        FilterComments(setup.general.output_mode == "draft"),  # do before FilterFootnotes and after FilterImages
        FilterFootnotes(),
        FilterQuotes(),
        FilterBold(),  # do before FilterItalics
        FilterItalics(),
        FilterDots(),
        FilterRestoreEscapedCharacters(),  # do last
    ]
    return filters


class ChapterCollector(object):
    def __init__(self):
        self.chapters = []

    def add_chapter(self, name):
        label_text = str(self.count()) + name
        self.chapters.append({'id': label_text, 'name': name})
        return label_text

    def count(self):
        return len(self.chapters)


class Filter(object):
    def __init__(self):
        pass

    @classmethod
    def mask_substring(cls, string, substring, masked_substring):
        return string.replace(substring, masked_substring)

    @classmethod
    def mask_double_quotes(cls, string):
        return cls.mask_substring(string, '"', '$DQ$')

    @classmethod
    def add_running_index_to_pattern(cls, string, pattern, start_index=1):
        index = start_index
        while True:
            string, n = re.subn(pattern + r'(?!\d)', (pattern + str(index)), string, 2)
            index += 1
            if n < 2:
                break
        return string

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
            result = "<h2>%s</h2>" % (text,)
            return result

        pattern = r'^<p.*>##\s*(.*?)</p>$'
        new, n = re.subn(pattern, replace_func, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            old_chapter_count = latex_chapters.count()
            label_text = latex_chapters.add_chapter(text)
            result = "\n{\\label{%s}\\vspace{0.5cm}\\noindent\\LARGE %s}\n\\renewcommand{\\storychapter}{%s}" \
                     % (label_text, text, text,)
            if self.latex_chapter_pagebreak and old_chapter_count > 0:
                result = "\\clearpage\n\n" + result
            if self.latex_hide_chapter_header:
                result += "\n\\thispagestyle{empty}"
            return result

        pattern = r'^##\s*(.*?)$'
        new, n = re.subn(pattern, replace_func, s, flags=re.MULTILINE)
        log.info("Made %s headline replacements.", n)
        return new


class FilterDots(Filter):
    def to_html(self, s):
        return s.replace("...", "&hellip;")

    def to_latex(self, s):
        return s.replace("...", r"{\dots}")


class FilterQuotes(Filter):
    def to_html(self, s):
        def replace_func(match_obj):
            quote = match_obj.group(1)
            # Implement paragraphs with vertical space and w/o indentation.
            quote = quote.replace('<p class=$DQ$indent$DQ$>', "<p>")
            result = "»%s«" % (quote,)
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
            result = "<strong>%s</strong>" % (text,)
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = r'\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n + m)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "{\\boldfont\\textbf{%s}}" % text
            return result

        pattern = '__(.*?)__'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = r'\*\*(.*?)\*\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s bold replacements.", n + m)
        return new


# Text surrounded by underscores or asterisks will be shown in italics
class FilterItalics(Filter):
    def to_html(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            result = "<em>%s</em>" % (text,)
            return result

        pattern = '_(.*?)_'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = r'\*(.*?)\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n + m)
        return new

    def to_latex(self, s):
        def replace_func(match_obj):
            text = match_obj.group(1)
            if "\n" in text:  # itshape works over multiple lines but gets easily disturbed
                result = "\\begin{itshape}%s\\end{itshape}" % text
            else:  # \textit can be combined with \textbf etc. but does not work over multiple lines
                result = "\\textit{%s}" % text
            return result

        pattern = r'_(.*?)_'
        new, n = re.subn(pattern, replace_func, s, flags=re.DOTALL)
        pattern = r'\*(.*?)\*'
        new, m = re.subn(pattern, replace_func, new, flags=re.DOTALL)
        log.info("Made %s italic replacements.", n + m)
        return new


class FilterImages(Filter):
    # ![Alt text](/path/to/img.jpg "optional title")
    pattern = r'!\[(.*)\]\(([^")]*)(\s"(.*)")?\)'

    def to_html(self, s):
        def replace_func(match_obj):
            alt_text = match_obj.group(1)
            path = match_obj.group(2)
            title = match_obj.group(4)
            result = '<figure class=$DQ$textimage$DQ$>\n'
            result += '<img src=$DQ$%s$DQ$ alt=$DQ$%s$DQ$ ' % (path, alt_text,)
            # if title != None:
            #     result += 'title=$DQ$%s$DQ$ ' %(title, )
            result += ' />\n'
            if title is not None:
                result += '<figcaption>%s</figcaption>\n' % (title,)
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
            result = '\\begin{figure}' + get_escape('[') + '!ht' + get_escape(']') + '\n'
            result += '\\centering\n'
            max_height = '1.0\\textheight'
            caption = ''
            if title is not None:
                max_height = '0.9\\textheight'
                caption = '\\caption$asterisk${%s}\n' % (title,)
            result += '\\includegraphics' + get_escape('[') + 'max height=' + max_height \
                      + ',max width=1.0\\textwidth' + get_escape(']') + '{%s}\n' % (path,)
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
        new = "<section>\n<p>%s</p>\n</section>" % (new,)
        return new

    def to_latex(self, s):
        section_sep = "\n\n\\vspace{0.5cm}\\noindent\n"
        paragraph_sep = "\n\n"
        return self._convert(s, section_sep, paragraph_sep)


class FilterMaskEscapedCharacters(Filter):
    def _convert(self, s):
        return escape_all(s)

    def to_html(self, s):
        return self._convert(s)

    def to_latex(self, s):
        return self._convert(s)


class FilterRestoreEscapedCharacters(Filter):
    def to_html(self, s):
        return escape_to_html(s)

    def to_latex(self, s):
        return escape_to_latex(s)


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
        pattern = r"\[(.*?)\]"
        new, n = re.subn(pattern, replacement, s, flags=re.DOTALL)
        log.info("Made %s footnote replacements.", n)
        return new

    @classmethod
    def add_footnote_indices(cls, string):
        return cls.add_running_index_to_pattern(string, 'sn-tufte-handout')

    def to_html(self, s):
        replacement = self.mask_double_quotes(
            '<label for="sn-tufte-handout" class="margin-toggle sidenote-number">'
            '</label><input type="checkbox" id="sn-tufte-handout" class="margin-toggle"/>'
            '<span class="sidenote">\\1</span>')
        return self.add_footnote_indices(self._convert(s, replacement))

    def to_latex(self, s):
        return self._convert(s, r"\\footnote{\1}")


class FilterComments(Filter):
    def __init__(self, show_comments):
        super(FilterComments, self).__init__()
        self.show_comments = show_comments

    def _convert(self, input_text, pattern, replacement_pattern, log_string="commentary"):
        output, n = re.subn(pattern, replacement_pattern, input_text, flags=re.DOTALL)
        log.info("Made %s %s replacements.", n, log_string)
        return output

    @classmethod
    def add_comment_indices(cls, string):
        return cls.add_running_index_to_pattern(string, 'sn-tufte-comment')

    def to_html(self, input_text):
        # text highlighting
        highlighting_pattern = r'\(\((.*?)\)\)'
        if self.show_comments:
            highlighting_replacement_pattern = self.mask_double_quotes('<span class="highlighted">\\1</span>')
        else:
            highlighting_replacement_pattern = '\\1'
        output_text = self._convert(input_text, highlighting_pattern, highlighting_replacement_pattern,
                                         "text highlighting")
        # inline comment
        inline_pattern = r'\{\{(.*?)\}\}'
        if self.show_comments:
            inline_replacement_pattern = self.mask_double_quotes('<span class="inline-comment">\\1</span>')
        else:  # TODO may create empty <p>-tags and so mess with text indent
            inline_replacement_pattern = ''
        output_text = self._convert(output_text, inline_pattern, inline_replacement_pattern, "inline commentary")

        # sidenote comment
        comment_pattern = r'\[\[(.*?)\]\]'
        if self.show_comments:
            comment_replacement_pattern = self.mask_double_quotes(
                '<label for="sn-tufte-comment" class="margin-toggle sidenote-comment-number">'
                '</label><input type="checkbox" id="sn-tufte-comment" class="margin-toggle"/>'
                '<span class="sidenote-comment">\\1</span>')
        else:
            comment_replacement_pattern = ''
        return self.add_comment_indices(self._convert(output_text, comment_pattern, comment_replacement_pattern))

    def to_latex(self, input_text):
        # text highlighting
        input_pattern = r'\(\((.*?)\)\)'
        replacement_pattern = r'\\wiggle{\1}'
        processed_text = self._convert(input_text, input_pattern, replacement_pattern, "text highlighting")

        # inline comment  # TODO when not in draft mode there are cases where inline comments create empty lines
        input_pattern = r'\{\{(.*?)\}\}'
        replacement_pattern = r'{\\todo$squareBracketOpen$inline$squareBracketClose${\1}}'
        processed_text = self._convert(processed_text, input_pattern, replacement_pattern, "inline commentary")

        # sidenote comment
        input_pattern = r'\[\[(.*?)\]\]'
        replacement_pattern = r'{\\todo{\1}}'
        return self._convert(processed_text, input_pattern, replacement_pattern)
