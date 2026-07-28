start with the uv crash course before any agentic things. We mention the "UV_CACHE_DIR" because uv must symlink dependencies, other than conda / venv it does not copy but ideally symlink to a shared cache. If you have nfs mounts like /data /work /tikhome you should define e.g. direnv such that the UV_CACHE_DIR for each is set to e.g. `/data/<your-user-name>/uv-cache` and `/work/<your-user-name/<uv-cache` respectively. Otherwise it will default to your home and if uv can't symlink it will fallback to copy which you should avoid.
UV is great because of the cache it is fast, it resolve is fast, it ships a lock, different python binaries easily assesible etc, looks similiar to venv ... (subagent what people love about uv)

"uv run python scripts/run_decay.py" can just be `uv run scripts/run_decay.py` as well.
Mention `uv init` for new projects as well.

"Get the repo running" is missing a git clone and cd repo cmd.

"Explore before you change" -> there is a "claude /init" command for this
"§3 · Understand the repo" should be redone and use the `/init` command


somewhere add a slide with useful tools like https://github.com/sirmalloc/ccstatusline , https://github.com/obra/superpowers , https://github.com/mattpocock/skills ...

Check `/context` slash command in claude code. Check `/Users/fzills/tools/presentations` has an agentic ai presentation and what can be reused from there e.g. review which version this or theirs is better and incroporate here.

Phase 5 e.g switch to a branch and commit should be much earlier! E.g. before you even implement you must switch to a branch. Then you can follow TDD e.g. write a failing test, commit the test, add the implementation, commit it. Don't be afraid of commits. You can / should have more than a single commit per feature at least tests and implementation in two commits.

Include maybe in the setup or here the "https://cli.github.com/" tool to create PRs from the CLI via claude code. Consider letting claude label the PR as well with e.g. `claude` and priority and effort labels like `p0-critical` or `effort-2-small`. This will also allow claude to find PRs easier or comment / review them.

