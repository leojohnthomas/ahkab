This electronic circuit simulator has a SPICE-like syntax.

Circuits are described in text files called _netlists_.

Each line in a netlist file is falls in one of these categories:
  * The title.
  * A element declaration.
  * A analysis declaration.
  * A comment. Comments start with `*`
  * Blank line (ignored)

**Table of Contents**


# Title #
The title is a special type of comment and it is always the first line of the file. Do not put any other directive here.

# Elements #
A element is declared with the following general syntax:

`<K><description_string> <n1> <n2> [value] [<option>=<value>] [...] ...`

Where:
  * `<K>` is a character, a unique identifier for each type of element (e.g. R for resistor)
  * `<description_string>` is a string without spaces (e.g 1)
  * `<n1>`, a string, is the node of the circuit to which the anode of the element is connected.
  * `<n2>`, a string, is the node of the circuit to which the cathode of the element is connected.
  * `[value]` if supported, is the 'value' of the element, in mks (e.g. [R1](https://code.google.com/p/ahkab/source/detail?r=1) 1 0 500k)
  * `<option>=<value>` are the parameters of the element

Nodes may have any label, without spaces, except the _reference_ _node_ which has to be 0.


## Independent sources ##

### Voltage source ###

`v<string> n1 n2 [type=vdc vdc=float] [type=vac vac=float] [type=....]`

Where the third type (if added) is one of:
  * Sinusoidal source:
`type=sin vo=<float> va=<float> freq=<float> td=<float> theta=<float>`
  * Exp. source
`type=exp v1=<float> v2=float td1=float tau1=<float> td2=<float> tau2=<float>`
  * Pulsed source
`type=pulse v1=<float> v2=<float> td=<float> tr=<float> tf=<float> pw=<float> per=<float>`


### Current source ###

`i<string> n1 n2 [type=idc idc=float] [type=iac iac=float] [type=....]`

The declaration of the time variant part is the same as stated above for voltage sources, except that `vo` becomes `io`, `va` becomes `ia` and so on.


## Linear components ##

### Resistors ###
`R<string> n+ n- <value>`

### Capacitors ###
`C<string> n+ n- <value> [ic=<float>]`

### Inductors ###
`L<string> n+ n- <value> [ic=<float>]`

### Mutual Inductors ###
Possible syntax:

`K<string> <inductor1> <inductor2> <float>`

or

`K<string> <inductor1> <inductor2> k=<float>`

More information is available in the [MutualInductors](MutualInductors.md) page.

## Dependent sources ##

### Voltage controlled voltage source (vcvs) ###
`E<string> N+ N- Ns+ Ns- <value>`

### Voltage controlled current source (vccs) ###
`G<string> N+ N- Ns+ Ns- <value>`


## Nonlinear components ##
The simulator has a few nonlinear components built-in. Others may easily be added as external modules.

### Diode ###
`D<string> N+ N- <model_id> [<AREA=float> <T=float> <IC=float> <OFF=boolean>]`



### MOS Transistor ###
`M<string> ND NG NS NB <model_id> W=<float> L=<float>`

A MOS device declaration requires:
  * ND: the drain node
  * NG: the gate node
  * NS: the source node
  * NB: the bulk node
  * model\_id: this is a string that connects this device to a .model declaration that has to be available in the netlist. The model is actually responsible of the operation of the device.
  * W: gate width, in meters
  * L: gate length, in meters

## User-defined elements ##
`Y<X> <n1> <n2> module=<module_name> type=<type> [<param1>=<value1> ...]`

Ahkab can parse user-defined elements. In order for this to work, you should write a Python module that supplies the element class. The simulator will attempt to load the module `<module_name>` and it will then look for a class named `<type>` within.

See doc(netlist\_parser.parse\_elem\_user\_defined) for further information.

## Other ##

### Subcircuit calls ###
`X<string> name=<subckt_label> [<subckt_node1>=<node_a> <subckt_node2>=<node_b> ... ]`

Insert a subcircuit, connected as specified.

All nodes in the subcircuit specification must be connected to a circuit node. The call can be placed before or after the corresponding .subckt directive.

# Device models #

## Rudimentary EKV 3.0 MOS model ##
`.model ekv <model_id> TYPE=<n/p> [TNOM=<float> COX=<float> GAMMA=<float> NSUB=<float> PHI=<float> VTO=<float> KP=<float> TOX=<float> VFB=<float> U0=<float> TCV=<float> BEX=<float>]`


The EKV model was developed by Matthias Bucher, Christophe Lallement, Christian Enz, Fabien Théodoloz, François Krummenacher at the Electronics Laboratories, Swiss Federal Institute of Technology (EPFL), Lausanne, Switzerland.

It is described here:
2.6 - http://legwww.epfl.ch/ekv/pdf/ekv_v262.pdf
3.0 - http://www.nsti.org/publications/MSM/2002/pdf/346.pdf

The authors are in no way responsible for any bug that is (very likely) present in my implementation. :)

The model is missing:
  * **channel length modulation**
  * complex mobility reduction
  * RSCE
  * transcapacitances
  * quasistatic implementation

It does identify weak, moderate and strong inversion zones, it is fully symmetrical, it treats N and P devices equally.

## Square-law MOS model ##

`.model mosq <model_id> TYPE=<n/p> [TNOM=<float> COX=<float> GAMMA=<float> NSUB=<float> PHI=<float> VTO=<float> KP=<float> TOX=<float> VFB=<float> U0=<float> TCV=<float> BEX=<float>]`

This is a square-law MOS model without velocity saturation (and second order effects like punch-through and such).

<a href='Hidden comment: 
M<string> ND NG NS KP=<float> Vt=<float> W=<float> L=<float> type=<n/p> <LAMBDA=float>
'></a>

## DIODE model ##

`.model diode <model_id> [IS=<float> N=<float> ISR=<float> NR=<float> RS=<float> CJ0=<float> M=<float> VJ=<float> FC=<float> CP=<float> TT=<float> BV=<float> IBV=<float> KF=<float> AF=<float> FFE=<float> TEMP=<float> XTI=<float> EG=<float> TBV=<float> TRS=<float> TTT1=<float> TTT2=<float> TM1=<float> TM2=<float>]`

The diode model implements the [Shockley diode equation](http://en.wikipedia.org/wiki/Shockley_diode_equation#Shockley_diode_equation). Currently the capacitance modeling part is missing.

The most important parameters are:

| **Parameter** | **Default value** | **Description** |
|:--------------|:------------------|:----------------|
| IS | 1e-14  A | Specific current |
| N | 1.0 | Emission coefficient |
| ISR | 0.0 A | Recombination current |
|NR | 2.0 | Recombination coefficient |
| RS | 0.0 ohm | Series resistance per unit area |

please refer to the SPICE documentation and the `diode.py` file for the others.

# Types of analyses #


## Operating point (OP) ##
`.op [guess=<ic_label>]`

This analysis tries to find a DC solution through a pseudo Newthon Rahpson (NR) iteration method. Notice that a non-linear circuit may have zero, a discrete number or infinite OPs.

Which one is found depends on the circuit and on the initial guess supplied to the method.
The program has a built in method that tries to generate a "smart" initial guess to speed up convergence. When that fails, or is disabled from command line (see --help), the initial guess is set to all zeros.

The user may supply a better guess, if known. This can be done adding a .ic directive somewhere in the netlist file and setting `guess=<ic_label>` where `<ic_label>` matches the .ic's `name=<ic_label>`.

The t=0 value is automatically added as dc value to every time-variant independent source without a explicit dc value.


## DC sweep ##
`.DC src=<src_name> start=<float> stop=<float> step=<float> type=<linear/log>`

Performs a DC sweep (repeated OP analysis with the value of a voltage or current source changing at every iteration).

Parameters:
  * src: the id of the source to be swept (V12, Ibias...). Only independent current and voltage sources.
  * start: start value.
  * stop: stop value.
  * type: either "linear" or "log"
  * step: sets the value of the source from an iteration (k) to the next (k+1):
    * if type=log, S(k+1) = S(k) `*` step
    * if type=linear, S(k+1) = S(k) + step

## Transient analysis ##
`.TRAN TSTEP=<float> TSTOP=<float> [TSTART=<float>  UIC=0/1/2/3 [IC_LABEL=<string>] METHOD=<string>]`

Performs a transient analysis from tstart (which defaults to 0) to tstop, using the step provided as initial step and the method specified (if any, otherwise defaults to implicit\_euler).

Parameters:
  * tstart: the starting point, defaults to zero.
  * tstep: this is the initial step. By default, the program will try to adjust it to keep the estimate error within bounds.
  * tstop: Stop time.
  * UIC (Use Initial Conditions): This is used to specify the state of the circuit at time t=tstart. Available values are 0/1/2/3
    * uic=0: all node voltages and currents through v/h/e/sources will be assumed to be zero at t=tstart
    * uic=1: the status at t=tstart is the last result from a OP analysis.
    * uic=2: the status at t=tstart is the last result from a OP analysis on which are set the values of currents through inductors and voltages on capacitors specified in their ic. This is done very roughly, checking is recommended.
    * uic=3: Load a user supplied ic. This requires a .ic directive somewhere in the netlist and a .ic's name and ic\_label must match.
  * method: the integration method to be used in transient analysis. Built-in methods are: implicit\_euler, trap, gear2, gear3, gear4, gear5 and gear6. Defaults to implicit\_euler. May be overriden by the value specified on the command line with the option: -t METHOD or --tran-method=METHOD.

High order methods are slower per iteration, but they often can afford a longer step with comparable error, hence they are actually faster in many cases.

If a transient analysis stops because of a step size too small, use a low order method (ie/trap) and set --t-max-nr to a high value (eg 1000).

## AC ##
`.AC start=<float> stop=<float> nsteps=<integer>`

Performs an AC analysis.

If the circuit is non-linear, a successful Operating Point (OP) is needed to linearize the circuit.

The sweep type is by default (and currently unchangeable) logarithmic.

Parameters:
  * start: the starting _angular_ _frequency_ of the sweep.
  * stop: the final angular frequency
  * nsteps: the number of steps to be executed

## Shooting ##
`.SHOOTING period=n [points=n step=n method=<string> autonomous=bool]`

This analysis tries to find the periodic steady state (PSS) solution of the circuit.

Parameters:
  * period: the period of the solution. To be specified only in not autonomous circuits (which are somehow clocked).
  * points: How many time istants use to discretize the solution. If step is set, this is automatically computed.
  * step: Time step on the period. If points is set, this is automatically computed.
  * method: the PSS algorithm to be employed. Options are: shooting (default) and brute-force.
  * autonomous: self-explanatory boolean. If set to true, currently the simulator halts, autonomous circuits are not supported.

## Symbolic small-signal and Transfer function ##

`.symbolic [tf=<source_name> ac=bool]`

  * tf: If the source is specified, all results are differentiated with respect to the source value (transfer functions).
  * ac: If set to True, capacitors and inductors will be included. Defaults to False.

Performs a small-signal analysis of the circuit, optionally including AC elements (slows down the solution). In the results, the imaginary unit is shown as `I`, the angular frequency as `w`.

Results are printed to stdout.

We rely on the sympy library for symbolic computations. The library is under development and might have trouble (or take a long time) with medium-big netlists. Improvements are on their way.

# Other directives #

## End ##
`.end`

Force the parser to stop reading the netlist. Everything after this line is disregarded.

## Ends ##
`.ends`

Closes a subcircuit block.

## Ic ##
`.ic name=<ic_label> [v<node>=<value> i<element_name>=<value> ... ]`

This allows the specification of a state of a circuit. Every node voltage or current (through appropriate elements) may be specified. If not set, it will be set to 0.
Notice that setting a inappropriate or inconsistent ic will create convergence problems.

To use a ic in a transient analysis, set '`UIC=3`' and '`IC_LABEL=<ic_label>`'.

## Include ##
`.include <filename>`

Include a file. It's equivalent to copy & paste the contents of the file to the bottom of the netlist.

## Subckt ##
`.subckt <subckt_label> [node1 node2 ... ]`

Subcircuits are netlist block that may be called anywhere in the circuit using a subckt call. They can have other subckt calls within - but beware of recursively calling the same subcircuit!

They can hold other directives, but the placement of the directive doesn't change its meaning (ie if you add a .op line in the subcircuit or outside of it it's the same).

They can't be nested and have to be ended by a `.ends` directive.

## Plot ##
`.plot <simulation_type> [variable1 variable2 ... ]`

Parameters:
  * simulation\_type: the which simulation will have the data plotted. Currently the available options are tran, shooting and dc.
  * variableN might be:
  * a voltage, syntax `V(<node>)` or `V(<node2>, <node1>)`, the second will plot the difference of the node voltages. Eg `V(in)` or `V(2,1)`.
  * a current, syntax `I(<source name>)`, eg. `I(V2)` or `I(Vsupply)`