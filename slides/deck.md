# Agentic AI for Coding — deck as text

Exported from `index.html` by `to_markdown.py` — 53 slides. The deck is the source of truth; re-run the script instead of editing this file.

---

# Agentic AI for Coding

A hands-on introduction to Claude Code — and to a workflow you can trust with research code.

Fabian Zills · Tobias Fellner  
Institute for Computational Physics · University of Stuttgart  
Söllerhaus Workshop · 2026

> **Notes:** Welcome. Today you go from zero Claude Code experience to shipping a small, tested, reviewed change — using a disciplined workflow you can take straight back to your own research code.

---

## Why you are here — The promise

By the end you will have **shipped a small, tested, reviewed change** with Claude Code — using a workflow you can reuse on your own research code.

- **Assumes** — Python and git. **No** prior Claude Code.
- **Style** — Short input, **lots** of hands-on.
- **Practice repo** — `odelab` — a tiny 1D ODE integrator.

> **Notes:** Set expectations: mostly hands-on, interleaved — short input, then you drive. Reassure the beginners; nobody is expected to know Claude Code already.

---

## Two hours — Agenda

| §   | Section                                         | Format         |
|-----|-------------------------------------------------|----------------|
| 0   | `uv` crash course — get the repo running        | Hands-on       |
| 1–2 | The agent loop + a live demo                    | Input · demo   |
| 3   | Understand the repo                             | Hands-on       |
| 4   | Steering the agent                              | Hands-on       |
| ☕  | Break                                           | 5 min          |
| 5   | **Ship a feature: plan → TDD → review → merge** | The main event |
| 6–7 | Pitfalls · advanced demo · wrap                 | Input · demo   |

> **Notes:** The heart is §5 — 46 of the 110 active minutes. Everything else earns time for it. If we run late, we protect §5 and cut the extras.

---

## Read this with a date on it — This deck has a half-life

Everything here is the state of the art in **July 2026**. Tell the durable parts from the volatile ones.

- **Durable** — The loop. A check the agent can run. Small reviewable diffs. Finding the divergence early. You owning the review.
- **Volatile** — Model names and their habits. Slash commands. Which third-party skills are worth installing. How much instruction text helps.

    24 Jul 2026, the day Opus 5 shipped: Anthropic removed over 80% of Claude Code’s own
      system prompt, with no measurable loss on its coding evaluations.
    Feb 2026: same model, better harness — Terminal-Bench 2.0 52.8% → 66.5%.
    Since Feb 2026: four Opus-tier flagships in 170 days.

*How to prompt an agent is an open argument, not a settled craft — and every model answers differently.*

> **Notes:** Say this early and mean it: it buys you honesty for the rest of the session and it inoculates them against treating any single command as gospel. The two facts are the argument. Anthropic deleted most of its own system prompt the day Opus 5 shipped and reported no eval loss (Thariq Shihipar, Anthropic, 24 July 2026) — while LangChain showed that holding the model fixed and improving the harness alone moved Terminal-Bench 2.0 by fourteen points (Feb 2026). Structure up, instructions down. Karpathy's reply this week is the third leg: benchmarks do not capture production. Nobody in this argument is obviously wrong, which is exactly why you teach the loop and the verification habit rather than a prompt recipe.

---

# §0 — `uv` crash course

The substrate: environments you can reproduce

---

## §0 · uv — Why `uv`?

One fast tool for **environments + packages + Python itself**.

- **10–100× faster than pip** — fast enough to rebuild an environment per job
- One tool where you had `pip`, `pip-tools`, `pipx`, `poetry`, `pyenv`, `virtualenv`
- `uv.lock` — a universal lockfile: commit it, and everyone resolves the same versions
- It installs **Python interpreters** too: `uv python install 3.12`
- A single static binary, and an ordinary `.venv` underneath — installs in `$HOME` on a cluster with no admin rights

*Install: `docs.astral.sh/uv/getting-started/installation` · speed figure is Astral’s own benchmark, warm cache. Reproducibility for a paper: commit `pyproject.toml` and `uv.lock`.*

> **Notes:** Keep it short — uv is the substrate, not the point. The reproducibility line is the one that lands with this audience: the lockfile is what makes "it worked on my machine" a checkable claim. For a plot script you email around, PEP 723 inline dependencies (`# /// script`) make it self-contained — mention it if there is time.

---

## §0 · uv — The commands you need

