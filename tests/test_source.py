from source import parse_title, topic_match, topic_words


def test_parse_title_with_batch_and_dash():
    assert parse_title("Launch HN: Bullet (YC S26) – A Faster Coding Agent") == (
        "Bullet", "S26", "A Faster Coding Agent")


def test_parse_title_without_separator():
    # Real title from the dataset: no dash between the batch and the tagline.
    assert parse_title("Launch HN: ProvenMetal (YC S26) delivers circuit boards in days") == (
        "ProvenMetal", "S26", "delivers circuit boards in days")


def test_parse_title_without_batch():
    assert parse_title("Launch HN: Freestyle – Sandboxes for Coding Agents") == (
        "Freestyle", None, "Sandboxes for Coding Agents")


def test_topic_words_drop_filler():
    assert topic_words("AI agents for SMBs") == ["ai", "agents", "smbs"]


def hit(text, title="Launch HN: Example"):
    return {"title": title, "story_text": text}


def test_topic_match_requires_every_word():
    words = topic_words("voice AI")
    assert topic_match(hit("We build voice agents with AI"), words)
    assert topic_match(hit("We build voice agents"), words) is None


def test_topic_match_is_whole_word():
    # "ai" inside "email" must not count.
    assert topic_match(hit("An email client"), ["ai"]) is None


def test_topic_match_plural_topic_finds_singular_text():
    assert topic_match(hit("an <b>agent</b> for every SMB"), topic_words("agents for SMBs"))
    assert topic_match(hit("small business owners"), topic_words("businesses"))


def test_topic_match_returns_snippet_around_match():
    snippet = topic_match(hit("Intro text. One MCP server for everything."), ["mcp"])
    assert "One MCP server" in snippet
