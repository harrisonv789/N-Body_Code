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
model_name = "kepler"       # The name of the model
dt = 0.01                   # The step size
output_dt = 0.01            # The output timestep to save data
tmax = 10                   # The max timestep
output = "body.dat"         # The output filename to store the data
use_analysis = True        # A flag for using the analysis tool
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
integrator.execute(system, time, output, output_timestep = output_dt)

# If using the analysis tool
if use_analysis:
    analysis = Analysis("output/body_00000.dat", True)
    analysis.output()



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter()
    plotter.ask_plot()