import numpy as np
from .vector import Vector
from .state import State

# Stores all information related to a body
class Body:

    ##########################################################################
    # PARAMETERS
    ##########################################################################

    # State Vectors
    state: State = State()

    # Mass of the Body (in Code Units)
    mass: np.float64 = 1.0

    # Specific angular momentum
    L: Vector = Vector()

    # Specific energy
    E: np.float64 = 0.0



    ##########################################################################
    # FUNCTIONS
    ##########################################################################

    # Default Constructor
    def __init__ (self, state: State = State(), mass: np.float64 = 1.0):
        self.state = state
        self.mass = mass

    # Updates properties
    def update (self):
        self.update_momentum()

    # Updates the momentum based on the calculation
    def update_momentum (self):
        self.L = self.position.cross(self.velocity)


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

    # Returns the momentum
    @property
    def momentum (self) -> Vector:
        return self.L

    # Returns the Energy
    @property
    def energy (self) -> np.float64:
        return self.E



    ##########################################################################
    # CONVERSION FUNCTIONS
    ##########################################################################

    # Returns the string conversion
    def __str__ (self):
        return str(self.state) + "\n" + ("Mass:         %s" % self.mass)

    # Returns the output for file
    def output (self) -> str:
        return "%s\t%8.4f\t%s%8.4f\t" % (self.state.output(), self.mass, self.L.output(), self.E)

    # Defines the list of parameters
    PARAMETERS = ["time", "pos_x", "pos_y", "pos_z", "vel_x", "vel_y", "vel_z", \
        "acc_x", "acc_y", "acc_z", "mass", "mom_x", "mom_y", "mom_z", "energy"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "    "
        for p in Body.PARAMETERS:
            output += p + "    "
        return output[:-4] + "\n"