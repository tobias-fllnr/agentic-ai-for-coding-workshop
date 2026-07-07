# Agentic AI for Coding — Workshop

## Goal

Design a hands-on workshop that teaches the **basic principles of agentic coding with
Claude Code**. Participants should leave able to run a disciplined agent-assisted
workflow (understand a repo → plan → TDD → review → small PR) on their own projects, and
understand how to steer the agent with configuration (CLAUDE.md, skills) and use it safely.

## Audience

- **PhD-level computational physicists.**
- Assume solid Python and git basics; assume **no** prior Claude Code experience.
- Keep the practice material **domain-light** (generic numerics, not deep physics) so
  attention stays on the agentic-coding concepts, not on the science. A light physics
  flavor is fine as long as it never becomes a barrier.

## Format

- **~2 hours total.** No validated pacing benchmark exists for a 2h agentic-coding
  session (comparable full courses run ~6h), so **timing is unproven — plan to cut
  aggressively and pilot it** before delivery.
- **Interleave** short input/lecture sections with longer hands-on sections (not
  lecture-then-practice) where participants work on the practice repository.
- **Demos run live, not slides-only** — the agent making and recovering from mistakes is
  itself the teaching moment.
- **Backbone hands-on exercise:** implement one small feature end-to-end using the full
  **understand repo → plan → TDD → review → small targeted PR** cycle (e.g. via
  `superpowers:brainstorming` then a plan). Everything else is built around making time
  for this. Note: the canonical Anthropic workflow is Explore → Plan → Code → Commit;
  **our TDD and explicit-review steps are deliberate additions** — well-supported, but
  frame them as our emphasis, not the default loop.

## Locked-in design decisions

- **Materials language: English** (slides, repo docs, talking points).
- **Slides: Markdown-based** (Marp or reveal.js) — text/git-friendly, live-editable by
  Claude Code, and can live in the repo. Not PowerPoint/Beamer.
- **Participants arrive fully set up** via a pre-workshop email: Claude Code installed &
  authenticated, GitHub account ready, repo cloned/forked, git + Python basics assumed.
  The workshop does **not** spend live time on install/auth.
- **`uv` is a required thread**: give a short `uv` crash course early (incl. `direnv` +
  `UV_CACHE_DIR`), then use `uv` throughout the practical part.

## Content to cover

Core (input + hands-on):
- **Agent-loop mental model** — introduce `goal → plan → act → observe → revise` by name
  in the opening input section, before any hands-on.
- **Codebase understanding first** — before feature work, have participants ask Claude to
  explain the practice repo (plan-mode exploration / an "explain this repo" opener). Keep
  it short (~5 min, the repo is prepared) but **do not skip it** — it maps to the canonical
  Explore phase.
- `uv` crash course (environments, running, caching; `direnv`, `UV_CACHE_DIR`).
- **CLAUDE.md steering** — demonstrate how instructions change output, e.g. OOP vs
  functional, class-based vs function-scoped tests, dataclasses, docstring style. Teach
  **concision** (bloated CLAUDE.md files get ignored), not completeness.
- **Skills** — install skills, use skills, write your own (e.g. slide style, personal
  conventions for a given topic).
- Permissions / safety modes.
- The understand → plan → TDD → review cycle (the backbone exercise).
- Working in **small, targeted, reviewable PRs** — don't let Claude run free; you won't
  meaningfully review a 1000-line PR.
- **Task triage** — agents excel at small, well-specified tasks and fail on tasks needing
  architectural decisions; teach participants to recognize when *not* to delegate.
- **Common failure patterns** — adopt Anthropic's five named pitfalls: kitchen-sink
  session → `/clear` between tasks; over-correcting → after two failed tries `/clear` and
  reprompt; over-specified CLAUDE.md → prune; trust-then-verify gap → always give a
  verifiable check; infinite exploration → scope narrowly or use subagents.
- ⚠️ **Models & reasoning effort** — NOT found in any existing curriculum. Keep only if we
  justify it as our own differentiator; otherwise fold into a broader "controlling the
  agent" segment or trim. Decide during planning.

Real demo, time permitting (not a throwaway mention):
- **Subagents, hooks, MCP / memory** — Anthropic's own beginner courses treat these as
  core customization, so give them a genuine live demo rather than a passing pointer.

Teaser / pointers only:
- GitHub Actions auto-review + human review.
- git worktrees (keeping this as a teaser is supported by the research).
- Reference: https://claude.com/blog/steering-claude-code-skills-hooks-rules-subagents-and-more

## Project structure

- `first_notes.md` — original brainstorm and idea list. Source material; keep for
  reference, but this `CLAUDE.md` is the current source of truth.
- `research_agentic_coding_workshops.md` — deep-research report on how other agentic-
  coding workshops are taught; the basis for the design decisions above.
- `Repository/` — the practice repository participants work in during the workshop.
  Domain-light generic numerics (e.g. a small numerical routine / integrator), a feature
  to add (e.g. an extra term + a plotting script), and **a few intentionally planted
  bugs** for a debugging exercise. Must be `uv`-managed.
- `Presentation/` — the Markdown slides **plus** the concrete session plan and talking
  points for delivering the workshop.

## Working conventions for future sessions

- Write everything in **English**.
- Prefer `uv` for anything Python in the practice repo; model good agentic-coding
  practice in the materials themselves (small commits, tests, clear structure).
- When designing new workshop material, run it through `superpowers:brainstorming`
  before implementing, per the repo's superpowers setup.

## Open items (resolve before finalizing)

- Exact Markdown slide tool (Marp vs reveal.js) — pick when starting `Presentation/`.
- Realistic per-segment timing for a 2h session — unproven; needs a dry run.
- Fate of the "models & reasoning effort" module (justify, fold, or trim — see above).
- **Scientific-computing angle** — numerical correctness, reproducibility, HPC/SLURM,
  notebooks are uncovered by other workshops. Decide how much to own this; it pairs
  naturally with the `uv` module (reproducibility) and TDD (numerical/property tests as
  the verifiable check).
- GitHub flow specifics: fork-per-participant vs shared org repo, and where PRs target
  (affects the GH Actions auto-review teaser).
- Confirm the pre-workshop setup email contents and send date with organizers.
