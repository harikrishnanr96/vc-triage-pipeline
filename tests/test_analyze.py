import json

import pytest

from analyze import decide, fit_from_business_model, parse_response, quote_found, retry_delay_seconds, source_sections


# --- parsing Gemini's reply ---

def test_parse_valid_reply(make_analysis):
    data, error = parse_response(json.dumps(make_analysis()))
    assert error is None and data["case_summary"] == "For and against."


def test_parse_strips_markdown_fences(make_analysis):
    data, error = parse_response("```json\n" + json.dumps(make_analysis()) + "\n```")
    assert error is None


def test_parse_rejects_broken_json():
    # The shape of RonanRX's real failure: a list closed with } instead of ].
    data, error = parse_response('{"risks": [{"risk": "x"}}, "scores": {}}')
    assert data is None and error.startswith("invalid JSON")


@pytest.mark.parametrize("breakage, expected", [
    (lambda a: a.pop("data_gaps"), "missing keys: data_gaps"),
    (lambda a: a["market"].pop("why_now"), "market is missing: why_now"),
    (lambda a: a["business_model"].update(category="robotics"), "business_model.category must be one of"),
    (lambda a: a["scores"]["defensibility"].update(score="high"), "scores.defensibility.score is not a number"),
])
def test_parse_rejects_unusable_shapes(make_analysis, breakage, expected):
    analysis = make_analysis()
    breakage(analysis)
    data, error = parse_response(json.dumps(analysis))
    assert data is None and error.startswith(expected)


# --- thesis fit and verdict rules ---

@pytest.mark.parametrize("pay_for, category, fit", [
    ("physical_goods", "engineering_software", "off-thesis"),   # ProvenMetal: plugins, but paid per board order
    ("services", "ai_infrastructure", "off-thesis"),
    ("software", "hardware", "off-thesis"),
    ("software", "other", "off-thesis"),
    ("software", "ai_infrastructure", "on-thesis"),
    ("ip_or_research", "ai_for_technical_domain", "on-thesis"),  # Discovered Materials
    ("unclear", "engineering_software", "on-thesis"),            # free open-source tools
])
def test_fit_rules(pay_for, category, fit):
    assert fit_from_business_model({"customers_pay_for": pay_for, "category": category})[0] == fit


@pytest.mark.parametrize("scores, verdict", [
    ((19, 19, 19, 18), "Take a meeting"),  # 75
    ((19, 19, 19, 17), "Watch"),           # 74
    ((15, 15, 15, 15), "Watch"),           # 60
    ((15, 15, 15, 14), "Pass"),            # 59
])
def test_verdict_cutoffs(make_analysis, scores, verdict):
    assert decide(make_analysis(scores=scores))["verdict"] == verdict


def test_off_thesis_is_pass_even_with_top_scores(make_analysis):
    result = decide(make_analysis(pay_for="physical_goods", scores=(25, 25, 25, 25)))
    assert result["score"] == 100 and result["verdict"] == "Pass"


def test_scores_are_clamped_to_0_25(make_analysis):
    assert decide(make_analysis(scores=(40, -5, 10, 10)))["score"] == 45


# --- quote checking ---

ROW = {
    "name": "Example", "points": 10, "num_comments": 2,
    "hn_post_text": "Hey HN, we’re Will & Johnny. We charge a simple margin on the order value.",
    "hn_comments": [{"author": "m_w_", "created_at": "2026-07-09", "text": "Unclear what difference exists against Firecrawl"}],
    "site_text": "Get a Quote", "site_url": "https://example.com", "github": None,
}


@pytest.mark.parametrize("item, found", [
    ({"source": "hn_post", "quote": "We charge a simple margin on the order value."}, True),
    ({"source": "hn_post", "quote": "we're Will & Johnny"}, True),                       # straight vs curly apostrophe
    ({"source": "hn_post", "quote": "Hey HN, ... a simple margin"}, True),               # ellipsis cut
    ({"source": "comments", "author": "m_w_", "quote": "against Firecrawl"}, True),
    ({"source": "comments", "author": "someone_else", "quote": "against Firecrawl"}, False),
    ({"source": "site", "quote": "We charge a simple margin"}, False),                  # wrong section
    ({"source": "hn_post", "quote": "We charge a fixed fee per order"}, False),         # paraphrase
    ({"source": "hn_post", "quote": ""}, False),
])
def test_quote_found(item, found):
    assert quote_found(item, source_sections(ROW), ROW) is found


# --- rate limits ---

def test_retry_delay_read_from_error_text():
    assert retry_delay_seconds(Exception("429 ... retry_delay {\n  seconds: 38\n}")) == 40
    assert retry_delay_seconds(Exception("429 quota exceeded"), default=30) == 30


def test_fit_rule_reads_as_plain_words():
    _, rule = fit_from_business_model({"customers_pay_for": "unclear", "category": "engineering_software"})
    assert rule == "engineering software; no revenue model stated yet"
