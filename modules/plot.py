# Import relevant packages
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
from .color import Color
from .analysis import Analysis

# Create a class for a plotter
class Plotter:

    # Store the data as a dictionary
    data = {}
    data_analysis = {}

    # Store a list of standard plots
    preset_plots = {
        "pos":      ["pos_x",   "pos_y",                        "equal, star, grid, anim"],
        "3d":       ["pos_x",   "pos_y, pos_z",                 "star, anim, 3d"],
        "energy":   ["time",    "E_tot, E_kin, E_pot, E_err",   "grid"],
        "timepos":  ["time",   "pos_x, pos_y, pos_z",           "grid"],
    }

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
        
        print("\n  %s(Q)\tQUIT%s" % (Color.WARNING, Color.END))

        # Remember previous commands (for x, y and params)
        previous = ["", "", ""]

        # Loop while plotting
        while True:
            print("\n---")

            # Ask for a preset
            preset = input("\nPreset Plot\n\tOptions = %s%s%s: " \
                % (Color.DEFAULT, ", ".join(self.preset_plots.keys()), Color.RESET)).lower()

            # Check for quit
            if preset == "q": break
            
            # Check if has a valid plot
            if preset in self.preset_plots.keys():
                previous = self.preset_plots[preset]

            # Get the X and Y axis and check for valid
            x_axis = input("\nPlot Selection for (%sx%s) Axis\n\tPrevious = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, previous[0] if previous[0] != "" else "None", Color.RESET)).lower()

            # If empty, use defaults
            if x_axis == "":
                x_axis = previous[0]

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
                previous = [x_axis, y_axis, "grid"]
                continue

            # Otherwise, standard method
            if x_axis == "q": break 
            if not (x_axis.isnumeric() and int(x_axis) < len(self.headers)) and x_axis not in self.headers: continue
            x_axis = self.headers[int(x_axis)] if x_axis.isnumeric() else x_axis
            
            # Get multiple Y axis
            y_axis_in = input("\nPlot Selection(s) for (%sy%s) Axis\n\tPrevious = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, previous[1] if previous[1] != "" else "None", Color.RESET))

            # Check for missing y values
            if y_axis_in == "":
                y_axis_in = previous[1]

            # Get all y axis values
            y_axis_in = [y.strip() for y in y_axis_in.split(",")]
            if y_axis_in[0] == "q": break
            if '"' in y_axis_in[0]: # For grouping multiple graphs
                y_axis_in = y_axis_in[0].replace('"', "")
                y_axis_in = [head for head in self.headers if y_axis_in.lower() == head.lower().split("_")[0]]
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
            params = input("\nGraphing %sparameters%s (space separated)\n\tPrevious = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, previous[2] if previous[2] != "" else "None", Color.RESET)).lower()

            # If missing parameters or quitting
            if params == "q": break
            if params == "": params = previous[2]

            # Split the parameters into a list
            params = [p.lower().strip() for p in params.replace(",", " ").split(" ") if p != ""]
            
            # Make a plot with the parameters
            self.plot(x_axis, y_axis, params)
            previous = [x_axis, ", ".join(y_axis), ", ".join(params)]



    # Makes a simple plot
    def plot (self, x, y_plots, args, title = "", analysis = False, files = []):

        # If files is empty
        if files == []:
            files = self.data.keys()

        # Check arguments prior to plotting
        marker = "o" if "points" in args else ""
        linestyle = "dashed" if "dashed" in args else "solid"
        linestyle = 'none' if "points" in args else linestyle

        # Will set a 3D graph if it is an argument and 2 Y values are used (the second for Z)
        _3d = "3d" in args and len(y_plots) == 2 and not analysis

        # Create the subplots
        if not _3d: fig, ax = plt.subplots()
        else:
            fig = plt.figure()     
            ax = plt.axes(projection='3d')

        # If analysis
        if analysis:
            row = self.headers.index(y_plots[0])

            # Loop through each data file
            for idx, key in enumerate(files):
                data = self.data_analysis[key]
                ax.plot(idx, data[x][row], marker="o", linestyle=linestyle, markersize=10, label=key)
                ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        else:
            # 3D graphing
            if _3d:
                # Loop through each y plot
                for key in files:          
                    data = self.data[key]
                    ax.plot3D(data[x], data[y_plots[0]], data[y_plots[1]], marker=marker, linestyle=linestyle, markersize=2, label="3D plot")

            # 2D graphing
            else:
                # Loop through each y plot
                for key in files:
                    
                    data = self.data[key]

                    for y in y_plots:
                        # Determine label
                        label = "%s - %s" % (y, key) if self.multiple else y

                        # Plot the data
                        ax.plot(data[x], data[y], marker=marker, linestyle=linestyle, markersize=2, label=label)
            
        # Get the X 
        ax.set_xlabel(self.__get_latex(x))

        # Get the Y and Z label
        if _3d:
            ax.set_ylabel(self.__get_latex(y_plots[0]))
            ax.set_zlabel(self.__get_latex(y_plots[1]))
        # Get the Y label for 2D plots
        else:
            ax.set_ylabel(self.__get_latex(y_plots))

        # Add a legend
        if (len(y_plots) > 1 and not _3d) or self.multiple:
            ax.legend()

        # Add the arguments
        if "equal" in args:
            if not _3d: ax.axis('equal')
            else:
                world_limits = ax.get_w_lims()
                ax.set_box_aspect((world_limits[1]-world_limits[0],world_limits[3]-world_limits[2],world_limits[5]-world_limits[4]))

        if "logx" in args:
            ax.set_xscale("log")
        if "logy" in args:
            ax.set_yscale("log")
        if "star" in args:
            if _3d: ax.plot3D(0, 0, 0, "*", markersize=10)
            else: ax.plot(0, 0, "*", markersize=10)
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

            # If 3d animation
            if _3d:
                point, = ax.plot3D(data[x][0], data[y_plots[0]][0], data[y_plots[1]][0], marker="o", color="black")
                points.append(point)
            
            # If 2d animation
            else:
                # Loop through the y plots
                for y in y_plots:

                    # Get the first position of the data
                    point, = ax.plot(data[x][0], data[y][0], marker="o", color="black")
                    points.append(point)

            # Create an update with some alpha value between 0 and 1
            def update (a: float):
                val = int(len(data[x]) * a)
                for idx, p in enumerate(points):
                    if _3d:
                        p.set_data(data[x][val], data[y_plots[0]][val])
                        p.set_3d_properties(data[y_plots[1]][val])
                    else:   
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