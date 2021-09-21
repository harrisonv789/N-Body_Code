#!/usr/bin/env python3

# Import all needed packages
from matplotlib.pyplot import plot
import modules.mathematics as math
from modules.integrator import Integrator
from modules.time import Time
from modules.vector import Vector
from modules.state import State
from modules.plot import Plotter
from modules.body import Body



##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.1             # The step size
tmax = 2 * 3.141596   # The max timestep
output = "output.dat"   # The output filename
plot_data = True        # Whether or not to plot data

# Initial conditions
a = 1.0         # Ellipse radius
e = 0.1         # Ellipse eccentricity
theta = 0.0     # Ellipse angle



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the initial position, velocity and acceleration
x = Vector(math.get_kepler_x(a, e, theta),   0.0,                                0.0)
v = Vector(0.0,                              math.get_kepler_v(a, e, theta),     0.0)
a = math.calculate_acceleration(x)

# Create the initial state and time
state = State(x, v, a)
body = Body(state)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

inter = Integrator(output)
inter.execute(time, body)



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter(output=output)
    plotter.ask_plot()