import os, sys
from numpy import float64
from .time import Time
from .body import Body
from .system import System
from .model import Model


# Base Integrator class
class Integrator:

    # Parameters that can be changed with the kwargs input

    # A flag for showing progress to the screen
    verbose = True

    # Initialises the integrator with some output
    def __init__ (self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
        print("%s Integrator Initialised." % name)



    ##########################################################################
    # INTEGRATION FUNCTIONS
    ##########################################################################

    # Updates a particle with new properties
    # This function must be overriden by the integrator class
    def update (self, body: Body, dt: float64):
        pass


    # Executes the integration with a system
    # Takes in the model, time, list of bodies and the output file
    def execute (self, time: Time, system: System, output: str = "output.dat"):

        # Set the global variables
        self.system = system
        self.output = output

        # Call check to see if needing to update
        if not self.needs_update(time, system.body) and False:
            print("\nInitial conditions unchanged.")
            return

        # Clear the output and open the file
        with open(output, "w") as file:

            # Print status
            print("\nPerforming Integration...")

            # Add the header row
            file.write(system.body.get_header())

            # Loop while the time is less than maximum
            while time.running:

                # Write the data to the output
                file.write("%8.4f\t%s\n" % (time(), system.body.output()))

                # Increment the time
                time.increment()

                # Run the integrator
                self.update(system.body, time.delta)

                # Output the progress and flush the buffer
                if time.steps_max >= 50 and time.steps % int(time.steps_max / 50) == 0:
                    print("=", end="")
                    sys.stdout.flush()


    # Determines if the data needs to be run again
    def needs_update (self, time: Time, body: Body):

        # Create parameter line
        save = "%s\n%s\n%s" % (str(time), str(body), str(self.system.model.__dict__))

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





# Runs the integration
class LeapFrogIntegrator (Integrator):

    # Initialise the integrator with some timestep
    def __init__ (self, **kwargs):
        super().__init__("Leap Frog", **kwargs)


    # Takes in an Input position, Velocity, Accleration and Delta Time
    def update(self, body: Body, dt: float):

        # Set up the initial velocity
        body.state.v += 0.5 * dt * body.state.a

        # Calculate the new parameters
        body.state.x += dt * body.state.v
        body.state.a = self.system.model.calc_acceleration(body.state.x)
        body.state.v += 0.5 * dt * body.state.a

        # Update the body
        body.update()
