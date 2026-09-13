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


def test_pass_leads_with_weakest_score_only(make_analysis):
    r = row("Acme", "Pass", 48, make_analysis)
    r["analysis"]["scores"]["defensibility"].update(score=6, why="Easy to copy.")
    text = render_memo(r)
    assert "> **Held back by defensibility (6/25).** Easy to copy." in text
    assert "For and against." not in text  # the model's summary would repeat it


def test_meeting_shows_model_summary_only(make_analysis):
    text = render_memo(row("Acme", "Take a meeting", 80, make_analysis))
    assert "> For and against." in text
    assert "Held back by" not in text


def test_off_thesis_leads_with_fit_reason(make_analysis):
    r = row("Acme", "Pass", 90, make_analysis, thesis_fit="off-thesis",
            thesis_fit_rule="customers pay for physical goods")
    text = render_memo(r)
    assert "> **Passed as off-thesis:** customers pay for physical goods." in text
    assert "For and against." not in text


def test_exactly_one_summary_paragraph(make_analysis):
    for verdict in ("Take a meeting", "Watch", "Pass"):
        lines = render_memo(row("Acme", verdict, 70, make_analysis)).splitlines()
        assert sum(1 for line in lines if line.startswith(">")) == 1, verdict
