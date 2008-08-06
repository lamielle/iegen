# Please enter here the locations for CloogLib include and libraries if they
# aren't the default values (/usr/lib and /usr/include).
POLYLIB_INC = $(HOME)/software/polylib/include
POLYLIB_LIB = $(HOME)/software/polylib/lib

CLOOG_INC = $(HOME)/software/cloog/include
CLOOG_LIB = $(HOME)/software/cloog/lib

CC = gcc
LDLIBS= -lcloog
CFLAGS= -I $(POLYLIB_INC) -L $(POLYLIB_LIB) -I $(CLOOG_INC) -L $(CLOOG_LIB)

all: simple pycloog

simple: simple.c
	$(CC) simple.c -o simple $(CFLAGS) $(LDLIBS)

pycloog: pycloog.c
	$(CC) pycloog.c -o pycloog.so -shared -fPIC $(CFLAGS) $(LDLIBS)

clean:
	-rm -f simple pycloog.so