```bash
uv init myproject         # new project: pyproject.toml, .python-version, git
uv sync                   # make .venv match uv.lock exactly
uv add numpy              # add a dependency: pyproject + lock + .venv
uv run pytest             # run inside the project environment
uv run scripts/plot.py    # for a .py file, the word "python" is optional
uvx ruff check .          # run a tool in a throwaway environment
```

Six commands cover the day. Everything today runs through `uv run`.

> **Notes:** `uv run` syncs the environment first, so it is always up to date — that is why the agent can trust it as a check. `uv init` is the one they will use back at their desks on Monday; it also runs git init for you.

---

## §0 · uv — The cache is the trick

Installing links a package out of one global cache into your `.venv` — copy-on-write **clone** on macOS and Linux, **hardlink** on Windows. Both need the cache and the venv on the **same filesystem**.

    warning: Failed to hardlink files; falling back to full copy.
    This may lead to degraded performance.

Cache in `$HOME`, project on `/data` — that is a byte-for-byte copy of every wheel. Give each mount its own cache, with `direnv`:

```bash
# /data/<user>/.envrc          → and the same under /work, /tikhome
export UV_CACHE_DIR=/data/$USER/uv-cache
```

*On a cluster, prefer the site Python where MPI and BLAS are tuned: `--no-managed-python`. Watch inode quotas — `UV_PROJECT_ENVIRONMENT` moves the venv to scratch.*

> **Notes:** This is the slide nobody else teaches. The mechanism: uv tries reflink (clone), falls back to hardlink, then to a full copy — and only the copy fallback warns. Links cannot cross filesystems, so a home-directory cache plus an NFS project directory silently costs you the entire speed and disk-dedup benefit. Astral's docs put it plainly: the cache directory should live on the same filesystem as the environment. Setting UV_LINK_MODE=copy only silences the warning; co-locating the cache is the actual fix. The NFS-per-mount direnv recipe is our own guidance, the docs do not cover HPC.

---

## §0 · uv — Get the repo running  ·  *your turn*

**Fork first** — recommended, so you can push today’s work and open a PR afterwards. A plain clone of the upstream repo works for everything we do here.

```bash
git clone https://github.com/<your-user>/odelab.git
cd odelab
uv sync
uv run pytest                    # 4 tests pass — your green baseline
uv run scripts/run_decay.py
uv add matplotlib                # you will plot later
```

**Done when:** the tests are green and the decay script prints a result.

> **Notes:** These are the checks from the setup email, so most of the room should be green in two minutes — the rest of the five is for the stragglers, and whoever already has the cache right can help their neighbour. Circulate. Most common snags: cloning the upstream repo rather than their own fork, and running uv from the wrong directory — it needs to see pyproject.toml. Everyone must hit green before we move on; the whole of §5 depends on a working test command. If anyone sees the hardlink warning here, that is the previous slide made real.

---

# §1 — The agent loop

A mental model that lasts all day

---

## §1 · The agent loop — How you use an LLM today

You ask

→

It answers

→

You copy & paste

→

You run it

- **You are the executor** — the model only advises
- It never sees your files, your environment, or what your code actually did
- Every result comes back through you, by hand

> **Notes:** Everyone in the room has done exactly this in a browser tab. Say the line out loud: the human is the executor. The next slide removes that constraint, and the whole workshop follows from it.

---

## §1 · The agent loop — What makes it “agentic”?

The model gets **tools**, and **acts in a loop**.

- **act** — read and write files, run commands, run tests
- **observe** — read the output: errors, test results, diffs
- **revise** — adjust and go again, until the goal is met

**goal** → **plan** → **act** → **observe** → **revise**

> **Notes:** Introduce the loop BY NAME; we refer back to it all day. The agent isn't magic — it's this loop, plus your tools and your steering. Point at the rail: you will see it again in §5, where the same five beats become plan, test, implement, review, ship.

---

## §1 · The agent loop — The one skill: find the divergence

You say what you want built. The agent forms its own plan. **Your job is to find where that plan and your intent come apart** — and to decide, early, which gaps matter.

- **It reaches for `pytest`; you write `unittest`** — Same result, different taste. — *Align with it. Move on.*
- **You want the analytic solution; it plans a neural network** — Different science. — *Catch it in the plan, before any code.*

Give the agent as much freedom as you are comfortable with. Spend your attention on the divergences that **change the result**.

*Autonomous runs name this failure implementation drift under execution pressure — the agent quietly substitutes an approach it finds easier. Trehan & Chopra, arXiv:2601.03315 (2026).*

