# macro to set compiler to g++
CC = g++

# create macro with flags
CXXFLAGS += -O0 -g -Wall

# first target is built by default
all: test main 


# create target for main
MAINFILES += main.cpp hello.cpp
main: $(MAINFILES)
	$(CC) $(MAINFILES) -omain $(CXXFLAGS)


# create target for test
TESTFILES += test.cpp
test: $(TESTFILES)
	$(CC) $(TESTFILES) -otest $(CXXFLAGS)


# indicate that target clean should always be executed
.PHONY: clean
clean:
	@rm -f test main # '@' supresses output of this line
