#summary Transient simulation of a Colpitts oscillator

# Transient simulation of a [Colpitts oscillator](http://en.wikipedia.org/wiki/Colpitts_oscillator) #

## Introduction ##

This is an example of transient simulation, featuring a well-known oscillator.

![http://ahkab.googlecode.com/svn/wiki/images/colpitts/colpitts.png](http://ahkab.googlecode.com/svn/wiki/images/colpitts/colpitts.png)

Bias: Vdd=2.5V, Vbias=2V.

L1 5 nH, [R0](https://code.google.com/p/ahkab/source/detail?r=0) 3.14 kOhm (QL=33 @ 3 GHz)

C1 = C2 = 1.012 pF (n = C1/(C1 + C2) = 0.5)

C2 has a Q greater than 10 for every Ib less than (w0 C2)<sup>2</sup>/(2 K 10<sup>2</sup>) = 4.8 mA.

Under such condition, the minimum transconductance required for oscillation can be calculated considering the MOS transistor an ideal voltage probe. The presence of the MOS has to be taken into account when evaluating the overall Q of the tank.

Under such hypothesis: gm\_min = 1/(n(1-n)[R0](https://code.google.com/p/ahkab/source/detail?r=0)). Ib\_min = 1.27 mA. In the following we use Ib = 1.3mA.


## Netlist ##
```
MOS COLPITTS OSCILLATOR

vdd dd 0 type=vdc vdc=2.5

* Ql = 33 at 3GHz
l1 dd nd 5n ic=-1n
r0 nd dd 3.5k 

* n = 0.5, f0 = 3GHz
c1 nd ns 1.12p ic=2.5
c2 ns 0  1.12p *ic=.01

m1 nd1 bias ns ns nmos w=200u l=1u
vtest nd nd1 type=vdc vdc=0 *read current

* Bias
vbias bias 0 type=vdc vdc=2
ib ns 0 type=idc idc=1.3m

.model ekv nmos TYPE=n VTO=.4 KP=10e-6

.op
.tran tstop=250n tstep=.1n method=trap uic=2
.plot tran v(nd)
```

The voltage generator Vtest has been added to the circuit in series with M1's drain to add the drain current to the variables.


We need to simulate the circuit for roughly ~10\*QL/f0 = 110ns to approach the steady state solution. The simulation above stops at t=2.5us.

## Running the simulation ##
Save the netlist in a file and start ahkab with:

`$ ahkab colpitts_mos.spc -o colpitts_graph`

The simulation takes some time. Set tstop to a lower value to make it faster.

## Results ##

### Operating point (.OP) ###

The operating point is shown in this section of the program output:

```
(Voltage: er=0.001, ea=1e-06, Current: er=0.001, ea=1e-09)
Solution without Gmin:
Vdd:                   2.5  V  
Vnd:                   2.5  V  
Vns:       -0.376425620771  V  
Vnd1:                  2.5  V  
Vbias:                 2.0  V  
I(Vdd):            -0.0013  A  
I(L1):              0.0013  A  
I(Vtest):           0.0013  A  
I(Vbias):              0.0  A  
OP INFORMATION:
R0  V(n1-n2):  0.0  [V]  I(n2-n1):  0.0  [A]  P:  0.0  [W]  
-------------------
C1  V(n1-n2):  2.87642562077  [V]  Q:  3.22159669526e-12  [C]  E:  4.63334163702e-12  [J]  
-------------------
C2  V(n1-n2):  -0.376425620771  [V]  Q:  -4.21596695263e-13  [C]  E:  7.93498988647e-14  [J]  
-------------------
M1        N ch   STRONG INVERSION                         LINEAR                                                                                 
beta  [A/V^2]:  0.000751220305143  Weff  [m]:    0.0002 (0.0002)   Leff      [m]:  1.33116742606e-06 (1e-06)  M/N:                          1/1  
Vdb       [V]:      2.87642562077   Vgb  [V]:      2.37642562077    Vsb      [V]:                        0.0    Vp      [V]:      1.17710715699  
VTH       [V]:                0.4   VOD  [V]:      1.60668460319   nq:                         1.44047246384    VA      [V]:      2.02340246677  
Ids       [A]:   0.00129999990092  nv:             1.36494336446  Ispec      [A]:          3.85082827087e-06  TEF:              0.0629116999631  
gmg       [S]:   0.00184704182955   gms  [S]:  -0.00316358960639    rob    [Ohm]:               1556.4635546                                     
if:                 472.305466827   ir:             22.917075486     Qf  [C/m^2]:           0.00110725636224    Qr  [C/m^2]:  0.000224868741041  
-------------------
TOTAL POWER: 0.003739353307 W
```

### Transient simulation (.TRAN) ###

The oscillation builds up quickly, as shown in this plot of Vnd:

![http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot-startup.png](http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot-startup.png)

From inspection, the circuit oscillates at 3.002 GHz with an oscillation amplitude of roughly 4V.

The following graph is the drain current of the mos transistor. M1 is on only for a fraction of each period, this happens if Ib is greater than approx. 1.5Ib\_min.

It can be shown that an increase in Ib increases the oscillation amplitude. When The oscillation amplitude (at nd) approaches Vdd, a damping will appear at the middle of the current peak, because Vds = Vnd - Vns will be near to zero. If the oscillation amplitude increases further Vds crosses 0V and becomes negative for a small period of time. Accordingly, Id crosses 0A and becomes negative for such period. This does not happen in this case, but it can be tested changing the neltist.

Of course, in any case, the average current through M1 has to be equal to Ib.

![http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot-id.png](http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot-id.png)

This plot shows the voltages across M1 that corresponding to the current waveform above.

![http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot.png](http://ahkab.googlecode.com/svn/wiki/images/colpitts/plot.png)

During the period, M1 is always on, switching from saturation region (Vgs > Vt, Vgd < Vt) to ohmic operation (channel at both source and drain). The latter happens when Id is maximum.

The next plot shows the oscillation starting off from the very beginning in a phase plane:

![http://ahkab.googlecode.com/svn/wiki/images/colpitts/colpitts_phase_plane.png](http://ahkab.googlecode.com/svn/wiki/images/colpitts/colpitts_phase_plane.png)