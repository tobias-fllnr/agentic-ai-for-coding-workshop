"""Plotting helpers for visualising integrator output."""

from __future__ import annotations

import matplotlib.pyplot as plt
import numpy as np

from odelab.problems import analytic_decay


def plot_solution(t, y, y0, k=1.0, ax=None):
    """Plot a numerical decay solution against the analytic curve."""
    if ax is None:
        _, ax = plt.subplots()
    ax.plot(t, y, "o-", label="numerical")
    exact = y0 * np.exp(k * np.asarray(t))
    ax.plot(t, exact, "-", label="analytic")
    ax.set_xlabel("t")
    ax.set_ylabel("y")
    ax.set_title("Exponential decay")
    ax.legend()
    return ax


def plot_error(t, y, y0, k=1.0, ax=None):
    """Plot the absolute error of a numerical solution vs. the analytic one."""
    if ax is None:
        _, ax = plt.subplots()
    exact = analytic_decay(t, y0, k)
    error = np.abs(y[:-1] - exact)
    ax.semilogy(t, error)
    ax.set_xlabel("t")
    ax.set_ylabel("|error|")
    ax.set_title("Integration error")
    return ax
