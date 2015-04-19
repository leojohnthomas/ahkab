# Introduction #

There are two MOS simulation models available in the simulator:
  * an implementation of the EKV model,
  * an implementation of the square law MOS model.

# EKV implementation #

## NMOS/PMOS model declaration ##

The model declaration is described in
[the relevant section of the Netlist syntax page](http://code.google.com/p/ahkab/wiki/NetlistSyntax#Rudimentary_EKV_3.0_MOS_model).

**NOTE THAT (_ENHANCEMENT_) PMOS DEVICES NEED A NEGATIVE THRESHOLD VOLTAGE** to operate correctly.

## NMOS characteristic ##

The device has KP=50uA/V^2, VTO=.4, everything else is left as DEFAULT and the voltages are VS=VB=0, VG=1, VD=2 (when they are not being swept.)

![http://ahkab.googlecode.com/svn/wiki/images/ekv/mosc_r0.png](http://ahkab.googlecode.com/svn/wiki/images/ekv/mosc_r0.png)

## NMOS TEF ##

Comparison of the (gm Vt)/Id for the two models. Notice how the square model fails to describe the sub-threshold region.

![http://ahkab.googlecode.com/svn/wiki/images/ekv/TEF.png](http://ahkab.googlecode.com/svn/wiki/images/ekv/TEF.png)

## OP information ##

As a design aid or just to gain insight in the circuit operation, the operating point solution prints the following information:

```
M1        N ch   STRONG INVERSION                     SATURATION                                                                                 
beta  [A/V^2]:  0.000247729775369  Weff  [m]:      1e-05 (1e-05)   Leff      [m]:  1.00916411694e-06 (1e-06)  M/N:                          1/1  
Vdb       [V]:                2.0   Vgb  [V]:                1.0    Vsb      [V]:                        0.0    Vp      [V]:     0.296484601435  
VTH       [V]:                0.4   VOD  [V]:      0.44498815655   nq:                          1.5428877488    VA      [V]:      2.17807647946  
Ids       [A]:  2.94741286575e-05  nv:             1.50088117358  Ispec      [A]:          1.03115399826e-06  TEF:               0.172685738397  
gmg       [S]:  0.000122160491895   gms  [S]:  -0.00019688056505    rob    [Ohm]:              73897.9090704                                     
if:                 29.2999434926   ir:           0.454365558078     Qf  [C/m^2]:           0.00027563279107    Qr  [C/m^2]:  1.89450556533e-05
```

increasing the verbosity level in the command line produces a print-out of the model parameters:

```
model_ekv0                            N MOS  EKV MODEL                                                                         
KP                [A/V^2]  5e-05        VTO       [V]:            0.4               TOX      [m]  None  COX  [F/m^2]:  0.0007  
PHI                  [V]:    0.7      GAMMA    sqrt(V)              1              NSUB  [cm^-3]  None  VFB      [V]:    None  
U0          [cm^2/(V*s)]:   None        TCV      [V/K]          0.001               BEX           -1.5                         
INTERNAL                          SAT LIMIT             54.5981500331  W/M/S INV FACTOR             10
```