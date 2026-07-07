# odelab

A tiny 1D ODE integrator, used as the practice project for the *Agentic AI for
Coding* workshop.

## What this is

`odelab` integrates initial-value problems `dy/dt = f(t, y)` with fixed-step,
one-step methods. Only forward Euler is implemented so far.

- `odelab/integrators.py` — the integrators (`euler_step`, `integrate`).
- `odelab/problems.py` — example right-hand sides and analytic solutions.
- `odelab/plotting.py` — plotting helpers.
- `tests/` — the pytest test-suite.
- `scripts/` — small runnable examples.

## Running things

This project uses [uv](https://docs.astral.sh/uv/).

- Sync the environment: `uv sync`
- Run the tests: `uv run pytest`
- Run an example: `uv run python scripts/run_decay.py`

## Conventions

- Keep functions small and pure where practical.
- A new numerical method must come with tests that check it against an analytic
  solution or a known convergence order.
