#!/usr/bin/env python3

# Import all needed packages
from matplotlib.pyplot import plot
from modules.integrator import Integrator
from modules.time import Time
from modules.vector import Vector
from modules.state import State
from modules.plot import Plotter
from modules.body import Body
from modules.constants import *
from modules.model import *



##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.001             # The step size
tmax = 6 * PI   # The max timestep
output = "output.dat"   # The output filename
plot_data = True        # Whether or not to plot data

# Initial conditions
a = 1.0         # Ellipse radius
e = 0.7         # Ellipse eccentricity
theta = 0.0     # Ellipse angle



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
model = IsochroneModel()

# Store the initial position, velocity and acceleration
x = model.initial_position(a, e, theta)
v = model.initial_velocity(x, a, e, theta)
a = model.calc_acceleration(x)

# Create the initial state and time
state = State(x, v, a)
body = Body(state)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

inter = Integrator(model, output)
inter.execute(time, body)



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter(output=output)
    plotter.ask_plot()