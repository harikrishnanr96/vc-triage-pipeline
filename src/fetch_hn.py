"""Fetch Launch HN stories from the HN Algolia API, optionally narrowed to a topic."""

import json
import os
import time

import requests

API_URL = "http://hn.algolia.com/api/v1/search_by_date"
RUN_DIR = os.environ.get("RUN_DIR", ".")  # set by run.py for topic runs
CACHE_PATH = os.path.join(RUN_DIR, "cache", "hn_raw.json")
TOPIC = os.environ.get("TOPIC", "").strip()

# Launch HN averages a couple of posts a week, so a topic search needs a longer
# window than the default run to find enough matches.
DAYS = int(os.environ.get("DAYS") or (365 if TOPIC else 90))

cutoff = int(time.time()) - DAYS * 24 * 60 * 60

if TOPIC:
    # Every topic word must appear in the title or the launch post text. The
    # match is loose (a post that mentions "testing" in passing counts); the
    # thesis rules in the analysis stage do the real filtering.
    params = {
        "tags": "story",
        "query": '"Launch HN" {}'.format(TOPIC),
        "numericFilters": "created_at_i>{}".format(cutoff),
        "hitsPerPage": 1000,
        "restrictSearchableAttributes": "title,story_text",
    }
else:
    params = {
        "tags": "story",
        "query": '"Launch HN"',
        "numericFilters": "created_at_i>{}".format(cutoff),
        "hitsPerPage": 50,
        # Phrase-quoted query plus title-only search: without both, Algolia's loose
        # full-text match pulls in any story with "launch" in its title or URL.
        "restrictSearchableAttributes": "title",
    }

response = requests.get(API_URL, params=params, timeout=60)
response.raise_for_status()
payload = response.json()
payload["query_params"] = params  # so the raw file records how it was fetched

os.makedirs(os.path.dirname(CACHE_PATH), exist_ok=True)
with open(CACHE_PATH, "w", encoding="utf-8") as handle:
    json.dump(payload, handle, indent=2, ensure_ascii=False)

hits = payload.get("hits", [])
print("{} stories since {}{}\n".format(
    len(hits), time.strftime("%Y-%m-%d", time.localtime(cutoff)),
    ' matching "{}"'.format(TOPIC) if TOPIC else ""))

for hit in hits:
    title = hit.get("title") or "(no title)"
    points = hit.get("points") or 0
    num_comments = hit.get("num_comments") or 0
    url = hit.get("url") or "https://news.ycombinator.com/item?id={}".format(hit.get("objectID"))
    print("{:<60.60}  {:>4} pts  {:>4} cmts  {}".format(title, points, num_comments, url))
