#include <iostream>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <string.h>
#include <stdlib.h>
#include <stdio.h>
#include <signal.h>
#include <string.h>
#include <fcntl.h>
#include <unistd.h>
#include <sys/select.h>

#include "message.h" 

#define PORT "12345"

using namespace std;

static struct spike msg_buf;
static int sockfd = 0;

void cleanExit(int sigVal) {
	cout << "\nclient: exiting" << endl;
	close(sockfd);
	exit(EXIT_SUCCESS);
}

int main() {
	signal(SIGINT, cleanExit);

	struct addrinfo hints, *res;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_STREAM;

	int rv;
	if ((rv = getaddrinfo(NULL, PORT, &hints, &res)) != 0) {
		cerr << "getaddrinfo: " << gai_strerror(rv) << endl;
	}

	struct addrinfo *p;
	for (p=res; p!=NULL; p=p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
			perror("client socket");
			continue;
		}
		if (connect(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("client connect");
			continue;
		}
		break;
	}
	if (p == NULL) {
		cerr << "client failed to connect" << endl;
		exit(EXIT_FAILURE);
	}

	freeaddrinfo(res);

	fcntl(sockfd, F_SETFL, O_NONBLOCK);
	fd_set readfds;
	ssize_t bytes_recv, bytes_rem;
	while (true) {
		memset(&msg_buf, 0, sizeof(msg_buf));
		//cout << "\nclient listening for data from server" << endl;
		FD_ZERO(&readfds);
		FD_SET(sockfd, &readfds);
		int ready = select(sockfd+1, &readfds, NULL, NULL, NULL);
		if (ready == -1) {
			perror("client select");
			close(sockfd);
			exit(EXIT_FAILURE);
		}
		//cout << "data from server ready, reading data" << endl;

		if (FD_ISSET(sockfd, &readfds)) {
            bytes_rem = sizeof(msg_buf);
			while (bytes_rem > 0) {
				bytes_recv = recv(sockfd, ((char *)&msg_buf) + sizeof(msg_buf) - bytes_rem, bytes_rem, 0);
				if (bytes_recv > 0) {
                    bytes_rem -= bytes_recv;
				} else {
					break;
				}
			}
            if (bytes_rem < 0) {
                cout << "weird buffering" << endl;
            }
			//cout << "done receiving data" << endl;
			if (bytes_recv < 0 && errno!=EWOULDBLOCK) {
				perror("client recv");
			} else if (bytes_recv == 0) {
				cout << "server closed connection" << endl;
				close(sockfd);
				exit(EXIT_SUCCESS);
			}
		} else {
			cerr << "select produces unexpected readfds" << endl;
		}
	}
}

