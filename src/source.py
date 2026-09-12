"""Parse cached Launch HN stories into ranked candidate rows."""

import io
import json
import os
import re

CACHE_PATH = os.path.join("cache", "hn_raw.json")
OUTPUT_PATH = os.path.join("data", "candidates.jsonl")
TOP_N = 10

# "Launch HN: Bullet (YC S26) - A Faster Coding Agent"
#             ^^^^^^  ^^^^^^^^   ^^^^^^^^^^^^^^^^^^^
TITLE_RE = re.compile(
    r"^Launch HN:\s*(?P<name>.+?)\s*\(YC\s*(?P<batch>[A-Z]\d{2})\)\s*(?P<tagline>.*)$"
)

# Separator between company and tagline varies: en dash, em dash, hyphen, colon,
# or nothing at all ("ProvenMetal (YC S26) delivers circuit boards in days").
LEADING_SEP_RE = re.compile(r"^[\s–—:-]+")


def parse_title(title):
    match = TITLE_RE.match(title)
    if not match:
        return title.replace("Launch HN:", "").strip(), None, ""
    name = match.group("name")
    batch = match.group("batch")
    tagline = LEADING_SEP_RE.sub("", match.group("tagline")).strip()
    return name, batch, tagline


with io.open(CACHE_PATH, encoding="utf-8") as handle:
    payload = json.load(handle)

rows = []
for hit in payload.get("hits", []):
    name, batch, tagline = parse_title(hit.get("title") or "")

    # Text-only launches have no url key; anything pointing back at HN is not a
    # company site either. Both become null, and the row is kept regardless.
    site_url = hit.get("url") or None
    if site_url and "news.ycombinator.com" in site_url:
        site_url = None

    rows.append({
        "name": name,
        "yc_batch": batch,
        "tagline": tagline,
        "hn_url": "https://news.ycombinator.com/item?id={}".format(hit.get("objectID")),
        "site_url": site_url,
        "points": hit.get("points") or 0,
        "num_comments": hit.get("num_comments") or 0,
        "created_at": hit.get("created_at"),
    })

rows.sort(key=lambda row: row["points"], reverse=True)
top = rows[:TOP_N]

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with io.open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
    for row in top:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

print("wrote {} rows to {}".format(len(top), OUTPUT_PATH))
for row in top:
    print("{:>4} pts  {:<20.20} {:<6} {}".format(
        row["points"], row["name"], row["yc_batch"] or "-", row["site_url"] or "(no site)"))
