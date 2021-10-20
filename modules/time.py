# Use numpy for storing the floats as doubles
from numpy import float64
from datetime import datetime

# Class with some time properties
class Time:
    
    # Stores the current time
    time: float64 = 0

    # Stores the timestep interval
    delta: float64 = 0.01

    # Stores the starting time
    start: float64 = 0

    # Stores the final time
    end: float64 = 1.0

    # The number of total steps
    steps_max: int = 0

    # The number of current steps
    steps: int = 0

    # Realtime duration when the time was reset
    timestamp: datetime

    # Initialiser constructor
    def __init__ (self, start_time: float64 = 0.0, end_time: float64 = 1.0, delta_time: float64 = 0.01):
        self.start = start_time
        self.end = end_time
        self.delta = delta_time
        self.reset()

    ##########################################################################



    ##########################################################################
    # CLOCK FUNCTIONS
    ##########################################################################

    # Resets the clock back to the start time
    def reset (self):
        self.time = self.start
        self.steps = 0
        self.steps_max = int((self.end - self.start) / self.delta)
        self.timestamp = datetime.now()

    # Increments the time by the delta time
    def increment (self):
        self.time += self.delta
        self.steps += 1

    # Increases the time by a certain amount of steps (+=)
    def __iadd__ (self, other: int):
        self.time += self.delta * int(other)
        self.steps += int(other)
        return self

    # Returns the progress as a fraction from 0 to 1
    @property
    def progress (self) -> float64:
        prog = (self.time - self.start) / (self.end - self.start)
        return prog if prog < 1.0 else 1.0

    # Function that returns whether or not the time is running
    @property
    def running (self) -> bool:
        return self.time <= self.end

    # Duration in seconds
    @property
    def duration (self) -> float:
        return (datetime.now() - self.timestamp).total_seconds()

    ##########################################################################



    ##########################################################################
    # EQUALITY FUNCTIONS
    ##########################################################################

    # Equality operator
    def __eq__(self, other: object) -> bool:
        return self.time == other.time

    # Inequality operator
    def __ne__(self, other: object) -> bool:
        return self.time != other.time

    # Greater than operator
    def __gt__(self, other: object) -> bool:
        return self.time > other.time
    
    # Greater than or equal to operator
    def __ge__(self, other: object) -> bool:
        return self.time >= other.time

    # Less than operator
    def __lt__(self, other: object) -> bool:
        return self.time < other.time
    
    # Less than or equal to operator
    def __le__(self, other: object) -> bool:
        return self.time <= other.time

    ##########################################################################



    ##########################################################################
    # CONVERSION FUNCTIONS
    ##########################################################################

    # Returns the value of the time
    def __call__ (self) -> float64:
        return self.time

    # Returns the float value of the time
    def __float__ (self) -> float:
        return self.time

    # Returns the string form
    def __str__ (self) -> str:
        return "Time: %8.4f,  Start: %8.4f,  End: %8.4f,  Delta: %8.4f" % (self.time, self.start, self.end, self.delta)

    ##########################################################################