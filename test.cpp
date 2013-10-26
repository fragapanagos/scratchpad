#include <iostream>
#include <vector>
#include <cstdlib>

using namespace std;

class A{
public:
	A(int x) { x_ = x; }
	~A() {}
	inline int getX() { return x_; }
private:
	int x_;
};

int main()
{
	vector<A *> x;
	for (int i=0; i<10; i++) {
		x.push_back(new A(i));
	}

	for (vector<A *>::iterator it = x.begin(); it != x.end(); ++it) {
		cout << (*it)->getX() << ' ';
	}
	cout << endl;


	for (vector<A *>::iterator it = x.begin(); it != x.end(); ++it) {
		delete *it;
	}
	x.clear();

	cout << "x cleared" << endl;
	for (vector<A *>::iterator it = x.begin(); it != x.end(); ++it) {
		cout << (*it)->getX() << ' ';
	}
	cout << endl;

	return 0;
}
