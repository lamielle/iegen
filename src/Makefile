# MMS, 5/30/08
# Simple makefile for building the test driver that unit
# tests the hypergraph datastructure.

SRCS = Hypergraph.c test_Hypergraph.c IAG_cpack.c

test_Hypergraph: Hypergraph.h $(SRCS)
	g++ -Wall -g  $(SRCS) -o test_Hypergraph

