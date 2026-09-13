"""Score enriched candidates against the thesis with Gemini."""

import hashlib
import io
import json
import os
import re
import time

from dotenv import load_dotenv

load_dotenv()

INPUT_PATH = os.path.join("data", "enriched.jsonl")
OUTPUT_PATH = os.path.join("data", "analyses.jsonl")
CACHE_DIR = os.path.join("cache", "llm")
# Pinned rather than an alias like "gemini-flash-latest", so a reviewer's rerun
# gets the same model. Lite has its own free-tier quota, separate from Flash.
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash-lite")
ATTEMPTS = 2  # first try plus one retry when the JSON is unusable

# Free-tier quotas are per minute, so space out live calls and, if Google still
# rejects one, wait the delay it asks for instead of failing straight away.
MIN_CALL_INTERVAL = float(os.environ.get("GEMINI_MIN_INTERVAL_SECONDS", "13"))
RATE_LIMIT_RETRIES = 3

THESIS = (
    "Seed-stage AI infra and dev tools with technical founders shipping in public. "
    "For this category the engineering trail is a better early signal than the pitch, "
    "because the buyers are engineers."
)

# Placeholders are swapped with str.replace, not str.format, because the JSON
# example is full of literal braces.
PROMPT_TEMPLATE = """You are a seed-stage VC analyst. Below is everything publicly
available about one startup: their Hacker News launch post, the
comments on it, their website text, and GitHub stats if any.

THESIS: [THESIS]

Analyse ONLY from the text provided. If something isn't in the
text, write "not found in sources". Never use outside knowledge
about this company. Never guess.

Return JSON only, no markdown fences:

{
  "team": {"summary": "...", "source": "hn_post|comments|site|github"},
  "product": {"summary": "...", "source": "..."},
  "market": {"summary": "...", "source": "..."},
  "risks": [{"risk": "...", "source": "..."}],
  "scores": {
    "founder_depth":     {"score": 0-25, "why": "...", "source": "..."},
    "shipping_evidence": {"score": 0-25, "why": "...", "source": "..."},
    "demand_signal":     {"score": 0-25, "why": "...", "source": "..."},
    "defensibility":     {"score": 0-25, "why": "...", "source": "..."}
  },
  "verdict": "Pass|Watch|Take a meeting",
  "verdict_reason": "one sentence",
  "would_change_my_mind": ["...", "...", "..."],
  "thesis_fit": "on-thesis|off-thesis",
  "data_gaps": ["..."]
}

SOURCES:
[SOURCES]
"""

REQUIRED_KEYS = (
    "team", "product", "market", "risks", "scores", "verdict",
    "verdict_reason", "would_change_my_mind", "thesis_fit", "data_gaps",
)

_model = None


def get_model():
    # Created on first cache miss, so a fully cached run needs no API key.
    global _model
    if _model is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            raise SystemExit("GEMINI_API_KEY is not set. Add it to .env in the project root.")
        import google.generativeai as genai
        genai.configure(api_key=api_key)
        _model = genai.GenerativeModel(
            MODEL_NAME,
            generation_config={"response_mime_type": "application/json", "temperature": 0.2},
        )
    return _model


_last_call_at = 0.0


def throttle():
    global _last_call_at
    wait = MIN_CALL_INTERVAL - (time.time() - _last_call_at)
    if wait > 0:
        time.sleep(wait)
    _last_call_at = time.time()


def is_rate_limited(exc):
    return type(exc).__name__ == "ResourceExhausted" or "429" in str(exc)


def retry_delay_seconds(exc, default=30):
    # Google puts the wait it wants in the error text: "retry_delay { seconds: 38 }".
    match = re.search(r"retry_delay\s*\{\s*seconds:\s*(\d+)", str(exc))
    return int(match.group(1)) + 2 if match else default


def call_model(prompt):
    """Return the model's text. Waits out rate limits; raises on any other failure."""
    for attempt in range(RATE_LIMIT_RETRIES + 1):
        throttle()
        try:
            return get_model().generate_content(prompt).text
        except SystemExit:
            raise
        except Exception as exc:
            if not is_rate_limited(exc) or attempt == RATE_LIMIT_RETRIES:
                raise
            delay = retry_delay_seconds(exc)
            print("    rate limited, waiting {}s before retrying".format(delay))
            time.sleep(delay)


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "unnamed"


