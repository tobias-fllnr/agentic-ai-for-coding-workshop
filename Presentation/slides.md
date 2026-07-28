---
marp: true
paginate: true
backgroundColor: '#0d1117'
color: '#e6edf3'
style: |
  section {
    font-family: -apple-system, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
    font-size: 26px;
    padding: 60px 70px;
    line-height: 1.4;
  }
  h1 { color: #6cb6ff; font-size: 44px; }
  h2 { color: #6cb6ff; font-size: 34px; }
  h3 { color: #adbac7; font-size: 26px; }
  a { color: #6cb6ff; }
  strong { color: #f0f6fc; }
  code { background: #161b22; color: #e6edf3; padding: 2px 6px; border-radius: 4px; font-size: 0.9em; }
  pre { background: #161b22; border: 1px solid #30363d; border-radius: 8px; padding: 14px 16px; }
  pre code { background: transparent; padding: 0; }
  blockquote { border-left: 4px solid #6cb6ff; color: #adbac7; padding-left: 16px; font-style: italic; }
  table { font-size: 0.85em; border-collapse: collapse; margin: 8px 0; }
  th, td { border: 1px solid #30363d; padding: 8px 14px; }
  thead th { background: #1b2230; color: #6cb6ff; font-weight: 600; }
  tbody td { background: #12161d; color: #e6edf3; }
  tbody tr:nth-child(even) td { background: #0d1117; }
  footer { color: #6e7681; font-size: 15px; }
  section::after { color: #6e7681; font-size: 15px; }
  ul, ol { line-height: 1.5; }
  .sub { color: #f0b429; font-size: 22px; display: block; margin-top: 22px; }
  .meta { color: #6e7681; font-size: 20px; display: block; margin-top: 44px; }
  section.divider { justify-content: center; text-align: center; }
  section.divider h1 { font-size: 72px; margin: 0; }
  section.divider h2 { color: #adbac7; font-weight: 400; margin-top: 6px; }
  section.title { justify-content: center; text-align: center; }
  section.title h1 { font-size: 58px; }
  section.title h2 { color: #adbac7; font-weight: 400; }
  section.task { border-left: 14px solid #3fb950; }
  section.task h2 { color: #3fb950; }
  section.lead { justify-content: center; text-align: center; }
  section.lead h2 { font-size: 40px; }
---

<!-- _class: title -->
<!-- _paginate: false -->

# Agentic AI for Coding
## A hands-on introduction to Claude Code

<span class="meta">Fabian Zills · Tobias Fellner · Institute for Computational Physics (ICP), University of Stuttgart · 2026</span>

<!-- Welcome. Today you go from zero Claude Code experience to shipping a small, tested, reviewed PR — using a disciplined workflow you can take straight back to your own research code. -->

---

## The promise

By the end you will have **shipped a small, tested, reviewed pull request** with Claude Code — using a workflow you can reuse on your own research code.

- Assumes: **Python + git**. No prior Claude Code needed.
- Style: short input, **lots** of hands-on.
- Practice repo: **`odelab`**, a tiny 1D ODE integrator.

<!-- Set expectations: mostly hands-on, interleaved — short input, then you drive. Reassure the beginners; nobody is expected to know Claude Code already. -->

---

## Agenda

| # | Section |
|---|---|
| 0–1 | The agent loop + a live demo |
| 2 | `uv` crash course |
| 3 | Understand the repo |
| 4 | Steering the agent |
| ☕ | Break |
| 5 | **Ship a feature: plan → TDD → review → PR** |
| 6–7 | Pitfalls · advanced demo · wrap |

<!-- The heart is §5. Everything else earns time for it. If we run late, we protect §5 and cut the extras. -->

---

<!-- _class: divider -->
<!-- footer: '§0 · The agent loop' -->

# §0
## The agent loop

---

## What makes it "agentic"?

Not autocomplete. Not chat. The model **acts in a loop** with tools:

### goal → plan → act → observe → revise

- **act** — read/write files, run commands, run tests
- **observe** — read the output, errors, test results
- **revise** — adjust, and go again — until the goal is met

<!-- Introduce the loop BY NAME; we refer back to it all day. The agent isn't magic — it's this loop, plus your tools and your steering. -->

---

## Vibe-coding vs. AI-assisted engineering

| Vibe-coding | Disciplined use |
|---|---|
| Prompt, accept, hope | Plan, verify, review |
| You read little | **You own** architecture & review |
| Fine for throwaway | Right for real work |

> Studies of professional developers: they **plan before implementing and validate every output.**

<!-- Reassure the physicists: you stay in control. The agent types; you decide and check. This framing recurs in §5. -->

---

## When to delegate

Agents shine on **small, well-specified** tasks.
They struggle where **architectural judgement** is needed.

- ✅ "Add an RK4 step and test its convergence order"
- ⚠️ "Redesign how the solver handles stiff systems"

Today's task is deliberately small — and that's the point.

<!-- Teach the triage instinct. Part of the skill is recognizing what NOT to hand off. -->

---

<!-- _class: divider -->
<!-- footer: '§1 · Live demo' -->

# §1
## A live demo

---

## Watch the loop (live)

Plain script → a proper CLI, in real time.

`scripts/run_decay.py`  →  add `argparse`, `--help`, type hints

Watch for:
- the **plan** before any code
- a **mistake** and the **recovery** — that's the real skill

<!-- LIVE, not slides. Run it in the terminal. Let them see Claude stumble and fix itself; narrate the loop as it happens. Keep it brief. Ask them to jot one thing they want to try. -->

---

<!-- _class: divider -->
<!-- footer: '§2 · uv' -->

# §2
## `uv` crash course

---

## Why `uv`?

One fast tool for **environments + packages + running**.

- Reproducible: a locked `uv.lock` everyone shares
- No manual `venv` juggling
- `uv run` = "run this inside the project's environment"

Optional niceties: **`direnv`** (auto-activate) · **`UV_CACHE_DIR`** (shared cache).

<!-- Keep it short — uv isn't the point, it's the substrate. Reproducibility ties directly to good scientific practice. -->

---

## The four commands you need

```bash
uv sync              # create/refresh the env from pyproject + lock
uv run pytest        # run something inside that env
uv run python scripts/run_decay.py
uv add matplotlib    # add a dependency
```

<!-- These four cover ~95% of daily use. Everything today runs through `uv run`. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — get the repo running

```bash
uv sync
uv run pytest                       # 4 tests should pass (green baseline)
uv run python scripts/run_decay.py
uv add matplotlib                   # you'll plot later
```

✅ **Done when:** tests are green and the decay script prints a result.

<!-- Circulate. Most common snag: wrong working directory. Everyone should hit green before we move on. -->

---

<!-- _class: divider -->
<!-- footer: '§3 · Understand the repo' -->

# §3
## Understand the repo first

---

## Explore before you change

The **Explore** phase: build a mental map before touching code.

- **Plan mode** = read-only. Claude reads and answers; it doesn't edit.
- Ask it to map structure, entry points, and tests.
- Understanding now is cheaper than unwinding a wrong change later.

<!-- Show how to enter plan mode. This maps to the canonical first step: Explore. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — ask Claude to explain `odelab`

In **plan mode**, ask Claude to:
> explain this repository — structure, what each module does, how to run it and the tests

then follow up:
> where would I add a new integration method, and what should I test?

✅ **Done when:** you can describe the repo in a sentence and know where RK4 will go.

<!-- The point is the habit, not the answer. Let two or three people share what Claude told them. -->

---

<!-- _class: divider -->
<!-- footer: '§4 · Steering the agent' -->

# §4
## Steering the agent

---

## `CLAUDE.md` — project memory

Instructions Claude reads **every session**: conventions, how to run things, gotchas.

**Keep it concise.** For each line ask: *"would removing this cause a mistake?"* If not — cut it.

> Bloated `CLAUDE.md` files get **ignored** — the important rules drown in the noise.

<!-- Concision over completeness is THE lesson here. Show odelab's short CLAUDE.md as the model. -->

---

## More levers

- **Skills** — reusable instructions you invoke on demand; use existing ones or write your own (e.g. a personal docstring style).
- **Model & reasoning effort** — more power for hard, ambiguous tasks; smaller/faster for routine edits. Not "biggest by default."
- **Permissions & safety** — plan mode vs. accept-edits; `/permissions`. Keep the agent on a leash.

<!-- Fold model/effort in here: pick more power when the task is genuinely hard. Briefly show /permissions and the safety modes. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — feel the steering

Pick **one or two**:

1. Add a rule to `CLAUDE.md` (e.g. *"use NumPy-style docstrings"* or *"prefer dataclasses"*), ask Claude to write a small helper, then **toggle the rule** and regenerate — spot the difference.
2. Use, or write, a tiny **skill** encoding a personal convention.
3. Compare **plan mode** vs **accept-edits** on a trivial edit; open `/permissions`.

✅ **Done when:** you've seen config visibly change Claude's output.

<!-- The "aha" is that a one-line rule changes the output. Keep it snappy — this is a warm-up for §5. -->

---

<!-- _class: divider -->
<!-- _paginate: false -->
<!-- footer: '☕ Break' -->

# ☕
## Break

---

<!-- _class: divider -->
<!-- footer: '§5 · plan → TDD → review → PR' -->

# §5
## Ship a feature
<span class="sub">plan → TDD → review → PR · the main event</span>

---

## The task: add RK4

Add a **4th-order Runge–Kutta** step alongside Euler — and prove it's better.

The disciplined loop:
### plan → test (red) → implement (green) → review → PR

> Canonical Claude workflow is *Explore → Plan → Code → Commit*.
> The **TDD** and **review** steps are our deliberate additions.

<!-- Set the arc. Short input before each phase, then they work. -->

---

## Phase 1 — Plan

Use **plan mode** / brainstorming. Get a plan *before* any code.

- Have Claude draft the plan
- **Read it. Annotate it.** Then: *"address all notes, don't implement yet."*
- Don't let it code until the plan is right.

<!-- The annotation trick prevents premature coding — Claude tends to jump straight to implementing. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — plan RK4

> Ask Claude (plan mode) to plan adding an `rk4_step` to `odelab`, reusing the existing `integrate(..., method=...)` hook.

- Review the plan; add a note or two.
- Tell it to revise the plan — **without coding yet**.

✅ **Done when:** you have a plan you'd sign off on.

---

## Phase 2 — Test first (red)

Give the agent a **pass/fail check**. For numerical code, that's a test.

- RK4 matches the analytic decay to a tight tolerance
- **Convergence order ≈ 4:** double the steps → error drops **~16×**

<!-- Contrast with Euler's ~2x factor (see test_euler_is_first_order in the repo). The convergence-order test is the real property to assert. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — write the failing test

> Ask Claude to add tests for `rk4_step` **before** implementing it — matching the analytic solution and checking convergence order.

```bash
uv run pytest -q      # should be RED — rk4_step doesn't exist yet
```

✅ **Done when:** a new test exists and fails for the right reason.

---

## Phase 3 — Implement (green)

Now let Claude implement — and **let the tests close the loop**.

```bash
uv run pytest -q      # iterate until green
```

Without a runnable check, *"looks done"* is the only signal — and **you** become the verification loop.

<!-- This is the payoff of the self-verifying loop. Let them watch Claude iterate against pytest. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — make it green

> Ask Claude to implement `rk4_step` until your tests pass.

```bash
uv run pytest -q
```

✅ **Done when:** all tests pass, including your convergence-order test.

---

## Phase 4 — Review

Two reviewers: the agent, and **you**.

- `/code-review`, or ask Claude to **adversarially** review its own diff
- **Read the diff yourself** — correctness, clarity
- Request changes; re-run the tests

<!-- Universally recommended: validate the output. Don't merge what you didn't read. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — review the diff

```bash
git diff
```

> Ask Claude to review its own change for correctness & clarity — then read it yourself and request one improvement.

✅ **Done when:** you've read every changed line and tests still pass.

---

## Phase 5 — Small, targeted PR

Commit in small steps; open a **small** PR.

```bash
git switch -c add-rk4
git add -A
git commit -m "Add RK4 integrator + convergence tests"
git push -u origin add-rk4
```

You won't meaningfully review a 1000-line PR. Keep it small.

<!-- Adjust the remote/flow to your GitHub setup (fork-per-person vs shared org). Open the PR in the browser — CI runs the tests. -->

---

<!-- _class: task -->
## 🧑‍💻 Your turn — open the PR

Create a branch, commit, push, and open a PR describing **what & why** and **how you tested it**.

✅ **Done when:** your PR is open and CI is running the tests.

**Fast finishers:** the plots/examples misbehave — hunt & fix the planted **bugs** (`scripts/plot_decay.py` and the logistic example).

---

<!-- _class: divider -->
<!-- footer: '§6 · Failure patterns' -->

# §6
## Common failure patterns

---

## Five ways it goes wrong — and the fix

1. **Kitchen-sink session** → `/clear` between unrelated tasks
2. **Correcting over & over** → after 2 tries, `/clear` + a better prompt
3. **Over-specified `CLAUDE.md`** → prune ruthlessly
4. **Trust-then-verify gap** → always give a check; can't verify → don't ship
5. **Infinite exploration** → scope narrowly, or use a subagent

<!-- Tie each to what they just experienced in §5. Quick round: "what tripped you up?" → map it to a pattern. -->

---

<!-- _class: divider -->
<!-- footer: '§7 · Beyond the basics' -->

# §7
## Beyond the basics

---

## A glimpse further (live)

One quick live demo — pick one:

- **Subagents** — delegate a scoped task to a fresh context
- **Hooks** — deterministic automation on events (format, test, block)
- **MCP / memory** — connect external tools & persistent context

<!-- A REAL short demo, not a throwaway — whichever you're most fluent in. -->

---

## Take it further

**Teasers:** GitHub Actions auto-review + human review · git worktrees for parallel work

**For your research code:**
- numerical / property tests = your verifiable check
- `uv` = reproducible environments

**Resources:** Anthropic Claude Code docs · `research_agentic_coding_workshops.md` (in this repo)

<!-- Point them at the research doc for the evidence base and further reading. -->

---

<!-- _class: lead -->
<!-- footer: '' -->

## goal → plan → act → observe → revise

Plan first · verify everything · review before you ship · keep it small.

### Now go run the loop on your own code.

<!-- Take-home: run the full loop on one small piece of your own code this week. Thank them. -->
