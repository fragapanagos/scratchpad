# macro to set compiler to g++
CC = g++

# create macro with flags
CXXFLAGS += -O0 -g -Wall -std=c++0x

# first target is built by default
all: client server

client: client.cpp
	$(CC) client.cpp $(CXXFLAGS) -o client

server: server.cpp
	$(CC) server.cpp $(CXXFLAGS) -o server

# indicate that target clean should always be executed
.PHONY: clean
clean:
	@rm -f client server # '@' supresses output of this line
