import os
import sys

import pytest

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", "src"))


@pytest.fixture
def make_analysis():
    """Build a minimal analysis dict shaped like a valid Gemini reply."""
    def build(pay_for="software", category="ai_infrastructure", scores=(15, 15, 15, 15)):
        keys = ("founder_depth", "shipping_evidence", "demand_signal", "defensibility")
        return {
            "business_model": {"customers_pay_for": pay_for, "category": category,
                               "summary": "What it is.", "evidence": []},
            "team": {"summary": "Two founders.", "evidence": []},
            "product": {"summary": "An API.", "evidence": []},
            "market": {k: {"summary": "not found in sources", "evidence": []}
                       for k in ("size_hint", "competitors", "why_now")},
            "risks": [],
            "scores": {k: {"score": s, "why": "because", "evidence": []} for k, s in zip(keys, scores)},
            "case_summary": "For and against.",
            "would_change_my_mind": ["a", "b"],
            "data_gaps": [],
        }
    return build
