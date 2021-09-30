# Use numpy for storing the floats as doubles
from numpy import float64, sqrt

# This class stores three floats and can perform operations on them
class Vector:

    # Store the values of the vector
    x: float64 = 0.0
    y: float64 = 0.0
    z: float64 = 0.0

    # Initialises the Vector with the values
    def __init__ (self, x: float64 = 0.0, y: float64 = 0.0, z: float64 = 0.0):
        self.x = x
        self.y = y
        self.z = z

    ##########################################################################



    ##########################################################################
    # SIMPLE OPERATORS
    ##########################################################################

    # Overrides the equals function
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z

    # Overrides the not equals function
    def __ne__(self, other) -> bool:
        return not self.__eq__ (other)

    # Overrides the greater than function (using magnitude)
    def __gt__(self, other) -> bool:
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return self.magnitude > other
        # Check for vector
        elif type(other) is Vector:
            return self.magnitude > other.magnitude
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return self.magnitude > Vector(other[0], other[1], other[2]).magnitude

        return False

    # Overrides the less than or equal to function (using magnitude)
    def __le__ (self, other) -> bool:
        return not self.__gt__ (other)

    # Overrides the greater than or equal to function (using magitude)
    def __ge__ (self, other) -> bool:
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return self.magnitude >= other
        # Check for vector
        elif type(other) is Vector:
            return self.magnitude >= other.magnitude
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return self.magnitude >= Vector(other[0], other[1], other[2]).magnitude

        return False

    # Overrides the less than function (using magnitude)
    def __lt__ (self, other) -> bool:
        return not self.__ge__ (other)



    ##########################################################################
    # ADDITION
    ##########################################################################

    # Override the addition function
    def __add__ (self, other):
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return Vector(self.x + other, self.y + other, self.z + other)
        # Check for vector
        elif type(other) is Vector:
            return Vector(self.x + other.x, self.y + other.y, self.z + other.z)    
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return Vector(self.x + other[0], self.y + other[1], self.z + other[2])

        return self

    # Override the right hand addition
    def __radd__ (self, other):
        return self.__add__(other)

    # Override the += function
    def __iadd__(self, other):
        self = self.__add__(other)
        return self


    
    ##########################################################################
    # SUBTRACTION
    ##########################################################################

    # Override the subraction function
    def __sub__ (self, other):
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return Vector(self.x - other, self.y - other, self.z - other)
        # Check for vector
        elif type(other) is Vector:
            return Vector(self.x - other.x, self.y - other.y, self.z - other.z)    
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return Vector(self.x - other[0], self.y - other[1], self.z - other[2])

        return self

    # Override the right hand subtraction
    def __rsub__ (self, other):
        return self.__sub__(other)

    # Override the -= function
    def __isub__(self, other):
        self = self.__sub__(other)
        return self



    ##########################################################################
    # MULTIPLICATION
    ##########################################################################

    # Override the multiplication function
    def __mul__ (self, other):
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return Vector(self.x * other, self.y * other, self.z * other)
        # Check for vector
        elif type(other) is Vector:
            return Vector(self.x * other.x, self.y * other.y, self.z * other.z)    
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return Vector(self.x * other[0], self.y * other[1], self.z * other[2])

        return self

    # Override the right hand multiplication
    def __rmul__ (self, other):
        return self.__mul__(other)

    # Override the *= function
    def __imul__(self, other):
        self = self.__mul__(other)
        return self



    ##########################################################################
    # DIVISION
    ##########################################################################

    # Override the division function
    def __div__ (self, other):
        # Check for float or int
        if type(other) is float64 or type(other) is float or type(other) is int:
            return Vector(self.x / other, self.y / other, self.z / other)
        # Check for vector
        elif type(other) is Vector:
            return Vector(self.x / other.x, self.y / other.y, self.z / other.z)    
        # Check for list
        elif type(other) is list:
            if len(other) >= 3:
                return Vector(self.x / other[0], self.y / other[1], self.z / other[2])

        return self

    # Override the right hand division
    def __rdiv__ (self, other):
        return self.__div__(other)

    # Override the /= function
    def __idiv__(self, other):
        self = self.__div__(other)
        return self

    # Python3 division function
    def __truediv__ (self, other):
        return self.__div__(other)

    # Python3 right hand division
    def __rtruediv__ (self, other):
        return self.__rdiv__(other)

    # Python3 /= function
    def __itruediv__ (self, other):
        return self.__idiv__(other)



    ##########################################################################
    # LIST ELEMENTS
    ##########################################################################

    # Gets a specific x, y or z from the list using []
    # If invalid index used, then return a 0
    def __getitem__(self, idx: int) -> float64:
        if idx == 0:
            return self.x
        if idx == 1:
            return self.y
        if idx == 2:
            return self.z
        return 0.0

    # Sets a particular item in the list
    def __setitem__(self, idx: int, val: float64):
        if idx == 0:
            self.x = val
        elif idx == 1:
            self.y = val
        elif idx == 2:
            self.z = val

    # Gets the length of the list
    def __len__ (self):
        return 3

    # Iterates through the list
    def __iter__ (self):
        for elem in [self.x, self.y, self.z]:
            yield elem



    ##########################################################################
    # CONVERSIONS
    ##########################################################################
    
    # To string, which can be used as print lines
    def __str__ (self):
        return "X: %f, Y: %f, Z: %f" % (self.x, self.y, self.z)

    # Convert the vector to a string that can be used as the file
    def output (self) -> str:
        return "%8.4f\t%8.4f\t%8.4f" % (self.x, self.y, self.z)

    # Converts the value to a list
    @property
    def array (self) -> list:
        return [self.x, self.y, self.z]

    

    ##########################################################################
    # MATHEMATICAL CALCULATIONS
    ##########################################################################

    # Dot product
    def dot (self, other) -> float64:
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    # Cross product
    def cross (self, other):
        i = self.y * other.z - self.z * other.y
        j = self.z * other.x - self.x * other.z
        k = self.x * other.y - self.y * other.x
        return Vector(i, j, k)

    # Magnitude of the vector
    @property
    def magnitude (self) -> float64:
        return sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # Magnitude of the vector (different name)
    @property
    def mag (self) -> float64:
        return self.magnitude

    # Directional (hat) normalized vector
    @property
    def normalized (self):
        return self / self.magnitude

    # Unit vector (different name)
    @property
    def unit (self):
        return self.normalized

    ##########################################################################
