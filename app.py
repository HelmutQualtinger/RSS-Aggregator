from fastapi import FastAPI
from fastapi.responses import HTMLResponse, Response
from fastapi.templating import Jinja2Templates
from fastapi.staticfiles import StaticFiles
from starlette.requests import Request
import os
import requests
from datetime import datetime
import re
import schedule
import time
import threading

try:
    import xml.etree.ElementTree as ET
except ImportError:
    import ElementTree as ET

try:
    from lxml import etree as lxml_etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False

app = FastAPI(title="RSS Aggregator", version="1.0.0")
templates = Jinja2Templates(directory="templates")

# Mount static files directory
if os.path.exists("static"):
    app.mount("/static", StaticFiles(directory="static"), name="static")

# Multiple RSS feeds for different categories
RSS_FEEDS = {
    'Top-News': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=2311992',
    'Sport': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=989',
    'Wirtschaft': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=136',
    'Politik': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=305',
    'Österreich': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=102',
    'Welt': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=90',
    'Wissenschaft': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=350',
    'Wetter': 'https://api.krone.at/v1/rss/rssfeed-google.xml?id=1789989',
}

# Global variable to store the latest fetched articles
latest_articles_data = {"articles": [], "error": None, "last_updated": None}
articles_lock = threading.Lock() # To ensure thread-safe access to latest_articles_data

def parse_rss_feed_logic():
    """Fetch and parse all RSS feeds. This is the core logic."""
    all_articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    fetch_errors = []

    for category_name, feed_url in RSS_FEEDS.items():
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()

            articles = parse_single_feed(response.content, response.text, category_name)
            for article in articles:
                article['category'] = category_name
            all_articles.extend(articles)
        except Exception as e:
            print(f"Error fetching {category_name}: {str(e)}")
            fetch_errors.append(f"{category_name}: {str(e)}")
            continue
    
    if fetch_errors:
        return all_articles, ", ".join(fetch_errors)
    else:
        return all_articles, None

def refresh_feeds():
    """Fetches and parses RSS feeds, then updates the global cache."""
    print("Refreshing RSS feeds...")
    articles, error = parse_rss_feed_logic()
    with articles_lock:
        latest_articles_data["articles"] = articles
        latest_articles_data["error"] = error
        latest_articles_data["last_updated"] = datetime.now().isoformat()
    print(f"Feeds refreshed. Found {len(articles)} articles. Errors: {error}")

# --- Existing parsing functions (parse_single_feed, extract_image, clean_html, format_date, parse_rss_with_regex) remain the same ---
def parse_single_feed(feed_content, feed_text, category_name):
    """Fetch and parse single RSS feed"""
    articles = []
    try:
        if HAS_LXML:
            try:
                parser = lxml_etree.XMLParser(recover=True)
                root = lxml_etree.fromstring(feed_content, parser=parser)
                items = root.findall('.//item')

                for item in items:
                    title_elem = item.find('title')
                    link_elem = item.find('link')
                    desc_elem = item.find('description')
                    date_elem = item.find('pubDate')
                    content_elem = item.find('.//{http://purl.org/rss/1.0/modules/content/}encoded')

                    title = (title_elem.text or '').strip() if title_elem is not None else 'Ohne Titel'
                    link = (link_elem.text or '').strip() if link_elem is not None else '#'
                    description = desc_elem.text if desc_elem is not None else ''
                    full_content = content_elem.text if content_elem is not None else description
                    pub_date = date_elem.text if date_elem is not None else ''

                    image_url = extract_image(description)
                    if not image_url:
                        media_elem = item.find('.//{http://search.yahoo.com/mrss/}content')
                        if media_elem is not None:
                            image_url = media_elem.get('url')
                    if not image_url:
                        thumb_elem = item.find('.//{http://search.yahoo.com/mrss/}thumbnail')
                        if thumb_elem is not None:
                            image_url = thumb_elem.get('url')
                    if not image_url:
                        enclosure_elem = item.find('enclosure')
                        if enclosure_elem is not None:
                            enc_url = enclosure_elem.get('url')
                            if enc_url and enc_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                                image_url = enc_url

                    clean_desc = clean_html(description)[:150]
                    clean_full_content = clean_html(full_content)
                    formatted_date = format_date(pub_date)

                    articles.append({
                        'title': title if title else 'Ohne Titel',
                        'link': link if link else '#',
                        'description': clean_desc,
                        'full_content': clean_full_content,
                        'image': image_url,
                        'date': formatted_date,
                        'pub_date_raw': pub_date,
                        'category': category_name
                    })
                return articles
            except Exception as lxml_error:
                pass # Fallback to regex

        articles = parse_rss_with_regex(feed_text, category_name)
        return articles
    except Exception as e:
        print(f"Error parsing single feed: {e}")
        return []

