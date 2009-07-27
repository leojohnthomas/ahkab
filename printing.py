# -*- coding: iso-8859-1 -*-
# printing.py
# Printing module
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
This is the printing module of the simulator. Using its functions, the output will
be somewhat uniform.
"""

import sys
import circuit, options
	
def print_circuit(circ):
	"""Prints the whole circuit to stdout, in a format similar to 
	the original netlist.
	
	Parameters:
	circ: the circuit instance to be printed.
	
	Returns: None
	"""
	if circ.title:
		print "TITLE:", circ.title
		
	for elem in circ.elements:
		print_netlist_elem_line(elem, circ)
	
	print "(analysis directives are omitted)"
	return None
	
def print_netlist_elem_line(elem, circ):
	"""Prints a elem to stdout from the provided circuit instance.
	
	Parameters:
	elem: the elem to be printed
	circ: the circuit instance to which the element belongs.
	
	Returns: None
	"""
	ext_n1 = circ.nodes_dict[elem.n1]
	ext_n2 = circ.nodes_dict[elem.n2]
	sys.stdout.write(elem.letter_id.upper() + elem.descr + " ")
	
	if isinstance(elem, circuit.resistor) or isinstance(elem, circuit.diode) or \
	isinstance(elem, circuit.isource) or isinstance(elem, circuit.vsource) or \
	isinstance(elem, circuit.capacitor) or isinstance(elem, circuit.inductor):
		sys.stdout.write(ext_n1 + " " + ext_n2 + " ")
	elif isinstance(elem, circuit.evsource) or isinstance(elem, circuit.gisource):
		sys.stdout.write(ext_n1 + " " + ext_n2 + " " + circ.nodes_dict[elem.sn1]+ " " + \
		circ.nodes_dict[elem.sn2] + " ")
	elif isinstance(elem, circuit.mosq): #quadratic mos
		sys.stdout.write(ext_n1 + " " + circ.nodes_dict[elem.ng] + " " + ext_n2 + " ")
	elif elem.letter_id == "y":
		sys.stdout.write(ext_n1 + " " + ext_n2 + " ")
	else:
		print ""
		print_general_error("Unknown element, this is probably a bug: " + elem.__class__.__name__)
		sys.exit(1)
	
	print str(elem)
	
	return None
	
def print_analysis(an):
	"""Prints a analysis to stdout, with the netlist syntax
	
	Parameters:
	an: an analisys, a element of the list returned from netlist_parser.parse_analysis
	
	Returns: None
	"""
	if an["type"] == "op":
		print ".op"
	elif an["type"] == "dc":
		print ".dc", an["source_name"], "start =", an["start"], "stop =", an["stop"], "step =", an["step"]
	elif an["type"] == "tran":
		sys.stdout.write(".tran tstep="+str(an["tstep"])+" tstop="+str(an["tstop"])+" tstart="+str(an["tstart"])+" uic="+str(an["uic"]))
		if an["uic"] == 3:
			sys.stdout.write(" ic_label="+an["ic_label"])
		if an["method"] is not None:
			print " method =", an["method"]
		else:
			print ""
	elif an["type"] == "shooting":
		sys.stdout.write(".shooting period="+ str(an["period"])+" method="str(an["method"]))
		if an["points"] is not None:
			sys.stdout.write(" points=" + str(an["points"]))
		if an["step"] is not None:
			sys.stdout.write(" step=" + str(an["step"]))
		print " autonomous=", an["autonomous"]

def print_general_error(description, print_to_stdout=False):
	"""Prints a error message to stderr.
	
	Parameters:
	description: the error's description
	print_to_stdout:
	
	Returns: None
	"""
	the_error_message = "E: " + description
	if print_to_stdout:
		print the_error_message
	else:
		sys.stderr.write(the_error_message+"\n")
	return None

def print_warning(description, print_to_stdout=False):
	"""Prints a warning message to stderr.
	
	Parameters:
	description: the warning's description
	print_to_stdout:
	
	Returns: None
	"""
	the_warning_message = "W: " + description
	if print_to_stdout:
		print the_warning_message
	else:
		sys.stderr.write(the_warning_message+"\n")
	return None
	

def print_parse_error(nline, line, print_to_stdout=False):
	"""Prints a parsing error in the netlist to stderr.
	
	Parameters:
	nline: number of the line on which the error was found
	line: the line of the file
	print_to_stdout:
	
	Returns: None
	"""
	print_general_error("Parse error on line " + str(nline) + ":", print_to_stdout)
	if print_to_stdout:
		print line
	else:
		sys.stderr.write(line+"\n")
	return None
	
	
def print_dc_results(x, error, circ, print_int_nodes=False, print_error=True):
	"""Prints out a set of DC results.
	x: the result set
	error: the residual error after solution,
	circ: the circuit instance of the simulated circuit
	print_int_nodes: a boolean to be set True if you wish to see voltage values 
	of the internal nodes added automatically by the simulator.
	
	Returns: None
	"""
	#We have mixed current and voltage results
	# per primi vengono tanti valori di tensioni quanti sono i nodi del circuito meno uno,
	# quindi tante correnti quanti sono gli elementi definiti in tensione presenti
	# (per questo, per misurare una corrente, si può fare uso di generatori di tensione da 0V)
	
	
	nv_1 = len(circ.nodes_dict) - 1 # numero di soluzioni di tensione (al netto del ref)
	skip_nodes_list = []	      # nodi da saltare, solo interni
	
	# descrizioni dei componenti non definibili in tensione
	idescr = [ (elem.letter_id.upper() + elem.descr) \
		for elem in circ.elements if circuit.is_elem_voltage_defined(elem) ] #cleaner ??

	#print "Solution:"
	for index in xrange(x.shape[0]):
		if index < nv_1:
			if print_int_nodes or not circ.is_int_node_internal_only(index+1):
				print "V" + str(circ.nodes_dict[index + 1]) + ": " + \
				str(x[index, 0]) + " V"
			else:
				skip_nodes_list.append(index)
		else:
			print "I: "+str(x[index, 0])+" A  (through "+idescr[index-nv_1]+")"
	if print_error:
		print "Residual error:"
		for index in xrange(x.shape[0]):
			if skip_nodes_list.count(index) == 0:
				print error[index]
	return None

def print_result_check(x2, x1, circ, verbose=2): #fixme I don't like it!
	"""Checks the differences between two sets of results and prints to stdout.
	It assumes one set of results is calculated with Gmin, the other without.
	x1, x2: the results vectors
	circ: 	circuit description
	
	Returns:
	True, if the check was passed
	False, otherwise.
	"""
	first_time = True
	nv_1 = len(circ.nodes_dict) - 1
	
	# descrizioni dei componenti non definibili in tensione
	idescr = [ (elem.letter_id.upper() + elem.descr) \
		for elem in circ.elements if circuit.is_elem_voltage_defined(elem) ] #cleaner ??
	
	dxg = x2 - x1
	for index in xrange(x2.shape[0]):
		if (index < nv_1 and abs(dxg[index, 0]) > options.ver*max(abs(x1[index, 0]), abs(x2[index, 0])) + \
		options.vea) or \
		(index >= nv_1 and abs(dxg[index, 0]) > options.ier*max(abs(x1[index, 0]), abs(x2[index, 0]))+options.iea):
			if first_time:
				print "Warning: solution is heavvily dependent on gmin."
				first_time = False
				if verbose:
					print "Affected variables:"
			if verbose:
				if index < nv_1:
					print "V" + str(circ.nodes_dict[index + 1])
				else:
					print "I through " + idescr[index - nv_1]
	if first_time:
		if verbose: 
			print "Difference check is within margins." 
			print "(Voltage: er=" + str(options.ver) + ", ea=" + str(options.vea) + \
			", Current: er=" + str(options.ier) + ", ea=" + str(options.iea) + ")"
		return True
	return False

def print_results_header(circ, fp, print_int_nodes=False, print_time=False):
	"""Prints the header of the results.
	circ, a circuit instance
	fp, the file pointer to which the header should be written
	print_int_nodes=False, Print internal nodes
	print_time=False, Print the time (it's always the first column)
	
	Returns: None
	"""
	#node_names = map(lambda n: circ.nodes_dict[n], range(1, len(circ.nodes_dict)))
	#if not print_int_nodes:
		#node_names = filter(lambda name: not (name.find("INT") > -1), node_names)
	#labels = map(lambda n: "V"+n, node_names)

	voltage_labels = [ "V" + circ.nodes_dict[n] \
		for n in range(1, len(circ.nodes_dict)) \
		if (print_int_nodes or not circ.is_int_node_internal_only(n)) ]
	
	current_labels = [ "I("+elem.letter_id.upper()+elem.descr+")" \
			for elem in circ.elements \
			if circuit.is_elem_voltage_defined(elem)]
	labels = voltage_labels + current_labels
	
	if print_time:
		labels.insert(0, "#T")
	else:
		labels[0] = "#" + labels[0]
	
	for lab in labels:
		fp.write(lab+"\t")
	fp.write("\n")
	fp.flush()
	
	return None

	
def print_results_on_a_line(time, x, fdata, circ, print_int_nodes=False, iter_n=0):
	"""Prints the time (if it's not None) and the values of the elements of x (a numpy matrix Nx1) 
	in order to the stream fdata.
	If time is None it will be skipped
	
	When iter_n % 10 == 0 (and iter_n != 0), flushes the stream so that the simulation
	results may be read before the simulation ends.
	
	Parameters:
	time: a float, the time at which the results are valid, None otherwise
	x: a numpy Nx1 matrix
	fdata: the output stream
	circ: the circuit instance
	print_int_nodes: print internal nodes too
	iter_n: the number of the iteration. If set to something that's not zero, it will be checked and
	if iter_n % 10 == 0 the stream will be flushed.
	
	Returns: None.
	"""
	nv_1 = len(circ.nodes_dict) - 1
	
	if time is not None:
		fdata.write(str(time)+"\t")
	
	for i in range(x.shape[0]):
		if print_int_nodes or circ.is_int_node_internal_only(i) or i > nv_1:
			fdata.write(str(x[i, 0])+"\t")
	fdata.write("\n")
	
	if iter_n != 0 and iter_n % 10 == 0:
		fdata.flush()
	
	return None
