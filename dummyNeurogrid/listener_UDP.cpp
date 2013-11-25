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
	cout << "\nlistener: exiting" << endl;
	close(sockfd);
	exit(EXIT_SUCCESS);
}

int main() {
	signal(SIGINT, cleanExit);

	struct addrinfo hints, *res;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;

	int rv;
	if ((rv = getaddrinfo(NULL, PORT, &hints, &res)) != 0) {
		cerr << "getaddrinfo: " << gai_strerror(rv) << endl;
	}

	struct addrinfo *p;
	for (p=res; p!=NULL; p=p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
			perror("listener socket");
			continue;
		}
		int yes=1;
		if ((setsockopt(sockfd, SOL_SOCKET, SO_REUSEADDR, &yes, sizeof(yes)) == -1)) {
			perror("server setsockopt");
			continue;
		}
		if (bind(sockfd, p->ai_addr, p->ai_addrlen) == -1) {
			close(sockfd);
			perror("server bind");
			continue;
		}
		break;
	}
	if (p == NULL) {
		cerr << "listener failed to connect" << endl;
		exit(EXIT_FAILURE);
	}

	freeaddrinfo(res);

    struct sockaddr_storage src_addr;
    socklen_t addrlen;
	ssize_t bytes_recv, bytes_rem;
	while (true) {
		memset(&msg_buf, 0, sizeof(msg_buf));
		//cout << "\nlistener listening for data from server" << endl;
        bytes_rem = sizeof(msg_buf);
		while (bytes_rem > 0) {
			bytes_recv = recvfrom(sockfd, 
                                  ((char *)&msg_buf) + sizeof(msg_buf) - bytes_rem,
                                  bytes_rem, 0, 
                                  (struct sockaddr *)&src_addr, &addrlen);
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
		if (bytes_recv < 0) {
			perror("listener recvfrom");
		} else if (bytes_recv == 0) {
			cout << "server closed connection" << endl;
			close(sockfd);
			exit(EXIT_SUCCESS);
		}
	}
}

