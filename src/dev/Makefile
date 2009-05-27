# MMS, 5/30/08
# Simple makefile for building the test driver that unit
# tests the hypergraph and explicit relation datastructures.

all: test_RectDomain test_ExplicitRelation  #driver_moldyn_FST_hand 

#########
SRCS_RELATION = ExplicitRelation.c test_ExplicitRelation.c \
                RectDomain.c  \
                util.c ERG_cpack.c ERG_lexmin.c ERG_blockpart1D.c

test_ExplicitRelation: ExplicitRelation.h util.h RectDomain.h $(SRCS_RELATION)
	g++ -Wall -g  $(SRCS_RELATION) -o test_ExplicitRelation

#########
# MMS, as of 8/19/08 does not build because ERG_cpack now uses ExplicitRelation
#SRCS_HYPER = Hypergraph.c test_Hypergraph.c ERG_cpack.c util.c
#
#test_Hypergraph: Hypergraph.h util.h $(SRCS_HYPER)
#	g++ -Wall -g  $(SRCS_HYPER) -o test_Hypergraph

#########
SRCS_RD = RectDomain.c test_RectDomain.c 

test_RectDomain: RectDomain.h $(SRCS_RD)
	g++ -Wall -g  $(SRCS_RD) -o test_RectDomain


#########
SRCS = driver_moldyn_FST_hand.c util.c Hypergraph.c ERG_cpack.c ERG_lexmin.c 

driver_moldyn_FST_hand: util.h Hypergraph.h $(SRCS)
	g++ -Wall -g  $(SRCS) -o driver_moldyn_FST_hand


#########
docs: $(SRCS_Relation) ExplicitRelation.h RectDomain.h
	@echo "Generating doxygen docs to html/ subdirectory..."
	doxygen doxygen.config 

#########
clean:
	@echo "Cleaning up project directory ..."
	rm -f *.o test_RectDomain test_Hypergraph test_ExplicitRelation driver_moldyn_FST_hand core a.out
	rm -rf *.dSYM
	@echo ""
	@echo "Clean."
