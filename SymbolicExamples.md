# Syntax #

A small signal symbolic analysis is requested through the .symbolic directive. Its syntax is:
```
.symbolic [tf=<source_name> ac=<bool>]
```

If the source is specified, all results are differentiated with respect to the source value (transfer functions).

If `ac` is set to 1, True or yes, capacitors and inductors will be taken into account.

# Examples #

## Output resistance of a degenerated MOS transistor ##

![http://ahkab.googlecode.com/svn/wiki/images/rd_symb.png](http://ahkab.googlecode.com/svn/wiki/images/rd_symb.png)

Let's say we wish to check the expression of the output resistance of the circuit in the figure above, the small signal -v2/I(v2).

Save the following netlist to a file, for example rd.ckt.

```
* Output resistance of a degenerated MOS transistor
m1 low gate deg 0 pch w=1u l=1u
rs deg s 1k
v1 gate 0 type=vdc vdc=1
v3 s 0 type=vdc vdc=1
v2 low 0 type=vdc vdc=1

.model ekv pch type=p kp=10e-6 vto=-1
.symbolic tf=v2
```

Start ahkab with:

```
./ahkab rd.ckt
```

### Results ###
```
* OUTPUT RESISTANCE OF A DEGENERATED MOS TRANSISTOR
Starting symbolic DC...
Building symbolic MNA, N and x...  done.
Building equations...
Performing auxiliary simplification...
Auxiliary simplification solved the problem.
Success!
[ ... very long lines omitted  ... ]
Calculating small-signal symbolic transfer functions (v2))... done.
Small-signal symbolic transfer functions:
I_[V1]/v2 = 0
	DC: 0
I_[V2]/v2 = -1.0/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
	DC: -1.0/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
I_[V3]/v2 = 1.0/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
	DC: 1.0/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
V_deg/v2 = 1.0*R_s/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
	DC: 1.0*R_s/(R_s*gm_M1*r0_M1 + R_s + r0_M1)
V_gate/v2 = 0
	DC: 0
V_low/v2 = 1.00000000000000
	DC: 1.00000000000000
V_s/v2 = 0
	DC: 0
```

The simulator solves the circuit symbolically and the differentiates the results according to the transfer function requested.

We wish to know the transfer function between V2 and -I(V2), rearranging the results above:

```
Rout = -dV2/dI[V2] = r0_M1 + R_s + gm_M1*r0_M1*R_s
```


## Small-signal transfer function of various Operational amplifier configurations ##

### Basic scheme ###


![http://ahkab.googlecode.com/svn/wiki/images/leaky_integrator.png](http://ahkab.googlecode.com/svn/wiki/images/leaky_integrator.png)

### Integrator with finite gain ###

The ideal integrator is the configuration shown above with no [R2](https://code.google.com/p/ahkab/source/detail?r=2) resistor. It has a transfer function equal to T(s) = K/s for all frequencies. Notice the infinite zero frequency gain.

A real integrator will have a transfer function differing from the one above because of many factors. One of which is the finite gain of every amplifier. This goes well with the simulator as it does not like "infinite quantities".

Netlist:
```
PERFECT INTEGRATOR
v1 in 0 type=vdc vdc=1
r1 in inv 1k
e1 out 0 0 inv 1e6
c1 inv out 1p

.symbolic tf=v1 ac=1
```

If the amplifier has a gain equal to **e1**, then skipping to the results we get:
```
I[E1]	 = (C1*s*v1 + C1*e1*s*v1)/(1 + C1*R1*s + C1*R1*e1*s)
I[V1]	 = -(C1*s*v1 + C1*e1*s*v1)/(1 + C1*R1*s + C1*R1*e1*s)
Vin	 = v1
Vinv	 = v1/(1 + C1*R1*s + C1*R1*e1*s)
Vout	 = -e1*v1/(1 + C1*R1*s + C1*R1*e1*s)
Calculating symbolic transfer functions (v1)... done!
d/dv1 I[E1] = (C1*s + C1*e1*s)/(1 + C1*R1*s + C1*R1*e1*s)
	DC: 0
	P0: 1/(-C1*R1 - C1*R1*e1)
	Z0: 0
d/dv1 I[V1] = -(C1*s + C1*e1*s)/(1 + C1*R1*s + C1*R1*e1*s)
	DC: 0
	P0: 1/(-C1*R1 - C1*R1*e1)
	Z0: 0
d/dv1 Vin = 1
	DC: 1
d/dv1 Vinv = 1/(1 + C1*R1*s + C1*R1*e1*s)
	DC: 1
	P0: 1/(-C1*R1 - C1*R1*e1)
d/dv1 Vout = -e1/(1 + C1*R1*s + C1*R1*e1*s)
	DC: -e1
	P0: 1/(-C1*R1 - C1*R1*e1)
```

`d/dv1 Vout` is what we are interested in here: the DC gain increases proportionally to e1 and the position of the low frequency pole moves back towards DC with e1 as well.

### Feedback resistor ###
If we introduce a resistor [R2](https://code.google.com/p/ahkab/source/detail?r=2) shunting the capacitor, we get a low frequency amplifier, which more or less behaves like an amplifier with constant gain -[R2](https://code.google.com/p/ahkab/source/detail?r=2)/[R1](https://code.google.com/p/ahkab/source/detail?r=1) before w = -1/(C1 [R2](https://code.google.com/p/ahkab/source/detail?r=2)), then the gain decreases by 20dB/decade.

Netlist:
```
INVERTING AMPLIFIER WITH BW LIMITATION
v1 in 0 type=vdc vdc=1
r1 in inv 1k
e1 out 0 0 inv 1e6
c1 inv out 1p
r2 inv out 1k

.symbolic tf=v1 ac=1

```

From the simulation:

```
I[E1]	 = (v1 + e1*v1 + C1*R2*s*v1 + C1*R2*e1*s*v1)/(R1 + R2 + R1*e1 + C1*R1*R2*s + C1*R1*R2*e1*s)
I[V1]	 = (v1 + e1*v1 + C1*R2*s*v1 + C1*R2*e1*s*v1)/(-R1 - R2 - R1*e1 - C1*R1*R2*s - C1*R1*R2*e1*s)
Vin	 = v1
Vinv	 = R2*v1/(R1 + R2 + R1*e1 + C1*R1*R2*s + C1*R1*R2*e1*s)
Vout	 = R2*e1*v1/(-R1 - R2 - R1*e1 - C1*R1*R2*s - C1*R1*R2*e1*s)
Calculating symbolic transfer functions (v1)... done!
d/dv1 I[E1] = (1 + e1 + C1*R2*s + C1*R2*e1*s)/(R1 + R2 + R1*e1 + C1*R1*R2*s + C1*R1*R2*e1*s)
	DC: (1 + e1)/(R1 + R2 + R1*e1)
	P0: (R1 + R2 + R1*e1)/(-C1*R1*R2 - C1*R1*R2*e1)
	Z0: -1/(C1*R2)
d/dv1 I[V1] = (1 + e1 + C1*R2*s + C1*R2*e1*s)/(-R1 - R2 - R1*e1 - C1*R1*R2*s - C1*R1*R2*e1*s)
	DC: (1 + e1)/(-R1 - R2 - R1*e1)
	P0: (R1 + R2 + R1*e1)/(-C1*R1*R2 - C1*R1*R2*e1)
	Z0: -1/(C1*R2)
d/dv1 Vin = 1
	DC: 1
d/dv1 Vinv = R2/(R1 + R2 + R1*e1 + C1*R1*R2*s + C1*R1*R2*e1*s)
	DC: R2/(R1 + R2 + R1*e1)
	P0: (R1 + R2 + R1*e1)/(-C1*R1*R2 - C1*R1*R2*e1)
d/dv1 Vout = R2*e1/(-R1 - R2 - R1*e1 - C1*R1*R2*s - C1*R1*R2*e1*s)
	DC: R2*e1/(-R1 - R2 - R1*e1)
	P0: (R1 + R2 + R1*e1)/(-C1*R1*R2 - C1*R1*R2*e1)
```

If e1 is indeed very high, the circuit results are as expected.

Effects of finite output resistance, differential input capacitance, finite input resistance can all be simulated similarly.