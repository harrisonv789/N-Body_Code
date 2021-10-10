from numpy import float64, sqrt, arctan2
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
    r: float64 = 0.0

    # Theta
    theta: float64 = 0.0

    # Specific angular momentum
    L: Vector = Vector()

    # Mass of the Body (in Code Units)
    mass: float64 = 1.0

    # Specific energy
    E: float64 = 0.0

    # Kinetic energy
    KE: float64 = 0.0

    # Potential energy
    PE: float64 = 0.0

    # Error energy
    E_error: float64 = 0.0

    # Initial energy
    init_energy = None
    



    ##########################################################################
    # FUNCTIONS
    ##########################################################################

    # Default Constructor
    def __init__ (self, model: Model, state: State, mass: float64 = 1.0):
        self.model = model
        self.state = state
        self.mass = mass
        self.reset()

    # Resets the data
    def reset (self):
        self.init_energy = None
        self.update()
        self.init_energy = self.E

    # Updates properties
    def update (self):
        self.update_momentum()
        self.update_radius()
        self.update_theta()
        self.update_energy()
        if self.init_energy != None: self.update_energy_error()

    # Updates the momentum based on the calculation
    def update_momentum (self):
        self.L = self.position.cross(self.velocity)

    # Updates the radius
    def update_radius (self):
        r2 = self.position.dot(self.position)
        self.r = sqrt(r2)

    # Updates the theta
    def update_theta (self):
        self.theta = arctan2(self.position.y, self.position.x)

    # Updates the Energy based on the calculation
    def update_energy (self):
        self.KE = 0.5 * self.velocity.dot(self.velocity)
        self.PE = self.model.potential(self.position)
        self.E = self.KE + self.PE

    # Updaes the Energy error based on the energy
    def update_energy_error (self):
        self.E_error = abs((self.init_energy - self.E) / self.init_energy)

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
    def radius (self) -> float64:
        return self.r

    # Returns the momentum
    @property
    def momentum (self) -> Vector:
        return self.L

    # Returns the Total Energy
    @property
    def energy (self) -> float64:
        return self.E

    # Returns the Kinetic Energy
    @property
    def kinetic_energy (self) -> float64:
        return self.KE

    # Returns the Potential Energy
    @property
    def potential_energy (self) -> float64:
        return self.PE



    ##########################################################################
    # CONVERSION FUNCTIONS
    ##########################################################################

    # Returns the string conversion
    def __str__ (self):
        return str(self.state) + "\n" + ("Mass:         %s" % self.mass)

    # Returns the output for file
    def output (self) -> str:
        return "%s\t%8.4f\t%8.4f\t%s\t%8.4f\t%8.4f\t%8.4f\t%8.4f\t%8.4f" % \
        (self.state.output(), self.r, self.theta, self.L.output(), self.mass, self.E, self.KE, self.PE, self.E_error)

    # Defines the list of parameters
    PARAMETERS = ["time", "pos_x", "pos_y", "pos_z", "vel_x", "vel_y", "vel_z", \
        "acc_x", "acc_y", "acc_z", "radius", "theta", "mom_x", "mom_y", "mom_z", "mass", \
        "E_tot", "E_kin", "E_pot", "E_err"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "   "
        for p in Body.PARAMETERS:
            output += p + "    "
        return output[:-4] + "\n"