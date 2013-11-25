#include <iostream>
#include <iomanip>
#include <sys/types.h>
#include <sys/socket.h>
#include <netdb.h>
#include <stdlib.h>
#include <signal.h>
#include <unistd.h>
#include <string.h>
#include <assert.h>
#include <sys/time.h>

#include "message.h" 

#define PORT "12345"

using namespace std;

static int sockfd = 0;

void intHandler(int sigVal) {
	assert(sigVal == SIGINT);
	cout << "\ntalker: received SIGINT exiting" << endl;
	close(sockfd);
	exit(EXIT_SUCCESS);
}

void pipeHandler(int sigVal) {
	assert(sigVal == SIGPIPE);
	cout << "client closed connection" << endl;
	close(sockfd);
	exit(EXIT_SUCCESS);
}

int main() {
	signal(SIGINT, intHandler);
	signal(SIGPIPE, pipeHandler);

	struct addrinfo hints, *res;
	memset(&hints, 0, sizeof(hints));
	hints.ai_family = AF_INET;
	hints.ai_socktype = SOCK_DGRAM;

	int rv = getaddrinfo(NULL, PORT, &hints, &res);
	if (rv != 0) {
		cerr << "getaddrinfo: " << gai_strerror(rv) << endl;
	}

	int sockfd;
	struct addrinfo *p;
	for (p=res; p!=NULL; p=p->ai_next) {
		if ((sockfd = socket(p->ai_family, p->ai_socktype, p->ai_protocol)) == -1) {
			perror("talker socket");
			continue;
		}
		break;
	}
	if (p == NULL) {
		cerr << "talker failed to bind" << endl;
		exit(EXIT_FAILURE);
	}
	
    struct spike msg;
    int Nruns = 30;
    int Nsends = 1000000;
	int bytes_sent, bytes_rem;
	struct timeval start, finish, diff;
    for (int j=0; j<Nruns; j++) {
	    gettimeofday(&start, NULL);
        for (int i=0; i<Nsends; i++) {
            msg.t = 1.4;
            msg.lyr_z = 0;
            msg.x = 16;
            msg.y = 17;

	    	bytes_rem = sizeof(msg);
	    	while (bytes_rem > 0) {
	    		bytes_sent = sendto(sockfd, &msg, bytes_rem, 0, 
                                    (sockaddr *)p->ai_addr, p->ai_addrlen);
	    		if (bytes_sent == -1) {
	    			perror("talker sendto");
	    			close(sockfd);
	    			exit(EXIT_FAILURE);
	    		}
	    		// cout << bytes_sent << " bytes sent" << endl;
	    		bytes_rem -= bytes_sent;
	    	}
	    	if (bytes_rem != 0) {
	    		cerr << "transmition error" << endl;
	    	}
	    }
        
	    gettimeofday(&finish, NULL);
        timersub(&finish, &start, &diff);
	    cout << Nsends << " sends took " << diff.tv_sec << ".";
	    cout << setw(6) << setfill('0') << diff.tv_usec  << "s" << endl;
    }

	close(sockfd);
	exit(EXIT_SUCCESS);
}
