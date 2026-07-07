# Research: What other agentic-coding workshops teach

*Deep-research report — background input for designing our workshop. Companion to `first_notes.md` and `CLAUDE.md`.*

**Method:** 6 search angles → 24 sources fetched → 119 candidate claims → top 25 verified with 3-vote adversarial checking (need 2/3 to kill). 20 confirmed, 5 refuted. Confidence levels below reflect those votes. This is a fast-moving space; sources span mid-2025 to mid-2026.

---

## TL;DR

The dominant taught workflow everywhere is **plan-first, verify-everything** — canonically Anthropic's **Explore → Plan → Code → Commit**. That directly validates our plan→…→PR backbone. Our **TDD** and **explicit review** steps are *our own additions* — well-supported, but not part of the canonical four phases, so frame them as deliberate emphases.

**Two findings should change our plan:**
1. **Add a short codebase-understanding / exploration step before feature work.** Lifecycle-ordered courses start here; our plan currently folds it into CLAUDE.md steering.
2. **Don't relegate CLAUDE.md/skills/subagents/hooks/MCP entirely to end teasers.** Anthropic's own *beginner* courses treat customization as core content. Middle ground for 2h: promote CLAUDE.md + skills to full core status; give subagents/hooks/MCP a *real* (not throwaway) demo.

**Two of our planned items are NOT corroborated by any curriculum** and need justification or trimming: the **"models & reasoning effort"** module, and any assumption that a full curriculum *fits* in 2h (no validated 2h pacing benchmark exists — our timing is unproven design work).

---

## 1. What the research validates in our current plan

| Our plan element | Verdict | Evidence (confidence) |
|---|---|---|
| Plan → … → PR backbone | ✅ Strongly validated | Anthropic's recommended workflow is 4 phases: Explore (plan mode) → Plan → Implement → Commit+PR. An empirical study of professionals (13 field obs + 99 surveys) finds *"Professional developers do not vibe code… they plan before implementing and validate all agentic outputs."* **(high, 9-0)** |
| TDD / self-verifying loop | ✅ Validated as *our* emphasis | Anthropic: *"Set up Claude to verify its own work by running builds, tests, and lints… especially effective when you ask Claude to generate tests before writing code."* The mechanism: without a runnable pass/fail check, *"looks done" is the only signal and you become the verification loop.* **(high, 6-0)** |
| Explicit review step | ✅ Validated | Standard learning objective ("critically review agent-generated code for correctness, maintainability, security"); docs recommend an adversarial "Writer–Reviewer" review step. **(high, 3-0)** |
| Small, reviewable PRs | ✅ Validated | Agents excel at small well-specified tasks, fail on architectural ones (see §5). Keep the feature small. **(high, 6-0)** |
| Permissions / safety | ✅ Standard | Covered as "responsible use" module in research-audience curricula. |
| uv / reproducible envs | ✅ Good fit, unique | Not taught elsewhere as agentic content, but pairs naturally with the science-audience reproducibility gap (see §7). |

**Caveat to internalize:** TDD and the review step are *not* in the canonical four named phases. They're well-grounded additions — present them as "we go beyond the default loop, and here's why," not as "this is the standard."

---

## 2. FLAGGED changes to our plan

### FLAG 1 — Add a codebase-understanding / exploration step *before* feature work
Lifecycle-ordered courses (DeepLearning.AI/Anthropic) start with **"Setup & Codebase Understanding"** as its own module *before* "Adding Features." This maps to the **Explore** phase and to `/init` / repo-onboarding. Our plan doesn't distinguish it from CLAUDE.md steering. **(high; single-course basis)**
- **Action:** even a 5-minute opener — *"ask Claude to explain this repo"* / plan-mode exploration — fills the gap. With a well-prepared workshop repo a full module is likely compressible to this opener.

### FLAG 2 — Rethink "customization = end-of-session teasers"
Anthropic's **Claude Code 101** bundles it as one *core* lesson: *"Module 4: Customizing Claude Code — CLAUDE.md, Subagents, Skills, MCP, Hooks."* "Claude Code in Action" has a core **"Controlling Context"** module. The foundations webinar structures it as Foundations → **"Teach Claude your repo"** (CLAUDE.md, plan mode, skills, hooks) → "Scale & integrate" (subagents, MCP). **(high, 8-1)**
- **Action for 2h:** promote **CLAUDE.md + skills (+ custom commands)** to full core status (we already largely do). Give **subagents/hooks/MCP** a *real demo*, not a throwaway mention. Keep **git worktrees** as a teaser — promoting *that* specifically was refuted (1-2).

