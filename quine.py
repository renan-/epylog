#!/usr/bin/python
# -*- encoding: utf-8 -*-
from collections import Counter
from copy import deepcopy
from yacc import parser

from models import BinaryStmt, Atom, Not, TRUE, FALSE

def print_step(s, lvl):
	indent = ''.join(['\t' for i in range(lvl)])
	print("%s%s" % (indent, s))

def run_algorithm(f, val, lvl=0):
	# First let's determine which atom to replace
	to_replace = Counter([l for l in str(f) if l.isalpha()]).most_common(1)[0][0]

	print_step('[%s]'% f, lvl)
	# Replace it
	f.replace(Atom(to_replace), val)
	print_step(f, lvl)

	# Reduce f with Quine's algorithm rules,
	# until it becomes either 1 or 0
	while not(f == TRUE or f == FALSE):
		f = f.reduce()
		print_step(f, lvl)
		# Re-run the algorithm when needed
		if f.isatomic:
			l = run_algorithm(deepcopy(f), TRUE, lvl + 1)
			r = run_algorithm(deepcopy(f), FALSE, lvl + 1)
			
			if l == TRUE and r == TRUE:
				return TRUE
			return FALSE

	return f

def prove(formula):
	try:
		f = parser.parse(formula)
	except SyntaxError as e:
		return e

	print('============================================================')
	print(' Running Quine\'s algorithm on [%s]' % formula)
	print('============================================================')
	print('----[Expanding with True]----')
	l = run_algorithm(deepcopy(f), TRUE)
	print('----[Done, got %s]----' % l)
	print('----[Expanding with False]----')
	r = run_algorithm(deepcopy(f), FALSE)
	print('----[Done, got %s]----' % r)

	if l == TRUE and r == TRUE:
		print('[%s] is a tautology' % formula)
	else:
		print('Cannot decide [%s]' % formula)
	print('============================================================')
