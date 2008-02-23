# -*- coding: iso-8859-1 -*-
# dc_analysis.py
# DC simulation methods
# Copyright 2006 Giuseppe Venturini

# This file is part of the ahkab simulator.
#
# Ahkab is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, version 2 of the License.
#
# Ahkab is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License v2
# along with ahkab.  If not, see <http://www.gnu.org/licenses/>.

"""
This module offers the functions needed to perform a dc simulation.

The principal are:
	dc_analysis() - which performs a dc sweep
	op_analysis() - which does a normal dc analysis or Operation Point
	
dc_analysis calls op_analysis.
The actual solution is done by mdn_solver, that uses a modified
version of the Newton Rhapson method.
"""

import sys
import numpy, numpy.linalg
import constants, ticker, options, circuit, printing, utilities, dc_guess



def dc_solve(mna, N, circ, use_gmin=True, x0=None, time=None, MAXIT=None, locked_nodes=None, verbose=3):
	"""Tries to perform a DC analysis of the circuit. 
	The system we want to solve is:
	mna*x + N + T(x) = 0
	
	mna is the reduced mna matrix with the required KVL rows
	N is the constant part of ?termine noto?
	T(x) will be built.
	
	circ is the circuit instance from which mna, N were built.
	
	x0 is the (optional) initial guess. If not specified, the all-zeros vector will be used
	
	This method is used ever by transient analysis. For transient analysis, time has to be set.
	In "real" DC analysis, time may be left to None. See circuit.py for more info about the default
	behaviour of time variant sources that also have a dc value.
	
	MAXIT is the maximum number of NR iteration to be supplied to mdn_solver.
	
	locked_nodes: array of tuples of nodes controlling non linear elements of the circuit.
	This is generated by circ.get_locked_nodes() and will be generated that way if left to none.
	However, if you are doing lots of simulations of the same circuit (a transient analysis), it's
	a good idea to generate it only once.
	"""
	if MAXIT == None:
		MAXIT = options.dc_max_nr_iter
	if locked_nodes is None:
		locked_nodes = circ.get_locked_nodes()
	mna_size = mna.shape[0]
	nv = len(circ.nodes_dict)
	#removed if use_gmin: gets built anyway.
	if use_gmin:
		if verbose: print "Building Gmin matrix..."
		Gmin_matrix = numpy.mat(numpy.zeros((mna_size, mna_size)))
		for index in xrange(len(circ.nodes_dict)-1):
			Gmin_matrix[index, index] = options.gmin
			# the three missing terms of the stample matrix go on [index,0] [0,0] [0, index] but since 
			# we discarded the 0 row and 0 column, we simply don't need to add them
			#the last lines are the KVL lines, introduced by voltage sources. Don't add gmin there.
	else:
		Gmin_matrix = 0
	
	#time variable component: Tt this is always the same in each iter. So we build it once for all.
	Tt = numpy.mat(numpy.zeros((mna_size, 1)))
	v_eq = 0
	for elem in circ.elements:
		if (isinstance(elem, circuit.vsource) or isinstance(elem, circuit.isource)) and elem.is_timedependent:
			if isinstance(elem, circuit.vsource):
				Tt[nv - 1 + v_eq, 0] = -1 * elem.V(time)
			elif isinstance(elem, circuit.isource):
				if elem.n1:
					Tt[elem.n1 - 1, 0] = Tt[elem.n1 - 1, 0] + elem.I(time)
				if elem.n2:
					Tt[elem.n2 - 1, 0] = Tt[elem.n2 - 1, 0] - elem.I(time)
		if circuit.is_elem_voltage_defined(elem):
			v_eq = v_eq + 1
	
	solved = True
	converged = False
	
	if verbose: 
		sys.stdout.write("Solving... ")
	#initial guess, if specified, otherwise it's zero
	if x0 is not None:
		x = x0
	else:
		x = numpy.mat(numpy.zeros((mna_size, 1))) # has n-1 rows because of discard of ^^^

	try:
		(x, error, converged, n_iter) = mdn_solver(x, mna + (use_gmin)*Gmin_matrix, circ.elements, Tf=N, Tt=Tt, \
		 nv=nv, print_steps=(verbose > 0), locked_nodes=locked_nodes, time=time, MAXIT=MAXIT)
	except numpy.linalg.linalg.LinAlgError:
		solved = False
		print "failed."
		printing.print_general_error("J Matrix is singular")
	except OverflowError:
		solved = False
		print "failed."
		printing.print_general_error("Overflow")
	
	if not converged and solved:
		solved = False
		print "failed."
		printing.print_general_error("Error: Hitted MAXIT ("+str(MAXIT)+")")
	
	if solved:
		if verbose: 
			print " done."
	else:
		x = None
		error = None
	
	return (x, error, solved)

