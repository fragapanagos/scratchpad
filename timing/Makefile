# macro to set compiler to g++
CC = g++

# create macro with flags
CXXFLAGS += -O0 -g -Wall -std=c++0x

# first target is built by default
all: main 

# create target for main
MAINFILES += main.cpp
main: $(MAINFILES)
	$(CC) $(MAINFILES) $(CXXFLAGS) -omain -lrt

# indicate that target clean should always be executed
.PHONY: clean
clean:
	@rm -f test main # '@' supresses output of this line
