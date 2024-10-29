#include <iostream>

class person
{
private:
	string name;
	int age;

public:
	display()
	{
		std::cout << "name : " << name << "age : " << age << std::endl;
	}
};

class employee
{
public:
	void display()
	{
		std::cout << "fly bird" << std::endl;
	}
};

class student
{
public:
	void swim()
	{
		std::cout << "swim fish" << std::endl;
	}
};

class workingstudent : public person, public employee, public student
{
public:
	void swim() 
	{
		fish::swim();  
	}
};


void main()
{
	penguin pororo;
	pororo.swim();
}