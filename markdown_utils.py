# FPTU EventHub: Safe Markdown Rendering with Bleach Sanitization (Anti-XSS)

import markdown
import bleach

ALLOWED_TAGS = [
    "a", "abbr", "acronym", "b", "blockquote", "code", "em", "i", "li", "ol",
    "pre", "strong", "ul", "h1", "h2", "h3", "h4", "p", "br", "hr", "table",
    "thead", "tbody", "tr", "th", "td", "span", "img"
]

ALLOWED_ATTRIBUTES = {
    "a": ["href", "title", "target", "rel"],
    "abbr": ["title"],
    "acronym": ["title"],
    "img": ["src", "alt", "title", "class", "style"],
    "*": ["class"]
}

def render_safe_markdown(text):
    if not text:
        return ""
    html = markdown.markdown(text, extensions=["fenced_code", "tables", "nl2br"])
    clean_html = bleach.clean(
        html,
        tags=ALLOWED_TAGS,
        attributes=ALLOWED_ATTRIBUTES,
        strip=True
    )
    return bleach.linkify(clean_html)
