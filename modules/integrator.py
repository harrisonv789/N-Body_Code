import numpy as np
from . import mathematics as math
from .time import Time
from .state import State

# Takes in an Input position, Velocity, Accleration and Delta Time
def step_leapfrog(state: State, dt: float):

    # Set up the immediate velocity
    state.v += 0.5 * dt * state.a


    # Calculate the new parameters
    state.x += dt * state.v
    state.a = math.calculate_acceleration(state.x)
    state.v += 0.5 * dt * state.a

    # Return the values
    return state



# Runs the integration
class Integrator:

    # Initialise the integrator with some timestep
    def __init__ (self, time: Time, output: bool = False):
        self.time = time
        self.output = output

    # Call the integrator with a starting position, velocity and acceleration
    def execute (self, state: State):
        # Store the data
        data = {"x": [[], [], []], "v": [[], [], []], "a": [[], [], []], "t": []}

        # Loop while the time is less than maximum
        while self.time.valid():

            # Run the integrator
            state = step_leapfrog(state, self.time.delta)

            # Save the data
            data["x"][0].append(state.x.x)
            data["x"][1].append(state.x.y)
            data["x"][2].append(state.x.z)
            data["v"][0].append(state.v.x)
            data["v"][1].append(state.v.y)
            data["v"][2].append(state.v.z)
            data["a"][0].append(state.a.x)
            data["a"][1].append(state.a.x)
            data["a"][2].append(state.a.x)
            data["t"].append(self.time())

            if self.output:
                # Print the current output
                #print("Position:     [%6.4f    %6.4f     %6.4f]" % (x[0], x[1], x[2]))
                #print("Velocity:     [%6.4f    %6.4f     %6.4f]" % (v[0], v[1], v[2]))
                #print("Acceleration: [%6.4f    %6.4f     %6.4f]" % (a[0], a[1], a[2]))
                pass

            # Increment the time
            self.time.increment()

        return data
