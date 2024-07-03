CC = g++
#CFLAGS = -Wall -g
CFLAGS = -Wall -O2 -fopenmp -isystem /home/dxu03/adios210/include -Wl,-rpath,/home/dxu03/adios210/lib /home/dxu03/adios210/lib/libadios2_cxx11_mpi.so.2.10.0 /home/dxu03/adios210/lib/libadios2_cxx11.so.2.10.0 -Wl,-rpath-link,/home/dxu03/adios210/lib
LDFLAGS = -lstdc++ -fopenmp -isystem /home/dxu03/adios210/include -Wl,-rpath,/home/dxu03/adios210/lib /home/dxu03/adios210/lib/libadios2_cxx11_mpi.so.2.10.0 /home/dxu03/adios210/lib/libadios2_cxx11.so.2.10.0 -Wl,-rpath-link,/home/dxu03/adios210/lib
# project files
#--------------------------------------------
PROGRAM = main
OBJECTS = main.o
# rules
#--------------------------------------------
all: $(PROGRAM)
$(PROGRAM): $(OBJECTS)
	$(CC) -o $@ $+ $(LDFLAGS)
# generic rule for compiling *.cpp -> *.o
%.o: %.cpp kd_tree.hpp
	$(CC) $(CFLAGS) $(CPPFLAGS) -c $*.cpp

clean:
	rm -f $(PROGRAM) $(OBJECTS)
