import sys
from numpy import float64
from .time import Time
from .body import Body
from .system import System
from .color import Color
from .file import *


##########################################################################
# BASE INTEGRATOR CLASS
##########################################################################

# Base Integrator class
class Integrator:

    # Parameters that can be changed with the kwargs input

    # A flag for showing progress to the screen
    verbose = True

    # The number of progress ticks
    ticks = 67

    # Initialises the integrator with some output
    def __init__ (self, name: str, **kwargs):
        self.name = name
        self.__dict__.update(kwargs)
        print("%s Integrator Initialised." % name)



    ##########################################################################
    # INTEGRATION FUNCTIONS
    ##########################################################################

    # Updates a body with new properties
    # This function must be overriden by the integrator class
    def update (self, body: Body, dt: float64):
        pass


    # Executes the integration with a system
    # Takes in the model, time, list of bodies and the output file
    def execute (self, system: System, time: Time, output: str = "output.dat"):

        # Reset the time
        time.reset()

        # Set the global variables
        self.system = system
        self.output = output

        # Call check to see if needing to update
        if not InitialFile.write(time, system.model):
            Color.print("\nInitial conditions unchanged.", Color.WARNING)
            return

        # Print status
        Color.print("\nPerforming Integration...", Color.WARNING)

        # Create the output file and add a header
        file = OutputFile(output)
        file.header()

        # Write the initial data to the file
        file.write(time, system.body)

        # Loop while the time is less than maximum
        while time.running:

            # Increment the time
            time.increment()

            # Loop through all the bodies
            for body in system.bodies:

                # Run the integrator on the bodies
                self.update(body, time.delta)

            # Write the data to the output
            file.write(time, system.body)

            # Output the progress and flush the buffer
            if self.verbose and time.steps_max >= self.ticks and time.steps % int(time.steps_max / self.ticks) == 0:
                print("\t%2.1f%%  |  %s%s%s" % ((time.progress * 100.0), Color.YELLOW_B, \
                    ("=" * int(time.progress * self.ticks)), Color.END), end="\r")
                sys.stdout.flush()

        # Print status
        Color.print("\nIntegration Complete!", Color.SUCCESS)
        print("\tDuration: %8.4f s" % time.duration)
                
        # Safely close the file
        file.close()



##########################################################################
# LEAPFROG INTEGRATOR
##########################################################################

# Leap Frog integration class
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
        body.state.a = self.system.model.acceleration(body.state.x)
        body.state.v += 0.5 * dt * body.state.a

        # Update the body
        body.update()


