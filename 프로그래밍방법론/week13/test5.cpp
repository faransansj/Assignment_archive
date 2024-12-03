#include <iostream>
#include <stack>

using namespace std;

int main() {
	stack<int> myStack;
	// 스택에 데이터 추가
	myStack.push(10);
	myStack.push(20);
	myStack.push(30);

	// 스택빌때 까지 계속 팝
	while(!myStack.empty())
	{
		cout << myStack.top() << endl;
		myStack.pop();
	}
}
