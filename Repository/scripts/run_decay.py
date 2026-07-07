"""Integrate the exponential-decay problem and print the result.

A deliberately plain script -- a good candidate to turn into a proper
command-line tool.
"""

from odelab.integrators import integrate
from odelab.problems import analytic_decay, exponential_decay

y0 = 1.0
k = 1.0
t0 = 0.0
t1 = 5.0
n_steps = 50

t, y = integrate(exponential_decay(k), y0, t0, t1, n_steps)

print(f"Integrating dy/dt = -{k} * y  from  y({t0}) = {y0}")
print(f"  steps:              {n_steps}")
print(f"  y({t1}) numerical:  {y[-1]:.6f}")
print(f"  y({t1}) analytic:   {analytic_decay(t1, y0, k):.6f}")
