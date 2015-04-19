# Introduction #

This page explains briefly how to use coupling between inductors.

If you are familiar with SPICE's mutual inductors, you can skip this page, they work the same way.

# Syntax #

`K<string> <inductor1> <inductor2> <float>`

or

`K<string> <inductor1> <inductor2> k=<float>`

# Usage and internal modeling #

The coupling needs the two inductors to be coupled and the coupling factor `k`. **The coupling factor (`k`) has to be lesser than one.**

**Dot convention:** for every inductor coupling, the dot is to be placed on the first node specified when the inductor was declared.

![http://ahkab.googlecode.com/svn/wiki/images/ci/ci_modeling.jpg](http://ahkab.googlecode.com/svn/wiki/images/ci/ci_modeling.jpg)

Eg. the left hand side of the figure above can be specified with the entries below:

```
L1 n1 n2 1u
L2 n3 n4 1u
K1 L1 L2 k=.2
```

Internally, the following equations are enforced (refer to the right hand side of the previous figure):


`VL1 = L1*dI(L1)/dt + M*dI(L2)/dt`

`VL2 = L2*dI(L2)/dt + M*dI(L1)/dt`

Where M is the _mutual inductance_ and it is defined as:

`M = K*sqrt(L1*L2)`

# Ideal transformers #

Ideal (perfect) transformers are not supported, but can be approximated with the following choices:

  * Set k=0.999 (an ideal transformer would have k=1)
  * Set the inductors values high enough that the primary and secondary inductances have a negligible effect on the current/voltages over the transformer. (an ideal tranformer would have "infinite" primary and secondary inductances)
  * Set the ratio of the primary/secondary inductances L1/L2 equal to the windings ratio n1/n2.

# Pathological circuits #

A few pathological circuits are shown in the next figure.

![http://ahkab.googlecode.com/svn/wiki/images/ci/ci_pathological.jpg](http://ahkab.googlecode.com/svn/wiki/images/ci/ci_pathological.jpg)

**Explanations:**

**(a)** is pathological because two elements are specifying the transformer input node at the same time. (think what would happen in real life...) The resulting MNA matrix is singular. -> insert a series resistor to break the loop.

**(b)** corrects the issue above, but has an isolated secondary, which means that all the voltages at the secondary winding are not unequivocally defined. The resulting MNA is singular. -> join the primary and secondary with a very high isolation resistor or set the voltage of one node at the secondary with a voltage source.

**(c)** has k=1. k has to be less than 1 or _instability ensues_.

# Multiple coupling #

It is possible to couple multiple inductors together, the following is an example of a transformer with a center tap (connected to ground in this case).

![http://ahkab.googlecode.com/svn/wiki/images/ci/multiple_ci.jpg](http://ahkab.googlecode.com/svn/wiki/images/ci/multiple_ci.jpg)

```
* Transformer with a grounded center tap: 
* Primary: n1, n2
* Secondary 1: nA, 0
* Secondary 2: 0, nB

L1 n1 n2 10u
LA nA 0 5u
LB 0 nB 5u
K1 L1 LA .49
K1 L1 LB .49
```

# Known limitations #

**For the time being mutual inductors are unsupported in subcircuits.**

