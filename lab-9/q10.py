#!/usr/bin/env python3

# Include previous directory
import sys

from matplotlib.pyplot import plot
sys.path.append("../")

# Import all needed packages
from modules.time import Time
from modules.body import Body
from modules.integrator import Integrator
from modules.analysis import Analysis
from modules.plot import Plotter
from modules.constants import *
from modules.model import *


##########################################################################
# CREATE ALL STARTING DATA
##########################################################################

# List of runs for different velocities and files
r = [1.0, 10.0]
files = ["q10_r1.0.dat", "q10_r10.0.dat"]

# Create the output files
for idx in range(len(r)):
    # Create the model
    model = OscillatorModel(r = r[idx], Omega = 1, M = 1.0)
    body = Body(model)

    # Create the timing settings
    time = Time(0, 2 * PI, 0.001)        # t_0, t_max, dt

    # Create and run the integrator and analysis tool
    inter = Integrator(model, files[idx])
    inter.execute(time, body)
    analysis = Analysis(files[idx], True)



##########################################################################
# QUESTION 10
##########################################################################

# Plots for Question 10
plotter = Plotter(outputs=files, analysis=True)

# Plot each question
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "10) Orbit Graph", files=files)
plotter.plot("time", ["pos_x"], ["grid"], "10) Orbit Position (x) vs Time", files=files)
plotter.plot("time", ["pos_y"], ["grid"], "10) Orbit Position (y) vs Time", files=files)
plotter.plot("time", ["theta"], ["grid", "dashed"], "10) Orbit Angle ($\\theta$) vs Time", files=files)
