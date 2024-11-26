#include <iostream>
#include <string>
using namespace std;

int main() {
	string str("C++ is ");
	string lang("a powerful language");

	str.append(lang, 0, 10);

	cout << str << endl;

	return 0;
}
