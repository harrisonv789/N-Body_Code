#!/usr/bin/env python3

# Import relevant packages
import matplotlib.pyplot as plt
import numpy as np


##########################################################################
# CONSTANTS
##########################################################################

M_d = 1e11      # Mass of disk in Solar masses
R_d = 5.0       # Radius of disk in kiloparsecs
G = 6.674e-11   # Gravitational constants 
PI = 3.141596
rho_0 = 2e-25     # Rho in grams per cm^-3
a = 1.0



##########################################################################
# CONVERSIONS
##########################################################################

# Returns the mass in kg from solar masses
def Msol_to_Mkg (M_sol):
    return M_sol * 1.989e30 

# Returns the distance in kpc from meters
def kpc_to_m (kpc):
    return kpc * 3.086e19

# Returns the density in kg / m^3 from g / cm^3
def gcm_to_kgm (gcm):
    return (gcm / 1000) * (100 ** 3)


##########################################################################
# PHYSICAL FUNCTIONS
########################################################################## 

# Calcaulates the total potential
def phi_tot (phi_d, phi_halo):
    return phi_d + phi_halo

# Returns the density function
def rho (R):
    _rho = gcm_to_kgm(rho_0)
    R = kpc_to_m(R)

    b = (R / a) * ((1 + (R / a)) ** 2)
    return _rho / b

# Returns the NFW velocity
def V_NFW ():
    _rho = gcm_to_kgm(rho_0)

    return np.sqrt(G * _rho * a ** 2)

# Calculate the velocity
def v_halo (R):
    R = kpc_to_m(R)

    fac = 4 * PI * (V_NFW() ** 2)
    fac2 = (a / R) * np.log(1 + (R / a)) - (1 / (1 + (R / a)))
    return np.sqrt(fac * fac2)

# Function for the velocity of the disk at some radius
def v_disk (R):
    # Convert units
    R = kpc_to_m(R)
    _R_d = kpc_to_m(R_d)
    _M_d = Msol_to_Mkg(M_d)

    # Calculate quantities
    fac1 = 0.767 * (G * _M_d / _R_d)
    fac2 = 0.44 * ((R / _R_d) ** 1.3)
    fac3 = 1 + 0.235 * ((R / _R_d) ** 2.3)
    squared = fac1 * (fac2 / fac3)

    # Return result
    return np.sqrt(squared)

# Return the velocity total function
def v_tot (R):
    return np.sqrt(v_disk(R) ** 2 + v_halo(R) ** 2)


##########################################################################
# GRAPHING
##########################################################################
 
# Function to plot values
def plot_a_values (axis, a_vals):
    global a
    # Plot each of the options for a
    for _a in a_vals:
        a = kpc_to_m(_a)

        # Create a plot of radius from 0 to 4 disk radius
        R = np.linspace(0.01, 4.0 * R_d, 1000)
        v = v_tot(R) / 1000.0

        # Create the plot
        axis.plot(R, v, label="$a = %.0f$ kpc" % _a)

    # Add in all the axis variables and the titles
    axis.set_xlabel("radius [kpc]")
    axis.set_ylabel("$v_\mathrm{circ}$ [km/s]")
    axis.set_title("Rotation curve for a Galaxy")
    axis.legend()
    axis.grid()

    # Plot the rotation line
    axis.plot([0, 4 * R_d], [220, 220], "--", color="black")


# Create the subplots for the first estimates
fig, ax = plt.subplots()
plot_a_values(ax, [10, 20, 30, 40, 50])
plt.show()

# Create the subplots for the more accurate estimates
fig, ax = plt.subplots()
plot_a_values(ax, [28, 29, 30, 31, 32])
ax.set_ylim(210, 240)
plt.show()