# 📰 RSS Aggregator - Kronen Zeitung

Ein modernes, interaktives Webanwendung zur Anzeige von RSS-Feeds der Kronen Zeitung (österreichische Zeitung) mit fortgeschrittenen Funktionen wie Live-Suche, Light/Dark Theme und dynamischen Kategorie-Farben.

![Python Version](https://img.shields.io/badge/python-3.12+-blue.svg)
![Flask Version](https://img.shields.io/badge/flask-2.3.2-green.svg)
![License](https://img.shields.io/badge/license-MIT-blue.svg)

## ✨ Features

### 📱 Benutzeroberfläche
- **Modernes Glassmorphism Design** - Frosted glass Effekt mit backdrop-filter blur
- **Responsive Grid Layout** - 5 Artikel pro Reihe (anpassbar auf kleineren Bildschirmen)
- **Smooth Animations** - Entrance-Animationen und Hover-Effekte mit cubic-bezier easing
- **Light/Dark Theme** - Umschaltbar mit 🌙/☀️ Button, Einstellung wird gespeichert
- **Dynamischer Hintergrund** - Farbige Gradient basierend auf aktiver Kategorie

### 🔍 Suche & Navigation
- **Echtzeit-Volltext-Suche** - Durchsucht Titel und gesamten Artikel-Inhalt
- **Keine API-Aufrufe** - 100% Frontend-basiert für Geschwindigkeit
- **8 Nachrichten-Kategorien** - Top-News, Sport, Wirtschaft, Politik, Österreich, Welt, Wissenschaft, Wetter
- **Tab-basierte Navigation** - Mit animierten Underlines in Kategorie-Farben
- **Artikel-Limitierung** - Max. 20 Artikel pro Kategorie

### 🎨 Visuelles Design
- **Kategorie-spezifische Farben**:
  - 🔵 Top-News: Blau (#667eea)
  - 🔴 Sport: Rot (#f85032)
  - 🟢 Wirtschaft: Grün (#00b894)
  - 🟠 Politik: Orange (#e55039)
  - 🔵 Österreich: Hellblau (#0984e3)
  - 🟣 Welt: Lila (#6c5ce7)
  - 🔷 Wissenschaft: Türkis (#00cec9)
  - 🟡 Wetter: Gelb (#fdcb6e)

- **Intelligente Bildverarbeitung** - Extrahiert Bilder aus mehreren RSS-Quellen
- **Smooth Transitions** - 0.6s cubic-bezier Übergänge zwischen Kategorien

### 🛠️ Backend-Features
- **Robuste XML-Verarbeitung** - Dual-Parser (lxml mit Fallback zu Regex)
- **Malformed XML Handling** - Verarbeitet auch fehlerhafte RSS-Feeds
- **Content Extraction** - Extrahiert vollständigen Artikel-Inhalt (`content:encoded`)
- **Image Extraction** - Sucht in HTML, media:content, media:thumbnail, enclosures
- **HTML Cleaning** - Entfernt Tags für saubere Textanzeige
- **Fehlerbehandlung** - Graceful Degradation bei Feed-Fehlern

## 🚀 Installation

### Anforderungen
- Python 3.12+
- pip (Python Package Manager)
- Moderner Webbrowser (Chrome 76+, Firefox 94+, Safari 15+)

### Schritt-für-Schritt

1. **Repository klonen**
```bash
git clone https://github.com/yourusername/RSS-Aggregator.git
cd RSS-Aggregator
```

2. **Dependencies installieren**
```bash
pip3 install -r requirements.txt
```

3. **Entwicklungs-Server starten**
```bash
python3 app.py
```

4. **Browser öffnen**
```
http://localhost:8080
```

## 📋 Dependencies

```
Flask==2.3.2          # Web Framework
requests==2.31.0      # HTTP Library
Werkzeug==2.3.6       # WSGI Utilities
lxml                  # XML Parser (optional, aber empfohlen)
```

## 🏗️ Projektstruktur

```
RSS-Aggregator/
├── app.py                    # Flask Backend (RSS-Parsing, API)
├── requirements.txt          # Python Dependencies
├── templates/
│   └── index.html           # Frontend (HTML + CSS + JS)
├── README.md                # Diese Datei
└── CLAUDE.md                # Entwickler-Dokumentation
```

## 💻 Verwendung

### Hauptseite
1. Öffne `http://localhost:8080` im Browser
2. Artikel werden automatisch von allen 8 RSS-Feeds geladen
3. Klick auf Kategorie-Tabs um zwischen News-Bereichen zu wechseln
4. Der Hintergrund ändert Farbe basierend auf aktiver Kategorie

### Suche
1. Nutze das Suchfeld oben um schnell Artikel zu filtern
2. Suche funktioniert in Echtzeit während du tippst
3. Sucht in Titel und vollständigem Artikel-Inhalt
4. "Keine Artikel gefunden" Nachricht wenn keine Treffer

### Theme-Umschaltung
1. Klick auf 🌙 Button oben rechts für Dark Mode
2. Klick auf ☀️ Button um zu Light Mode zurückzukehren
3. Deine Einstellung wird automatisch gespeichert

### Artikel-Navigation
1. Klick auf eine Artikel-Karte um den vollständigen Artikel zu öffnen
2. Das Bild und Text sind beide clickable
3. Artikel öffnet sich in neuem Tab

## 🔧 Konfiguration

### RSS-Feeds hinzufügen/ändern

Bearbeite `RSS_FEEDS` Dictionary in `app.py`:

```python
RSS_FEEDS = {
    'Kategorie-Name': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=FEED_ID',
}
```

Dann füge entsprechende Farbe in `templates/index.html` hinzu:

```javascript
const categoryColors = {
    'Kategorie-Name': '#HEXCOLOR',
};
```

### Port ändern

Bearbeite am Ende von `app.py`:

```python
if __name__ == '__main__':
    app.run(debug=True, port=8080)  # PORT hier ändern
```

## 🌐 RSS-Feed-IDs

Bekannte Kronen Zeitung Feed-IDs:
- Top-News: 2311992
- Sport: 989
- Wirtschaft: 136
- Politik: 305
- Österreich: 102
- Welt: 90
- Wissenschaft: 350
- Wetter: 1789989

Format: `https://api.krone.at/v1/rss/rssfeed-google.xml?id=FEED_ID`

## 🎨 Design-System

### CSS Custom Properties

```css
--bg-light              /* Light Mode Background Gradient */
--bg-dark               /* Dark Mode Background Gradient */
--category-color        /* Aktive Kategorie-Farbe */
--text-light           /* Light Mode Text Color */
--text-dark            /* Dark Mode Text Color */
--card-light           /* Light Mode Card Background */
--card-dark            /* Dark Mode Card Background */
--border-light         /* Light Mode Border Color */
--border-dark          /* Dark Mode Border Color */
```

### Farbpalette

Die Anwendung nutzt moderne Farben mit guter Kontrast-Verhältnisse:

| Kategorie | Hex-Farbe | RGB |
|-----------|-----------|-----|
| Top-News | #667eea | 102, 126, 234 |
| Sport | #f85032 | 248, 80, 50 |
| Wirtschaft | #00b894 | 0, 184, 148 |
| Politik | #e55039 | 229, 80, 57 |
| Österreich | #0984e3 | 9, 132, 227 |
| Welt | #6c5ce7 | 108, 92, 231 |
| Wissenschaft | #00cec9 | 0, 206, 201 |
| Wetter | #fdcb6e | 253, 203, 110 |

## 🔍 Suche-Implementation

### Wie die Suche funktioniert

1. **Indexierung**: Vollständiger Artikel-Text wird in `data-full-text` Attribut gespeichert
2. **Echtzeit-Filterung**: JavaScript filtert Artikel bei jedem Tastendruck
3. **Case-insensitive**: Groß-/Kleinschreibung spielt keine Rolle
4. **Keine API-Aufrufe**: Alles läuft im Browser für maximale Geschwindigkeit

### Suchbereich

Die Suche indexiert:
- Artikel-Titel
- Vollständige Artikel-Beschreibung
- Kompletter Artikel-Inhalt (aus `content:encoded`)

## 🖼️ Screenshot-Beschreibungen

Das Projekt präsentiert:
- Moderner Header mit Gradient-Text
- 5-spaltige Artikel-Grid mit Bildern
- Tab-Navigation mit animierten Underlines
- Suchfeld mit Fokus-Animation
- Article-Cards mit Hover-Effekten
- Light/Dark Theme Toggle oben rechts
- Responsive Layout auf mobilen Geräten

## 🚢 Deployment

### Mit Docker
```dockerfile
FROM python:3.12
WORKDIR /app
COPY requirements.txt .
RUN pip install -r requirements.txt
COPY . .
CMD ["python", "app.py"]
```

### Mit Gunicorn (Production)
```bash
pip install gunicorn
gunicorn -w 4 -b 0.0.0.0:8080 app:app
```

### Mit Heroku
1. Erstelle `Procfile`:
```
web: gunicorn app:app
```

2. Deploye:
```bash
git push heroku main
```

## 📊 Performance

- **Seitenladezeit**: ~2-3 Sekunden (abhängig von RSS-Feed)
- **Such-Performance**: Instant (<100ms)
- **Kategorie-Wechsel**: 0.6 Sekunden smooth Transition
- **Theme-Umschaltung**: Instant

## 🐛 Bekannte Limitierungen

- RSS-Feeds müssen öffentlich erreichbar sein
- Bildextraktionserfolg hängt von RSS-Feed-Struktur ab
- Manche Feeds können malformed XML enthalten (wird aber gehandhabt)
- Search funktioniert nur mit bereits geladenem Inhalt (keine Backend-Suche)

## 🤝 Beitragen

Contributions sind willkommen! Bitte:

1. Fork das Repository
2. Erstelle einen Feature Branch (`git checkout -b feature/AmazingFeature`)
3. Commit deine Änderungen (`git commit -m 'Add some AmazingFeature'`)
4. Push zum Branch (`git push origin feature/AmazingFeature`)
5. Öffne einen Pull Request

## 📝 Lizenz

Dieses Projekt ist unter der MIT-Lizenz lizenziert - siehe [LICENSE](LICENSE) Datei für Details.

## 👤 Autor

Erstellt mit ❤️ für Nachrichten-Aggregation

## 🙏 Danksagungen

- [Kronen Zeitung](https://www.krone.at/) für die öffentlichen RSS-Feeds
- [Flask](https://flask.palletsprojects.com/) für das Web-Framework
- [lxml](https://lxml.de/) für robustes XML-Parsing

## 📧 Support

Bei Fragen oder Problemen:
1. Überprüfe [CLAUDE.md](CLAUDE.md) für technische Details
2. Öffne ein [GitHub Issue](https://github.com/yourusername/RSS-Aggregator/issues)
3. Kontaktiere den Autor

## 🗺️ Roadmap

- [ ] Artikel-Favoriten speichern
- [ ] Kategorie-Filter anpassen
- [ ] Export zu verschiedenen Formaten (PDF, JSON)
- [ ] Backend-Suche mit Elasticsearch
- [ ] Mehrsprachige Unterstützung
- [ ] Mobile App (React Native)
- [ ] Artikel-Benachrichtigungen

---

**Viel Spaß mit dem RSS Aggregator! 📰✨**
