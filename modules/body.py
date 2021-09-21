from .vector import Vector
from .state import State

# Stores all information related to a body
class Body:

    # State Vector
    state: State = State()

    # Default Constructor
    def __init__ (self, state: State = State()):
        self.state = state

    # Returns the string conversion
    def __str__ (self):
        return str(self.state)

    # Returns the output for file
    def output (self) -> str:
        return self.state.output()