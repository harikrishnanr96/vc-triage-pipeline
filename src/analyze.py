"""Score enriched candidates against the thesis with Gemini."""

import hashlib
import io
import json
import os
import re
import time

from dotenv import load_dotenv

load_dotenv()

# Pinned rather than an alias like "gemini-flash-latest", so a reviewer's rerun
# gets the same model. Flash Lite was tried first and kept labelling a
# circuit-board maker as software even while quoting its per-order margin; full
# Flash labels it correctly. Free tier: about 5 requests a minute and a small
# daily cap per model, enough for one run of 10-20 companies.
MODEL_NAME = os.environ.get("GEMINI_MODEL", "gemini-3.5-flash")

RUN_DIR = os.environ.get("RUN_DIR", ".")  # set by run.py for topic runs
INPUT_PATH = os.path.join(RUN_DIR, "data", "enriched.jsonl")
OUTPUT_PATH = os.path.join(RUN_DIR, "data", "analyses.jsonl")
# Shared across runs, one folder per model, so trying another model never
# overwrites existing answers.
CACHE_DIR = os.path.join("cache", "llm", MODEL_NAME)
ATTEMPTS = 2  # first try plus one retry when the JSON is unusable

# Free-tier quotas are per minute, so space out live calls and, if Google still
# rejects one, wait the delay it asks for instead of failing straight away.
MIN_CALL_INTERVAL = float(os.environ.get("GEMINI_MIN_INTERVAL_SECONDS", "13"))
RATE_LIMIT_RETRIES = 3
REQUEST_TIMEOUT = 180  # seconds per Gemini call

THESIS = (
    "Seed-stage AI infra and dev tools with technical founders shipping in public. "
    "For this category the engineering trail is a better early signal than the pitch, "
    "because the buyers are engineers."
)

# The model classifies the business; code decides thesis fit from that
# classification (fit_from_business_model). Asking the model for fit directly
# failed: it called a circuit-board maker a dev tool because it ships plugins.
# Borderline calls made on Sep 13: Discovered Materials (AI discovery harness)
# and Adam (AI CAD for mechanical engineers) are both in.
PAY_FOR = {
    "software": "subscriptions, usage-based APIs, licences, or software "
                "products (including free or open-source software with paid tiers)",
    "ip_or_research": "rights to discoveries, research results, or licensed IP",
    "physical_goods": "hardware, devices, robots, manufactured "
                      "goods, drugs, or orders of physical products",
    "services": "work done by people, such as brokerage, consulting, manual operations, "
                "or care delivered to patients",
    "unclear": "the sources do not say what customers pay for",
}
CATEGORY = {
    "ai_infrastructure": "model serving, routing, compute, evals and benchmarks, "
                         "agent harnesses and runtimes, data or web access for "
                         "models and agents, MCP and agent tooling",
    "engineering_software": "software used by engineers of any discipline "
                            "(software, mechanical, electrical, hardware design) "
                            "in their technical work, such as coding agents, "
                            "testing tools, or CAD",
    "ai_for_technical_domain": "an AI system applied to a technical or scientific "
                               "domain, where the AI system itself is the main asset",
    "hardware": "hardware, robots, devices, or other physical products",
    "other": "any other business, such as manufacturing, pharma, healthcare, "
             "consumer, fintech, or insurance",
}
OFF_THESIS_PAY_FOR = ("physical_goods", "services")
IN_SCOPE_CATEGORIES = ("ai_infrastructure", "engineering_software", "ai_for_technical_domain")


def definitions(options):
    return "\n".join('  "{}": {}'.format(key, text) for key, text in options.items())


