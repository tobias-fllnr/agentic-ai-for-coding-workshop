"""Baseline tests for the odelab integrators. These should all pass."""

import numpy as np

from odelab.integrators import euler_step, integrate
from odelab.problems import analytic_decay, exponential_decay


def test_euler_step_advances_linearly():
    # dy/dt = 2  =>  one step of size 0.5 adds 1.0
    f = lambda t, y: 2.0
    assert euler_step(f, 0.0, 5.0, 0.5) == 5.0 + 0.5 * 2.0


def test_integrate_preserves_initial_condition():
    f = exponential_decay(k=1.0)
    t, y = integrate(f, y0=3.0, t0=0.0, t1=1.0, n_steps=10)
    assert t[0] == 0.0
    assert y[0] == 3.0
    assert len(t) == len(y) == 11


def test_integrate_matches_analytic_decay():
    y0, k = 1.0, 1.0
    t, y = integrate(exponential_decay(k), y0, 0.0, 2.0, n_steps=2000)
    exact = analytic_decay(t, y0, k)
    assert np.max(np.abs(y - exact)) < 1e-2


def test_euler_is_first_order():
    # Doubling the number of steps should roughly halve the error (order ~1).
    y0, k = 1.0, 1.0
    err = {}
    for n in (100, 200):
        t, y = integrate(exponential_decay(k), y0, 0.0, 1.0, n_steps=n)
        err[n] = np.max(np.abs(y - analytic_decay(t, y0, k)))
    ratio = err[100] / err[200]
    assert 1.7 < ratio < 2.3
