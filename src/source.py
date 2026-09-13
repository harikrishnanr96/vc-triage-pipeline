"""Parse cached Launch HN stories into ranked candidate rows."""

import io
import json
import os
import re

RUN_DIR = os.environ.get("RUN_DIR", ".")  # set by run.py for topic runs
CACHE_PATH = os.path.join(RUN_DIR, "cache", "hn_raw.json")
OUTPUT_PATH = os.path.join(RUN_DIR, "data", "candidates.jsonl")
TOP_N = int(os.environ.get("TOP_N") or 10)

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
        # No "(YC ...)" in the title, e.g. "Launch HN: Freestyle - Sandboxes for Coding Agents".
        rest = re.sub(r"^Launch HN:\s*", "", title)
        parts = re.split(r"\s+[–—-]\s+", rest, maxsplit=1)
        return parts[0].strip(), None, (parts[1].strip() if len(parts) > 1 else "")
    name = match.group("name")
    batch = match.group("batch")
    tagline = LEADING_SEP_RE.sub("", match.group("tagline")).strip()
    return name, batch, tagline


with io.open(CACHE_PATH, encoding="utf-8") as handle:
    payload = json.load(handle)

rows = []
for hit in payload.get("hits", []):
    # A topic search matches post text, so skip anything that isn't itself a launch.
    if not (hit.get("title") or "").startswith("Launch HN"):
        continue
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
if len(top) < TOP_N:
    print("WARNING: only {} Launch HN posts matched, fewer than the {} asked for. "
          "Try a broader topic or a longer window (--days).".format(len(top), TOP_N))
for row in top:
    print("{:>4} pts  {:<20.20} {:<6} {}".format(
        row["points"], row["name"], row["yc_batch"] or "-", row["site_url"] or "(no site)"))
