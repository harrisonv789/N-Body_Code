import numpy as np
import os
from . import mathematics as math
from .time import Time
from .state import State

# Runs the integration
class Integrator:

    # Initialise the integrator with some timestep
    def __init__ (self, output: str = "output.dat"):
        self.output = output


    # Takes in an Input position, Velocity, Accleration and Delta Time
    def step_leapfrog(self, state: State, dt: float):

        # Set up the initial velocity
        state.v += 0.5 * dt * state.a

        # Calculate the new parameters
        state.x += dt * state.v
        state.a = math.calculate_acceleration(state.x)
        state.v += 0.5 * dt * state.a

        # Return the values
        return state


    # Call the integrator with a starting position, velocity and acceleration
    def execute (self, time: Time, state: State):

        # Call check to see if needing to update
        if not self.needs_update(time, state):
            return

        # Clear the output and open the file
        with open(self.output, "w") as file:

            # Add the header row
            file.write("   time     pos_x     pos_y     pos_z     vel_x     vel_y     vel_z     acc_x     acc_y     acc_z   \n")

            # Loop while the time is less than maximum
            while time.running:

                # Run the integrator
                state = self.step_leapfrog(state, time.delta)

                # Write the data to the output
                file.write("%8.4f\t%s\n" % (time(), state.output()))

                # Increment the time
                time.increment()


    # Determines if the data needs to be run again
    def needs_update (self, time, state):
        if os.path.isfile("initial.dat"):
            with open("initial.dat", "r") as file:
                if file.read() == "%s\n%s" % (str(time), str(state)):
                    return False

        # Update the file
        with open("initial.dat", "w") as file:
            file.write("%s\n%s" % (str(time), str(state)))

        # Returns a requirement to restart
        return True
