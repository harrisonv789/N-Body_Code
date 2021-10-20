#!/usr/bin/env python3

# Import all needed packages
from modules.time import Time
from modules.cluster import Cluster
from modules.galaxy import Galaxy
from modules.system import System
from modules.integrator import *
from modules.analysis import Analysis
from modules.plot import Plotter
from modules.model import *
import numpy as np


##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
model_name = "kepler"  # The name of the model
dt = 1                  # The step size
output_dt = 0.01            # The output timestep to save data
tmax = 5000               # The max timestep
output = "body.dat"       # The output filename to store the data
use_analysis = False         # A flag for using the analysis tool
plot_data = True            # A flag for plotting data



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
if model_name.lower() == "kepler":
    model = KeplerModel(
        a       = 1.0, 
        e       = 0.6,
        v_mul   = 1.0,
    )

elif model_name.lower() == "isochrone":
    model = IsochroneModel(
        b       = 0.1,
        v_esc   = 0.5,
    )

elif model_name.lower() == "oscillator":
    model = OscillatorModel(
        rho     = 0.5,
    )

elif model_name.lower() == "logarithmic":
    model = LogarithmicModel(
        v0     = 1.0,
        Rc     = 0.2,
        q      = 0.8,
        v_mul  = 0.5,
    )

else:
    raise Exception("Invalid model name used.")

# Galaxy variables
galaxy_mass_a = 1.0
galaxy_mass_b = 1.0
rmin = 25
e = 0.6

# Calculated variables
M = sum([galaxy_mass_a, galaxy_mass_b])
a = rmin / (1.0 - e)
r = a * (1.0 + e)
v_0 = np.sqrt(a * (1 - e ** 2) * M) / r 

# Create the galaxy state vectors
galaxy_state_a = State(
    Vector(-r * galaxy_mass_a / M, 0, 0),
    Vector(0, -v_0 * galaxy_mass_a / M, 0),
    Vector()
)

# Create the first galaxy
galaxy_a = Galaxy(
    n_bodies = 120,
    mass = galaxy_mass_a,
    ring_spacing = 3,
    theta = 0,
    galaxy_pos = galaxy_state_a.x,
    galaxy_vel = galaxy_state_a.v,
)

# Create the first cluster
cluster_a = Cluster(
    model, 
    n_bodies = galaxy_a.n_bodies, 
    use_background = False,
    masses = galaxy_a.masses,
    init_callback = galaxy_a.init_callback,
)


# Get the second galaxy state
galaxy_state_b = State(
    Vector(r * galaxy_mass_b / M, 0, 0),
    Vector(0, v_0 * galaxy_mass_b / M, 0),
    Vector()
)

# Create the second galaxy
galaxy_b = Galaxy(
    n_bodies = 120,
    mass = galaxy_mass_b,
    ring_spacing = 3,
    theta = 45 * DEG2RAD,
    galaxy_pos = galaxy_state_b.x,
    galaxy_vel = galaxy_state_b.v,
)

# Create the second cluster
cluster_b = Cluster(
    model, 
    n_bodies = galaxy_b.n_bodies, 
    use_background = False,
    masses = galaxy_b.masses,
    init_callback = galaxy_b.init_callback,
)


# Create an array of clusters
clusters = [cluster_a, cluster_b]

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
integrator.execute(system, time, output, output_timestep = output_dt)

# If using the analysis tool
if use_analysis:
    analysis = Analysis("body_00000.dat", True)
    analysis.output()



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter()
    plotter.ask_plot()