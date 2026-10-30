"""Find fresh topics in your niche from Google News RSS (no API key needed)."""
from urllib.parse import urlencode

import feedparser


def find_topics(keywords: list[str], per_keyword: int = 5) -> list[dict]:
    topics, seen = [], set()
    for kw in keywords:
        url = "https://news.google.com/rss/search?" + urlencode(
            {"q": f"{kw} when:1d", "hl": "en-IN", "gl": "IN", "ceid": "IN:en"}
        )
        feed = feedparser.parse(url)
        for entry in feed.entries[:per_keyword]:
            link = entry.get("link")
            if not link or link in seen:
                continue
            seen.add(link)
            topics.append({"title": entry.get("title", "").strip(), "link": link, "keyword": kw})
    return topics
