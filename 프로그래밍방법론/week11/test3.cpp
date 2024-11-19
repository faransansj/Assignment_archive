#include <iostream>
using namespace std;

// Employee class 
class Employee
{
public:
    virtual void work() = 0;
    virtual ~Employee() {}
};

// manager class 
class Manager : public Employee
{
public:
    // work() overriding
    void work() override
    {
        cout << "manager" << endl;
    }
};

// engineer class 
class Engineer : public Employee {
public:
    // work() overriding 
    void work() override {
        cout << "engineer" << endl;
    }
};

int main() {
    Employee* emp;
    Manager man;
    Engineer eng;

    //manager
    emp = &man;
    emp->work();

    //engineer 
    emp = &eng;
    emp->work();

    return 0;
}