# Placeholders are swapped with str.replace, not str.format, because the JSON
# example is full of literal braces.
PROMPT_TEMPLATE = """You are a seed-stage VC analyst. Below is everything publicly
available about one startup: their Hacker News launch post, the
comments on it, their website text, and GitHub stats if any.

THESIS: [THESIS]

Analyse ONLY from the text provided. If something isn't in the
text, write "not found in sources". Never use outside knowledge
about this company. Never guess.

BUSINESS MODEL: classify the company as facts, not as a judgement of quality.
"customers_pay_for" is what the company's revenue comes from, or will come
from, according to the sources. Choose exactly one:
[PAY_FOR]
If a company gives away software to win orders for physical products, it is
"physical_goods", not "software".
"category" is what the core product is. Choose exactly one:
[CATEGORY]

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
  "business_model": {
    "customers_pay_for": "one of the options above",
    "category": "one of the options above",
    "summary": "one sentence: what the product is, who uses it, and what they pay for",
    "evidence": [{"quote": "...", "source": "hn_post"}]
  },
  "team":    {"summary": "...", "evidence": [...]},
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
  "case_summary": "one sentence: the strongest point for and against",
  "would_change_my_mind": ["...", "...", "..."],
  "data_gaps": ["..."]
}

SOURCES:
[SOURCES]
"""

REQUIRED_KEYS = (
    "business_model", "team", "product", "market", "risks", "scores",
    "case_summary", "would_change_my_mind", "data_gaps",
)
SCORE_KEYS = ("founder_depth", "shipping_evidence", "demand_signal", "defensibility")
MARKET_KEYS = ("size_hint", "competitors", "why_now")
TEMPERATURE = 0  # lowest run-to-run variance, though scores can still drift slightly
# At temperature 0 a retry returns the identical reply, so a broken one stays broken
# (RonanRX failed four times with the same malformed JSON). Retries sample instead.
RETRY_TEMPERATURE = 0.7

# The verdict is set here, not by the model, so the thesis is applied the same
# way to every company. Off-thesis is always Pass.
MEETING_CUTOFF = 75
WATCH_CUTOFF = 60

_model = None


class MissingApiKey(Exception):
    pass


def get_model():
    # Created on first cache miss, so a fully cached run needs no API key.
    global _model
    if _model is None:
        api_key = os.environ.get("GEMINI_API_KEY")
        if not api_key:
            # Only companies without a cached answer need a key; they get "No call"
            # and the rest of the run still produces memos.
            raise MissingApiKey("not in cache for this model and GEMINI_API_KEY is not set (add it to .env)")
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


def call_model(prompt, temperature):
    """Return the model's text. Waits out rate limits; raises on any other failure."""
    model = get_model()  # raises MissingApiKey before any throttle wait
    for attempt in range(RATE_LIMIT_RETRIES + 1):
        throttle()
        try:
            # Without a timeout a stalled request blocks the whole run indefinitely.
            config = {"response_mime_type": "application/json", "temperature": temperature}
            return model.generate_content(prompt, generation_config=config,
                                          request_options={"timeout": REQUEST_TIMEOUT}).text
        except SystemExit:
            raise
        except Exception as exc:
            # A daily cap won't lift within minutes, so waiting on it only stalls the run.
            if not is_rate_limited(exc) or "PerDay" in str(exc) or attempt == RATE_LIMIT_RETRIES:
                raise
            delay = retry_delay_seconds(exc)
            print("    rate limited, waiting {}s before retrying".format(delay), flush=True)
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
    for key in ("business_model", "team", "product"):
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
    business = data["business_model"] if isinstance(data["business_model"], dict) else {}
    for field, options in (("customers_pay_for", PAY_FOR), ("category", CATEGORY)):
        if business.get(field) not in options:
            return None, "business_model.{} must be one of {}, got {!r}".format(
                field, ", ".join(options), business.get(field))
    scores = data["scores"] if isinstance(data["scores"], dict) else {}
    for key in SCORE_KEYS:
        value = (scores.get(key) or {}).get("score") if isinstance(scores.get(key), dict) else None
        if not isinstance(value, (int, float)) or isinstance(value, bool):
            return None, "scores.{}.score is not a number".format(key)
    return data, None


