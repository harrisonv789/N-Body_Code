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



    ##########################################################################
    # FUNCTIONS
    ##########################################################################

    # Default Constructor
    def __init__ (self, state: State = State(), mass: np.float64 = 1.0):
        self.state = state
        self.mass = mass

    # Returns the string conversion
    def __str__ (self):
        return str(self.state) + "\n" + ("Mass:         %s" % self.mass)

    # Returns the output for file
    def output (self) -> str:
        return self.state.output() + ("\t%8.4f" % self.mass)

    # Defines the list of parameters
    PARAMETERS = ["time", "pos_x", "pos_y", "pos_z", "vel_x", "vel_y", "vel_z", \
        "acc_x", "acc_y", "acc_z", "mass"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "   "
        for p in Body.PARAMETERS:
            output += p + "     "
        return output[:-4] + "\n"