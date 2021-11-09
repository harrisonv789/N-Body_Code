#!/usr/bin/env python3

'''
EXAMPLE CASE: 3 BODY

This example shows three bodies with appropriate initial conditions following each
other that form a figure 8. This is a stable system.
'''

# Include previous directory
import sys
sys.path.append("../")

# Import all needed packages
from modules.time import Time
from modules.cluster import Cluster
from modules.system import System
from modules.integrator import *
from modules.plot import Plotter
from modules.model import *


##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.0001                  # The step size
output_dt = 0.01            # The output timestep to save data
tmax = 2 * PI               # The max timestep


##########################################################################
# SET UP THE SYSTEM 
##########################################################################

# Store the current model
model = KeplerModel(
    a       = 1.0, 
    e       = 0.7,
)

# Create a cluster
cluster = Cluster(
    model, 
    n_bodies = 3, 
    radius = 1.0, 
    vel_vec = Vector(0, 1, 0), 
    use_background = False,
    masses = [1],
    IC = "figure_eight"
)

# Create the system
system = System(
    cluster
)

# Create the time
time = Time(0, tmax, dt)


##########################################################################
# INTEGRATOR
##########################################################################

integrator = LeapFrogIntegrator()
integrator.execute(system, time, "body.dat", output_timestep = output_dt)



##########################################################################
# CREATES PLOT
##########################################################################

# Creates a plotter and asks user for plotting values
plotter = Plotter()
plotter.ask_plot()