---

## 3. Content/modules worth adding

- **The "agent loop" as an explicit mental model** — teach `goal → plan → act → observe → revise` by name in the opening input section. Both a research-audience course (VIB) and Anthropic's foundations module front-load it before any hands-on. **(high, 6-0)**
- **Task-triage: "is this a good task to delegate?"** — agents are *"suitable for well-described, straightforward tasks but not complex tasks requiring architectural decisions."* Google's 2025 DORA report links AI adoption to **+9% bug rate and +91% review time**. Teach participants to recognize when *not* to delegate. **(high, 6-0)**
- **The vibe-coding vs. AI-assisted-engineering distinction** — a recurring framing: the human stays responsible for architecture and reviews the output. Good one-slide framing for a research audience wary of "AI writes my science." *(source lead, not in verified top-25)*

---

## 4. Concrete hands-on / demo designs to adopt

- **Same task, four ways (opening aha exercise)** — MIT Missing Semester (2026), verbatim: *"Compare the experience of coding by hand, using AI autocomplete, inline chat, and agents by doing the same programming task four times."* Self-contained, short-workshop-friendly, builds intuition for *where agents actually help*. **(high, 3-0)**
- **Plain script → CLI tool (opening demo)** — MIT ships a ready demo: take a plain Python script, ask the agent to turn it into an `argparse` CLI with type hints. Fast, visible, relatable for scientists with throwaway scripts. *(source lead)*
- **Live demos, not slides** — the Carpentries treat live coding as a *trainable skill* (dedicated episodes): *"Instructors do not use slides to teach coding… Learners get to see instructors' mistakes and how to diagnose and correct them."* Our agent demos should be live; the agent's *recoveries* are the teaching moment. **(high, 3-0)**
- **The "annotation cycle" for plan mode** — draft a `plan.md`, add inline notes where the agent made wrong calls, then instruct *"address all notes, don't implement yet"* (otherwise it starts coding). A concrete, teachable planning technique. *(source lead)*

---

## 5. Beginner pitfalls to teach explicitly

**Anthropic's five named failure patterns** — adopt this checklist wholesale as a "common mistakes" segment **(high, 3-0):**
1. **Kitchen-sink session** → `/clear` between unrelated tasks.
2. **Correcting over and over** → after two failed corrections, `/clear` and write a better initial prompt.
3. **Over-specified CLAUDE.md** → prune ruthlessly.
4. **Trust-then-verify gap** → always provide a verification (tests, scripts, screenshots); *if you can't verify it, don't ship it.*
5. **Infinite exploration** → scope investigations narrowly or use subagents.

Plus:
- **Keep CLAUDE.md concise** — *"Bloated CLAUDE.md files cause Claude to ignore your actual instructions."* Ask of each line: "would removing this cause a mistake?" Community norm ~<300 lines. Teach concision *over* completeness. **(high, 3-0)**
- **One feature per prompt** — *"If your prompt is more than a paragraph, it's probably too much."* *(source lead)*
- ⚠️ **But don't overclaim CLAUDE.md's importance** — "CLAUDE.md is the single biggest lever on performance" was **refuted (0-3)**. Teach it as important, not supreme.

---

## 6. Pacing & structure

- **Interleave short input with longer hands-on** (not lecture-then-practice). Software Carpentry (evidence-based researcher pedagogy) alternates short lessons with practical exercises. **(high, 9-0)**
- **"Install → shipped change within the session" arc** is an established shape — Anthropic's foundations webinar goes *"from a cold install to a fixed bug"* in ~60 min. Our "arrive-set-up → ship a PR" backbone mirrors this. **(high)**
- ⚠️ **No validated 2-hour benchmark exists.** The claim that a full curriculum *fits* in ~2h was **refuted (0-3)**. Research-audience full courses run ~6h / 5 modules. **Our timing is unproven and must be piloted** — expect to cut aggressively.