> **Notes:** This is the thesis of the whole session — say it slowly and come back to it. Two failure directions: over-steering (you dictate every line and gain nothing) and under-steering (you accept a plan that answers a different question). The craft is telling those apart, and the cheapest place to do it is the plan, which is exactly why §5 Phase 1 has you read and annotate one. The cited paper found implementation drift in three of four autonomous research attempts — with a human reading the plan, it is catchable in a minute.

---

## §1 · The agent loop — Vibe-coding vs. AI-assisted engineering

- **Vibe-coding** — Prompt, accept, hope · You read little · Fine for throwaway
- **Disciplined use** — Plan, verify, review · **You own** architecture & review · Right for real work

> Studies of professional developers: they **plan before implementing and validate every output.**

> **Notes:** Reassure the physicists: you stay in control. The agent types; you decide and check. This framing recurs in §5.

---

## §1 · The agent loop — When to delegate

Agents shine on **small, well-specified** tasks. They struggle where **architectural judgement** is needed.

- **✓ Delegate** — “Add an RK4 step and test its convergence order.”
- **✗ Decide yourself** — “Redesign how the solver handles stiff systems.”

Today’s task is deliberately small — and that is the point.

> **Notes:** Teach the triage instinct. Part of the skill is recognizing what NOT to hand off. Ask: what is the smallest piece of your own work that would pass the left-hand test?

---

# §2 — A live demo

The loop in motion — mistakes included

---

## §2 · Live demo — Claude Code in 60 seconds

One terminal command, started **inside** the repo. Everything else is these five keys.

- **claude** — start a session in the current directory
- **Shift+Tab** — cycle the mode: **plan** (reads only) → edit automatically → manual
- **Esc** — interrupt — stop it mid-thought, no damage done
- **/clear** — wipe the context and start the next task clean
- **/permissions** — see and change what it may do without asking

- **Reasoning effort** — `low · medium · high · xhigh · max`, defaulting to `high`. More effort buys quality on genuinely hard work and costs you minutes of watching it think.

*Full reference: the cheat sheet at the end of this deck.*

> **Notes:** NEW slide, deliberately placed before the demo so absolute beginners can follow along. Show, don't just tell: open a terminal, run `claude`, press Shift+Tab twice so they see the mode indicator change, hit Esc once. 60 seconds, then move. The effort box moved here from §4 for one practical reason: they start their own first session in §3, and on high effort they will spend that segment watching a spinner. Say the recommendation out loud — sonnet, medium — and say why: nothing today is hard enough to need more.

---

## §2 · Live demo — Watch the loop

Plain script → a proper CLI, in real time.

    > turn scripts/run_decay.py into an argparse CLI with type hints and --help
    Reading scripts/run_decay.py…
    Editing scripts/run_decay.py…
    Running: uv run python scripts/run_decay.py --help
    error: unrecognized arguments: --steps
    Fixing the argument name…
    usage: run_decay.py [-h] [--k K] [--y0 Y0] [--steps STEPS]

Watch for the **plan** before any code — and for a **mistake** and its **recovery**. That recovery is the real skill.

> **Notes:** LIVE, not slides — this transcript is only a fallback if the demo cannot run. Run it in the terminal. Let them see Claude stumble and fix itself; narrate the loop as it happens. Keep it under six minutes. Ask them to jot down one thing they want to try.

---

# §3 — Understand the repo first

Read it, then write down what you found

---

## §3 · Understand the repo — Explore before you change

Build a mental map *before* touching code — yours and the agent’s.

- **Plan mode reads only** — Claude reads and answers, and leaves every file alone. Safe to point at code you care about.
- **Ask for the map** — Structure, entry points, how to run it, where the tests live.

> Understanding now is cheaper than unwinding a wrong change later.

> **Notes:** Show how to enter plan mode (Shift+Tab; the status line says plan mode on). This maps to the canonical first step: Explore. The same habit works on the 100k-line legacy code you inherited from a departed PhD student — that is the sales pitch for this audience.

---

## §3 · Understand the repo — Write the map down + `CLAUDE.md`

A repo can carry its own briefing: build and test commands, layout, the conventions it expects. `odelab` ships one — **read it**, it is the shape to aim for.

- **Plan mode** — How **you** read the repo. Answers land in the conversation and leave with it.
- **`CLAUDE.md`** — How the **repo** remembers. One file, on disk, in git, loaded every session.

Starting a repo that has none? `/init` explores it and drafts one for you — then you **cut it down**, which is what §4 is about.

