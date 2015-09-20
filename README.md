Ein Projekt zur Konversion eines Dokuments, geschrieben in einem simplen Markup-Format, zu HTML- und LaTeX-Dokumenten  -- optimiert für Lesbarkeit, mit besten typographischen Absichten.

Credits:

* [Python](https://www.python.org/)
* [TeX Live](https://www.tug.org/texlive/)
* [LaTeX / LuaTeX](http://www.luatex.org/)
* [KOMA-Script](https://www.ctan.org/pkg/koma-script?lang=en)
* [Microtype](https://www.ctan.org/pkg/microtype?lang=en)
* [Libertine](https://en.wikipedia.org/wiki/Linux_Libertine)
* [csquotes](https://www.ctan.org/pkg/csquotes?lang=en)
* [Tufte CSS](https://github.com/daveliepmann/tufte-css)
* [normalize.css](https://github.com/necolas/normalize.css)
* [HTML5 Boilerplate](https://html5boilerplate.com/)
* [Bembo](https://de.wikipedia.org/wiki/Bembo)


# Dokumentation
## 1) Konversion der Dokumentenquelle zu HTML & LaTeX
Die Konversion zu HTML & LaTeX wird mit `filt0r.py` durchgeführt. `filt0r.py` wurde mit Python 2.7 und 3.4 getestet. Erwartet wird ein Argument: der Pfad zur Dokumentenquelle. Beispiel:
```
$ python filt0r.py doc.txt
[...]
15:13:17:977.0  INFO: Wrote UTF-8-encoded LaTeX source file: latex/latex-body.tex.
[...]
15:13:17:987.0  INFO: Wrote UTF-8-encoded HTML document: html/index.html.
```

`filt0r.py` sollte im Stammverzeichnis dieses Projekts ausgeführt werden. Es schreibt die Dateien `latex/latex-body.tex` und `html/index.html` relativ zum current working directory.



## 2) LaTeX build
Im `latex`-Verzeichnis dieses Projekts muss `latex-document.tex` per `lualatex` kompiliert werden. `build.bat` dient als Helferlein für Windows:
```
$ build.bat
[...]
Output written on latex-document.pdf (35 pages, 115586 bytes).
Transcript written on latex-document.log.
```

Der Kompiliervorgang wurde mit TeX Live 2014's `lualatex` getestet.


## 3) Dateiformat der Dokumentenquelle
Erwartet wird eine Text-Datei in UTF-8-Kodierung mit einfachen Linefeed-Zeichen (UNIX-Format).


## 4) Markupformat der Dokumentenquelle
### Absatztrennung
Markup: Ein LF-Zeichen (`\n`)

### Sektionstrennung
Markup: Zwei LF-Zeichen (`\n\n`)

### Anführungszeichen
Markup: Einfache Double-Quote-Paare.

Beispiel: `Er sagte: "Oh, Kacke!"`

In der Ausgabe werden französische Anführungszeichen gesetzt.

Refs:

* https://de.wikipedia.org/wiki/Guillemets


### Bindestriche
Markup: Einfaches Minus.

Beispiel: `Damen- und Herrentoilette`

Wird unverändert in den HTML- und LaTeX-Code übertragen.

Refs:

* http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/


### Gedankenstriche
Markup: Doppelminus.

Beispiel: `erstes Wort -- zweites Wort -- drittes Wort`

HTML: wird übersetzt zu em-dash (`&mdash;`).
LaTeX: wird übersetzt zu `---`.

Refs:

* http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/


### Auslassungspunkte
Markup: Drei normale Punkte.

Beispiel: `Das ist... ähm... doof.`

HTML: wird übersetzt zu `&hellip;`.
LaTeX: wird übersetzt zu `\dots`.

Refs:

* https://en.wikipedia.org/wiki/Ellipsis


### Fußnoten
Markup: Eckige Klammern.

Beispiel: `Das ist das WortNachDemDieFußNoteKommt[Die Fußnote].`

