import numpy as np
import mathematics as math

# Takes in an Input position, Velocity, Accleration and Delta Time
def step_leapfrog(x: float, v: float, a: float, dt: float):
    # Set up the immediate velocity
    v += 0.5 * dt * a

    # Calculate the new parameters
    x += dt * v
    a = math.calculate_acceleration(x)
    v += 0.5 * dt * a

    # Return the values
    return x, v, a