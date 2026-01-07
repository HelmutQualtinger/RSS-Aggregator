# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

RSS Aggregator for Kronen Zeitung (Austrian newspaper) - A FastAPI-based web application that fetches and displays RSS feeds from multiple news categories in an interactive, modern web interface with Light/Dark theme support.

## Architecture

### Backend (FastAPI + Uvicorn)
- **app.py**: Single FastAPI application file containing:
  - RSS feed fetching and parsing logic
  - Multi-parser support: lxml (preferred) with fallback to regex-based parsing for malformed XML
  - Article extraction from multiple Kronen Zeitung RSS feeds (8 categories)
  - Full content extraction (`content:encoded` elements) for search indexing
  - Image extraction from multiple sources (description HTML, media:content, media:thumbnail, enclosures)
  - HTML cleaning and date formatting utilities
  - Background scheduler: Runs `refresh_feeds()` every 10 minutes via `@app.on_event("startup")`
  - Two main routes:
    - `GET /`: Renders main page with articles grouped and limited (max 20 per category)
    - `GET /api/articles`: JSON API endpoint
  - Auto-generated API documentation at `/docs` (OpenAPI/Swagger)

### Frontend (Jinja2 + Vanilla JS)
- **templates/index.html**: Single HTML file containing:
  - Complete responsive design with CSS (no external stylesheets)
  - Modern glassmorphism UI with backdrop-filter effects
  - Dynamic Light/Dark theme with localStorage persistence
  - Category-specific color schemes (8 unique colors per category)
  - Dynamic background gradient that changes per active category
  - Real-time full-text search across entire article content
  - Smooth animations and transitions (cubic-bezier easing)
  - 5-article responsive grid layout (4 at 1600px, 3 at 1200px, 2 at 800px, 1 at 768px)
  - Tab-based category navigation with animated underlines

## Key Data Flow

1. **Feed Fetching**: `parse_rss_feed()` iterates through `RSS_FEEDS` dict
2. **Parsing**: Each feed is parsed by `parse_single_feed()` (lxml) or fallback `parse_rss_with_regex()`
3. **Content Extraction**:
   - Full content from `content:encoded` element
   - Images from HTML description, media namespaces, or enclosures
   - All HTML tags stripped for clean text display
4. **Categorization**: Articles forced to category matching the feed URL
5. **Limiting**: Frontend receives all articles, backend limits to 20 per category
6. **Frontend Processing**: JavaScript indexes full content in `data-full-text` attributes for search

## RSS Feed Configuration

The application pulls from 8 Kronen Zeitung RSS feeds, each with a unique ID:
- Top-News (2311992), Sport (989), Wirtschaft (136), Politik (305)
- Österreich (102), Welt (90), Wissenschaft (350), Wetter (1789989)

To add/modify feeds, update the `RSS_FEEDS` dictionary in app.py and add corresponding category color in templates/index.html JavaScript.

## Running the Application

### Development
```bash
# Install dependencies
pip3 install -r requirements.txt

# Run development server (port 8080)
python3 app.py
```

Server runs at `http://localhost:8080`. Uvicorn supports auto-reload on file changes.

API documentation available at `http://localhost:8080/docs` (interactive Swagger UI).

### Production (Docker)
```bash
# Build and run with Docker Compose
docker-compose up --build -d

# View logs
docker-compose logs -f rss-aggregator
```

Multi-stage Docker build optimizes image size:
- Stage 1: Build dependencies (~600MB intermediate)
- Stage 2: Runtime only (~250MB final image)

## Development Notes

### Background Scheduler (FastAPI Startup Event)
- **Trigger**: `@app.on_event("startup")` - Runs when application starts
- **Behavior**:
  - Initial RSS feed fetch on startup
  - Background daemon thread starts scheduler loop
  - Scheduler runs `refresh_feeds()` every 10 minutes
  - Scheduler checks every 60 seconds for pending tasks
- **Thread Safety**: Uses `threading.Lock()` to protect shared `latest_articles_data` dict
- **Note**: Single worker recommended (in-memory cache doesn't support multi-worker scenario)

### Data Caching
- **Global Cache**: `latest_articles_data` dictionary with the following structure:
  ```python
  {
    "articles": [...],      # List of all fetched articles
    "error": None,          # Error message if fetch failed
    "last_updated": "ISO8601_TIMESTAMP"
  }
  ```
- **Thread Lock**: `articles_lock` (threading.Lock) protects cache access
- **Scope**: Global in-memory cache (shared across all requests in single process)

### Theming System
- CSS custom properties (--bg-light, --card-light, etc.) control all colors
- Dark theme class added to `<body>` for cascade styling
- Theme preference stored in localStorage under key 'theme'
- Dynamic --category-color updates background gradient on tab clicks

### Search Implementation
- Real-time filtering without API calls (100% frontend)
- Indexes full article text (title + complete content from RSS)
- Case-insensitive matching on each keystroke
- Shows "no results" message when appropriate

### XML Parsing Resilience
- Primary parser: lxml with `recover=True` (handles malformed XML)
- Fallback: Regex-based extraction if lxml fails
- Both parsers extract: title, link, description, pubDate, content:encoded, images
- Images searched in: description HTML, media:content, media:thumbnail, enclosures

### Image Handling
- Extracted from multiple RSS sources (priority order):
  1. HTML img tags in description
  2. media:content elements (MRSS namespace)
  3. media:thumbnail elements
  4. enclosure elements
  5. image element with url child
- Falls back to gradient placeholder if no image found
- Broken images hidden with `onerror` handler

## Browser Compatibility

Uses CSS features:
- backdrop-filter (blur effect)
- CSS custom properties (--variable syntax)
- color-mix() function (for gradient mixing)
- display: grid with auto-fill/repeat
- backdrop-filter blur

Requires modern browser (Chrome 76+, Firefox 94+, Safari 15+).

## Port Configuration

Application runs on port **8080** by default. To change:

### Development
Edit `uvicorn.run()` call at the end of app.py:
```python
if __name__ == '__main__':
    import uvicorn
    uvicorn.run(app, host='0.0.0.0', port=8080)  # Change port here
```

### Docker
Update `docker-compose.yml`:
```yaml
ports:
  - "8080:8080"  # Change first number to desired host port
```

## Reverse Proxy Integration

The container is configured to work with external reverse-proxy networks:

- **Network**: `reverse-proxy` (external, bridge driver)
- **Hostname**: `rss-aggregator` (resolvable within network)
- **Port**: `8080` (internal port)
- **Setup**: Network must be created before container starts:
  ```bash
  docker network create reverse-proxy
  docker-compose up -d
  ```

This allows other containers (nginx, traefik, etc.) to route traffic to `http://rss-aggregator:8080`.
