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
v_mults = [0.01, 0.10, 0.50, 1.00, 1.10, 1.40]
files = ["q9_0.01.dat", "q9_0.10.dat", "q9_0.50.dat", "q9_1.00.dat", "q9_1.10.dat", "q9_1.40.dat"]

# Create the output files
for idx in range(len(v_mults)):
    # Create the model
    model = IsochroneModel(r = 1.0, b = 0.1, M = 1.0, v_mul = v_mults[idx])
    body = Body(model)

    # Create the timing settings
    time = Time(0, 10 * PI, 0.01)        # t_0, t_max, dt

    # Create and run the integrator and analysis tool
    inter = Integrator(model, files[idx])
    inter.execute(time, body)
    analysis = Analysis(files[idx], True)



##########################################################################
# QUESTION A
##########################################################################

# Plots for Question a) ii.
plotter = Plotter(outputs=files, analysis=True)
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)a.ii. Orbit Graph", files=files[:4])
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)a.ii. Orbit Graph", files=files[3:])

# Plots for Question a) iii.
plotter.plot("max", ["radius"], ["grid"], "9)a.iii. Maximum Radius", True)
plotter.plot("min", ["radius"], ["grid"], "9)a.iii. Minimum Radius", True)
plotter.plot("time", ["radius"], ["grid"], "9)a.iii. Log Radius vs Time")
plotter.plot("time", ["radius"], ["grid", "logy"], "9)a.iii. Log Radius vs Time")

# Plots for Question a) iv.
time = Time(0, 100 * PI, 0.1)
model = IsochroneModel(r = 1.0, b = 0.1, M = 1.0, v_mul = v_mults[-1])
body = Body(model)
inter.execute(time, body)
plotter.load_data()
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)a.iv. 100 $\pi$ Orbit", files=files[-1:])

time = Time(0, 1000 * PI, 0.1)
body.reset()
inter.execute(time, body)
plotter.load_data()
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)a.iv. 1000 $\pi$ Orbit", files=files[-1:])


##########################################################################
# QUESTION B
##########################################################################

# Recreate runs for Question b)

# List of runs for different velocities and files
v_esc = [0.5, 0.9, 0.95, 0.99, 1.0]
files = ["q9_vesc_0.5.dat", "q9_vesc_0.9.dat", "q9_vesc_0.95.dat", "q9_vesc_0.99.dat", "q9_vesc_1.0.dat"]

# Create the output files
for idx in range(len(v_esc)):
    # Create the model
    model = IsochroneModel(r = 1.0, b = 0.1, M = 1.0, v_esc = v_esc[idx])
    body = Body(model)

    # Create the timing settings
    time = Time(0, 1000 * PI, 0.1)        # t_0, t_max, dt

    # Create and run the integrator and analysis tool
    inter = Integrator(model, files[idx])
    inter.execute(time, body)
    analysis = Analysis(files[idx], True)

# Plot each of the orbits b)i.
plotter = Plotter(outputs=files, analysis=True)
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)b.i. Orbit Graph", files=files[:-1])
plotter.plot("time", ["radius"], ["grid"], "9)b.i. Radius vs Time Graph", files=files[:-1])
plotter.plot("time", ["radius"], ["grid", "logy"], "9)b.i. Log Radius vs Time Graph", files=files[:-1])

# Plot for Question b)ii.
plotter.plot("pos_x", ["pos_y"], ["grid", "star", "equal"], "9)b.ii. Orbit Graph for $v=v_\mathrm{esc}$", files=files[-1:])
plotter.plot("time", ["tot_E", "pot_E", "kin_E"], ["grid"], "9)b.ii. Energy vs Time Graph for $v=v_\mathrm{esc}$", files=files[-1:])
