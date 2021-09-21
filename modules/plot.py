# Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
from .color import Color

# Create a class for a plotter
class Plotter:

    # Init constructor takes in some output data file and some arguments
    def __init__ (self, **kwargs):

        # Load the data
        self.output = kwargs.get("output", "output.dat")
        self.load_data()


    # Loads the data and stores it in a object
    def load_data (self):
        self.data = np.genfromtxt(self.output, names=True)


    # Asks the user what to plot from a selection
    def ask_plot (self):
        # Gets the options from the output file
        with open(self.output, "r") as file:
            headers = [h.strip() for h in file.readline().strip().split(" ") if h != ""]
        
        # Print all the options from the headers
        print("\n\nPlease select from the following options:\n")
        for idx, h in enumerate(headers):
            print("\t%s(%d) %s" % (Color.CYAN, idx, h))
        print("\n\t%s(Q) QUIT%s\n" % (Color.GREEN, Color.NORMAL))

        # Loop while plotting
        while True:
            print("---")

            # Get the X and Y axis and check for valid
            x_axis = input("Plot Selection for (x) Axis: ").lower()
            if x_axis[0] == "q": break 
            if not (x_axis.isnumeric() and int(x_axis) < len(headers)) and x_axis not in headers: continue
            x_axis = headers[int(x_axis)] if x_axis.isnumeric() else x_axis

            # Get multiple Y axis
            y_axis_in = input("Plot Selection for (y) Axis: ").lower()
            y_axis_in = [y.strip() for y in y_axis_in.split(",")]
            if y_axis_in[0] == "q": break
            y_axis = []

            failed = False

            # Loop through each axis
            for y in y_axis_in:
                if not (y.isnumeric() and int(y) < len(headers)) and y not in headers:
                    failed = True
                    break
                y_axis.append(headers[int(y)] if y.isnumeric() else y)

            # Check for failed axis
            if failed: continue

            # Get extra parameters
            params = input("Please enter any parameters (separated) by commas: ").split(",")
            params = [p.lower().strip() for p in params]

            # Make a plot with the parameters
            self.plot(x_axis, y_axis, params)


    # Makes a simple plot
    def plot (self, x, y_plots, args):

        # Check arguments prior to plotting
        marker = "" if "lines" in args else "o"
        linestyle = 'solid' if "lines" in args else "none"

        # Loop through each y plot
        for y in y_plots:
            plt.plot(self.data[x], self.data[y], marker=marker, linestyle=linestyle, markersize=2)
        
        plt.xlabel("$\mathrm{" + x + "}$")
        plt.ylabel("$\mathrm{" + "}$, $\mathrm{".join(y_plots) + "}$")

        if len(y_plots) > 1:
            plt.legend(y_plots)

        if "equal" in args:
            plt.axis('equal')
        if "logx" in args:
            plt.xscale("log")
        if "logy" in args:
            plt.yscale("log")
        if "star" in args:
            plt.plot(0, 0, "*")

        # Show the plot
        plt.show()