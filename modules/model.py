import numpy as np
from .vector import Vector
from .state import State
from .constants import *



# Base mathematical model
class Model:

    # Stores the initial state
    init_state = State()

    # Initialise the model
    def __init__ (self, model, **kwargs):
        self.model = model
        self.__dict__.update(kwargs)

    # Get the initial State of the system
    @property
    def init_state (self) -> State:
        # Get the initial vectors
        x = self.initial_position ()
        v = self.initial_velocity (x)
        a = self.calc_acceleration (x)

        # Create the initial state
        return State(x, v, a)
    
    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:
        return Vector()

    # Calculates the potential from the radius
    def calc_potential (self, radius: np.float64) -> np.float64:
        return 0.0

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
        super().__init__("kepler", **kwargs)

    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:

        # Compute the position value
        r3 = position.magnitude ** 3

        a = Vector()

        # Calculate the acceleration
        a = position * (-1.0 / r3)

        # Return the acceleration
        return a

    # Calculates the potential from the radius
    def calc_potential (self, radius: np.float64) -> np.float64:
        return -1.0 / radius

    # Calculates the starting position
    def initial_position (self) -> Vector:
        x = (self.a * (1 - self.e ** 2)) / (1 + self.e * np.cos(self.theta))
        return Vector(x, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        y = np.sqrt(1.0 / self.a) * np.sqrt((1 + self.e) / (1 - self.e))
        return Vector(0, y, 0)




# Isochrone mathematical model
class IsochroneModel (Model):

    # Default parameters
    v_mul = None    # The circular velocity multiplier
    v_esc = None    # Using an escape velocity multipler

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("isochrone", **kwargs)

    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:

        # Calculate r
        r = position.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        a = position * ((-1. * G * self.M) / (c * ((self.b + c) ** 2)))

        # Return the acceleration
        return a

    # Calculates the potential from the radius
    def calc_potential (self, radius: np.float64) -> np.float64:
        return (-1. * G * self.M) / (self.b + np.sqrt(self.b ** 2 + radius ** 2))

    # Calculates the starting position
    def initial_position (self) -> Vector:
        return Vector(self.r, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        r = x.magnitude
        c = np.sqrt(r ** 2 + self.b ** 2)
        v = np.sqrt((G * self.M * r ** 2) / (c * ((self.b + c) ** 2)))
        vec = Vector(0, v, 0)

        # Return velocity based on input
        if self.v_esc != None:
            return vec.normalized * self.escape_velocity(x) * self.v_esc
        elif self.v_mul != None:
            return vec * self.v_mul
        else:
            return vec

    # Calculate the escape velocity
    def escape_velocity (self, x: Vector) -> np.float32:
        r = x.magnitude
        phi = (G * self.M * -1.) / (self.b + np.sqrt(self.b ** 2 + r ** 2))
        return np.sqrt(2. * abs(phi))




# Oscillator mathematical model
class OscillatorModel (Model):

    # Default parameters
    Omega = None

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("oscillator", **kwargs)

    # Calculates omega
    @property
    def omega (self) -> np.float64:
        if self.Omega == None:
            return np.sqrt(4.0 * PI * G * self.rho / 3.0)
        return self.Omega
        

    # Calculates the acceleration from some position
    def calc_acceleration (self, position: Vector) -> Vector:

        # Return the acceleration
        return position * -1. * (self.omega ** 2)

    # Calculates the potential from the radius
    def calc_potential (self, radius: np.float64) -> np.float64:
        return -0.5 * (radius ** 2) + (self.omega ** 2)

    # Calculates the starting position
    def initial_position (self) -> Vector:
        return Vector(self.r, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, x: Vector) -> Vector:
        v = self.r * self.omega
        return Vector(0, v, 0)