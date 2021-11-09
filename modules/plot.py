# Import relevant packages
import numpy as np
import os
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation
from mpl_toolkits import mplot3d
from numpy.lib.function_base import diff
from .color import Color
from .analysis import Analysis
from matplotlib import rc         # These are some default settings we will use
rc('animation', html='jshtml')    # jshtml is required for plotting in the browser

# Create a class for a plotter
class Plotter:

    # Output files
    outputs = []

    # Store the data as a dictionary
    data = {}
    data_analysis = {}

    # Store a list of standard plots
    preset_plots = {
        "body": {
            "pos":          ["pos_x",   "pos_y",                        {"equal": True, "star": True, "animate": True, "is3d": False}],
            "3d":           ["pos_x",   "pos_y, pos_z",                 {"equal": False, "star": True, "animate": True, "is3d": True}],
            "energy":       ["time",    "E_tot, E_kin, E_pot, E_err",   {}],
            "timepos":      ["time",    "pos_x, pos_y, pos_z",          {}],
            "galaxy_top":   ["pos_x",   "pos_y",                        {"equal": True, "animate": True, "is3d": False, "legend": False, "lines": False, "limits": True, "limits_x": 80, "limits_y": 80}],
            "galaxy_side":  ["pos_x",   "pos_z",                        {"equal": True, "animate": True, "is3d": False, "legend": False, "lines": False, "limits": True, "limits_x": 80, "limits_y": 80}],
            "galaxy_3d":    ["pos_x",   "pos_y, pos_z",                  {"equal": True, "animate": True, "is3d": True, "legend": False, "lines": False, "limits": True, "limits_x": 80, "limits_y": 80}],
        },
        "cluster": {
            "mom":      ["time",    "mom_x, mom_y, mom_z",          {}],
            "energy":   ["time",    "E_tot, E_kin, E_pot, E_err",   {}],
        },
        "system": {
            "mom":      ["time",    "mom_x, mom_y, mom_z",          {}],
            "energy":   ["time",    "E_tot, E_kin, E_pot, E_err",   {}],
        }
    }

    # Init constructor takes in some output data file and some arguments
    def __init__ (self, **kwargs):

        # Store references to the outputs
        self.outputs = kwargs.get("outputs", [])
        self.dir = kwargs.get("dir", "output/")
        self.multiple = len(self.outputs) > 1
        self.analysis = kwargs.get("analysis", False) and self.multiple
        self.option = "output files"

        # If no output specified, get the data from system or from bodies
        if len(self.outputs) == 0 and len(os.listdir(self.dir)) > 0:
            # If multiple files found
            if len(os.listdir(self.dir)) > 1:

                print("\nMultiple data files detected.")

                # Loop untit a valid option entered
                while True:

                    # Get the new option
                    option = input("Plotting Data File\n\tOptions = %s(B)odies, (C)luster, (S)ystem%s: " \
                        % (Color.DEFAULT, Color.RESET)).lower()
                    
                    # If using a system option
                    if option == "s":
                        self.option = "system"
                        self.outputs = [self.dir + file for file in os.listdir(self.dir) if "system" in file]
                        break

                    # If using a system option
                    if option == "c":
                        self.option = "cluster"

                        self.outputs = [self.dir + file for file in os.listdir(self.dir) if "cluster" in file]

                        # Check for only one cluster
                        if len(self.outputs) == 1: break
                        
                        # Ask for the cluster to plot
                        cluster_idx = input("Select a Cluster [%s%d, %d%s]: " \
                            % (Color.DEFAULT, 0, len(self.outputs) - 1, Color.RESET)).lower()

                        # Check if only one cluster is selected
                        if cluster_idx.isdigit() and int(cluster_idx) < len(self.outputs):
                            self.outputs = [self.outputs[int(cluster_idx)]]

                        break

                    # If using the body option
                    if option == "b":
                        self.option = "body"

                        self.outputs = [self.dir + file for file in os.listdir(self.dir) if "body" in file and "analysis" not in file]

                        # Check for only one body
                        if len(self.outputs) == 1: break
                        
                        # Ask for the body to plot
                        body_idx = input("Select a Body [%s%d, %d%s]: " \
                            % (Color.DEFAULT, 0, len(self.outputs) - 1, Color.RESET)).lower()

                        # Check if only one body is selected
                        if body_idx.isdigit() and int(body_idx) < len(self.outputs):
                            self.outputs = [self.outputs[int(body_idx)]]

                        break

                    # If quitting
                    if option == "q":
                        exit()

            # Otherwise set the one file
            else:
                self.outputs = self.dir + os.listdir(self.dir)[0]

        # Load the data
        self.load_data()

        # Gets the options from the output file
        with open(self.outputs[0], "r") as file:
            self.headers = [h.strip() for h in file.readline().strip().split(" ") if h != ""]

        # Get name of the header
        header = ", ".join(self.outputs).replace(self.dir, "") if len(self.outputs) < 4 else self.option + ".dat"

        # Print the header
        print("\n--------------------------------------------------")
        print("%sPLOTTING DATA FROM %s%s" % (Color.HEADER, header, Color.RESET))
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

        # Whether to repeat from start again
        back = False

        # Loop while plotting
        while True:
            print("\n---")

            # Ask for a preset
            preset = input("\nPreset Plot\n\tOptions = %s%s%s: " \
                % (Color.DEFAULT, ", ".join(self.preset_plots[self.option].keys()), Color.RESET)).lower()

            # Check for quit
            if preset == "q": break

            # Check for back
            if preset == "b":
                back = True
                break
            
            # Check if has a valid plot
            if preset in self.preset_plots[self.option].keys():
                previous = self.preset_plots[self.option][preset]

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
                self.plot(x_axis, [y_axis], analysis=True)
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

            # Convert the params to previous
            previous[2] = self.params_string(previous[2])

            # Get extra parameters
            params = input("\nGraphing %sparameters%s (space separated)\n\tPrevious = %s%s%s: " \
                % (Color.INPUT, Color.RESET, Color.DEFAULT, previous[2] if previous[2] != "" else "None", Color.RESET))

            # If missing parameters or quitting
            if params.lower() == "q": break
            if params.lower() == "": params = previous[2]

            # Get the params dictionary
            params = self.get_params(params)
            
            # Make a plot with the parameters
            self.plot(x_axis, y_axis, **params)
            previous = [x_axis, ", ".join(y_axis), params]

        # If starting again
        if back: 
            self.__init__()
            self.ask_plot()


    # Converts parameters to string
    def params_string (self, params: dict) -> str:
        if params == "": return ""
        args = []
        for arg in params.keys():
            args.append("%s=%s" % (arg, str(params[arg])))
        
        if len(args) > 0:
            return ", ".join(args)
        return ""


    # Converts some strings into params
    def get_params (self, string: str) -> dict:
        args = string.split(",")
        params = {}

        for arg in args:
            if "=" in arg:
                arg = arg.replace(" ","").split("=")

                # Convert to values
                
                if arg[1].lower() in ("t", "f", "true", "false"): arg[1] = arg[1][0].lower() == "t"
                elif arg[1].isdigit: arg[1] = int(arg[1])
                elif arg[1].isdecimal: arg[1] = float(arg[1])

                # Add to the params
                params[arg[0].lower()] = arg[1]

        return params



    ##########################################################################
    # PLOTTING DEFAULTS VALUES
    ##########################################################################

    defaults = {
        # Analyis
        "analysis": False,

        # Markers and lines Style
        "marker": "o",
        "marker_size": 3,
        "marker_color": "black",
        "lines": True,
        "linestyle": "solid",
        "star": False,

        # Axis properties
        "twin_axis": False,
        "equal": False,
        "log_x": False,
        "log_y": False,

        # Graph properties
        "grid": True,
        "title": "",

        # 3D properties
        "is3d": False,

        # Legend properties
        "legend": True,

        # Animation properties
        "animate": True,
        "interval": 100,
        "save": None,
        "fps": 15,
        "time_factor": 1,
        "show": True,

        # Limits
        "limits": False,
        "limits_x": 2,
        "limits_y": 2,
        "limits_x_min": None,
        "limits_y_min": None,
        "limits_x_max": None,
        "limits_y_max": None,
    }

    ##########################################################################
    # PLOTTING FUNCTION
    ##########################################################################

    # Makes a simple plot
    def plot (self, x, y_plots, files = [], **kwargs):

        # Update the kwargs and reset with defaults first
        self.__dict__.update(self.defaults)
        self.__dict__.update(kwargs)

        # Check if y plots is a string and not list
        if type(y_plots) is str:
            y_plots = [y_plots]

        # If files is empty
        if files == []:
            files = self.data.keys()

        # Will set a 3D graph if it is an argument and 2 Y values are used (the second for Z)
        _3d = self.is3d and len(y_plots) == 2 and not self.analysis

        # Create the subplots
        if not _3d: fig, ax = plt.subplots()
        else:
            fig = plt.figure()     
            ax = plt.axes(projection='3d')

        # In the case of multiple axis
        if self.twin_axis: ax2 = ax.twinx()

        # If analysis
        if self.analysis:
            row = self.headers.index(y_plots[0])

            # Loop through each data file
            for idx, key in enumerate(files):
                data = self.data_analysis[key]
                ax.plot(idx, data[x][row], marker="o", linestyle=self.linestyle, markersize=self.marker_size, label=key, color=self.marker_color)
                ax.tick_params(axis='x', which='both', bottom=False, top=False, labelbottom=False)

        elif not self.animate:
            # 3D graphing
            if _3d:
                # Loop through each y plot
                for key in files:          
                    data = self.data[key]
                    ax.plot3D(data[x], data[y_plots[0]], data[y_plots[1]], marker=self.marker, linestyle=self.linestyle, markersize=2, label="3D plot")

            # 2D graphing
            else:
                # Loop through each y plot
                for key in files:
                    
                    data = self.data[key]

                    for idx, y in enumerate(y_plots):
                        # Determine label
                        label = "%s - %s" % (y, key) if self.multiple else y

                        # Plot the data
                        if idx == 0 or not self.twin_axis:
                            ax.plot(data[x], data[y], marker=self.marker, linestyle=self.linestyle, markersize=2, label=label)
                        else: ax2.plot(data[x], data[y], marker=self.marker, linestyle=self.linestyle, markersize=2, label=label, color='orange')
        
        # Get the X 
        ax.set_xlabel(self.__get_latex(x))

        # Get the Y and Z label
        if _3d:
            ax.set_ylabel(self.__get_latex(y_plots[0]))
            ax.set_zlabel(self.__get_latex(y_plots[1]))
        # Get the Y label for 2D plots
        else:
            if self.twin_axis:
                ax.set_ylabel(self.__get_latex(y_plots[:1]))
                ax2.set_ylabel(self.__get_latex(y_plots[1:]))
            else:
                ax.set_ylabel(self.__get_latex(y_plots))

        # Add a legend
        if self.legend and (len(y_plots) > 1 and not _3d) or self.multiple:
            ax.legend()
            if self.twin_axis:
                ax2.legend()

        # Set the axis properties
        self.set_axis_properties(ax)

        # Animate the system
        if self.animate:

            # Create an update with some alpha value between 0 and 1
            def update (a: float):
                ax.clear()
                data_len = len(self.data[list(files)[0]][x])
                val = min(data_len - 1, int(data_len * a))
                for p_idx, key in enumerate(files):
                    for idx, y in enumerate(y_plots):
                        label = "%s - %s" % (y, key) if self.multiple else y
                        x_data = self.data[key][x]
                        y_data = self.data[key][y_plots[idx]]
                        if _3d:
                            z_data = self.data[key][y_plots[1]]
                            # Add the previous positions
                            if self.lines: ax.plot3D(x_data[:val], y_data[:val], z_data[:val], marker=self.marker, linestyle=self.linestyle, markersize=1, label=label, alpha=0.7)
                            # Add the current position
                            ax.plot3D(x_data[val], y_data[val], z_data[val], marker="o", color=self.marker_color, markersize=self.marker_size)
                        else:
                            # Add previous positions
                            if self.lines: ax.plot(x_data[:val], y_data[:val], marker=self.marker, linestyle=self.linestyle, markersize=1, label=label, alpha=0.7)
                            # Add the current position
                            ax.plot(x_data[val], y_data[val], marker="o", color=self.marker_color, markersize=self.marker_size)
                
                # Set the axis properties
                self.title = "Timestep: %.1f" % (float(val) * float(self.time_factor))
                self.set_axis_properties(ax)
                

                # Set the X and Y lable
                ax.set_xlabel(self.__get_latex(x))
                ax.set_ylabel(self.__get_latex(y_plots[0]))

                # Get the Y and Z label
                if _3d:
                    ax.set_zlabel(self.__get_latex(y_plots[1]))

            # Create the animation call
            self.anim = FuncAnimation(fig, update, repeat=True, frames=np.linspace(0, 1.0, self.interval, endpoint=True))

            if self.save != None:
                print("%s\nSaving Animation. Please wait...%s" % (Color.WARNING, Color.END))
                self.anim.save(self.save, fps=self.fps, extra_args=['-vcodec', 'libx264'])
                print("Animation saved %ssuccessfully%s to %s" % (Color.SUCCESS, Color.END, self.save))

        # Otherwise if saving image
        elif self.save != None:
            fig.savefig(self.save)
            print("Image saved %ssuccessfully%s to %s" % (Color.SUCCESS, Color.END, self.save))

        # Show the plot
        if self.show:
            plt.show()


    # Set the axis properties
    def set_axis_properties (self, ax):
        ax.set_title(self.title)

        # Show the legend
        if self.legend: ax.legend()

        # Add the arguments
        if self.equal:
            if self.is3d:
                world_limits = ax.get_w_lims()
                ax.set_box_aspect((world_limits[1]-world_limits[0],world_limits[3]-world_limits[2],world_limits[5]-world_limits[4]))
            else: ax.axis('equal')
                
        if self.log_x: ax.set_xscale("log")
        if self.log_y: ax.set_yscale("log")
        if self.star:
            if self.is3d: ax.plot3D(0, 0, 0, "*", markersize=10, color="yellow")
            else: ax.plot(0, 0, "*", markersize=10, color="yellow")
        if self.grid: ax.grid()

        # Set the range of limits
        if self.limits:

            # X Limits
            if self.limits_x_min != None and self.limits_x_max != None: ax.set_xlim(self.limits_x_min, self.limits_x_max)
            elif self.limits_x != None: ax.set_xlim(-self.limits_x, self.limits_x)

            # Y Limits
            if self.limits_y_min != None and self.limits_y_max != None: ax.set_ylim(self.limits_y_min, self.limits_y_max)
            elif self.limits_y != None: ax.set_ylim(-self.limits_y, self.limits_y)



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