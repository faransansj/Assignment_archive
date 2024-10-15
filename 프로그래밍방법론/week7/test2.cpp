#include <iostream>
#include <string>
using namespace std;

class BankAccount
{
private:
	string name;
	int pw,balance;

public:
	member(string memname, int mempw ,int membalance)
		: name(memname), pw(mempw), balance(membalance) {}

	// set info 
	void setname(string name)
	{name = memname;}
	void setbalance(int balance)
	{balance = membalance;}
	
	// in,out money
	void inMoney(int val)
	{

	}

	void outMoney(int val)
	{

	}


	// display info 
	void info()
	{cout << name << "´ÔÀÇ ÀÜ°í : " << balance << " ¿ø ÀÔ´Ï´Ù." << endl;}
}





//private:
//	string name;
//	int id, salary;
//
//public:
//	Employee(string empName, int empId, int empSalary)
//		: name(empName), id(empId), salary(empSalary) {}
//
//	//set info 
	//void setName(string empName)
//	{
//		name = empName;
//	}
//	void setSalary(int empSalary)
//	{
//		salary = empSalary;
//	}
//	//display info 
//	void info()
//	{
//		cout << "name : " << name << " ID : " << id << " salary : " << salary << " $ " << endl;
//	}

};

int main()
{
	BankAccount man1("Lee", 1234, 200);
	BankAccount man2("Kim", 5678, 100);

	man1.info();
	man2.info();
}