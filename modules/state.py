# Import the vector type
from .vector import Vector

# Stores a state vector of a particle (position, velocity, acceleration)
class State:

    # Position Vector
    x: Vector = Vector()

    # Velocity vector
    v: Vector = Vector()

    # Acceleration vector
    a: Vector = Vector()

    # Default constructor
    def __init__ (self, x: Vector = Vector(), v: Vector = Vector(), a: Vector = Vector()):
        self.x = x
        self.v = v
        self.a = a

    # Adds two states together
    def __add__ (self, other):
        state = State(self.x + other.x, self.v + other.v, self.a + other.a)
        return state

    # Subtracts two states together
    def __sub__ (self, other):
        state = State(self.x - other.x, self.v - other.v, self.a - other.a)
        return state

    # Returns the position
    @property
    def position (self) -> Vector:
        return self.x

    # Returns the velocity
    @property
    def velocity (self) -> Vector:
        return self.v

    # Returns the acceleration
    @property
    def acceleration (self) -> Vector:
        return self.a

    # Checks if the state is valid
    def valid (self) -> bool:
        return self.x != None and self.v != None and self.a != None

    # Overrides the string function
    def __str__ (self):
        return "Position:     %s\nVelocity:     %s\nAcceleration: %s" % (self.x, self.v, self.a)

    # Get's the output
    def output (self) -> str:
        return "%s\t%s\t%s" % (self.x.output(), self.v.output(), self.a.output())