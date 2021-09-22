import numpy as np
from .vector import Vector
from .state import State
from .model import *

# Stores all information related to a body
class Body:

    ##########################################################################
    # PARAMETERS
    ##########################################################################

    # State Vectors
    state: State = State()

    # Radius
    r: np.float64 = 0.0

    # Specific angular momentum
    L: Vector = Vector()

    # Mass of the Body (in Code Units)
    mass: np.float64 = 1.0

    # Specific energy
    E: np.float64 = 0.0

    # Kinetic energy
    KE: np.float64 = 0.0

    # Potential energy
    PE: np.float64 = 0.0
    



    ##########################################################################
    # FUNCTIONS
    ##########################################################################

    # Default Constructor
    def __init__ (self, model: Model, mass: np.float64 = 1.0):
        self.model = model
        self.state = model.init_state
        self.mass = mass

    # Updates properties
    def update (self):
        self.update_momentum()
        self.update_radius()
        self.update_energy()

    # Updates the momentum based on the calculation
    def update_momentum (self):
        self.L = self.position.cross(self.velocity)

    # Updates the radius
    def update_radius (self):
        r2 = self.position.dot(self.position)
        self.r = np.sqrt(r2)

    # Updates the Energy based on the calculation
    def update_energy (self):
        self.KE = 0.5 * self.velocity.dot(self.velocity)
        self.PE = self.model.calc_potential(self.r)
        self.E = self.KE + self.PE


    ##########################################################################
    # PROPERTY FUNCTIONS
    ##########################################################################

    # Returns the position
    @property
    def position (self) -> Vector:
        return self.state.x

    # Returns the velocity
    @property
    def velocity (self) -> Vector:
        return self.state.v

    # Returns the acceleration
    @property
    def acceleration (self) -> Vector:
        return self.state.a

    # Returns the Radius
    @property
    def radius (self) -> np.float64:
        return self.r

    # Returns the momentum
    @property
    def momentum (self) -> Vector:
        return self.L

    # Returns the Total Energy
    @property
    def energy (self) -> np.float64:
        return self.E

    # Returns the Kinetic Energy
    @property
    def kinetic_energy (self) -> np.float64:
        return self.KE

    # Returns the Potential Energy
    @property
    def potential_energy (self) -> np.float64:
        return self.PE



    ##########################################################################
    # CONVERSION FUNCTIONS
    ##########################################################################

    # Returns the string conversion
    def __str__ (self):
        return str(self.state) + "\n" + ("Mass:         %s" % self.mass)

    # Returns the output for file
    def output (self) -> str:
        return "%s\t%8.4f\t%s\t%8.4f\t%8.4f\t%8.4f\t%8.4f" % \
        (self.state.output(), self.r, self.L.output(), self.mass, self.E, self.KE, self.PE)

    # Defines the list of parameters
    PARAMETERS = ["time", "pos_x", "pos_y", "pos_z", "vel_x", "vel_y", "vel_z", \
        "acc_x", "acc_y", "acc_z", "radius", "mom_x", "mom_y", "mom_z", "mass", "tot_E", "kin_E", "pot_E"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "   "
        for p in Body.PARAMETERS:
            output += p + "     "
        return output[:-4] + "\n"