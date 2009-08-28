CC=gcc
INCLUDES=-I/home/lamielle/software/isl/include/isl -I/home/lamielle/software/isl/include
LIBS= -L/home/lamielle/software/isl/lib -lisl


all: simple

simple:
	$(CC) $(INCLUDES) $(LIBS) simple.c -o simple

clean:
	rm -f simple
