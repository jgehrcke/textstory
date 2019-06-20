# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals


# returns the string with all special expressions replaced by temporary escapes
def escape_all(string):
    escaped_string = string
    for name, escape_route in escape_routes.items():
        escaped_string = escaped_string.replace(escape_route.original, escape_route.temporary)
    return escaped_string


# returns the string with the named special expression replaced by temporary escapes
def escape(string, escape_route_name):
    escape_route = escape_routes[escape_route_name]
    return string.replace(escape_route.original, escape_route.temporary)


# returns the string with temporary escapes replaced by html escapes
def escape_to_html(string):
    escaped_string = string
    for name, escape_route in escape_routes.items():
        escaped_string = escaped_string.replace(escape_route.temporary, escape_route.html)
    return escaped_string


#  returns the string with temporary escapes replaced by latex escapes
def escape_to_latex(string):
    escaped_string = string
    for name, escape_route in escape_routes.items():
        escaped_string = escaped_string.replace(escape_route.temporary, escape_route.latex)
    return escaped_string


# returns the temporary escape with the given name
def get_escape(name):
    return escape_routes[name].temporary


# structure for defining how to escape and restore special characters
class EscapeRoute(object):
    def __init__(self, original, temporary, html, latex):
        self.original = original
        self.temporary = temporary
        self.html = html
        self.latex = latex


r"""
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
()  normal brackets
[]  square brackets
#   hash mark
"   doublequote
!   exclamation mark (only needs to be escaped when followed by '[')
--  double minus

"""
escape_routes = {
    "\\": EscapeRoute('\\\\', '$escapeChar$', '\\', '\\textbackslash{}'),
    "&": EscapeRoute('&', '$amp$', '&amp;', '\\&'),
    "<": EscapeRoute('<', '$lt$', '&lt;', '<'),
    ">": EscapeRoute('>', '$gt$', '&gt;', '>'),
    "%": EscapeRoute('%', '$percent$', '%', '\\% '),
    "$": EscapeRoute('\\$', '$dollar$', '$', '\\$ '),
    "#": EscapeRoute('\\#', '$hash$', '#', '\\# '),
    "_": EscapeRoute('\\_', '$underscore$', '_', '\\_ '),
    "{": EscapeRoute('\\{', '$curlyBracketOpen$', '{', '\\{ '),
    "}": EscapeRoute('\\}', '$curlyBracketClose$', '}', '\\} '),
    "(": EscapeRoute('\\(', '$bracketOpen$', '(', '('),
    ")": EscapeRoute('\\)', '$bracketClose$', ')', ')'),
    "[": EscapeRoute('\\[', '$squareBracketOpen$', '[', '['),
    "]": EscapeRoute('\\]', '$squareBracketClose$', ']', ']'),
    "~": EscapeRoute('~', '$tilde$', '~', '\\textasciitilde{}'),
    "^": EscapeRoute('^', '$circumflex$', '^', '\\textasciicircum{}'),
    "*": EscapeRoute('\\*', '$asterisk$', '*', '*'),
    "--": EscapeRoute('\\--', '$hyphen$', '--', '\\verb|--|'),
    '"': EscapeRoute('\\"', '$doubleQuote$', '&quot;', '"{}'),
    "!": EscapeRoute('\\!', '$exclamation$', '!', '!'),
    # "": EscapeRoute('\\', '', '', ''),
}
