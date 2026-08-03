#!/usr/bin/env python3
"""Convert the reveal.js deck into a readable Markdown handout.

    python3 slides/to_markdown.py            # writes slides/deck.md
    python3 slides/to_markdown.py -o out.md

`index.html` is the source of truth; this script is a one-way export, so re-run it
after editing the deck. It needs `pandoc` on PATH for the inline conversion and
nothing else.

The deck's markup is regular, which is what makes this possible: one top-level
`<section>` per slide, `p.eyebrow` for the section label, `h1`/`h2` for the title,
`aside.notes` for the speaker notes. The recurring visual idioms — cards, phase
rails, terminal transcripts, "Done when" bars — are rewritten into Markdown
equivalents before pandoc sees them, because pandoc alone would leave the wrapper
divs behind and silently turn the speaker notes into body text.
"""

from __future__ import annotations

import argparse
import html
import re
import subprocess
import sys
import textwrap
from pathlib import Path

HERE = Path(__file__).resolve().parent

SECTION_RE = re.compile(r"^<section\b([^>]*)>\n(.*?)^</section>", re.S | re.M)
NOTES_RE = re.compile(r'<aside class="notes">(.*?)</aside>', re.S)
SVG_RE = re.compile(r"<svg\b.*?</svg>", re.S)
TERM_RE = re.compile(r'<p class="term"[^>]*>(.*?)</p>', re.S)
RAIL_RE = re.compile(r'<ul class="rail">(.*?)</ul>', re.S)
RAIL_ITEM_RE = re.compile(r'<li(?:\s+class="([^"]*)")?>(.*?)</li>', re.S)
CARD_RE = re.compile(r'<div class="card([^"]*)"[^>]*>(.*?)</div>', re.S)
FIX_RE = re.compile(
    r'<div class="fix">\s*<p class="pat">(.*?)</p>\s*<p class="rem">(.*?)</p>\s*</div>', re.S
)
SPAN_RE = re.compile(r"</?span[^>]*>")
H3_RE = re.compile(r"<h3[^>]*>(.*?)</h3>", re.S)
VERDICT_RE = re.compile(r'<span class="verdict">(.*?)</span>', re.S)
DL_RE = re.compile(r'<dl class="kv"[^>]*>(.*?)</dl>', re.S)
DT_DD_RE = re.compile(r"<dt>(.*?)</dt><dd>(.*?)</dd>", re.S)
FOOTNOTE_RE = re.compile(r'<p class="footnote"[^>]*>(.*?)</p>', re.S)
DONE_RE = re.compile(
    r'<p class="done[^"]*">\s*<span class="done-label">(.*?)</span>(.*?)</p>', re.S
)
EYEBROW_RE = re.compile(r'<p class="eyebrow">(.*?)</p>', re.S)
CHIP_RE = re.compile(r'<span class="chip">(.*?)</span>', re.S)
HEADING_RE = re.compile(r"<(h1|h2)[^>]*>(.*?)</\1>", re.S)
SECNUM_RE = re.compile(r'<p class="sec-num">(.*?)</p>', re.S)
IMG_RE = re.compile(r"<img\b[^>]*>")
PRE_RE = re.compile(r"(<pre[^>]*>\s*<code[^>]*>)(.*?)(</code>\s*</pre>)", re.S)
CARD_ITEM_RE = re.compile(r'(<li class="card-item">.*?</li>\s*)+', re.S)
TAG_RE = re.compile(r"<[^>]+>")
ID_RE = re.compile(r'id="([^"]+)"')
CLASS_RE = re.compile(r'class="([^"]+)"')


def inline_md(fragment: str) -> str:
    """Flatten a title-sized HTML fragment to Markdown by hand.

    Titles only ever contain <code>, <strong>, <em> and <br/>, so a full pandoc
    round-trip per heading would be 53 subprocesses for no gain.
    """
    text = re.sub(r"<br\s*/?>", " ", fragment)
    text = re.sub(r"<code[^>]*>(.*?)</code>", r"`\1`", text, flags=re.S)
    text = re.sub(r"<strong[^>]*>(.*?)</strong>", r"**\1**", text, flags=re.S)
    text = re.sub(r"<em[^>]*>(.*?)</em>", r"*\1*", text, flags=re.S)
    text = TAG_RE.sub("", text)
    return html.unescape(text).strip()