def dc_analysis(circ, start, stop, step, elem_type, elem_descr, data_filename="stdout", print_int_nodes=True, guess=True, verbose=2):
	"""Performs a sweep of the value of V or I of a independent source from start 
	value to stop value using the provided step. 
	For every circuit generated, computes the op and prints it out.
	This function relays on dc_analysis.op_analysis to actually solve each circuit.
	
	circ: the circuit instance to be simulated
	start: start value of the sweep source
	stop: stop value of the sweep source
	step: step value of the sweep source
	elem_type: string, may be 'vsource' or 'isource'
	elem_descr: the description of the element, used to recognize it in circ (i.e v<desc>)
	data_filename: string, filename of the output file. If set to stdout, prints to screen
	print_int_nodes: do it
	guess: op_analysis will guess to start the first NR iteration for the first point, the previsious dc is used from then on
	verbose: verbosity level
	
	Returns:
	True, if a solution was found for each sweep value
	False, if an error occurred (eg invalid start/stop/step values) or there was no solution
	for a sweep value
	"""
	if verbose > 1 and data_filename != 'stdout': print "Starting DC analysis:"
	if step == 0:
		printing.print_general_error("Can't sweep with step=0 !")
		sys.exit(1)
	if verbose > 2 and start > stop:
		if step > 0: 
			print "Warning: start value of sweep is bigger than end value. Since step is > 0, no points will be calculated."
		elif step < 0 and verbose > 4: print "Notice: sweeping backwards."

	if elem_type != 'vsource' and elem_type != 'isource':
		printing.print_general_error("Sweeping is possible only with voltage and current sources. (" +str(elem_type)+ ")")
		sys.exit(1)

	if data_filename == "stdout":
		fpdata = sys.stdout
	else:
		fpdata = open(data_filename, "w")
			
	source_elem = None
	for index in xrange(len(circ.elements)):
		if circ.elements[index].descr == elem_descr:
			if elem_type == 'vsource': 
				if isinstance(circ.elements[index], circuit.vsource):
					source_elem = circ.elements[index]
					break
			if elem_type == 'isource':
				if isinstance(circ.elements[index], circuit.isource):
					source_elem = circ.elements[index]
					break
	if not source_elem:
		printing.print_general_error(elem_type + " element with descr. "+ elem_descr +" was not found.")
		sys.exit(1)
	
	if isinstance(source_elem, circuit.vsource):
		initial_value = source_elem.vdc
	else:
		initial_value = source_elem.idc

	# The initial value is set to None and this IS CORRECT. 
	# op_analysis will attempt to do a smart guess, if called with x0 = None and guess=True
	# For each iteration over the source voltage (current) value, the last result is used as x0.
	# op_analysis disregards guess is x0 is not None
	x = None
	solved = True
	
	printing.print_results_header(circ, fpdata, print_int_nodes=print_int_nodes, print_time=False)
	
	if verbose > 2 and fpdata != sys.stdout: 
		sys.stdout.write("Solving... ")
		tick = ticker.ticker(1)
		tick.display()
	
	#tarocca il generatore di tensione, avvia DC silenziosa, ritarocca etc
	for index in xrange(int((stop-start)/step)):
		if isinstance(source_elem, circuit.vsource):
			source_elem.vdc = start + index*step
		else:
			source_elem.idc = start + index*step
		#silently calculate the op
		x = op_analysis(circ, x0=x, guess=guess, verbose=0)
		if x is None:
			if verbose > 2 and fpdata != sys.stdout: 
				tick.hide()
			print "Could't solve the circuit for sweep value:", start + index*step
			solved = False
			break
		printing.print_results_on_a_line(time=None, x=x, fdata=fpdata, circ=circ, \
			print_int_nodes=print_int_nodes, iter_n=index)
		
		if guess:
			guess = False

		if verbose > 2 and fpdata != sys.stdout: 
			tick.step()
	
	if fpdata != sys.stdout: 
		if verbose > 2:
			tick.hide()
			if solved:
				print "done."
		fpdata.close()
	
	# clean up
	if isinstance(source_elem, circuit.vsource):
		source_elem.vdc = initial_value
	else:
		source_elem.idc = initial_value
	
	return solved	

