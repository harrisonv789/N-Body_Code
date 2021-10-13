from numpy import float64
from .constants import *
from .model import Model
from .body import Body
from .vector import Vector
from .state import State
from .initial_conditions import InitialConditions

# Stores information related to the system
class System:

    ##########################################################################
    # PARAMETERS
    ##########################################################################

    # Whether to use background model
    use_background: bool = False

    # The number of bodies
    n_bodies: int = 1

    # The masses of the bodies
    masses: list = []
    
    # A key for the Initial Conditions
    IC: str = ""

    # Initial radius
    radius: float = 1.0

    # Initial velocity vector
    vel_vec: Vector = Vector(0, 1.0, 0)

    # A list of all bodies
    bodies = []

    # The intial conditions function callback
    init_callback = None


    ##############################
    # Calculated Properties

    # The total mass of the system
    mass_total: float64 = 1.0

    # The angular momentum of the system
    L: Vector = Vector()

    # The total energy of the system
    E_tot: float64 = 0.0

    # The total initial energy of the system
    E_init = None

    # The kinetic energy of the system
    E_kin: float64 = 0.0

    # The potential energy of the system
    E_pot: float64 = 0.0

    # The energy error of the system
    E_err: float64 = 0.0


    ##########################################################################
    # SYSTEM FUNCTIONS
    ##########################################################################

    # Creates a new system with a number of bodies
    # By default, it will create 1 body
    def __init__ (self, model: Model, n_bodies: int = 1, **kwargs):
        self.model = model
        self.n_bodies = n_bodies
        self.__dict__.update(kwargs)
        self.reset()


    # Resets the system and sets up the bodies
    def reset (self):

        # If only one body, use a background model
        if self.n_bodies == 1: self.use_background = True

        # Resets the list of bodies
        self.bodies = []

        # Check for missing mass information and use ones
        if len(self.masses) < self.n_bodies:
            for i in range(len(self.masses), self.n_bodies):
                self.masses.append(1.0)
        
        # Calculate the total system mass
        self.mass_total = sum(self.masses)

        # Set the mass of the modle
        self.model.M = self.mass_total

        # Loop through each of the bodies to create
        for idx in range(self.n_bodies):

            # Create the new body
            b = Body(self.model, State(), self.masses[idx])

            # Get the initial state of the body
            b.state = self.get_initial(idx, b)

            # Add the body to the list
            self.bodies.append(b)

        # Set the starting properties of the bodies
        for idx in range(self.n_bodies):
            # Update the potential and reset the body
            self.bodies[idx].PE = self.get_potential(idx)
            self.bodies[idx].reset()


    # Updates the properties of the system
    def update(self):
        self.get_system_L()
        self.get_system_PE()
        self.get_system_KE()
        self.get_system_energy()
        self.get_system_E_error()


    # Returns the output data for the file
    def output (self) -> str:
        return "%8.4f\t%s\t%8.4f\t%8.4f\t%8.4f\t%8.4f" % \
        (self.mass_total, self.L.output(), self.E_tot, self.E_kin, self.E_pot, self.E_err)

    # Defines the list of parameters
    PROPERTIES = ["time", "mass", "mom_x", "mom_y", "mom_z", "E_tot", "E_kin", "E_pot", "E_err"]

    # Returns the headers of the body file
    @staticmethod
    def get_header () -> str:
        output = "   "
        for p in System.PROPERTIES:
            output += p + "    "
        return output[:-4] + "\n"

    

    ##########################################################################
    # MATHEMATICAL FUNCTIONS
    ##########################################################################

    # Calculates the acceleration vector of some body
    def get_acceleration (self, body_idx: int) -> Vector:

        # Get the body and background acceleration
        body: Body = self.bodies[body_idx]
        a: Vector = self.model.acceleration(body.state.x) if self.use_background else Vector()
        
        # Calculate the effects of all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx:
                distance: Vector = body.state.x - self.bodies[idx].state.x
                mag = distance.mag
                a_fac = (-1.0 * G * self.bodies[idx].mass) / (mag ** 3) if mag > 0 else 0.0
                a += a_fac * distance

        # Return the acceleration
        return a

    
    # Calculates the potential of some body
    def get_potential (self, body_idx: int) -> float64:

        # Get the body and background potential
        body = self.bodies[body_idx]
        pot = self.model.potential(body.position) if self.use_background else 0.0

        # Loop through all bodies
        for idx in range(self.n_bodies):
            if idx != body_idx:
                # Add the potential to the data
                mass = -1.0 * G * body.mass * self.bodies[idx].mass
                mag = (body.position - self.bodies[idx].position).mag
                pot += mass / mag if mag > 0 else 0.0

        # Return the potential over the mass
        return pot / body.mass

    
    # Calculates the current system total angular momentum
    def get_system_L (self) -> Vector:
        self.L = Vector()
        for body in self.bodies:
            self.L += body.L
        return self.L

    
    # Calculates the current system total kinetic energy
    def get_system_KE (self) -> float64:
        self.E_kin = 0.0
        for body in self.bodies:
            self.E_kin += body.KE
        return self.E_kin

    # Calculates the current system total potential energy
    def get_system_PE (self) -> float64:
        self.E_pot = 0.0
        for body in self.bodies:
            self.E_pot += body.PE * body.mass
        return self.E_pot / 2.0


    # Calculates the current system total energy
    def get_system_energy (self) -> float64:
        self.E_tot = self.E_kin + self.E_pot
        if not self.E_init: self.E_init = self.E_tot
        return self.E_tot


    # Calculates the current system total energy error
    def get_system_E_error (self) -> float64:
        if self.E_init and self.E_init != 0.0: self.E_err = abs((self.E_init - self.E_tot) / self.E_init)
        return self.E_err




    ##########################################################################
    # INITIAL STATE FUNCTIONS
    ##########################################################################

    # Sets the intial values of the bodies
    def get_initial (self, idx: int, body: Body) -> State:

        # If a callback exists
        if self.init_callback:
            return self.init_callback(self, idx, body)

        # If using two body problem
        if self.IC in InitialConditions.IC_KEYS:
            IC = InitialConditions(self.IC.lower(), self.model, self.mass_total)
            return IC.get_state(idx, body)

        # If standard system
        return self.model.init_state(self.radius, self.vel_vec)
