"""Example right-hand sides and analytic reference solutions.

Each ``*_rhs`` / factory returns a function with signature ``f(t, y) -> dy/dt``
suitable for passing to :func:`odelab.integrators.integrate`.
"""

from __future__ import annotations

import numpy as np


def exponential_decay(k: float = 1.0):
    """Return the RHS of ``dy/dt = -k y`` (exponential decay)."""

    def rhs(t: float, y: float) -> float:
        return -k * y

    return rhs


def analytic_decay(t, y0: float, k: float = 1.0):
    """Exact solution of ``dy/dt = -k y``:  ``y0 * exp(-k t)``."""
    return y0 * np.exp(-k * np.asarray(t))


def rhs_logistic(r: float = 1.0, K: float = 1.0):
    """Return the RHS of the logistic equation ``dy/dt = r y (1 - y/K)``.

    The solution should grow and then saturate at the carrying capacity ``K``.
    """

    def rhs(t: float, y: float) -> float:
        return r * y * (1 + y / K)

    return rhs