def op_analysis(circ, x0=None, guess=True, verbose=3):
	"""Returns a Operation Point solution, if found, None otherwise.
	circ: is the circuit instance
	x0: is the initial guess to be used to start the NR mdn_solver
	guess: if set to True and x0 is None, it will generate a smart guess
	verbose: verbosity
	"""
	#use_gmin = True
	#solved=False
	#x0 = numpy.mat(numpy.zeros((1,2)))
	
	(mna, N) = generate_mna_and_N(circ)
	if verbose > 3:
		print "MNA matrix and constant term (complete):"
		print mna
		print N
	
	# lets trash the unneeded col & row
	if verbose > 3:
		print "Removing unneeded row and column..."
	mna = utilities.remove_row_and_col(mna)
	N = utilities.remove_row(N, rrow=0)
	
	if verbose > 1: 
		print "Starting op analysis:"
	
	if x0 is None and guess:
		x0 = dc_guess.get_dc_guess(circ, verbose=verbose)
	# if x0 is not None, use that
	
	if verbose:
		print "Solving with Gmin:"
	(x1, error1, solved1) = dc_solve(mna, N, circ, use_gmin=True, x0=x0, verbose=verbose)
	
	# We'll check the results now. Recalculate them without Gmin (using previsious solution as initial guess)
	# and check that differences on nodes are not too big
	if solved1:
		if verbose: print "Solving without Gmin:"
		(x2, error2, solved2) = dc_solve(mna, N, circ, use_gmin=False, x0=x1, verbose=verbose)
		
		if not solved2:
			printing.print_general_error("Can't solve without Gmin.")
			if verbose:
				print "Displaying latest valid results."
				printing.print_dc_results(x1, error1, circ, print_int_nodes=True, print_error=(verbose>3))
			return x1
		else:
			check_ok = printing.print_result_check(x2, x1, circ, verbose=verbose)
			if not check_ok and verbose:
				print "Solution with Gmin:"
				printing.print_dc_results(x1, error1, circ, print_int_nodes=True, print_error=(verbose>3))
			if verbose:
				print "Solution without Gmin:"
				printing.print_dc_results(x2, error2, circ, print_int_nodes=True, print_error=(verbose>3))
			return x2
	else:
		printing.print_general_error("Couldn't solve circuit. Giving up.")
	return None
			

