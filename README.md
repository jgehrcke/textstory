Ein Projekt zur Konversion eines Dokuments, geschrieben in einem simplen Markup-Format, zu HTML- und LaTeX-Dokumenten -- optimiert für Lesbarkeit, mit besten typographischen Absichten.

**Document conversion from a simple markup format to HTML and LaTeX documents -- optimised for readability with best typographical intentions.**

## Credits

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

**English version [below](#markdown-header-english-documentation)**

## Anforderungen / Installation

Natürlich muss [Python](https://www.python.org/) installiert sein.

`filt0r.py` hat zudem folgende Voraussetzungen

* [Python TOML](https://pypi.python.org/pypi/toml)

Vor der ersten Ausführung sind diese zu installieren:  
`pip install -r requirements.txt`

## Konversion der Dokumentenquelle zu HTML & LaTeX

Die Konversion zu HTML & LaTeX wird mit `filt0r.py` durchgeführt. `filt0r.py` wurde mit Python 2.7 und 3.4 getestet. Erwartet wird ein Argument: der Pfad zur Dokumentenquelle. 

Beispiel:
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

In einer Setupdatei in TOML-Notation (default: `setup.toml`) werden allgemeine Einstellungen und Angaben zum zu generierenden Dokument gemacht. Dies sind Angaben wie Titel, Autor und verschiedene PDF- und HTML-Metadaten. 

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
outputMode = "Typ des auszugebenden Dokuments" #draft, final, manuscript #default: final 
    #draft:
        # Kommentare werden angezeigt
        # Seitenformat: A4
        # Schriftart: TeX Gyre Cursor (~Courier)
        # Hinweis: Dieser Modus ist noch in Arbeit
    #final:
        # Keine Kommentare
        # Dokument entsprechend der Konfiguration
    #manuscript 
        # Keine Kommentare
        # Seitenformat: A4
        # Schriftart: TeX Gyre Cursor (~Courier)
        # Hinweis: Dieser Modus ist noch in Arbeit
```
#### LaTeX Layout:
```
[latex]
pageFormat = "Seitenformat" #a0 - a6, b0 - b6 #default: a5 #Falls angegeben, werden pageWidth und pageHeight ignoriert
pageWidth = "Seitenbreite" #z.B. "210mm", "21.5cm"
pageHeight = "Seitenhöhe" #z.B. "210mm", "21.5cm"
bindingOffset = "Bundzugabe"
font = "Name der Schrift (siehe Abschnitt zu Schriften)"
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
hascolorlinks = "Farbige Links" #default: "false"
urlcolor = "URL-Farbe" #default: "blue"
linkcolor = "Linkfarbe" #default: "black"
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
outputMode = "final"

[latex]
bookPrint = true #true, false #Dokument wird für den Druck als Buch erstellt, es können Seiten zu Titelei und Anhang hinzugefügt werden (Verzeichnisse: latex/bookPreliminaries und latex/bookAppendix)
#headerLeft = "" #Text für Kopfzeile links festlegen; verfügbare Befehle \\storytitle, \\storysubtitle, \\storyhalftitle, \\storyauthor, \\storychapter; default: \\storytitle
#headerRight = "" #Text für Kopfzeile rechts festlegen; verfügbare Befehle \\storytitle, \\storysubtitle, \\storyhalftitle, \\storyauthor, \\storychapter; default: \\storychapter
#hideChapterHeader = true #true, false #default: chapterPagebreak #keine Kopfzeile zum Kapitelanfang
chapterPagebreak = true #true, false #true: neues Kapitel beginnt auf neuer Seite
tableOfContents = true #true, false #Inhaltsverzeichnis
#tableOfContentsPagebreak = true #true, false #default: false #true: neue Seite nach Inhaltsverzeichnis
contentsTitle = "Inhalt" #Falls angegeben, wird dies als Titel des Inhaltsverzeichnisses verwendet
isbn = "978-3-7460-9728-2"
pageFormat = "a5" # a0 - a6, b0 - b6 # Seitenformat festlegen
#pageWidth = "210" # in mm # Seitenbreite, nur wenn nicht durch 'pageFormat' festgelegt
#pageHeight = "297" # in mm # Seitenhöhe, nur wenn nicht durch 'pageFormat' festgelegt
bindingOffset = "15mm" #Seitenanteil der in der Bindung verschwindet
font = "gentium"
fontSize = "11" # e.g. 11 12.5 # Schriftgröße in pt
printAuthorOnTitle = false #true, false #Legt fest, ob die Titelseite mit dem Namen des Autors bzw. der Autorin beginnt
#title = "" #Auskommentieren, falls identisch mit 'general.title'
subtitle = "Eine Geschichte von Josa Wode" #Auskommentieren, falls identisch mit 'general.subtitle'
#halfTitle = "" #Schmutztitel für Buchdruck #Auskommentieren, falls identisch mit 'title'
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

Für die Verwendung in der Setup-TOML ist `\` als Escape-Charakter voranzustellen (z.B. `\\storytitle`).

## LaTeX Schriften

Es wird eine ganze Reihe von LaTeX-Schriften unterstützt. Das heißt nicht, dass diese Schriften eine gute Wahl für 
deine Textstory sind.

Es ist sehr zu empfehlen, für Fließtext eine Schrift mit Serifen zu wählen, da diese die Lesbarkeit verbessern.
Standardmäßig ist als Textstory-Schrift Gentium ausgewählt -- sie sieht gut aus, ist typografisch hochwertig 
und im Zusammenhang mit Textstorys gründlich erprobt.

Bisher kann nur diese Hauptschrift konfiguriert werden.

Für Draft und Manuskript ist TeX Gyre Cursor, eine Art Courier, eingestellt, um dem Standard zu entsprechen.

Die Schrift für den Lizenztext ist Cabin.  

### Schriften mit Serifen

* [Alegreya](http://www.tug.dk/FontCatalogue/alegreya/)
* Artemisia: siehe GFS Artemisia
* Baskerville: siehe Libre Baskerville
* Bonum, Bookman: siehe TeX Gyre Bonum
* [Caladea](http://www.tug.dk/FontCatalogue/caladea/)
* [Cochineal](http://www.tug.dk/FontCatalogue/cochineal/)
* Computer Modern: siehe Latin Modern Roman
* [DejaVu Serif](http://www.tug.dk/FontCatalogue/dejavuserif/)
* [DejaVu Serif Condensed](http://www.tug.dk/FontCatalogue/dejavuserifcondensed/)
* [Droid Serif](http://www.tug.dk/FontCatalogue/droidserif/)
* [fbb](http://www.tug.dk/FontCatalogue/fbb/)
* Free Serif, Freefont Serif: siehe GNU Freefont Serif
* Gentium: siehe Gentium Plus
* [Gentium Plus](https://software.sil.org/gentium/support/character-set-support/) (als Fettschrift wird [Gentium Basic](http://www.tug.dk/FontCatalogue/gentium/) verwendet, da Gentium Plus hier nicht vollständig ist)
* [GFS Artemisia](http://www.tug.dk/FontCatalogue/gfsartemisia/)
* [GFS Bodoni](http://www.tug.dk/FontCatalogue/gfsbodoni/)
* [GNU Freefont Serif](http://www.tug.dk/FontCatalogue/gnufreefontserif/)
* Gyre Bonum: siehe TeX Gyre Bonum
* Gyre Pagella: siehe TeX Gyre Pagella
* Gyre Schola: siehe TeX Gyre Schola
* Gyre Termes: siehe TeX Gyre Termes
* [Heuristica](http://www.tug.dk/FontCatalogue/heuristica/)
* [IM Fell English](http://www.tug.dk/FontCatalogue/imfellenglish/)
* [Junicode](http://www.tug.dk/FontCatalogue/junicode/)
* Kerkis: siehe TeX Gyre Bonum
* [Latin Modern Roman](http://www.tug.dk/FontCatalogue/latinmodernroman/)
* [Libre Baskerville](http://www.tug.dk/FontCatalogue/librebaskerville/)
* [Libre Bodoni](http://www.tug.dk/FontCatalogue/librebodoni/)
* [Merriweather](http://www.tug.dk/FontCatalogue/merriweather/)
* [Merriweather Light](http://www.tug.dk/FontCatalogue/merriweatherlight/)
* New PX: siehe TeX Gyre Pagella
* New TX, Nimbus Roman: siehe TeX Gyre Termes
* [Old Standard](http://www.tug.dk/FontCatalogue/oldstandard/)
* Pagella, Palladio: siehe TeX Gyre Pagella
* [Playfair Display](http://www.tug.dk/FontCatalogue/playfairdisplay/)
* PX Fonts: siehe TeX Gyre Pagella
* [Quattrocento](http://www.tug.dk/FontCatalogue/quattrocento/)
* [Roboto Slab](http://www.tug.dk/FontCatalogue/robotoslab/)
* [Roboto Slab Light](http://www.tug.dk/FontCatalogue/robotoslablight/)
* [Source Serif Pro Extra Light](http://www.tug.dk/FontCatalogue/sourceserifproextralight/)
* [Source Serif Pro Light](http://www.tug.dk/FontCatalogue/sourceserifprolight/)
* Source Serif Pro: siehe Source Serif Pro Regular
* [Source Serif Pro Regular](http://www.tug.dk/FontCatalogue/sourceserifproregular/)
* [TeX Gyre Bonum](http://www.tug.dk/FontCatalogue/tegyrebonum/)
* [TeX Gyre Pagella](http://www.tug.dk/FontCatalogue/texgyrepagella/)
* [TeX Gyre Schola](http://www.tug.dk/FontCatalogue/texgyreschola/)
* Termes: siehe TeX Gyre Termes
* [TeX Gyre Termes](http://www.tug.dk/FontCatalogue/texgyretermes/)
* TX Fonts: siehe TeX Gyre Termes
* Schola, Schoolbook, Schoolbook L: siehe TeX Gyre Schola
* URW Bookman, URW Bookman L: siehe TeX Gyre Bonum
* URW Nimbus Roman: siehe TeX Gyre Termes
* URW Palladio: siehe TeX Gyre Pagella
* URW Schoolbook, URW Schoolbook L: siehe TeX Gyre Schola
* [XCharter](http://www.tug.dk/FontCatalogue/xcharter/)
* [XITS](http://www.tug.dk/FontCatalogue/xits/)

### Schreibmaschinenschriften

* Courier: siehe TeX Gyre Cursor
* [Deja Vu Sans Mono](http://www.tug.dk/FontCatalogue/dejavumono/)
* [Fira Mono](http://www.tug.dk/FontCatalogue/firamono/)
* [Latin Modern Mono](http://www.tug.dk/FontCatalogue/latinmodernmono/)
* [Latin Modern Mono Light](http://www.tug.dk/FontCatalogue/latinmodernmonolight/)
* [Source Code Pro](http://www.tug.dk/FontCatalogue/sourcecodepro/)
* [TeX Gyre Cursor](http://www.tug.dk/FontCatalogue/texgyrecursor/)

### Schriften ohne Serifen

* Adventor: siehe TeX Gyre Adventor
* [Cabin](http://www.tug.dk/FontCatalogue/cabin/)
* [Cabin Condensed](http://www.tug.dk/FontCatalogue/cabincondensed/)
* [Carlito](http://www.tug.dk/FontCatalogue/carlito/)
* [Clear Sans](http://www.tug.dk/FontCatalogue/clearsans/)
* Computer Modern Sans Serif: siehe Latin Modern Sans
* [Cyklop](http://www.tug.dk/FontCatalogue/cyklop/)
* [DejaVu Sans](http://www.tug.dk/FontCatalogue/dejavusans/)
* [DejaVu Sans Condensed](http://www.tug.dk/FontCatalogue/dejavusanscondensed/)
* [Droid Sans](http://www.tug.dk/FontCatalogue/droidsans/)
* [Fira Sans Book](http://www.tug.dk/FontCatalogue/firasansbook/)
* [Fira Sans Extra Light](http://www.tug.dk/FontCatalogue/firasansextralight/)
* [Fira Sans Light](http://www.tug.dk/FontCatalogue/firasanslight/)
* Fira Sans: siehe Fira Sans Regular
* [Fira Sans Regular](http://www.tug.dk/FontCatalogue/firasansregular/)
* [Fira Sans Thin](http://www.tug.dk/FontCatalogue/firasansthin/)
* [Fira Sans Ultra Light](http://www.tug.dk/FontCatalogue/firasansultralight/)
* Freefont Sans, Free Sans: siehe GNU Freefont Sans
* [GFS Neohellenic](http://www.tug.dk/FontCatalogue/gfsneohellenic/)
* [GNU Freefont Sans](http://www.tug.dk/FontCatalogue/gnufreefontsans/)
* Gyre Adventor: siehe TeX Gyre Adventor
* Gyre Heros: siehe TeX Gyre Heros
* Heros: siehe TeX Gyre Heros
* [Iwona](http://www.tug.dk/FontCatalogue/iwona/)
* [Iwona Light](http://www.tug.dk/FontCatalogue/iwonalight/)
* [Kurier](http://www.tug.dk/FontCatalogue/kurier/)
* [Kurier Light](http://www.tug.dk/FontCatalogue/kurierlight/)
* [Latin Modern Sans](http://www.tug.dk/FontCatalogue/latinmodernsans/)
* [Lato](http://www.tug.dk/FontCatalogue/lato/)
* [Merriweather Sans](http://www.tug.dk/FontCatalogue/merriweathersans/)
* [Merriweather Sans Light](http://www.tug.dk/FontCatalogue/merriweathersanslight/)
* [Mintspirit](http://www.tug.dk/FontCatalogue/mintspirit/)
* Neohellenic: siehe GFS Neohellenic
* [Open Sans](http://www.tug.dk/FontCatalogue/opensans/)
* [Overlock](http://www.tug.dk/FontCatalogue/overlock/)
* [Quattrocento Sans](http://www.tug.dk/FontCatalogue/quattrocentosans/)
* [Raleway](http://www.tug.dk/FontCatalogue/raleway/)
* [Roboto](http://www.tug.dk/FontCatalogue/roboto/)
* [Roboto Condensed](http://www.tug.dk/FontCatalogue/robotocondensed/)
* [Roboto Light](http://www.tug.dk/FontCatalogue/robotolight/)
* [Source Sans Pro](http://www.tug.dk/FontCatalogue/sourcesanspro/)
* [TeX Gyre Adventor](http://www.tug.dk/FontCatalogue/texgyreadventor/)
* [TeX Gyre Heros](http://www.tug.dk/FontCatalogue/texgyreheros/)
* URW Nimbus Sans: siehe TeX Gyre Heros
* URW Gothic: siehe TeX Gyre Adventor

### Calligraphical and Handwritten

* [Lobster Two](http://www.tug.dk/FontCatalogue/lobstertwo/)
* [Miama Nueva](http://www.tug.dk/FontCatalogue/miamanueva/)
* [TeX Gyre Chorus](http://www.tug.dk/FontCatalogue/texgyrechorus/)

### Special

* [Cinzel](http://www.tug.dk/FontCatalogue/cinzel/)
* [Punk Nova](http://www.tug.dk/FontCatalogue/punknova/)

## LaTeX Lizenz

Unter dem Dateipfad `latex/license.tex` kann eine Lizenz (als gültiges LaTeX-Dokument) bereitgestellt werden. Fehlt diese Datei, wird keine Lizenz an das Dokument angefügt. 

Für die Lizenzen existieren Vorlagen im Verzeichnis `latex/templates/licenses`.

## LaTeX Titelei und Anhang

Wurde die Setup-Option `bookPrint` gewählt, können LaTeX-Dokumente für die Titelei und den Anhang des Buches in dafür vorgesehene Verzeichnisse eingefügt werden. 
Die Dateien im jeweiligen Verzeichnis werden in alphanumerischer Reihenfolge in das Dokument eingefügt.

Verzeichnis für die Titelei: `latex/bookPreliminaries`

Verzeichnis für den Anhang: `latex/bookAppendix`

Vorlagen finden sich unter `latex/templates`.

## LaTeX build

Im `latex`-Verzeichnis dieses Projekts muss `latex-document.tex` per `lualatex` kompiliert werden (für das Erstellen des Inhaltsverzeichnisses ist dies zweimal durchzuführen). `build.bat` dient als Helferlein für Windows (unter Linux  kann `./build.bash` ausgeführt werden).

```
$ build.bat
[...]
Output written on latex-document.pdf (35 pages, 115586 bytes).
Transcript written on latex-document.log.
```

Der Kompiliervorgang wurde mit TeX Live 2015's `lualatex` getestet.

## HTML Lizenz

Unter dem Dateipfad `html/license.tpl.html` kann eine Lizenz (als gültiges HTML ohne header und body) eingefügt werden. Das dafür vorgesehene CSS-Stylesheet findet sich unter `html/css/license-styles.css`. 

Für Lizenz und zugehöriges CSS finden sich Templates im Verzeichnis `html/templates/licenses`.

## Dateiformat der Dokumentenquelle
Erwartet wird eine Text-Datei in UTF-8-Kodierung.


## Markupformat der Dokumentenquelle


### Absatztrennung
Markup: Zeilenumbruch

Beispiel: 
```
Dies ist der erste Absatz.
Hier beginnt der zweite Absatz.
```


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

* <https://de.wikipedia.org/wiki/Viertelgeviertstrich#Bindestrich-Minus>


### Gedankenstriche (en-dash)
Markup: Doppelminus.

Beispiel: `Glitzer, Filz, Garn und Knöpfe -- seine Küche sah aus als wäre ein Clown in ihr explodiert.`

HTML: wird übersetzt zu en-dash (`&ndash;`).
LaTeX: wird übersetzt zu `--`.

Refs:

* <https://de.wikipedia.org/wiki/Halbgeviertstrich>


### Gedankenstriche (em-dash)
Markup: Dreifaches Minus.

Beispiel: `Glitter, felt, yarn, and buttons---his kitchen looked as if a clown had exploded.`

HTML: wird übersetzt zu em-dash (`&mdash;`).
LaTeX: wird übersetzt zu `---`.

Refs:

* <https://de.wikipedia.org/wiki/Geviertstrich>


### Kursiv
Markup: Mit Unterstrichen (_) oder Asterisken (*) umgeben.

Beispiel: `Hier ist _etwas_ kursiv geschrieben. Hier *noch etwas*.`

Der markierte Textabschnitt wird kursiv dargestellt.

Refs:

* <https://de.wikipedia.org/wiki/Kursivschrift>


### Fett
Markup: Mit doppelten Unterstrichen (__) oder doppelten Asterisken (**) umgeben.

Beispiel: `Hier ist __etwas__ fett gedruckt. Hier **noch etwas**.`

Der markierte Textabschnitt wird fett dargestellt.

Refs:

* <https://de.wikipedia.org/wiki/Schriftschnitt>


### Auslassungspunkte
Markup: Drei normale Punkte.

Beispiel: `Das ist... ähm... doof.`

HTML: wird übersetzt zu `&hellip;`.
LaTeX: wird übersetzt zu `\dots`.

Refs:

* <https://de.wikipedia.org/wiki/Auslassungspunkte>


### Fußnoten
Markup: Eckige Klammern.

Beispiel: `Das ist das WortNachDemDieFußNoteKommt[Die Fußnote].`


### Kommentare

#### Unterstreichen
Markup: Doppelte runde Klammern

Derart markierter Text wird im Entwurfsmodus (`outputMode = "draft"`) mit geschlängelter Linie unterstrichen.

Beispiel: `((Dieser Text ist überarbeitungswürdig))`

#### Randnotiz
Markup: Doppelte eckige Klammern

Derart markierter Text wird im Entwurfsmodus (`outputMode = "draft"`) als Randnotiz dargestellt und sonst ausgeblendet.

Beispiel: `Ihr Name war Thorsten[[Überlegen, ob Thorsten wirklich ein geeigneter Name ist.]]`

#### In Kombination

Es kann nützlich sein, die beiden Kommentarfunktionen zu kombinieren.

Beispiel: `((Dieser Text ist sehr sehr ultra mega schlecht))[[Leicht übertrieben? Überflüssige Adverben streichen.]].`  


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
`()`  Klammern (nur bei doppelten, also '((' bzw. '))', da dies Kommentar-Unterstreichungen markiert)  
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

* <https://www.w3.org/International/questions/qa-escapes.de#use>
* <https://www.namsu.de/Extra/strukturen/Sonderzeichen.html>

# English Documentation

## Requirements / Installation

Of course [Python](https://www.python.org/) has to be installed.

`filt0r.py` has the following additional requirements:

* [Python TOML](https://pypi.python.org/pypi/toml)

Install requirements before first usage:  
`pip install -r requirements.txt`

## Conversion of Source Document to HTML & LaTeX

The Conversion to HTML & LaTeX is done with `filt0r.py`. `filt0r.py` was tested with Python 2.7 and 3.4. One argument is expected: the path to the source document. 

Example:
```
$ python filt0r.py doc.txt
[...]
15:13:17:977.0  INFO: Wrote UTF-8-encoded LaTeX source file: latex/latex-body.tex.
[...]
15:13:17:987.0  INFO: Wrote UTF-8-encoded HTML document: html/index.html.
```

Optional argument: the path to setup file (see below) if different from `setup.toml`. Example:  
`python filt0r.py doc.txt toml.toml`

`filt0r.py` should be executed in the projects root directory. It writes the files `latex/latex-document.tex`, `latex/latex-body.tex` and `html/index.html` relative to the current working directory.

## Setup

In a setup file in TOML notation (default: `setup.toml`) general settings and details for the target document can be specified.

### The following settings are required:

#### General:
```
[general]
title = "Title of text"
author = "Author of text"
language = "Language shortcode" #de, en, ... (https://en.wikipedia.org/wiki/ISO_639-1)
```

#### LaTeX:
```
[latex]
pdfsubject = "Short description for PDF metadata"
pdfkeywords = "A sequence of keywords for PDF metadata separated by commas"
```

#### HTML:
```
[html]
locale = "Locale" #de_DE, en_GB, ... #meta property og:locale
metadescription = "Description for HTML metadata" #meta description und meta property og:description
url = "URL of text" #meta property og:url
sitename = "Name of Site that hosts text" #meta property og:site_name
```

### Optional Settings:

#### General:
```
[general]
subtitle = "Subtitle of text"
outputMode = "Type of generated document" #draft, final, manuscript #default: final 
    #draft:
        # comments are shown
        # page format: A4
        # font: TeX Gyre Cursor (~Courier)
        # please note: this mode is still work in progress
    #final:
        # no comments
        # output document as configured
    #manuscript 
        # no comments
        # page format: A4
        # font: TeX Gyre Cursor (~Courier)
        # please note: this mode is still work in progress
```
#### LaTeX Layout:
```
[latex]
pageFormat = "Page format" #a0 - a6, b0 - b6 #default: a5 #if set, pageWidth and pageHeight will be ignored
pageWidth = "Page width" #e.g. "210mm", "21.5cm"
pageHeight = "Page height" #e.g. "210mm", "21.5cm"
bindingOffset = "Binding offset"
font = "Name of the font (see section about fonts)"
fontSize = "Font size in pt" #e.g. 12.5 #default: 11
```

#### LaTeX Title
```
title = "Title of text" #default: general.title
subtitle = "Subtitle of text" #default: general.title
printAuthorOnTitle = "Author will be printed on title at document begin" #not relevant for bookPrint = "true" #default: false
halfTitle = "Half title" #Textcommand \\storyhalftitle #default: latex.title
isbn = "ISBN for this book" #Textcommand \\isbn
```

#### LaTeX Book Print
```
bookPrint = "Textlayout for book printing" #true, false #default: false
    #true: 
        #document type = "scrbook"
        #pages from latex/bookPreliminaries will be prepended to the text in alphanumerical order
        #pages from latex/bookAppendix will be appended to the text in alphanumerical order
    #false:
        #document type = "scrreprt"
        #at beginning of text title and subtitle will be printed
```    

#### LaTeX Header
```
headerLeft = "Header left" #Textcommands can be used (see below) #default: "\\storytitle"
headerRight = "Header right" #Textcommands can be used (see below) #default: "\\storychapter"
```

#### LaTeX Table of Contents
```
tableOfContents = "Table of contents will be printed" #true, false #default: false
contentsTitle = "Title for table of contents"
tableOfContentsPagebreak = "Pagebreak after table of contents" #true, false #default: false
```

#### LaTeX Chapter
```
chapterPagebreak = "New Page at new chapter" #true, false #default: false
hideChapterHeader = "No header at new chapter" #true, false #default: self.chapterPagebreak
```

#### LaTeX PDF Settings
```
hascolorlinks = "Colored links" #default: "false"
urlcolor = "URL color" #default: "blue"
linkcolor = "Link color" #default: "black"
```

#### HTML:
```
[html]
title = "Title of text" #if different from general.title
subtitle = "Subtitle of text" #if different from  general.subtitle
headertitle = "Text for HTML Title" #default: "title | author"
previewimage = "Link for preview image (metadata)" #meta property og:image
```

### Example Setup File
```
[general]
title = "Kommt und holt sie"
#subtitle = ""
author = "Josa Wode"
language = "de" #de, en, ...
outputMode = "final"

[latex]
bookPrint = true #true, false #create document for book printing, allow preliminaries and appendix (directories: latex/bookPreliminaries and latex/bookAppendix)
#headerLeft = "" #define text for left header, you may use commands \\storytitle, \\storysubtitle, \\storyhalftitle, \\storyauthor, \\storychapter; default: \\storytitle
#headerRight = "" #define text for right header, you may use commands \\storytitle, \\storysubtitle, \\storyhalftitle, \\storyauthor, \\storychapter; default: \\storychapter
#hideChapterHeader = true #true, false #default: chapterPagebreak
chapterPagebreak = true #true, false #true: new chapter starts on new page
tableOfContents = true #true, false
#tableOfContentsPagebreak = true #true, false #true: after tableOfContents a new page is started
contentsTitle = "Inhalt" #if specified this is used as title for the table of contents
isbn = "978-3-7460-9728-2"
pageFormat = "a5" # a0 - a6, b0 - b6 # define page size
#pageWidth = "210" # in mm # only when not using pageFormat
#pageHeight = "297" # in mm # only when not using pageFormat
bindingOffset = "15mm" #part of the page that is lost in binding
font = "gentium"
fontSize = "11" # e.g. 11 12.5 # in pt
printAuthorOnTitle = false #true, false #determines if title page begins with author name
#title = "" #comment out if same as general.title
subtitle = "Eine Geschichte von Josa Wode" #comment out if same as general.subtitle
#halfTitle = "" #half title for book printing #comment out if same as title
pdfsubject = "Geschichte"
pdfkeywords = "geschichte, alte, josa, wode"
hascolorlinks = "true"
urlcolor = "blue"
linkcolor = "black"
    
[html]
#title = "" #comment out if same as general.title
#subtitle = "" #comment out if same as general.subtitle
headertitle = "Kommt und holt sie | eine Geschichte von Josa Wode"
url = "http://writing.fotoelectrics.de/documents/come-get-her/de/html/" #meta property og:url
metadescription = "Eine kurze Geschichte von Josa Wode - Es könnte ein Märchen sein, wenn es sich benehmen würde. (Lizenz: Creative Commons BY-NC-SA 3.0)"    #meta description and meta property og:description
locale = "de_DE" #de_DE, en_GB, ... #meta property og:locale
sitename = "writing.fotoelectrics" #meta property og:site_name
#previewimage = "" #meta property og:image #comment out for no image tag
```

## LaTeX Textcommands

For usage in (aditional) LaTeX documents (see below) and some setup entries (see above) the following commands can be used (additional to the usual LaTeX commands):

* `\storytitle`     print title
* `\storysubtitle`  print subtitle
* `\storyhalftitle` print half title
* `\storyauthor`    print author
* `\storychapter`   print current chapter
* `\isbn`           print ISBN
* `\printtitle`     print formated title, with subtitle (if any) and when setup option `printAuthorOnTitle` is set also the author

For usage in setup TOML `\` has to be prepended to the command as escape character (e.g. `\\storytitle`).

## LaTeX Schriften

A whole lot of LaTeX fonts is supported. That doesn't mean they are a good choice for your textstory.

For running text you should choose a font with serifs to improve readability.
By default Gentium is selected as textstory font -- it looks good, is typographically high-end and thorougly
tested in the field of textstories.

Up to now only the main font can be configured.

For draft and manuscript mode TeX Gyre Cursor, kind of Courier, is set to conform to the standard.

The font for license text is Cabin.  

### Serif fonts

* [Alegreya](http://www.tug.dk/FontCatalogue/alegreya/)
* Artemisia: see GFS Artemisia
* Baskerville: see Libre Baskerville
* Bonum, Bookman: see TeX Gyre Bonum
* [Caladea](http://www.tug.dk/FontCatalogue/caladea/)
* [Cochineal](http://www.tug.dk/FontCatalogue/cochineal/)
* Computer Modern: see Latin Modern Roman
* [DejaVu Serif](http://www.tug.dk/FontCatalogue/dejavuserif/)
* [DejaVu Serif Condensed](http://www.tug.dk/FontCatalogue/dejavuserifcondensed/)
* [Droid Serif](http://www.tug.dk/FontCatalogue/droidserif/)
* [fbb](http://www.tug.dk/FontCatalogue/fbb/)
* Free Serif, Freefont Serif: see GNU Freefont Serif
* Gentium: see Gentium Plus
* [Gentium Plus](https://software.sil.org/gentium/support/character-set-support/) (as bold font [Gentium Basic](http://www.tug.dk/FontCatalogue/gentium/) is used, because Gentium Plus bold is not complete)
* [GFS Artemisia](http://www.tug.dk/FontCatalogue/gfsartemisia/)
* [GFS Bodoni](http://www.tug.dk/FontCatalogue/gfsbodoni/)
* [GNU Freefont Serif](http://www.tug.dk/FontCatalogue/gnufreefontserif/)
* Gyre Bonum: see TeX Gyre Bonum
* Gyre Pagella: see TeX Gyre Pagella
* Gyre Schola: see TeX Gyre Schola
* Gyre Termes: see TeX Gyre Termes
* [Heuristica](http://www.tug.dk/FontCatalogue/heuristica/)
* [IM Fell English](http://www.tug.dk/FontCatalogue/imfellenglish/)
* [Junicode](http://www.tug.dk/FontCatalogue/junicode/)
* Kerkis: see TeX Gyre Bonum
* [Latin Modern Roman](http://www.tug.dk/FontCatalogue/latinmodernroman/)
* [Libre Baskerville](http://www.tug.dk/FontCatalogue/librebaskerville/)
* [Libre Bodoni](http://www.tug.dk/FontCatalogue/librebodoni/)
* [Merriweather](http://www.tug.dk/FontCatalogue/merriweather/)
* [Merriweather Light](http://www.tug.dk/FontCatalogue/merriweatherlight/)
* New PX: see TeX Gyre Pagella
* New TX, Nimbus Roman: see TeX Gyre Termes
* [Old Standard](http://www.tug.dk/FontCatalogue/oldstandard/)
* Pagella, Palladio: see TeX Gyre Pagella
* [Playfair Display](http://www.tug.dk/FontCatalogue/playfairdisplay/)
* PX Fonts: see TeX Gyre Pagella
* [Quattrocento](http://www.tug.dk/FontCatalogue/quattrocento/)
* [Roboto Slab](http://www.tug.dk/FontCatalogue/robotoslab/)
* [Roboto Slab Light](http://www.tug.dk/FontCatalogue/robotoslablight/)
* [Source Serif Pro Extra Light](http://www.tug.dk/FontCatalogue/sourceserifproextralight/)
* [Source Serif Pro Light](http://www.tug.dk/FontCatalogue/sourceserifprolight/)
* Source Serif Pro: see Source Serif Pro Regular
* [Source Serif Pro Regular](http://www.tug.dk/FontCatalogue/sourceserifproregular/)
* [TeX Gyre Bonum](http://www.tug.dk/FontCatalogue/tegyrebonum/)
* [TeX Gyre Pagella](http://www.tug.dk/FontCatalogue/texgyrepagella/)
* [TeX Gyre Schola](http://www.tug.dk/FontCatalogue/texgyreschola/)
* Termes: see TeX Gyre Termes
* [TeX Gyre Termes](http://www.tug.dk/FontCatalogue/texgyretermes/)
* TX Fonts: see TeX Gyre Termes
* Schola, Schoolbook, Schoolbook L: see TeX Gyre Schola
* URW Bookman, URW Bookman L: see TeX Gyre Bonum
* URW Nimbus Roman: see TeX Gyre Termes
* URW Palladio: see TeX Gyre Pagella
* URW Schoolbook, URW Schoolbook L: see TeX Gyre Schola
* [XCharter](http://www.tug.dk/FontCatalogue/xcharter/)
* [XITS](http://www.tug.dk/FontCatalogue/xits/)

### Typewriter fonts

* Courier: see TeX Gyre Cursor
* [Deja Vu Sans Mono](http://www.tug.dk/FontCatalogue/dejavumono/)
* [Fira Mono](http://www.tug.dk/FontCatalogue/firamono/)
* [Latin Modern Mono](http://www.tug.dk/FontCatalogue/latinmodernmono/)
* [Latin Modern Mono Light](http://www.tug.dk/FontCatalogue/latinmodernmonolight/)
* [Source Code Pro](http://www.tug.dk/FontCatalogue/sourcecodepro/)
* [TeX Gyre Cursor](http://www.tug.dk/FontCatalogue/texgyrecursor/)

### Sans Serif fonts

* Adventor: see TeX Gyre Adventor
* [Cabin](http://www.tug.dk/FontCatalogue/cabin/)
* [Cabin Condensed](http://www.tug.dk/FontCatalogue/cabincondensed/)
* [Carlito](http://www.tug.dk/FontCatalogue/carlito/)
* [Clear Sans](http://www.tug.dk/FontCatalogue/clearsans/)
* Computer Modern Sans Serif: see Latin Modern Sans
* [Cyklop](http://www.tug.dk/FontCatalogue/cyklop/)
* [DejaVu Sans](http://www.tug.dk/FontCatalogue/dejavusans/)
* [DejaVu Sans Condensed](http://www.tug.dk/FontCatalogue/dejavusanscondensed/)
* [Droid Sans](http://www.tug.dk/FontCatalogue/droidsans/)
* [Fira Sans Book](http://www.tug.dk/FontCatalogue/firasansbook/)
* [Fira Sans Extra Light](http://www.tug.dk/FontCatalogue/firasansextralight/)
* [Fira Sans Light](http://www.tug.dk/FontCatalogue/firasanslight/)
* Fira Sans: see Fira Sans Regular
* [Fira Sans Regular](http://www.tug.dk/FontCatalogue/firasansregular/)
* [Fira Sans Thin](http://www.tug.dk/FontCatalogue/firasansthin/)
* [Fira Sans Ultra Light](http://www.tug.dk/FontCatalogue/firasansultralight/)
* Freefont Sans, Free Sans: see GNU Freefont Sans
* [GFS Neohellenic](http://www.tug.dk/FontCatalogue/gfsneohellenic/)
* [GNU Freefont Sans](http://www.tug.dk/FontCatalogue/gnufreefontsans/)
* Gyre Adventor: see TeX Gyre Adventor
* Gyre Heros: see TeX Gyre Heros
* Heros: see TeX Gyre Heros
* [Iwona](http://www.tug.dk/FontCatalogue/iwona/)
* [Iwona Light](http://www.tug.dk/FontCatalogue/iwonalight/)
* [Kurier](http://www.tug.dk/FontCatalogue/kurier/)
* [Kurier Light](http://www.tug.dk/FontCatalogue/kurierlight/)
* [Latin Modern Sans](http://www.tug.dk/FontCatalogue/latinmodernsans/)
* [Lato](http://www.tug.dk/FontCatalogue/lato/)
* [Merriweather Sans](http://www.tug.dk/FontCatalogue/merriweathersans/)
* [Merriweather Sans Light](http://www.tug.dk/FontCatalogue/merriweathersanslight/)
* [Mintspirit](http://www.tug.dk/FontCatalogue/mintspirit/)
* Neohellenic: see GFS Neohellenic
* [Open Sans](http://www.tug.dk/FontCatalogue/opensans/)
* [Overlock](http://www.tug.dk/FontCatalogue/overlock/)
* [Quattrocento Sans](http://www.tug.dk/FontCatalogue/quattrocentosans/)
* [Raleway](http://www.tug.dk/FontCatalogue/raleway/)
* [Roboto](http://www.tug.dk/FontCatalogue/roboto/)
* [Roboto Condensed](http://www.tug.dk/FontCatalogue/robotocondensed/)
* [Roboto Light](http://www.tug.dk/FontCatalogue/robotolight/)
* [Source Sans Pro](http://www.tug.dk/FontCatalogue/sourcesanspro/)
* [TeX Gyre Adventor](http://www.tug.dk/FontCatalogue/texgyreadventor/)
* [TeX Gyre Heros](http://www.tug.dk/FontCatalogue/texgyreheros/)
* URW Nimbus Sans: see TeX Gyre Heros
* URW Gothic: see TeX Gyre Adventor

### Calligraphical and Handwritten

* [Lobster Two](http://www.tug.dk/FontCatalogue/lobstertwo/)
* [Miama Nueva](http://www.tug.dk/FontCatalogue/miamanueva/)
* [TeX Gyre Chorus](http://www.tug.dk/FontCatalogue/texgyrechorus/)

### Special

* [Cinzel](http://www.tug.dk/FontCatalogue/cinzel/)
* [Punk Nova](http://www.tug.dk/FontCatalogue/punknova/)

## LaTeX License

At file path `latex/license.tex` a license can be provided (as valid LaTeX document). If this file is missing, no license will be appended to the document. 

Directory for license templates: `latex/templates/licenses`

## LaTeX Preliminaries and Appendix

With setup option `bookPrint` set to `true` LaTeX documents for preliminary pages and appendix pages can be put in designated directories. 
Files in those directories will be added to the document in alphanumerical order.

Directory for preliminaries: `latex/bookPreliminaries`

Directory for appendix: `latex/bookAppendix`

Templates can be found in `latex/templates`.

## LaTeX build

In the projects `latex` directory `latex-document.tex` has to be compiled with `lualatex` (for correct creation of table of contents this has to be done twice). `build.bat` is a helper for Windows, `./build.bash` can be used on Linux systems.

```
$ build.bat
[...]
Output written on latex-document.pdf (35 pages, 115586 bytes).
Transcript written on latex-document.log.
```

Compilation was tested with TeX Live 2015's `lualatex`.

## HTML License

At file path `html/license.tpl.html` a license can be provided (as valid HTML without header and body). The corresponding CSS stylesheet can be found at `html/css/license-styles.css`. 

For license and license CSS templates can be found in `html/templates/licenses`.

## File Format of Source Document

An UTF-8 encoded document is expected.


## Markup of Source Document

### New Paragraph
Markup: newline

Example: 
```
This is the first paragraph.
Here the second one begins.
```


### New Section
Markup: two newlines resp. blank line

Example:
`Here is the text of first section.

Here a new section begins.`


### Captions and Chapters
Markup: double hash at line beginning

Example: `## Chapter 1`

A line marked this way will be formated as a headline (and interpreted as beginning of a chapter).


### Quotes
Markup: Simple double quote pairs.

Example: `She said: "Oh shit!"`

In output French quotes will be printed.

Refs:

* <https://en.wikipedia.org/wiki/Guillemet>


### Hyphen
Markup: Simple minus.

Example: `man-eating shark`

Copied to HTML and LaTeX code as is.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### En-dash
Markup: Double minus.

Example: `Glitzer, Filz, Garn und Knöpfe -- seine Küche sah aus als wäre ein Clown in ihr explodiert.`

HTML: will be translated to en-dash (`&ndash;`).
LaTeX: still `--`.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### Em-dash
Markup: Triple minus.

Example: `Glitter, felt, yarn, and buttons---his kitchen looked as if a clown had exploded.`

HTML: translated to em-dash (`&mdash;`).
LaTeX: still `---`.

Refs:

* <http://jakubmarian.com/hyphen-minus-en-dash-and-em-dash-difference-and-usage-in-english/>


### Italics
Markup: Surround with underscores (_) or asterisks (*).

Example: `_This_ is *italic*.`

The marked text will be printed in italics.

Refs:

* <https://en.wikipedia.org/wiki/Italic_type>


### Bold
Markup: Surround with double underscores (__) or double asterisks (**).

Example: `__This__ is **bold**.`

The marked text will be printed in bold font.

Refs:

* <https://en.wikipedia.org/wiki/Emphasis_(typography)>


### Ellipsis
Markup: Three normal dots.

Example: `That is... ahem... crap.`

HTML: `&hellip;`.
LaTeX: `\dots`.

Refs:

* <https://en.wikipedia.org/wiki/Ellipsis>


### Footnotes
Markup: Square brackets.

Example: `This is the word-after-which-the-footnote-appears[The footnote].`


### Comments

#### Underline
Markup: Double round brackets.

Text marked like this will be underlined with a wiggly line in draft.

Example: `((This text may need rework))`

#### Sidenote
Markup: Double square bracktes.

Text marked like this will be shown as a sidenote in draft and is hidden otherwise.

Example: `Her name was Thorsten[[Think about it. Is this really a good name for her?]]`

#### Combined

You may want to combine both comment types.

Example: `((This text is very very ultra mega bad))[[Too much? Remove some adverbs.]].`  


### Images
Markup: \!\[altText\]\(Image path "optional title"\)

This way images at the given image path can be added. The optional title is used as an image caption. altText is shown in HTML when image cannot be displayed and used by screen readers. In LaTeX altText will be ignored.

Example: `![Alternative text](/path/to/img.jpg "optional title")`

### Masking of Special Characters
Markup: Backslash followed by special character ('`\specialchar`')

In HTML, LaTeX and our markup certain symbols are reserved as parts of the syntax. They have to be masked to be interpreted as the simple symbol and to be shown as such in the generated output text.

The following characters have to be escaped (prepend '`\`'):  
`\`   backslash &ndash; the escape character itself  
`*`   asterisk  
`_`   underscore  
`{}`  curly brackets  
`()`  normal brackets (only if used in double, like '((' or '))', because this marks commentary underlining)  
`[]`  square brackets  
`#`   hash  
`"`   double quote  
`!`   exclamation mark (only when followed by '[')  
`--`  double minus  
`$`   dollar  

The following characters can be used as normal and will automatically be translated in HTML and LaTeX representation:  
`&`   in HTML becomes '`&amp;`', in LaTeX '`\&`'  
`<`   in HTML becomes `&lt;`  
`>`   in HTML becomes `&gt;`  
`%`   in LaTeX becomes `\%`  
`~`   in LaTeX becomes `\textasciitilde`  
`^`   in LaTeX becomes `\textasciicircum`  

Example: `Angle brackets <very angular> and square brackets \[because it's square\].`

Refs:

* <https://www.w3.org/International/questions/qa-escapes#use>
* <https://en.wikibooks.org/wiki/LaTeX/Basics#Reserved_Characters>
