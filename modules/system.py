from .model import Model
from .body import Body

class System:

    # The number of bodies
    n_bodies: int = 0

    # A list of all bodies
    bodies = []

    # Creates a new system with a number of bodies
    # By default, it will create 1 body
    def __init__ (self, model: Model, n_bodies: int = 1):
        self.model = model
        self.n_bodies = n_bodies
        self.reset()



    # Function that sets up the system
    def reset (self):

        # Resets the list
        self.bodies = []

        # Create the bodies with the initial state
        for idx in range(self.n_bodies):
            state = self.model.init_state(1.0)
            b = Body(self.model, state)
            self.bodies.append(b)


    # TODO REMOVE
    # Rerturns the first body of the system
    @property
    def body (self):
        return self.bodies[0]