# Class with some time properties
class Time:
    
    # Stores the current time
    time: float = 0

    # Stores the timestep interval
    delta: float = 0.01

    # Stores the starting time
    start: float = 0

    # Stores the final time
    end: float = 1

    # Initialiser constructor
    def __init__ (self, start_time: float = 0.0, end_time: float = 1.0, delta_time: float = 0.01):
        self.start = start_time
        self.end = end_time
        self.delta = delta_time
        self.reset()

    # Function that resets the time
    def reset (self):
        self.time = self.start

    # Function that increments the time
    def increment (self):
        self.time += self.delta

    # Function that returns whether or not the time is at the end
    def valid (self):
        return self.time < self.end

    # Returns the value of the time
    def __call__ (self):
        return self.time

    # Returns the float value of the time
    def __float__ (self):
        return self.time

    # Returns the string form
    def __str__ (self):
        return "Time: %8.4f, Start: %8.4f, End: %8.4f, Delta: %8.4f" % (self.time, self.start, self.end, self.delta)