# Agentic AI for Coding — Workshop

Materials for a ~2-hour, hands-on workshop teaching the basics of **agentic coding with
Claude Code** to computational scientists.

**This is the full design repository** — for people building and delivering the workshop.
Participants don't use this repo; they fork the standalone practice repo **`odelab`**
(see below).

## Contents

- **`slides/`** — the deck as delivered: reveal.js (`index.html` + `styles.css`) themed to
  the University of Stuttgart corporate design. See `slides/README.md`.
- **`Presentation/`** — the timed run-sheet (`workshop_plan.md`), the instructor answer key
  (`instructor_notes.md`), and the original Marp deck (`slides.md`, `slides.pdf`).
- **`Repository/`** — a **git submodule** pointing at the standalone practice repo
  **`odelab`** (a tiny 1D ODE integrator with tests, CI, and a few intentionally planted
  bugs). `odelab` is the single source of truth; this repo pins a specific commit of it.
- **`research_agentic_coding_workshops.md`** — deep-research report on how other
  agentic-coding workshops are taught; the evidence base for the design.
- **`first_notes.md`** — the original brainstorm.
- **`CLAUDE.md`** — guidance for working on these materials with Claude Code.

## The two repositories

| Repository | Audience | Contents |
|---|---|---|
| `agentic-ai-for-coding-workshop` (this) | co-designers / instructors | everything; `Repository/` is a submodule |
| `odelab` | participants | the practice repo — the single source of truth |

`odelab` is canonical. This repo embeds it at `Repository/` as a **git submodule** pinned
to a specific commit.

**Clone this repo with submodules:**

```bash
git clone --recurse-submodules git@github.com:tobias-fllnr/agentic-ai-for-coding-workshop.git
# already cloned without --recurse-submodules?
git submodule update --init
```

**Change the practice code, then update the pin:**

```bash
cd Repository                                   # this is the odelab checkout
# edit files, then publish to odelab:
git add -A && git commit -m "..." && git push origin main
cd ..
git add Repository && git commit -m "Bump odelab pointer" && git push   # record the new hash
```

Or fast-forward the submodule to odelab's latest `main`:

```bash
git submodule update --remote Repository
git add Repository && git commit -m "Bump odelab pointer" && git push
```

## Viewing the slides

See `slides/README.md`. In short: serve `slides/` over HTTP and open `index.html` — press
`S` for the speaker view with notes.

```bash
uv run --no-project python -m http.server 8765   # from slides/
```
