#!/usr/bin/env python3

# Import all needed packages
import numpy as np
import matplotlib.pyplot as plt
import mathematics as math
import integrator

# Simulation parameters
dt = 0.0001             # The step size
time = 0                # The starting time
tmax = 4.0 * np.pi      # The max time
output = False          # Whether to output current values

# Store the initial conditions
a = 1.0
e = 0.99
theta = 0.0

# Store the initial position, velociy and acceleration
x = np.array([math.get_kepler_x(a, e, theta),   0.0,                                0.0])
v = np.array([0.0,                              math.get_kepler_v(a, e, theta),     0.0])
a = math.calculate_acceleration(x)

# Print the Initial Properties
print("Initial Position:     [%6.4f    %6.4f     %6.4f]" % (x[0], x[1], x[2]))
print("Initial Velocity:     [%6.4f    %6.4f     %6.4f]" % (v[0], v[1], v[2]))
print("Initial Acceleration: [%6.4f    %6.4f     %6.4f]" % (a[0], a[1], a[2]))

# Store the data
data = {"x": [[], [], []], "v": [[], [], []], "a": [[], [], []], "t": []}

# Loop while the time is less than maximum
while time < tmax:
    # Run the integrator
    x, v, a = integrator.step_leapfrog(x, v, a, dt)

    # Save the data
    data["x"][0].append(x[0])
    data["x"][1].append(x[1])
    data["x"][2].append(x[2])
    data["v"][0].append(v[0])
    data["v"][1].append(v[1])
    data["v"][2].append(v[2])
    data["a"][0].append(a[0])
    data["a"][1].append(a[1])
    data["a"][2].append(a[2])
    data["t"].append(time)

    if output:
        # Print the current output
        print("Position:     [%6.4f    %6.4f     %6.4f]" % (x[0], x[1], x[2]))
        print("Velocity:     [%6.4f    %6.4f     %6.4f]" % (v[0], v[1], v[2]))
        print("Acceleration: [%6.4f    %6.4f     %6.4f]" % (a[0], a[1], a[2]))

    # Increment the time
    time += dt

# Plot the x-y plane
plt.plot(data["x"][0], data["x"][1], 'o', markersize=1)
plt.plot(0, 0, '*')
plt.axis('equal')
plt.xlabel("X Position")
plt.ylabel("Y Position")
plt.title("Position Graph")
plt.show()

# Plot the x-vx plane
plt.plot(data["x"][0], data["v"][0], 'o', markersize=1)
plt.xlabel("X Position")
plt.ylabel("$v_x$ Velocity")
plt.title("X Position-Velocity Phase Graph")
plt.show()

# Plot the y-vy plane
plt.plot(data["x"][1], data["v"][1], 'o', markersize=1)
plt.xlabel("Y Position")
plt.ylabel("$v_y$ Velocity")
plt.title("Y Position-Velocity Phase Graph")
plt.show()