#include <iostream>
#include <string>
using namespace std;

class Employee 
{
private:
	string name;
	int id, salary;
	
public:
	Employee(string empName, int empId, empSalary)
		: name(empName), id(empId), salary(empSalary) {}

	//set info 
	void setName(string empName) 
	{name = empName;}
	void setSalary(int empSalary) 
	{salary = empSalary;}
	//display info 
	void info()
	{cout << "name : " << name << "ID : " << id << "salary : " << salary << endl;}

};

int main() 
{
	Employee man1("Lee", 1234, 200);
	Employee man2("Kim", 5678, 100);

	man1.info();
	man2.info();
}