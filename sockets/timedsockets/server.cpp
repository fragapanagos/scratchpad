#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>

#define PORT "12345"

using namespace std;

static int client_sockfd = 0;
static int msg[5] = {0, 1, 2, 3, 4};

void intHandler(int sigVal) {
	assert(sigVal == SIGINT);
	cout << "\nserver: received SIGINT exiting" << endl;
	close(client_sockfd);
	exit(EXIT_SUCCESS);
}

void pipeHandler(int sigVal) {
	assert(sigVal == SIGPIPE);
	cout << "client closed connection" << endl;
	close(client_sockfd);
	exit(EXIT_SUCCESS);
}

int main() {
	signal(SIGINT, intHandler);
	signal(SIGPIPE, pipeHandler);

	struct addrinfo hints, *res;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	int rv = getaddrinfo(NULL, PORT, &hints, &res);
	if (rv != 0) {
		cerr << "getaddrinfo: " << gai_strerror(rv) << endl;
	}

	int listen_sockfd;
	struct addrinfo *p;
	for (p=res; p!=NULL; p=p->ai_next) {
		if ((listen_sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
			perror("server socket");
			continue;
		}
		int yes=1;
		if ((setsockopt(listen_sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) == -1)) {
			perror("server setsockopt");
			continue;
		}
		if (bind(listen_sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(listen_sockfd);
			perror("server bind");
			continue;
		}
		break;
	}
	if (p == NULL) {
		cerr << "server failed to bind" << endl;
		exit(EXIT_FAILURE);
	}
	freeaddrinfo(res);
	
	if (listen(listen_sockfd, 1) == -1) {
		perror("server listen");
		exit(EXIT_FAILURE);
	}

	cout << "server: waiting for client connection" << endl;
	struct sockaddr_storage client_addr;
	socklen_t sin_size = sizeof(client_addr);
	client_sockfd = accept(listen_sockfd, (struct sockaddr *)&client_addr, &sin_size);
	if (client_sockfd == -1) {
		perror("server accept");
		exit(EXIT_FAILURE);
	}
	close(listen_sockfd);
	cout << "server: connected to client" << endl;

	int bytes_sent, bytes_rem;
	int msglen = sizeof(msg);
	while (true) {
		bytes_rem = msglen;
		while (bytes_rem > 0) {
			bytes_sent = send(client_sockfd, msg, bytes_rem, 0);
			cout << bytes_sent << " bytes sent" << endl;
			if (bytes_sent == -1) {
				perror("server send");
				close(client_sockfd);
				exit(EXIT_FAILURE);
			}
			bytes_rem -= bytes_sent;
		}
		if (bytes_rem != 0) {
			cerr << "transmition error" << endl;
		}
		sleep(1);
	}
	exit(EXIT_SUCCESS);
}
