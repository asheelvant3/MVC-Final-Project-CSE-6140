# MVC-Final-Project-CSE-6140

# Dependencies
You will need the following packages to run the code. To install the packages used in this project, run the following command.
```
$ pip install networkx
$ pip install matplotlib 
$ pip install numpy
```
Python version 3.9.6 is used for the code.

# Run the executable
To run the code, please use the following commands:

python -inst <filename> -alg [bnb|approx|ls1|ls2] -time <cutoff in seconds> -seed <random seed>

seed is an optional argument, since Branch and Bound and Approx algorithms don't need to use it. 

# Directory Structure
    .
    ├── py                      # Python code files for bnb, approx and local search
    ├── output                  # Solution & Trace files for all algorithms
    └── README.md

