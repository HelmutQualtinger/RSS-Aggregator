from flask import Flask, render_template, jsonify
import requests
from datetime import datetime
import re

try:
    import xml.etree.ElementTree as ET
except ImportError:
    import ElementTree as ET

try:
    from lxml import etree as lxml_etree
    HAS_LXML = True
except ImportError:
    HAS_LXML = False

app = Flask(__name__)

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

def parse_rss_feed():
    """Fetch and parse all RSS feeds"""
    all_articles = []
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }

    for category_name, feed_url in RSS_FEEDS.items():
        try:
            response = requests.get(feed_url, headers=headers, timeout=10)
            response.raise_for_status()

            articles = parse_single_feed(response.content, response.text, category_name)
            # Force all articles from this feed to have the correct category
            for article in articles:
                article['category'] = category_name
            all_articles.extend(articles)
        except Exception as e:
            print("Error fetching {}: {}".format(category_name, str(e)))
            continue

    return all_articles, None

def parse_single_feed(feed_content, feed_text, category_name):
    """Fetch and parse single RSS feed"""
    try:
        articles = []

        # Try lxml first (more forgiving with malformed XML)
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

                    title = title_elem.text if title_elem is not None else 'Ohne Titel'
                    link = link_elem.text if link_elem is not None else '#'
                    description = desc_elem.text if desc_elem is not None else ''
                    full_content = content_elem.text if content_elem is not None else description
                    pub_date = date_elem.text if date_elem is not None else ''

                    # Extract image from description
                    image_url = extract_image(description)

                    # Try to find image in media:content
                    if not image_url:
                        media_elem = item.find('.//{http://search.yahoo.com/mrss/}content')
                        if media_elem is not None:
                            image_url = media_elem.get('url')

                    # Try to find image in media:thumbnail
                    if not image_url:
                        thumb_elem = item.find('.//{http://search.yahoo.com/mrss/}thumbnail')
                        if thumb_elem is not None:
                            image_url = thumb_elem.get('url')

                    # Try to find image in enclosure
                    if not image_url:
                        enclosure_elem = item.find('enclosure')
                        if enclosure_elem is not None:
                            enc_url = enclosure_elem.get('url')
                            if enc_url and enc_url.lower().endswith(('.jpg', '.jpeg', '.png', '.gif', '.webp')):
                                image_url = enc_url

                    # Clean description
                    clean_desc = clean_html(description)[:150]

                    # Clean full content for search indexing
                    clean_full_content = clean_html(full_content)

                    # Format date
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
                # Fall back to regex parsing
                pass

        # Fallback: Use regex-based parsing for malformed XML
        articles = parse_rss_with_regex(feed_text, category_name)
        return articles

    except Exception as e:
        return []

def parse_rss_with_regex(xml_text, category_name):
    """Parse RSS feed using regex as fallback for malformed XML"""
    articles = []

    # Extract all item blocks
    item_pattern = r'<item>.*?</item>'
    items = re.findall(item_pattern, xml_text, re.DOTALL)

    for item in items:
        # Extract fields using regex
        title_match = re.search(r'<title[^>]*>([^<]+)</title>', item)
        link_match = re.search(r'<link[^>]*>([^<]+)</link>', item)
        desc_match = re.search(r'<description[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</description>', item, re.DOTALL)
        date_match = re.search(r'<pubDate[^>]*>([^<]+)</pubDate>', item)
        content_match = re.search(r'<content:encoded[^>]*>([^<]*(?:<[^>]+>[^<]*)*)</content:encoded>', item, re.DOTALL)

        title = title_match.group(1) if title_match else 'Ohne Titel'
        link = link_match.group(1) if link_match else '#'
        description = desc_match.group(1) if desc_match else ''
        full_content = content_match.group(1) if content_match else description
        pub_date = date_match.group(1) if date_match else ''

        # Extract image from description first
        image_url = extract_image(description)

        # Try to find image in media:content
        if not image_url:
            media_match = re.search(r'<media:content[^>]+url=["\']?([^"\'\s>]+)', item)
            if media_match:
                image_url = media_match.group(1)

        # Try to find image in media:thumbnail
        if not image_url:
            thumbnail_match = re.search(r'<media:thumbnail[^>]+url=["\']?([^"\'\s>]+)', item)
            if thumbnail_match:
                image_url = thumbnail_match.group(1)

        # Try to find image in enclosure
        if not image_url:
            enclosure_match = re.search(r'<enclosure[^>]+url=["\']?([^"\'\s>]+\.(?:jpg|jpeg|png|gif|webp))', item, re.IGNORECASE)
            if enclosure_match:
                image_url = enclosure_match.group(1)

        # Try to find image element
        if not image_url:
            image_match = re.search(r'<image[^>]*>.*?<url>([^<]+)</url>', item, re.DOTALL)
            if image_match:
                image_url = image_match.group(1)

        # Clean description
        clean_desc = clean_html(description)[:150]

        # Clean full content for search indexing
        clean_full_content = clean_html(full_content)

        # Format date
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
    if not html_content:
        return None

    # Look for img tag with src attribute (various formats)
    patterns = [
        r'<img[^>]+src=["\']?([^"\'\s>]+)',  # src with or without quotes
        r'<img[^>]+src="([^"]+)"',  # img with quoted src
        r'https?://[^\s<>"]+\.(?:jpg|jpeg|png|gif|webp)',  # Direct URL in content
        r'<figure[^>]*>.*?<img[^>]+src=["\']?([^"\'\s>]+)',  # img in figure
    ]

    for pattern in patterns:
        match = re.search(pattern, html_content, re.IGNORECASE | re.DOTALL)
        if match:
            url = match.group(1) if match.lastindex else match.group(0)
            if url and url.startswith(('http://', 'https://', '//')):
                return url

    return None

def clean_html(html_content):
    """Remove HTML tags from content"""
    if not html_content:
        return ""

    # Remove HTML tags
    clean = re.sub(r'<[^>]+>', '', html_content)
    # Decode HTML entities
    clean = clean.replace('&amp;', '&').replace('&lt;', '<').replace('&gt;', '>')
    clean = clean.replace('&quot;', '"').replace('&#39;', "'")

    return clean.strip()

def format_date(date_string):
    """Format RFC 2822 date to readable format"""
    if not date_string:
        return ""

    try:
        # Parse RFC 2822 format
        dt = datetime.strptime(date_string, '%a, %d %b %Y %H:%M:%S %z')
        return dt.strftime('%d. %B %Y, %H:%M')
    except:
        return date_string

@app.route('/')
def index():
    """Render the main page"""
    articles, error = parse_rss_feed()

    # Initialize categories dict with all feed categories
    categories = {}
    for cat_name in RSS_FEEDS.keys():
        categories[cat_name] = []

    # Group articles by category and limit to 20 per category
    for article in articles:
        cat = article.get('category', 'Top-News')
        if cat in categories and len(categories[cat]) < 20:
            categories[cat].append(article)

    # Sort categories in custom order
    category_order = ['Top-News', 'Politik', 'Sport', 'Wirtschaft', 'Österreich', 'Welt', 'Wissenschaft', 'Wetter']
    sorted_categories = []
    for cat_name in category_order:
        if cat_name in categories:
            sorted_categories.append((cat_name, categories[cat_name]))

    return render_template('index.html', categories=sorted_categories, error=error, articles=articles)

@app.route('/api/articles')
def get_articles():
    """API endpoint for articles"""
    articles, error = parse_rss_feed()
    return jsonify({
        'articles': articles,
        'error': error,
        'count': len(articles)
    })

if __name__ == '__main__':
    app.run(debug=True, port=8080)
