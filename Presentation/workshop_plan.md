# Workshop Session Plan — Agentic AI for Coding

*Concrete run-sheet for the ~2-hour hands-on workshop. Draft for review.*
*Companion to `../CLAUDE.md` (design decisions) and `../research_agentic_coding_workshops.md` (evidence base).*

## At a glance

- **Audience:** PhD-level computational physicists; know Python + git; **no** prior Claude Code.
- **Duration:** 120 min, incl. one 5-min break + 5-min end buffer → **110 min active**.
- **Split:** target ~30% input / ~70% hands-on. This draft lands at **~40% input / ~60% hands-on** (~46 min input+demo / ~69 min hands-on). To move back toward 30/70, trim the live demo (§2) and framing (§1), and move §4 material into speaker notes. See *Timing notes*.
- **Prerequisites (via setup email):** Claude Code installed & authenticated, GitHub account, practice repo forked & cloned, `uv` installed.
- **Backbone deliverable:** each participant ships one small, tested, reviewed **PR** on their fork.
- **Assumed practice example:** a **1D ODE integrator** (see *Repo dependencies*). Swap-safe — task wording adapts if the example changes.

## Timeline

| Clock | # | Section | Format | Min |
|---|---|---|---|---|
| 0:00 | 0 | `uv` crash course + get the repo running | Input + hands-on | 14 |
| 0:14 | 1 | Welcome & the agent loop | Input | 8 |
| 0:22 | 2 | Live "aha" demo | Demo | 6 |
| 0:28 | 3 | Understand the repo (`/init`) | Hands-on | 10 |
| 0:38 | 4 | Steering the agent | Input + hands-on | 16 |
| 0:54 | – | ☕ Stretch break | — | 5 |
| 0:59 | 5 | **Backbone: branch → TDD → review → PR** | Input + hands-on | 46 |
| 1:45 | 6 | Failure-patterns debrief + context window | Input + share | 8 |
| 1:53 | 7 | Advanced demo + teasers + wrap | Demo + input | 7 |
| 2:00 | – | Buffer / Q&A | — | 0 |
| 2:00 | | **End** | | |

---

## §0 — `uv` crash course (14 min · 4 input / 10 hands-on)

**Goal:** everyone can run, test, and manage the project with `uv`; reproducibility framing.

**Why first:** it is the substrate for everything else, and it is the one segment that must succeed for
every participant before §5 can work. Starting here also gets laptops warm and green while the room
settles.

**Talking points:** why `uv` (speed, one tool for envs + packages + interpreters, `uv.lock` as the
reproducibility story). The six commands: `uv init`, `uv sync`, `uv add`, `uv run`, `uv run script.py`,
`uvx`. Then the cache: installs *link* out of one global cache (copy-on-write clone on macOS/Linux,
hardlink on Windows), which only works within one filesystem — so a `$HOME` cache with a project on
`/data` silently degrades to full copies. Give each mount its own `UV_CACHE_DIR` via `direnv`.

**Participant tasks:**
1. `git clone` their fork, `cd` into it.
2. `uv sync`.
3. `uv run pytest` → existing tests pass (green baseline).
4. `uv run scripts/run_decay.py` → run the example.
5. `uv add matplotlib` → the dep they'll plot with later.

**Deliverable:** working environment, tests green.

---

## §1 — Welcome & the agent loop (8 min · input)

**Goal:** frame the session and give a shared mental model before anyone touches the keyboard.

**Talking points:**
- What "agentic" coding means vs. autocomplete/chat. Introduce the **agent loop** by name: `goal → plan → act → observe → revise`.
- **Vibe-coding vs. disciplined AI-assisted engineering** — *you* stay responsible for architecture and review; the agent does the typing.
- **Task triage** (one line): agents shine on small, well-specified tasks; they struggle on tasks needing architectural judgement. Today's task is deliberately small.
- **Finding the divergence** — the thesis of the session. You say what you want; the agent forms its
  own plan; the skill is spotting where the two come apart and deciding which gaps matter. `pytest`
  where you'd have written `unittest` → align and move on. A neural network where you wanted the
  analytic solution → catch it in the plan. Give as much freedom as you are comfortable with.
- The promise: *by the end you'll have shipped a small, tested, reviewed PR.*

