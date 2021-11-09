#!/usr/bin/env python3

'''
EXAMPLE CASE: GALAXY ROTATION

This example shows rotation in a galaxy, showing a number of particles orbiting a
single galaxy. Each particle does not have a mass except for the central bulge particle.
'''

# Include previous directory
import sys
sys.path.append("../")

# Import all needed packages
from modules.time import Time
from modules.cluster import Cluster
from modules.galaxy import Galaxy
from modules.system import System
from modules.integrator import *
from modules.plot import Plotter
from modules.model import *


##########################################################################
# PARAMETERS
##########################################################################

# Time parameters
dt = 0.1                          # The step size
output_dt = 1                     # The output timestep to save data
tmax = 100                        # The max timestep


##########################################################################
# GALAXY 
##########################################################################

# Create the galaxy
galaxy = Galaxy(
    n_bodies = 120,
    mass = 1.0,
    ring_spacing = 3,
    theta = 0,
)

# Create the cluster of stars
cluster = Cluster(
    KeplerModel(), 
    n_bodies = galaxy.n_bodies, 
    use_background = False,
    masses = galaxy.masses,
    init_callback = galaxy.init_callback,
)


##########################################################################
# SYSTEM
##########################################################################

# Create an array of clusters
clusters = [cluster]

# Create the system
system = System(
    clusters
)

# Create the time step
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
