"""Enrich candidates with HN thread text, site text, and GitHub repo stats."""

import html
import io
import json
import os
import re
import time
from urllib.parse import urlparse

import requests
from dotenv import load_dotenv

load_dotenv()

RUN_DIR = os.environ.get("RUN_DIR", ".")  # set by run.py for topic runs
INPUT_PATH = os.path.join(RUN_DIR, "data", "candidates.jsonl")
OUTPUT_PATH = os.path.join(RUN_DIR, "data", "enriched.jsonl")
CACHE_DIR = os.path.join("cache", "enrich")  # shared across runs
TIMEOUT = 20

HN_ITEM_URL = "https://hn.algolia.com/api/v1/items/{}"
GITHUB_API = "https://api.github.com"

SITE_HEADERS = {
    "User-Agent": "Mozilla/5.0 (vc-triage-pipeline; research script)",
    "Accept": "text/html,application/xhtml+xml",
}

GITHUB_HEADERS = {"Accept": "application/vnd.github+json"}
# Optional: unauthenticated GitHub allows 60 requests/hour, plenty for 10 rows.
if os.environ.get("GITHUB_TOKEN"):
    GITHUB_HEADERS["Authorization"] = "Bearer " + os.environ["GITHUB_TOKEN"]

BLOCK_TAGS = r"p|div|li|ul|ol|h[1-6]|tr|section|article|header|footer|pre|blockquote"


def html_to_text(markup):
    if not markup:
        return ""
    text = re.sub(r"(?is)<(script|style|noscript|svg|template|head)\b.*?</\1\s*>", " ", markup)
    text = re.sub(r"(?s)<!--.*?-->", " ", text)
    text = re.sub(r"(?i)<br\s*/?>|</?(?:" + BLOCK_TAGS + r")\b[^>]*>", "\n", text)
    text = re.sub(r"(?s)<[^>]+>", " ", text)
    text = html.unescape(text)
    text = re.sub(r"[ \t\r\f\v]+", " ", text)
    text = re.sub(r" *\n *", "\n", text)
    text = re.sub(r"\n{3,}", "\n\n", text)
    return text.strip()


def fetch(url, headers=None, params=None, as_json=True):
    """Return a cache entry dict. Never raises: failures land in entry["error"]."""
    entry = {
        "url": url,
        "params": params,
        "fetched_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "status": None,
        "content_type": None,
        "body": None,
        "error": None,
    }
    try:
        response = requests.get(url, headers=headers, params=params, timeout=TIMEOUT)
        entry["status"] = response.status_code
        entry["content_type"] = response.headers.get("Content-Type")
        response.raise_for_status()
        entry["body"] = response.json() if as_json else response.text
    except (requests.RequestException, ValueError) as exc:
        entry["error"] = "{}: {}".format(type(exc).__name__, exc)
    return entry


def cached_fetch(cache, key, url, **kwargs):
    # Reuse successful responses only, so a rerun retries anything that failed.
    entry = cache.get(key)
    if entry and entry.get("error") is None and entry.get("url") == url:
        return entry
    entry = fetch(url, **kwargs)
    cache[key] = entry
    return entry


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "unnamed"


def github_repo(site_url):
    """Return "owner/repo", "" for a non-repo GitHub page, or None if not GitHub."""
    parsed = urlparse(site_url)
    if parsed.netloc.lower() not in ("github.com", "www.github.com"):
        return None
    parts = [p for p in parsed.path.split("/") if p]
    if len(parts) < 2:
        return ""
    return "{}/{}".format(parts[0], re.sub(r"\.git$", "", parts[1]))


def record_error(errors, source, entry):
    if entry["error"]:
        errors.append({"source": source, "url": entry["url"], "error": entry["error"]})