*We are not running `/init` today: `odelab` already has a `CLAUDE.md`, so it would only offer to tidy it.*

> **Notes:** Be explicit about the division of labour: CLAUDE.md is how the repo remembers, plan mode is how you understand code. People conflate them. Open odelab's CLAUDE.md on screen and read two lines out loud — short, imperative, checkable — that lands the concision lesson before §4 even starts. Mention /init as the bootstrap for a repo with nothing, and say plainly that nobody needs to run it today; that saves twenty people generating a diff against a file we want to keep.

---

## §3 · Understand the repo — Explain `odelab`  ·  *your turn*

```bash
claude --model sonnet --effort medium
```

**Sonnet on `medium` is enough for everything today** — anything more and you spend the hands-on segments watching it think.

In **plan mode** (Shift+Tab), ask:

> explain this repository — structure, what each module does, how to run it and the tests

> where would I add a new integration method, and what should I test?

**Done when:** you can describe the repo in one sentence, and you have read its `CLAUDE.md`.

> **Notes:** Put the model line on the board before they start — sonnet, medium — and repeat the reason: on high effort this segment becomes a waiting room. The point is the habit, the repo is small enough to read by hand. Let two or three people share what Claude told them — especially anything it got wrong. Have them open odelab's CLAUDE.md at the end and compare it against what Claude just told them: the file is the short version of the same map.

---

# §4 — Steering the agent

Memory, skills, permissions — and where your data goes

---

## §4 · Steering the agent — Three kinds of memory

- **`~/.claude/CLAUDE.md`** — **User memory.** Every project, every session. How *you* work.
- **`./CLAUDE.md`** — **Project memory.** This repo, shared with the team through git.
- **Auto memory** — **Claude’s own notes** — what it learned about your project. On by default, machine-local.

The first two are instructions *you* write, and user memory pays its cost in **every** session. A real one:

    All Python projects use uv!
    Docstrings must follow numpy style!
    Never modify tests marked @pytest.mark.protected without explicit approval!
    GH issues and PRs must include p-<x> priority and effort-<x> labels.
    New features must start in a branch or git worktree.
    Explicit Error > User Warning > Silent Failure > Crash.

*`/memory` lists and opens all of them; the file closest to your working directory has the last word.*

> **Notes:** This excerpt is the instructor's actual user memory, which is why it reads like a person rather than a style guide. The line to point at is "new features must start in a branch" — it comes back in §5, so the audience sees a rule turn into behaviour within the hour. The label rule is a house convention for working PRs with an agent; we do not use it today, so name it in half a sentence and move on. Every line is imperative and checkable; none of them explain what git is. That is the register to aim for. Mention auto memory because they will see "Saved 2 memories" in the transcript and ask: Claude keeps its own notes per project under ~/.claude/projects/, loaded every session, and you can switch it off in /memory. The useful distinction is authorship — you write instructions, it writes observations.

---

## §4 · Steering the agent — `CLAUDE.md` — project memory

Instructions Claude reads **every session**: conventions, how to run things, gotchas. Loaded in full, however long it is — the official target is **under 200 lines**.

- **The concision test** — For each line ask: **“would removing this cause a mistake?”** If not — cut it.

> Bloated `CLAUDE.md` files get **ignored** — the rules that matter drown in the noise.

*It is context, delivered as a message — guidance, not enforcement. To make something impossible instead of merely requested, use a hook (§7).*

> **Notes:** Concision over completeness is THE lesson here. Show odelab's short CLAUDE.md as the model, and be honest that the failure mode is writing a style guide nobody — human or model — reads.

---

## §4 · Steering the agent — Skills — instructions on demand

`CLAUDE.md` is always loaded. A **skill** loads only when its description matches what you are doing — which keeps both of them short.

```markdown
# .claude/skills/decay-plots/SKILL.md
---
name: decay-plots
description: Plot solver output against the analytic solution.
             Use when making figures from odelab results.
---

Use matplotlib. Put the error on a log axis.
Label every axis with units. Save to figures/ as PDF.
```

- **`description`** says *when* to use it — the line beginners get wrong
- The body is plain instructions. A folder and a Markdown file is the entire format

> **Notes:** Skills deserve their own beat — they are the main customization lever people take home. Show the file, because the hands-on asks them to write one: people who have never seen a SKILL.md stall for five minutes on the frontmatter. Hammer the description field: write it as "use when…", since that is what the model matches against. Good first candidates: their plotting conventions, their docstring style, their group's slide template.

---

## §4 · Steering the agent — Permissions

