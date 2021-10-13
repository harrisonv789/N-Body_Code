from .model import Model
from .body import Body
from .state import State
from .vector import Vector
from numpy import float64

# Base Initial conditions class
class InitialConditions:

    # Intialises the conditions with required parameters
    def __init__ (self, key: str, model: Model, mass_total: float64):
        self.model = model
        self.mass_total = mass_total
        self.key = key

    
    # Returns a list of all valid initial conditions
    IC_KEYS = [
        "two_body",
        "figure_eight",
        "unstable_triple",
        "stable_triple"
    ]


    # Calls the initial conditions function
    # Takes in an index and the body object
    def get_state (self, index: int, body: Body) -> State:
        if self.key == "two_body": return self.two_body_IC(index, body)
        if self.key == "figure_eight": return self.figure_eight_IC(index, body)
        if self.key == "unstable_triple": return self.unstable_triple_IC(index, body)
        if self.key == "stable_triple": return self.stable_triple_IC(index, body)
        return State()


    # Two body initial conditions
    def two_body_IC (self, index: int, body: Body) -> State:
        state = self.model.init_state(1.0, Vector(0, 1, 0))
        state.x *= ((self.mass_total - body.mass) / self.mass_total)
        state.v *= ((self.mass_total - body.mass) / self.mass_total)

        # Move the first mass to the opposite
        if index == 0:
            state.x *= -1.0
            state.v *= -1.0

        return state


    # Figure-8 initial conditions
    def figure_eight_IC (self, index: int, body: Body) -> State:
        state = State()

        # Set custom positions and velocities
        px = -0.97000436
        py =  0.24308753
        vx = -0.466203685
        vy = -0.43236573
        
        # Update each of the particles
        if index == 0:
            state.x = Vector(px, py, 0.0)
            state.v = Vector(vx, vy, 0.0)
        elif index == 1:
            state.x = Vector(-px, -py, 0.0)
            state.v = Vector(vx, vy, 0.0)
        elif index == 2:   
            state.x = Vector(0.0, 0.0, 0.0)
            state.v = Vector(-2.0 * vx, -2.0 * vy, 0.0)

        return state


    # Unstable Triple
    def unstable_triple_IC (self, index: int, body: Body) -> State:
        state = State()

        # Set custom positions
        if index == 0:
            state.x = Vector(-1.1, 0.0, 0.0)
            state.v = Vector(0.0, -1.216, 0.0)
        elif index == 1:
            state.x = Vector(-0.1, 0.0, 0.0)
            state.v = Vector(0.0, 0.198, 0.0)
        elif index == 2:   
            state.x = Vector(1.2, 0.0, 0.0)
            state.v = Vector(0.0, 1.018, 0.0)

        return state

    
    # Stable Triple
    def stable_triple_IC (self, index: int, body: Body) -> State:
        state = State()

        # Set custom positions
        if index == 0:
            state.x = Vector(-1.7, 0.0, 0.0)
            state.v = Vector(0.0, -1.067, 0.0)
        elif index == 1:
            state.x = Vector(-0.7, 0.0, 0.0)
            state.v = Vector(0.0, 0.347, 0.0)
        elif index == 2:   
            state.x = Vector(2.4, 0.0, 0.0)
            state.v = Vector(0.0, 0.720, 0.0)

        return state