def fit_from_business_model(business):
    """Apply the thesis to the model's classification. Returns (fit, rule)."""
    pay_for, category = business["customers_pay_for"], business["category"]
    if pay_for in OFF_THESIS_PAY_FOR:
        return "off-thesis", "customers pay for {}".format(pay_for.replace("_", " "))
    if category not in IN_SCOPE_CATEGORIES:
        return "off-thesis", "category is {}".format(category.replace("_", " "))
    return "on-thesis", "{}, customers pay for {}".format(
        category.replace("_", " "), pay_for.replace("_", " "))


def decide(analysis):
    """Turn the model's classification and scores into fit, total, and verdict, by fixed rules."""
    fit, fit_rule = fit_from_business_model(analysis["business_model"])
    score = sum(max(0, min(25, int(round(analysis["scores"][key]["score"])))) for key in SCORE_KEYS)
    if fit == "off-thesis":
        verdict, rule = "Pass", "off-thesis is always Pass"
    elif score >= MEETING_CUTOFF:
        verdict, rule = "Take a meeting", "on-thesis and score {} >= {}".format(score, MEETING_CUTOFF)
    elif score >= WATCH_CUTOFF:
        verdict, rule = "Watch", "on-thesis and score {} is {}-{}".format(score, WATCH_CUTOFF, MEETING_CUTOFF - 1)
    else:
        verdict, rule = "Pass", "on-thesis but score {} < {}".format(score, WATCH_CUTOFF)
    return {"thesis_fit": fit, "thesis_fit_rule": fit_rule, "score": score,
            "verdict": verdict, "verdict_rule": rule}


def analyze(row):
    """Return (analysis, error, from_cache)."""
    prompt = (PROMPT_TEMPLATE.replace("[THESIS]", THESIS)
              .replace("[PAY_FOR]", definitions(PAY_FOR))
              .replace("[CATEGORY]", definitions(CATEGORY))
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
    failures = []
    for attempt in range(1, ATTEMPTS + 1):
        try:
            temperature = TEMPERATURE if attempt == 1 else RETRY_TEMPERATURE
            text = call_model(prompt, temperature)
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
                    "temperature": temperature,
                    "raw_response": text,
                    "analysis": analysis,
                }, handle, indent=2, ensure_ascii=False)
            return analysis, None, False
        failures.append({"attempt": attempt, "temperature": temperature, "error": last_error, "raw_response": text})

    # Kept beside the cache so a bad reply can be inspected; never read back as a result.
    with io.open(cache_path.replace(".json", ".failed.json"), "w", encoding="utf-8") as handle:
        json.dump({"name": row["name"], "model": MODEL_NAME, "failures": failures},
                  handle, indent=2, ensure_ascii=False)
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
    row.update({"thesis_fit": None, "thesis_fit_rule": None, "score": None,
                "verdict": None, "verdict_rule": None, "quote_check": None})
    if analysis is not None:
        # Applied to cached answers too, so changing a rule, a cutoff, or the
        # quote check needs no API calls.
        row.update(decide(analysis))
        row["quote_check"] = check_quotes(analysis, row)
    results.append(row)

    if analysis is not None:
        print("{:<20.20} {:<6} {:<15} score={:<4} {:<11} {:<48} quotes {}/{}".format(
            str(row.get("name")), "cached" if from_cache else "live", row["verdict"], row["score"],
            row["thesis_fit"], row["thesis_fit_rule"], row["quote_check"]["verified"],
            row["quote_check"]["total"]), flush=True)
    else:
        print("{:<20.20} ERROR  {}".format(str(row.get("name")), " ".join(error.split())[:150]), flush=True)

os.makedirs(os.path.dirname(OUTPUT_PATH), exist_ok=True)
with io.open(OUTPUT_PATH, "w", encoding="utf-8") as handle:
    for row in results:
        handle.write(json.dumps(row, ensure_ascii=False) + "\n")

failed = sum(1 for row in results if row["analysis_error"])
print("\nwrote {} rows to {} ({} failed)".format(len(results), OUTPUT_PATH, failed))
