import feedparser

def parse_feed(url):
    try:
        feed = feedparser.parse(url)
        print(f"Titre: {feed.feed.get('title', 'No title')}")
        for entry in feed.entries[:3]:
            print(f"- {entry.get('title', 'N/A')}")
    except Exception as e:
        print(f"Erreur parsing {url}: {e}")

test_url = 'https://flux.saynete.com/encart_rss_informatique_cybersecurite_fr.xml'
parse_feed(test_url)