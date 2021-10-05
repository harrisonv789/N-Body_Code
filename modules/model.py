import numpy as np
from .vector import Vector
from .state import State
from .constants import *



# Base mathematical model
class Model:

    # The mass of the central body
    M = 1.0


    ##########################################################################
    # Model Equations

    # Initialise the model
    def __init__ (self, model, **kwargs):
        self.model = model
        self.__dict__.update(kwargs)

    # Calculates the radius of a particle from some position
    def radius (self, position: Vector) -> np.float64:
        return position.magnitude

    # Calculates the potential of the system at some position
    def potential (self, position: Vector) -> np.float64:
        return 0.0

    # Calculates the acceleration of a particle at some position
    def acceleration (self, position: Vector) -> Vector:
        return Vector(0, 0, 0)


    ##########################################################################
    # Initial State and equations
    
    # Stores the initial state
    init_state = State()

    # Get the initial State of the system at some radius
    def init_state (self, radius: np.float64) -> State:
        # Get the initial vectors
        x = self.initial_position (radius)
        v = self.initial_velocity (x)
        a = self.acceleration (x)

        # Create the initial state
        return State(x, v, a)

    # Calculates the starting position at some radius
    def initial_position (self, radius: np.float64) -> Vector:
        return Vector()

    # Calculates the starting velocity from some position
    def initial_velocity (self, position: Vector) -> Vector:
        return Vector()

    ##########################################################################





# Kepler mathematical model
class KeplerModel (Model):

    # Semi-Major axis of the orbit
    a       = 1.0

    # Eccentricity of the orbits
    e       = 0.0

    # Angle of the orbits (TODO remove)
    theta   = 0.0


    ##########################################################################
    # Model Equations

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("kepler", **kwargs)

    # Calculates the potential of the system at some position
    def potential (self, position: Vector) -> np.float64:
        return -1.0 / self.radius(position)

    # Calculates the acceleration of a particle at some position
    def acceleration (self, position: Vector) -> Vector:

        # Compute the position value
        r3 = position.magnitude ** 3

        a = Vector()

        # Calculate the acceleration
        a = position * (-1.0 / r3)

        # Return the acceleration
        return a


    ##########################################################################
    # Initial State and equations

    # Calculates the starting position at some radius
    def initial_position (self, radius: np.float64) -> Vector:
        x = (self.a * (1 - self.e ** 2)) / (1 + self.e * np.cos(self.theta)) * radius 
        return Vector(x, 0, 0)

    # Calculates the starting velocity from some position
    def initial_velocity (self, position: Vector) -> Vector:
        y = np.sqrt(1.0 / self.a) * np.sqrt((1 + self.e) / (1 - self.e))
        return Vector(0, y, 0)

    ##########################################################################





# Isochrone mathematical model
class IsochroneModel (Model):

    # The scale of the potential
    b       = 0.1

    # The circular velocity multiplier
    v_mul   = None

    # Using an escape velocity multipler
    v_esc   = None


    ##########################################################################
    # Model Equations

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("isochrone", **kwargs)

    # Calculates the potential of the system at some position
    def potential (self, position: Vector) -> np.float64:
        return (-1. * G * self.M) / (self.b + np.sqrt(self.b ** 2 + self.radius(position) ** 2))

    # Calculates the acceleration of a particle at some position
    def acceleration (self, position: Vector) -> Vector:

        r = self.radius(position)
        c = np.sqrt(r ** 2 + self.b ** 2)
        a = position * ((-1. * G * self.M) / (c * ((self.b + c) ** 2)))

        # Return the acceleration
        return a

    # Calculate the escape velocity
    def escape_velocity (self, x: Vector) -> np.float32:
        r = x.magnitude
        phi = (G * self.M * -1.) / (self.b + np.sqrt(self.b ** 2 + r ** 2))
        return np.sqrt(2. * abs(phi))

    
    ##########################################################################
    # Initial State and equations

    # Calculates the starting position at some radius
    def initial_position (self, radius: np.float64) -> Vector:
        return Vector(radius, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, position: Vector) -> Vector:
        r = position.mag
        c = np.sqrt(r ** 2 + self.b ** 2)
        v = np.sqrt((G * self.M * r ** 2) / (c * ((self.b + c) ** 2)))
        vec = Vector(0, v, 0)

        # Return velocity based on input
        if self.v_esc != None:
            return vec.normalized * self.escape_velocity(position) * self.v_esc
        elif self.v_mul != None:
            return vec * self.v_mul
        else:
            return vec

    ##########################################################################





# Oscillator mathematical model
class OscillatorModel (Model):

    # The density of the oscillator
    rho     = 1.0

    # The orbit potential
    Omega   = None


    ##########################################################################
    # Model Equations

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("oscillator", **kwargs)

    # Calculates the potential of the system at some position
    def potential (self, position: Vector) -> np.float64:
        return -0.5 * (self.radius(position) ** 2) + (self.omega ** 2)

    # Calculates the acceleration of a particle at some position
    def acceleration (self, position: Vector) -> Vector:

        # Return the acceleration
        return position * -1. * (self.omega ** 2)

    # Calculates omega
    @property
    def omega (self) -> np.float64:
        if self.Omega == None:
            return np.sqrt(4.0 * PI * G * self.rho / 3.0)
        return self.Omega


    ##########################################################################
    # Initial State and equations
    
    # Calculates the starting position at some radius
    def initial_position (self, radius: np.float64) -> Vector:
        return Vector(radius, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, position: Vector) -> Vector:
        v = position.mag * self.omega
        return Vector(0, v, 0)

    ##########################################################################





# Logarithmic mathematical model
class LogarithmicModel (Model):

    # The scaling velocity
    v0      = 1.0

    # The core radius
    Rc      = 1.0

    # The flattening parameter, where q=1 gives a spherical potential
    q       = 1.0


    ##########################################################################
    # Model Equations

    # Initialise the model
    def __init__ (self, **kwargs):
        super().__init__("logarithmic", **kwargs)

    # Calculates the potential of the system at some position
    def potential (self, position: Vector) -> np.float64:
        return 0.5 * (self.v0 ** 2) * np.log(self.psi(position))

    # Calculates the acceleration of a particle at some position
    def acceleration (self, position: Vector) -> Vector:

        # Calculate the factor in front of the vector
        fac = -1.0 * (self.v0 ** 2) * self.psi(position)

        # Return the acceleration factor
        return Vector(position.x, position.y, position.z / (self.q ** 2)) * fac

    # Calculates the planar radius component
    def radius_plane (self, position: Vector) -> np.float64:
        return np.sqrt((position.x ** 2) + (position.y ** 2))

    # Calculates psi from the equation
    def psi (self, position: Vector) -> np.float64:
        return (self.radius_plane(position) ** 2) + (self.Rc ** 2) + ((position.z ** 2) / (self.q ** 2))


    ##########################################################################
    # Initial State and equations
    
    # Calculates the starting position at some radius
    def initial_position (self, radius: np.float64) -> Vector:
        return Vector(radius, 0, 0)

    # Calculates the starting velocity
    def initial_velocity (self, position: Vector) -> Vector:
        return Vector(0, self.v0, 0)

    ##########################################################################