---

## 7. Scientific / research-audience specifics

**Good news:** the *most transferable* evidence in this research comes *from* research-audience programs — VIB (PhD students/postdocs/staff scientists), Software Carpentry (researchers), MIT Missing Semester. Their shared choices (agent-loop mental model, responsible-use/critical-review objective, interleaved input+practice, comparative-modality exercises, live demos) are therefore *already validated for our kind of audience*. **(medium)**

**Gap = our opportunity:** *none* of the sources addressed scientific-computing specifics — **numerical correctness, reproducibility, HPC/SLURM/cluster workflows, Jupyter/notebook integration, scientific-library conventions.** This is uncovered territory we can own, and it pairs naturally with two things we already have:
- **uv module → reproducibility** angle.
- **TDD section → numerical / property-based tests** as *the* verifiable pass/fail check for research code.

**Must-read for this audience:** "Claude Code for Scientists" (neuroai.science) — a researcher's concrete playbook (Plan-Execute-Evaluate loop) for scientific, non-web-dev code. *(source lead — high relevance, not in verified top-25.)*

---

## 8. What the research did NOT support (constrains our plan)

| Refuted claim | Vote | Implication for us |
|---|---|---|
| A 2h format is a proven/validated pacing benchmark | 0-3 | Our timing is unproven — pilot it. |
| "Apply different reasoning approaches for complexity levels" is a taught topic | 0-3 | **Our "models & reasoning effort" module is not corroborated as standard curriculum** — justify it as our differentiator, fold it into a broader "controlling the agent" segment, or trim it. |
| CLAUDE.md is the single biggest performance lever | 0-3 | Important, not supreme. |
| Context-window management is the single most important skill | 0-3 | Teach `/clear`, but don't over-elevate it. |
| Promote git worktrees from teaser to core | 1-2 | Keeping worktrees as a teaser is defensible. |

---

## 9. Open questions (for us to decide / pilot)

1. Realistic per-segment time allocation for *2h specifically* — no source gives one; needs a dry run.
2. How to adapt agentic pedagogy to *scientific code* (numerical correctness, reproducibility, HPC/SLURM, notebooks) — unaddressed by any source.
3. Is a dedicated codebase-understanding module worth the time in 2h, or does a prepared repo reduce it to a brief "explain this repo" opener?
4. What to do with the "models & reasoning effort" module given it isn't found in official curricula.

---

## Key sources

**Primary:**
- Anthropic — Best practices for Claude Code: https://code.claude.com/docs/en/best-practices
- Anthropic — Claude Code 101: https://anthropic.skilljar.com/claude-code-101
- Anthropic — Claude Code in Action: https://anthropic.skilljar.com/claude-code-in-action
- Anthropic — Foundations workshop webinar: https://www.anthropic.com/webinars/claude-code-workshop-foundations-june-11
- Anthropic — How Anthropic teams use Claude Code (PDF): https://www-cdn.anthropic.com/58284b19e702b49db9302d5b6f135ad8871e7658.pdf
- DeepLearning.AI/Anthropic — Claude Code course: https://www.deeplearning.ai/courses/claude-code-a-highly-agentic-coding-assistant
- VIB — Agentic Coding with GitHub Copilot (research audience): https://training.vib.be/all-trainings/agentic-coding-github-copilot
- Software Carpentry (researcher pedagogy): https://software-carpentry.org/
- MIT Missing Semester — Agentic Coding (2026): https://missing.csail.mit.edu/2026/agentic-coding/
- Empirical study of professional developers (arXiv): https://arxiv.org/html/2512.14012

**Notable secondary / leads:**
- Claude Code for Scientists (neuroai.science): https://www.neuroai.science/p/claude-code-for-scientists
- Agentic coding handbook — TDD workflow (Tweag): https://tweag.github.io/agentic-coding-handbook/WORKFLOW_TDD/
- Common beginner mistakes: https://claude-world.com/articles/common-beginner-mistakes/
- Vibe coding vs. AI-assisted engineering (A. Osmani): https://medium.com/@addyosmani/vibe-coding-is-not-the-same-as-ai-assisted-engineering-3f81088d5b98
