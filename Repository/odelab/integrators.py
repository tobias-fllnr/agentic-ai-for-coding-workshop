"""Explicit one-step ODE integrators for 1D initial-value problems.

An integrator advances the solution of ``dy/dt = f(t, y)`` from an initial
value ``y0`` over a time interval using a fixed number of equal steps.

Currently only the forward Euler method is implemented. Adding a higher-order
method (for example the classical Runge-Kutta method, RK4) is left as a
workshop exercise.
"""

from __future__ import annotations

from collections.abc import Callable

import numpy as np

# A right-hand side f(t, y) -> dy/dt
RHS = Callable[[float, float], float]
# A one-step method: given (f, t, y, dt) return y at t + dt
Method = Callable[[RHS, float, float, float], float]


def euler_step(f: RHS, t: float, y: float, dt: float) -> float:
    """Advance one forward-Euler step: ``y + dt * f(t, y)``."""
    return y + dt * f(t, y)


def integrate(
    f: RHS,
    y0: float,
    t0: float,
    t1: float,
    n_steps: int,
    method: Method = euler_step,
) -> tuple[np.ndarray, np.ndarray]:
    """Integrate ``dy/dt = f(t, y)`` from ``t0`` to ``t1`` in ``n_steps`` steps.

    Parameters
    ----------
    f:
        Right-hand side ``f(t, y)`` returning ``dy/dt``.
    y0:
        Initial value ``y(t0)``.
    t0, t1:
        Start and end of the integration interval.
    n_steps:
        Number of equal steps to take.
    method:
        One-step method used to advance the solution. Defaults to
        :func:`euler_step`.

    Returns
    -------
    (t, y):
        Arrays of length ``n_steps + 1`` including the initial point
        ``(t0, y0)``.
    """
    t = np.linspace(t0, t1, n_steps + 1)
    dt = (t1 - t0) / n_steps
    y = np.empty(n_steps + 1)
    y[0] = y0
    for i in range(n_steps):
        y[i + 1] = method(f, t[i], y[i], dt)
    return t, y
