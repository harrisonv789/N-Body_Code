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

    # The number of total steps
    steps_max: 0

    # The number of current steps
    steps: int = 0

    # Initialiser constructor
    def __init__ (self, start_time: float = 0.0, end_time: float = 1.0, delta_time: float = 0.01):
        self.start = start_time
        self.end = end_time
        self.delta = delta_time
        self.reset()

    # Function that resets the time
    def reset (self):
        self.time = self.start
        self.steps = 0
        self.steps_max = int((self.end - self.start) / self.delta)

    # Function that increments the time
    def increment (self):
        self.time += self.delta
        self.steps += 1

    # Returns the progress as a fraction from 0 to 1
    @property
    def progress (self):
        return (self.time - self.start) / (self.end - self.start)

    # Function that returns whether or not the time is running
    @property
    def running (self):
        return self.time < self.end

    # Returns the value of the time
    def __call__ (self):
        return self.time

    # Returns the float value of the time
    def __float__ (self):
        return self.time

    # Returns the string form
    def __str__ (self):
        return "Time: %8.4f,  Start: %8.4f,  End: %8.4f,  Delta: %8.4f" % (self.time, self.start, self.end, self.delta)