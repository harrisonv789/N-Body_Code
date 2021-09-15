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
    def __init__ (self, x: Vector, v: Vector, a: Vector):
        self.x = x
        self.v = v
        self.a = a

    # Overrides the string function
    def __str__ (self):
        return "Position:     %s\nVelocity:     %s\nAcceleration: %s" % (self.x, self.v, self.a)

    # Checks if the state is valid
    def valid (self) -> bool:
        return self.x != None and self.v != None and self.a != None

    # Gets the output
    def output (self) -> str:
        return "%s\t%s\t%s" % (self.x.output(), self.v.output(), self.a.output())