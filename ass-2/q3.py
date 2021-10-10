#!/usr/bin/env python3

# Import relevant packages
import matplotlib.pyplot as plt
import numpy as np

# Constants
M_d = 1e11      # Mass of disk in Solar masses
R_d = 5.0       # Radius of disk in kiloparsecs
G = 6.674e-11   # Gravitational constants 

# Returns the mass in kg from solar masses
def Msol_to_Mkg (M_sol):
    return M_sol * 1.989e30 

# Returns the distance in kpc from meters
def kpc_to_m (kpc):
    return kpc * 3.086e19
    

# Function for the velocity of the disk at some radius
def v_circ (R):
    # Convert units
    R = kpc_to_m(R)
    _R_d = kpc_to_m(R_d)
    _M_d = Msol_to_Mkg(M_d)

    # Calculate quantities
    a = 0.767 * (G * _M_d / _R_d)
    b = 0.44 * ((R / _R_d) ** 1.3)
    c = 1 + 0.235 * ((R / _R_d) ** 2.3)
    squared = a * (b / c)

    # Return result
    return np.sqrt(squared)

# Create a plot of radius from 0 to 4 disk radius
R = np.linspace(0, 4.0 * R_d, 1000)
v = v_circ(R) / 1000.0

# Create the plot
fig, ax = plt.subplots()
ax.plot(R, v)
ax.set_xlabel("radius [kpc]")
ax.set_ylabel("$v_\mathrm{circ}$ [km/s]")
ax.set_title("Rotation curve for a Galaxy")
ax.grid()
plt.show()