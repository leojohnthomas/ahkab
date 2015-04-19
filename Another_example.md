#summary Transient analysis of a single balanced mixer
#labels Deprecated,Outdated

# Transient analysis of a single balanced mixer #

## Introduction ##
This is an example of simulation.

![http://ahkab.googlecode.com/svn/wiki/images/mixer-sb.png](http://ahkab.googlecode.com/svn/wiki/images/mixer-sb.png)

The RF source is sinusoidal with amplitude 0.2V at frf=11MHz, the local oscillator (LO) differential signal is a square wave at flo=10MHz between -5V and +5V to ensure complete switching of the MOS pair. Biasing is not shown.

## Netlist ##
```
Single balance mixer

vdd dd 0 type=vdc vdc=5
rl1 dd out1 1.5k
rl2 dd out2 1.5k

mlo1 out1 lo_in1 centre type=n kp=1e-3 vt=+1 w=10u l=1u lambda=0.001
mlo2 out2 lo_in2 centre type=n kp=1e-3 vt=+1 w=10u l=1u lambda=0.001

mlrf centre rf_in 0 type=n kp=1e-3 vt=+1 w=3u l=1u lambda=0.001
c1 centre 0 1p

vrf rf_in 0 type=vdc vdc=1.5 type=sin vo=1.5 va=0.2 freq=11e6 td=0 theta=0

vlo_dc lo_in_centre 0 type=vdc vdc=2.5

vlo_diff1 lo_in1 lo_in_centre type=vdc vdc=0 type=pulse v1=2.5 v2=-2.5 td=0 tr=1n tf=1n pw=49n per=100n
vlo_diff2 lo_in_centre lo_in2 type=vdc vdc=0 type=pulse v1=2.5 v2=-2.5 td=0 tr=1n tf=1n pw=49n per=100n

.op
.tran tstop=40u tstep=1n uic=1
```

## Running the simulation ##
Start ahkab with:

`./ahkab.py -o mixer-sb-graph  --t-max-nr 1000 -t trap --t-fixed-step mixer-sb.spc`

The simulation takes some time because we required 40e3 time steps, depending on the type of machine. The simulation time may be shorted setting `tstop` to a lower value.

## Results ##
The following image shows the differential output voltage Vout for a short time interval.

![http://ahkab.googlecode.com/svn/wiki/images/mixer-sb-vout.png](http://ahkab.googlecode.com/svn/wiki/images/mixer-sb-vout.png)

Amplitude plot of the FFT of Vout:

![http://ahkab.googlecode.com/svn/wiki/images/mixer-sb-vout-fft.png](http://ahkab.googlecode.com/svn/wiki/images/mixer-sb-vout-fft.png)

The results show correctly:
  * The down-converted signal at f = frf-flo = 1MHz
  * The up-converted signal at f = frf + flo = 21MHz
  * Strong LO feed-through at f=flo=10MHz, with odd order harmonics only
  * Various signals due to the products between the RF signal and the LO signal harmonics (eg at f = 3\*flo-frf = 19MHz)