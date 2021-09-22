import numpy as np
import os, sys
from .time import Time
from .body import Body
from .model import Model

# Runs the integration
class Integrator:

    # Initialise the integrator with some timestep
    def __init__ (self, model: Model, output: str = "output.dat"):
        self.model = model
        self.output = output


    # Takes in an Input position, Velocity, Accleration and Delta Time
    def step_leapfrog(self, body: Body, dt: float):

        # Set up the initial velocity
        body.state.v += 0.5 * dt * body.state.a

        # Calculate the new parameters
        body.state.x += dt * body.state.v
        body.state.a = self.model.calc_acceleration(body.state.x)
        body.state.v += 0.5 * dt * body.state.a

        # Update the body
        body.update()

        # Return the values
        return body


    # Call the integrator with a starting position, velocity and acceleration
    def execute (self, time: Time, body: Body):

        # Call check to see if needing to update
        if not self.needs_update(time, body):
            print("\nInitial conditions unchanged.")
            return

        # Clear the output and open the file
        with open(self.output, "w") as file:

            # Print status
            print("\nPerforming Integration...")

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
                if time.steps_max >= 50 and time.steps % int(time.steps_max / 50) == 0:
                    print("=", end="")
                    sys.stdout.flush()


    # Determines if the data needs to be run again
    def needs_update (self, time, body):

        # Create parameter line
        save = "%s\n%s\n%s" % (str(time), str(body), str(self.model.__dict__))

        # Check to see if the file is the same
        if os.path.isfile("initial.dat"):
            with open("initial.dat", "r") as file:
                if file.read() == save:
                    return False

        # Update the file
        with open("initial.dat", "w") as file:
            file.write(save)

        # Returns a requirement to restart
        return True
