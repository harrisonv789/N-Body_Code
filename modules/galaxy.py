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
    ring_bodies = []

    # The radius of each ring
    ring_radius = []

    # A list of masses
    masses: list = [1]

    # The total mass
    mass: float64 = 1

    # The inclination angle theta
    theta: float64 = 0.0

    # The ring spacing
    ring_spacing: float64 = 1.0

    # Initial position
    galaxy_pos: Vector = Vector()

    # Initial velocity
    galaxy_vel: Vector = Vector()


    # Constructor for galaxy class
    def __init__(self, n_bodies: int = 1, mass: float64 = 1.0, **kwargs):
        self.n_bodies = n_bodies + 1
        self.masses = [mass]
        self.__dict__.update(kwargs)

        # Create the rest of the masses
        for idx in range(1, self.n_bodies): self.masses.append(0)

        # Constructs the rings
        self.construct_rings()



    # Constructs the rings in the galaxy
    def construct_rings (self):

        # Reset the variables
        self.ring_bodies = []
        self.ring_radius = []
        ring = 0
        ring_max = 0

        # Construct the first ring
        self.ring_radius.append(self.ring_spacing)
        self.ring_bodies.append(0)

        # Loop hrough all the bodies and check the max particles
        for idx in range(1, self.n_bodies):
            if idx > self.max_particles_per_ring(ring) + ring_max:
                ring_max += self.max_particles_per_ring(ring)
                ring += 1
                self.ring_radius.append(self.ring_spacing * (ring + 1))
                self.ring_bodies.append(0)
            self.ring_bodies[ring] += 1

        # Set the number of rings
        self.rings = ring + 1


    # The maximum particles per ring
    def max_particles_per_ring (self, ring: int) -> int:
        return 12 + (6 * ring)


    # Returns the velocity
    def v_phi (self, radius: float64) -> float64:
        return sqrt(G * self.mass / radius)


    # Callback function for returning the initial state of the bodies
    def init_callback (self, cluster: Cluster, index: int, body: Body) -> State:

        # If it is the first body in the cluster, set to base conditions
        if index == 0:
            state = State()
        
        else:
        
            # Determine the ring
            ring = 0
            prev_index = 1
            while index - prev_index >= self.ring_bodies[ring]:
                prev_index += self.ring_bodies[ring]
                ring += 1

            fraction = (index - prev_index) / self.ring_bodies[ring]
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
            state = State(position, velocity, Vector())

        return state + self.galaxy_state()


    # Returns the galaxy state
    def galaxy_state (self) -> State:
        return State(self.galaxy_pos, self.galaxy_vel, Vector())