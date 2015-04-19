# Transient simulation of a ring oscillator composed by 13 inverters #

## Introduction ##
This is an example of transient simulation. 26 MOSFETs compose a ring oscillator. The initial operating point is set with a ic=3 condition.


## Netlist ##
```
*RING OSCILLATOR with 13 inverters

X1 name=inv1 in=1 out=3 psupply=2 nsupply=0
X2 name=inv1 in=3 out=4 psupply=2 nsupply=0
X3 name=inv1 in=4 out=5 psupply=2 nsupply=0
X4 name=inv1 in=5 out=6 psupply=2 nsupply=0
X5 name=inv1 in=6 out=7 psupply=2 nsupply=0
X6 name=inv1 in=7 out=8 psupply=2 nsupply=0
X7 name=inv1 in=8 out=9 psupply=2 nsupply=0
X8 name=inv1 in=9 out=10 psupply=2 nsupply=0
X9 name=inv1 in=10 out=11 psupply=2 nsupply=0
X10 name=inv1 in=11 out=12 psupply=2 nsupply=0
X11 name=inv1 in=12 out=13 psupply=2 nsupply=0
X12 name=inv1 in=13 out=14 psupply=2 nsupply=0
X13 name=inv1 in=14 out=1 psupply=2 nsupply=0

.subckt inv1 in out psupply nsupply
        m1 out in psupply type=p kp=1e-3 vt=+1 w=1u l=1u lambda=0.01
        m2 out in nsupply type=n kp=1e-3 vt=+1 w=1u l=1u lambda=0.01
        c1 out 0 1p
.ends

v2 2 0 type=vdc vdc=3

.op

.ic name=tran_start v1=0 v2=3 v3=3 v4=0 v5=3 v6=0 v7=3 v8=0 v9=3 v10=0 v11=3 v12=0 v13=3 v14=0 *v15=3

.tran tstop=50n tstep=10n uic=3 ic_label=tran_start method=trap

.plot tran v(14) v(12) v(10) v(8) v(6) v(4) v(1)
```

## Running the simulation ##
Save the netlist to a file named ring-osc-13.spc and start ahkab with:

`./ahkab.py ring-osc-13.spc -o ring-osc-13-data`

The simulation takes some time, it may be shorted setting `tstop` to a lower value.

## Results ##
The period of each voltage waveform in the ring is approximatively 37.8ns, the corresponding frequency is approx. 26.5MHz.

The following image shows the in/out voltages of all the inverters composing the ring.

![http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-13-v.png](http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-13-v.png)

The current from the supply is in the next figure.

![http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-13-i.png](http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-13-i.png)

## Verbose output with notes ##
```
Parsed circuit:
TITLE: *ring oscillator with 13 inverters
M-x1-inv1-1 3 1 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x1-inv1-2 3 1 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x1-inv1-1 3 0 1e-12
M-x2-inv1-1 4 3 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x2-inv1-2 4 3 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x2-inv1-1 4 0 1e-12
M-x3-inv1-1 5 4 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x3-inv1-2 5 4 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x3-inv1-1 5 0 1e-12
M-x4-inv1-1 6 5 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x4-inv1-2 6 5 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x4-inv1-1 6 0 1e-12
M-x5-inv1-1 7 6 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x5-inv1-2 7 6 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x5-inv1-1 7 0 1e-12
M-x6-inv1-1 8 7 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x6-inv1-2 8 7 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x6-inv1-1 8 0 1e-12
M-x7-inv1-1 9 8 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x7-inv1-2 9 8 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x7-inv1-1 9 0 1e-12
M-x8-inv1-1 10 9 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x8-inv1-2 10 9 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x8-inv1-1 10 0 1e-12
M-x9-inv1-1 11 10 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x9-inv1-2 11 10 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x9-inv1-1 11 0 1e-12
M-x10-inv1-1 12 11 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x10-inv1-2 12 11 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x10-inv1-1 12 0 1e-12
M-x11-inv1-1 13 12 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x11-inv1-2 13 12 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x11-inv1-1 13 0 1e-12
M-x12-inv1-1 14 13 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x12-inv1-2 14 13 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x12-inv1-1 14 0 1e-12
M-x13-inv1-1 1 14 2 type=p kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
M-x13-inv1-2 1 14 0 type=n kp=0.001 vt=1.0 w=1e-06 l=1e-06 lambda=0.01
C-x13-inv1-1 1 0 1e-12
V2 2 0 type=vdc vdc=3.0 
(analysis directives are omitted)
Requested an.:
.op
.tran tstep=1e-08 tstop=5e-08 tstart=0.0 uic=3.0 ic_label=tran_start method = trap
```

The subcircuits are correctly inserted in the circuit.

```
MNA matrix and constant term (complete):
[[ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0. -1.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  1.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [ 0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]
 [-1.  0.  0.  1.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.  0.]]
[[ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [ 0.]
 [-3.]]
Removing unneeded row and column...
```

There are no linear elements except capacitors (not included in .OP) and a voltage source. Therefore the MNA matrix is all 0, except for 4 elements (two KCL lines and one KVL).

```
Starting op analysis:
Calculating guess: 
(...omitted...)
Guess:
[[ 1.15333333]
 [ 1.15333333]
 [ 2.30666667]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 1.15333333]
 [ 0.        ]]
```

We try to start from a useful point, where the transistors are barely ON, so they will shut off completely or switch on at the forst NR iteration.

```
Solving with Gmin:
Building Gmin matrix...
Solving...  done.
Solving without Gmin:
Solving...  done.
Difference check is within margins.
(Voltage: er=0.001, ea=1e-06, Current: er=0.001, ea=1e-09)
Solution without Gmin:
V3: 1.5 V
V1: 1.5 V
V2: 3.0 V
V4: 1.5 V
V5: 1.5 V
V6: 1.5 V
V7: 1.5 V
V8: 1.5 V
V9: 1.5 V
V10: 1.5 V
V11: 1.5 V
V12: 1.5 V
V13: 1.5 V
V14: 1.5 V
```

There is only one DC solution: the metastable equilibrium.

```
M-x1-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x1-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x2-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x2-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x3-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x3-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x4-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x4-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x5-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x5-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x6-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x6-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x7-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x7-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x8-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x8-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x9-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x9-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x10-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x10-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x11-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x11-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x12-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x12-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x13-inv1-1: P sat vgs: [[-1.5]] vgd: [[ 0.]] vds: [[-1.5]]
   id = [[-0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
M-x13-inv1-2: N sat vgs: [[ 1.5]] vgd: [[ 0.]] vds: [[ 1.5]]
   id = [[ 0.00012625]] gm: [[ 0.000505]] ro: [[ 800000.]]
```

Information about the status of the transistors.

```
Starting transient analysis: 
Selected method: TRAP
Using the supplied op as x(t=0.0).
x0:
#V3	V1	V2	V4	V5	V6	V7	V8	V9	V10	V11	V12	V13	V14	I(V2)	
3.0	0.0	3.0	0.0	3.0	0.0	3.0	0.0	3.0	0.0	3.0	0.0	3.0	0.0	0.0	
Selecting the appropriate DF (TRAP)... done
Setting up the buffer... done
MNA and D (reduced): omitted
Building Gmin matrix...
Initial step: 5.00050005001e-12
Solving... done.
Average time step: 7.33137829912e-11
Please press return to continue...


real	0m48.250s
user	0m7.800s
sys	0m0.060s


```