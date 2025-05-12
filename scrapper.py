import feedparser

KEYWORDS_FILE = 'mots_cles.txt'
RESULT_FILE = 'resultat.txt'

def load_urls(path='rss_list.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_keywords(path=KEYWORDS_FILE):
    with open(path, 'r', encoding='utf-8') as f:
        return [kw.strip().lower() for kw in f if kw.strip()]

def parse_feed_entries(url):
    try:
        feed = feedparser.parse(url)
        articles = []
        for entry in feed.entries:
            articles.append({
                'title': entry.get('title', 'N/A'),
                'summary': entry.get('summary', ''),
                'link': entry.get('link', 'N/A'),
                'published': entry.get('published', 'N/A')
            })
        return articles
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return []

def filter_articles(articles, keywords):
    filtered = []
    for art in articles:
        text = (art['title'] + ' ' + art['summary']).lower()
        for kw in keywords:
            if kw in text:
                art['keyword'] = kw
                filtered.append(art)
                break
    return filtered

def process_url(url, keywords):
    articles = parse_feed_entries(url)
    return filter_articles(articles, keywords)

urls = load_urls()
keywords = load_keywords()
with open(RESULT_FILE, 'w', encoding='utf-8') as out:
    for url in urls[:5]:
        entries = parse_feed_entries(url)
        matches = filter_articles(entries, keywords)
        for m in matches:
            line = f"{m['title']} | {m['published']} | {m['link']} | {m['keyword']}\n"
            out.write(line)
            print(line, end='')