Three modes, cycled with **Shift+Tab** — plus an allowlist for the commands you are tired of approving.

- **Plan** — reads only. Explore anything, change nothing.
- **Manual** — the default — asks before each edit and command.
- **Edit automatically** — edits freely, still asks for commands. Fast, wants a clean git tree.
- **/permissions** — the allowlist — grant `Bash(uv run pytest)` once, stop being asked.

> Your real protection is **git**, not the permission prompt. Commit before you let it run.

*Keep the agent on a leash you have consciously chosen — a dirty git tree is the one thing that makes a mistake expensive.*

> **Notes:** Demo /permissions live. The safety message: your real protection is git, not the permission prompt. The reasoning-effort card that used to sit here now lives on the §2 interface slide, where it arrives before their first session rather than after it.

---

## §4 · Steering the agent — Where does your data go?

$ git clone git@gitlab.icp.uni-stuttgart.de:icp/me/unpublished-results
    $ claude “summarise these results and write the methods section”

- **The agent reads everything** — Files it opens are sent to a service outside your institution.
- **Policies vary and change** — Retention and training terms differ per plan, and get revised.
- **Unpublished work** — Results, drafts, grant text, reviewer comments, student data.
- **Rules you signed** — Institutional policy, funder terms, GDPR, industry NDAs.

> Would you be comfortable with this content being read by a third party? If the answer is no, keep it out of the agent.

*University AI services: `uni-stuttgart.de/en/digital-services/ai-for-students` · ICP runs a local model for privacy-sensitive questions.*

> **Notes:** Do not skip this and do not moralise it — for this room it is the question that decides whether they use any of this on real work. Answer it in one honest sentence: code and files you point the agent at leave the building, so choose what you point it at. The local ICP model is the escape hatch for privacy-sensitive chat; verify the current URL, model and Mattermost command before the session, and be explicit that a local chat model is a different thing from the agentic loop we just taught — it will not run your tests for you.

---

## §4 · Steering the agent — Feel the steering  ·  *your turn*

Pick **one or two**:

1.  Add a rule to `CLAUDE.md` (“use NumPy-style docstrings”, “prefer dataclasses”), ask Claude for a small helper, then **remove the rule** and regenerate. Spot the difference.
2.  Use — or write — a tiny **skill** that encodes one personal convention.
3.  Compare **plan** and **edit automatically** on a trivial edit; open `/permissions`.

**Done when:** you have watched configuration visibly change Claude’s output.

> **Notes:** The "aha" is that a one-line rule changes the output. Keep it snappy — this is a warm-up for §5, not a project. Watch the clock: this is the segment to cut if §5 is at risk.

---

# ☕ Five minutes

Back for the main event

---

# §5 — Ship a feature

plan → test → implement → review → ship

---

## §5 · Ship a feature — The task: add RK4

Add a **4th-order Runge–Kutta** step alongside Euler — and prove it is better.

- **One branch** — Open `add-rk4` **before** any code lands. A feature starts on its own branch.
- **Several commits** — The tests, then the implementation. Two commits at least — commits are cheap.

*The canonical loop is Explore → Plan → Implement → Commit, and adversarial review is now part of it. **Test-first is our addition** — on numerical code it is what makes the rest trustworthy.*

plan → test → implement → review → ship

> **Notes:** Set the arc. Same five beats as the agent loop from §1 — point back at it. Two things to hammer: the branch exists before the first edit, and the failing test gets its own commit. A branch whose history reads "tests, then implementation" is reviewable; one giant commit is not. Total 46 minutes; call the phase changes out loud.

---

## §5 · Ship a feature — Say it precisely

- **Vague** — “Fix the integrator.” “Write some tests.” “Make it more accurate.” — *The agent guesses scope, place and approach.*
- **Precise** — “Add an `rk4_step` to `odelab/integrators.py`, used through `integrate(..., method=...)`, and assert convergence order 4 the way `test_euler_is_first_order` does.” — *One reading. Nothing left to invent.*

**Reduce what the agent has to assume:** which file, which function, what is wrong, how you want it fixed.

> **Notes:** The four questions are the checklist. This is the practical form of the divergence lesson from §1: every assumption you leave open is a place the plan can quietly diverge from your intent. Read the precise version out loud — people underestimate how much detail is useful, and it is still only one sentence.

---

## §5 · Phase 1 — Plan, then branch

Get a plan **before** any code. Plan mode, or a brainstorming pass.

