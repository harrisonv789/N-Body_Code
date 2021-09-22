# Import relevant packages
import numpy as np
from .color import Color

# Class for analysising data
class Analysis:

    # Stores the data as a dictionary
    data = {}

    # Constructor for initialising the analysis
    def __init__ (self, file):
        self.file = file
        self.raw_data = np.genfromtxt(file, names=True)
        self.analyse_data()

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

    # Outputs all of the analysis
    def output (self):

        # Print the header
        print("\n--------------------------------------------------")
        print(  "ANALYSING DATA %s" % self.file)
        print(  "--------------------------------------------------")
        print("%s\n\t\t    min\t\t    max\t\t    ave\n%s" % (Color.DEFAULT, Color.END))
        
        # Loop through each key and output the information
        for key in self.data.keys():
            dict_ = self.data[key]
            print("%s    %s%s\t%8.4f\t%8.4f\t%8.4f" % (Color.PARAM, key, Color.END, dict_["min"], dict_["max"], dict_["ave"]))