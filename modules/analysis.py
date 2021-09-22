# Import relevant packages
import numpy as np
from .color import Color

# Class for analysising data
class Analysis:

    # Stores the data as a dictionary
    data = {}

    # Constructor for initialising the analysis
    def __init__ (self, file, save = False):
        self.file = file
        self.raw_data = np.genfromtxt(file, names=True)
        self.analyse_data()
        if save: self.save()

    # Create analysis on each of the data points
    # Min, Max, Average
    def analyse_data (self):
        headers = []

        # Gets the options from the output file
        with open(self.file, "r") as file:
            headers = [h.strip() for h in file.readline().strip().split(" ") if h != ""]

        # Loop through each of the fields
        for key in headers:
            minval = min(self.raw_data[key])
            maxval = max(self.raw_data[key])
            aveval = sum(self.raw_data[key]) / len(self.raw_data[key])

            # Add the key to the data
            self.data[key] = {"min": minval, "max": maxval, "ave": aveval}


    # If saving a file
    def save (self):
        self.savefile = self.file_name(self.file)

        # Saves the data to the file
        with open (self.savefile, "w") as file:
            keys = list(self.data.keys())
            keys.insert(0, "key")
            file.write(" key    \t%s" % "\t     ".join(self.headers()))

            # Loop through all the headers and write the data
            for param in self.data.keys():
                file.write("\n%s" % param)
                for key in self.headers():
                    file.write("\t%8.4f" % self.data[param][key])

        # Output success
        print("\nSuccessfully written analysis data to %s" % self.savefile)


    # Outputs all of the analysis
    def output (self):

        # Print the header
        print("\n--------------------------------------------------")
        print(  "ANALYSING DATA %s" % self.file)
        print(  "--------------------------------------------------")
        print("%s\n\t\t    %s\n%s" % (Color.DEFAULT, "\t\t    ".join(self.headers()), Color.END))
        
        # Loop through each key and output the information
        for key in self.data.keys():
            dict_ = self.data[key]
            print("%s    %s%s\t%8.4f\t%8.4f\t%8.4f" % (Color.PARAM, key, Color.END, dict_["min"], dict_["max"], dict_["ave"]))


    # Returns the current analytical keys
    @staticmethod
    def headers ():
        return ["min", "max", "ave"]

    # Returns the name of the anlysis file
    @staticmethod
    def file_name (file):
        return file[:-4] + "_analysis.dat"
