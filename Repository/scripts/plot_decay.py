"""Plot the decay solution and its error.

Run this and look at the figures -- does the output look the way you'd expect?
"""

import matplotlib.pyplot as plt

from odelab.integrators import integrate
from odelab.plotting import plot_error, plot_solution
from odelab.problems import exponential_decay

y0, k = 1.0, 1.0
t, y = integrate(exponential_decay(k), y0, 0.0, 5.0, n_steps=50)

plot_solution(t, y, y0, k)
plot_error(t, y, y0, k)
plt.show()
