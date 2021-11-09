#!/usr/bin/env python3

'''
EXAMPLE CASE: LOGARITHMIC POTENTIAL

Moves a point mass about a logarithmic potential background.
This state has 2κ = 3Ω for the epicyclic frequency.
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
dt = 0.01                   # The step size
output_dt = 0.01            # The output timestep to save data
tmax = 10 * PI            # The max timestep


##########################################################################
# SET UP THE SYSTEM 
##########################################################################

# Create the model
model = LogarithmicModel(
    v0     = 1.0,
    Rc     = 0.2,
    q      = 0.8,
    v_mul  = 1.0,
    use_v_circ = False
)

# Create a cluster
cluster = Cluster(
    model, 
    n_bodies = 1, 
    radius = 1.0, 
    use_background = True,
    masses = [1],
    vel_vec=Vector(0, 1, 0)
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
