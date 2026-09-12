"""Fetch recent Launch HN stories from the HN Algolia API and print them."""

import json
import os
import time

import requests

API_URL = "http://hn.algolia.com/api/v1/search_by_date"
CACHE_PATH = os.path.join("cache", "hn_raw.json")
DAYS = 90

cutoff = int(time.time()) - DAYS * 24 * 60 * 60

params = {
    "tags": "story",
    "query": '"Launch HN"',
    "numericFilters": "created_at_i>{}".format(cutoff),
    "hitsPerPage": 50,
    # Phrase-quoted query plus title-only search: without both, Algolia's loose
    # full-text match pulls in any story with "launch" in its title or URL.
    "restrictSearchableAttributes": "title",
}

response = requests.get(API_URL, params=params, timeout=30)
response.raise_for_status()
payload = response.json()

os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
with open(CACHE_PATH, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, ensure_ascii=False)

hits = payload.get("hits", [])
print("{} stories since {}\n".format(len(hits), time.strftime("%Y-%m-%d", time.localtime(cutoff))))

for hit in hits:
    title = hit.get("title") or "(no title)"
    points = hit.get("points") or 0
    num_comments = hit.get("num_comments") or 0
    url = hit.get("url") or "https://news.ycombinator.com/item?id={}".format(hit.get("objectID"))
    print("{:<60.60}  {:>4} pts  {:>4} cmts  {}".format(title, points, num_comments, url))
