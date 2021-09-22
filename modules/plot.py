# Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
from .color import Color

# Create a class for a plotter
class Plotter:

    # Store the data as a dictionary
    data = {}

    # Init constructor takes in some output data file and some arguments
    def __init__ (self, **kwargs):

        # Store references to the outputs
        self.outputs = kwargs.get("outputs", ["output.dat"])
        self.output = self.outputs[0]
        self.multiple = len(self.outputs) > 1

        # Load the data
        self.load_data()

        # Print the header
        print("\n--------------------------------------------------")
        print(  "PLOTTING DATA FROM %s" % ", ".join(self.outputs))
        print(  "--------------------------------------------------")


    # Loads the data from all outputs and stores it in a object
    def load_data (self):
        for output in self.outputs:
            self.data[output] = np.genfromtxt(output, names=True)


    # Asks the user what to plot from a selection
    def ask_plot (self):
        # Gets the options from the output file
        with open(self.output, "r") as file:
            headers = [h.strip() for h in file.readline().strip().split(" ") if h != ""]
        
        # Print all the options from the headers
        print("\nPlease select from the following options:\n")
        for idx, h in enumerate(headers):
            print("  %s(%d)\t%s" % (Color.PARAM, idx, h))
        print("\n  %s(Q)\tQUIT%s\n" % (Color.WARNING, Color.END))

        # Loop while plotting
        while True:
            print("---")

            # Get the X and Y axis and check for valid
            x_axis = input("Plot Selection for (x) Axis: ").lower()
            if x_axis[0] == "q": break 
            if not (x_axis.isnumeric() and int(x_axis) < len(headers)) and x_axis not in headers: continue
            x_axis = headers[int(x_axis)] if x_axis.isnumeric() else x_axis

            # Get multiple Y axis
            y_axis_in = input("Plot Selection(s) for (y) Axis: ").lower()
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
    def plot (self, x, y_plots, args, title = ""):

        # Check arguments prior to plotting
        marker = "o" if "points" in args else ""
        linestyle = 'none' if "points" in args else "solid"

        # Loop through each y plot
        for key in self.data.keys():
            data = self.data[key]
            for y in y_plots:
                # Determine label
                label = "%s - %s" % (y, key) if self.multiple else y
                plt.plot(data[x], data[y], marker=marker, linestyle=linestyle, markersize=2, label=label)
            
        plt.xlabel("$\mathrm{" + x + "}$")
        plt.ylabel("$\mathrm{" + "}$, $\mathrm{".join(y_plots) + "}$")

        if len(y_plots) > 1 or self.multiple:
            plt.legend()

        if "equal" in args:
            plt.axis('equal')
        if "logx" in args:
            plt.xscale("log")
        if "logy" in args:
            plt.yscale("log")
        if "star" in args:
            plt.plot(0, 0, "*", markersize=10)
        if "grid" in args:
            plt.grid()

        plt.title(title)

        # Show the plot
        plt.show()