- Have Claude draft the plan
- **Read it. Annotate it.** Then: *“address all my notes, do not implement yet”*
- This is the **divergence check** from §1 — the cheapest minute in the workshop
- Sign it off — then open the branch the work will live on

```bash
git switch -c add-rk4      # before the first edit, always
```

**plan** → test → implement → review → ship

> **Notes:** The annotation trick prevents premature coding — Claude tends to jump straight to implementing. "Do not implement yet" is the phrase to teach; make them say it out loud.

---

## §5 · Phase 1 — Plan RK4, open the branch  ·  *your turn*

> In plan mode: plan adding an `rk4_step` to `odelab`, reusing the existing `integrate(..., method=...)` hook.

- Review the plan and add a note or two of your own
- Tell it to revise the plan — **without coding yet**

```bash
git switch -c add-rk4
```

**Done when:** you have a plan you would sign off on, on a fresh branch.

> **Notes:** Circulate and read plans over shoulders. Common failure: the plan silently invents a new dispatch mechanism instead of reusing the method= hook — a good teaching moment about being specific. Check that everyone is off main before Phase 2 starts.

---

## §5 · Phase 2 — Test first — red, then commit

Give the agent a **pass/fail check** it can run itself. For numerical code, that is a test.

- **Accuracy** — RK4 matches the analytic decay to a tight tolerance.
- **Convergence order ≈ 4** — Double the steps → the error drops **~16×**. Euler manages ~2×.

The red test is a result worth keeping — **commit it on its own.**

plan → **test** → implement → review → ship

> **Notes:** Contrast with test_euler_is_first_order in the repo — it already asserts the ~2x factor, so they have a template. The convergence-order test is the real property to assert: it pins the method, not just one number.

---

## §5 · Phase 2 — Write the failing test  ·  *your turn*

> Add tests for `rk4_step` **before** implementing it — matching the analytic solution, and checking the convergence order.

```bash
uv run pytest -q                 # RED — rk4_step does not exist yet
git commit -am "Add failing RK4 accuracy + convergence tests"
```

**Done when:** the test fails for the right reason — and that failure is committed.

> **Notes:** "Fails for the right reason" matters: an ImportError is the expected red, a passing test means the test is wrong. Check a few screens for tests that assert nothing. Committing the red test is the habit to instil — it is the specification, and it survives whatever the implementation turns into.

---

## §5 · Phase 3 — Implement — green

Now let Claude implement, and **let the tests close the loop**.

    Editing odelab/integrators.py…
    Running: uv run pytest -q
    FAILED test_rk4_convergence_order — factor 8.1, expected ~16
    The k3 term steps a full dt. Fixing…
    - k3 = f(t + dt / 2, y + dt * k2)
    + k3 = f(t + dt / 2, y + dt / 2 * k2)
    6 passed

Without a runnable check, *“looks done”* is the only signal — and **you** become the verification loop. Green tests earn the **second commit**.

plan → test → **implement** → review → ship

> **Notes:** This is the payoff of the self-verifying loop: observe → revise, driven by pytest rather than by you. Let them watch Claude iterate. Point out that the failure message did the teaching, not the human.

---

## §5 · Phase 3 — Make it green  ·  *your turn*

> Implement `rk4_step` until my tests pass.

```bash
uv run pytest -q
git commit -am "Add RK4 integrator"
git log --oneline           # two commits: the spec, then the code
```

**Done when:** all tests pass and your branch holds two commits.

> **Notes:** Hands off the keyboard where possible — the point is watching the loop run itself. If someone is stuck in a correction spiral, that is failure pattern 2 from §6: /clear and reprompt. End by having them read their own git log: "tests, then implementation" is the shape to recognise.

---

## §5 · Phase 4 — Review

Two reviewers: the agent, and **you**. Both read the **whole branch**, both commits.

- `/code-review` takes your branch against `main`, or ask Claude to review it **adversarially**
- **Read the diff yourself** — correctness first, then clarity
- Request changes; re-run the tests; commit the fixes

> Do not merge what you did not read.

plan → test → implement → **review** → ship

> **Notes:** Universally recommended across every serious source: validate the output. "Adversarially" is the useful word — asking "is this correct?" invites agreement, asking "find what is wrong with this" does not.

---

## §5 · Phase 4 — Review the diff  ·  *your turn*

```bash
git diff main...HEAD      # the whole branch, both commits
```

> Review your change for correctness and clarity — find what is wrong with it.

Then read it yourself and request one improvement.

**Done when:** you have read every changed line and the tests still pass.

