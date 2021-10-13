# N-Body Code :apple:

This repository aims to create an **N-body** code for simulating test particles in a system. Currently, it is developed for a Monash University project in ASP3012 - Stars and Galaxies. It aims to simulate particles in a galaxy colliding with each other. It is a simple experiment and makes use of simple integrators in Python.

This code is currently unfinished and being worked on. All **Lab 12** questions can be found in the `lab-12` folder. Please make sure you are on the **lab-12** branch to see all the code that was submitted prior to this submission of the lab. DO NOT USE the **master** branch as this may have newer code that does not apply for the **Lab 12** code.

### Setup :scroll:

To install the repository, use the *git* command line:

```
git clone https://github.com/harrisonv789/N-body_code.git
cd N-body_code
```

If running the **Lab 12** code, make sure to check out the correct branch:

```
git checkout lab-12 --
git pull
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

To run the Lab 12 code for each of the questions, run the following code:
```
cd lab-12
python3 q4.py
```
