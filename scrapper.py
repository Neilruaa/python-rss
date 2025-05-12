import feedparser

def parse_feed(url):
    try:
        feed = feedparser.parse(url)
        print(f"Titre: {feed.feed.get('title', 'No title')}")
        for entry in feed.entries[:3]:
            print(f"- {entry.get('title', 'N/A')}")
    except Exception as e:
        print(f"Erreur parsing {url}: {e}")

def load_urls(path='rss_list.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

urls = load_urls()
for url in urls[:10]:
    print(f"Parsing {url}")
    parse_feed(url)