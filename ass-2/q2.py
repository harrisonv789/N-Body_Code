#!/usr/bin/env python3

# Include previous directory
import sys
sys.path.append("../")

# Import all needed packages
from modules.time import Time
from modules.system import System
from modules.integrator import *
from modules.analysis import Analysis
from modules.plot import Plotter
from modules.model import *


##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.001                  # The step size
tmax = 2 * PI               # The max timestep
output = "output.dat"       # The output filename to store the data



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Create the model
model = LogarithmicModel(
    v0     = 1.0,
    Rc     = 0.2,
    q      = 0.8,
    v_mul  = 1.0
)

# Create the system and the time
system = System(model, 1, radius=1.0)
time = Time(0, tmax, dt)

# Create the integrator
integrator = LeapFrogIntegrator()
integrator.execute(system, time, output)


##########################################################################
# QUESTION A
##########################################################################

# Creates a plotter with the outputs
plotter = Plotter(outputs=["output.dat"])
plotter.plot("pos_x", ["pos_y"], "equal, star, grid, anim", "Question 2)a.")


##########################################################################
# QUESTION B
##########################################################################

# Question i
time.end = 10.75
model.v_mul = 1.01
system = System(model, 1, radius=0.52915)
integrator.execute(system, time, output)

# Plot the orbits
plotter = Plotter(outputs=["output.dat"])
plotter.plot("time", ["theta"], "grid", "Question 2)b.i.")
plotter.plot("pos_x", ["pos_y"], "equal, star, grid, anim", "Question 2)b.i.")
plotter.plot("time", ["radius", "E_kin"], "grid", "Question 2)b.i.")
plotter.plot("time", ["E_pot", "E_kin", "E_tot", "E_err"], "grid", "Question 2)b.i.")
