from html import escape

from markdown import markdown


def render_markdown(markdown_text: str) -> str:
    return markdown(escape(markdown_text))
