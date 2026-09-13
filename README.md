# VC triage pipeline

Turns Hacker News "Launch HN" posts into one-page investment memos with a Pass / Watch / Take a meeting call, scored against a fixed thesis. Every claim in a memo carries a quote that is checked, in code, against the source it cites.

**Start here:** [memos/README.md](memos/README.md) ranks the 10 companies from the committed run (2 Take a meeting, 3 Watch, 5 Pass). All 227 supporting quotes in those memos were found word for word in their sources.

## Run it

Requires Python 3.11.

```bash
python -m venv venv
venv\Scripts\activate          # macOS/Linux: source venv/bin/activate
pip install -r requirements.txt

python run.py                  # replay the committed run from cache: no API key, a few seconds
```

To analyse a topic you need a free Gemini key from [Google AI Studio](https://aistudio.google.com). Copy `.env.example` to `.env` and paste the key in.

```bash
python run.py --topic "voice AI"               # memos land in runs/voice-ai/memos/
python run.py --topic "MCP" --top 15 --days 180
python run.py --refresh                        # refetch the default Launch HN list (changes the companies)
python -m pytest                               # 47 tests, no network
```

## How it works

Five plain scripts, each reading the previous one's output from disk. `run.py` chains them.

| Stage | Script | Output |
|---|---|---|
| Fetch | `src/fetch_hn.py` | Launch HN posts from the HN Algolia API, `cache/hn_raw.json` |
| Source | `src/source.py` | Top N by points, with name, YC batch, tagline, site and traction, `data/candidates.jsonl` |
| Enrich | `src/enrich.py` | Launch post text, top-level comments, website text, GitHub stars, last commit and open issues, `data/enriched.jsonl` |
| Analyse | `src/analyze.py` | Gemini writes team, product, market, risks and four scores, each with quotes. Code checks every quote and sets fit and verdict. `data/analyses.jsonl` |
| Memo | `src/memo.py` | One markdown page per company plus a ranked index, `memos/`. No model calls. |

**Caching makes runs replayable.** HN search covers a rolling window, websites change, and model scores drift, so the raw HN list, every fetched page and every Gemini reply are committed under `cache/`. Gemini replies are keyed on the exact prompt, model and temperature, so changing any of them triggers a fresh call instead of reusing a stale answer. Replies from different models are kept in separate folders.

**Failures don't stop the run.** A dead website, a failed GitHub lookup, an unusable model reply or a missing API key is recorded, and that company gets a "No call" page. Rerunning retries only what failed.

## Thesis and scoring

> Seed-stage AI infra and dev tools with technical founders shipping in public. For this category the engineering trail is a better early signal than the pitch, because the buyers are engineers.

**Fit is decided by code, not by the model.** Gemini classifies two facts, each backed by a quote:
- **What customers pay for:** software, IP or research, physical goods, services, or unclear.
- **What the product is:** AI infrastructure, engineering software, AI applied to a technical domain, hardware, or other.

A company is off-thesis if customers pay for physical goods or services, or if the product is hardware or other. Asking the model for fit directly didn't hold: it called a circuit-board maker a dev tool because the company ships design plugins.

**Scores.** Four dimensions worth 25 points each, with written anchors for low, middle and high: founder depth, shipping evidence, demand signal, and defensibility. Missing evidence scores low.

**Verdict, by rule.** Off-thesis is always Pass. On-thesis companies get Take a meeting at 75 or above, Watch from 60 to 74, and Pass below 60.

## Known limits

- **One source.** Launch HN only, so it covers YC companies and roughly 100 launches a year. Most topic searches find fewer than 10 matches, and the runner warns when that happens.
- **Topic matching is keyword-based.** A launch is kept if every topic word appears in its title or post, even in passing.
- **Founder evidence is thin.** It comes from the launch post and top-level comments only. Founders' replies in nested comments aren't collected.
- **No JavaScript rendering.** Websites built mostly in JavaScript yield little text.
- **Text-only launches show no website,** even when the post names one.
- **Scores drift between runs** by several points, so companies near a cutoff can flip between runs. The committed cache freezes one run.
- **Off-thesis memos still list "what would change the call",** even though only a change in business model would.
- **Free-tier Gemini limits.** About 5 requests a minute and roughly 20 a day per model, which is enough for one fresh run of 10 to 20 companies a day. Google may use free-tier prompts to improve its products. Only public HN posts, comments and website text are sent.
- **Deprecated SDK.** `google-generativeai` is deprecated but still works.

## How this was built


## What Claude Code wrote

All the code, end to end: every script in src, run.py, the tests, the requirements file and .env example, and the ignore file. Each came from your prompt for that stage.
The factual README sections: install, how it works, thesis rules and known limits.
The analysis prompt, rewritten several times. You supplied the original prompt and JSON shape. Claude later added the thesis scope, score anchors, quote evidence, and the business-model classification.

## Decisions I took

HN as the source, skipping Product Hunt, Crunchbase and the YC directory. This is in your worklog from before the coding started.
Launch HN over Show HN, after Show HN turned up mostly weekend projects.
The thesis wording.
Gemini's free tier, so a reviewer can run it.
Keeping off-thesis companies in the set, so the pipeline visibly rejects some.
Committing the cache. Claude had added it to the ignore file, and you reversed that because HN search only covers a rolling window.
The borderline calls: Discovered Materials and Adam on-thesis, with strict cutoffs.
Two quality calls: requiring a one-command run a reviewer could actually use, and pushing on free-tier quota as a real problem.
Spotting Adam in the MCP results, which led to the exact-word topic filter.

## Where Claude caught something

The first HN query: only 8 of 50 results were real Launch HN posts.
A crash in enrichment: the enrichment script crashed on a failed GitHub lookup. Deliberate bad-input testing found it.
The missing URL field: text-only launches have no URL field at all, rather than a link back to HN as the spec assumed.
The first full analysis: 7 of 10 got a meeting, and thesis fit was being judged on quality, not category.
Flash Lite's labelling: Flash Lite quoted ProvenMetal's per-order margin and still labelled it software.
The useless retry: at temperature zero, a retry returns the identical broken reply, which is why RonanRX kept failing.

## where claude was wrong 

The Adam fix: Claude's wording change to fix Adam is what let ProvenMetal back in as on-thesis.
Flash Lite: Claude recommended it with throttling, and it later proved unreliable at classification.
The retry design: Claude wrote retry logic that couldn't work at temperature zero.


The trail, in the order it happened:
- [docs/worklog.md](docs/worklog.md): dated notes on decisions, mistakes and fixes, written as the work went.

- `git log`: one commit per stage, including the committed baseline run before the thesis fixes.

