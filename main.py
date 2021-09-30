#!/usr/bin/env python3

# Import all needed packages
from modules.time import Time
from modules.body import Body
from modules.integrator import *
from modules.analysis import Analysis
from modules.plot import Plotter
from modules.constants import *
from modules.model import *



##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.0003               # The step size
tmax = 2 * PI          # The max timestep
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
        b       = 0.1,
        v_esc   = 0.5,
        M       = 1.0
    )

elif model_name.lower() == "oscillator":
    model = OscillatorModel(
        r       = 1.0,
        rho     = 0.5,
        M       = 1.0
    )

else:
    raise Exception("Invalid model name used.")


# Create the initial state and time
body = Body(model)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

integrator = LeapFrogIntegrator()
integrator.execute(model, time, body, output)

analysis = Analysis(output, True)
#analysis.output()



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
if plot_data:

    # Creates a plotter with the outputs
    plotter = Plotter(outputs=["output.dat"])
    plotter.ask_plot()