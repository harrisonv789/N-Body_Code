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
    def update (self, body: Body, body_idx: int, dt: float64):
        pass



    # Executes the integration with a system
    # Takes in the model, time, list of bodies and the output file
    def execute (self, system: System, time: Time, output: str = "output.dat", output_timestep: float = 1):

        # Reset the time
        time.reset()

        # Set the global variables
        self.system = system
        self.output = output

        # Call check to see if needing to update
        if not InitialFile.write(time, system, output_timestep=output_timestep) and False:
            Color.print("\nInitial conditions unchanged.", Color.WARNING)
            return

        # Clear the previous files
        File.clear_files()

        # Stores the output files for each body
        files = []

        # Loops through and creates an output file for each 
        for idx, body in enumerate(system.bodies):

            # Get the file name and create the header
            file_name = File.get_file_name(output, idx)
            file = BodyFile(name = file_name)
            file.header()

            # Write the initial data to the file
            file.write(time, body)
            
            # Add the file to the list
            files.append(file)

        # Stores the output files from each cluster
        cluster_files = []

        # Loops through and creates an output file for each 
        for idx, cluster in enumerate(system.clusters):

            # Get the file name and create the header
            file_name = File.get_file_name("cluster", idx)
            file = ClusterFile(name = file_name)
            file.header()

            # Write the initial data to the file
            file.write(time, cluster)
            
            # Add the file to the list
            cluster_files.append(file)


        # Creates system file to store system data
        sys_file = SystemFile()
        sys_file.header()
        self.system.update()
        sys_file.write(time, self.system)

        # Print status
        Color.print("\nPerforming Integration...", Color.WARNING)

        # Get the next write time
        next_write_time = output_timestep - time.delta

        # Loop while the time is less than maximum
        while time.running:

            # Increment the time
            time.increment()

            # Determine if can write to this timestep
            can_write: bool = False

            # Calculates the next time and sets the can_write flag
            if time.time >= next_write_time or time.steps == time.steps_max:
                next_write_time += output_timestep
                can_write = True

            # Loop through all the bodies
            for idx, body in enumerate(system.bodies):

                # Run the integrator on the bodies
                self.update(body, idx, time.delta)

                # Write data to file if able to write
                if can_write: files[idx].write(time, body)        
                    
            # Update the system and cluster data file
            if can_write: 
                self.system.update()
                sys_file.write(time, self.system)     
                for idx, cluster in enumerate(system.clusters): cluster_files[idx].write(time, cluster)   

            # Output the progress and flush the buffer
            if self.verbose:
                print("\t%2.1f%%  |  %s%s%s" % ((time.progress * 100.0), Color.YELLOW_B, \
                    ("=" * int(time.progress * self.ticks)), Color.END), end="\r")
                sys.stdout.flush()

        # Print status
        Color.print("\nIntegration Complete!", Color.SUCCESS)
        print("\tDuration: %8.4f s" % time.duration)
                
        # Safely close the files
        for file in files: file.close()
        sys_file.close()



##########################################################################
# LEAPFROG INTEGRATOR
##########################################################################

# Leap Frog integration class
class LeapFrogIntegrator (Integrator):

    # Initialise the integrator with some timestep
    def __init__ (self, **kwargs):
        super().__init__("Leap Frog", **kwargs)


    # Takes in an Input position, Velocity, Accleration and Delta Time
    def update(self, body: Body, body_idx: int, dt: float):

        # Set up the initial velocity
        body.state.v += 0.5 * dt * body.state.a

        # Calculate the new parameters
        body.state.x += dt * body.state.v
        body.state.a = self.system.get_acceleration(body_idx)
        body.state.v += 0.5 * dt * body.state.a

        # Update the potential
        body.PE = self.system.get_potential(body_idx)

        # Update the body
        body.update()
        