def mdn_solver(x, mna, element_list, Tf, Tt, MAXIT, nv, locked_nodes, time=None, print_steps=False, vector_norm=lambda v: max(abs(v))):
	"""
	Solves a problem like F(x) = 0 using the Newton Algorithm with a variable damping td.
	
	Where:
	
	F(x) = mna*x + Tf + Tt + T(x)
	mna is the Modified Network Analysis matrix of the circuit
	T(x) is the contribute of nonlinear elements to KCL
	Tf -> independent sources, time invariant _ Those are both seen as constant within this method...
	Tt -> independent sources, time variant   -
	
	
	x is the initial guess.
	
	Every x is given by:
	x = x + td*dx
	Where td is a damping coefficient to avoid overflow in non-linear components and
	excessive oscillation in the very first iteration. Afterwards td=1
	To calculate td, an array of locked nodes is needed.
	
	The convergence check is done this way:
	if (vector_norm(dx) < alpha*vector_norm(x) + beta) and (vector_norm(residuo) < alpha*vector_norm(x) + beta):
	beta should be the machine precision, alpha 1e-(N+1) where N is the number of the significative 
	digits you wish to have.
	
	Parameters:
	x: the initial guess. If set to None, it will be initialized to all zeros. Specifying a initial guess
	may improve the convergence time of the algorithm and determine which solution (if any) 
	is found if there are more than one.
	mna: the Modified Network Analysis matrix of the circuit, reduced, see above
	element_list:
	Tf: see above.
	Tt: see above. Note: Tf and Tt are the same thing from the method's POV. We may remove one and set Tf=Tf+Tt...
	MAXIT: Maximum iterations that the method may perform.
	nv: number of nodes in the circuit (counting the ref, 0)
	locked_nodes: see get_td() and dc_solve(), generated by circ.get_locked_nodes()
	time: the value of time to be passed to non_linear _and_ time variant elements.
	print_steps: show a progress indicator
	vector_norm:
	
	Returns a tuple with:
	the solution, 
	the remaining error, 
	a boolean that is true whenever the method exits because of a successful convergence check
	the number of NR iterations performed
	
	"""
	# OLD COMMENT: FIXME REWRITE: solve through newton 
	# problem is F(x)= mna*x +H(x) = 0
	# H(x) = N + T(x)
	# lets say: J = dF/dx = mna + dT(x)/dx 
	# J*dx = -1*(mna*x+N+T(x))
	# dT/dx � lo jacobiano -> g_eq (o gm)
	#print_steps = False
	#locked_nodes = get_locked_nodes(element_list)
	mna_size = mna.shape[0]
	if print_steps: 
		tick = ticker.ticker(increments_for_step=1)
		tick.display()
	if x is None:
		x = numpy.mat(numpy.zeros((mna_size, 1))) # if no guess was specified, its all zeros
	else:
		if not x.shape[0] == mna_size:
			raise Exception, "x0s size is different from expected: "+str(x.shape[0])+" "+str(mna_size)
	if Tt is None:
		printing.print_warning("dc_analysis.mdn_solver called with Tf=is=None, setting Tf=0. BUG?")
		Tt = numpy.mat(numpy.zeros((mna_size, 1)))

	converged = False
	iteration = 0
	for iteration in xrange(MAXIT): # newton iteration counter
		if print_steps: 
			tick.step()
		J = numpy.mat(numpy.zeros((mna_size, mna_size)))
		T = numpy.mat(numpy.zeros((mna_size, 1)))
		for elem in element_list:
			 # build dT(x)/dx (stored in J) and T(x)
			if elem.is_nonlinear:
				ports = elem.get_ports()
				#print ports
				v_ports = []
				for port in ports:
					v = 0 # build v: remember we removed the 0 row and 0 col of mna -> -1
					if port[0]:
						v = v + x[port[0] - 1, 0]
					if port[1]:
						v = v - x[port[1] - 1, 0]
					v_ports.append(v)
					#print v
				if elem.n1:
					T[elem.n1 - 1, 0] = T[elem.n1 - 1, 0] + elem.i(v_ports, time)
				if elem.n2:
					T[elem.n2 - 1, 0] = T[elem.n2 - 1, 0] - elem.i(v_ports, time)
				for index in xrange(len(ports)):
					if elem.n1:
						if ports[index][0]:
							J[elem.n1 - 1, ports[index][0] - 1] = \
							J[elem.n1 - 1, ports[index][0] - 1] + elem.g(v_ports, index, time)
						if ports[index][1]:
							J[elem.n1 - 1, ports[index][1] - 1] = \
							J[elem.n1 - 1, ports[index][1] - 1] - 1.0*elem.g(v_ports, index, time)
					if elem.n2:
						if ports[index][0]:
							J[elem.n2 - 1, ports[index][0] - 1] = \
							J[elem.n2 - 1, ports[index][0] - 1] - 1.0*elem.g(v_ports, index, time)
						if ports[index][1]:
							J[elem.n2 - 1, ports[index][1] - 1] = \
							J[elem.n2 - 1, ports[index][1] - 1] + elem.g(v_ports, index, time)
						
		J = J + mna
		residuo = mna*x + T + Tf + Tt
		dx = numpy.linalg.inv(J) * (-1 * residuo)
		x = x + get_td(dx, locked_nodes, n=iteration)*dx
		# convergence and maxit test FIXME: check the residual
		if convergence_check(x, dx, residuo, nv-1):
		#(vector_norm(dx[:nv-1, 0]) < options.ver*vector_norm(x[:nv-1, 0]) + options.vea) and \
			#(mna_size == nv-1 or vector_norm(dx[nv-1:, 0]) < options.ier*vector_norm(x[nv-1:, 0]) + options.iea):
			#and vector_norm(residuo) < options.iea: fixme!
			converged = True
			break
		elif vector_norm(dx) is numpy.nan: #needs work fixme
			raise OverflowError
			#break
	if print_steps: tick.hide()
	return (x, residuo, converged, iteration)


