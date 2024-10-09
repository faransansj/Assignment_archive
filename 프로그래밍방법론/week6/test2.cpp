#include <iostream>
#include <vector>
using namespace std;


void main()
{
	int array[10];
	for (int i = 0; i < 10; i++)
	{
		int k;
		cout << "input num : ";
		cin >> k;

		array[i] = k;
	}

	int element_num[10];
	int count,


	//search same num
    for (int i = 0; i < SIZE; ++i) {
        bool isDuplicate = false;

        for (int j = 0; j < uniqueCount; ++j) {
            if (numbers[i] == unique[j]) {
                isDuplicate = true;
                break;
            }
        }

        if (!isDuplicate) {
            unique[uniqueCount] = numbers[i];
            uniqueCount++;
        }
    }

    std::cout << "unique array : ";
    for (int i = 0; i < uniqueCount; ++i) 
    {std::cout << unique[i] << " ";}
    std::cout << std::endl;

    return 0;
}