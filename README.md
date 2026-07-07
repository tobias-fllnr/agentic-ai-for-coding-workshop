# Agentic AI for Coding — Workshop

Materials for a ~2-hour, hands-on workshop teaching the basics of **agentic coding with
Claude Code** to computational scientists.

**This is the full design repository** — for people building and delivering the workshop.
Participants don't use this repo; they fork the standalone practice repo **`odelab`**
(see below).

## Contents

- **`Presentation/`** — the slide deck (`slides.md`, rendered `slides.pdf`), the timed
  run-sheet (`workshop_plan.md`), the instructor answer key (`instructor_notes.md`), and
  build/preview instructions (`README_slides.md`).
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

## Building the slides

See `Presentation/README_slides.md`. In short: open `Presentation/slides.md` with the
"Marp for VS Code" extension, or export a PDF with marp-cli.
