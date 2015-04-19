# Transient simulation of a ring oscillator composed by 3 inverters #

## Updates ##
  * July 11, 2011 - Updated transistors models to EKV.

## Introduction ##
This is an example of transient simulation. 6 MOSFETs compose a ring oscillator. The initial operating point is set with a ic=3 condition.


## Netlist ##
```
RING OSCILLATOR with 3 inverters

X1 name=inv1 in=1 out=3 psupply=2 nsupply=0
X2 name=inv1 in=3 out=4 psupply=2 nsupply=0
X3 name=inv1 in=4 out=1 psupply=2 nsupply=0

.subckt inv1 in out psupply nsupply
        m1 out in psupply psupply pch w=3u l=1u
        m2 out in nsupply nsupply nch w=1u l=1u
        c1 out 0 10f
.ends

v2 2 0 type=vdc vdc=2.5

.model ekv nch TYPE=n VTO=.4 KP=40e-6
.model ekv pch TYPE=p VTO=-.4 KP=12e-6

.op
.ic name=tran_start v1=0 v2=2.5 v3=2.5 v4=0
.tran tstop=50n tstep=1n uic=3 ic_label=tran_start method=trap
.plot tran v(1) v(3) v(4)
```

## Running the simulation ##
Save the netlist to a file named ring-osc-3.spc and start ahkab with:

`./ahkab.py ring-osc-3.spc -o ring-osc-3-data`

The simulation takes some time, it may be shorted setting `tstop` to a lower value.

## Results ##
The period of each voltage waveform in the ring is approximately 4.4ns, the corresponding frequency is approx. 227MHz.

The following image shows the in/out voltages of all the inverters composing the ring.

