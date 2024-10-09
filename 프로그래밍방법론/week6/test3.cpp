#include <iostream>
#include <vector>
using namespace std;

void main() 
{
    vector<int> numbers; 
    
    // input vector nums 
    for (int i = 0; i < 5; i++)
    {
        int num;
        cout << "input num : " << endl;
        cin >> num;
        numbers.push_back(num);
    }

    // print vector nums
    for (int i = 0; i < numbers.size(); i++) 
    {
        cout << numbers[i];
    }
    return 0;
}
