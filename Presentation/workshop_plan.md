# Workshop Session Plan — Agentic AI for Coding

*Concrete run-sheet for the ~2-hour hands-on workshop. Draft for review.*
*Companion to `../CLAUDE.md` (design decisions) and `../research_agentic_coding_workshops.md` (evidence base).*

## At a glance

- **Audience:** PhD-level computational physicists; know Python + git; **no** prior Claude Code.
- **Duration:** 120 min, incl. one 5-min break + 5-min end buffer → **110 min active**.
- **Split:** target ~30% input / ~70% hands-on. This draft lands at **~35% input / ~65% hands-on** (~40 min input / ~70 min hands-on) — realistic for beginners. To hit a strict 30/70, trim the live demo (§1) and framing (§0). See *Timing notes*.
- **Prerequisites (via setup email):** Claude Code installed & authenticated, GitHub account, practice repo forked & cloned, `uv` installed.
- **Backbone deliverable:** each participant ships one small, tested, reviewed **PR** on their fork.
- **Assumed practice example:** a **1D ODE integrator** (see *Repo dependencies*). Swap-safe — task wording adapts if the example changes.

## Timeline

| Clock | # | Section | Format | Min |
|---|---|---|---|---|
| 0:00 | 0 | Welcome & the agent loop | Input | 6 |
| 0:06 | 1 | Live "aha" demo | Demo | 6 |
| 0:12 | 2 | `uv` crash course | Input + hands-on | 12 |
| 0:24 | 3 | Understand the repo | Hands-on | 10 |
| 0:34 | 4 | Steering the agent | Input + hands-on | 16 |
| 0:50 | – | ☕ Stretch break | — | 5 |
| 0:55 | 5 | **Backbone: plan → TDD → review → PR** | Input + hands-on | 46 |
| 1:41 | 6 | Failure-patterns debrief | Input + share | 6 |
| 1:47 | 7 | Advanced demo + teasers + wrap | Demo + input | 8 |
| 1:55 | – | Buffer / Q&A | — | 5 |
| 2:00 | | **End** | | |

---

## §0 — Welcome & the agent loop (6 min · input)

**Goal:** frame the session and give a shared mental model before anyone touches the keyboard.

**Talking points:**
- What "agentic" coding means vs. autocomplete/chat. Introduce the **agent loop** by name: `goal → plan → act → observe → revise`.
- **Vibe-coding vs. disciplined AI-assisted engineering** — *you* stay responsible for architecture and review; the agent does the typing.
- **Task triage** (one line): agents shine on small, well-specified tasks; they struggle on tasks needing architectural judgement. Today's task is deliberately small.
- The promise: *by the end you'll have shipped a small, tested, reviewed PR.*

**Participant task:** none — just confirm Claude Code opens inside the cloned repo.

---

## §1 — Live "aha" demo (6 min · demo)

**Goal:** show the loop in motion; create the "oh, I want that" moment. **Live, not slides** — including a mistake and the agent's recovery.

**Instructor demo (pick one, run at speed):**
- Take a plain throwaway script in the repo and ask Claude to turn it into an `argparse` CLI with type hints and a `--help`, then run it. *(MIT Missing Semester opener — relatable for scientists with ad-hoc scripts.)*
- Or: do one tiny task "by hand vs. by agent" back-to-back to contrast effort.

**Participant task:** watch; jot down one thing they'll try later.

---

## §2 — `uv` crash course (12 min · 4 input / 8 hands-on)

**Goal:** everyone can run, test, and manage the project with `uv`; reproducibility framing.

**Talking points:** why `uv` (fast, reproducible envs, no manual venv juggling). The handful of commands they'll actually use: `uv sync`, `uv run …`, `uv add …`. Briefly: `direnv` + `UV_CACHE_DIR` for auto-activation and a shared cache.

**Participant tasks:**
1. `uv sync` in the repo.
2. `uv run pytest` → watch existing tests pass (green baseline).
3. `uv run python -m <package>` (or the provided entry point) → run the example.
4. `uv add matplotlib` → add the dep you'll use for plotting later.

**Deliverable:** working environment, tests green.

---

## §3 — Understand the repo (10 min · 2 input / 8 hands-on)

**Goal:** the **Explore** step — use the agent to build a mental map before changing anything.

**Talking points:** plan mode (read-only exploration); how to ask the agent to map a codebase; why exploring first beats diving in.

**Participant tasks:**
1. Ask Claude (plan mode): *"Explain this repository — structure, what each module does, how to run it and the tests."*
2. Follow-up: *"Where would I add a new integration method, and what would I need to test?"*

**Deliverable:** participant can describe the repo in their own words and knows where the feature will live.

---

## §4 — Steering the agent (16 min · 6 input / 10 hands-on)

**Goal:** show how configuration changes the agent's behaviour; cover safety.

**Talking points:**
- **CLAUDE.md** — project memory. **Keep it concise** — bloated files get ignored. "Would removing this line cause a mistake? If not, cut it."
- **Skills** — reusable instructions; using existing ones and writing your own (e.g. a personal docstring-style preference).
- **Models & reasoning effort** (folded in) — quick guidance on when a bigger model / more thinking effort is worth it.
- **Permissions / safety modes** — plan mode vs. accept-edits; `/permissions`; why to keep the agent on a leash.

