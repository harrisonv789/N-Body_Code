import numpy as np

# This class stores a three float 
class Vector:

    # Store the values of the vector
    x: np.float64 = 0.0
    y: np.float64 = 0.0
    z: np.float64 = 0.0

    # Initialises the vector
    def __init__ (self, x: np.float64 = 0.0, y: np.float64 = 0.0, z: np.float64 = 0.0):
        self.x = x
        self.y = y
        self.z = z



    ##########################################################################
    # SIMPLE OPERATORS
    ##########################################################################

    # Overrides the equals function
    def __eq__(self, other) -> bool:
        return self.x == other.x and self.y == other.y and self.z == other.z



    ##########################################################################
    # ADDITION
    ##########################################################################

    # Override the addition function
    def __add__ (self, other):
        # Check for float or int
        if type(other) is np.float64 or type(other) is float or type(other) is int:
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
        if type(other) is np.float64 or type(other) is float or type(other) is int:
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
        if type(other) is np.float64 or type(other) is float or type(other) is int:
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
        if type(other) is np.float64 or type(other) is float or type(other) is int:
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

    # Override the *= function
    def __idiv__(self, other):
        self = self.__div__(other)
        return self



    ##########################################################################
    # CONVERSIONS
    ##########################################################################
    
    # To string, which can be used as print lines
    def __str__ (self):
        return "X: %f, Y: %f, Z: %f" % (self.x, self.y, self.z)

    # To output file
    def output (self):
        return "%8.4f\t%8.4f\t%8.4f" % (self.x, self.y, self.z)

    # Converts the value to a list
    @property
    def array (self) -> list:
        return [self.x, self.y, self.z]

    

    ##########################################################################
    # MATHEMATICAL CALCULATIONS
    ##########################################################################

    # Dot product
    def dot (self, other):
        return (self.x * other.x) + (self.y * other.y) + (self.z * other.z)

    # Cross product
    def cross (self, other):
        i = self.y * other.z - self.z * other.y
        j = self.z * other.x - self.x * other.z
        k = self.x * other.y - self.y * other.x
        return Vector(i, j, k)

    # Magnitude of the vector
    @property
    def magnitude (self):
        return np.sqrt(self.x ** 2 + self.y ** 2 + self.z ** 2)

    # Directional (hat) normalized vector
    @property
    def normalized (self):
        return self * (1.0 / self.magnitude)
