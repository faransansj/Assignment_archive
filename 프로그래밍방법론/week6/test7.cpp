#include <iostream>

using namespace std;

int main()
{
    int array[3][3];

    // input num
    cout << "3x3 정수 배열의 요소를 입력하세요:\n";
    for (int i = 0; i < 3; i++)
    {
        for (int j = 0; j < 3; j++)
        {
            cout << "array[" << i << "][" << j << "] : ";
            cin >> array[i][j];
        }
    }

    // print array 
    cout << "입력한 3x3 정수 배열:\n";
        for (int i = 0; i < 3; i++)
        {
            for (int j = 0; j < 3; j++)
            {
                cout << array[i][j] << " ";
            }
            cout << endl;
        }
    return 0;
    }
