#!/usr/bin/python
# -*- encoding: utf-8 -*-
from quine import prove

while True:
	try:
		formula = input('Please enter a valid FOPL formula [q = QUIT]\n:: ')
	except (EOFError, KeyboardInterrupt):
		print('Bye!')
		break
	else:
		if formula == 'q' or formula == 'Q':
			break

	try:
		prove(formula)
	except SyntaxError as err:
		print('Try again... %s' % err)
		continue