**Participant tasks (menu — pick 1–2):**
- Add a rule to CLAUDE.md (e.g. *"use NumPy-style docstrings"* or *"prefer dataclasses"*), ask Claude to write a small helper, observe the change; toggle the rule to see the impact.
- Use a skill, or write a tiny custom skill encoding a personal convention.
- Compare plan mode vs. accept-edits on a trivial edit; inspect `/permissions`.

**Deliverable:** one CLAUDE.md rule added; a felt sense of "config steers output."

---

## ☕ Break (5 min)

---

## §5 — Backbone: ship a feature via plan → TDD → review → PR (46 min · ~6 input / ~40 hands-on)

**Goal:** the heart of the workshop — implement one small feature end-to-end with the full disciplined loop. Short instructor input (~1 min) before each phase, then participants work.

**Feature (default):** add a second integration method (e.g. **RK4** alongside the existing Euler step). Small, well-specified, testable against a known analytic solution.

**Phases & participant tasks:**

1. **Plan (~8 min)** — *input: plan mode / brainstorming.*
   Ask Claude to draft an implementation plan. **Review & annotate it**, then instruct: *"address all notes, don't implement yet."* Don't let it code until the plan is right.
2. **TDD — red (~8 min)** — *input: tests as the verifiable check.*
   Ask Claude to **write failing tests first** — numerical/property tests (e.g. RK4 error scales as expected; matches the analytic solution within tolerance). Run them: `uv run pytest` → red.
3. **Implement — green (~12 min)** — *input: self-verifying loop.*
   Have Claude implement until tests pass, iterating with `uv run pytest`. The pass/fail check closes the loop.
4. **Review (~10 min)** — *input: adversarial + human review.*
   Run `/code-review` or ask Claude to adversarially review its own diff; **also read the diff yourself**. Request changes; re-run tests.
5. **PR (~8 min)** — *input: small, targeted PRs.*
   Commit in small steps; open a **small targeted PR** to your fork with a clear description of what/why and how it was tested.

**Deliverable:** a green-tested, reviewed PR on the participant's fork.

**Stretch (fast finishers):** fix a **planted bug** in the repo using the same loop; or add a plotting script (`matplotlib`) comparing Euler vs. RK4 error.

---

## §6 — Failure-patterns debrief (6 min · 4 input / 2 share)

**Goal:** name the pitfalls while the experience is fresh. Adopt **Anthropic's five named failure patterns**:

1. **Kitchen-sink session** → `/clear` between unrelated tasks.
2. **Correcting over and over** → after two failed corrections, `/clear` and write a better initial prompt.
3. **Over-specified CLAUDE.md** → prune ruthlessly.
4. **Trust-then-verify gap** → always give a verifiable check; if you can't verify it, don't ship it.
5. **Infinite exploration** → scope narrowly or delegate to a subagent.

**Participant task:** quick share — *"what tripped you up?"* — and map it to a pattern.

---

## §7 — Advanced demo + teasers + wrap (8 min · 6 demo / 2 input)

**Goal:** show there's more, without pretending to teach it in depth.

- **Real (short) live demo** of one advanced capability — **subagents**, **hooks**, or **MCP/memory** (genuine demo, not a throwaway mention).
- **Rapid teasers / pointers:** GitHub Actions auto-review + human review; git worktrees; where to go deeper (Anthropic docs, `research_agentic_coding_workshops.md`).
- **Wrap:** recap the loop; encourage applying it to their own research code. Flag the **scientific-computing angle** — numerical/property tests as the verifiable check, and `uv` for reproducibility.

**Participant task:** none — take-home challenge: run the full loop on a small piece of your own code.

---

## Buffer / Q&A (5 min)

Overrun cushion + open questions.

---

## Timing notes

- **The 30/70 target is aggressive for beginners.** This draft is ~35/65. The realistic levers to buy hands-on time: shorten §0 to 4 min, cut §1 to a 4-min demo, or drop §7's advanced demo to pure pointers.
- **§5 is the sacrificial buffer in reverse:** if earlier sections overrun, protect §5 — it's the whole point. The stretch tasks absorb fast finishers so the group can move together.
- No source provides a validated 2h breakdown — **pilot this run-sheet once** and adjust minutes.

## Repo dependencies (blocking §2–§5)

The practice repo (`../Repository/`) must exist before this plan is runnable, with:
- A `uv`-managed 1D ODE integrator (existing **Euler** step) + a runnable example/entry point.
- A **passing test suite** (green baseline for §2) and an analytic reference solution for §5's tests.
- **A few planted bugs** for the §5 stretch task.
- A plain throwaway script for the §1 demo.
- A concise starter `CLAUDE.md` participants will extend in §4.

## Prep checklist

- [ ] Build/finalize `../Repository/` per above.
- [ ] Send setup email (Claude Code auth, fork+clone, `uv` install) — verify send date with organizers.
- [ ] Decide fork-per-participant vs. shared org repo (affects §5 PR target).
- [ ] Pilot the run-sheet end-to-end once; adjust minutes.
- [ ] Prepare slides in `Presentation/` (Marp/reveal.js) mirroring these sections.