def plain(fragment: str) -> str:
    """Strip a fragment to bare text, preserving <br/> as newlines."""
    text = re.sub(r"<br\s*/?>", "\n", fragment)
    text = TAG_RE.sub("", text)
    return html.unescape(text).strip()


def inline_html(fragment: str) -> str:
    """Collapse whitespace but keep inline tags, so pandoc can still see them.

    Used wherever slide content is re-parented into a list item: stripping tags here
    would throw away the <code> and <strong> that carry meaning.
    """
    return " ".join(fragment.split())


def flatten_paragraphs(fragment: str) -> str:
    """One line of inline HTML from a fragment of several <p> elements.

    A card body becomes a single list item, so its paragraphs have to join up; left
    as <p> they would turn every card into a loose list with a nested block.
    """
    fragment = re.sub(r"<br\s*/?>", " ", fragment)
    pieces = []
    for piece in fragment.split("</p>"):
        piece = re.sub(r"<p\b[^>]*>", "", piece)
        piece = inline_html(piece)
        if piece:
            pieces.append(piece)
    return " · ".join(pieces)


def term_text(fragment: str) -> str:
    """Bare text for a terminal transcript: one source line per <br/>.

    The HTML indents for readability and pads with &nbsp; for alignment. Drop the
    former, keep the latter — which is why leading ASCII spaces go before the
    non-breaking ones are turned into ordinary spaces.
    """
    lines = []
    for line in plain(fragment).splitlines():
        line = line.rstrip().lstrip(" \t").replace("\xa0", " ")
        if line.strip():
            lines.append(line)
    return "\n".join(lines)


def normalise_idioms(body: str) -> str:
    """Rewrite the deck's visual conventions into markup pandoc handles well."""
    body = SVG_RE.sub("", body)
    body = IMG_RE.sub("", body)

    # Terminal transcripts are styled paragraphs with <br/> and colour spans;
    # as a code block they read the way they look on the slide.
    body = TERM_RE.sub(
        lambda m: f"<pre><code>{html.escape(term_text(m.group(1)))}</code></pre>", body
    )

    # The phase rail is a progress indicator: one line, current phase bolded.
    def rail(match: re.Match[str]) -> str:
        steps = []
        for classes, label in RAIL_ITEM_RE.findall(match.group(1)):
            name = plain(label)
            steps.append(f"<strong>{name}</strong>" if "is-active" in classes else name)
        return "<p>" + " &rarr; ".join(steps) + "</p>" if steps else ""

    body = RAIL_RE.sub(rail, body)

    # A verdict span is the punchline of the card it sits in.
    body = VERDICT_RE.sub(lambda m: f" &mdash; <em>{inline_html(m.group(1))}</em>", body)

    # The §6 pitfall rows are a pattern paired with its fix.
    body = FIX_RE.sub(
        lambda m: f'<li class="card-item"><strong>{inline_html(m.group(1))}</strong>'
        f" &mdash; {inline_html(m.group(2))}</li>",
        body,
    )

    # Cards are a heading plus a sentence or two; a bullet keeps that pairing.
    def card(match: re.Match[str]) -> str:
        inner = match.group(2)
        title = H3_RE.search(inner)
        rest = flatten_paragraphs(H3_RE.sub("", inner))
        if title:
            return (
                f'<li class="card-item"><strong>{inline_html(title.group(1))}</strong>'
                f" &mdash; {rest}</li>"
            )
        return f'<li class="card-item">{rest}</li>'

    # Cards nest inside grid wrappers, so convert innermost-first until stable.
    while True:
        new = CARD_RE.sub(card, body)
        if new == body:
            break
        body = new
    # Only wrap the items this function created; a real <ul> already has its own.
    body = CARD_ITEM_RE.sub(lambda m: f"<ul>{m.group(0)}</ul>", body)

    # Definition lists have no GFM equivalent; bullets do.
    def deflist(match: re.Match[str]) -> str:
        rows = DT_DD_RE.findall(match.group(1))
        items = "".join(
            f"<li><strong>{inline_html(dt)}</strong> &mdash; {inline_html(dd)}</li>"
            for dt, dd in rows
        )
        return f"<ul>{items}</ul>"

    body = DL_RE.sub(deflist, body)

    body = DONE_RE.sub(
        lambda m: f"<p><strong>{plain(m.group(1))}:</strong> {inline_html(m.group(2))}</p>",
        body,
    )
    # Footnotes read as fine print, so italicise the whole line — but an <em> inside
    # would close the outer emphasis early, so flatten any nested one first.
    body = FOOTNOTE_RE.sub(
        lambda m: f"<p><em>{re.sub(r'</?em>', '', m.group(1))}</em></p>", body
    )

    # Whatever spans are left are purely decorative (arrows, ticks, terminal colours);
    # unwrap them once everything that keys off a span class has run.
    body = SPAN_RE.sub("", body)

    # <pre> keeps the source file's indentation and data-trim's trailing blank line.
    body = PRE_RE.sub(
        lambda m: m.group(1) + textwrap.dedent(m.group(2)).strip("\n") + m.group(3), body
    )
    return body