def get_td(dx, locked_nodes, n=-1):
	"""Calculates the damping coefficient for the Newthon method.
	
	The damping coefficient is choosen as the lowest between:
	- the damping required for the first NR iterations
	- the biggest factor that keeps the change in voltage above the locked nodes
	  less than the max variation allowed (nl_voltages_lock_factor*Vth)
	
	Requires:
	dx - the undamped increment
	locked_nodes - a vector of tuples of nodes that are a port of a NL component
	n - the newthon iteration counter
	k - the maximum number of Vth allowed on a NL component
	
	Note:
	If n is set to -1 (or any negative value), td is independent from the iteration number.
	
	Returns: a float, the damping coefficient (td)
	"""
	
	# questo � per evitare sovraoscillazioni iniziali
	if not options.nr_damp_first_iters or n < 0:
		td = 1
	else:
		if n < 10:
			td = 1e-2
		elif n < 20:
			td = 0.1
		else:
			td = 1
	# per i componenti NL, vogliamo evitare OVERFLOW!
	td_new = 1
	if options.nl_voltages_lock:
		for (n1, n2) in locked_nodes:
			if n1 != 0:
				if n2 != 0:
					if abs(dx[n1 - 1, 0] - dx[n2-1, 0]) > options.nl_voltages_lock_factor * constants.Vth:
						td_new = (options.nl_voltages_lock_factor * constants.Vth)/abs(dx[n1 - 1, 0] - dx[n2 - 1, 0])
				else:
					if abs(dx[n1 - 1, 0]) > options.nl_voltages_lock_factor * constants.Vth:
						td_new = (options.nl_voltages_lock_factor * constants.Vth)/abs(dx[n1 - 1, 0])
			else:
				if abs(dx[n2 - 1, 0]) > options.nl_voltages_lock_factor * constants.Vth:
					td_new = (options.nl_voltages_lock_factor * constants.Vth)/abs(dx[n2 - 1, 0])
			if td_new < td:
				td = td_new
	return td


