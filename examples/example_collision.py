#!/usr/bin/env python3

'''
EXAMPLE CASE: GALACTIC COLLISION

This is an example on how to code a galaxy collision with the N-body-code.
This code showcases uses the M51 galaxy initial conditions and the collision with the smaller galaxy.

NOTE:
This code takes a long time to simulate.
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

# Time Parameters
dt          = 0.2                   # The step size
output_dt   = 10                    # The output timestep to save data
tmax        = 5000                  # The max timestep

# Galaxy Parameters
rmin        = 25                    # The minimum distance between the two galaxies
e           = 0.8                   # The eccentricity of the galactic orbit
mass_g_a    = 1.0                   # The mass of Galaxy A [10^11 Msun]
mass_g_b    = 1.0/3.0               # The mass of Galaxy B [10^11 Msun]
theta_g_a   = 0                     # The inclination angle of Galaxy A [degrees]
theta_g_b   = -70                   # The inclination angle of Galaxy B [degrees]
spacing_g_a = 3                     # The ring spaing of Galaaxy A [kpc]
spacing_g_b = 3                     # The ring spaing of Galaaxy B [kpc]
bodies_g_a  = 120                   # The number of test bodies of Galaxy A
bodies_g_b  = 120                   # The number of test bodies of Galaxy B



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
model = KeplerModel()

# Calculated Variables
M = sum([mass_g_a, mass_g_b])               # Total Mass
a = rmin / (1.0 - e)                        # Semi-Major Axis
r = a * (1.0 + e)                           # Separation Distance
v_0 = ((a * (1 - e ** 2) * M) ** 0.5) / r   # Base Velocity Factor
model = KeplerModel()                       # The model of the system used


##########################################################################
# GALAXY A
##########################################################################

# Create the Galaxy A state vectors
galaxy_state_a = State(
    Vector(-r * mass_g_b / M, 0, 0),
    Vector(0, -v_0 * mass_g_b / M, 0),
    Vector()
)

# Create Galaxy A
galaxy_a = Galaxy(
    n_bodies = bodies_g_a,
    mass = mass_g_a,
    ring_spacing = spacing_g_a,
    theta = theta_g_a * DEG2RAD,
    galaxy_pos = galaxy_state_a.x,
    galaxy_vel = galaxy_state_a.v,
)

# Create the cluster for Galaxy A
cluster_a = Cluster(
    model, 
    n_bodies = galaxy_a.n_bodies, 
    use_background = False,
    masses = galaxy_a.masses,
    init_callback = galaxy_a.init_callback,
)


##########################################################################
# GALAXY B
##########################################################################

# Create the Galaxy B state vectors
galaxy_state_b = State(
    Vector(r * mass_g_a / M, 0, 0),
    Vector(0, v_0 * mass_g_a / M, 0),
    Vector()
)

# Create Galaxy B
galaxy_b = Galaxy(
    n_bodies = bodies_g_b,
    mass = mass_g_b,
    ring_spacing = spacing_g_b,
    theta = theta_g_b * DEG2RAD,
    galaxy_pos = galaxy_state_b.x,
    galaxy_vel = galaxy_state_b.v,
)

# Create the cluster for Galaxy B
cluster_b = Cluster(
    model, 
    n_bodies = galaxy_b.n_bodies, 
    use_background = False,
    masses = galaxy_b.masses,
    init_callback = galaxy_b.init_callback,
)


##########################################################################
# SYSTEM
##########################################################################

# Create the system
system = System (clusters = [cluster_a, cluster_b])

# Create the time step
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

# Create the integrator and execute the integration
integrator = LeapFrogIntegrator()
integrator.execute(system, time, "body.dat", output_timestep = output_dt)



##########################################################################
# CREATES PLOT
##########################################################################

# Creates a plotter with the outputs
# Gets list of body files
body_outputs = ["output/" + file for file in os.listdir("output") if "body" in file]
plotter = Plotter(outputs = body_outputs)

# Create the parameters
params = {
    "animate": True,
    "legend": False,
    "lines": False,
    "limits": True,
    "limits_x_min": -75.0,
    "limits_x_max": +200.0,
    "limits_y_min": -100.0,
    "limits_y_max": +100.0,
    "marker_size": 1.5,
    "marker_color": "red",
    "save": "M51_plot.mp4",
    "interval": 30,
}

# Plot the X-Y plot
plotter.plot(
    "pos_x", 
    "pos_y",
    **params,
)

# Plot the energy plot
system_outputs = ["output/" + file for file in os.listdir("output") if "system" in file]
plotter = Plotter(outputs = system_outputs)
plotter.plot(
    "time",
    ["E_kin", "E_pot", "E_tot"],
    animate = False,
    line_style = "dashed",
    marker = "",
    title = "M51 Energy Conservation over Time",
    save = "M51_energy.png",
)

# Ask plot for user input
plotter = Plotter()
plotter.ask_plot()
