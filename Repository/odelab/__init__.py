"""odelab — a tiny 1D ODE integrator for the agentic-coding workshop."""

from odelab.integrators import euler_step, integrate
from odelab.problems import analytic_decay, exponential_decay

__all__ = ["euler_step", "integrate", "exponential_decay", "analytic_decay"]