**Participant task:** none — just confirm Claude Code opens inside the cloned repo.

---

## §2 — Live "aha" demo (6 min · demo)

**Goal:** show the loop in motion; create the "oh, I want that" moment. **Live, not slides** — including a mistake and the agent's recovery.

**Instructor demo (pick one, run at speed):**
- Take a plain throwaway script in the repo and ask Claude to turn it into an `argparse` CLI with type hints and a `--help`, then run it. *(MIT Missing Semester opener — relatable for scientists with ad-hoc scripts.)*
- Or: do one tiny task "by hand vs. by agent" back-to-back to contrast effort.

**Participant task:** watch; jot down one thing they'll try later.

---

## §3 — Understand the repo (10 min · 2 input / 8 hands-on)

**Goal:** the **Explore** step — use the agent to build a mental map before changing anything.

**Talking points:** plan mode (read-only exploration); how to ask the agent to map a codebase; why
exploring first beats diving in. Then the division of labour: **plan mode is how *you* read the repo,
`/init` is how the *repo* remembers** — it drafts a `CLAUDE.md` from what it discovered. Run `/init`
live and delete half the result out loud; that sets up §4's concision lesson.

**Participant tasks:**
1. Ask Claude (plan mode): *"Explain this repository — structure, what each module does, how to run it and the tests."*
2. Follow-up: *"Where would I add a new integration method, and what would I need to test?"*
3. Run `/init` and read the `CLAUDE.md` it produced.

**Deliverable:** participant can describe the repo in their own words, knows where the feature will
live, and has read a generated `CLAUDE.md`.

---

## §4 — Steering the agent (16 min · 6 input / 10 hands-on)

**Goal:** show how configuration changes the agent's behaviour; cover safety.

**Talking points:**
- **Two scopes of memory** — `~/.claude/CLAUDE.md` (user, every session) and `./CLAUDE.md` (project,
  shared via git). Show a real user-memory file; user memory pays its cost every session, so it earns
  the tightest editing. `/memory` opens either.
- **CLAUDE.md** — project memory. **Keep it concise** — bloated files get ignored. "Would removing this line cause a mistake? If not, cut it."
- **Skills** — reusable instructions; **show an actual SKILL.md**, since the hands-on asks them to write
  one. The `description` field is what beginners get wrong: write it as "use when…".
- **Models & reasoning effort** (folded in) — quick guidance on when a bigger model / more thinking effort is worth it.
- **Permissions / safety modes** — plan mode vs. accept-edits; `/permissions`; why to keep the agent on a leash.
- **Where does your data go?** — files the agent opens leave the institution. Unpublished results,
  grant text, student data, GDPR, NDAs. Decision rule: would you be comfortable with a third party
  reading this? The ICP local model is the escape hatch for privacy-sensitive chat — verify its URL and
  model before the session, and say plainly that it is chat, not the agentic loop.

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

0. **Say it precisely (~1 min input).** Vague vs precise prompt, side by side. Reduce what the agent has
   to assume: which file, which function, what is wrong, how you want it fixed.
1. **Plan, then branch (~8 min)** — *input: plan mode / brainstorming.*
   Ask Claude to draft an implementation plan. **Review & annotate it**, then instruct: *"address all
   notes, don't implement yet."* This is the divergence check from §1. Sign the plan off, then
   `git switch -c add-rk4` — **the branch exists before the first edit.**
2. **TDD — red, then commit (~8 min)** — *input: tests as the verifiable check.*
   Ask Claude to **write failing tests first** — numerical/property tests (e.g. RK4 error scales as expected; matches the analytic solution within tolerance). Run them: `uv run pytest` → red.
   **Commit the failing test on its own** — it is the specification, and it outlives the implementation.
3. **Implement — green, then commit (~12 min)** — *input: self-verifying loop.*
   Have Claude implement until tests pass, iterating with `uv run pytest`. The pass/fail check closes the loop.
   Commit again. Have them read `git log --oneline`: "tests, then implementation" is the shape to recognise.
4. **Review (~10 min)** — *input: adversarial + human review.*
   Run `/code-review` (it takes the branch against `main`) or ask Claude to adversarially review it;
   **also read the diff yourself** — `git diff main...HEAD`, both commits. Request changes; re-run tests.
