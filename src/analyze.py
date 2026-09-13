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

# The boundary is what makes thesis_fit a category call instead of a quality call.
# Borderline calls made on Sep 13: Discovered Materials (AI discovery harness) and
# Adam (AI CAD for mechanical engineers) are both in.
THESIS_SCOPE = """IN SCOPE:
- AI infrastructure: model serving, routing, compute, evals and benchmarks,
  agent harnesses and runtimes, data or web access for models and agents,
  MCP and agent tooling.
- Developer and engineering tools: software used by engineers of any
  discipline (software, mechanical, electrical, hardware design) in their
  technical work. This includes AI-native tools such as coding agents,
  testing tools, and mechanical CAD or design software. The tool must be
  software; a physical product is out of scope even if engineers buy it.
- AI systems applied to a technical domain, when the AI system itself is the
  main asset (for example, agents that run scientific discovery).

OUT OF SCOPE:
- Hardware and physical products, including robots and devices, even when
  sold to developers.
- Manufacturing, logistics, or brokerage services where customers pay for
  physical goods or orders, even if the company also ships software such as
  plugins or automation to win or run that work.
- Healthcare, pharma, consumer, fintech, insurance, and other vertical
  businesses that are not AI infrastructure or engineering tools."""

# Placeholders are swapped with str.replace, not str.format, because the JSON
# example is full of literal braces.
PROMPT_TEMPLATE = """You are a seed-stage VC analyst. Below is everything publicly
available about one startup: their Hacker News launch post, the
comments on it, their website text, and GitHub stats if any.

THESIS: [THESIS]

[SCOPE]

THESIS FIT: decide "on-thesis" or "off-thesis" only from what the product is,
who uses it, and what customers pay for. Never decide fit from quality,
traction, team strength, or defensibility. Those belong in the scores.

Analyse ONLY from the text provided. If something isn't in the
text, write "not found in sources". Never use outside knowledge
about this company. Never guess.

SCORING (each 0-25). Missing evidence scores low, not in the middle.
Reserve 18-25 for strong, explicit evidence in the sources.
- founder_depth: 0-8 no founder information or no technical background
  shown; 9-17 technical backgrounds stated but little domain depth or prior
  shipping; 18-25 deep domain expertise plus prior shipped products or exits.
- shipping_evidence: 0-8 waitlist, demo, or claims only; 9-17 product is live
  but the public engineering trail is thin; 18-25 public code, docs,
  benchmarks, frequent releases, or paying users.
- demand_signal: 0-8 little engagement, or sceptical comments dominate;
  9-17 solid HN engagement but no named users or revenue; 18-25 revenue,
  named customers, or many commenters who want to use it.
- defensibility: 0-8 thin wrapper, commenters say it is easy to copy, or many
  named competitors; 9-17 some workflow, integration, or data depth;
  18-25 proprietary data, a hard technical moat, or network effects.

EVIDENCE: every claim needs "evidence", a list of 1-3 short quotes copied
word for word from the SOURCES (each quote under 25 words). Do not paraphrase
inside a quote, do not fix typos, do not join text from different places.
"source" is the section the quote came from: hn_post, comments, site, or
github. For comments, also give "author", the commenter's username exactly as
shown. If nothing supports a claim, write "not found in sources" as the
summary and return an empty evidence list.

Return JSON only, no markdown fences:

{
  "team":    {"summary": "...", "evidence": [{"quote": "...", "source": "hn_post"}]},
  "product": {"summary": "...", "evidence": [...]},
  "market": {
    "size_hint":   {"summary": "...", "evidence": [...]},
    "competitors": {"summary": "...", "names": ["..."], "evidence": [{"quote": "...", "source": "comments", "author": "..."}]},
    "why_now":     {"summary": "...", "evidence": [...]}
  },
  "risks": [{"risk": "...", "evidence": [...]}],
  "scores": {
    "founder_depth":     {"score": 0-25, "why": "...", "evidence": [...]},
    "shipping_evidence": {"score": 0-25, "why": "...", "evidence": [...]},
    "demand_signal":     {"score": 0-25, "why": "...", "evidence": [...]},
    "defensibility":     {"score": 0-25, "why": "...", "evidence": [...]}
  },
  "thesis_fit": "on-thesis|off-thesis",
  "thesis_fit_reason": "one sentence on what the product is, who uses it, and what they pay for",
  "case_summary": "one sentence: the strongest point for and against",
  "would_change_my_mind": ["...", "...", "..."],
  "data_gaps": ["..."]
}

SOURCES:
[SOURCES]
"""

