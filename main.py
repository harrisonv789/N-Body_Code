#!/usr/bin/env python3

# Import all needed packages
from modules.time import Time
from modules.body import Body
from modules.integrator import Integrator
from modules.plot import Plotter
from modules.constants import *
from modules.model import *



##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.1             # The step size
tmax = 6 * PI   # The max timestep
output = "output.dat"   # The output filename
plot_data = True        # Whether or not to plot data
model_name = "kepler"   # The name of the model


##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the current model
if model_name.lower() == "kepler":
    model = KeplerModel(
        a       = 1.0, 
        e       = 0.7, 
        theta   = 0.0,
        M       = 1.0
    )

elif model_name.lower() == "isochrone":
    model = IsochroneModel(
        r       = 1.0,
        b       = 0.10,
        v_esc   = 0.95,
        M       = 1.0
    )

elif model_name.lower() == "oscillator":
    model = OscillatorModel(
        r       = 1.0,
        rho     = 1.0,
        M       = 1.0
    )

else:
    raise Exception("Invalid model name used.")


# Create the initial state and time
body = Body(model.init_state)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

inter = Integrator(model, output)
inter.execute(time, body)



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter(output=output)
    plotter.ask_plot()