5. **PR (~8 min)** — *input: small, targeted PRs.*
   `git push -u origin add-rk4`, then `gh pr create --label claude --label p2-medium --label
   effort-2-small`. Let Claude write the description. Labels make the work findable later
   (`gh pr list --label claude`, `gh pr view`, `gh pr comment`).

**Deliverable:** a green-tested, reviewed, labelled PR on the participant's fork, whose branch holds at
least two commits.

**Prerequisites:** `gh auth login` done (setup email), and the three labels created in the target repo
beforehand — `gh pr create` fails on a label that does not exist.

**Stretch (fast finishers):** fix a **planted bug** in the repo using the same loop; or add a plotting script (`matplotlib`) comparing Euler vs. RK4 error.

---

## §6 — Failure-patterns debrief (8 min · 6 input / 2 share)

**Goal:** name the pitfalls while the experience is fresh. Adopt **Anthropic's five named failure patterns**:

1. **Kitchen-sink session** → `/clear` between unrelated tasks.
2. **Correcting over and over** → after two failed corrections, `/clear` and write a better initial prompt.
3. **Over-specified CLAUDE.md** → prune ruthlessly.
4. **Trust-then-verify gap** → always give a verifiable check; if you can't verify it, don't ship it.
5. **Infinite exploration** → scope narrowly or delegate to a subagent.

Then **why 1 and 2 are the same bug**: everything the agent reads sits in one finite window. Run
`/context` live — the `CLAUDE.md` line makes §4's concision lesson visible in tokens. `/clear` between
tasks, `/compact` through one, and **write decisions to disk** so they survive a compaction.

**Participant task:** quick share — *"what tripped you up?"* — and map it to a pattern.

---

## §7 — Advanced demo + teasers + wrap (7 min · 5 demo / 2 input)

**Goal:** show there's more, without pretending to teach it in depth.

- **Real (short) live demo** of one advanced capability — **subagents**, **hooks**, or **MCP/memory** (genuine demo, not a throwaway mention).
- **Rapid teasers / pointers:** GitHub Actions auto-review + human review; git worktrees; where to go deeper (Anthropic docs, `research_agentic_coding_workshops.md`).
- **Wrap:** recap the loop; encourage applying it to their own research code. Flag the **scientific-computing angle** — numerical/property tests as the verifiable check, and `uv` for reproducibility.

**Participant task:** none — take-home challenge: run the full loop on a small piece of your own code.

---

## Buffer / Q&A

⚠️ **The 5-minute buffer is spent.** The revised deck adds ~9 slides (uv cache, the divergence framing,
`/init`, memory scopes, SKILL.md anatomy, data privacy, precise prompting, the context window, MCP,
tools) and the timeline above now lands exactly on 2:00 with nothing left over. Before delivery, decide
which of these to cut or to move into speaker notes — the honest candidates are §4 (six input slides in
six minutes is optimistic) and §7's advanced demo.

---

## Timing notes

- **The 30/70 target is aggressive for beginners.** This draft is ~35/65. The realistic levers to buy hands-on time: shorten §1 to 6 min, cut §2 to a 4-min demo, or drop §7's advanced demo to pure pointers.
- **§5 is the sacrificial buffer in reverse:** if earlier sections overrun, protect §5 — it's the whole point. The stretch tasks absorb fast finishers so the group can move together.
- No source provides a validated 2h breakdown — **pilot this run-sheet once** and adjust minutes.

## Repo dependencies (blocking §0–§5)

The practice repo (`../Repository/`) must exist before this plan is runnable, with:
- A `uv`-managed 1D ODE integrator (existing **Euler** step) + a runnable example/entry point.
- A **passing test suite** (green baseline for §0) and an analytic reference solution for §5's tests.
- **A few planted bugs** for the §5 stretch task.
- A plain throwaway script for the §2 demo.
- A concise starter `CLAUDE.md` participants will extend in §4.

## Prep checklist

- [ ] Build/finalize `../Repository/` per above.
- [ ] Send setup email (Claude Code auth, fork+clone, `uv` install) — verify send date with organizers.
- [ ] Decide fork-per-participant vs. shared org repo (affects §5 PR target).
- [ ] Pilot the run-sheet end-to-end once; adjust minutes.
- [ ] Prepare slides in `Presentation/` (Marp/reveal.js) mirroring these sections.
