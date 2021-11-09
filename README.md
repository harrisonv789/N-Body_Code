# N-Body Code :apple:

This repository aims to create an **N-body** code for simulating test particles in a system. Currently, it is developed for a Monash University project in ASP3012 - Stars and Galaxies. It aims to simulate particles in a galaxy colliding with each other. It is a simple experiment and makes use of simple integrators in Python.

At this stage, the code is in a working version and is able to simulate point masses, background potential functions (including Kepler, Logarithmic, Isochrone and Oscillator) and collisions between clusters or even galaxies. This README will outline the steps to use the module and create your own simulations, however, it is recommended that the example code located in the *examples* folder is looked at and used as a base to develop new simulations.

### Setup :scroll:

To install the repository, use the *git* command line:

```
git clone https://github.com/harrisonv789/N-body_code.git
cd N-body_code
```

Make sure the following Python3 packages are installed:

```
pip3 install matplotlib
pip3 install numpy
```

To run the N-body code, run the following line inside the project directory:
```
./main.py
```

To run the example simulations:
```
cd examples
./example_galaxy.py
```

### Examples :book:

1. **Collision**:
    This example simulates the collision of two galaxies, each with 120 point particles. This particular collision models the M51 galaxies, simulated over a long timeframe. This simulation will take over 10 minutes to run, just because the amount of points that need to be computed, but show how to use multiple galaxies.
<br>

2. **Galaxies**:
    This example simulates a galaxy and shows how to connect galaxy initial conditions to a cluster. Each of the point particles in the galaxy are massless and follow the central bulge of the galaxy. This simulation rotates the particles around the centre of mass.
<br>

3. **Logarithmic Potential**:
    This example uses a single mass orbiting a background potential. In this case, it uses a logarithmic potential, as modelled by a globular cluster and the orbiting mass has a epicyclic frequency of 3/2 times the angular frequency.
<br>

4. **Three Body**:
    This simulation uses three bodies in a stable figure-8 orbit. It shows how to set up clusters with small numbers of particles and how to use the initial conditions to set up specific orbits for certain objects. See the *initial_conditions.py* file for more initial condition set ups.
<br>

5. **Two Body**:
    A simple two body problem with two masses of different masses orbiting each other in a stable orbit. This is a simple simulation which shows how to use clusters and specific initial conditions.


### Graphing :chart:

Each simulation can be plotted. Plots can be configured in code using the plotter, or the terminal based plotting interface can be toggled using the `ask_plot()` function. Depending on the simulation, users will be able to plot properties from all the bodies of the simulation (pressing 0 will show all bodies and not just specific ones), all bodies from a cluster and all simulation properties.

Once the data has been seleced, it is possible to plot particular properties from the simulation. The following properties are recorded for each of the bodies:

- time
- position (x, y, z)
- velocity (x, y, z)
- acceleration (x, y, z)
- radius
- theta
- momentum (x, y, z)
- mass
- energy total
- energy kinetic
- energy potential
- energy error

There are also a set of preset options available which will set up the plot selection for the x and y axis, along with some parameters. All parameters (along with the default parameter) that are available are shown below:

- analysis: False
- marker: "o"
- marker_size: 3
- marker_color: "black"
- lines: True
- linestyle: "solid"
- star: False
- twin_axis: False
- equal: False
- log_x: False
- log_y: False
- grid: True
- title: ""
- is3d: False
- legend: True
- animate: True
- interval: 100
- save: None
- fps: 15
- time_factor: 1
- show: True
- limits: False
- limits_x: 2
- limits_y: 2
- limits_x_min: None
- limits_x_max: None
- limits_y_min: None
- limits_y_max: None

These parameters can be found in the *plot.py* script. Additionally, multiple y axis plots can be used, by separating each axis with a comma.