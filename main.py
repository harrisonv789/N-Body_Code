#!/usr/bin/env python3

# Import all needed packages
import numpy as np
import matplotlib.pyplot as plt
import modules.mathematics as math
import modules.integrator as integrator
from modules.time import Time
from modules.vector import Vector
from modules.state import State



##########################################################################
# PARAMETERS
##########################################################################

# Simulation parameters
dt = 0.0001             # The step size
tmax = 2.0 * np.pi      # The max time
output = "output.dat"   # The output filename

# Store the initial conditions
a = 1.0
e = 0.99
theta = 0



##########################################################################
# INITIAL CONDITIONS
##########################################################################

# Store the initial position, velociy and acceleration
x = Vector(math.get_kepler_x(a, e, theta),   0.0,                                0.0)
v = Vector(0.0,                              math.get_kepler_v(a, e, theta),     0.0)
a = math.calculate_acceleration(x)

# Create the initial state and time
state = State(x, v, a)
time = Time(0, tmax, dt)



##########################################################################
# INTEGRATOR
##########################################################################

inter = integrator.Integrator(time, output)
inter.execute(state)


##########################################################################
# DATA AND PLOTS
##########################################################################

data = np.genfromtxt(output, delimiter='\t', names=True)

# Plot the x-y plane
plt.plot(data["pos_x"], data["pos_y"], 'o', markersize=1)
plt.plot(0, 0, '*')
plt.axis('equal')
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Position Graph")
plt.show()

# Plot the x-vx plane
plt.plot(data["pos_x"], data["vel_x"], 'o', markersize=1)
plt.xlabel("X Position")
plt.ylabel("$v_x$ Velocity")
plt.title("X Position-Velocity Phase Graph")
plt.show()

# Plot the y-vy plane
plt.plot(data["pos_y"], data["vel_y"], 'o', markersize=1)
plt.xlabel("Y Position")
plt.ylabel("$v_y$ Velocity")
plt.title("Y Position-Velocity Phase Graph")
plt.show()