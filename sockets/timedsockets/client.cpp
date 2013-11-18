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
#include <sys/select.h>

#define PORT "12345"
#define BUFLEN 12
#define MSGLEN 5

using namespace std;

static int read_buf[BUFLEN];
static int msg_buf[MSGLEN];
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
	ssize_t bytes_recv;
	int buflen=0;
	while (true) {
		memset(msg_buf, 0, MSGLEN*sizeof(int));
		cout << "\nclient listening for data from server" << endl;
		FD_ZERO(&readfds);
		FD_SET(sockfd, &readfds);
		int ready = select(sockfd+1, &readfds, NULL, NULL, NULL);
		if (ready == -1) {
			perror("client select");
			close(sockfd);
			exit(EXIT_FAILURE);
		}
		cout << "data from server ready, reading data" << endl;

		if (FD_ISSET(sockfd, &readfds)) {
			while (true) {
				bytes_recv = recv(sockfd, read_buf, sizeof(read_buf), 0);
				if (bytes_recv > 0) {
					buflen = bytes_recv/sizeof(int);
					cout << "received " << bytes_recv << " bytes, buflen " << buflen << endl;
					cout << "buffer contents:" << endl;
					for (int i=0; i<BUFLEN; i++) {
						cout << read_buf[i] << endl;
					}
					for (int i=buflen-1; i>=MSGLEN; i--) {
						if (read_buf[i] == -1) {
							memcpy(msg_buf, &read_buf[i-MSGLEN], MSGLEN*sizeof(int));
							memset(read_buf, 0, sizeof(read_buf));
							break;
						}
					}
				} else {
					break;
				}
			}
			cout << "done receiving data" << endl;
			if (bytes_recv < 0 && errno!=EWOULDBLOCK) {
				perror("client recv");
			} else if (bytes_recv == 0) {
				cout << "server closed connection" << endl;
				close(sockfd);
				exit(EXIT_SUCCESS);
			}
			cout << "last complete message:" << endl;
			for (int i=0; i<MSGLEN; i++) {
				cout << msg_buf[i] << endl;
			}

		} else {
			cerr << "select produces unexpected readfds" << endl;
		}

		sleep(4);
	}
}

