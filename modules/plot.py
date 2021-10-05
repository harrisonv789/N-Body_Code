# Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from .color import Color
from .analysis import Analysis

# Create a class for a plotter
class Plotter:

    # Store the data as a dictionary
    data = {}
    data_analysis = {}

    # Init constructor takes in some output data file and some arguments
    def __init__ (self, **kwargs):

        # Store references to the outputs
        self.outputs = kwargs.get("outputs", ["output.dat"])
        self.multiple = len(self.outputs) > 1
        self.analysis = kwargs.get("analysis", False) and self.multiple
        self.output = self.outputs[0]

        # Load the data
        self.load_data()

        # Gets the options from the output file
        with open(self.output, "r") as file:
            self.headers = [h.strip() for h in file.readline().strip().split(" ") if h != ""]

        # Print the header
        print("\n--------------------------------------------------")
        print("%sPLOTTING DATA FROM %s%s" % (Color.HEADER, ", ".join(self.outputs), Color.RESET))
        print(  "--------------------------------------------------")



    # Loads the data from all outputs and stores it in a object
    def load_data (self):
        # Clear the keys
        self.data = {}
        self.data_analysis = {}

        for output in self.outputs:
            self.data[output] = np.genfromtxt(output, names=True)

            # If plotting the analysis too
            if self.analysis: 
                self.data_analysis[output] = np.genfromtxt(Analysis.file_name(output), names=True)



    # Asks the user what to plot from a selection
    def ask_plot (self):
        
        # Print all the options from the headers
        print("\nPlease select from the following options:\n")
        for idx, h in enumerate(self.headers):
            print("  %s(%d)\t%s" % (Color.PARAM, idx, h))

        # Print analysis options
        if self.analysis:
            print()
            for idx, h in enumerate(Analysis.headers()):
                print("  %s(%d)\t%s" % (Color.PARAM, idx + len(self.headers), h))
        
        print("\n  %s(Q)\tQUIT%s\n" % (Color.WARNING, Color.END))

        # Remember previous commands (for x, y and params)
        defaults = ["pos_x", "pos_y", "grid, anim"]

        # Loop while plotting
        while True:
            print("\n---")

            # Get the X and Y axis and check for valid
            x_axis = input("\nPlot Selection for (%sx%s) Axis\n\tDefault = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, defaults[0], Color.RESET)).lower()

            # If empty, use defaults
            if x_axis == "":
                x_axis = defaults[0]

            # Check to see if it an analysis value
            if self.analysis and (x_axis.isnumeric() and int(x_axis) >= len(self.headers) and int(x_axis) < len(self.headers) + len(Analysis.headers())) or x_axis in Analysis.headers():
                # Determine the x axis header
                x_axis = Analysis.headers()[int(x_axis) - len(self.headers)] if x_axis.isnumeric() else x_axis
                
                # Ask the user for a y axis to check
                y_axis = input("Analysis for %s value: " % x_axis).lower()
                if not (y_axis.isnumeric() and int(y_axis) < len(self.headers)) and y_axis not in self.headers: continue
                y_axis = self.headers[int(y_axis)] if y_axis.isnumeric() else y_axis

                # Plot this tool
                self.plot(x_axis, [y_axis], ["grid"], analysis=True)
                defaults = [x_axis, y_axis, "grid"]
                continue

            # Otherwise, standard method
            if x_axis == "q": break 
            if not (x_axis.isnumeric() and int(x_axis) < len(self.headers)) and x_axis not in self.headers: continue
            x_axis = self.headers[int(x_axis)] if x_axis.isnumeric() else x_axis
            
            # Get multiple Y axis
            y_axis_in = input("\nPlot Selection(s) for (%sy%s) Axis\n\tDefault = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, defaults[1], Color.RESET)).lower()

            # Check for missing y values
            if y_axis_in == "":
                y_axis_in = defaults[1]

            # Get all y axis values
            y_axis_in = [y.strip() for y in y_axis_in.split(",")]
            if y_axis_in[0] == "q": break
            if '"' in y_axis_in[0]: # For grouping multiple graphs
                y_axis_in = y_axis_in[0].replace('"', "")
                y_axis_in = [head for head in self.headers if y_axis_in == head.lower().split("_")[0]]
            y_axis = []

            failed = False

            # Loop through each axis
            for y in y_axis_in:
                if not (y.isnumeric() and int(y) < len(self.headers)) and y not in self.headers:
                    failed = True
                    break
                y_axis.append(self.headers[int(y)] if y.isnumeric() else y)

            # Check for failed axis
            if failed: continue

            # Get extra parameters
            params = input("\nGraphing %sparameters%s (space separated)\n\tDefault = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, defaults[2], Color.RESET)).lower()

            # If missing parameters or quitting
            if params == "q": break
            if params == "": params = defaults[2]

            # Split the parameters into a list
            params = [p.lower().strip() for p in params.replace(",", " ").split(" ") if p != ""]
            
            # Make a plot with the parameters
            self.plot(x_axis, y_axis, params)
            defaults = [x_axis, ", ".join(y_axis), ", ".join(params)]



    # Makes a simple plot
    def plot (self, x, y_plots, args, title = "", analysis = False, files = []):

        # If files is empty
        if files == []:
            files = self.data.keys()

        # Check arguments prior to plotting
        marker = "o" if "points" in args else ""
        linestyle = "dashed" if "dashed" in args else "solid"
        linestyle = 'none' if "points" in args else linestyle

        # Create the subplots
        fig, ax = plt.subplots()

        # If analysis
        if analysis:
            row = self.headers.index(y_plots[0])

            # Loop through each data file
            for idx, key in enumerate(files):
                data = self.data_analysis[key]
                ax.plot(idx, data[x][row], marker="o", linestyle=linestyle, markersize=10, label=key)
                ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        else:
            # Loop through each y plot
            for key in files:
                
                data = self.data[key]

                for y in y_plots:
                    # Determine label
                    label = "%s - %s" % (y, key) if self.multiple else y

                    # Plot the data
                    ax.plot(data[x], data[y], marker=marker, linestyle=linestyle, markersize=2, label=label)
        
        # Get the X and Y labels
        ax.set_xlabel(self.__get_latex(x))
        ax.set_ylabel(self.__get_latex(y_plots))

        if len(y_plots) > 1 or self.multiple:
            ax.legend()

        # Add the arguments
        if "equal" in args:
            ax.axis('equal')
        if "logx" in args:
            ax.set_xscale("log")
        if "logy" in args:
            ax.set_yscale("log")
        if "star" in args:
            ax.plot(0, 0, "*", markersize=10)
        if "grid" in args:
            ax.grid()

        # Animate the system
        if "anim" in args:

            if "slow" in args:
                interval = 100
            elif "fast" in args:
                interval = 10
            else:
                interval = 20

            # Store a list of points
            points = []

            # Loop through the y plots
            for y in y_plots:

                # Get the first poition of the data
                point, = ax.plot(data[x][0], data[y][0], marker="o", color="black")
                points.append(point)

            # Create an update with some alpha value between 0 and 1
            def update (a: float):
                val = int(len(data[x]) * a)
                for idx, p in enumerate(points):
                    p.set_data([[data[x][val]], [data[y_plots[idx]][val]]])

            # Create the animation call
            anim = FuncAnimation(fig, update, interval=interval, repeat=True, frames=np.linspace(0,1.0,100, endpoint=False))

        # Add a title
        plt.title(title)

        # Show the plot
        plt.show()



    # Determines the latex symbol for a column name
    def __get_latex (self, columns) -> str:
        # Remove listing for single columns
        if type(columns) is list:
            if len(columns) == 1:
                columns = columns[0]
        
        # Check if columns is still a list
        if type(columns) is list:
            lat_c = []
            for c in columns:
                lat_c.append(self.__get_latex(c))
            return ", ".join(lat_c)
        else:
            if "_" not in columns:
                return "$\mathrm{" + columns + "}$"
            else:
                data = columns.split("_")
                return "$\mathrm{" + data[0] + "_{" + data[1] + "}}$"