> **Notes:** Insist on the human read. Ask afterwards: who found something Claude's own review missed? Usually at least one person has an unnecessary helper or a docstring that contradicts the code.

---

## §5 · Phase 5 — Land it on `main`

The branch exists, holds two commits, and you have read every line. Bring it home.

```bash
git switch main
git merge --no-ff add-rk4        # keep the branch visible in the history
git log --oneline --graph
```

**Small and targeted is the point**, not the transport. Two commits you can read in a minute; nobody meaningfully reviews a thousand-line change — human or agent.

*Same discipline with a remote: push the branch and open a pull request, which is where CI and a second reader come in — see §7.*

plan → test → implement → review → **ship**

> **Notes:** Deliberately local: gh is not installed on the ICP machines and push credentials are one failure surface too many for twenty people at once. Nothing is lost — the reviewable-diff lesson is the durable part, and --no-ff keeps "tests, then implementation, on a branch" legible in the graph. Have them read their own git log --graph out loud. If anyone forked and wants the real thing, they can push and open the PR in the browser afterwards; point at §7 for gh and CI.

---

## §5 · Phase 5 — Merge it  ·  *your turn*

Ask Claude for the merge message first — **what & why**, and **how you tested it**. That paragraph is what a reviewer, or you in six months, actually reads.

```bash
git switch main
git merge --no-ff add-rk4
uv run pytest                    # green on main
git log --oneline --graph
```

- **Fast finishers** — The plots and the logistic example misbehave. Hunt and fix the planted **bugs** — start with `scripts/plot_decay.py`.

**Done when:** `main` holds your feature, the tests are green, and the graph shows the branch.

> **Notes:** Re-running pytest after the merge is the habit worth naming: green on the branch is not green on main. Three planted bugs for the fast finishers, answer key in instructor_notes.md: a sign error in the analytic overlay, an off-by-one in plot_error, and a wrong sign in rhs_logistic. The first one is the best teaching moment — the bug is in the reference, not the integrator.

---

# §6 — Common failure patterns

Five ways it goes wrong

---

## §6 · Failure patterns — Five ways it goes wrong — and the fix

- **Kitchen-sink session** — `/clear` between unrelated tasks
- **Correcting over and over** — After two tries: `/clear` and a better prompt
- **Over-specified `CLAUDE.md`** — Prune ruthlessly
- **Trust-then-verify gap** — Always give a check. Cannot verify → do not ship
- **Infinite exploration** — Scope narrowly, or delegate to a subagent

*Autonomous runs fail the same ways: overexcitement (declaring success on a failure), implementation drift, context degradation on long tasks. Trehan & Chopra, arXiv:2601.03315 · taxonomy: Cemri et al., arXiv:2503.13657.*

> **Notes:** Tie each one to what they just experienced in §5. Quick round: "what tripped you up?" — then map their answer onto a pattern. This debrief is worth protecting; it is where the session's lessons get named.

---

## §6 · Failure patterns — Why two of those are the same bug

Everything the agent reads — your files, test output, its own reasoning — sits in one finite window.

    0%|░░░░░░░░░░░░░░░░░░░░| fresh session
     80%|████████████████░░░░| explore · plan · edits · test output
    100%|████████████████████| full → /compact
     20%|████░░░░░░░░░░░░░░░░| summarised — the detail is gone

- `/context` — see what is filling it, including what your `CLAUDE.md` costs every session
- `/clear` between unrelated tasks · `/compact` to keep going through one
- **Write it to disk.** A plan file survives compaction; a subagent keeps its reading out of your window

> **Notes:** This slide explains pitfalls 1 and 2 — without it they are arbitrary rules. Run /context live: the CLAUDE.md line is the punchline of §4's concision lesson, made visible in tokens. "Write it down" is the durable habit: the annotated plan from §5 Phase 1 is not just a review artefact, it is the memory that survives a compaction.

---

# §7 — Beyond the basics

One more demo, and where to go next

---

## §7 · Beyond the basics — Subagents and hooks

- **Subagents** — A scoped task in its own context, reporting back a summary. The reading stays out of your window.
- **Hooks** — Deterministic automation on events. This one runs the suite after every edit:

```
// .claude/settings.json
"hooks": { "PostToolUse": [ {
    "matcher": "Edit|Write",
    "hooks": [ { "type": "command", "command": "uv run pytest -q" } ]
} ] }
```

Both are configuration, both are steering — §4 with a wider reach.

