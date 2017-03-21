#!/usr/bin/python
# -*- encoding: utf-8 -*-
import ply.yacc as yacc
import re

from models import Stmt, Atom, Not, And, Or, IfThen, IfAndOnlyIf 
from lex import tokens, t_ATOM, t_AND, t_OR, t_IFTHEN, t_IFANDONLYIF

precedence = (
	('left', 'AND', 'IFANDONLYIF',),
	('left', 'IFTHEN', 'OR',),
	('right', 'NOT',),
)

def p_formula(p):
	"""formula : formula AND formula
	           | formula OR formula
	           | formula IFTHEN formula
	           | formula IFANDONLYIF formula
	           | ATOM
	           | LPAREN formula RPAREN
	           | NOT formula"""
	# atomic formula
	if len(p) == 2:
		# if isinstance(p[2], str) and re.match(t_ATOM, p[2]) is not None:
		#	p[2] = Atom(p[2])
		p[0] = Atom(p[1])
	# NOT formula
	elif len(p) == 3:
		p[0] = Not(p[2])
	# binary formula or (formula)
	elif len(p) == 4:
		if p[1] == "(" and p[3] == ")":
			p[0] = p[2]
		else:
			if re.match(t_AND, p[2]) is not None:
				p[0] = And(p[1], p[2], p[3])
			elif re.match(t_OR, p[2]) is not None:
				p[0] = Or(p[1], p[2], p[3])
			elif re.match(t_IFTHEN, p[2]) is not None:
				p[0] = IfThen(p[1], p[2], p[3])
			elif re.match(t_IFANDONLYIF, p[2]) is not None:
				p[0] = IfAndOnlyIf(p[1], p[2], p[3])

def p_error(p):
	raise SyntaxError

parser = yacc.yacc()
