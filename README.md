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
- **`Repository/`** — the practice repository participants work in: **`odelab`**, a tiny
  1D ODE integrator with tests, CI, and a few intentionally planted bugs. Published
  separately for participants to fork (kept in sync from here).
- **`research_agentic_coding_workshops.md`** — deep-research report on how other
  agentic-coding workshops are taught; the evidence base for the design.
- **`first_notes.md`** — the original brainstorm.
- **`CLAUDE.md`** — guidance for working on these materials with Claude Code.

## The two repositories

| Repository | Audience | Contents |
|---|---|---|
| `agentic-ai-for-coding-workshop` (this) | co-designers / instructors | everything |
| `odelab` | participants | just `Repository/`, synced via `git subtree` |

The practice code lives here in `Repository/` as the single source of truth. To
re-publish it to the participant repo after changes:

```bash
git subtree push --prefix=Repository odelab main
```

(`odelab` is the git remote pointing at the participant repository.)

## Viewing the slides

See `slides/README.md`. In short: serve `slides/` over HTTP and open `index.html` — press
`S` for the speaker view with notes.

```bash
uv run --no-project python -m http.server 8765   # from slides/
```
