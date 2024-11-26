#include <iostream>
#include <string>
using namespace std;

int main() 
{
    string str1, str2;

    cout << "Enter the first string: ";
    getline(cin, str1);  

    cout << "Enter the second string: ";
    getline(cin, str2); 

    // compare() 함수로 문자열 비교
    int result = str1.compare(str2);

    // 출력
    if (result < 0) {
        cout << "str1 is less than str2" << endl;
    }
    else if (result == 0) {
        cout << "str1 is equal to str2" << endl;
    }
    else {
        cout << "str1 is greater than str2" << endl;
    }

    return 0;
}
