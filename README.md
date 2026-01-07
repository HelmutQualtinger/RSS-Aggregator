# 📰 RSS Aggregator - Kronen Zeitung

Ein modernes, interaktives Webanwendung zur Anzeige von RSS-Feeds der Kronen Zeitung (österreichische Zeitung) mit fortgeschrittenen Funktionen wie Live-Suche, Light/Dark Theme und dynamischen Kategorie-Farben.

![Python Version](https://img.shields.io/badge/python-3.9+-blue.svg)
![FastAPI Version](https://img.shields.io/badge/fastapi-0.109.0-green.svg)
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
fastapi==0.109.0      # Modern ASGI Web Framework
uvicorn==0.25.0       # ASGI Server
requests==2.31.0      # HTTP Library
schedule==1.2.2       # Background Task Scheduler
jinja2==3.1.3         # Template Engine
lxml==6.0.2           # XML Parser
```

## 🏗️ Projektstruktur

```
RSS-Aggregator/
├── app.py                    # FastAPI Backend (RSS-Parsing, API, Scheduling)
├── requirements.txt          # Python Dependencies
├── Dockerfile               # Multi-stage Docker build configuration
├── docker-compose.yml       # Docker Compose for container orchestration
├── templates/
│   └── index.html           # Frontend (Tailwind CSS + Vanilla JS)
├── static/
│   └── style.css            # Custom styles (animations, dark mode, gradients)
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
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)  # PORT hier ändern
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

### Tailwind CSS + Custom CSS

Das Projekt verwendet eine Kombination aus:
- **Tailwind CSS CDN** - Utility-first CSS Framework für responsive Design
- **Custom CSS (`static/style.css`)** - Für komplexe Animationen, Gradienten und Dark Mode Styling

#### Tailwind Konfiguration
```javascript
tailwind.config = {
    darkMode: 'class',  // Dark mode aktiviert durch 'dark' Klasse auf <html>
    theme: {
        extend: {
            backdropBlur: {
                xs: '2px'  // Custom backdrop blur value
            }
        }
    }
}
```

#### CSS Custom Properties (in style.css)

```css
--bg-light              /* Light Mode Background Gradient */
--bg-dark               /* Dark Mode Background Gradient */
--category-color        /* Aktive Kategorie-Farbe */
--text-dark-mode        /* Dark Mode Text Color (#ffffff) */
--text-secondary-dark   /* Dark Mode Secondary Text (#b0b0b0) */
--card-dark             /* Dark Mode Card Background */
--border-dark           /* Dark Mode Border Color */
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

### Mit Docker (Recommended)
```bash
# Build und starte mit Docker Compose
docker-compose up --build -d

# Oder mit einzelnem Docker-Befehl
docker build -t rss-aggregator .
docker run -p 8080:8080 rss-aggregator
```

Das Projekt verwendet **Multi-Stage Docker Build** für optimale Image-Größe:
- Stage 1 (Builder): Installiert alle Dependencies
- Stage 2 (Runtime): Kopiert nur notwendige Packages
- Result: ~250MB statt 600MB+ Image

### Mit Uvicorn (Production)
```bash
# Starte mit Uvicorn direkt
uvicorn app:app --host 0.0.0.0 --port 8080

# Mit mehreren Workers (Single Worker empfohlen für In-Memory Cache)
uvicorn app:app --host 0.0.0.0 --port 8080 --workers 1
```

### Mit Docker Compose + Reverse Proxy
```bash
# Externe reverse-proxy Network erstellen
docker network create reverse-proxy

# Container in reverse-proxy Network starten
docker-compose up -d
```

Der Container verbindet sich mit der externen `reverse-proxy` Netzwerk:
- Hostname: `rss-aggregator`
- Port: `8080`
- Erreichbar von anderen Containern im Netzwerk

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
- [FastAPI](https://fastapi.tiangolo.com/) für das moderne ASGI Web-Framework
- [Uvicorn](https://www.uvicorn.org/) für den ASGI Server
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
