#!/usr/bin/env python3

# Include previous directory
import sys
sys.path.append("../")

# Import all needed packages
from modules.time import Time
from modules.body import Body
from modules.integrator import Integrator
from modules.plot import Plotter
from modules.constants import *
from modules.model import *

##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Create the Kepler model
model = KeplerModel(
    a       = 1.0, 
    e       = 0.7, 
    theta   = 0.0,
    M       = 1.0
)


##########################################################################
# CREATE ALL DATA
##########################################################################

# List of runs for different dts and file names
dts = [0.08, 0.04, 0.02]
files = ["q7_dt0.08.dat", "q7_dt0.04.dat", "q7_dt0.02.dat"]

# Create the output files
for idx in range(len(dts)):
    body = Body(model)
    time = Time(0, 6 * PI, dts[idx])        # t_0, t_max, dt
    inter = Integrator(model, files[idx])
    inter.execute(time, body)



##########################################################################
# CREATES PLOT
##########################################################################

# If plotting data
# Creates a plotter with the outputs
plotter = Plotter(outputs=files)

# Plot for Question a)
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "7)a.")

# Plot for Question b)
plotter.plot("time", ["tot_E"], ["grid"], "7)b.")