"""Lightweight template filters for rendering user-entered content.

Deliberately tiny — avoids pulling in a full Markdown dependency for what is
only ever a paragraph plus an optional bullet list.
"""

import base64

from django import template
from django.utils.html import conditional_escape, format_html, format_html_join
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name="b64email")
def b64email(value):
    """Base64-encode an email so it never appears literally in the HTML source.

    Bots (and Cloudflare's email obfuscator) scan for ``user@domain`` patterns
    and ``mailto:`` links. An opaque base64 blob has neither, so the visible UI
    can never be hijacked by an edge-side obfuscator. Decoded client-side.
    """
    if not value:
        return ""
    return base64.b64encode(str(value).encode("utf-8")).decode("ascii")


@register.filter(name="localize_url")
def localize_url(value, language_code):
    """Rewrite a hardcoded ``/en/`` or ``/fr/`` path segment to the active locale.

    A project demo link that points at ``…/en/`` would otherwise strand a French
    visitor on the English site. Only the first such segment is replaced;
    external links without a locale prefix pass through untouched.
    """
    if not value or language_code not in ("en", "fr"):
        return value
    text = str(value)
    for marker in ("/en/", "/fr/"):
        if marker in text and marker != f"/{language_code}/":
            return text.replace(marker, f"/{language_code}/", 1)
    return value


@register.filter(name="bullets")
def bullets(value):
    """Render plain text where lines starting with '- ' become a <ul>.

    Consecutive non-bullet lines collapse into <p> blocks. All user input is
    HTML-escaped first — only the structural tags we add are trusted.
    """
    if not value:
        return ""

    lines = [ln.rstrip() for ln in str(value).splitlines()]
    blocks = []
    para_buffer = []
    list_buffer = []

    def flush_para():
        if para_buffer:
            text = " ".join(para_buffer)
            blocks.append(format_html('<p class="content-p">{}</p>', text))
            para_buffer.clear()

    def flush_list():
        if list_buffer:
            items = format_html_join(
                "",
                "<li>{}</li>",
                ((conditional_escape(item),) for item in list_buffer),
            )
            blocks.append(format_html('<ul class="content-list">{}</ul>', items))
            list_buffer.clear()

    for line in lines:
        stripped = line.strip()
        if stripped.startswith(("- ", "* ")):
            flush_para()
            list_buffer.append(stripped[2:].strip())
        elif stripped:
            flush_list()
            para_buffer.append(stripped)
        else:
            flush_para()
            flush_list()

    flush_para()
    flush_list()
    return mark_safe("".join(blocks))
