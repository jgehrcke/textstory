# -*- coding: utf-8 -*-
# Copyright (c) 2015-2019 Jan-Philip Gehrcke. See LICENSE file for details.
from __future__ import unicode_literals

# from nose.tools import nottest
import unittest
from test_base import TestBase, test_data_folder_path

import os
from subprocess import Popen, PIPE

import filt0r
from fonts import FontManager
from logger import log
from textstory_setup import Setup


@unittest.skip("disabled slow tests, also some will fail (correlating fonts are disabled)")
class TestFonts(TestBase):

    def check_pdf_generation_output(self, stdout):
        line = stdout.readline()
        if line != b'':
            line_string = line.decode("utf-8").strip().lower()
            self.assertFalse('error' in line_string, "Pdf generation error: " + line_string)
            self.check_pdf_generation_output(stdout)

    def font_check(self, font_name):
        # Set test paths  # TODO move to setup classmethod
        test_folder_path = os.path.join(test_data_folder_path, "font_tests")
        self.set_paths(test_folder_path)

        # Load setup and exchange font for test font
        setup = Setup(self.setup_file_path, self.input_file_path, self.output_folder_path)
        log.info("Font test: changing font to " + font_name)
        setup.latex.font = FontManager().get_latex_font_setup(font_name)

        # Make sure, font is used (and not default)
        self.assertTrue(font_name.lower().replace(" ", "") in setup.latex.font.lower().replace(" ", ""),
                        "Font " + font_name + " should be used, but is " + setup.latex.font)

        # Execute LaTeX and Html creation
        filt0r.run_with_setup(setup)

        # generate pdf
        process = Popen(['lualatex', '--interaction=nonstopmode', '--output-format=pdf', "latex-document.tex"],
                        cwd=self.output_latex_folder_path, stdout=PIPE, stderr=PIPE)
        self.check_pdf_generation_output(process.stdout)

    # default fonts

    def test_gentium(self):
        self.font_check('gentium')

    def test_courier(self):  # TODO
        self.font_check('tgcursor')

    def test_cabin(self):
        self.font_check('cabin')

    # serif fonts

    def test_accanthis(self):  # fail
        self.font_check('Accanthis')

    def test_alegreya(self):
        self.font_check('Alegreya')

    def test_algol(self):  # fail
        self.font_check('Algol')

    def test_antykwa_poltawskiego(self):  # fail
        self.font_check('Antykwa Półtawskiego')

    def test_antykwa_poltawskiego_light(self):  # fail
        self.font_check('Antykwa Półtawskiego Light')

    def test_antykwa_torunska(self):  # fail
        self.font_check('Antykwa Toruńska')

    def test_antykwa_torunska_cond(self):  # fail
        self.font_check('Antykwa Toruńska Condensed')

    def test_antykwa_torunska_l(self):  # fail
        self.font_check('Antykwa Toruńska Light')

    def test_antykwa_torunska_l_c(self):  # fail
        self.font_check('Antykwa Toruńska Light Condensed')

    def test_berenis(self):  # fail
        self.font_check('berenis')

    def test_caladea(self):
        self.font_check('caladea')

    def test_cochineal(self):
        self.font_check('cochineal')

    def test_coelacanth_extra_light(self):  # fail
        self.font_check('Coelacanth Extra Light')

    def test_coelacanth_light(self):  # fail
        self.font_check('Coelacanth Light')

    def test_coelacanth(self):  # fail
        self.font_check('coelacanth')

    def test_cormorant_garamond(self):  # fail
        self.font_check('Cormorant Garamond')

    def test_cormorant_garamond_l(self):  # fail
        self.font_check('Cormorant Garamond Light')

    def test_crimson_pro_extra_light(self):  # fail
        self.font_check('Crimson Pro Extra Light')

    def test_crimson_pro_light(self):  # fail
        self.font_check('Crimson Pro Light')

    def test_crimson_pro_m(self):  # fail
        self.font_check('Crimson Pro Medium')

    def test_crimson_pro(self):  # fail
        self.font_check('Crimson Pro Regular')

    def test_crimson(self):  # fail
        self.font_check('crimson')

    def test_dejavu_serif(self):
        self.font_check('DejaVu Serif')

    def test_dejavu_serif_c(self):
        self.font_check('DejaVu Serif Condensed')

    def test_drm(self):  # fail
        self.font_check('drm')

    def test_droidserif(self):
        self.font_check('droidserif')

    def test_fbb(self):
        self.font_check('fbb')

    def test_gandhi(self):  # fail
        self.font_check('gandhi')

    def test_garamond_expert(self):  # fail
        self.font_check('Garamond Expert')

    def test_artemisia(self):
        self.font_check('Artemisia')

    def test_gfsbodoni(self):
        self.font_check('gfsbodoni')

    def test_free_serif(self):
        self.font_check('FreeSerif')

    def test_heuristica(self):
        self.font_check('heuristica')

    def test_plex_serif_extra_light(self):  # fail
        self.font_check('Plex Serif Extra Light')

    def test_plex_serif_m(self):  # fail
        self.font_check('Plex Serif Medium')

    def test_plex_serif(self):  # fail
        self.font_check('Plex Serif')

    def test_plex_serif_text(self):  # fail
        self.font_check('Plex Serif Text')

    def test_plex_serif_thin(self):  # fail
        self.font_check('Plex Serif Thin')

    def test_im_fell_english(self):
        self.font_check('imfellEnglish')

    def test_junicode(self):
        self.font_check('Junicode')

    def test_latin_modern_roman(self):
        self.font_check('Latin Modern Roman')

    def test_libertinus(self):  # fail
        self.font_check('libertinus')

    def test_baskerville(self):
        self.font_check('baskerville')

    def test_libre_bodoni(self):
        self.font_check('Libre Bodoni')

    def test_librecaslon(self):  # fail
        self.font_check('librecaslon')

    def test_libertine(self):  # fail
        self.font_check('libertine')

    def test_merriweather(self):
        self.font_check('merriweather')

    def test_merriweather_l(self):
        self.font_check('Merriweather Light')

    def test_nimbus_serif(self):  # fail
        self.font_check('nimbusserif')

    def test_old_standard(self):
        self.font_check('Old Standard')

    def test_paratype(self):  # fail
        self.font_check('paratype')

    def test_paratype_c(self):  # fail
        self.font_check('Paratype Caption')

    def test_playfair_display(self):
        self.font_check('PlayfairDisplay')

    def test_quattrocento(self):
        self.font_check('quattrocento')

    def test_roboto_slab(self):
        self.font_check('Roboto Slab')

    def test_roboto_slab_l(self):
        self.font_check('Roboto Slab Light')

    def test_roboto_slab_t(self):  # fail
        self.font_check('Roboto Slab Thin')

    def test_shobhika(self):  # fail
        self.font_check('Shobhika')

    def test_source_serif_pro_extra_light(self):
        self.font_check('Source Serif Pro Extra Light')

    def test_test_source_serif_pro_light(self):
        self.font_check('Source Serif Pro Light')

    def test_sourceserifpro(self):
        self.font_check('sourceserifpro')

    def test_stix(self):  # fail
        self.font_check('stix')

    def test_bonum(self):
        self.font_check('Bonum')

    def test_pagella(self):
        self.font_check('Pagella')

    def test_schola(self):
        self.font_check('Schola')

    def test_termes(self):
        self.font_check('Termes')

    def test_venturis(self):  # fail
        self.font_check('venturis')

    def test_venturis2(self):  # fail
        self.font_check('venturis2')

    def test_venturisold(self):  # fail
        self.font_check('venturisold')

    def test_xcharter(self):
        self.font_check('XCharter')

    def test_xits(self):
        self.font_check('XITS')

    # sans serif

    def test_alegreya_sans(self):  # fail
        self.font_check('AlegreyaSans')

    def test_arimo(self):  # fail
        self.font_check('arimo')

    def test_biolinum(self):  # fail
        self.font_check('biolinum')

    def test_cabin_condensed(self):
        self.font_check('Cabin Condensed')

    def test_carlito(self):
        self.font_check('carlito')

    def test_chivo_light(self):  # fail
        self.font_check('Chivo Light')

    def test_chivo(self):  # fail
        self.font_check('Chivo')

    def test_clear_sans(self):
        self.font_check('ClearSans')

    def test_cyklop(self):
        self.font_check('cyklop')

    def test_dejavu_sans(self):
        self.font_check('DejaVuSans')

    def test_dejavu_sans_c(self):
        self.font_check('DejaVu Sans Condensed')

    def test_droid_sans(self):
        self.font_check('droidsans')

    def test_fetamont(self):  # fail
        self.font_check('fetamont')

    def test_fira_sans_book(self):
        self.font_check('Fira Sans Book')

    def test_fira_sans_extra_light(self):
        self.font_check('Fira Sans Extra Light')

    def test_fira_sans_light(self):
        self.font_check('Fira Sans Light')

    def test_fira_sans(self):
        self.font_check('Fira Sans')

    def test_fira_sans_thin(self):
        self.font_check('Fira Sans Thin')

    def test_fira_sans_ultra_light(self):
        self.font_check('Fira Sans Ultra Light')

    def test_gandhi_sans(self):  # fail
        self.font_check('Gandhi Sans')

    def test_gfs_neohellenic(self):
        self.font_check('GFS Neohellenic')

    def test_gillius(self):  # fail
        self.font_check('gillius')

    def test_free_sans(self):
        self.font_check('FreeSans')

    def test_inria_sans_light(self):  # fail
        self.font_check('Inria Sans Light')

    def test_inria_sans(self):  # fail
        self.font_check('Inria Sans')

    def test_iwona(self):
        self.font_check('Iwona')

    def test_iwona_condensed(self):  # fail
        self.font_check('Iwona Condensed')

    def test_iwona_light(self):
        self.font_check('Iwona Light')

    def test_iwona_light_condensed(self):  # fail
        self.font_check('Iwona Light Condensed')

    def test_kurier(self):
        self.font_check('kurier')

    def test_kurier_condensed(self):  # fail
        self.font_check('Kurier Condensed')

    def test_kurier_light(self):
        self.font_check('Kurier Light')

    def test_kurier_light_condensed(self):  # fail
        self.font_check('Kurier Light Condensed')

    def test_latin_modern_sans(self):
        self.font_check('Latin Modern Sans')

    def test_latin_modern_sans_extended(self):  # fail
        self.font_check('Latin Modern Sans Extended')

    def test_lato(self):
        self.font_check('lato')

    def test_libertinus_sans(self):  # fail
        self.font_check('Libertinus Sans')

    def test_merriweather_sans(self):
        self.font_check('Merriweather Sans')

    def test_merriweather_sans_light(self):
        self.font_check('Merriweather Sans Light')

    def test_mintspirit(self):
        self.font_check('mintspirit')

    def test_montserrat_alternates_extra_light(self):  # fail
        self.font_check('Montserrat Alternates Extra Light')

    def test_montserrat_alternates_light(self):  # fail
        self.font_check('Montserrat Alternates Light')

    def test_montserrat_alternates(self):  # fail
        self.font_check('Montserrat Alternates')

    def test_montserrat_extra_light(self):  # fail
        self.font_check('Montserrat Extra Light')

    def test_montserrat_light(self):  # fail
        self.font_check('Montserrat Light')

    def test_montserrat(self):  # fail
        self.font_check('Montserrat')

    def test_montserrat_thin(self):  # fail
        self.font_check('Montserrat Thin')

    def test_nimbus_sans(self):  # fail
        self.font_check('Nimbus Sans')

    def test_open_sans(self):
        self.font_check('opensans')

    def test_overlock(self):
        self.font_check('overlock')

    def test_pandora_sans(self):  # fail
        self.font_check('Pandora Sans')

    def test_paratype_sans(self):  # fail
        self.font_check('Paratype Sans')

    def test_paratype_sans_caption(self):  # fail
        self.font_check('Paratype Sans Caption')

    def test_paratype_sans_narrow(self):  # fail
        self.font_check('Paratype Sans Narrow')

    def test_quattrocento_sans(self):
        self.font_check('Quattrocento Sans')

    def test_raleway(self):
        self.font_check('raleway')

    def test_roboto(self):
        self.font_check('roboto')

    def test_roboto_condensed(self):
        self.font_check('Roboto Condensed')

    def test_roboto_light(self):
        self.font_check('Roboto Light')

    def test_roboto_light_condensed(self):  # fail
        self.font_check('Roboto Light Condensed')

    def test_roboto_thin(self):  # fail
        self.font_check('Roboto Thin')

    def test_rosario(self):  # fail
        self.font_check('Rosario')

    def test_source_sans_pro(self):
        self.font_check('sourcesanspro')

    def test_adventor(self):
        self.font_check('Adventor')

    def test_heros(self):
        self.font_check('Heros')

    def test_universalis_condensed(self):  # fail
        self.font_check('Universalis Condensed')

    def test_universalis(self):  # fail
        self.font_check('Universalis')

    def test_urw_classico(self):  # fail
        self.font_check('URW Classico')

    def test_venturis_sans(self):  # fail
        self.font_check('Venturis Sans')

    # typewriter

    def test_dejavu_sans_mono(self):
        self.font_check('DejaVuSansMono')

    def test_droid_sans_mono(self):  # fail
        self.font_check('droidsansmono')

    def test_fira_mono(self):
        self.font_check('FiraMono')

    def test_plex_mono_extra_light(self):  # fail
        self.font_check('plexmonoextralight')

    def test_plex_mono_light(self):  # fail
        self.font_check('plexmonolight')

    def test_plex_mono_medium(self):  # fail
        self.font_check('plexmonomedium')

    def test_plex_mono(self):  # fail
        self.font_check('plexmono')

    def test_plex_mono_thin(self):  # fail
        self.font_check('plexmonothin')

    def test_inconsolata(self):  # fail
        self.font_check('inconsolata')

    def test_latin_modern_mono(self):
        self.font_check('Latin Modern Mono')

    def test_latin_modern_mono_l(self):
        self.font_check('Latin Modern Mono Light')

    def test_latin_modern_mono_c(self):  # fail
        self.font_check('Latin Modern Mono Light Condensed')

    def test_libertinus_mono(self):  # fail
        self.font_check('Libertinus Mono')

    def test_nimbus_mono(self):  # fail
        self.font_check('nimbusmono')

    def test_nimbus_mono_narrow(self):  # fail
        self.font_check('nimbusmononarrow')

    def test_ocr(self):  # fail
        self.font_check('ocr')

    def test_source_code_pro(self):
        self.font_check('sourcecodepro')

    # Calligraphical and Handwritten

    def test_lobster_two(self):
        self.font_check('Lobster Two')

    def test_miama_nueva(self):
        self.font_check('Miama Nueva')

    def test_chorus(self):
        self.font_check('TeX Gyre Chorus')

    # Blackletter

    def test_missaali(self):  # fail
        self.font_check('Missaali-Regular')
    # Special

    def test_punk_nova(self):
        self.font_check('Punk Nova')

    def test_beuron(self):  # fail
        self.font_check('beuron')

    def test_cinzel(self):
        self.font_check('cinzel')

    def test_baroque_initials(self):  # fail
        self.font_check('Baroque Initials')
