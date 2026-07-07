# odelab — practice repository

Practice project for the **Agentic AI for Coding** workshop. A tiny 1D ODE
integrator you'll extend, test, review, and ship a pull request for — all with
Claude Code.

## Setup

Requires [uv](https://docs.astral.sh/uv/) and Python ≥ 3.10.

```bash
uv sync                              # create the environment
uv run pytest                        # run the tests (should be green)
uv run python scripts/run_decay.py   # run an example
```

## Layout

| Path | What |
|---|---|
| `odelab/integrators.py` | `euler_step`, `integrate` |
| `odelab/problems.py` | example right-hand sides + analytic solutions |
| `odelab/plotting.py` | plotting helpers |
| `tests/` | pytest suite |
| `scripts/` | runnable examples |

## Ideas to explore during the workshop

- Add a higher-order method (e.g. classical Runge–Kutta, **RK4**) alongside Euler.
- Write tests that check a new method's **convergence order**.
- Add a script comparing methods' error vs. step size.
- Try integrating the **logistic** equation (`odelab.problems.rhs_logistic`) —
  does the solution behave the way you'd expect?
- Some of the plotting and example scripts may not be behaving correctly.
  Can you find and fix the bugs?