> **Notes:** A REAL short demo, not a throwaway mention — whichever you are most fluent in. The hook lands hardest with this audience: a failing test suite that speaks up before the agent claims success is exactly the trust-then-verify fix from §6, automated. A subagent is defined by a Markdown file in .claude/agents/ with a name, a description of when to use it, and a prompt — same shape as a skill.

---

## §7 · Beyond the basics — MCP — hand the agent a new tool

One protocol between agents and tools. Anthropic published it in November 2024; the other vendors adopted it.

```python
import subprocess
from fastmcp import FastMCP

mcp = FastMCP("cluster")

@mcp.tool
def job_status(job_id: str) -> str:
    """State of a SLURM job. Use when asked whether a run finished."""
    return subprocess.check_output(["squeue", "-j", job_id], text=True)
```

- The type hints tell the agent **what to pass**
- The docstring tells it **when to call** — the same lesson as a skill’s `description`

*The one to try first: **Context7**, which fetches current library documentation so the agent stops guessing APIs.*

> **Notes:** Nine lines to give any agent a new capability — that is the whole demystification. Pick whichever example is real for you; a squeue wrapper lands with this audience because everyone has typed it a hundred times. Note the trade-off honestly: an MCP server's tools sit in context whether you use them or not, so a skill wrapping a CLI you already have is often the cheaper answer. Use both, and know why.

---

## §7 · Beyond the basics — What other people have built

- **sirmalloc/ccstatusline** — a status line: model, context left, cost, at a glance
- **obra/superpowers** — a large skill collection — brainstorming, planning, TDD workflows
- **mattpocock/skills** — curated skills you can read in a minute each
- **anthropics/claude-code-action** — review every PR in CI — `/install-github-app` wires it up

Install from the official marketplace: `/plugin install superpowers@claude-plugins-official`

Read a skill before you install it. It is instructions going straight into your agent — the same trust question as any dependency.

*The fastest-moving slide in the deck: `mattpocock/skills` did not exist six months ago, and there are already eight community forks of `superpowers` with similar names. Check what you are installing.*

> **Notes:** Pointers, not a lab exercise — do not have twenty people npx-install a third-party skill pack mid-session; that is a network dependency and twenty new debugging surfaces. The transferable lesson is the one on the slide: a skill is instructions with your agent's privileges, so read it like you would read a dependency. Re-check these four links before every delivery.

---

## §7 · Beyond the basics — Take it further

### For your research code

- Numerical and property tests = your verifiable check
- `uv` + a lockfile = a reproducible environment
- Small PRs = code review that actually happens

### Worth a look next

- GitHub Actions auto-review, in front of human review
- `git worktree` for parallel agent work
- The `gh` CLI — let Claude open, read and comment on PRs

*Docs: `code.claude.com/docs` · `research_agentic_coding_workshops.md` in this repo for the evidence base.*

> **Notes:** Point them at the research doc for further reading. The worktree teaser is deliberate: mention it, do not demo it — it is the natural next step once one agent is not enough. Same for gh: it is not installed on the ICP machines, which is why §5 merged locally, but it is worth a sentence — `gh pr list --label claude`, then `gh pr view` and `gh pr comment`, is how an agent picks its own work back up tomorrow.

---

## §7 · Beyond the basics — Cheat sheet

### Driving the agent

- **claude** — start, in the repo — `--model sonnet --effort medium`
- **Shift+Tab** — plan / edit automatically / manual
- **Esc** — interrupt
- **/init** — draft a `CLAUDE.md` for a repo with none
- **/memory** — open user or project memory
- **/context** — what is filling the window
- **/clear** — new task, clean context
- **/permissions** — the allowlist
- **/code-review** — review the diff

### The workflow

- **explore** — plan mode, ask for the map
- **plan** — read it, annotate, revise
- **branch** — `git switch -c`, before any edit
- **test** — red for the right reason, commit
- **implement** — green, commit again
- **review** — adversarial, then your own eyes
- **ship** — `git merge --no-ff`, or a PR

*Photograph this slide.  Install `uv`: `docs.astral.sh/uv/getting-started/installation` · docs: `code.claude.com/docs`*

> **Notes:** NEW slide — the takeaway artifact. Pause here and let people actually photograph it; it is the one slide they will use tomorrow.

---

# Now run the loop on your own code.

goal → plan → act → observe → revise

Plan first · verify everything · review before you ship · keep it small

> **Notes:** Take-home: run the full loop on one small piece of your own code this week — one function, one test, one PR. Thank them, and stay for questions.

---
