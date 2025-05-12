import feedparser
import aiohttp
import asyncio
import logging
import time

KEYWORDS_FILE = 'mots_cles.txt'
RESULT_FILE = 'resultat.txt'
logging.basicConfig(level=logging.INFO)

def load_urls(path='rss_list.txt'):
    with open(path, 'r', encoding='utf-8') as f:
        return [line.strip() for line in f if line.strip()]

def load_keywords(path=KEYWORDS_FILE):
    with open(path, 'r', encoding='utf-8') as f:
        return [kw.strip().lower() for kw in f if kw.strip()]

async def fetch_feed(session, url):
    try:
        async with session.get(url) as response:
            content = await response.read()
            return content
    except Exception as e:
        print(f"Erreur sur {url}: {e}")
        return None

def parse_feed_entries(content):
    feed = feedparser.parse(content)
    articles = []
    for entry in feed.entries:
        articles.append({
            'title': entry.get('title', 'N/A'),
            'summary': entry.get('summary', ''),
            'link': entry.get('link', 'N/A'),
            'published': entry.get('published', 'N/A')
        })
    return articles

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

async def process_url(session, url, keywords):
    content = await fetch_feed(session, url)
    if content is None:
        return []
    articles = parse_feed_entries(content)
    return filter_articles(articles, keywords)

async def main():
    start = time.time()
    urls = load_urls()
    keywords = load_keywords()
    results = []

    async with aiohttp.ClientSession() as session:
        tasks = [process_url(session, url, keywords) for url in urls]
        responses = await asyncio.gather(*tasks, return_exceptions=True)

        for url, res in zip(urls, responses):
            if isinstance(res, Exception):
                logging.error(f"Erreur sur {url}: {res}")
            else:
                results.extend(res)

    with open(RESULT_FILE, 'w', encoding='utf-8') as out:
        for m in results:
            out.write(f"{m['title']} | {m['published']} | {m['link']} | {m['keyword']}\n")

    elapsed = time.time() - start
    print(f"Completer en {elapsed:.2f}s")


asyncio.run(main())


