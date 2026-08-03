#!/usr/bin/env python3
"""Turn setup_email.md into HTML you can paste into Thunderbird.

    python3 Presentation/email_to_html.py          # writes Presentation/setup_email.html

Thunderbird composes plain text or HTML, never Markdown, so the Markdown has to be
rendered once up front. Styling is written as inline `style=` attributes rather than a
stylesheet, because mail clients routinely drop <style> blocks — inline attributes are
the only thing that reliably survives Thunderbird, Outlook and webmail.

Everything above the "Hi everyone," line is our own note-to-self and is not sent.
"""

from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent

BLUE = "#004191"  # University of Stuttgart Mittelblau, as in the deck
# Single quotes inside the font stacks: these end up inside style="..." attributes,
# where a double quote would terminate the attribute early.
MONO = "ui-monospace, SFMono-Regular, Menlo, Consolas, monospace"
SANS = "-apple-system, 'Segoe UI', Helvetica, Arial, sans-serif"

BODY_STYLE = f"font-family: {SANS}; font-size: 14px; line-height: 1.55; color: #1a1a1a; max-width: 44em;"
STYLES = {
    "h1": f"font-family: {SANS}; font-size: 19px; font-weight: 700; color: {BLUE}; margin: 0 0 12px;",
    "h2": f"font-family: {SANS}; font-size: 16px; font-weight: 700; color: {BLUE}; margin: 24px 0 8px;",
    "p": "margin: 0 0 11px;",
    "li": "margin: 0 0 5px;",
    "a": f"color: {BLUE};",
}
PRE_STYLE = (
    f"font-family: {MONO}; font-size: 13px; line-height: 1.45; background: #f4f6f8; "
    f"border-left: 3px solid {BLUE}; padding: 10px 13px; margin: 0 0 13px; "
    "white-space: pre; overflow-x: auto;"
)
CODE_IN_PRE_STYLE = f"font-family: {MONO}; font-size: 13px; background: none; padding: 0;"
INLINE_CODE_STYLE = (
    f"font-family: {MONO}; font-size: 13px; background: #eef1f4; "
    "padding: 1px 4px; border-radius: 3px;"
)


def render(markdown: str) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "gfm", "-t", "html5", "--no-highlight", "--wrap=none"],
        input=markdown,
        capture_output=True,
        text=True,
        check=True,
    )
    html = result.stdout

    # Code blocks first, so the <code> inside them is already styled when the
    # inline-code pass runs and can be skipped.
    html = re.sub(
        r"<pre[^>]*>\s*<code[^>]*>",
        f'<pre style="{PRE_STYLE}"><code style="{CODE_IN_PRE_STYLE}">',
        html,
    )
    # Insert the style attribute after the tag name instead of rewriting the whole
    # opening tag — rewriting it would throw away href on <a> and id on <h2>.
    html = re.sub(r"<code(?! style)(?![\w-])", f'<code style="{INLINE_CODE_STYLE}"', html)
    for tag, style in STYLES.items():
        html = re.sub(rf"<{tag}(?! style)(?![\w-])", f'<{tag} style="{style}"', html)
    return f'<div style="{BODY_STYLE}">\n{html}</div>\n'


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, default=HERE / "setup_email.md")
    parser.add_argument("-o", "--output", type=Path, default=HERE / "setup_email.html")
    args = parser.parse_args()

    text = args.input.read_text(encoding="utf-8")
    start = text.find("Hi everyone,")
    if start == -1:
        print(f'no "Hi everyone," line found in {args.input}', file=sys.stderr)
        return 1

    body = text[start:]
    # An unbracketed <SLIDES LINK> would be parsed as an HTML tag and vanish.
    body = body.replace("<SLIDES LINK>", "PASTE-LINK-HERE")

    args.output.write_text(render(body), encoding="utf-8")
    print(f"{args.output}: paste into Thunderbird via Insert > HTML")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
