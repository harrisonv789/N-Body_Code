import numpy as np
import os, sys
from . import mathematics as math
from .time import Time
from .state import State
from .body import Body

# Runs the integration
class Integrator:

    # Initialise the integrator with some timestep
    def __init__ (self, output: str = "output.dat"):
        self.output = output


    # Takes in an Input position, Velocity, Accleration and Delta Time
    def step_leapfrog(self, body: Body, dt: float):

        # Set up the initial velocity
        body.state.v += 0.5 * dt * body.state.a

        # Calculate the new parameters
        body.state.x += dt * body.state.v
        body.state.a = math.calculate_acceleration(body.state.x)
        body.state.v += 0.5 * dt * body.state.a

        # Return the values
        return body


    # Call the integrator with a starting position, velocity and acceleration
    def execute (self, time: Time, body: Body):

        # Call check to see if needing to update
        if not self.needs_update(time, body) and False:
            print("Initial conditions unchanged.")
            return

        # Clear the output and open the file
        with open(self.output, "w") as file:

            # Print status
            print("Performing Integration...")

            # Add the header row
            file.write(body.get_header())

            # Loop while the time is less than maximum
            while time.running:

                # Run the integrator
                body = self.step_leapfrog(body, time.delta)

                # Write the data to the output
                file.write("%8.4f\t%s\n" % (time(), body.output()))

                # Increment the time
                time.increment()

                # Output the progress and flush the buffer
                if time.steps % int(time.steps_max / 50) == 0:
                    print("=", end="")
                    sys.stdout.flush()


    # Determines if the data needs to be run again
    def needs_update (self, time, body):
        if os.path.isfile("initial.dat"):
            with open("initial.dat", "r") as file:
                if file.read() == "%s\n%s" % (str(time), str(body)):
                    return False

        # Update the file
        with open("initial.dat", "w") as file:
            file.write("%s\n%s" % (str(time), str(body)))

        # Returns a requirement to restart
        return True
