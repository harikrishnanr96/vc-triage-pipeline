"""Render one markdown memo per analysed candidate, plus a ranked index. No model calls."""

import glob
import io
import json
import os
import re

RUN_DIR = os.environ.get("RUN_DIR", ".")  # set by run.py for topic runs
INPUT_PATH = os.path.join(RUN_DIR, "data", "analyses.jsonl")
MEMO_DIR = os.path.join(RUN_DIR, "memos")
MAX_QUOTES = 2  # per claim, to keep each memo to roughly one page

VERDICT_ORDER = {"Take a meeting": 0, "Watch": 1, "Pass": 2}
SCORE_LABELS = [
    ("founder_depth", "Founder depth"),
    ("shipping_evidence", "Shipping evidence"),
    ("demand_signal", "Demand signal"),
    ("defensibility", "Defensibility"),
]


def safe_filename(name):
    return re.sub(r"[^A-Za-z0-9._-]+", "_", name).strip("._") or "unnamed"


def one_line(text):
    return " ".join(str(text or "").split())


def cell(text):
    return one_line(text).replace("|", "\\|")


def source_link(item, row):
    source = item.get("source")
    if source == "comments":
        author = item.get("author")
        label = "HN comment by {}".format(author) if author else "HN comments"
        return "[{}]({})".format(label, row["hn_url"])
    if source == "hn_post":
        return "[HN post]({})".format(row["hn_url"])
    if source == "site" and row.get("site_url"):
        return "[website]({})".format(row["site_url"])
    if source == "github" and row.get("github"):
        return "[GitHub](https://github.com/{})".format(row["github"]["repo"])
    return source or "unknown source"


def evidence_lines(evidence, row, indent=""):
    lines = []
    for item in (evidence if isinstance(evidence, list) else [])[:MAX_QUOTES]:
        if not isinstance(item, dict):
            continue
        flag = "" if item.get("verified") else " **(not found word for word in this source)**"
        lines.append('{}- "{}" ({}){}'.format(indent, one_line(item.get("quote")), source_link(item, row), flag))
    return lines


def claim_block(claim, row):
    claim = claim if isinstance(claim, dict) else {}
    return [one_line(claim.get("summary")) or "not found in sources", ""] + evidence_lines(claim.get("evidence"), row)


def render_failed(row):
    return "\n".join([
        "# {}".format(row["name"]),
        "",
        "**No call.** The analysis failed, so this company was not scored.",
        "",
        "Error: `{}`".format(one_line(row.get("analysis_error"))[:300]),
        "",
        "[HN launch]({})".format(row.get("hn_url")),
        "",
    ] + (['Matched topic "{}": "...{}..."'.format(row["topic"], one_line(row["topic_match"])), ""]
         if row.get("topic_match") else []))


def render_memo(row):
    a = row["analysis"]
    check = row.get("quote_check") or {"verified": 0, "total": 0}

    links = ["[HN launch]({}) ({} points, {} comments, {})".format(
        row["hn_url"], row.get("points"), row.get("num_comments"), (row.get("created_at") or "")[:10])]
    links.append("[website]({})".format(row["site_url"]) if row.get("site_url") else "no website (text-only launch)")
    if row.get("github"):
        g = row["github"]
        links.append("[GitHub](https://github.com/{}) ({} stars, last commit {})".format(
            g["repo"], g.get("stars"), (g.get("last_commit_date") or "unknown")[:10]))

    out = [
        "# {}".format(row["name"]),
        "",
        "**{}** | {}/100 | {} | YC {}".format(
            row["verdict"], row["score"], row["thesis_fit"], row.get("yc_batch") or "unknown"),
        "",
        "> {}".format(one_line(a.get("case_summary"))),
        "",
        "**Why this call:** {} ({}). {}".format(
            row["verdict_rule"], row["thesis_fit_rule"], one_line((a.get("business_model") or {}).get("summary"))),
        "",
    ] + evidence_lines((a.get("business_model") or {}).get("evidence"), row) + [
        "",
        " | ".join(links),
        "",
    ] + ([
        '**Why it matched "{}":** "...{}..." ([HN post]({}))'.format(
            row["topic"], one_line(row["topic_match"]), row["hn_url"]),
        "",
    ] if row.get("topic_match") else []) + [
        "{} of {} supporting quotes were found word for word in the sources.".format(
            check["verified"], check["total"]),
        "",
        "## Scores",
        "",
        "| | Score | Why |",
        "|---|---|---|",
    ]
    for key, label in SCORE_LABELS:
        s = a["scores"][key]
        out.append("| {} | {}/25 | {} |".format(label, s["score"], cell(s.get("why"))))

    out += ["", "<details><summary>Quotes behind the scores</summary>", ""]
    for key, label in SCORE_LABELS:
        out += ["**{}**".format(label), ""] + evidence_lines(a["scores"][key].get("evidence"), row) + [""]
    out += ["</details>", "", "## Team", ""] + claim_block(a.get("team"), row)
    out += ["", "## Product", ""] + claim_block(a.get("product"), row)

    market = a.get("market") or {}
    competitors = market.get("competitors") or {}
    names = ", ".join(n for n in competitors.get("names") or [] if n)
    out += ["", "## Market", "", "**Size:** " + " ".join(claim_block(market.get("size_hint"), row)[:1])]
    out += evidence_lines((market.get("size_hint") or {}).get("evidence"), row)
    out += ["", "**Competitors:** " + (names + ". " if names else "") + one_line(competitors.get("summary"))]
    out += evidence_lines(competitors.get("evidence"), row)
    out += ["", "**Why now:** " + " ".join(claim_block(market.get("why_now"), row)[:1])]
    out += evidence_lines((market.get("why_now") or {}).get("evidence"), row)

    out += ["", "## Risks", ""]
    for risk in a.get("risks") or []:
        out.append("- {}".format(one_line((risk or {}).get("risk"))))
        out += evidence_lines((risk or {}).get("evidence"), row, indent="  ")
    if not a.get("risks"):
        out.append("- not found in sources")

    out += ["", "## What would change the call", ""]
    out += ["- {}".format(one_line(x)) for x in a.get("would_change_my_mind") or []] or ["- none given"]
    out += ["", "## Data gaps", ""]
    out += ["- {}".format(one_line(x)) for x in a.get("data_gaps") or []] or ["- none noted"]

    unverified = check.get("unverified") or []
    if unverified:
        out += ["", "## Quotes that failed the source check", ""]
        out += ['- {} ({}): "{}"'.format(u["claim"], u["source"], one_line(u["quote"])) for u in unverified]

    out += ["", "---", "", "*Generated by src/memo.py from data/analyses.jsonl. Analysis model: {}.*".format(
        row.get("model") or "unknown"), ""]
    return "\n".join(out)


