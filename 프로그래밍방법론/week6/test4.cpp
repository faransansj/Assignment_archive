#include <iostream>
#include <vector>
using namespace std;

int main()
{
    vector<int> numbers;

    // input vector nums 
    for (int i = 0; i < 10; i++)
    {
        int num;
        cout << "input num : ";
        cin >> num;
        numbers.push_back(num);
    }

    // print even vector nums
    for (int i = 0; i < numbers.size(); i++)
    {   
        if (numbers[i] % 2 == 0)
        {cout << numbers[i] << " ";}
    }
    return 0;
}