def parse_rss_with_regex(xml_text, category_name):
    """Parse RSS feed using regex as fallback for malformed XML"""
    articles = []
    item_pattern = r'<item>.*?</item>'
    items = re.findall(item_pattern, xml_text, re.DOTALL)

    for item in items:
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', item)
        link_match = re.search(r'<link[^>]*>([^<]+)</link>', item)
        desc_match = re.search(r'<description[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</description>', item, re.DOTALL)
        date_match = re.search(r'<pubDate[^>]*>([^<]+)</pubDate>', item)
        content_match = re.search(r'<content:encoded[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</content:encoded>', item, re.DOTALL)

        title = (title_match.group(1) if title_match else 'Ohne Titel').strip()
        link = (link_match.group(1) if link_match else '#').strip()
        description = desc_match.group(1) if desc_match else ''
        full_content = content_match.group(1) if content_match else description
        pub_date = date_match.group(1) if date_match else ''

        image_url = extract_image(description)
        if not image_url:
            # Corrected regex: changed [^"\'s>] to [^"'\s>]
            media_match = re.search(r'<media:content[^>]+url=["\"]?([^"\'\s>]+)', item)
            if media_match:
                image_url = media_match.group(1)

        if not image_url:
            thumbnail_match = re.search(r'<media:thumbnail[^>]+url=["\"]?([^"\'\s>]+)', item)
            if thumbnail_match:
                image_url = thumbnail_match.group(1)

        if not image_url:
            enclosure_match = re.search(r'<enclosure[^>]+url=["\"]?([^"\'\s>]+\.(?:jpg|jpeg|png|gif|webp))', item, re.IGNORECASE)
            if enclosure_match:
                image_url = enclosure_match.group(1)
        
        if not image_url:
            # Added check for <image><url>...</url> pattern
            image_tag_match = re.search(r'<image[^>]*>.*?<url>([^<]+)</url>', item, re.DOTALL)
            if image_tag_match:
                image_url = image_tag_match.group(1)


        clean_desc = clean_html(description)[:150]
        clean_full_content = clean_html(full_content)
        formatted_date = format_date(pub_date)

        articles.append({
            'title': title,
            'link': link,
            'description': clean_desc,
            'full_content': clean_full_content,
            'image': image_url,
            'date': formatted_date,
            'pub_date_raw': pub_date,
            'category': category_name
        })
    return articles

def extract_image(html_content):
    """Extract image URL from HTML content"""
    if not html_content: return None
    patterns = [
        r'<img[^>]+src=["\"]?([^"\'\s>]+)', r'<img[^>]+src=["\"]([^"\"]+)"["\"]',
        r'https?://[^\s<>"\"]+\.(?:jpg|jpeg|png|gif|webp)',
        r'<figure[^>]*>.*?<img[^>]+src=["\"]?([^"\'\s>]+)',
    ]
    for pattern in patterns:
        match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if match:
            url = match.group(1) if match.lastindex else match.group(0)
            if url and url.startswith(('http://', 'https://', '//')): return url
    return None

def clean_html(html_content):
    """Remove HTML tags from content"""
    if not html_content: return ""
    clean = re.sub(r'<[^>]+>', '', html_content)
    clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>').replace('&quot;', '"').replace('&#39;', "'")
    return clean.strip()

def format_date(date_string):
    """Format RFC 2822 date to readable format"""
    if not date_string: return ""
    try:
        dt = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%d. %B %Y, %H:%M')
    except: return date_string
# --- End of existing parsing functions ---


@app.get("/", response_class=HTMLResponse)
async def index(request: Request):
    """Render the main page using cached data."""
    with articles_lock:
        articles_data = latest_articles_data.copy()

    # Group articles by category and limit to 20 per category
    categories = {}
    for cat_name in RSS_FEEDS.keys():
        categories[cat_name] = []

    for article in articles_data["articles"]:
        cat = article.get('category', 'Top-News')
        if cat in categories and len(categories[cat]) < 20:
            categories[cat].append(article)

    # Sort categories in custom order
    category_order = ['Top-News', 'Politik', 'Sport', 'Wirtschaft', 'Österreich', 'Welt', 'Wissenschaft', 'Wetter']
    sorted_categories = []
    for cat_name in category_order:
        if cat_name in categories and categories[cat_name]: # Only include categories with articles
            sorted_categories.append((cat_name, categories[cat_name]))

    return templates.TemplateResponse(
        "index.html",
        {
            "request": request,
            "categories": sorted_categories,
            "error": articles_data["error"],
            "articles": articles_data["articles"]
        }
    )

@app.get("/api/articles")
async def get_articles():
    """API endpoint for articles using cached data."""
    with articles_lock:
        articles_data = latest_articles_data.copy()

    return {
        'articles': articles_data['articles'],
        'error': articles_data['error'],
        'count': len(articles_data['articles']),
        'last_updated': articles_data['last_updated']
    }

@app.get("/api/image")
async def get_image(url: str):
    """Proxy endpoint for images to bypass CORS issues."""
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
        }
        response = requests.get(url, headers=headers, timeout=10)
        response.raise_for_status()

        return Response(
            content=response.content,
            media_type=response.headers.get('content-type', 'image/jpeg'),
            headers={'Cache-Control': 'public, max-age=86400'}
        )
    except Exception as e:
        print(f"Error fetching image from {url}: {str(e)}")
        return Response(status_code=404, content=b'')


def run_scheduler_loop():
    """Background loop for scheduler."""
    while True:
        schedule.run_pending()
        time.sleep(60) # Check every minute

@app.on_event("startup")
async def startup_event():
    """Initialize feeds and start background scheduler on app startup."""
    print("Starting RSS Aggregator...")
    # Initial fetch of feeds
    refresh_feeds()

    # Setup and start the scheduler
    schedule.every(10).minutes.do(refresh_feeds)
    scheduler_thread = threading.Thread(target=run_scheduler_loop, daemon=True)
    scheduler_thread.start()
    print("Scheduler started. Next refresh in 10 minutes.")

if __name__ == '__main__':
    import uvicorn
    # Run the FastAPI app (only in development)
    # Use host='0.0.0.0' and port=8080 to match Docker container settings
    uvicorn.run(app, host='0.0.0.0', port=8080)
