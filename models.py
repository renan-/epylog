#!/usr/bin/python
# -*- encoding: utf-8 -*-
import re

from lex import t_ATOM

class Stmt(object):
	def reduce(self):
		pass

	def replace(self, atom, value):
		pass

	@property
	def isatomic(self):
	    return False

	def __str__(self):
		pass

class Atom(Stmt):
	def __init__(self, name):
		self.name = name

	def reduce(self):
		return self

	def replace(self, atom, value):
		if self == atom:
			self.name = value.name

	@property
	def isatomic(self):
		return re.match(t_ATOM, self.name) is not None

	def __eq__(self, obj):
		if hasattr(obj, 'name'):
			return self.name == obj.name

		return False

	def __str__(self):
		return self.name

TRUE = Atom('1')
FALSE = Atom('0')

class UnaryStmt(Stmt):
	def __init__(self, op, expr):
		self.op = op
		self.expr = expr

	def reduce(self):
		pass

	def replace(self, atom, value):
		self.expr.replace(atom, value)

	@property
	def isatomic(self):
		return self.expr.isatomic

	def __str__(self):
		return '%s%s' % (op, expr)

class BinaryStmt(Stmt):
	def __init__(self, lexpr, op, rexpr):
		self.lexpr = lexpr
		self.op = op
		self.rexpr = rexpr

	def reduce(self):
		pass

	def replace(self, atom, value):
		self.lexpr.replace(atom, value)
		self.rexpr.replace(atom, value)

	@property
	def isatomic(self):
		return self.rexpr.isatomic and self.lexpr.isatomic

	def __str__(self):
		return '(%s %s %s)' % (str(self.lexpr), self.op, str(self.rexpr))

class And(BinaryStmt):
	def __init__(self, lexpr, op, rexpr):
		BinaryStmt.__init__(self, lexpr, op, rexpr)

	def reduce(self):
		if self.lexpr == TRUE and self.rexpr == FALSE:
			return TRUE
		elif self.lexpr == FALSE or self.rexpr == FALSE:
			return FALSE
		elif self.lexpr == TRUE:
			return self.rexpr
		elif self.rexpr == TRUE:
			return self.lexpr
		
		return And(self.lexpr.reduce(), self.op, self.rexpr.reduce())

class Or(BinaryStmt):
	def __init__(self, lexpr, op, rexpr):
		BinaryStmt.__init__(self, lexpr, op, rexpr)

	def reduce(self):
		if self.lexpr == TRUE or self.rexpr == TRUE:
			return TRUE
		elif self.lexpr == FALSE and self.rexpr == FALSE:
			return FALSE
		elif self.lexpr == FALSE:
			return self.rexpr
		elif self.rexpr == FALSE:
			return self.lexpr
		
		return Or(self.lexpr.reduce(), self.op, self.rexpr.reduce())

class IfThen(BinaryStmt):
	def __init__(self, lexpr, op, rexpr):
		BinaryStmt.__init__(self, lexpr, op, rexpr)

	def reduce(self):
		if self.lexpr == FALSE or self.rexpr == TRUE:
			return TRUE
		elif self.lexpr == TRUE and self.rexpr == FALSE:
			return FALSE
		elif self.lexpr == TRUE:
			return self.rexpr
		elif self.rexpr == FALSE:
			return Not(self.lexpr)

		return IfThen(self.lexpr.reduce(), self.op, self.rexpr.reduce())

class IfAndOnlyIf(BinaryStmt):
	def __init__(self, lexpr, op, rexpr):
		BinaryStmt.__init__(self, lexpr, op, rexpr)

	def reduce(self):
		if self.lexpr == self.rexpr:
			return TRUE
		elif self.lexpr == TRUE and self.rexpr == FALSE:
			return FALSE
		elif self.lexpr == FALSE and self.rexpr == TRUE:
			return FALSE
		elif self.lexpr == TRUE:
			return self.rexpr
		elif self.lexpr == FALSE:
			return Not(self.rexpr)
		elif self.rexpr == TRUE:
			return self.lexpr
		elif self.rexpr == FALSE:
			return Not(self.lexpr)

		return IfAndOnlyIf(self.lexpr.reduce(), self.op, self.rexpr.reduce())

class Not(UnaryStmt):
	def __init__(self, expr):
		self.expr = expr

	def replace(self, atom, value):
		self.expr.replace(atom, value)

	def reduce(self):
		if self.expr == TRUE:
			return FALSE
		elif self.expr == FALSE:
			return TRUE

		return Not(self.expr.reduce())

	def __str__(self):
		return '~%s' % self.expr
