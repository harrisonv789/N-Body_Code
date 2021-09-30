from .body import Body
from .time import Time


# Class for writing to an output file
class OutputFile:

    # Constructor to initialise a file with some path
    def __init__ (self, path: str, write: bool = True):
        self.path = path
        self.open(write)

    # Opens a file
    def open (self, write: bool):
        flag = "w" if write else "r"
        self.file = open(self.path, flag)

    # Writes a header
    # Option to write a custom header
    def header (self, custom = None):
        if not custom:
            self.file.write(Body.get_header())
        else:
            self.file.write(custom)

    # Writes the information of a body to the file
    def write (self, time: Time, body: Body):
        self.file.write("%8.4f\t%s\n" % (time(), body.output()))

    # Closes a file
    def close (self):
        self.file.close()