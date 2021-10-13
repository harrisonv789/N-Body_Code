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
dt = 0.0001                  # The step size
output_dt = 0.01            # The output timestep to save data
tmax = 2 * PI               # The max timestep
output = "body.dat"         # The output filename to store the data



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
model = KeplerModel(
    a       = 1.0, 
    e       = 0.7,
)

# Create the system
system = System(
    model, 
    n_bodies = 2, 
    radius = 1.0, 
    vel_vec = Vector(0, 1, 0), 
    use_background = False,
    masses = [2, 1],
    IC = "two_body"
)

# Create the time
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

integrator = LeapFrogIntegrator()
integrator.execute(system, time, output, output_timestep = output_dt)



##########################################################################
# QUESTION 4 -> e = 0.7
##########################################################################

# Plots the position
plotter = Plotter(outputs = ["output/body_00000.dat", "output/body_00001.dat"])
plotter.plot(
    "pos_x", 
    ["pos_y"], 
    ["anim", "equal", "limits", "grid", "nolegend", "fast"],
    "$e=0.7$ Keplerian 2-body Plot",
    )

# Plots the conservation
plotter = Plotter(outputs = ["output/system.dat"])
plotter.plot(
    "time", 
    ["E_kin", "E_pot", "E_tot", "E_err"], 
    ["grid"],
    "$e=0.7$ Energy Conservation",
    )



##########################################################################
# QUESTION 4 -> e = 0.9
##########################################################################

# Reset the system
system.model.e = 0.9
system.reset()

# Execute the solution again
integrator.execute(system, time, output, output_timestep = output_dt)

# Plots the position
plotter = Plotter(outputs = ["output/body_00000.dat", "output/body_00001.dat"])
plotter.plot(
    "pos_x", 
    ["pos_y"], 
    ["anim", "equal", "limits", "grid", "nolegend", "fast"],
    "$e=0.9$ Keplerian 2-body Plot",
    )

# Plots the conservation
plotter = Plotter(outputs = ["output/system.dat"])
plotter.plot(
    "time", 
    ["E_kin", "E_pot", "E_tot", "E_err"], 
    ["grid"],
    "$e=0.9$ Energy Conservation",
    )