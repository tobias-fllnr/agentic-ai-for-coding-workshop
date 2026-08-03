# Pre-workshop setup email

Send to everyone attending the retreat. Replace `<SLIDES LINK>` once the deck is online.

To send it with the formatting intact: `python3 Presentation/email_to_html.py`, then paste
`setup_email.html` into a Thunderbird compose window via *Insert → HTML*.

---

**Subject:** Agentic AI for Coding — 5 minutes of setup before the retreat

---

Hi everyone,

At the retreat we will have a hands-on session on **agentic AI for coding** with Claude
Code. To ensure everthing goes smoothly, please set everything up by working through the three
steps below **before** you leave. They take about five minutes.

## 1. Get the practice repository

We work in `odelab`, a small ODE-integrator project:
https://github.com/tobias-fllnr/odelab

Click **Fork** (top right) to create your own copy, then clone it:

```bash
git clone https://github.com/<your-github-user>/odelab.git
cd odelab
git remote show origin      # should show your fork, not ours
```

## 2. Check `uv`

We use `uv` throughout the workshop, so you do need it. It manages the Python environment
for you and runs everything through `uv run ...`. On the ICP machines it is **already installed**, 
so a quick check is enough:

```bash
uv --version
```

Only if that comes back as `command not found`, install it:
https://docs.astral.sh/uv/getting-started/installation

Then, inside the `odelab` folder:

```bash
uv sync                     # creates the environment
uv run pytest               # 4 tests should pass
uv cache dir                # e.g. /tikhome/<you>/.cache/uv
```

Is that cache path on the same filesystem as your `odelab` folder — both under `/tikhome`,
for example? If yes, there is nothing to do. If not, nothing is broken either: installs are
just slower, and we will cover the fix in the workshop.

## 3. Check that Claude Code runs

If you have access to Claude Code — through a seat on the institute team plan or your own
private subscription — please install it (https://code.claude.com/docs) and check that it
starts **inside** the repository:

```bash
claude
```

**No access at all? Then there is nothing to do here.** Not everyone has a seat, and you will work with someone who has access to Claude.

Never used `uv` or Claude Code before? That is fine — the session assumes no prior
experience and starts with `uv` from scratch. If something does not work, just ask Tobi.

Already courious about the workshop? Check out the slides here: <SLIDES LINK>

See you at the retreat!

Fabi and Tobi
