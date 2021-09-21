import numpy as np
from .vector import Vector
from .state import State
from .constants import *



# Base mathematical model
class Model:

    # Stores the initial state
    init_state = State()

    # Initialise the model
    def __init__ (self, **kwargs):
        self.__dict__.update(kwargs)

        # Get the initial vectors
        x = self.initial_position ()
        v = self.initial_velocity (x)
        a = self.calc_acceleration (x)

        # Create the initial state
        self.init_state = State(x, v, a)
    
    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:
        return Vector()

    # Calculates the starting position
    def initial_position (self) -> Vector:
        return Vector()

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        return Vector()




# Kepler mathematical model
class KeplerModel (Model):

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)

    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:

        # Compute the position value
        r3 = position.magnitude ** 3

        a = Vector()

        # Calculate the acceleration
        a = position * (-1.0 / r3)

        # Return the acceleration
        return a

    # Calculates the starting position
    def initial_position (self) -> Vector:
        x = (self.a * (1 - self.e ** 2)) / (1 + self.e * np.cos(self.theta))
        return Vector(x, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        y = np.sqrt(1.0 / self.a) * np.sqrt((1 + self.e) / (1 - self.e))
        return Vector(0, y, 0)




# Kepler mathematical model
class IsochroneModel (Model):

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__(**kwargs)

    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:

        # Calculate r
        r = position.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        a = position * ((-1. * G * M) / (c * ((self.b + c) ** 2)))

        # Return the acceleration
        return a

    # Calculates the starting position
    def initial_position (self) -> Vector:
        return Vector(self.a, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        r = x.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        v = np.sqrt((G * M * r ** 2) / (c * ((self.b + c) ** 2)))
        vec = Vector(0, v, 0).normalized
        return vec * self.escape_velocity(x) * self.v_esc

    # Calculate the escape velocity
    def escape_velocity (self, x: Vector) -> np.float32:
        r = x.magnitude
        phi = (G * M * -1.) / (self.b + np.sqrt(self.b ** 2 + r ** 2))
        return np.sqrt(2. * abs(phi))