def render_index(rows):
    analysed = [r for r in rows if r.get("analysis")]
    failed = [r for r in rows if not r.get("analysis")]
    analysed.sort(key=lambda r: (VERDICT_ORDER.get(r["verdict"], 9), -(r["score"] or 0)))

    counts = {v: sum(1 for r in analysed if r["verdict"] == v) for v in VERDICT_ORDER}
    thesis = next((r.get("thesis") for r in rows if r.get("thesis")), None)
    model = next((r.get("model") for r in rows if r.get("model")), "unknown")

    out = ["# Candidate memos", ""]
    if thesis:
        out += ["**Thesis:** {}".format(thesis), ""]
    out += [
        "{} companies: {} Take a meeting, {} Watch, {} Pass{}. Analysis model: {}.".format(
            len(rows), counts["Take a meeting"], counts["Watch"], counts["Pass"],
            ", {} failed".format(len(failed)) if failed else "", model),
        "",
        "Fit and verdicts are set by rule, not by the model. The model classifies what customers "
        "pay for and what the product is; companies paid for physical goods or services, or "
        "outside AI infrastructure and engineering software, are off-thesis. Off-thesis is always "
        "Pass; on-thesis is Take a meeting at 75+, Watch at 60-74, Pass below 60.",
        "",
        "| # | Company | Verdict | Score | Fit | Case | Quotes checked |",
        "|---|---|---|---|---|---|---|",
    ]
    for i, r in enumerate(analysed, 1):
        check = r.get("quote_check") or {"verified": 0, "total": 0}
        out.append("| {} | [{}]({}.md) | {} | {} | {} | {} | {}/{} |".format(
            i, r["name"], safe_filename(r["name"]), r["verdict"], r["score"],
            r["thesis_fit"], cell(r["analysis"].get("case_summary")),
            check["verified"], check["total"]))
    for r in failed:
        out.append("| - | [{}]({}.md) | No call | - | - | analysis failed | - |".format(
            r["name"], safe_filename(r["name"])))
    return "\n".join(out) + "\n"


with io.open(INPUT_PATH, encoding="utf-8") as handle:
    rows = [json.loads(line) for line in handle if line.strip()]

os.makedirs(MEMO_DIR, exist_ok=True)
# Rebuilt from scratch each run, so a company dropped from the input leaves no stale memo.
for old in glob.glob(os.path.join(MEMO_DIR, "*.md")):
    os.remove(old)

for row in rows:
    text = render_memo(row) if row.get("analysis") else render_failed(row)
    path = os.path.join(MEMO_DIR, safe_filename(row["name"]) + ".md")
    with io.open(path, "w", encoding="utf-8") as handle:
        handle.write(text)

with io.open(os.path.join(MEMO_DIR, "README.md"), "w", encoding="utf-8") as handle:
    handle.write(render_index(rows))

print("wrote {} memos and {}".format(len(rows), os.path.join(MEMO_DIR, "README.md")))