def build_sources(row):
    lines = [
        "=== HN POST [source: hn_post] ===",
        "Name: {}".format(row.get("name")),
        "YC batch: {}".format(row.get("yc_batch") or "unknown"),
        "Tagline: {}".format(row.get("tagline") or ""),
        "Posted: {}".format(row.get("created_at")),
        "Points: {}  Comments: {}".format(row.get("points"), row.get("num_comments")),
        "",
        row.get("hn_post_text") or "(no post text)",
        "",
        "=== COMMENTS [source: comments] ===",
    ]
    comments = row.get("hn_comments") or []
    if not comments:
        lines.append("(no comments)")
    for comment in comments:
        lines.append("- {} ({}): {}".format(
            comment.get("author"), (comment.get("created_at") or "")[:10], comment.get("text")))

    lines += ["", "=== WEBSITE TEXT [source: site] ==="]
    if row.get("site_text"):
        lines.append(row["site_text"])
    elif row.get("github"):
        lines.append("(no website fetched: the launch linked to a GitHub repository)")
    elif not row.get("site_url"):
        lines.append("(no website: text-only launch post)")
    else:
        lines.append("(website could not be fetched)")

    lines += ["", "=== GITHUB [source: github] ==="]
    github = row.get("github")
    if github:
        lines += [
            "Repository: {}".format(github.get("repo")),
            "Stars: {}".format(github.get("stars")),
            "Last commit: {}".format(github.get("last_commit_date")),
            "Open issues (excluding pull requests): {}".format(github.get("open_issues")),
        ]
    else:
        lines.append("(no GitHub repository linked from the launch)")
    return "\n".join(lines)


def parse_response(text):
    """Return (data, None) on success or (None, reason) when the output is unusable."""
    cleaned = re.sub(r"^\s*```(?:json)?\s*|\s*```\s*$", "", text or "")
    try:
        data = json.loads(cleaned)
    except ValueError as exc:
        return None, "invalid JSON: {}".format(exc)
    if not isinstance(data, dict):
        return None, "expected a JSON object, got {}".format(type(data).__name__)
    missing = [key for key in REQUIRED_KEYS if key not in data]
    if missing:
        return None, "missing keys: {}".format(", ".join(missing))
    return data, None


def analyze(row):
    """Return (analysis, error, from_cache)."""
    prompt = PROMPT_TEMPLATE.replace("[THESIS]", THESIS).replace("[SOURCES]", build_sources(row))
    # The model name is part of the key so switching models never serves a stale answer.
    prompt_hash = hashlib.sha256((MODEL_NAME + "\n" + prompt).encode("utf-8")).hexdigest()
    cache_path = os.path.join(CACHE_DIR, safe_filename(row["name"]) + ".json")

    if os.path.exists(cache_path):
        try:
            with io.open(cache_path, encoding="utf-8") as handle:
                cached = json.load(handle)
            if cached.get("prompt_hash") == prompt_hash:
                return cached["analysis"], None, True
        except (ValueError, KeyError):
            pass  # corrupt cache file: fall through and call the API again

    last_error = None
    for attempt in range(1, ATTEMPTS + 1):
        try:
            text = call_model(prompt)
        except SystemExit:
            raise
        except Exception as exc:
            # Rate limits were already waited out in call_model. Anything left is
            # recorded, not cached, so the next run tries again.
            return None, "API error: {}: {}".format(type(exc).__name__, exc), False

        analysis, last_error = parse_response(text)
        if analysis is not None:
            with io.open(cache_path, "w", encoding="utf-8") as handle:
                json.dump({
                    "name": row["name"],
                    "model": MODEL_NAME,
                    "prompt_hash": prompt_hash,
                    "created_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                    "attempts": attempt,
                    "raw_response": text,
                    "analysis": analysis,
                }, handle, indent=2, ensure_ascii=False)
            return analysis, None, False

    return None, "unusable model output after {} attempts: {}".format(ATTEMPTS, last_error), False


with io.open(INPUT_PATH, encoding="utf-8") as handle:
    rows = [json.loads(line) for line in handle if line.strip()]

os.makedirs(CACHE_DIR, exist_ok=True)
results = []
print("model: {}  (live calls spaced {:.0f}s apart; cached rows are instant)\n".format(
    MODEL_NAME, MIN_CALL_INTERVAL))

for row in rows:
    try:
        analysis, error, from_cache = analyze(row)
    except SystemExit:
        raise
    except Exception as exc:
        # A bug on one candidate must not lose the rest of the run.
        analysis, error, from_cache = None, "internal: {}: {}".format(type(exc).__name__, exc), False

    row["analysis"] = analysis
    row["analysis_error"] = error
    results.append(row)

    if analysis is not None:
        try:
            total = sum(int(s.get("score") or 0) for s in analysis["scores"].values())
        except (AttributeError, TypeError, ValueError):
            total = "?"
        print("{:<20.20} {:<6} {:<15} score={:<4} {}".format(
            str(row.get("name")), "cached" if from_cache else "live",
            str(analysis.get("verdict")), total, analysis.get("thesis_fit")))
    else:
        print("{:<20.20} ERROR  {}".format(str(row.get("name")), " ".join(error.split())[:150]))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with io.open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
    for row in results:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

failed = sum(1 for row in results if row["analysis_error"])
print("\nwrote {} rows to {} ({} failed)".format(len(results), OUTPUT_PATH, failed))