def generate_mna_and_N(circ):
	"""La vecchia versione usava il sistema visto a lezione, quella nuova mira ad essere 
	magari meno elegante, ma funzionale, flessibile e comprensibile. 
	MNA e N vengono creati direttamente della dimensione det. dal numero dei nodi, poi se 
	ci sono voltage sources vengono allargate.
	
	Il vettore incognita � fatto cos�:
	x vettore colonna di lunghezza (N_nodi - 1) + N_vsources, i primi N_nodi valori di x, corrispondono
	alle tensioni ai nodi, gli altri alle correnti nei generatori di tensione.
	Le tensioni nodali sono ordinate tramite i numeri interni dei nodi, in ordine CRESCENTE, saltando
	il nodo 0, preso a riferimento.
	L'ordine delle correnti nei gen di tensione � det. dall'ordine in cui essi vengono incontrati 
	scorrendo circ.elements. Viene sempre usata la convenzione normale.
	
	Il sistema � cos� fatto: MNA*x + N = 0
	
	Richiede in ingresso la descrizione del circuito, circ.
	Restituisce: (MNA, N)
	"""
	n_of_nodes = len(circ.nodes_dict)
	mna = numpy.mat(numpy.zeros((n_of_nodes, n_of_nodes)))
	N = numpy.mat(numpy.zeros((n_of_nodes, 1)))
	for elem in circ.elements:
		if elem.is_nonlinear:
			continue
		elif isinstance(elem, circuit.resistor):
			mna[elem.n1, elem.n1] = mna[elem.n1, elem.n1] + 1.0/elem.R
			mna[elem.n1, elem.n2] = mna[elem.n1, elem.n2] - 1.0/elem.R
			mna[elem.n2, elem.n1] = mna[elem.n2, elem.n1] - 1.0/elem.R
			mna[elem.n2, elem.n2] = mna[elem.n2, elem.n2] + 1.0/elem.R
		elif isinstance(elem, circuit.capacitor):
			pass #In a capacitor I(V) = 0
		elif isinstance(elem, circuit.gisource):
			mna[elem.n1, elem.sn1] = mna[elem.n1, elem.sn1] + elem.alpha
			mna[elem.n1, elem.sn2] = mna[elem.n1, elem.sn2] - elem.alpha
			mna[elem.n2, elem.sn1] = mna[elem.n2, elem.sn1] - elem.alpha
			mna[elem.n2, elem.sn2] = mna[elem.n2, elem.sn2] + elem.alpha
		elif isinstance(elem, circuit.isource):
			if not elem.is_timedependent: #convenzione normale!
				N[elem.n1, 0] = N[elem.n1, 0] + elem.I()
				N[elem.n2, 0] = N[elem.n2, 0] - elem.I()
			else:
				pass #vengono aggiunti volta per volta
		elif circuit.is_elem_voltage_defined(elem):
			pass
			#we'll add its lines afterwards
		else:
			print "dc_analysis.py: BUG - Unknown linear element. Ref. #28934"
	#process vsources
	# i generatori di tensione non sono pilotabili in tensione: g � infinita
	# for each vsource, introduce a new variable: the current flowing through it.
	# then we introduce a KVL equation to be able to solve the circuit
	for elem in circ.elements:
		if circuit.is_elem_voltage_defined(elem):
			index = mna.shape[0] #get_matrix_size(mna)[0]
			mna = utilities.expand_matrix(mna, add_a_row=True, add_a_col=True)
			N = utilities.expand_matrix(N, add_a_row=True, add_a_col=False)
			# KCL
			mna[elem.n1, index] = 1.0
			mna[elem.n2, index] = -1.0
			# KVL
			mna[index, elem.n1] = +1.0
			mna[index, elem.n2] = -1.0
			if isinstance(elem, circuit.vsource) and not elem.is_timedependent:
				# corretto, se � def una parte tempo-variabile ci pensa
				# mdn_solver a scegliere quella giusta da usare.
				N[index, 0] = -1.0*elem.V()
			elif isinstance(elem, circuit.evsource):
				mna[index, elem.sn1] = -1.0 * elem.alpha
				mna[index, elem.sn2] = +1.0 * elem.alpha
			elif isinstance(elem, circuit.inductor):
				#N[index,0] = 0 pass, it's already zero
				pass
			elif isinstance(elem, circuit.hvsource):
				print "dc_analysis.py: BUG - hvsources are not implemented yet."
				sys.exit(33)
	#all done
	return (mna, N)

