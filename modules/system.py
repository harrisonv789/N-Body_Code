from numpy import float64
from .cluster import Cluster
from .constants import *
from .model import Model
from .body import Body
from .vector import Vector
from .state import State
from .initial_conditions import InitialConditions

# Stores information related to the system
class System:

    ##########################################################################
    # PARAMETERS
    ##########################################################################

    # The number of clusters
    n_clusters: int = 1
    
    # A list of the clusters
    clusters: list = [] 

    # The number of bodies
    n_bodies: int = 1

    # A list of all bodies
    bodies: list = []


    ##############################
    # Calculated Properties

    # The total mass of the system
    mass_total: float64 = 1.0

    # The angular momentum of the system
    L: Vector = Vector()

    # The total energy of the system
    E_tot: float64 = 0.0

    # The total initial energy of the system
    E_init = None

    # The kinetic energy of the system
    E_kin: float64 = 0.0

    # The potential energy of the system
    E_pot: float64 = 0.0

    # The energy error of the system
    E_err: float64 = 0.0


    ##########################################################################
    # SYSTEM FUNCTIONS
    ##########################################################################

    # Creates a new system with a number of bodies
    def __init__ (self, clusters: list, **kwargs):
        self.clusters = clusters if type(clusters) is list and len(clusters) != 1 else [clusters]
        self.__dict__.update(kwargs)
        self.reset()


    # Resets the system and sets up the bodies
    def reset (self):

        # Resets the clusters
        for cluster in self.clusters: cluster.reset()

        # Calculate the total mass
        self.mass_total = sum([cluster.mass_total for cluster in self.clusters])

        # Resets the bodies
        self.bodies = []

        # Gets all the bodies
        for cluster in self.clusters: self.bodies.extend(cluster.bodies)

        # Gets the number of bodies
        self.n_bodies = len(self.bodies)

        # Sets the starting properties of the bodies
        for idx in range(self.n_bodies):
            # Update the potential and reset the body
            self.bodies[idx].PE = self.get_potential(idx)
            self.bodies[idx].reset()


    # Updates the properties of the system
    def update(self):
        for cluster in self.clusters: cluster.update()
        self.get_system_L()
        self.get_system_PE()
        self.get_system_KE()
        self.get_system_energy()
        self.get_system_E_error()


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
        for p in System.PROPERTIES:
            output += p + "    "
        return output[:-4] + "\n"

    

    ##########################################################################
    # MATHEMATICAL FUNCTIONS
    ##########################################################################

    # Calculates the acceleration vector of some body
    def get_acceleration (self, body_idx: int) -> Vector:

        # Get the body and background acceleration
        body: Body = self.bodies[body_idx]
        a: Vector = Vector()

        # Add in elements from the cluster's background
        for cluster in self.clusters:
            if cluster.use_background:
                a += cluster.model.acceleration(body.state.x)
              
        # Calculate the effects of all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx and self.bodies[idx].has_mass:
                distance: Vector = body.state.x - self.bodies[idx].state.x
                mag = distance.mag
                a_fac = (-1.0 * G * self.bodies[idx].mass) / (mag ** 3) if mag > 0 else 0.0
                a += a_fac * distance

        # Return the acceleration
        return a

    
    # Calculates the potential of some body
    def get_potential (self, body_idx: int) -> float64:

        # Get the body and background potential
        body = self.bodies[body_idx]
        pot = 0.0

        # Add in elements from the cluster's potential
        for cluster in self.clusters:
            if cluster.use_background:
                pot += cluster.model.potential(body.position)

        # Loop through all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx and self.bodies[idx].has_mass:
                # Add the potential to the data
                mass = -1.0 * G * body.mass * self.bodies[idx].mass
                mag = (body.position - self.bodies[idx].position).mag
                pot += mass / mag if mag > 0 else 0.0

        # Return the potential over the mass
        return pot / body.mass if body.mass > 0 else 0.0

    
    # Calculates the current system total angular momentum
    def get_system_L (self) -> Vector:
        self.E_pot = sum([cluster.L for cluster in self.clusters])
        return self.E_pot
    
    # Calculates the current system total kinetic energy
    def get_system_KE (self) -> float64:
        self.E_kin = sum([cluster.E_kin for cluster in self.clusters])
        return self.E_kin

    # Calculates the current system total potential energy
    def get_system_PE (self) -> float64:
        self.E_pot = sum([cluster.E_pot for cluster in self.clusters])
        return self.E_pot

    # Calculates the current system total energy
    def get_system_energy (self) -> float64:
        self.E_tot = self.E_kin + self.E_pot
        if not self.E_init: self.E_init = self.E_tot
        return self.E_tot

    # Calculates the current system total energy error
    def get_system_E_error (self) -> float64:
        if self.E_init and self.E_init != 0.0: self.E_err = abs((self.E_init - self.E_tot) / self.E_init)
        return self.E_err