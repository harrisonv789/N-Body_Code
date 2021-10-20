from .vector import Vector
from .state import State
from .body import Body
from .cluster import Cluster
from .constants import *
from numpy import float64
from math import sin, cos, sqrt

# Class for creating a galaxy
class Galaxy:

    # The number of bodies
    n_bodies: int = 1

    # The number of rings
    rings: int = 1

    # The number of bodies per ring
    ring_bodies = [0]

    # The radius of each ringe
    ring_radius = [1]

    # A list of masses
    masses: list = [1]

    # The total mass
    mass: float64 = 1

    # The inclination angle theta
    theta: float64 = 0.0


    # Constructor for galaxy class
    def __init__(self, n_bodies: int = 1, mass: float64 = 1.0, **kwargs):
        self.n_bodies = n_bodies
        self.masses = [mass]
        self.__dict__.update(kwargs)

        # Create the rest of the masses
        for idx in range(1, n_bodies): self.masses.append(0)

        # Constructs the rings
        self.construct_rings()



    # Constructs the rings in the galaxy
    def construct_rings (self):
        ring = 0
        for idx in range(1, self.n_bodies):
            self.ring_bodies[ring] += 1


    # Returns the velocity
    def v_phi (self, radius: float64) -> float64:
        return sqrt(G * self.mass / radius)


    # Callback function for returning the initial state of the bodies
    def init_callback (self, cluster: Cluster, index: int, body: Body) -> State:
        
        # If it is the first body in the cluster, set to base conditions
        if index == 0:
            return self.galaxy_state()
        
        else:
            ring = 0
            fraction = (index - 1) / self.ring_bodies[ring]
            phi = fraction * 2 * PI

            # Determine the position
            pos_x = cos(phi) * cos(self.theta)
            pos_y = sin(phi)
            pos_z = -1 * cos(phi) * sin(self.theta)
            position = Vector(pos_x, pos_y, pos_z) * self.ring_radius[ring]

            # Determine the velocity
            vel_x = -1 * sin(phi) * cos(self.theta)
            vel_y = cos(phi)
            vel_z = sin(phi) * sin(self.theta)
            velocity = Vector(vel_x, vel_y, vel_z) * self.v_phi(self.ring_radius[ring])

            # Create and return the state
            return State(position, velocity, Vector())


        return State()


    # Returns the galaxy state
    def galaxy_state (self) -> State:
        return State()