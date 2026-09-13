from memo import render_failed, render_index, render_memo


def row(name, verdict, score, make_analysis, **extra):
    analysis = make_analysis()
    analysis["team"]["evidence"] = [{"quote": "made up", "source": "hn_post", "verified": False}]
    base = {
        "name": name, "hn_url": "https://news.ycombinator.com/item?id=1", "site_url": None,
        "points": 1, "num_comments": 0, "created_at": "2026-09-01T00:00:00Z", "github": None,
        "analysis": analysis, "analysis_error": None, "verdict": verdict, "score": score,
        "verdict_rule": "rule", "thesis_fit": "on-thesis", "thesis_fit_rule": "ai infrastructure",
        "quote_check": {"verified": 0, "total": 1, "unverified": []}, "model": "test-model",
    }
    base.update(extra)
    return base


def test_memo_leads_with_the_call(make_analysis):
    text = render_memo(row("Acme", "Watch", 66, make_analysis))
    assert text.splitlines()[2] == "**Watch** | 66/100 | on-thesis | YC unknown"
    assert "no website (text-only launch)" in text


def test_memo_flags_unverified_quotes(make_analysis):
    assert "(not found word for word in this source)" in render_memo(row("Acme", "Watch", 66, make_analysis))


def test_memo_shows_topic_match(make_analysis):
    text = render_memo(row("Acme", "Watch", 66, make_analysis, topic="MCP", topic_match="One MCP server"))
    assert 'Why it matched "MCP"' in text


def test_failed_analysis_gets_no_call_page():
    text = render_failed({"name": "Broken", "hn_url": "u", "analysis_error": "API error:\n429"})
    assert "**No call.**" in text and "API error: 429" in text


def test_index_ranks_by_verdict_then_score(make_analysis):
    rows = [
        row("PassCo", "Pass", 90, make_analysis),
        row("WatchLow", "Watch", 61, make_analysis),
        row("MeetCo", "Take a meeting", 80, make_analysis),
        row("WatchHigh", "Watch", 70, make_analysis),
        {"name": "Broken", "analysis": None, "analysis_error": "x"},
    ]
    order = [line.split("[")[1].split("]")[0] for line in render_index(rows).splitlines() if line.startswith("| ") and "[" in line]
    assert order == ["MeetCo", "WatchHigh", "WatchLow", "PassCo", "Broken"]
