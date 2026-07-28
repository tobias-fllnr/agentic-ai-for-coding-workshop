# Slides — preview & export

The deck is a single self-contained [Marp](https://marp.app/) file: `slides.md`
(dark theme + speaker notes embedded; no external assets).

## Preview live (recommended while editing)

- **VS Code:** install the **"Marp for VS Code"** extension, open `slides.md`, click the
  preview icon. Speaker notes and per-slide layout render as you type — ideal for
  live-editing during the workshop.

## Export

Needs Node (uses `npx`, no install):

```bash
# HTML (has a presenter view — press "p" in the browser)
npx @marp-team/marp-cli@latest slides.md -o slides.html

# PDF
npx @marp-team/marp-cli@latest slides.md --pdf -o slides.pdf

# PDF with speaker notes included
npx @marp-team/marp-cli@latest slides.md --pdf --pdf-notes -o slides-notes.pdf

# PowerPoint (if you must)
npx @marp-team/marp-cli@latest slides.md --pptx -o slides.pptx
```

## Conventions in this deck

- **Speaker notes** live in `<!-- ... -->` comments (Marp presenter view / `--pdf-notes`).
- **Section dividers** use `<!-- _class: divider -->`; **task cards** use `<!-- _class: task -->`.
- The per-section **footer** (`§N · topic`) is set once per section via
  `<!-- footer: '...' -->` and carries forward.
- Timings are kept out of the deck on purpose — they live in `workshop_plan.md`. The
  answer key for the practice repo is in `instructor_notes.md`.