def enrich_candidate(candidate):
    row = dict(candidate)
    errors = []
    row["errors"] = errors
    cache_path = os.path.join(CACHE_DIR, safe_filename(candidate["name"]) + ".json")

    cache = {}
    if os.path.exists(cache_path):
        try:
            with io.open(cache_path, encoding="utf-8") as handle:
                cache = json.load(handle)
        except ValueError:
            cache = {}

    # HN thread: post text plus top-level comments.
    row["hn_post_text"] = None
    row["hn_comments"] = []
    match = re.search(r"[?&]id=(\d+)", candidate.get("hn_url") or "")
    if not match:
        errors.append({"source": "hn_thread", "url": candidate.get("hn_url"), "error": "could not parse item id"})
    else:
        entry = cached_fetch(cache, "hn_thread", HN_ITEM_URL.format(match.group(1)))
        record_error(errors, "hn_thread", entry)
        thread = entry["body"] or {}
        row["hn_post_text"] = html_to_text(thread.get("text")) or None
        for child in thread.get("children") or []:
            # Deleted or flagged comments come back with no text.
            if child.get("type") != "comment" or not child.get("text"):
                continue
            row["hn_comments"].append({
                "author": child.get("author"),
                "created_at": child.get("created_at"),
                "text": html_to_text(child.get("text")),
            })

    # Site: GitHub API for repos, plain-text scrape for everything else.
    row["site_text"] = None
    row["github"] = None
    site_url = candidate.get("site_url")
    repo = github_repo(site_url) if site_url else None

    if repo == "":
        errors.append({"source": "github", "url": site_url, "error": "GitHub URL is not a repository"})
    elif repo:
        base = "{}/repos/{}".format(GITHUB_API, repo)
        info = cached_fetch(cache, "github_repo", base, headers=GITHUB_HEADERS)
        commits = cached_fetch(cache, "github_commits", base + "/commits",
                               headers=GITHUB_HEADERS, params={"per_page": 1})
        # The repo endpoint's open_issues_count includes pull requests, so ask
        # search for issues only.
        issues = cached_fetch(cache, "github_issues", GITHUB_API + "/search/issues",
                              headers=GITHUB_HEADERS,
                              params={"q": "repo:{} type:issue state:open".format(repo), "per_page": 1})
        for source, entry in (("github_repo", info), ("github_commits", commits), ("github_issues", issues)):
            record_error(errors, source, entry)

        last_commit = None
        if isinstance(commits["body"], list) and commits["body"]:
            last_commit = commits["body"][0].get("commit", {}).get("committer", {}).get("date")

        row["github"] = {
            "repo": repo,
            "stars": (info["body"] or {}).get("stargazers_count"),
            "last_commit_date": last_commit,
            "open_issues": (issues["body"] or {}).get("total_count"),
        }
    elif site_url:
        entry = cached_fetch(cache, "site", site_url, headers=SITE_HEADERS, as_json=False)
        content_type = (entry["content_type"] or "").lower()
        if entry["error"] is None and "html" not in content_type:
            entry["error"] = "unsupported content type: {}".format(entry["content_type"])
        record_error(errors, "site", entry)
        if entry["error"] is None:
            row["site_text"] = html_to_text(entry["body"]) or None

    with io.open(cache_path, "w", encoding="utf-8") as handle:
        json.dump(cache, handle, indent=2, ensure_ascii=False)

    return row


def main():
    with io.open(INPUT_PATH, encoding="utf-8") as handle:
        candidates = [json.loads(line) for line in handle if line.strip()]

    os.makedirs(CACHE_DIR, exist_ok=True)
    enriched = []

    for candidate in candidates:
        try:
            row = enrich_candidate(candidate)
        except Exception as exc:
            # Last line of defence: a bug on one candidate must not lose the others.
            row = dict(candidate)
            row.update({"hn_post_text": None, "hn_comments": [], "site_text": None, "github": None})
            row["errors"] = [{"source": "internal", "url": None, "error": "{}: {}".format(type(exc).__name__, exc)}]
        enriched.append(row)

        stars = (row.get("github") or {}).get("stars")
        print("{:<20.20} comments={:<3} post={:<5} site={:<6} stars={:<6} errors={}".format(
            str(row.get("name")),
            len(row.get("hn_comments") or []),
            len(row.get("hn_post_text") or ""),
            len(row.get("site_text") or ""),
            "-" if stars is None else stars,
            len(row["errors"]),
        ))
        for error in row["errors"]:
            print("    ! {}: {}".format(error["source"], error["error"][:120]))

    os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
    with io.open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
        for row in enriched:
            handle.write(json.dumps(row, ensure_ascii=False) + "\n")

    print("\nwrote {} rows to {}".format(len(enriched), OUTPUT_PATH))


if __name__ == "__main__":
    main()