def pandoc(fragment: str) -> str:
    result = subprocess.run(
        ["pandoc", "-f", "html", "-t", "gfm", "--wrap=none"],
        input=fragment,
        capture_output=True,
        text=True,
        check=True,
    )
    out = result.stdout
    # Drop the wrapper divs pandoc faithfully preserves, and its empty-div markers.
    out = re.sub(r"^</?div[^\n]*$", "", out, flags=re.M)
    out = re.sub(r"^<!-- -->$", "", out, flags=re.M)
    out = re.sub(r"^``` (\w+)$", r"```\1", out, flags=re.M)
    out = re.sub(r"\n{3,}", "\n\n", out)
    return out.strip()


def convert_slide(attrs: str, raw: str, number: int) -> str:
    classes = (CLASS_RE.search(attrs) or re.match("", "")).group(1) if CLASS_RE.search(attrs) else ""
    slide_id = ID_RE.search(attrs).group(1) if ID_RE.search(attrs) else f"slide-{number}"

    notes_match = NOTES_RE.search(raw)
    notes = " ".join(plain(notes_match.group(1)).split()) if notes_match else ""
    body = NOTES_RE.sub("", raw)

    eyebrow_match = EYEBROW_RE.search(body)
    eyebrow = plain(eyebrow_match.group(1)) if eyebrow_match else ""
    body = EYEBROW_RE.sub("", body)

    secnum_match = SECNUM_RE.search(body)
    secnum = plain(secnum_match.group(1)) if secnum_match else ""
    body = SECNUM_RE.sub("", body)

    hands_on = bool(CHIP_RE.search(body))
    body = CHIP_RE.sub("", body)

    heading_match = HEADING_RE.search(body)
    title = inline_md(heading_match.group(2)) if heading_match else slide_id
    if heading_match:
        body = body.replace(heading_match.group(0), "", 1)

    label = " · ".join(x for x in (secnum or eyebrow,) if x)
    parts = [x for x in (label, title) if x]
    heading = " — ".join(parts) if len(parts) == 2 else (parts[0] if parts else slide_id)
    if hands_on:
        heading += "  ·  *your turn*"

    is_divider = "section-divider" in classes or "title-slide" in classes
    level = "#" if is_divider else "##"

    out = [f"{level} {heading}", ""]
    converted = pandoc(normalise_idioms(body))
    if converted:
        out += [converted, ""]
    if notes:
        out += [f"> **Notes:** {notes}", ""]
    return "\n".join(out)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("-i", "--input", type=Path, default=HERE / "index.html")
    parser.add_argument("-o", "--output", type=Path, default=HERE / "deck.md")
    args = parser.parse_args()

    source = args.input.read_text(encoding="utf-8")
    slides = SECTION_RE.findall(source)
    if not slides:
        print(f"no <section> slides found in {args.input}", file=sys.stderr)
        return 1

    chunks = [
        "# Agentic AI for Coding — deck as text",
        "",
        f"Exported from `{args.input.name}` by `to_markdown.py` — {len(slides)} slides. "
        "The deck is the source of truth; re-run the script instead of editing this file.",
        "",
        "---",
        "",
    ]
    for number, (attrs, raw) in enumerate(slides):
        chunks.append(convert_slide(attrs, raw, number))
        chunks.append("---")
        chunks.append("")

    args.output.write_text("\n".join(chunks).rstrip() + "\n", encoding="utf-8")
    print(f"{args.output}: {len(slides)} slides")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
