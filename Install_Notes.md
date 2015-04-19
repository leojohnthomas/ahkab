# Install Notes #

## Requirements ##
The program requires the **Python** interpreter (version 2: at least v. 2.6, also see `[0]`), **numpy**, **matplotlib** and **sympy**.

[Numpy](http://numpy.scipy.org/) is needed for all the numeric computations. On a Debian system, python and numpy may be installed running:

> `# aptitude install python python-numpy`

Plotting requires [matplotlib](http://matplotlib.sourceforge.net/):

> `# aptitude install python-matplotlib`

The symbolic analysis capabilities rely on [sympy](http://code.google.com/p/sympy/). Any version of sympy will do if you are interested only in numeric simulations, but, if you run symbolic simulations, **sympy version 0.7.3 or higher** is needed.

> `# aptitude install python-sympy`

`[0]` Python 3 is currently unsupported, but since all the dependencies support it, porting is possible, albeit it has a low priority for the time being.


## Install ##
No packages are available now. The project is hosted on a Subversion server: to run ahkab, check out the code [as explained here](http://code.google.com/p/ahkab/source).

If you don't have [subversion](http://subversion.tigris.org/) already installed:

> `# aptitude install subversion`

## Runtime ##
ahkab can be run from the command line or inside a python script. See the wiki for more information.

A typical command line is:

> `$ ahkab -o graph.dat <netlist file>`

See `ahkab --help` for command line switches.

## Thanks ##

Many thanks to the developers of the above libraries, their effort made this project possible. :)