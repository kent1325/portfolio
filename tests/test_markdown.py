from portfolio.markdown import render_markdown


def test_render_markdown_converts_markdown_to_html() -> None:
    html = render_markdown("# Hello\n\nBody text.")

    assert "<h1>Hello</h1>" in html
    assert "<p>Body text.</p>" in html


def test_render_markdown_escapes_html() -> None:
    html = render_markdown("<script>alert('x')</script>")

    assert "<script>" not in html
