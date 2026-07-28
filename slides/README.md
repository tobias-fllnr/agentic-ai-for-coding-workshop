# Slides — preview, present & export

The deck is [reveal.js](https://revealjs.com/) 5 loaded from a CDN: `index.html` plus
`styles.css`. No build step. The only local assets are `fonts/` and `images/`.

## Preview

The fonts load from `fonts/`, so serve the folder:

```bash
uv run --no-project python -m http.server 8765   # from slides/
# → http://127.0.0.1:8765/index.html
```

Live-editing works the same way: save `index.html` or `styles.css`, reload the page.

## Presenting

- **`S`** — speaker view: notes, timer, next slide. Every slide carries notes.
- **`Esc`** / **`O`** — slide overview, to jump between sections.
- **`B`** — blank the screen while people work.
- **`F`** — fullscreen. Arrows or space to advance.

The deck is deliberately linear — `→` walks every slide in order.

## Export

```bash
npx decktape reveal "http://127.0.0.1:8765/index.html?print-pdf" slides.pdf
```

## Theme

University of Stuttgart corporate design:

| Token | Value | Use |
|---|---|---|
| `--blue` | `#004191` Mittelblau | headings, rules, section dividers |
| `--cyan` | `#00BEFF` Hellblau | accents, active rail dot, bullets |
| `--ink` | `#323232` Anthracite | body text |
| `--go` | `#59B200` | hands-on slides only |
| `--err` | `#d90000` | the call you have to make yourself |

Type is **Uni Stuttgart Sans** — the university's own license-free web font, self-hosted
in `fonts/`, Light + Bold only — with JetBrains Mono for code.

## Conventions in this deck

- **Speaker notes** live in `<aside class="notes">`.
- **Section dividers** — `class="section-divider" data-state="is-divider"`; the
  `<p class="sec-num">` is the bled watermark numeral, clipped by `overflow: hidden`.
- **Hands-on slides** — `class="task"` gives the green spine and the `YOUR TURN` chip.
  Each ends with `<p class="done push">`: the *Done when* contract, pinned to the bottom.
- **The phase rail** — `<ul class="rail">` with `is-active` / `is-done` on the `<li>`s.
  It appears only where it carries information: the agent loop in §1 and the five §5
  phases. Keep it that way.
- **Terminal transcripts** — `<p class="term">` with `.p` `.c` `.ok` `.bad` `.add` `.del`
  spans. Real code blocks use `<pre><code class="language-bash">` and highlight.js.
- **Comparison pairs** — `.card go` and `.card stop` with a `<span class="verdict">` for the
  ruling. Used where the point is *which of these two matters*.
- **`.flow`** — the copy-and-paste row in §1, `.flow-node` / `.flow-node fill` / `.flow-arrow`.
  One slide only; the rail is the deck's diagram idiom.
- **Citations** — `.cite` superscript, or a `.footnote` with the arXiv id.
- Content sits in `<div class="content">` and is vertically centred; anything with
  `class="push"` pins an element to the bottom.
- Timings are kept out of the deck on purpose — they live in
  `../Presentation/workshop_plan.md`. The answer key for the practice repo is in
  `../Presentation/instructor_notes.md`.

## Facts with an expiry date

The deck makes specific, dated claims on purpose — see slide 4, *This deck has a half-life*.
Re-check these before each delivery, because they move:

- Model generation and the reasoning-effort levels (§4 permissions slide).
- Permission-mode UI labels: the mode whose config value is `default` currently shows as
  **Manual**. These have been renamed before.
- The four links on the tools slide, and the `/plugin install …@claude-plugins-official` syntax.
- The ICP local-model pointer on the privacy slide — URL, model, and Mattermost command.
- Docs live at `code.claude.com/docs`; the old `docs.anthropic.com` paths redirect.
