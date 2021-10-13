from numpy import float64
from .constants import *
from .model import Model
from .body import Body
from .vector import Vector
from .state import State

class System:

    # Whether to use a sink particle
    use_background: bool = True

    # The number of bodies
    n_bodies: int = 1

    # The masses of the bodies
    masses: list = [1]

    # Initial radius
    radius: float = 1.0

    # Initial velocity vector
    vel_vec: Vector = Vector(0, 1.0, 0)

    # A list of all bodies
    bodies = []

    # Creates a new system with a number of bodies
    # By default, it will create 1 body
    def __init__ (self, model: Model, n_bodies: int = 1, **kwargs):
        self.model = model
        self.n_bodies = n_bodies
        self.__dict__.update(kwargs)

        self.reset()



    # Function that sets up the system
    def reset (self):

        # Resets the list
        self.bodies = []

        # Check for missing mass information and use ones
        if len(self.masses) < self.n_bodies:
            for i in range(len(self.masses), self.n_bodies):
                self.masses.append(1.0)
        
        # Total system mass
        self.mass = sum(self.masses)

        # Set the mass of the system
        self.model.M = self.mass

        # Create the bodies with the initial state
        for idx in range(self.n_bodies):
            state = self.get_initial(idx)

            # Create the new body
            b = Body(self.model, state, self.masses[idx])

            # Add the body to the list
            self.bodies.append(b)


        # Set the starting properties of the bodies
        for idx in range(self.n_bodies):
            # Update the potential and reset the body
            self.bodies[idx].PE = self.get_potential(idx)
            self.bodies[idx].reset()

    

    # Calculates the acceleration vector of some body
    def get_acceleration (self, body_idx: int) -> Vector:
        # Get the body and base acceleration
        body: Body = self.bodies[body_idx]
        a: Vector = self.model.acceleration(body.state.x) if self.use_background else Vector()
        
        # Calculate the effects of all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx:
                distance: Vector = body.state.x - self.bodies[idx].state.x
                a_fac = (-1.0 * G * self.bodies[idx].mass) / (distance.mag ** 3)
                a += a_fac * distance

        # Return the acceleration
        return a

    
    # Calculates the potential of some body
    def get_potential (self, body_idx: int) -> float64:
        body = self.bodies[body_idx]

        # Get the background potential
        pot = self.model.potential(body.position) if self.use_background else 0.0

        # Loop through all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx:
                # Add the potential to the data
                mass = -1.0 * G * body.mass * self.bodies[idx].mass
                pot += mass / (body.position - self.bodies[idx].position).mag

        # Return the potential over the mass
        return pot / body.mass


    # Sets the intial values of the bodies
    def get_initial (self, idx: int) -> State:
        # If using two body problem
        if self.n_bodies == 2:
            return self.two_body_initial(idx)
        
        # If standard system
        return self.model.init_state(self.radius, self.vel_vec)



    # Two-body problem
    def two_body_initial (self, idx: int) -> State:
        state = self.model.init_state(self.radius, self.vel_vec)
        state.x *= ((self.mass - self.masses[idx]) / self.mass)
        state.v *= ((self.mass - self.masses[idx]) / self.mass)

        # Move the first mass opposite
        if idx == 0:
            state.x *= -1.0
            state.v *= -1.0

        return state
