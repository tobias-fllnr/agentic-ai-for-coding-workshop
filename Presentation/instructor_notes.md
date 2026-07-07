# Instructor notes — `Repository/` answer key

*Keep this in `Presentation/` — it is **not** part of the participant repo.*

## Baseline

`uv sync && uv run pytest` → **4 tests pass** (green baseline for §2). Verified with
uv 0.11.18 / Python 3.12, numpy 2.5, matplotlib 3.11.

## Planted bugs (§5 stretch: bug hunt)

All three live in code paths the baseline tests do **not** cover, so they don't break the
green suite. Surfaced by `uv run python scripts/plot_decay.py` and by trying the logistic
example (see `README.md` "Ideas to explore").

1. **Sign error — `odelab/plotting.py::plot_solution`.**
   Analytic overlay is `y0 * np.exp(k * t)` (missing the minus sign) → the "analytic"
   line grows instead of decaying, making the *correct* numerical solution look wrong.
   **Fix:** `np.exp(-k * t)` (or reuse `analytic_decay`). Teaching point: the bug was in
   the *reference/plot*, not the integrator — beware misattributing blame.

2. **Off-by-one — `odelab/plotting.py::plot_error`.**
   `error = np.abs(y[:-1] - exact)` — `y[:-1]` has length `n` but `exact`/`t` have length
   `n+1` → `ValueError: operands could not be broadcast (50,) (51,)`.
   **Fix:** `error = np.abs(y - exact)`.

3. **Wrong model term — `odelab/problems.py::rhs_logistic`.**
   Returns `r * y * (1 + y / K)` → positive feedback, solution diverges to `inf` instead
   of saturating at the carrying capacity `K`.
   **Fix:** `r * y * (1 - y / K)`. (Docstring already states the correct equation, a good
   spot-the-mismatch clue.)

## Backbone feature (§5): add RK4

Reference implementation participants (via Claude, TDD) should arrive at:

```python
def rk4_step(f, t, y, dt):
    k1 = f(t, y)
    k2 = f(t + dt / 2, y + dt / 2 * k1)
    k3 = f(t + dt / 2, y + dt / 2 * k2)
    k4 = f(t + dt, y + dt * k3)
    return y + dt / 6 * (k1 + 2 * k2 + 2 * k3 + k4)
```

Used via the existing hook: `integrate(f, y0, t0, t1, n, method=rk4_step)`.

**Expected tests (TDD, red → green):**
- Matches `analytic_decay` to tight tolerance (e.g. `< 1e-6` for modest `n`).
- **Convergence order ~4:** doubling `n_steps` shrinks the max error by ~16× (contrast
  with Euler's ~2× in `test_euler_is_first_order`).

## Notes / levers

- If a group is fast, the logistic bug + a plot comparing Euler vs RK4 error is a natural
  extension.
- `scripts/run_decay.py` is intentionally plain (hardcoded params) for the §1 "turn it
  into an argparse CLI" demo.
