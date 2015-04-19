# Introduction #

Interacting with ahkab inside a python program gives the user the ability to employ the extreme flexibility and power of Python.

This page gives an (incomplete) example showing how to do it. More can be found in `help(circuit.circuit)`.

**Notice this code is still experimental.**

## Updates ##
  * Dec 19, 2011 - rev. 0
  * Dec 20, 2011 - rev. 0.1b
  * Jan 5, 2011 - rev. 0.1c
  * Aug 10, 2013 - rev. 0.1d
  * Aug 20, 2013 - rev 0.1e


# Example #

Let's say we would like to simulate the AC characteristics and the step response of a Butterworth low pass filter, such as this:

![http://ahkab.googlecode.com/svn/wiki/images/library/example_circuit.jpg](http://ahkab.googlecode.com/svn/wiki/images/library/example_circuit.jpg)

This example is example 7.4 in from Hercules G. Dimopoulos, _Analog Electronic Filters: Theory, Design and Synthesis_, Springer.

The code to describe the circuit is the following:

First import the modules and create a new circuit:

```
import ahkab
import circuit, printing, devices

mycircuit = circuit.circuit(title="Butterworth Example circuit")
```

Elements are to be connected to _nodes_. There is one special node, the reference (gnd):

```
import ahkab
from ahkab import circuit, printing, devices
mycircuit = circuit.circuit(title="Butterworth Example circuit")

gnd = mycircuit.get_ground_node()
```

and ordinary nodes.

Ordinary nodes can be defined as:
```
import ahkab
from ahkab import circuit, printing, devices
mycircuit = circuit.circuit(title="Butterworth Example circuit")
# use arbitrary strings to describe the nodes
# like this:
n1 = 'n1'
# or like this, 
# the helper function create_node() will check that this is not a
# node name that was used somewhere else in your circuit
n1 = mycircuit.create_node('n1')
```

Then you can use the nodes you have defined to add your elements to the circuit. The circuit instance provides convenient helper functions.

You can use any of these styles:

```
import ahkab
from ahkab import circuit, printing, devices
mycircuit = circuit.circuit(title="Butterworth Example circuit")
# first option: define the new nodes and add to the circuit using 
# positional arguments
n1 = mycircuit.create_node("n1")
n2 = mycircuit.create_node("n2")
mycircuit.add_resistor("R1", n1, n2, 600.)
# or add directly to the circuit (better double check the node names in big circuits) using keyword args:
mycircuit.add_resistor(name="R1", ext_n1="n1", ext_n2="n2", R=600)
```

Using the second style, the passives in example 7.4 can be added as:

```
import ahkab
from ahkab import circuit, printing, devices
mycircuit = circuit.circuit(title="Butterworth Example circuit")

gnd = mycircuit.get_ground_node()

mycircuit.add_resistor(name="R1", ext_n1="n1", ext_n2="n2", R=600)
mycircuit.add_inductor(name="L1", ext_n1="n2", ext_n2="n3", L=15.24e-3)
mycircuit.add_capacitor(name="C1", ext_n1="n3", ext_n2=gnd, C=119.37e-9)
mycircuit.add_inductor(name="L2", ext_n1="n3", ext_n2="n4", L=61.86e-3)
mycircuit.add_capacitor(name="C2", ext_n1="n4", ext_n2=gnd, C=155.12e-9)
mycircuit.add_resistor(name="R2", ext_n1="n4", ext_n2=gnd, R=1.2e3)
```

Next, we want to add the voltage source V1.

  * First, we define a pulse function to provide the time-variable characteristics of V1, to be used in the transient simulation: `voltage_step = devices.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)`

  * Then we add a voltage source named V1 to the circuit, with the time-function we have just built: `mycircuit.add_vsource(name="V1", ext_n1="n1", ext_n2=gnd, vdc=5, vac=1, function=voltage_step)`

Putting all together:

```
voltage_step = devices.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)
mycircuit.add_vsource(name="V1", ext_n1="n1", ext_n2=gnd, vdc=5, vac=1, function=voltage_step)
```

We can now check that the circuit is defined as we intended, generating a netlist.

```
printing.print_circuit(mycircuit)
```

If you invoke python now, you should get an output like this:

```
* TITLE: Butterworth Example circuit
R1 n1 n2 600
L1 n2 n3 0.01524
C1 n3 0 1.1937e-07
L2 n3 n4 0.06186
C2 n4 0 1.5512e-07
R2 n4 0 1200.0
V1 n1 0 type=vdc vdc=5 vac=1 arg=0 type=pulse v1=0 v2=1 td=5e-07 per=2 tr=1e-12 tf=1e-12 pw=1
(analysis directives are omitted)
```

Next, we need to define the analyses to be carried out:

```
op_analysis = {"type":"op", "guess_label":None}
ac_analysis = {"type":"ac", "start":1e3, "stop":1e5, "nsteps":100}
tran_analysis = {"type":"tran", "tstart":0, "tstop":1.2e-3, "tstep":1e-6, "uic":0, "method":None, "ic_label":None}
```

Next, we process the analyses with verbosity set to zero:

```
r = ahkab.process_analysis(an_list=[op_analysis, ac_analysis, tran_analysis], circ=mycircuit, outfile="script_output", verbose=0, cli_tran_method=None, guess=True, disable_step_control=False)
```

Since the output filename has been set to `script_output`, three files will be generated in your working directory: `script_output.ac  script_output.op  script_output.tran`. Inside each one there are the results for the respective simulations.

Save the script to a file and start python in interactive model with:

`python -i script.py`

All results where saved in a variable 'r'. Let's take a look at the OP results:

```
>>> r
`{'ac': <results.ac_solution instance at 0xb57e4ec>, 'op': <results.op_solution instance at 0xb57e4cc>, 'tran': <results.tran_solution instance at 0xb57e4fc>}`

>>> dir(r['op'])
['__contains__', '__doc__', '__getitem__', '__init__', '__iter__', '__len__', '__module__', '__str__', 'asmatrix', 'errors', 'filename', 'get', 'get_elements_op', 'get_table_array', 'get_type', 'gmin', 'gmin_check', 'has_key', 'iea', 'ier', 'items', 'iterations', 'keys', 'netlist_file', 'netlist_title', 'next', 'op_info', 'print_short', 'results', 'skip_nodes_list', 'temp', 'timestamp', 'units', 'values', 'variables', 'vea', 'ver', 'write_to_file', 'x']

>>> r['op'].results
{'VN4': 3.3333333333333335, 'VN3': 3.3333333333333335, 'VN2': 3.3333333333333335, 'I(L1)': 0.0027777777777777779, 'I(V1)': -0.0027777777777777779, 'I(L2)': 0.0027777777777777779, 'VN1': 5.0}
```

You can get all the available variables calling the keys() method:

```
>>> r['op'].keys()
['VN1', 'VN2', 'VN3', 'VN4', 'I(L1)', 'I(L2)', 'I(V1)']
>>> r['op']['VN4']
3.3333333333333335
```

Then you can access the data through the dictionary interface, eg:

```
>>> "The DC output voltage is %s %s" % (r['op']['VN4'] , r['op'].units['VN4'])
'The DC output voltage is 3.33333333333 V'
```

A similar interface is available for the AC simulation results:

```
>>> dir(r['ac'])
['__contains__', '__doc__', '__getitem__', '__init__', '__iter__', '__len__', '__module__', '__str__', '_init_file_done', 'add_line', 'filename', 'get', 'get_type', 'gmin', 'has_key', 'iea', 'ier', 'items', 'keys', 'linearization_op', 'netlist_file', 'netlist_title', 'next', 'opoints', 'ostart', 'ostop', 'skip_nodes_list', 'stype', 'temp', 'timestamp', 'units', 'values', 'variables', 'vea', 'ver']
>>> print(r['ac'])
<AC simulation results for Butterworth Example circuit (netlist None). LOG sweep, from 1000 Hz to 100000 Hz, 100 points. Run on 2011-12-19 17:24:29, data filename script_output.ac.>
>>> r['ac'].keys()
['#w', '|Vn1|', 'arg(Vn1)', '|Vn2|', 'arg(Vn2)', '|Vn3|', 'arg(Vn3)', '|Vn4|', 'arg(Vn4)', '|I(L1)|', 'arg(I(L1))', '|I(L2)|', 'arg(I(L2))', '|I(V1)|', 'arg(I(V1))']
```

A similar approach can be used to access the TRAN data set.

The data can be plotted through matplotlib, for example:

```
import pylab

fig = pylab.figure()
pylab.title(mycircuit.title + " - TRAN Simulation")
pylab.plot(r['tran']['T'].T, r['tran']['VN1'].T, label="Input voltage")
pylab.hold(True)
pylab.plot(r['tran']['T'].T, r['tran']['VN4'].T, label="output voltage")
pylab.legend()
pylab.hold(False)
pylab.grid(True)
pylab.ylim([0,1.2])
pylab.ylabel('Step response')
pylab.xlabel('Time [s]')
fig.savefig('tran_plot.png')

fig = pylab.figure()
pylab.subplot(211)
pylab.semilogx(r['ac']['w'].T, r['ac']['|Vn4|'].T, 'o-')
pylab.ylabel('abs(V(n4)) [V]')
pylab.title(mycircuit.title + " - AC Simulation")
pylab.subplot(212)
pylab.grid(True)
pylab.semilogx(r['ac']['w'].T, r['ac']['arg(Vn4)'].T, 'o-')
pylab.xlabel('Angular frequency [rad/s]')
pylab.ylabel('arg(V(n4)) [rad]')
fig.savefig('ac_plot.png')
pylab.show()
```

The previous code generates the following plots:

![http://ahkab.googlecode.com/svn/wiki/images/library/tran_plot.png](http://ahkab.googlecode.com/svn/wiki/images/library/tran_plot.png)

![http://ahkab.googlecode.com/svn/wiki/images/library/ac_plot.png](http://ahkab.googlecode.com/svn/wiki/images/library/ac_plot.png)

It is also possible to extract attenuation in pass-band (0-2kHz) and stop-band (6.5kHz and up).

The problem is that the voltages/currents we are looking for may not have been evaluated by ahkab at the desired points. This can be easily overcome with interpolation through scipy.

Here is a snippet of code to evaluate the attenuation is pass-band and stop band in the example:

```
import scipy, numpy, scipy.interpolate 

# Normalize the output to the low frequency value and convert to array
norm_out = numpy.asarray(r['ac']['|Vn4|'].T/r['ac']['|Vn4|'].max())
# Convert to dB
norm_out_db = 20*numpy.log10(norm_out)
# Reshape to be scipy-friendly
norm_out_db = norm_out_db.reshape((max(norm_out_db.shape), ))
# Convert angular frequencies to Hz and convert matrix to array
frequencies = numpy.asarray(r['ac']['w'].T/2/math.pi)
# Reshape to be scipy-friendly
frequencies = frequencies.reshape((max(frequencies.shape), ))
# call scipy to interpolate
norm_out_db_interpolated = scipy.interpolate.interp1d(frequencies, norm_out_db)

print "Maximum attenuation in the pass band (0-%g Hz) is %g dB" % \
(2e3, -1.0*norm_out_db_interpolated(2e3))
print "Minimum attenuation in the stop band (%g Hz - Inf) is %g dB" % \
(6.5e3, -1.0*norm_out_db_interpolated(6.5e3))
```

You should see the following output:

```
Maximum attenuation in the pass band (0-2000 Hz) is 0.351373 dB
Minimum attenuation in the stop band (6500 Hz - Inf) is 30.2088 dB
```

[Download the python file.](http://ahkab.googlecode.com/svn/wiki/script.py)

# Known issues #

Notice:

  * ~~the inconsistency in AC wrt referring to the frequency as '#w' or 'w'. This is a bug and will be corrected ASAP.~~ Done.
  * You need to transpose the matrices for plotting or matplotlib will misinterpret them.