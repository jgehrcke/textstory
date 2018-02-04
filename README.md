Ein Projekt zur Konversion eines Dokuments, geschrieben in einem simplen Markup-Format, zu HTML- und LaTeX-Dokumenten  &ndash; optimiert für Lesbarkeit, mit besten typographischen Absichten.

Document conversion from a simple markup format to HTML and LaTeX documents &ndash; optimised for readability with best typographical intentions.

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
* [Markdown](https://daringfireball.net/projects/markdown/syntax)
* [TOML](https://github.com/toml-lang/toml)

# Dokumentation

English version [below](#markdown-header-english-documentation)

## Anforderungen / Installation
Natürlich muss [Python](https://www.python.org/) installiert sein.

`filt0r.py` hat zudem folgende Voraussetzungen

* [Python TOML](https://pypi.python.org/pypi/toml)

Vor der ersten Ausführung sind diese zu installieren:  
`pip install -r requirements.txt`

## Konversion der Dokumentenquelle zu HTML & LaTeX
Die Konversion zu HTML & LaTeX wird mit `filt0r.py` durchgeführt. `filt0r.py` wurde mit Python 2.7 und 3.4 getestet. Erwartet wird ein Argument: der Pfad zur Dokumentenquelle. Beispiel:
```
$ python filt0r.py doc.txt
[...]
15:13:17:977.0  INFO: Wrote UTF-8-encoded LaTeX source file: latex/latex-body.tex.
[...]
15:13:17:987.0  INFO: Wrote UTF-8-encoded HTML document: html/index.html.
```

Optionales Argument: der Pfad zur Setupdatei (s.u.), falls abweichend von `setup.toml`. Beispiel:  
`python filt0r.py doc.txt toml.toml`

`filt0r.py` sollte im Stammverzeichnis dieses Projekts ausgeführt werden. Es schreibt die Dateien `latex/latex-document.tex`, `latex/latex-body.tex` und `html/index.html` relativ zum current working directory.

## Setup

In einer Setupdatei in TOML-Notation (default: `setup.toml`) werden allgemeine Einstellungen und Angaben zum zu generierenden Dokument gemacht. Dies sind Angaben wie Titel, Autor und verschiedene PDF- und HTML-Metadaten. Die meisten dieser Angaben sind zwingend erforderlich. Nicht erforderliche Angaben sind durch Kommentare als solche markiert.

### Folgende Angaben sind zwingend erforderlich:

#### Allgemein:
```
[general]
title = "Titel des Textes"
author = "Autor des Textes"
language = "Sprachkürzel" #de, en, ... (https://wiki.selfhtml.org/wiki/Sprachk%C3%BCrzel)
```

#### LaTeX:
```
[latex]
pdfsubject = "Kurzbeschreibung für PDF Metadaten"
pdfkeywords = "Eine Reihe Schlüsselwörter für PDF Metadaten getrennt durch Kommata"
```

#### HTML:
```
[html]
locale = "Regionalangabe" #de_DE, en_GB, ... #meta property og:locale
metadescription = "Kurzbeschreibung für HTML Metadaten" #meta description und meta property og:description
url = "URL des Textes" #meta property og:url
sitename = "Name der Seite, auf der der Text zu finden ist" #meta property og:site_name
```

### Optionale Angaben:

#### Allgemein:
```
[general]
subtitle = "Untertitel des Textes"
```
#### Latex Layout:
```
[latex]
pageFormat = "Seitenformat" #a0 - a6, b0 - b6 #default: a5 #Falls angegeben, werden pageWidth und pageHeight ignoriert
pageWidth = "Seitenbreite" #z.B. "210mm", "21.5cm"
pageHeight = "Seitenhöhe" #z.B. "210mm", "21.5cm"
bindingOffset = "Bundzugabe"
fontSize = "Schriftgröße in pt" #z.B. 12.5 #default: 11
```

#### LaTeX Titel
```
title = "Titel des Textes" #default: general.title
subtitle = "Untertitel des Textes" #default: general.title
printAuthorOnTitle = "Im Anfangstitel wird Autor mit angegeben" #nicht relevant, wenn bookPrint = "true" #default: false
halfTitle = "Schmutztitel" #Textkommando \\storyhalftitle #default: latex.title
isbn = "ISBN dieses Buches" #Textkommando \\isbn
```

#### LaTeX Buchdruck
```
bookPrint = "Textlayout für Buchdruck" #true, false #default: false
    #true: 
        #document type = "scrbook"
        #Seiten aus latex/bookPreliminaries werden dem Text in alphanumerischer Reihenfolge vorangestellt
        #Seiten aus latex/bookAppendix werden dem Text in alphanumerischer Reihenfolge angehängt
    #false:
        #document type = "scrreprt"
        #zu Textbeginn werden Titel und Untertitel gezeigt
```    

#### LaTeX Kopfzeile
```
headerLeft = "Kopfzeile links" #Es können Textkommandos verwendet werden (s.u.) #default: "\\storytitle"
headerRight = "Kopfzeile rechts" #Es können Textkommandos verwendet werden (s.u.) #default: "\\storychapter"
```

#### LaTeX Inhaltsverzeichnis
```
tableOfContents = "Inhaltsverzeichnis wird angezeigt" #true, false #default: false
contentsTitle = "Titel des Inhaltsverzeichnis"
tableOfContentsPagebreak = "Seitenumbruch nach Inhaltsverzeichnis" #true, false #default: false
```

#### LaTeX Kapitel
```
chapterPagebreak = "Neue Seite bei Kapitelanfang" #true, false #default: false
hideChapterHeader = "Keine Kopfzeile bei Kapitelanfang" #true, false #default: self.chapterPagebreak
```

#### LaTeX PDF-Einstellungen
```
hascolorlinks = "Farbige Links" #default: false
urlcolor = "URL-Farbe" #default: blue
linkcolor = "Linkfarbe" #default: black
```

#### HTML:
```
[html]
title = "Titel des Textes" #falls abweichend von general.title
subtitle = "Untertitel des Textes" #falls abweichend von general.subtitle
headertitle = "Text für den HTML Titel" #default: "title | author"
previewimage = "Link für Vorschaubild (Metadaten)" #meta property og:image
```

### Beispiel einer Setupdatei:
```
[general]
title = "Kommt und holt sie"
#subtitle = ""
author = "Josa Wode"
language = "de" #de, en, ...

[latex]
bookPrint = "true" #true, false #Dokument wird für den Druck als Buch erstellt, es können Seiten zu Titelei und Anhang hinzugefügt werden (Verzeichnisse: latex/bookPreliminaries und latex/bookAppendix)
pageFormat = "a5" # a0 - a6, b0 - b6 # define page size
#pageWidth = "210" # in mm # only when not using pageFormat
#pageHeight = "297" # in mm # only when not using pageFormat
bindingOffset = "15mm" #Seitenanteil der in der Bindung verschwindet
fontSize = "11" # e.g. 11 12.5 # in pt
printAuthorOnTitle = "false" #true, false #Legt fest, ob die Titelseite mit dem Namen des Autors bzw. der Autorin beginnt
#title = "" #Auskommentieren, falls identisch mit 'general.title'
subtitle = "Eine Geschichte von Josa Wode" #Auskommentieren, falls identisch mit 'general.subtitle'
pdfsubject = "Geschichte"
pdfkeywords = "geschichte, alte, josa, wode"
hascolorlinks = "true"
urlcolor = "blue"
linkcolor = "black"
    
[html]
#title = "" #Auskommentieren, falls identisch mit 'general.title'
#subtitle = "" #Auskommentieren, falls identisch mit 'general.subtitle'
headertitle = "Kommt und holt sie | eine Geschichte von Josa Wode"
url = "http://writing.fotoelectrics.de/documents/come-get-her/de/html/" #meta property og:url
metadescription = "Eine kurze Geschichte von Josa Wode - Es könnte ein Märchen sein, wenn es sich benehmen würde. (Lizenz: Creative Commons BY-NC-SA 3.0)"    #meta description und meta property og:description
locale = "de_DE" #de_DE, en_GB, ... #meta property og:locale
sitename = "writing.fotoelectrics" #meta property og:site_name
#previewimage = "" #meta property og:image #Auskommentieren, falls kein image tag erwünscht ist
```

## LaTeX Textkommandos

Für die Verwendung in (zusätzlichen) LaTeX-Dokumenten (s.u.) und bestimmten Setup-Einträgen (s.o.) stehen folgende Befehle (über den gewöhnlichen LaTeX-Befehlsumfang hinaus) zur Verfügung:

* `\storytitle`     gibt den Titel aus
* `\storysubtitle`  gibt den Untertitel aus
* `\storyhalftitle` gibt den Schmutztitel aus
* `\storyauthor`    gibt den Autor aus
* `\storychapter`   gibt das aktuelle Kapitel aus
* `\isbn`           gibt die ISBN aus
* `\printtitle`     gibt formatiert Titel, ggf. Untertitel und bei Setup-Option `printAuthorOnTitle` zusätzlich den Autor aus

Für die Verwendung in der Setup-TOML ist `\` als Escape-Charakter voranzustellen (e.g. `\\storytitle`).

## LaTeX Templates, Lizenz, Titelei und Anhang

tbd

## LaTeX build
Im `latex`-Verzeichnis dieses Projekts muss `latex-document.tex` per `lualatex` kompiliert werden (für das Erstellen des Inhaltsverzeichnisses ist dies zweimal durchzuführen). `build.bat` dient als Helferlein für Windows:
```
$ build.bat
[...]
Output written on latex-document.pdf (35 pages, 115586 bytes).
Transcript written on latex-document.log.
```

Der Kompiliervorgang wurde mit TeX Live 2015's `lualatex` getestet.

## HTML Templates und Lizenz

tbd

## Dateiformat der Dokumentenquelle
Erwartet wird eine Text-Datei in UTF-8-Kodierung.


## Markupformat der Dokumentenquelle


### Absatztrennung
Markup: Zeilenumbruch

Beispiel: 
`Dies ist der erste Absatz.
Hier beginnt der zweite Absatz.`


### Sektionstrennung
Markup: Doppelter Zeilenumbruch bzw. Leerzeile

Beispiel:
`Hier steht der Text des ersten Abschnitts.

Hier beginnt eine neue Sektion.`


### Überschriften
Markup: Doppelraute am Zeilenanfang

Beispiel: `## Kapitel 1`

Eine derart markierte Zeile wird als Überschrift (und Kapitelanfang) interpretiert.


### Anführungszeichen
Markup: Einfache Double-Quote-Paare.

Beispiel: `Er sagte: "Oh, Kacke!"`

In der Ausgabe werden französische Anführungszeichen gesetzt.

Refs:

* <https://de.wikipedia.org/wiki/Guillemets>


### Bindestriche
Markup: Einfaches Minus.

Beispiel: `Damen- und Herrentoilette`

Wird unverändert in den HTML- und LaTeX-Code übertragen.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### Gedankenstriche (en-dash)
Markup: Doppelminus.

Beispiel: `Glitzer, Filz, Garn und Knöpfe -- seine Küche sah aus als wäre ein Clown in ihr explodiert.`

HTML: wird übersetzt zu en-dash (`&ndash;`).
LaTeX: wird übersetzt zu `--`.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### Gedankenstriche (em-dash)
Markup: Dreifaches Minus.

Beispiel: `Glitter, felt, yarn, and buttons---his kitchen looked as if a clown had exploded.`

HTML: wird übersetzt zu em-dash (`&mdash;`).
LaTeX: wird übersetzt zu `---`.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### Kursiv
Markup: Mit Unterstrichen (_) oder Asterisken (*) umgeben.

Beispiel: `Hier ist _etwas_ kursiv geschrieben. Hier *noch etwas*.`

Der markierte Textabschnitt wird kursiv dargestellt.

Refs:

* <https://en.wikipedia.org/wiki/Italic_type>


### Fett
Markup: Mit doppelten Unterstrichen (__) oder doppelten Asterisken (**) umgeben.

Beispiel: `Hier ist __etwas__ fett gedruckt. Hier **noch etwas**.`

Der markierte Textabschnitt wird fett dargestellt.

Refs:

* <https://en.wikipedia.org/wiki/Emphasis_(typography)>


### Auslassungspunkte
Markup: Drei normale Punkte.

Beispiel: `Das ist... ähm... doof.`

HTML: wird übersetzt zu `&hellip;`.
LaTeX: wird übersetzt zu `\dots`.

Refs:

* <https://en.wikipedia.org/wiki/Ellipsis>


### Fußnoten
Markup: Eckige Klammern.

Beispiel: `Das ist das WortNachDemDieFußNoteKommt[Die Fußnote].`


### Bilder
Markup: \!\[altText\]\(Bildpfad "optionaler Titel"\)

Auf diese Weise können Bilder integriert werden, die am angegebenen Pfad liegen. Der optionale Titel wird zu einer Bildunterschrift. Der altText dient im HTML als Alternative, falls das Bild nicht dargestellt wird, und für Screen Reader. Im LaTeX wird diese Angabe ignoriert.

Beispiel: `![Alternativtext](/path/to/img.jpg "optional title")`

### Maskierung von Sonderzeichen
Markup: Backslash gefolgt vom Sonderzeichen ('`\Sonderzeichen`')

In HTML, LaTeX und dem hier verwendeten Markup sind bestimmte Symbole als Teil der Syntax reserviert. Sie müssen maskiert werden, um als das bloße Symbol interpretiert zu werden und als solches im generierten Text aufzutauchen.

Folgende Zeichen sind zu maskieren ('`\`' voranstellen):  
`\`   Backslash &ndash; das Maskierungszeichen selbst  
`*`   Asterisk  
`_`   Unterstrich  
`{}`  Geschweifte Klammern  
`[]`  Eckige Klammern  
`#`   Raute  
`"`   Anführungszeichen / Double-Quote  
`!`   Ausrufezeichen (nur nötig, wenn '[' folgt)  
`--`  Doppel-Minus  
`$`   Dollar  

Folgende Zeichen können normal verwendet werden und werden automatisch in HTML- bzw. LaTeX-Schreibweise übertragen:  
`&`   wird in HTML zu '`&amp;`', in LaTeX zu '`\&`'  
`<`   wird in HTML zu `&lt;`  
`>`   wird in HTML zu `&gt;`  
`%`   wird in LaTeX zu `\%`  
`~`   wird in LaTeX zu `\textasciitilde`  
`^`   wird in LaTeX zu `\textasciicircum`  

Beispiel: `Spitze <voll spitze> und eckige Klammern \[weil es so schön ist\].`

Refs:

* <https://www.w3.org/International/questions/qa-escapes#use>
* <https://www.namsu.de/Extra/strukturen/Sonderzeichen.html>

# English Documentation

tbd
