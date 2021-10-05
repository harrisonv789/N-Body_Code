#!/usr/bin/env python3

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
model_name = "logarithmic"   # The name of the model
dt = 0.001                  # The step size
tmax = 10 * PI               # The max timestep
output = "output.dat"       # The output filename to store the data
use_analysis = False        # A flag for using the analysis tool
plot_data = True            # A flag for plotting data



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
if model_name.lower() == "kepler":
    model = KeplerModel(
        a       = 1.0, 
        e       = 0.9,
        theta   = 0.0,
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
    )

else:
    raise Exception("Invalid model name used.")


# Create the system and the time
system = System(model, 1)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

integrator = LeapFrogIntegrator()
integrator.execute(system, time, output)

# If using the analysis tool
if use_analysis:
    analysis = Analysis(output, True)
    analysis.output()



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter(outputs=["output.dat"])
    plotter.ask_plot()