REQUIRED_KEYS = (
    "team", "product", "market", "risks", "scores", "thesis_fit",
    "thesis_fit_reason", "case_summary", "would_change_my_mind", "data_gaps",
)
SCORE_KEYS = ("founder_depth", "shipping_evidence", "demand_signal", "defensibility")
MARKET_KEYS = ("size_hint", "competitors", "why_now")
TEMPERATURE = 0  # lowest run-to-run variance, though scores can still drift slightly

# The verdict is set here, not by the model, so the thesis is applied the same
# way to every company. Off-thesis is always Pass.
MEETING_CUTOFF = 75
WATCH_CUTOFF = 60

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
            generation_config={"response_mime_type": "application/json", "temperature": TEMPERATURE},
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


def source_sections(row):
    """Return {source name: text}, the exact text the model sees for each source."""
    hn_post = "\n".join([
        "Name: {}".format(row.get("name")),
        "YC batch: {}".format(row.get("yc_batch") or "unknown"),
        "Tagline: {}".format(row.get("tagline") or ""),
        "Posted: {}".format(row.get("created_at")),
        "Points: {}  Comments: {}".format(row.get("points"), row.get("num_comments")),
        "",
        row.get("hn_post_text") or "(no post text)",
    ])

    comments = row.get("hn_comments") or []
    comment_lines = ["- {} ({}): {}".format(
        c.get("author"), (c.get("created_at") or "")[:10], c.get("text")) for c in comments]

    if row.get("site_text"):
        site = row["site_text"]
    elif row.get("github"):
        site = "(no website fetched: the launch linked to a GitHub repository)"
    elif not row.get("site_url"):
        site = "(no website: text-only launch post)"
    else:
        site = "(website could not be fetched)"

    github = row.get("github")
    if github:
        github_text = "\n".join([
            "Repository: {}".format(github.get("repo")),
            "Stars: {}".format(github.get("stars")),
            "Last commit: {}".format(github.get("last_commit_date")),
            "Open issues (excluding pull requests): {}".format(github.get("open_issues")),
        ])
    else:
        github_text = "(no GitHub repository linked from the launch)"

    return {
        "hn_post": hn_post,
        "comments": "\n".join(comment_lines) or "(no comments)",
        "site": site,
        "github": github_text,
    }


SECTION_TITLES = {"hn_post": "HN POST", "comments": "COMMENTS", "site": "WEBSITE TEXT", "github": "GITHUB"}


def build_sources(row):
    return "\n\n".join("=== {} [source: {}] ===\n{}".format(SECTION_TITLES[name], name, text)
                       for name, text in source_sections(row).items())


def normalise(text):
    # Models swap curly quotes and dashes, turn double quotes into single ones to
    # keep the JSON valid, and re-flow whitespace, even when told to copy exactly.
    # None of that alters meaning, so ignore it when matching.
    text = (text or "").lower()
    for fancy, plain in (("‘", "'"), ("’", "'"), ("“", "'"), ("”", "'"),
                         ('"', "'"), ("–", "-"), ("—", "-"), ("…", "...")):
        text = text.replace(fancy, plain)
    return " ".join(text.split())


def quote_found(item, sections, row):
    """True when every fragment of the quote appears verbatim in its claimed source."""
    source = item.get("source")
    if source == "comments" and item.get("author"):
        haystack = "\n".join(c.get("text") or "" for c in row.get("hn_comments") or []
                             if c.get("author") == item["author"])
    else:
        haystack = sections.get(source, "")
    haystack = normalise(haystack)
    # An ellipsis marks a deliberate cut, so each side must match on its own.
    fragments = [f.strip(" .,;:\"'") for f in normalise(item.get("quote")).split("...")]
    fragments = [f for f in fragments if f]
    return bool(fragments) and bool(haystack) and all(f in haystack for f in fragments)


