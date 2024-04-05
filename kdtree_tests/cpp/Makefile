#
# GNU makefile fuer kd-tree demo program
#============================================


# compiler options
#--------------------------------------------
CC = g++
#CFLAGS = -Wall -g
CFLAGS = -Wall -O2
LDFLAGS = -lstdc++

# project files
#--------------------------------------------
PROGRAM = demo_3d
OBJECTS = demo_3d.o kdtree.o

# rules
#--------------------------------------------
all: $(PROGRAM)

$(PROGRAM): $(OBJECTS)
	$(CC) -o $@ $+ $(LDFLAGS)

# generic rule for compiling *.cpp -> *.o
%.o: %.cpp kdtree.hpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $*.cpp

clean:
	rm -f $(PROGRAM) $(OBJECTS)

