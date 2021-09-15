import numpy as np
from .vector import Vector
from .state import State

# Calculates the Acceleration from some Position input
def calculate_acceleration (x: Vector) -> Vector:

    # Compute the position value
    r2 = x.dot(x)
    r = np.sqrt(r2)
    r3 = float(r2 * r)

    a = Vector()

    # Calculate the acceleration
    a = x * (-1.0 / r3)

    # Return the acceleration
    return a


# Kepler's Equation for radius in an ellipse
def get_kepler_x (a: float, e: float, theta: float) -> float:
    # Return the equation
    return (a * (1 - e ** 2)) / (1 + e * np.cos(theta))

# Kepler's Equation for velocity in an ellipse
def get_kepler_v (a: float, e: float, theta: float) -> float:
    # Return the equation
    return np.sqrt(1.0 / a) * np.sqrt((1 + e) / (1 - e))