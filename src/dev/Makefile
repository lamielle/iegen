# MMS, 5/30/08
# Simple makefile for building the test driver that unit
# tests the hypergraph datastructure.

all: test_Hypergraph driver_moldyn_FST_hand

SRCS_HYPER = Hypergraph.c test_Hypergraph.c IAG_cpack.c util.c

test_Hypergraph: Hypergraph.h util.h $(SRCS_HYPER)
	g++ -Wall -g  $(SRCS_HYPER) -o test_Hypergraph

SRCS = driver_moldyn_FST_hand.c util.c Hypergraph.c IAG_cpack.c IAG_lexmin.c 

driver_moldyn_FST_hand: util.h Hypergraph.h $(SRCS)
	g++ -Wall -g  $(SRCS) -o driver_moldyn_FST_hand

clean:
	@echo "Cleaning up project directory ..."
	rm -f *.o test_Hypergraph driver_moldyn_FST_hand core a.out
	rm -rf *.dSYM
	@echo ""
	@echo "Clean."