def check_circuit(circ):
	"""Performs some easy sanity checks.
	
	Returns: a tuple consisting of a boolean (test was passed or not)
	and a string describing the error, if any.
	"""
	
	if len(circ.nodes_dict) < 2:
		test_passed = False
		reason = "the circuit has less than two nodes."
	elif not circ.nodes_dict.has_key(0):
		test_passed = False
		reason = "the circuit has no ref. Quitting."
	elif len(circ.elements) < 2:
		test_passed = False
		reason = "the circuit has less than two elements."
	else:
		test_passed = True
		reason = ""
		
	return test_passed, reason

def build_x0_from_user_supplied_ic(circ, voltages_dict, currents_dict):
	"""Builds a numpy.matrix of appropriate size (reduced!) from the values supplied
	in voltages_dict and currents_dict. What is not found in the dictionary is set to 0.
	
	Parameters:
	circ: the circuit instance
	voltages_dict: keys are the external nodes, values are the node voltages.
	currents_dict: keys are the elements names (eg l1, v4), the values are the currents
		
	Note: this simulator uses the normal convention.
	
	Returns:
	The x0 matrix
	"""
	nv = len(circ.nodes_dict) #number of voltage variables
	voltage_defined_elements = [ x for x in circ.elements if circuit.is_elem_voltage_defined(x) ]
	ni = len(voltage_defined_elements) #number of current variables
	current_labels_list = [ elem.letter_id + elem.descr for elem in voltage_defined_elements ]
	
	x0 = numpy.mat(numpy.zeros((nv + ni, 1)))
	
	for ext_node, value in voltages_dict.iteritems():
		int_node = circ.ext_node_to_int(ext_node)
		x0[int_node, 0] = value
	
	for current_label, value in currents_dict.iteritems():
		index = current_labels_list.index(current_label)
		x0[nv + index, 0] = value

	return x0[1:, :]

def modify_x0_for_ic(circ, x0):
	"""Modifies a supplied x0.
	"""
	nv = len(circ.nodes_dict) #number of voltage variables
	voltage_defined_elements = [ x for x in circ.elements if circuit.is_elem_voltage_defined(x) ]
	
	# setup voltages this may _not_ work properly
	for elem in circ.elements:
		if isinstance(elem, circuit.capacitor) and elem.ic:
			x0[elem.n1 - 1, 0] = x0[elem.n2 - 1, 0] + elem.ic
			
	# setup the currents
	for elem in voltage_defined_elements:
		if isinstance(elem, circuit.inductor) and elem.ic:
			x0[nv - 1 + voltage_defined_elements.index(elem), 0] = elem.ic
	
	return x0

def convergence_check(x, dx, residuum, nv_minus_one):
	return (voltage_convergence_check(x[:nv_minus_one, 0], dx[:nv_minus_one, 0], residuum[:nv_minus_one, 0]) and current_convergence_check(x[nv_minus_one:], dx[nv_minus_one:], residuum[nv_minus_one:]))
	
def voltage_convergence_check(x, dx, residuum):
	return custom_convergence_check(x, dx, residuum, er=options.ver, ea=options.vea, eresiduum=options.iea)

def current_convergence_check(x, dx, residuum):
	return custom_convergence_check(x, dx, residuum, er=options.ier, ea=options.iea, eresiduum=options.vea)

def custom_convergence_check(x, dx, residuum, er, ea, eresiduum, vector_norm=lambda v: max(abs(v))):
	if x.shape[0]:
		if vector_norm(dx) < er*vector_norm(x) + ea and vector_norm(residuum) < eresiduum:
			ret = True
		else:
			ret = False
	else:
		# We get here when there's no variable to be checked. This is because there aren't variables 
		# of this type. 
		# Eg. the circuit has no voltage sources nor voltage defined elements. In this case, the actual check is done
		#only by current_convergence_check, voltage_convergence_check always returns True.
		ret = True
	return ret