![http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-3-v.png](http://ahkab.googlecode.com/svn/wiki/images/ring-osc/ring-osc-3-v.png)

## Verbose output with notes ##
```
RING OSCILLATOR WITH 3 INVERTERS
Starting op analysis:
Calculating guess: done.
Solving with Gmin:
Building Gmin matrix...
Solving...  done.
Solving without Gmin:
Solving...  done.
Difference check is within margins.
(Voltage: er=0.001, ea=1e-06, Current: er=0.001, ea=1e-09)
Solution without Gmin:
V3:          1.22840144686  V  
V1:          1.22840144686  V  
V2:                    2.5  V  
V4:          1.22840144686  V  
I(V2):  -1.31608144334e-05  A  
OP INFORMATION:
M-x1-inv1-1      P ch    STRONG INVERSION                         LINEAR                                                                                
beta         [A/V^2]:   1.62685646495e-05  Weff  [m]:      3e-06 (3e-06)   Leff      [m]:  1.1064282798e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      -1.27159855314   Vgb  [V]:     -1.27159855314    Vsb      [V]:                       0.0    Vp      [V]:     0.454624441205  
VTH              [V]:                 0.4   VOD  [V]:    -0.666169268968   nq:                          1.519226695    VA      [V]:      -1.7229412864  
Ids              [A]:  -4.38693761481e-06  nv:             1.46531776251  Ispec      [A]:         7.31045282498e-08  TEF:               0.129444097007  
gmg              [S]:   3.88393511086e-11   gms  [S]:  -2.1965905404e-05    rob    [Ohm]:             392743.512145                                     
if:                         68.1069293312   ir:            1.71115392657     Qf  [C/m^2]:           0.0004271148273    Qr  [C/m^2]:  4.95092696458e-05  
-------------------
M-x1-inv1-2      N ch   STRONG INVERSION                          LINEAR                                                                                 
beta         [A/V^2]:  1.82248003017e-05  Weff  [m]:       1e-06 (1e-06)   Leff      [m]:  1.09740571468e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      1.22840144686   Vgb  [V]:       1.22840144686    Vsb      [V]:                        0.0    Vp      [V]:     0.428776131386  
VTH              [V]:                0.4   VOD  [V]:      0.630564763884   nq:                         1.52288324984    VA      [V]:      1.73430564039  
Ids              [A]:  4.38693777725e-06  nv:              1.47061535782  Ispec      [A]:          8.14227556436e-08  TEF:               0.135471824775  
gmg              [S]:  1.39120467735e-05   gms  [S]:  -2.29887763669e-05    rob    [Ohm]:              395333.995705                                     
if:                        60.5747405392   ir:             1.44814197766     Qf  [C/m^2]:          0.000402303586421    Qr  [C/m^2]:  4.42663676539e-05  
-------------------
C-x1-inv1-1  V(n1-n2):  1.22840144686  [V]  Q:  1.22840144686e-14  [C]  E:  7.5448505732e-15  [J]  
-------------------
M-x2-inv1-1      P ch    STRONG INVERSION                         LINEAR                                                                                
beta         [A/V^2]:   1.62685646495e-05  Weff  [m]:      3e-06 (3e-06)   Leff      [m]:  1.1064282798e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      -1.27159855314   Vgb  [V]:     -1.27159855314    Vsb      [V]:                       0.0    Vp      [V]:     0.454624441205  
VTH              [V]:                 0.4   VOD  [V]:    -0.666169268968   nq:                          1.519226695    VA      [V]:      -1.7229412864  
Ids              [A]:  -4.38693761481e-06  nv:             1.46531776251  Ispec      [A]:         7.31045282498e-08  TEF:               0.129444097007  
gmg              [S]:   3.88393511086e-11   gms  [S]:  -2.1965905404e-05    rob    [Ohm]:             392743.512145                                     
if:                         68.1069293312   ir:            1.71115392657     Qf  [C/m^2]:           0.0004271148273    Qr  [C/m^2]:  4.95092696458e-05  
-------------------
M-x2-inv1-2      N ch   STRONG INVERSION                          LINEAR                                                                                 
beta         [A/V^2]:  1.82248003017e-05  Weff  [m]:       1e-06 (1e-06)   Leff      [m]:  1.09740571468e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      1.22840144686   Vgb  [V]:       1.22840144686    Vsb      [V]:                        0.0    Vp      [V]:     0.428776131386  
VTH              [V]:                0.4   VOD  [V]:      0.630564763884   nq:                         1.52288324984    VA      [V]:      1.73430564039  
Ids              [A]:  4.38693777725e-06  nv:              1.47061535782  Ispec      [A]:          8.14227556436e-08  TEF:               0.135471824775  
gmg              [S]:  1.39120467735e-05   gms  [S]:  -2.29887763669e-05    rob    [Ohm]:              395333.995705                                     
if:                        60.5747405392   ir:             1.44814197766     Qf  [C/m^2]:          0.000402303586421    Qr  [C/m^2]:  4.42663676539e-05  
-------------------
C-x2-inv1-1  V(n1-n2):  1.22840144686  [V]  Q:  1.22840144686e-14  [C]  E:  7.5448505732e-15  [J]  
-------------------
M-x3-inv1-1      P ch    STRONG INVERSION                         LINEAR                                                                                
beta         [A/V^2]:   1.62685646495e-05  Weff  [m]:      3e-06 (3e-06)   Leff      [m]:  1.1064282798e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      -1.27159855314   Vgb  [V]:     -1.27159855314    Vsb      [V]:                       0.0    Vp      [V]:     0.454624441205  
VTH              [V]:                 0.4   VOD  [V]:    -0.666169268968   nq:                          1.519226695    VA      [V]:      -1.7229412864  
Ids              [A]:  -4.38693761481e-06  nv:             1.46531776251  Ispec      [A]:         7.31045282498e-08  TEF:               0.129444097007  
gmg              [S]:   3.88393511086e-11   gms  [S]:  -2.1965905404e-05    rob    [Ohm]:             392743.512145                                     
if:                         68.1069293312   ir:            1.71115392657     Qf  [C/m^2]:           0.0004271148273    Qr  [C/m^2]:  4.95092696458e-05  
-------------------
M-x3-inv1-2      N ch   STRONG INVERSION                          LINEAR                                                                                 
beta         [A/V^2]:  1.82248003017e-05  Weff  [m]:       1e-06 (1e-06)   Leff      [m]:  1.09740571468e-06 (1e-06)  M/N:                          1/1  
Vdb              [V]:      1.22840144686   Vgb  [V]:       1.22840144686    Vsb      [V]:                        0.0    Vp      [V]:     0.428776131386  
VTH              [V]:                0.4   VOD  [V]:      0.630564763884   nq:                         1.52288324984    VA      [V]:      1.73430564039  
Ids              [A]:  4.38693777725e-06  nv:              1.47061535782  Ispec      [A]:          8.14227556436e-08  TEF:               0.135471824775  
gmg              [S]:  1.39120467735e-05   gms  [S]:  -2.29887763669e-05    rob    [Ohm]:              395333.995705                                     
if:                        60.5747405392   ir:             1.44814197766     Qf  [C/m^2]:          0.000402303586421    Qr  [C/m^2]:  4.42663676539e-05  
-------------------
C-x3-inv1-1  V(n1-n2):  1.22840144686  [V]  Q:  1.22840144686e-14  [C]  E:  7.5448505732e-15  [J]  
-------------------
TOTAL POWER: 3.29020360835e-05 W
Starting transient analysis: 
Selected method: TRAP
Building Gmin matrix...
Solving... done.
Average time step: 4.20521446594e-11
```