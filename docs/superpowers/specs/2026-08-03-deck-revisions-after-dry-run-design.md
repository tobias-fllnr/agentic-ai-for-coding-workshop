# Deck revisions after the first dry run — design

Date: 2026-08-03 · Authors: Tobias Fellner, Fabian Zills (decisions), Claude (implementation)

## Context

Tobias walked the whole workshop end to end and found the shape and timing sound. Four
concrete problems came out of that run and the follow-up chat with Fabian:

1. Reasoning effort is unspecified, so participants may run a high-effort model and spend
   the hands-on segments watching the agent think.
2. `odelab` already ships a `CLAUDE.md`. `/init` therefore only offers to tweak it, which
   makes the §3 hands-on step confusing rather than instructive.
3. `gh` is not installed on the ICP machines — `gh pr create` failed in the dry run, so
   §5 Phase 5 cannot run as written.
4. Forking is assumed by the deck (`github.com/<your-user>/odelab`) but never stated as a
   recommendation, and no pre-flight check confirms people are on their own fork.

## Decisions

- **Effort:** Sonnet at `medium` is the workshop setting. The Reasoning-effort box moves
  from §4 to §2 (`Claude Code in 60 seconds`), and §3's first hands-on slide carries the
  concrete tip. Framing is *time*, not abstract quality: more effort means more waiting.
  Named mechanism is `claude --model sonnet --effort medium` — verified against
  `claude --help`, unlike a guessed slash command.
- **`CLAUDE.md` / `/init`:** keep odelab's `CLAUDE.md` as the worked example of a good one.
  The §3 slide is retitled away from the command and towards the file; `/init` is described
  as what you run on a repo that has none, and explicitly *not* run today — by anyone.
- **Phase 5:** a local merge, not a PR. `git switch main` → `git merge --no-ff add-rk4` →
  `git log --oneline --graph`. No `gh`, no push, no auth. The small-reviewable-diff lesson
  stays on the slide; the transport was never the point.
- **`gh`:** demoted to one bullet under §7 "Worth a look next", beside GH Actions
  auto-review and worktrees.
- **Fork:** recommended, not required — stated on the §0 hands-on slide, which also
  absorbs the pre-flight checks (`git remote show origin`, `uv cache dir`) that the setup
  email will list. No separate checklist slide.

## Changes to `slides/index.html`

| Slide | Change |
|---|---|
| `title` (notes), `promise` | "reviewed PR" / "pull request" → "reviewed **change**" |
| `agenda` | §5 row: "plan → TDD → review → PR" → "… → merge" |
| `task-uv` | fork recommendation + `git remote show origin` + `uv cache dir`; notes mention the email checklist |
| `interface` | gains the Reasoning-effort box, reworded around waiting time and `--model` / `--effort` |
| `init` | retitled "Write the map down — `CLAUDE.md`"; reframed around odelab's existing file; "not running it today" |
| `task-explore` | `/init` removed from title and command block; gains the Sonnet/medium tip; "Done when" now ends at reading the repo's `CLAUDE.md` |
| `memory-scopes` (notes) | drop the claim that the PR-label rule "comes back in §5" |
| `permissions` | Reasoning-effort box removed; retitled "Permissions"; notes updated |
| `phase-ship` | "A small, targeted PR" → "Land it on `main`"; merge commands; PR named as the same discipline with a remote (§7); obsolete `gh auth login` / label-precreation notes deleted |
| `task-ship` | "Open the PR" → "Merge it"; merge commands; fast-finisher bug hunt unchanged |
| `further` | new bullet: `gh` CLI — let Claude open, read and comment on PRs |
| `cheatsheet` | `ship → gh pr create --label` → `ship → merge to main`; `gh` install dropped from the footnote |

## Changes to root `CLAUDE.md`

- Open item "GitHub flow specifics: fork-per-participant vs shared org repo…" → recorded
  as resolved: fork recommended but optional, §5 ends in a local merge, `gh`/PRs are a §7
  pointer.
- "Models & reasoning effort — resolved: folded into §4" → §2.
- "Content to cover" PR bullet: small reviewable diffs, landed by a local merge in-session.
- `Repository/` description: note that odelab's `CLAUDE.md` is itself teaching material.

## Out of scope

`Presentation/slides.md`, `workshop_plan.md` and `instructor_notes.md` remain stale on all
of the above (they still promise "a green-tested, reviewed PR on the participant's fork").
The delivered deck is `slides/index.html`; `Presentation/` is archived source material and
is deliberately left alone.

## Verification

Slides are static HTML with no build step, so: the file parses as HTML, every `<section>`
still opens and closes, no `gh` remains outside §7, no "pull request"/"PR" promise remains
outside §7, and the deck still loads in a browser with all 53 slides.
