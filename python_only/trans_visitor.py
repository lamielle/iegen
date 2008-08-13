#!/usr/bin/env python

from visitor import DFVisitor
from pres_parser import PresParser

class TransVisitor(DFVisitor):
	pass

v=TransVisitor()

print
v.visit(PresParser.parse_set('{[i,j]:1<=i && i<=n && 1<=j && j<=n}'))

print
v.visit(PresParser.parse_relation('{[i,j]->[ip,jp]:1<=i && i<=n && 1<=j && j<=n}'))
