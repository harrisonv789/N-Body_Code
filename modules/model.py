import numpy as np
from .vector import Vector
from .state import State
from .constants import *



# Base mathematical model
class Model:

    # Initialise the model
    def __init__ (self):
        pass
    
    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:
        return Vector()

    # Calculates the starting position
    def initial_position (self, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        return Vector()

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        return Vector()




# Kepler mathematical model
class KeplerModel (Model):

    # Initialise the model
    def __init__(self):
        super().__init__()

    # Calculates the acceleration from some position
    def calc_acceleration(self, position: Vector) -> Vector:

        # Compute the position value
        r3 = position.magnitude ** 3

        a = Vector()

        # Calculate the acceleration
        a = position * (-1.0 / r3)

        # Return the acceleration
        return a

    # Calculates the starting position
    def initial_position(self, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        x = (a * (1 - e ** 2)) / (1 + e * np.cos(theta))
        return Vector(x, 0, 0)

    # Calculates the starting velocity
    def initial_velocity(self, x: Vector, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        y = np.sqrt(1.0 / a) * np.sqrt((1 + e) / (1 - e))
        return Vector(0, y, 0)




# Kepler mathematical model
class IsochroneModel (Model):

    # Initialise the model
    def __init__(self, b = 1.0):
        self.b = b
        super().__init__()

    # Calculates the acceleration from some position
    def calc_acceleration(self, position: Vector) -> Vector:

        # Calculate r
        r = position.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        a = position * ((-1. * G * M) / (c * ((self.b + c) ** 2)))

        # Return the acceleration
        return a

    # Calculates the starting position
    def initial_position(self, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        x = a
        return Vector(x, 0, 0)

    # Calculates the starting velocity
    def initial_velocity(self, x: Vector, a: np.float32, e: np.float32, theta: np.float32) -> Vector:
        r = x.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        v = np.sqrt((G * M * r ** 2) / (c * ((self.b + c) ** 2)))
        return Vector(0, v, 0)