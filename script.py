import ahkab
import circuit, printing, devices

mycircuit = circuit.circuit(title="Butterworth Example circuit", filename=None)

gnd = mycircuit.get_ground_node()

mycircuit.add_resistor(name="R1", ext_n1="n1", ext_n2="n2", R=600)
mycircuit.add_inductor(name="L1", ext_n1="n2", ext_n2="n3", L=15.24e-3)
mycircuit.add_capacitor(name="C1", ext_n1="n3", ext_n2=gnd, C=119.37e-9)
mycircuit.add_inductor(name="L2", ext_n1="n3", ext_n2="n4", L=61.86e-3)
mycircuit.add_capacitor(name="C2", ext_n1="n4", ext_n2=gnd, C=155.12e-9)
mycircuit.add_resistor(name="R2", ext_n1="n4", ext_n2=gnd, R=1.2e3)

voltage_step = devices.pulse(v1=0, v2=1, td=500e-9, tr=1e-12, pw=1, tf=1e-12, per=2)
mycircuit.add_vsource(name="V1", ext_n1="n1", ext_n2=gnd, vdc=5, vac=1, function=voltage_step)

printing.print_circuit(mycircuit)

op_analysis = {"type":"op", "guess_label":None}
ac_analysis = {"type":"ac", "start":1e3, "stop":1e5, "nsteps":100}
tran_analysis = {"type":"tran", "tstart":0, "tstop":1.2e-3, "tstep":1e-6, "uic":0, "method":None, "ic_label":None}

r = ahkab.process_analysis(an_list=[op_analysis, ac_analysis, tran_analysis], circ=mycircuit, outfile="script_output", verbose=0, cli_tran_method=None, guess=True, disable_step_control=False)

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
