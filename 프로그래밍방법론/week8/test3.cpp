#include <iostream>
#include <string>

class Person {
private:
    std::string name;
    int age;

public:
    Person(const std::string& name, int age) : name(name), age(age) {}

    void display() const {
        std::cout << "Name: " << name << ", Age: " << age << std::endl;
    }
};

class Employee {
private:
    int salary;

public:
    Employee(int salary) : salary(salary) {}

    void showSalary() const {
        std::cout << "Salary: " << salary << " won" << std::endl;
    }
};

class Student {
private:
    int studentID;

public:
    Student(int studentID) : studentID(studentID) {}

    void showStudentID() const {
        std::cout << "Student ID: " << studentID << std::endl;
    }
};

class WorkingStudent : public Person, public Employee, public Student {
public:
    WorkingStudent(const std::string& name, int age, int salary, int studentID)
        : Person(name, age), Employee(salary), Student(studentID) {}

    void display() const {
        Person::display();
        showSalary();
        showStudentID();
    }
};

int main() {
    WorkingStudent student1("Jun", 23, 100, 20224531);
    
    student1.display();  

    return 0;
}
