# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.

from __future__ import unicode_literals

import string

from logger import log


class FontManager(object):
    def __init__(self):
        self.fonts = dict()

        # serif

        # self.add_font([], 'accanthis', 'Accanthis')  # TODO fails
        self.add_font([], 'Alegreya', 'Alegreya')
        # self.add_font(['algol'], 'algolrevived', 'Algol Revived')  # TODO fails
        # self.add_font(['Antykwa Poltawskiego', 'poltawski'], 'antpolt', 'Antykwa Półtawskiego')  # TODO fails
        # self.add_font(['Antykwa Poltawskiego Light', 'poltawskilight'], '[light]{antpolt}',
        #              'Antykwa Półtawskiego Light')  # TODO fails
        # self.add_font(['Antykwa Torunska'], '[math]{anttor}', 'Antykwa Toruńska')  # TODO fails
        # self.add_font(['Antykwa Torunska Condensed'], '[condensed,math]{anttor}',
        #              'Antykwa Toruńska Condensed')  # TODO fails
        # self.add_font(['Antykwa Torunska Light'], '[light,math]{anttor}', 'Antykwa Toruńska Light')  # TODO fails
        # self.add_font(['Antykwa Torunska Light Condensed'], '[light,condensed,math]{anttor}',
        #              'Antykwa Toruńska Light Condensed')  # TODO fails
        # http://www.tug.dk/FontCatalogue/asanamath/
        # http://www.tug.dk/FontCatalogue/baskervaldx/
        # self.add_font(['berenis'], 'berenis', 'Berenis ADF')  # TODO fails
        self.add_font([], 'caladea', 'Caladea')
        self.add_font([], 'cochineal', 'Cochineal')
        # self.add_font([], '[el,nf]{coelacanth}', 'Coelacanth Extra Light')  # TODO fails
        # self.add_font([], '[l,nf]{coelacanth}', 'Coelacanth Light')  # TODO fails
        # self.add_font(['Coelacanth'], '[nf]{coelacanth}', 'Coelacanth Regular')  # TODO fails
        # self.add_font([], 'CormorantGaramond', 'Cormorant Garamond')  # TODO fails
        # self.add_font([], '[light]{CormorantGaramond}', 'Cormorant Garamond Light')  # TODO fails
        # self.add_font([], '[extralight]{CrimsonPro}', 'Crimson Pro Extra Light')  # TODO fails
        # self.add_font([], '[light]{CrimsonPro}', 'Crimson Pro Light')  # TODO fails
        # self.add_font([], '[medium]{CrimsonPro}', 'Crimson Pro Medium')  # TODO fails
        # self.add_font(['Crimson Pro'], 'CrimsonPro', 'Crimson Pro Regular')  # TODO fails
        # self.add_font(['Crimson'], 'crimson', 'Crimson Text')  # TODO fails
        self.add_font([], 'DejaVuSerif', 'DejaVu Serif')
        self.add_font([], 'DejaVuSerifCondensed', 'DejaVu Serif Condensed')
        # self.add_font(['DRM', 'Don\'s Revised Modern', 'Dons Revised Modern'], 'drm',
        #              'DRM (Don\'s Revised Modern)')  # TODO fails
        self.add_font([], '[default]{droidserif}', 'Droid Serif')
        # http://www.tug.dk/FontCatalogue/erewhon/
        self.add_font([], 'fbb', 'fbb')
        # self.add_font(['Gandhi'], '[lf]{gandhi}', 'Gandhi Serif')  # TODO fails
        # http://www.tug.dk/FontCatalogue/ebgaramond/
        # self.add_font([], 'garamondx', 'Garamond Expert')  # TODO fails
        # GentiumPlus currently does not support all characters in bold -> use GentiumBasic
        self.add_font(['gentium', 'gentiumplus'], 'gentium', 'GentiumPlus', 'GentiumBasic')
        self.add_font(['Artemisia'], 'gfsartemisia', 'GFS Artemisia')
        self.add_font([], '[default]{gfsbodoni}', 'GFS Bodoni')
        self.add_font(['GNU Freefont Serif', 'Freefont Serif'], None, 'FreeSerif')
        self.add_font([], 'heuristica', 'Heuristica')
        # self.add_font(['Plex Serif Extra Light'], 'plex-otf', 'IBM Plex Serif Extra Light')  # TODO fails
        # self.add_font(['Plex Serif Medium'], 'plex-otf', 'IBM Plex Serif Medium')  # TODO fails
        # self.add_font(['Plex Serif Regular', 'IBM Plex Serif', 'Plex Serif'], 'plex-otf',
        #              'IBM Plex Serif Regular')  # TODO fails
        # self.add_font(['Plex Serif Text'], 'plex-otf', 'IBM Plex Serif Text')  # TODO fails
        # self.add_font(['Plex Serif Thin'], 'plex-otf', 'IBM Plex Serif Thin')  # TODO fails
        self.add_font([], 'imfellEnglish', 'IM Fell English')
        # http://www.tug.dk/FontCatalogue/inriaseriflight/
        # http://www.tug.dk/FontCatalogue/inriaserifregular/
        self.add_font([], None, 'Junicode', 'Junicode-Bold')
        self.add_font(['Computer Modern'], 'lmodern', 'Latin Modern Roman')
        # self.add_font(['Libertinus'], 'libertinus', 'Libertinus Serif')  # TODO fails
        self.add_font(['baskerville'], 'librebaskerville', 'Libre Baskerville')
        self.add_font([], 'LibreBodoni', 'Libre Bodoni')
        # self.add_font(['Caslon'], 'librecaslon', 'Libre Caslon')  # TODO fails
        # self.add_font(['Libertine'], 'libertine', 'Linux Libertine')  # TODO fails
        self.add_font([], 'merriweather', 'Merriweather')
        self.add_font([], '[light]{merriweather}', 'Merriweather Light')
        # self.add_font(['Nimbus Serif'], 'nimbusserif', 'Nimbus 15 Serif')  # TODO fails
        self.add_font([], None, 'Old Standard')
        # self.add_font(['Paratype'], 'paratype', 'Paratype Serif')  # TODO fails
        # self.add_font(['Paratype Caption'], 'PTSerifCaption', 'Paratype Serif Caption')  # TODO fails
        self.add_font([], 'PlayfairDisplay', 'Playfair Display')
        self.add_font([], 'quattrocento', 'Quattrocento')
        self.add_font([], '[rm]{roboto}', 'Roboto Slab')
        self.add_font([], '[rm,light]{roboto}', 'Roboto Slab Light')
        # self.add_font([], '[rm,thin]{roboto}', 'Roboto Slab Thin')  # TODO fails
        # self.add_font([], None, 'Shobhika')  # TODO fails
        self.add_font([], '[default,extralight,semibold]{sourceserifpro}', 'Source Serif Pro Extra Light')
        self.add_font([], '[default,light,bold]{sourceserifpro}', 'Source Serif Pro Light')
        self.add_font(['Source Serif Pro'], '[default,regular,black]{sourceserifpro}',
                     'Source Serif Pro Regular')
        # self.add_font(['stix', 'Stix 2'], 'stickstootext', 'Sticks Too')  # TODO fails
        self.add_font(['Bonum', 'Bookman', 'Gyre Bonum', 'Kerkis', 'URW Bookman', 'URW Bookman L'], 'tgbonum',
                     'TeX Gyre Bonum')
        self.add_font(['Gyre Pagella', 'New PX', 'Pagella', 'Palladio', 'PX Fonts', 'URW Palladio'], 'tgpagella',
                     'TeX Gyre Pagella')
        self.add_font(['Gyre Schola', 'Schola', 'Schoolbook', 'Schoolbook L', 'URW Schoolbook L', 'URW Schoolbook'],
                     'tgschola', 'TeX Gyre Schola')
        self.add_font(['Gyre Termes', 'New TX', 'Nimbus Roman', 'Termes', 'TX Fonts', 'URW Nimbus Roman'], 'tgtermes',
                     'TeX Gyre Termes')
        # self.add_font(['Venturis'], '[lf]{venturis}', 'Venturis ADF')  # TODO fails
        # self.add_font(['venturis2', 'Venturis No2'], 'venturis2', 'Venturis ADF No2')  # TODO fails
        # self.add_font(['venturisold'], 'venturisold', 'Venturis ADF Old')  # TODO fails
        self.add_font([], 'XCharter', 'XCharter')
        self.add_font([], None, 'XITS')

        # sans serif

        # self.add_font([], '[sfdefault]{AlegreyaSans}', 'Alegreya Sans')  # TODO fails
        # self.add_font([], '[sfdefault]{arimo}', 'Arimo')  # TODO fails
        # self.add_font([], 'libertine', 'Biolinum')  # TODO fails
        self.add_font([], '[sfdefault]{cabin}', 'Cabin')
        self.add_font([], '[sfdefault,condensed]{cabin}', 'Cabin Condensed')
        self.add_font([], '[sfdefault,lf]{carlito}', 'Carlito')
        # self.add_font([], '[familydefault,light]{Chivo}', 'Chivo Light')  # TODO fails
        # self.add_font(['Chivo'], '[familydefault,regular]{Chivo}', 'Chivo Regular')  # TODO fails
        self.add_font([], '[sfdefault]{ClearSans}', 'Clear Sans')
        self.add_font([], 'cyklop', 'Cyklop')
        self.add_font([], 'DejaVuSans', 'DejaVu Sans')
        self.add_font([], 'DejaVuSansCondensed', 'DejaVu Sans Condensed')
        self.add_font([], '[defaultsans]{droidsans}', 'Droid Sans')
        # self.add_font(['logo'], 'fetamont', 'Fetamont')  # TODO fails
        self.add_font([], '[sfdefault,book]{FiraSans}', 'Fira Sans Book')
        self.add_font([], '[sfdefault,extralight]{FiraSans}', 'Fira Sans Extra Light')
        self.add_font([], '[sfdefault,light]{FiraSans}', 'Fira Sans Light')
        self.add_font(['Fira Sans'], '[sfdefault]{FiraSans}', 'Fira Sans Regular')
        self.add_font([], '[sfdefault,thin]{FiraSans}', 'Fira Sans Thin')
        self.add_font([], '[sfdefault,ultralight]{FiraSans}', 'Fira Sans Ultra Light')
        # self.add_font([], '[lf,sfdefault]{gandhi}', 'Gandhi Sans')  # TODO fails
        self.add_font(['Neohellenic'], '[default]{gfsneohellenic}', 'GFS Neohellenic')
        # self.add_font([], '[default]{gillius}', 'Gillius')  # TODO fails
        self.add_font(['Freefont Sans', 'GNU Freefont Sans'], None, 'FreeSans')
        # http://www.tug.dk/FontCatalogue/ibmplexmonoregular/
        # http://www.tug.dk/FontCatalogue/ibmplexsansextralight/
        # http://www.tug.dk/FontCatalogue/ibmplexsanslight/
        # http://www.tug.dk/FontCatalogue/ibmplexsansmedium/
        # http://www.tug.dk/FontCatalogue/ibmplexsansregular/
        # http://www.tug.dk/FontCatalogue/ibmplexsanstext/
        # http://www.tug.dk/FontCatalogue/ibmplexsansthin/
        # self.add_font([], '[lining,light]{InriaSans}', 'Inria Sans Light')  # TODO fails
        # self.add_font(['Inria Sans'], '[lining]{InriaSans}', 'Inria Sans Regular')  # TODO fails
        self.add_font([], '[math]{iwona}', 'Iwona')
        # self.add_font([], '[condensed,math]{iwona}', 'Iwona Condensed')  # TODO fails
        self.add_font([], '[light,math]{iwona}', 'Iwona Light')
        # self.add_font([], '[light,condensed,math]{iwona}', 'Iwona Light Condensed')  # TODO fails
        self.add_font([], '[math]{kurier}', 'Kurier')
        # self.add_font([], '[condensed,math]{kurier}', 'Kurier Condensed')  # TODO fails
        self.add_font([], '[light,math]{kurier}', 'Kurier Light')
        # self.add_font([], '[light,condensed,math]{kurier}', 'Kurier Light Condensed')  # TODO fails
        self.add_font(['Computer Modern Sans Serif'], 'lmodern', 'Latin Modern Sans')
        # self.add_font([], 'lmodern', 'Latin Modern Sans Extended')  # TODO fails
        self.add_font([], '[default]{lato}', 'Lato')
        # self.add_font([], 'libertinus', 'Libertinus Sans')  # TODO fails
        self.add_font([], '[sfdefault]{merriweather}', 'Merriweather Sans')
        self.add_font([], '[sfdefault,light]{merriweather}', 'Merriweather Sans Light')
        self.add_font([], '[default]{mintspirit}', 'Mintspirit')
        # self.add_font([], '[defaultfam,extralight,tabular,lining,alternates]{montserrat}', 'Montserrat Alternates Extra Light')  # TODO fails
        # self.add_font([], '[defaultfam,light,tabular,lining,alternates]{montserrat}', 'Montserrat Alternates Light')  # TODO fails
        # self.add_font(['Montserrat Alternates'], '[defaultfam,tabular,lining,alternates]{montserrat}', 'Montserrat Alternates Regular')  # TODO fails
        # self.add_font([], '[defaultfam,extralight,tabular,lining]{montserrat}', 'Montserrat Extra Light')  # TODO fails
        # self.add_font([], '[defaultfam,light,tabular,lining]{montserrat}', 'Montserrat Light')  # TODO fails
        # self.add_font(['Montserrat'], '[defaultfam,tabular,lining]{montserrat}', 'Montserrat Regular')  # TODO fails
        # self.add_font([], '[defaultfam,thin,tabular,lining]{montserrat}', 'Montserrat Thin')  # TODO fails
        # self.add_font(['Nimbus Sans'], 'nimbussans', 'Nimbus 15 Sans')  # TODO fails
        self.add_font([], '[default,osfigures,scale=0.95]{opensans}', 'Open Sans')
        self.add_font([], '[sfdefault]{overlock}', 'Overlock')
        # self.add_font(['Pandora Sans'], 'pandora', 'Pandora Sans Serif')  # TODO fails
        # self.add_font([], 'paratype', 'Paratype Sans')  # TODO fails
        # self.add_font([], 'PTSansCaption', 'Paratype Sans Caption')  # TODO fails
        # self.add_font([], 'PTSansNarrow', 'Paratype Sans Narrow')  # TODO fails
        self.add_font([], '[sfdefault]{quattrocento}', 'Quattrocento Sans')
        self.add_font([], '[default]{raleway}', 'Raleway')
        self.add_font([], '[sfdefault]{roboto}', 'Roboto')
        self.add_font([], '[sfdefault,condensed]{roboto}', 'Roboto Condensed')
        self.add_font([], '[sfdefault,light]{roboto}', 'Roboto Light')
        # self.add_font([], '[sfdefault,light,condensed]{roboto}', 'Roboto Light Condensed')  # TODO fails
        # self.add_font([], '[sfdefault,thin]{roboto}', 'Roboto Thin')  # TODO fails
        # self.add_font([], '[familydefault]{Rosario}', 'Rosario')  # TODO fails
        self.add_font([], '[default]{sourcesanspro}', 'Source Sans Pro')
        self.add_font(['Adventor', 'Gyre Adventor', 'URW Gothic'], 'tgadventor', 'TeX Gyre Adventor')
        self.add_font(['Gyre Heros', 'Heros', 'URW Nimbus Sans'], 'tgheros', 'TeX Gyre Heros')
        # self.add_font(['Universalis Condensed'], '[condensed,sfdefault]{universalis}', 'Universalis ADF Condensed')  # TODO fails
        # self.add_font(['Universalis', 'Universalis Standard'], '[sfdefault]{universalis}', 'Universalis ADF Standard')  # TODO fails
        # self.add_font([], '[sfdefault]{classico}', 'URW Classico')  # TODO fails
        # self.add_font(['Venturis Sans'], '[lf]{venturis}', 'Venturis ADF Sans')  # TODO fails

        # typewriter

        self.add_font([], 'DejaVuSansMono', 'Deja Vu Sans Mono')
        # self.add_font(['droidsansmono'], '[defaultmono]{droidmono}', 'Droid Mono')  # TODO fails
        self.add_font([], 'FiraMono', 'FiraMono')
        # self.add_font(['plexmonoextralight'], 'plex-otf', 'IBM Plex Mono Extra Light')  # TODO fails
        # self.add_font(['plexmonolight'], 'plex-otf', 'IBM Plex Mono Light')  # TODO fails
        # self.add_font(['plexmonomedium'], 'plex-otf', 'IBM Plex Mono Medium')  # TODO fails
        # self.add_font(['plexmono', 'plexmonotext'], 'plex-otf', 'IBM Plex Mono Text')  # TODO fails
        # self.add_font(['plexmonothin'], 'plex-otf', 'IBM Plex Mono Thin')  # TODO fails
        # self.add_font([], 'inconsolata', 'Inconsolata')  # TODO fails
        self.add_font(['lmodernmono'], 'lmodern', 'Latin Modern Mono')
        self.add_font(['lmodernmonolight'], 'lmodern', 'Latin Modern Mono Light')
        # self.add_font(['lmodernmonolightcondensed'], 'lmodern', 'Latin Modern Mono Light Condensed')  # TODO fails
        # http://www.tug.dk/FontCatalogue/latinmodernmonoproportional/
        # self.add_font([], 'libertinus', 'Libertinus Mono')  # TODO fails
        # self.add_font(['nimbusmono'], 'nimbusmono', 'Nimbus 15 Mono')  # TODO fails
        # self.add_font(['nimbusmononarrow'], 'nimbusmononarrow', 'Nimbus 15 Mono Narrow')  # TODO fails
        # self.add_font(['ocr', 'ocr-b', 'Optical Character Recognition Font B', 'Optical Character Recognition Font'],
        #              'ocr', 'OCR-B Optical Character Recognition Font B')  # TODO fails
        self.add_font([], '[default]{sourcecodepro}', 'Source Code Pro')
        self.add_font(['courier', 'tgcursor'], 'tgcursor', 'TeX Gyre Cursor')

        # Calligraphical and Handwritten
        self.add_font([], 'LobsterTwo', 'Lobster Two')
        self.add_font([], 'miama', 'Miama Nueva')
        self.add_font([], 'tgchorus', 'TeX Gyre Chorus')

        # Blackletter
        # self.add_font([], None, 'Missaali-Regular.otf')  # TODO fails

        # Special
        self.add_font([], None, 'Punk Nova')
        # self.add_font([], 'beuron', 'Beuron')  # TODO fails
        self.add_font([], 'cinzel', 'Cinzel')
        # self.add_font([], 'yfonts', 'Baroque Initials')  # TODO fails

    def add_font(self, aliases, latex_package, latex_font, latex_bold_font=None):
        font = Font(latex_package, latex_font, latex_bold_font)
        aliases.append(latex_font)
        for name in aliases:
            self.fonts[name.lower().replace(" ", "")] = font

    def get_latex_font_setup(self, font_name):
        # lookup font by name, if not found use gentium as default
        font = self.fonts.get(font_name.lower().replace(" ", ""), None)
        if not font:
            log.info("Font '" + font_name + "' not found. Using: " + 'gentium')
            font = self.fonts.get('gentium')
        return font.latex_font_setup


class Font(object):
    def __init__(self, latex_package, latex_font, latex_bold_font=None):
        if latex_bold_font:
            latex_bold_font = latex_bold_font
        else:
            latex_bold_font = latex_font

        package_string = '\\usepackage{$font_package}\n'
        if not latex_package:
            # special case: non package
            package_string = '$font_package'
            latex_package = ''
        elif '[' in latex_package:
            # special case: we need the package options so expect the string like e.g. [defaultmono]{droidmono}
            package_string = '\\usepackage$font_package'
        font_string = '\\setmainfont{$font}\n'
        bold_string = '\\newfontfamily\\boldfont{$bold_font}'
        template_string = package_string + font_string + bold_string
        self.latex_font_setup = string.Template(template_string).substitute(font_package=latex_package,
                                                                            font=latex_font,
                                                                            bold_font=latex_bold_font)
