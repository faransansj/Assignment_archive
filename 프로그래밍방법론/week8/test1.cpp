#include <iostream>
#include <string>

class Person 
{
protected:
    std::string name;
    int age;

public:
    Person(const std::string& name, int age) : name(name), age(age) {}

    virtual void display() const {
        std::cout << "Name: " << name << ", Age: " << age;
    }
};

class Student : public Person 
{
private:
    std::string studentID;

public:
    Student(const std::string& name, int age, const std::string& studentID)
        : Person(name, age), studentID(studentID) {}

    void display() const override 
    {
        Person::display(); 
        std::cout << ", Student ID: " << studentID << std::endl;
    }
};

int main() {
    Student jun("seungjun",23,"20224531");
    jun.display(); 

    return 0;
}
