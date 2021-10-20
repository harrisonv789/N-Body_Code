from numpy import float64
from .constants import *
from .model import Model
from .body import Body
from .vector import Vector
from .state import State
from .initial_conditions import InitialConditions

# Stores information about a cluster of stars (such as a galaxy)
class Cluster:

    ##########################################################################
    # PARAMETERS
    ##########################################################################

    # Whether to use background model
    use_background: bool = False

    # The number of bodies
    n_bodies: int = 1

    # The masses of the bodies
    masses: list = []
    
    # A key for the Initial Conditions
    IC: str = ""

    # Initial radius
    radius: float = 1.0

    # Initial velocity vector
    vel_vec: Vector = Vector(0, 1.0, 0)

    # A list of all bodies
    bodies = []

    # The intial conditions function callback
    init_callback = None


    ##############################
    # Calculated Properties

    # The total mass of the cluster
    mass_total: float64 = 1.0

    # The angular momentum of the cluster
    L: Vector = Vector()

    # The total energy of the cluster
    E_tot: float64 = 0.0

    # The total initial energy of the cluster
    E_init = None

    # The kinetic energy of the cluster
    E_kin: float64 = 0.0

    # The potential energy of the cluster
    E_pot: float64 = 0.0

    # The energy error of the cluster
    E_err: float64 = 0.0


    ##########################################################################
    # CLUSTER FUNCTIONS
    ##########################################################################

    # Creates a new cluster with a number of bodies
    # By default, it will create 1 body
    def __init__ (self, model: Model, n_bodies: int = 1, **kwargs):
        self.model = model
        self.n_bodies = n_bodies
        self.__dict__.update(kwargs)
        self.reset()


    # Resets the cluster and sets up the bodies
    def reset (self):

        # If only one body, use a background model
        if self.n_bodies == 1: self.use_background = True

        # Resets the list of bodies
        self.bodies = []

        # Check for missing mass information and use ones
        if len(self.masses) < self.n_bodies:
            default = 1.0 if len(self.masses) == 0 else self.masses[0]
            for i in range(len(self.masses), self.n_bodies):
                self.masses.append(default)
        
        # Calculate the total cluster mass
        self.mass_total = sum(self.masses)

        # Set the mass of the modle
        self.model.M = self.mass_total

        # Loop through each of the bodies to create
        for idx in range(self.n_bodies):

            # Create the new body
            b = Body(self.model, State(), self.masses[idx])

            # Get the initial state of the body
            b.state = self.get_initial(idx, b)

            # Add the body to the list
            self.bodies.append(b)



    # Updates the properties of the cluster
    def update(self):
        self.get_cluster_L()
        self.get_cluster_PE()
        self.get_cluster_KE()
        self.get_cluster_energy()
        self.get_cluster_E_error()


    # Returns the output data for the file
    def output (self) -> str:
        return "%8.4f\t%s\t%8.4f\t%8.4f\t%8.4f\t%8.4f" % \
        (self.mass_total, self.L.output(), self.E_tot, self.E_kin, self.E_pot, self.E_err)

    # Defines the list of parameters
    PROPERTIES = ["time", "mass", "mom_x", "mom_y", "mom_z", "E_tot", "E_kin", "E_pot", "E_err"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "   "
        for p in Cluster.PROPERTIES:
            output += p + "    "
        return output[:-4] + "\n"

    

    ##########################################################################
    # MATHEMATICAL FUNCTIONS
    ##########################################################################

    # Calculates the current cluster total angular momentum
    def get_cluster_L (self) -> Vector:
        self.L = Vector()
        for body in self.bodies:
            self.L += body.L
        return self.L

    
    # Calculates the current cluster total kinetic energy
    def get_cluster_KE (self) -> float64:
        self.E_kin = 0.0
        for body in self.bodies:
            self.E_kin += body.KE
        return self.E_kin

    # Calculates the current cluster total potential energy
    def get_cluster_PE (self) -> float64:
        self.E_pot = 0.0
        for body in self.bodies:
            self.E_pot += body.PE * body.mass
        self.E_pot /= 2.0
        return self.E_pot


    # Calculates the current cluster total energy
    def get_cluster_energy (self) -> float64:
        self.E_tot = self.E_kin + self.E_pot
        if not self.E_init: self.E_init = self.E_tot
        return self.E_tot


    # Calculates the current cluster total energy error
    def get_cluster_E_error (self) -> float64:
        if self.E_init and self.E_init != 0.0: self.E_err = abs((self.E_init - self.E_tot) / self.E_init)
        return self.E_err




    ##########################################################################
    # INITIAL STATE FUNCTIONS
    ##########################################################################

    # Sets the intial values of the bodies
    def get_initial (self, idx: int, body: Body) -> State:

        # If a callback exists
        if self.init_callback:
            return self.init_callback(self, idx, body)

        # If using two body problem
        if self.IC in InitialConditions.IC_KEYS:
            IC = InitialConditions(self.IC.lower(), self.model, self.mass_total)
            return IC.get_state(idx, body)

        # If standard cluster
        return self.model.init_state(self.radius, self.vel_vec)
