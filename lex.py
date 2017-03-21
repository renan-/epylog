#!/usr/bin/python
# -*- encoding: utf-8 -*-

from collections import defaultdict
import ply.lex as lex

tokens = (
	# atoms
	'ATOM',

	# parenthesis
	'LPAREN',
	'RPAREN',

	# operators
	'NOT',
	'AND',
	'OR',
	'IFTHEN',
	'IFANDONLYIF',
)

t_ATOM = r'[A-z]'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_NOT = r'(\~|\!|\¬)'
t_AND = r'(\/\\|\^|\&|\∧|\∙)'
t_OR  = r'(\\\/|[v]|\|\||\∨)'
t_IFTHEN = r'(\-\>|\-\-\>|\=\>|\→|\⊃)'
t_IFANDONLYIF = r'(\<\-\>|\<\-\-\>|\<\=\>|\↔|\≡)'

t_ignore  = ' \t'

# Error handling rule
def t_error(t):
	if not(t.value[0].strip()):
		t.lexer.skip(1)
	else:
		print("Illegal character '%s'" % t.value[0])

lexer = lex.lex()
