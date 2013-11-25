# macro to set compiler to g++
CC = g++

# create macro with flags
CXXFLAGS += -O0 -g -Wall -std=c++0x

# first target is built by default
all: client_TCP server_TCP listener_UDP talker_UDP 

client_TCP: client_TCP.cpp
	$(CC) client_TCP.cpp $(CXXFLAGS) -o client_TCP

server_TCP: server_TCP.cpp
	$(CC) server_TCP.cpp $(CXXFLAGS) -o server_TCP -lrt

listener_UDP: listener_UDP.cpp
	$(CC) listener_UDP.cpp $(CXXFLAGS) -o listener_UDP

talker_UDP: talker_UDP.cpp
	$(CC) talker_UDP.cpp $(CXXFLAGS) -o talker_UDP -lrt

# indicate that target clean should always be executed
.PHONY: clean
clean:
	@rm -f client_TCP server_TCP listener_UDP talker_UDP # '@' supresses output of this line