def evidence_lists(analysis):
    """Yield (label, evidence list) for every claim in an analysis."""
    for key in ("team", "product"):
        yield key, (analysis.get(key) or {}).get("evidence")
    for key in MARKET_KEYS:
        yield "market." + key, ((analysis.get("market") or {}).get(key) or {}).get("evidence")
    for i, risk in enumerate(analysis.get("risks") or []):
        yield "risks[{}]".format(i), (risk or {}).get("evidence")
    for key in SCORE_KEYS:
        yield "scores." + key, ((analysis.get("scores") or {}).get(key) or {}).get("evidence")


def check_quotes(analysis, row):
    """Mark each quote verified or not, and summarise. Mutates the analysis in place."""
    sections = source_sections(row)
    total, verified, unverified = 0, 0, []
    for label, evidence in evidence_lists(analysis):
        for item in evidence if isinstance(evidence, list) else []:
            if not isinstance(item, dict):
                continue
            item["verified"] = quote_found(item, sections, row)
            total += 1
            if item["verified"]:
                verified += 1
            else:
                unverified.append({"claim": label, "source": item.get("source"), "quote": item.get("quote")})
    return {"total": total, "verified": verified, "unverified": unverified}


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
    market = data["market"] if isinstance(data["market"], dict) else {}
    missing = [key for key in MARKET_KEYS if not isinstance(market.get(key), dict)]
    if missing:
        return None, "market is missing: {}".format(", ".join(missing))
    if data["thesis_fit"] not in ("on-thesis", "off-thesis"):
        return None, "thesis_fit must be on-thesis or off-thesis, got {!r}".format(data["thesis_fit"])
    scores = data["scores"] if isinstance(data["scores"], dict) else {}
    for key in SCORE_KEYS:
        value = (scores.get(key) or {}).get("score") if isinstance(scores.get(key), dict) else None
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return None, "scores.{}.score is not a number".format(key)
    return data, None


def decide(analysis):
    """Turn the model's scores and fit into a total and a verdict, by fixed rules."""
    score = sum(max(0, min(25, int(round(analysis["scores"][key]["score"])))) for key in SCORE_KEYS)
    if analysis["thesis_fit"] == "off-thesis":
        return score, "Pass", "off-thesis is always Pass"
    if score >= MEETING_CUTOFF:
        return score, "Take a meeting", "on-thesis and score {} >= {}".format(score, MEETING_CUTOFF)
    if score >= WATCH_CUTOFF:
        return score, "Watch", "on-thesis and score {} is {}-{}".format(score, WATCH_CUTOFF, MEETING_CUTOFF - 1)
    return score, "Pass", "on-thesis but score {} < {}".format(score, WATCH_CUTOFF)


def analyze(row):
    """Return (analysis, error, from_cache)."""
    prompt = (PROMPT_TEMPLATE.replace("[THESIS]", THESIS).replace("[SCOPE]", THESIS_SCOPE)
              .replace("[SOURCES]", build_sources(row)))
    # Model and temperature are part of the key so changing either never serves a stale answer.
    key = "{}\ntemperature={}\n{}".format(MODEL_NAME, TEMPERATURE, prompt)
    prompt_hash = hashlib.sha256(key.encode("utf-8")).hexdigest()
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
    row["model"] = MODEL_NAME
    row["thesis"] = THESIS
    row["score"], row["verdict"], row["verdict_rule"], row["quote_check"] = None, None, None, None
    if analysis is not None:
        # Applied to cached answers too, so changing a cutoff or the quote check
        # needs no API calls.
        row["score"], row["verdict"], row["verdict_rule"] = decide(analysis)
        row["quote_check"] = check_quotes(analysis, row)
    results.append(row)

    if analysis is not None:
        print("{:<20.20} {:<6} {:<15} score={:<4} {:<11} quotes {}/{}".format(
            str(row.get("name")), "cached" if from_cache else "live", row["verdict"], row["score"],
            analysis["thesis_fit"], row["quote_check"]["verified"], row["quote_check"]["total"]))
    else:
        print("{:<20.20} ERROR  {}".format(str(row.get("name")), " ".join(error.split())[:150]))

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with io.open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
    for row in results:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

failed = sum(1 for row in results if row["analysis_error"])
print("\nwrote {} rows to {} ({} failed)".format(len(results), OUTPUT_PATH, failed))
