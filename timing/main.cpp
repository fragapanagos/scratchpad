#include <iostream>
#include <iomanip>
#include <time.h>

using namespace std;

int main(int argc, char *argv[]) {
	struct timespec t;
	clock_getres(CLOCK_REALTIME, &t);
	cout << "CLOCK_REALTIME resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_REALTIME_COARSE, &t);
	cout << "CLOCK_REALTIME_COARSE resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_MONOTONIC, &t);
	cout << "CLOCK_MONOTONIC resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_MONOTONIC_COARSE, &t);
	cout << "CLOCK_MONOTONIC_COARSE resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_MONOTONIC_RAW, &t);
	cout << "CLOCK_MONOTONIC_RAW resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_BOOTTIME, &t);
	cout << "CLOCK_BOOTTIME resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_PROCESS_CPUTIME_ID, &t);
	cout << "CLOCK_PROCESS_CPUTIME_ID resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

	clock_getres(CLOCK_THREAD_CPUTIME_ID, &t);
	cout << "CLOCK_THREAD_CPUTIME_ID resolution: " << t.tv_sec << ".";
	cout << setw(9) << setfill('0') << t.tv_nsec << "s" << endl;

    return 0;
}
