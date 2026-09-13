from enrich import github_repo, html_to_text


def test_html_to_text_drops_scripts_and_unescapes():
    markup = "<head><title>x</title></head><script>var a=1;</script><p>Hey HN, we&#x27;re here</p><p>Line two</p>"
    assert html_to_text(markup) == "Hey HN, we're here\n\nLine two"  # paragraphs stay separated


def test_html_to_text_handles_empty():
    assert html_to_text(None) == ""


def test_github_repo_url():
    assert github_repo("https://github.com/Adam-CAD/CADAM") == "Adam-CAD/CADAM"
    assert github_repo("https://github.com/org/repo.git") == "org/repo"


def test_github_org_page_is_not_a_repo():
    assert github_repo("https://github.com/anthropics") == ""


def test_non_github_url():
    assert github_repo("https://speko.ai/") is None
