#include <iostream>

class person 
{
public:
    person() 
    {
        std::cout << "person is created" << std::endl;
    }
};
class employee:person
{
public:
    employee()
    {
        std::cout << "employee is created" << std::endl;
    }
};


int main() 
{
    employee test;

    return 0;
}
