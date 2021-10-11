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
dt = 0.01                  # The step size
tmax = 2.06 * PI            # The max timestep
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
plotter.plot("pos_x", ["pos_y"], "equal, star, grid, anim", "Question 2)a. Orbit Graph")


##########################################################################
# QUESTION B
##########################################################################

time.end = 7.15
model.v_mul = 1.01
system = System(model, 1, radius=0.52915)
integrator.execute(system, time, output)

# Plot the orbits
plotter = Plotter(outputs=["output.dat"])

# Question i
plotter.plot("pos_x", ["pos_y"], "equal, star, grid, anim", "Question 2)b.i. Orbit Graph")

# Question ii
plotter.plot("time", ["radius", "pos_x"], "grid, diffaxis", "Question 2)b.ii. Radius vs X Position")
plotter.plot("time", ["radius", "pos_y"], "grid, diffaxis", "Question 2)b.ii. Radius vs Y Position")
plotter.plot("time", ["radius", "theta"], "grid, diffaxis", "Question 2)b.ii. Radius vs Angle")

# Question iii
plotter.plot("time", ["E_pot", "E_kin", "E_tot", "E_err"], "grid", "Question 2)b.iii. Conservation of Energy")


##########################################################################
# QUESTION C
##########################################################################

time.end = 80 * PI
model.v_mul = 1.0
model.use_v_circ = False
system = System(model, 1, radius=1.0, vel_vec=Vector(0, 0, 1))
integrator.execute(system, time, output)

# Plot the orbits
plotter = Plotter(outputs=["output.dat"])
plotter.plot("pos_x", ["pos_z"], "equal, star, grid, anim, slow", "Question 2)c. Orbit Graph")


##########################################################################
# QUESTION D
##########################################################################

model.v_mul = 0.5
system = System(model, 1, radius=1.0, vel_vec=Vector(0, 0, 1))
integrator.execute(system, time, output)

# Plot the orbits
plotter = Plotter(outputs=["output.dat"])
plotter.plot("pos_x", ["pos_z"], "equal, star, grid, anim, slow", "Question 2)d. Orbit Graph")


##########################################################################
# QUESTION E
##########################################################################

model.v_mul = 1.0
system = System(model, 1, radius=1.0, vel_vec=Vector(0, 1, 1))
integrator.execute(system, time, output)

# Plot the orbits
plotter = Plotter(outputs=["output.dat"])
plotter.plot("pos_x", ["pos_y", "pos_z"], "3d, star, grid, anim, slow", "Question 2)e. 3D Orbit Graph")
