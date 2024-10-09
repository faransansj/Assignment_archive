#include <iostream>
#include <vector>
using namespace std;


void main()
{
	int array[5];
	for (int i = 0; i < 5; i++)
	{
		int k;
		cout << "input num : ";
		cin >> k;

		array[i] = k;
	}

	//search max num
	int max_num = array[0];
	for (int i = 1; i < 5; i++)
	{
		if (max_num < array[i])
		{max_num = array[i];}
	}
	cout << "max_num : " << max_num;
}